Param(
  [string[]]$Workspaces = @(
    "C:\Users\Admin\toyfoundry_ai_0",
    "C:\Users\Admin\toysoldiers_ai_0"
  ),
  [switch]$AckReceived
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

    if ($AckReceived) {
      # Mark pending ACKs as received
      $pendingAckDir = Join-Path $exchange 'acknowledgements\pending'
      if (Test-Path $pendingAckDir) {
        $changed = $false
        Get-ChildItem -Path $pendingAckDir -Filter '*.json' -File | ForEach-Object {
          $p = $_.FullName
          try {
            $ack = Get-Content $p -Raw | ConvertFrom-Json
          } catch {
            Write-Warning "[field] Unreadable ACK JSON: $p"
            return
          }
          if ($ack.status -ne 'received') {
            $ack.status = 'received'
            $ack.timestamp_requested = (Get-Date).ToUniversalTime().ToString('s') + 'Z'
            $ack | ConvertTo-Json -Depth 10 | Set-Content -Encoding UTF8 $p
            $changed = $true
          }
        }
        if ($changed) {
          git add acknowledgements/pending/*.json | Out-Host
          $nothingToCommit = $false
          try { git diff --cached --quiet; $nothingToCommit = $true } catch { $nothingToCommit = $false }
          if (-not $nothingToCommit) {
            git commit -m ("{0}: ACKs marked received" -f (Split-Path $ws -Leaf)) | Out-Host
            git push origin main | Out-Host
          }
        }
      }
    }
  }
  finally { Pop-Location }

  # Run watcher from workspace root
  Push-Location $ws
  try { python -m tools.exchange_watcher | Out-Host } catch { Write-Warning "[field] Watcher failed in $ws: $_" }
  finally { Pop-Location }
}
