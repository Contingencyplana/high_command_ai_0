Param(
  [string[]]$Workspaces = @(
    "C:\Users\Admin\toyfoundry_ai_0",
    "C:\Users\Admin\toysoldiers_ai_0"
  )
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

foreach ($ws in $Workspaces) {
  if (-not (Test-Path $ws)) { Write-Warning "[field] Workspace not found: $ws"; continue }

  $exchange = Join-Path $ws 'exchange'
  if (-not (Test-Path $exchange)) { Write-Warning "[field] Exchange missing in $ws"; continue }

  Push-Location $exchange
  try {
    git fetch origin | Out-Host
    git checkout -B main origin/main | Out-Host
    git pull --ff-only | Out-Host

    # Ensure watcher present
    $tools = Join-Path $ws 'tools'
    if (-not (Test-Path $tools)) { New-Item -ItemType Directory -Force -Path $tools | Out-Null }
    $attached = Join-Path $exchange 'attachments\tools\exchange_watcher.py'
    $localWatcher = Join-Path $tools 'exchange_watcher.py'
    if (Test-Path $attached) { Copy-Item $attached $localWatcher -Force }
  }
  finally { Pop-Location }

  # Run watcher from workspace root
  Push-Location $ws
  try { python -m tools.exchange_watcher | Out-Host } catch { Write-Warning "[field] Watcher failed in $ws: $_" }
  finally { Pop-Location }
}

