<#
.SYNOPSIS
  Start the KCD test instance, wait for the KRS test harness to finish, collect its log lines, stop the game.

.PARAMETER GameDir   KCD folder that contains Bin\win64releasedll\kingdomcome.exe and Mods\krs_harness
.PARAMETER OutFile   where to write the extracted log (default: harness_result.log next to this script)
.PARAMETER TimeoutSec  how long to wait for the harness before the game is stopped (default 240)
.PARAMETER Harness  folder name of the test mod that must exist in Mods (krs_harness or krs_gate)
.PARAMETER Mods  mods to load, in order (default: only krs_harness). The game only loads mods listed in
                 Mods\mod_order.txt; this script backs the file up and always restores it afterwards.
                 Pass the full list (e.g. 'Cheat','krs_harness') to test together with other mods.

  Nothing is clicked or typed; the harness script (Scripts\Startup\krs_harness.lua) runs itself and quits the game.
  The game is only stopped by this script if the harness did not finish within the timeout.
#>
param(
  [Parameter(Mandatory = $true)][string]$GameDir,
  [string]$OutFile = (Join-Path $PSScriptRoot 'harness_result.log'),
  [int]$TimeoutSec = 240,
  [string[]]$Mods = @('krs_harness'),
  [string]$Harness = 'krs_harness'
)

$Mods = @($Mods | ForEach-Object { $_ -split ',' } | Where-Object { $_ })   # -File passes a,b as one string
$exe = Join-Path $GameDir 'Bin\win64releasedll\kingdomcome.exe'
$log = Join-Path $GameDir 'kcd.log'
if (-not (Test-Path $exe)) { throw "not found: $exe" }
if (-not (Test-Path (Join-Path $GameDir "Mods\$Harness"))) { throw "run build_harness.py or build_gate.py first (Mods\$Harness is missing)" }
if (Get-Process -Name 'kingdomcome' -ErrorAction SilentlyContinue) { throw 'a KCD process is already running; close it first' }
if (-not (Get-Process -Name 'steam' -ErrorAction SilentlyContinue)) { Write-Warning 'Steam is not running; the game may refuse to start' }

$orderFile = Join-Path $GameDir 'Mods\mod_order.txt'
$orderBackup = Join-Path $GameDir 'Mods\mod_order.txt.krs_backup'
if (Test-Path $orderBackup) { throw "$orderBackup exists: a previous run did not restore mod_order.txt. Restore it by hand first." }
Copy-Item $orderFile $orderBackup
try {
Set-Content -Path $orderFile -Value ($Mods -join "`r`n") -Encoding ASCII
$started = Get-Date
$p = Start-Process -FilePath $exe -WorkingDirectory $GameDir -PassThru
Write-Host "started PID $($p.Id)"

function Read-LogLines {
  if (-not (Test-Path $log)) { return @() }
  try {
    $fs = [System.IO.File]::Open($log, 'Open', 'Read', 'ReadWrite')
    $sr = New-Object System.IO.StreamReader($fs)
    $text = $sr.ReadToEnd(); $sr.Close(); $fs.Close()
    return $text -split "`r?`n"
  } catch { return @() }
}

$done = $false
while (((Get-Date) - $started).TotalSeconds -lt $TimeoutSec) {
  Start-Sleep -Seconds 3
  if ($p.HasExited) { break }
  # only trust a log that was (re)written after this launch
  if ((Test-Path $log) -and ((Get-Item $log).LastWriteTime -ge $started)) {
    if ((Read-LogLines | Select-String -SimpleMatch 'KRS_HARNESS end' -Quiet)) { $done = $true; break }
  }
}
if ($done) { Start-Sleep -Seconds 8 }                 # let the game quit by itself
if (-not $p.HasExited) {
  Write-Warning 'game still running; stopping it'
  Stop-Process -Id $p.Id -Force
  Start-Sleep -Seconds 2
}
# wait until every KCD process is gone so a following run can start
for ($i = 0; $i -lt 30 -and (Get-Process -Name 'kingdomcome' -ErrorAction SilentlyContinue); $i++) { Start-Sleep -Seconds 1 }
$lines = Read-LogLines
$keep = $lines | Where-Object { $_ -match 'KRS_HARNESS|KRS_GATE|krs_harness|krs_gate|krs_h[0-9]|no such rpg constant|Setting RPG constant|is patched by|\[Mod\]|Lua Error|food__|ocalization|text__|Failed to open|[Mm]anifest|Loading level|[Ss]cript error|error in' }
$keep | Set-Content -Path $OutFile -Encoding UTF8
Write-Host ("finished in {0:N0}s, harness done={1}, {2} lines -> {3}" -f ((Get-Date) - $started).TotalSeconds, $done, $keep.Count, $OutFile)
} finally {
  Copy-Item $orderBackup $orderFile -Force
  Remove-Item $orderBackup -Force
  Write-Host 'mod_order.txt restored'
}
