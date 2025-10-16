param(
  [string]$ConfigPath = 'exchange/config.json',
  [switch]$WhatIf
)

$ErrorActionPreference = 'Stop'
if (-not (Test-Path -LiteralPath $ConfigPath)) {
  Write-Error "Config not found: $ConfigPath (copy exchange/config.example.json to exchange/config.json and edit)"
}

$cfg = Get-Content -Raw -LiteralPath $ConfigPath | ConvertFrom-Json -AsHashtable
if ($cfg['mode'] -ne 'local') { Write-Error "Only mode=local is supported in this script." }
$upRoot = $cfg['upstream_root']
if (-not $upRoot -or -not (Test-Path -LiteralPath $upRoot)) { Write-Error "Upstream root missing or not found: $upRoot" }

function Sync-Tree([string]$src, [string]$dst){
  if (-not (Test-Path -LiteralPath $src)) { return }
  if (-not (Test-Path -LiteralPath $dst)) { New-Item -ItemType Directory -Force -Path $dst | Out-Null }
  Get-ChildItem -LiteralPath $src -File -Filter *.json | ForEach-Object {
    $to = Join-Path $dst $_.Name
    if ($WhatIf) { Write-Host "[WhatIf] Pull $($_.FullName) -> $to" }
    else { Copy-Item -LiteralPath $_.FullName -Destination $to -Force }
  }
}

$map = $cfg['mapping']
$local = $map['local']
$up = $map['upstream']

# Pull common upstream inbox/logged areas down to local mirror
Sync-Tree (Join-Path $upRoot $up['orders_pending']) $local['orders_pending']
Sync-Tree (Join-Path $upRoot $up['reports_inbox']) $local['reports_inbox']
Sync-Tree (Join-Path $upRoot $up['acks_pending']) $local['acks_pending']
Sync-Tree (Join-Path $upRoot $up['acks_logged']) $local['acks_logged']

Write-Host "Pulled inbox/logged from upstream." -ForegroundColor Green

