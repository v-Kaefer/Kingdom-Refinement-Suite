# krs_skipcost changes

## 0.1.0 (2026-10-10)
- First module, built from the prototype in `tools/harness/skipcost/` (the scripts moved here; the harness builds a test copy from them).
- Charges hunger after a skip: awake rate x skipped hours x share by posture (standing 0.75, sitting 0.5, lying 0.5).
- Skips are found from long frames (about 0.25 s, normal 0.02 to 0.05 s) because the clock ratio changes with the hours and the last hour runs at the normal ratio.
- The kind comes from `player.player:IsLaying()` / `IsSitting()`, not from using a bed, so opening and cancelling a bed does not change the next Wait.
- Checked in game 1.9.8 with `krs_items`: Wait of 3.991 h cost 9.534 and Wait of 1.993 h cost 4.761 (rate 3.19 x hours x 0.75); the bar read back equal to the target. Not tested: a real sleep, a Wait sitting, reading, fainting.
