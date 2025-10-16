param(
  [string]$Out = 'logs/clerk_monitor/035/telemetry.jsonl',
  [int]$PolicyViolations = 0,
  [int]$OpsPerMin = 0,
  [int]$DarkSigns = 0
)

$ErrorActionPreference = 'Stop'

$dir = Split-Path -Parent $Out
if ($dir -and -not (Test-Path $dir)) {
  New-Item -ItemType Directory -Force -Path $dir | Out-Null
}

$ts = [DateTime]::UtcNow.ToString('o')
$lines = @()
$lines += (@{ timestamp = $ts; metric = 'policy_violations'; value = $PolicyViolations } | ConvertTo-Json -Compress)
$lines += (@{ timestamp = $ts; metric = 'ops_per_min'; value = $OpsPerMin } | ConvertTo-Json -Compress)
$lines += (@{ timestamp = $ts; metric = 'dark_signs'; value = $DarkSigns } | ConvertTo-Json -Compress)

Add-Content -Path $Out -Value ($lines -join "`n") -Encoding UTF8
Write-Host "Appended sample(s) to $Out at $ts"

