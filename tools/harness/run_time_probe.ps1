<#
.SYNOPSIS
  Start the KCD test instance with only krs_timeprobe, stamp every KRS_TP log line with the real time it appeared, stop when the
  probe ends (or after the timeout) and restore mod_order.txt.

.PARAMETER GameDir     KCD folder (the replica); Mods\krs_timeprobe must exist (tools/harness/build_timeprobe.py)
.PARAMETER OutFile     stamped lines: "<ISO time with ms>  <log line>"
.PARAMETER TimeoutSec  total wait including the time until someone presses Continue (default 1500)

  The person has to press Continue in the game window; nothing is clicked or typed by this script.
#>
param(
  [Parameter(Mandatory = $true)][string]$GameDir,
  [string]$OutFile = (Join-Path $PSScriptRoot 'timeprobe_result.log'),
  [int]$TimeoutSec = 1500
)

$exe = Join-Path $GameDir 'Bin\win64releasedll\kingdomcome.exe'
$log = Join-Path $GameDir 'kcd.log'
if (-not (Test-Path $exe)) { throw "not found: $exe" }
if (-not (Test-Path (Join-Path $GameDir 'Mods\krs_timeprobe'))) { throw 'run build_timeprobe.py first' }
if (Get-Process -Name 'kingdomcome' -ErrorAction SilentlyContinue) { throw 'a KCD process is already running; close it first' }
if (-not (Get-Process -Name 'steam' -ErrorAction SilentlyContinue)) { Write-Warning 'Steam is not running; the game may refuse to start' }

$orderFile = Join-Path $GameDir 'Mods\mod_order.txt'
$orderBackup = Join-Path $GameDir 'Mods\mod_order.txt.krs_backup'
if (Test-Path $orderBackup) { throw "$orderBackup exists: a previous run did not restore mod_order.txt. Restore it by hand first." }
Copy-Item $orderFile $orderBackup
try {
  Set-Content -Path $orderFile -Value 'krs_timeprobe' -Encoding ASCII
  Set-Content -Path $OutFile -Value '' -Encoding UTF8
  $started = Get-Date
  $p = Start-Process -FilePath $exe -WorkingDirectory $GameDir -PassThru
  Write-Host "started PID $($p.Id) at $($started.ToString('HH:mm:ss'))"
  $seen = 0
  $done = $false
  while (((Get-Date) - $started).TotalSeconds -lt $TimeoutSec) {
    Start-Sleep -Milliseconds 400
    if ((Test-Path $log) -and ((Get-Item $log).LastWriteTime -ge $started.AddSeconds(-2))) {
      try {
        $fs = [System.IO.File]::Open($log, 'Open', 'Read', 'ReadWrite')
        $sr = New-Object System.IO.StreamReader($fs)
        $text = $sr.ReadToEnd(); $sr.Close(); $fs.Close()
      } catch { continue }
      $lines = $text -split "`r?`n"
      if ($lines.Count -lt $seen) { $seen = 0 }
      $now = (Get-Date).ToString('yyyy-MM-ddTHH:mm:ss.fff')
      $new = @()
      for ($i = $seen; $i -lt $lines.Count; $i++) {
        if ($lines[$i] -match 'KRS_TP|Lua Error|Script error') { $new += "$now  $($lines[$i])" }
        if ($lines[$i] -match 'KRS_TP end') { $done = $true }
      }
      $seen = $lines.Count
      if ($new.Count) { Add-Content -Path $OutFile -Value $new -Encoding UTF8 }
    }
    if ($done -or $p.HasExited) { break }
  }
  if ($done) { Start-Sleep -Seconds 8 }
  if (-not $p.HasExited) { Write-Warning 'game still running; stopping it'; Stop-Process -Id $p.Id -Force; Start-Sleep -Seconds 2 }
  for ($i = 0; $i -lt 30 -and (Get-Process -Name 'kingdomcome' -ErrorAction SilentlyContinue); $i++) { Start-Sleep -Seconds 1 }
  Write-Host ("finished in {0:N0}s, probe done={1} -> {2}" -f ((Get-Date) - $started).TotalSeconds, $done, $OutFile)
} finally {
  Copy-Item $orderBackup $orderFile -Force
  Remove-Item $orderBackup -Force
  Write-Host 'mod_order.txt restored'
}
