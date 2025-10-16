param(
  [string]$Out = 'logs/clerk_monitor/035/telemetry.jsonl',
  [int]$PolicyViolations = 0,
  [int]$OpsPerMin = 0,
  [int]$DarkSigns = 0,
  [string]$Agent
)

$ErrorActionPreference = 'Stop'

$dir = Split-Path -Parent $Out
if ($dir -and -not (Test-Path $dir)) {
  New-Item -ItemType Directory -Force -Path $dir | Out-Null
}

$ts = [DateTime]::UtcNow.ToString('o')

# Base record fields
$base = [hashtable]@{ timestamp = $ts }
if ($Agent) { $base['agent'] = $Agent }

function New-Rec($metric, $value) {
  $h = $base.Clone()
  $h['metric'] = $metric
  $h['value'] = $value
  return ($h | ConvertTo-Json -Compress)
}

$lines = @()
$lines += (New-Rec 'policy_violations' $PolicyViolations)
$lines += (New-Rec 'ops_per_min' $OpsPerMin)
$lines += (New-Rec 'dark_signs' $DarkSigns)

Add-Content -Path $Out -Value ($lines -join "`n") -Encoding UTF8
if ($Agent) {
  Write-Host "Appended sample(s) to $Out at $ts (Agent: $Agent)"
} else {
  Write-Host "Appended sample(s) to $Out at $ts"
}
