param(
    [string]$Telemetry = "logs\\clerk_monitor\\035\\telemetry.jsonl",
    [string]$Out = "exchange\\reports\\inbox\\order-2025-10-16-035-result.json",
    [int]$CapsOpsPerMin = 3,
    [int]$CapsOpsPerOrder = 6,
    [int]$CapsOpsPerDay = 60,
    [string]$OrderId = "035",
    [string]$StartedAt = "",
    [string]$ExpectedEndAt = ""
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

if (-not (Test-Path -LiteralPath $Telemetry)) {
    Write-Error "Telemetry file not found: $Telemetry"
    exit 1
}

# Read JSONL telemetry lines safely
$lines = Get-Content -LiteralPath $Telemetry -ErrorAction Stop
$records = @()
foreach ($line in $lines) {
    if ([string]::IsNullOrWhiteSpace($line)) { continue }
    try {
        $obj = $line | ConvertFrom-Json -ErrorAction Stop
        if ($null -ne $obj -and $obj.PSObject.Properties.Name -contains 'metric') {
            $records += $obj
        }
    } catch {
        Write-Warning "Skipping non-JSON or malformed line: $line"
    }
}

$sampleCount = $records.Count
$firstTs = ($records | Select-Object -ExpandProperty timestamp -ErrorAction SilentlyContinue | Sort-Object | Select-Object -First 1)
$lastTs  = ($records | Select-Object -ExpandProperty timestamp -ErrorAction SilentlyContinue | Sort-Object | Select-Object -Last 1)

# Extract metric series
$opsPerMinValues = @()
$opsPerMinPoints = @()
$violationsValues = @()
$violationsPoints = @()
$darkValues = @()
$darkPoints = @()
$opsTotalValues = @()

foreach ($r in $records) {
    switch ($r.metric) {
        'ops_per_min' {
            $opsPerMinValues += [double]$r.value
            $opsPerMinPoints += $r
        }
        'policy_violations' {
            $violationsValues += [double]$r.value
            $violationsPoints += $r
        }
        'dark_signs' {
            $darkValues += [double]$r.value
            $darkPoints += $r
        }
        'ops_total' {
            $opsTotalValues += [double]$r.value
        }
    }
}

function Measure-Average([double[]]$vals) {
    if ($null -eq $vals -or $vals.Count -eq 0) { return $null }
    return ($vals | Measure-Object -Average).Average
}

function Measure-Max([double[]]$vals) {
    if ($null -eq $vals -or $vals.Count -eq 0) { return $null }
    return ($vals | Measure-Object -Maximum).Maximum
}

$avgOps = Measure-Average $opsPerMinValues
$maxOps = Measure-Max $opsPerMinValues
$sumViol = if ($violationsValues.Count -gt 0) { [double]($violationsValues | Measure-Object -Sum).Sum } else { 0 }
$sumDark = if ($darkValues.Count -gt 0) { [double]($darkValues | Measure-Object -Sum).Sum } else { 0 }

# Identify breaches over the run
$breaches = @()
foreach ($p in $violationsPoints) {
    if ([double]$p.value -gt 0) {
        $breaches += [ordered]@{ timestamp = $p.timestamp; metric = $p.metric; value = [double]$p.value; reason = 'policy_violations>0' }
    }
}
foreach ($p in $darkPoints) {
    if ([double]$p.value -gt 0) {
        $breaches += [ordered]@{ timestamp = $p.timestamp; metric = $p.metric; value = [double]$p.value; reason = 'dark_signs>0' }
    }
}
foreach ($p in $opsPerMinPoints) {
    if ([double]$p.value -gt $CapsOpsPerMin) {
        $breaches += [ordered]@{ timestamp = $p.timestamp; metric = $p.metric; value = [double]$p.value; reason = "ops_per_min>$CapsOpsPerMin" }
    }
}

$status = if ($breaches.Count -gt 0) { 'abort' } else { 'success' }
$recommendation = if ($status -eq 'abort') { 'rollback' } else { 'promote' }

$withinOpsPerMin = $null
if ($null -ne $maxOps) { $withinOpsPerMin = ([double]$maxOps -le [double]$CapsOpsPerMin) }

$opsTotal = $null
if ($opsTotalValues.Count -gt 0) {
    # Use the maximum observed ops_total as the run total if present
    $opsTotal = ($opsTotalValues | Measure-Object -Maximum).Maximum
}

$result = [ordered]@{
    order_id = $OrderId
    started_at = $StartedAt
    expected_end_at = $ExpectedEndAt
    status = $status
    totals = [ordered]@{
        samples = $sampleCount
        ops_total = $opsTotal
    }
    avg_ops_per_min = if ($null -ne $avgOps) { [math]::Round($avgOps, 3) } else { $null }
    max_ops_per_min = $maxOps
    violations = $sumViol
    dark_signs = $sumDark
    alerts = $breaches
    watcher_state = [ordered]@{
        first_timestamp = $firstTs
        last_timestamp = $lastTs
        caps = [ordered]@{
            ops_per_min = $CapsOpsPerMin
            ops_per_order = $CapsOpsPerOrder
            ops_per_day = $CapsOpsPerDay
        }
        adherence = [ordered]@{
            within_ops_per_min = $withinOpsPerMin
            within_ops_per_order = $null  # not derivable from current telemetry
            within_ops_per_day = $null    # not derivable from current telemetry
        }
    }
    recommendation = $recommendation
}

# Ensure output directory exists
$outDir = Split-Path -Parent $Out
if (-not (Test-Path -LiteralPath $outDir)) { New-Item -ItemType Directory -Path $outDir -Force | Out-Null }

$json = $result | ConvertTo-Json -Depth 8
Set-Content -LiteralPath $Out -Value $json -Encoding UTF8
Write-Host "Wrote summary to $Out" -ForegroundColor Green

