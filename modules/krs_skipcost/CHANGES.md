# krs_skipcost changes

## 0.1.2 (2026-10-11)
- The player is told what the skip cost, on screen, right after it: "Waited 2.0 h: hunger -5", "Slept 6.0 h: hunger -10 (you are hungry)", "Rested 3.0 h: hunger -5 (starving)". The game's own Wait and sleep dialogs predict no change in nourishment, so without this the drop is a surprise. Sent through `Game.ShowNotification` with plain English text (no localization key; the text carries numbers), falling back to `Game.SendInfoText`; both exist in the game's scripts. `KRS_SC_CFG.notify = 0` turns it off. **Not seen on screen yet**: whether the game shows a text that is not a localization key is to be confirmed in the game.
- Author's decisions (11 Oct 2026): keep the KRS Items hunger rate as it is; sitting costs 50%; the hunger-reaching-0 question is answered by the warning, not by a floor.
- 33 checks in `tools/harness/skipcost/test_skipcost.py` (6 new: the three messages, fallback to the info line, no `Game` table, `notify = 0`).

## 0.1.1 (2026-10-11)
- R1: a run of long frames is a skip only if the world clock ran at 100 world seconds or more per real second (`MIN_SKIP_RATE`; normal play is 15, a skip hundreds). Under about 6 frames per second normal play was read as a Wait and charged. Checked while the episode runs (dropped after 3 real seconds under the rate) and when it ends.
- R2: the starter respawns the entity at most once every 10 real seconds, and no longer stops after 40 respawns (the cap of 40 only applies when `os.time` is missing).
- Checked outside the game with Lua 5.1 (`lupa`): `tools/harness/skipcost/test_skipcost.py` loads both scripts against a fake game and runs 33 checks (syntax, rate measurement, Wait, sleep, sitting, vigour rising, slow play at 5 fps, a Wait after slow play, a save load, a hitch, no `os.time`, respawn interval, owner takeover). Not run in the real game after these two changes.
- Still planned: an optional floor for the cost (hunger reaching 0 by a skip).

## 0.1.0 (2026-10-10)
- First module, built from the prototype in `tools/harness/skipcost/` (the scripts moved here; the harness builds a test copy from them).
- Charges hunger after a skip: awake rate x skipped hours x share by posture (standing 0.75, sitting 0.5, lying 0.5).
- Skips are found from long frames (about 0.25 s, normal 0.02 to 0.05 s) because the clock ratio changes with the hours and the last hour runs at the normal ratio.
- The kind comes from `player.player:IsLaying()` / `IsSitting()`, not from using a bed, so opening and cancelling a bed does not change the next Wait.
- Checked in game 1.9.8 with `krs_items`: Wait of 3.991 h cost 9.534 and Wait of 1.993 h cost 4.761 (rate 3.19 x hours x 0.75); the bar read back equal to the target. Not tested: a real sleep, a Wait sitting, reading, fainting.
