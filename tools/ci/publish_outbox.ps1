param(
  [string]$ConfigPath = 'exchange/config.json',
  [switch]$WhatIf
)

$ErrorActionPreference = 'Stop'
function Resolve-PathSafe([string]$p){ (Resolve-Path -LiteralPath $p -ErrorAction Stop).Path }

if (-not (Test-Path -LiteralPath $ConfigPath)) {
  Write-Error "Config not found: $ConfigPath (copy exchange/config.example.json to exchange/config.json and edit)"
}

$cfg = Get-Content -Raw -LiteralPath $ConfigPath | ConvertFrom-Json -AsHashtable
if ($cfg['mode'] -ne 'local') { Write-Error "Only mode=local is supported in this script." }
$upRoot = $cfg['upstream_root']
if (-not $upRoot -or -not (Test-Path -LiteralPath $upRoot)) { Write-Error "Upstream root missing or not found: $upRoot" }

function Copy-TreeJson([string]$src, [string]$dst){
  if (-not (Test-Path -LiteralPath $src)) { return }
  if (-not (Test-Path -LiteralPath $dst)) { New-Item -ItemType Directory -Force -Path $dst | Out-Null }
  Get-ChildItem -LiteralPath $src -File -Filter *.json | ForEach-Object {
    $to = Join-Path $dst $_.Name
    if ($WhatIf) {
      Write-Host "[WhatIf] Copy $($_.FullName) -> $to"
    } else {
      Copy-Item -LiteralPath $_.FullName -Destination $to -Force
    }
  }
}

$map = $cfg['mapping']
$local = $map['local']
$up = $map['upstream']

$localOrders = $local['orders_pending']
$localReports = $local['reports_inbox']

$upOrders = Join-Path $upRoot $up['orders_pending']
$upReports = Join-Path $upRoot $up['reports_inbox']

Write-Host "Publishing outbox → upstream" -ForegroundColor Cyan
Copy-TreeJson $localOrders $upOrders
Copy-TreeJson $localReports $upReports

Write-Host "Done." -ForegroundColor Green

