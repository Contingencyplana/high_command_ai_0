Param(
  [Parameter(Mandatory=$false)] [string] $CasesPath = "tools/ci/red_team/cases.json",
  [Parameter(Mandatory=$false)] [string] $OutputPath = "logs/red_team/results.jsonl",
  [Parameter(Mandatory=$false)] [string] $RepoRoot = ".",
  [switch] $List,
  [switch] $DryRun
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Write-ResultJson {
  param([string]$CaseId, [string]$Result, [string]$Reason, [string[]]$Guardrails)
  $obj = [ordered]@{
    ts = (Get-Date).ToString("o")
    case_id = $CaseId
    result = $Result
    reason = $Reason
    guardrails_touched = $Guardrails
  }
  $line = ($obj | ConvertTo-Json -Compress)
  $line
}

function Get-EmojiOutboxPath {
  param([string]$RepoRoot)
  $root = Resolve-Path -LiteralPath $RepoRoot | Select-Object -ExpandProperty Path
  return Join-Path $root "outbox/orders/emoji_runtime"
}

function Invoke-RT001-FarmLoopPressure {
  param([hashtable]$Case)
  if ($DryRun) {
    return Write-ResultJson -CaseId $Case.id -Result 'pass' -Reason 'dry-run' -Guardrails @('loot_governor','xp_rate_limit','economy_drift')
  }
  $log = Join-Path (Resolve-Path -LiteralPath $RepoRoot) 'logs/fun_guardrails/events.jsonl'
  if (-not (Test-Path -LiteralPath $log)) {
    return Write-ResultJson -CaseId $Case.id -Result 'fail' -Reason 'no guardrail events observed' -Guardrails @('loot_governor','xp_rate_limit')
  }
  $now = Get-Date
  $windowMinutes = 10
  $found = $false
  try {
    Get-Content -LiteralPath $log | ForEach-Object {
      $line = $_.Trim()
      if (-not $line) { return }
      try {
        $obj = $line | ConvertFrom-Json
        $ts = [DateTimeOffset]::Parse($obj.ts)
        if ($ts -lt ($now.AddMinutes(-$windowMinutes))) { return }
        foreach ($t in $obj.triggers) {
          if ($t.type -in @('xp_velocity','loot_units_per_payload','units_per_minute')) { $found = $true; break }
        }
      } catch { }
    }
  } catch { }
  if ($found) {
    return Write-ResultJson -CaseId $Case.id -Result 'pass' -Reason 'would-clamp events detected' -Guardrails @('loot_governor','xp_rate_limit')
  }
  return Write-ResultJson -CaseId $Case.id -Result 'fail' -Reason 'no would-clamp events detected in window' -Guardrails @('loot_governor','xp_rate_limit')
}

function Invoke-RT008-ReplayIdempotency {
  param([hashtable]$Case)
  $outbox = Get-EmojiOutboxPath -RepoRoot $RepoRoot
  if (-not (Test-Path -LiteralPath $outbox)) {
    return Write-ResultJson -CaseId $Case.id -Result 'pass' -Reason 'no outbox yet; no duplicates observed' -Guardrails @('idempotency','audit_log')
  }
  $files = Get-ChildItem -LiteralPath $outbox -Filter *.json -File -ErrorAction SilentlyContinue
  $seen = @{}
  $dupes = @()
  foreach ($f in $files) {
    try {
      $obj = Get-Content -LiteralPath $f.FullName -Raw | ConvertFrom-Json -ErrorAction Stop
      $batch = $obj.telemetry_stub.batch_id
      if ([string]::IsNullOrWhiteSpace($batch)) { continue }
      if ($seen.ContainsKey($batch)) { $dupes += $batch } else { $seen[$batch] = 1 }
    } catch { continue }
  }
  if ($dupes.Count -gt 0) {
    $uniq = ($dupes | Sort-Object -Unique)
    return Write-ResultJson -CaseId $Case.id -Result 'fail' -Reason ("duplicate batch_id: " + ($uniq -join ',')) -Guardrails @('idempotency','audit_log')
  }
  return Write-ResultJson -CaseId $Case.id -Result 'pass' -Reason 'no duplicate batch_id observed' -Guardrails @('idempotency','audit_log')
}

function Invoke-RedTeamCase {
  param([hashtable]$Case)
  # Stub implementation – replace with actual harness calls.
  $id = $Case.id
  $guardrails = @($Case.guardrails)
  switch ($id) {
    'RT-001' { return Invoke-RT001-FarmLoopPressure -Case $Case }
    'RT-008' { return Invoke-RT008-ReplayIdempotency -Case $Case }
    default {
      if ($DryRun) { return Write-ResultJson -CaseId $id -Result 'pass' -Reason 'dry-run' -Guardrails $guardrails }
      return Write-ResultJson -CaseId $id -Result 'fail' -Reason 'NotImplemented' -Guardrails $guardrails
    }
  }
}

if ($List) {
  if (Test-Path $CasesPath) {
    $cases = Get-Content $CasesPath | ConvertFrom-Json
    $cases | ForEach-Object { $_.id }
  } else {
    Write-Host "No cases file found at $CasesPath. Refer to tools/ci/red_team/RED_TEAM_CASES.md" -ForegroundColor Yellow
  }
  exit 0
}

New-Item -ItemType Directory -Force -Path (Split-Path $OutputPath) | Out-Null

if (-not (Test-Path $CasesPath)) {
  Write-Host "No cases file found at $CasesPath. Create it or generate from RED_TEAM_CASES.md." -ForegroundColor Yellow
  $summary = [ordered]@{ pass=0; fail=0; notes='no cases' }
  $summary | ConvertTo-Json -Compress | Set-Content -Path $OutputPath
  exit 0
}

$cases = Get-Content $CasesPath | ConvertFrom-Json
$pass = 0; $fail = 0; $lines = @()
foreach ($c in $cases) {
  $line = Invoke-RedTeamCase -Case $c
  $lines += $line
  $obj = $line | ConvertFrom-Json
  if ($obj.result -eq 'pass') { $pass++ } else { $fail++ }
}

$lines | Out-File -FilePath $OutputPath -Encoding utf8
$summary = [ordered]@{ pass=$pass; fail=$fail }
$summary | ConvertTo-Json -Compress | Write-Output

if ($fail -gt 0) { exit 1 } else { exit 0 }
