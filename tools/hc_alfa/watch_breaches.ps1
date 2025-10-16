param(
  [string]$Telemetry = 'logs\\clerk_monitor\\035\\telemetry.jsonl',
  [int]$CapsOpsPerMin = 3,
  [switch]$ShowAll
)

$ErrorActionPreference = 'Stop'
if (-not (Test-Path -LiteralPath $Telemetry)) {
  Write-Error "Telemetry not found: $Telemetry"
}

Get-Content -LiteralPath $Telemetry -Wait | ForEach-Object {
  $line = $_
  if ([string]::IsNullOrWhiteSpace($line)) { return }
  try {
    $o = $line | ConvertFrom-Json -ErrorAction Stop
  } catch {
    if ($ShowAll) { Write-Host "(skip) $line" -ForegroundColor Yellow }
    return
  }

  $isBreach = $false
  if ($o.metric -eq 'policy_violations' -and [double]$o.value -gt 0) { $isBreach = $true }
  elseif ($o.metric -eq 'dark_signs' -and [double]$o.value -gt 0) { $isBreach = $true }
  elseif ($o.metric -eq 'ops_per_min' -and [double]$o.value -gt $CapsOpsPerMin) { $isBreach = $true }

  if ($isBreach) {
    $agentFrag = if ($o.PSObject.Properties.Name -contains 'agent' -and $o.agent) { " Alfa $($o.agent)" } else { '' }
    Write-Host ("BREACH$agentFrag: " + $line) -ForegroundColor Red
  } elseif ($ShowAll) {
    Write-Host $line
  }
}
