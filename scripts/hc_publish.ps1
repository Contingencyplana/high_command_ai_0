Param(
  [string]$Message = "Exchange: publish changes",
  [switch]$Validate
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

# Resolve paths
$root = Split-Path -Parent $PSScriptRoot
$exchange = Join-Path $root 'exchange'
if (-not (Test-Path $exchange)) { Throw "Exchange not found at $exchange" }

Push-Location $exchange
try {
  if ($Validate) {
    $validator = Join-Path $root 'tools\exchange_validator.py'
    if (Test-Path $validator) { python $validator } else { Write-Host "[hc] Validator not found; skipping." }
  }

  git add -A
  $nothingToCommit = $false
  try { git diff --cached --quiet; $nothingToCommit = $true } catch { $nothingToCommit = $false }
  if ($nothingToCommit) {
    Write-Host "[hc] Nothing to commit."
  } else {
    git commit -m $Message | Out-Host
  }
  git push origin main | Out-Host
}
finally { Pop-Location }

