param(
  [string]$Agent,
  [switch]$All,
  [switch]$Force
)

$ErrorActionPreference = 'Stop'

function Confirm-Action($Prompt) {
  if ($Force) { return $true }
  $resp = Read-Host "$Prompt (Y/N)"
  return ($resp -match '^(y|yes)$')
}

if (-not (Confirm-Action "Abort order 035 now")) {
  Write-Host "Abort cancelled." -ForegroundColor Yellow
  exit 0
}

# 1) End/disable scheduled tasks if present
$taskNames = @()
if ($All) {
  $taskNames += (schtasks /Query /FO LIST 2>$null | Select-String 'TaskName:' | ForEach-Object { ($_ -split ':',2)[1].Trim() } | Where-Object { $_ -like 'ClerkMonitor035*' })
} elseif ($Agent) {
  $taskNames += "ClerkMonitor035-$Agent"
} else {
  $taskNames += "ClerkMonitor035"
}

foreach ($tn in ($taskNames | Select-Object -Unique)) {
  try { schtasks /End /TN $tn 2>$null | Out-Null } catch {}
  try { schtasks /Change /TN $tn /Disable 2>$null | Out-Null } catch {}
}

# 2) Kill any running sampler processes for 035 (optionally narrowed by Agent)
$wql = "SELECT ProcessId, CommandLine FROM Win32_Process"
Get-CimInstance -Query $wql | Where-Object {
  ($_ .CommandLine -like '*monitor_sample.ps1*') -and
  ($_ .CommandLine -like '*\\logs\\clerk_monitor\\035\\telemetry.jsonl*') -and
  ( -not $Agent -or $_.CommandLine -match [regex]::Escape($Agent) )
} | ForEach-Object {
  try { Stop-Process -Id $_.ProcessId -Force -ErrorAction Stop } catch {}
}

# 3) Snapshot current telemetry
$telemetry = 'logs\\clerk_monitor\\035\\telemetry.jsonl'
if (Test-Path -LiteralPath $telemetry) {
  $stamp = (Get-Date).ToString('yyyyMMdd-HHmmss')
  $snap = "logs\\clerk_monitor\\035\\telemetry_breach_snapshot-$stamp.jsonl"
  try { Get-Content -LiteralPath $telemetry | Set-Content -LiteralPath $snap -Encoding UTF8 } catch {}
  Write-Host "Saved snapshot: $snap" -ForegroundColor Cyan
}

Write-Host "Order 035 aborted." -ForegroundColor Red

