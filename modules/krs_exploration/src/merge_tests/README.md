# Merge tests: cuts of other animation mods on top of the wash

Branch `krs-exploration-merges` (stacked on `krs-exploration`, before `develop`). Test bed for building ONE animation database from the game's file plus the
**cuts** (only the changed fragments) of several mods, instead of using their whole files, which can never be active together. Static test only: no merged
file has been run in the game yet. The cuts are third-party text (permission pending): this branch is for testing, not for publishing.

## Cuts
| File | Mod | Relative to | Operations | Note |
|---|---|---|---|---|
| `../wash/adb_wash.cut.xml` | 2372 Trough Washing | game 010902 | add 2 | the wash fragments (core of the module) |
| `1563_polearm.cut.xml` | 1563 Polearm Restoration | game 010902 | add 80, replace 2 | 2045 ships the same file: one candidate |
| `2276_herb.cut.xml` | 2276 Instant Herb Picking | game 010902 | replace 31, remove 2 | `speed="4"` on alchemy and herb fragments |
| `2049_hits_from_base.cut.xml` | 2049 Ragdoll Physics | ORIGINAL game file (`base`) | replace 324 | made on the old base, so it must be rebased |
| 2294 | Faster Combat | game 010902 | not cut yet | 8 variants; which one is still to be checked |

```bash
python tools/adb_cut.py make --mod 2276 --mod-adb <the mod's kcd_male_database.adb> [--base vanilla:010902|vanilla:base] --out cut.xml
python tools/adb_cut.py apply --cut ../wash/adb_wash.cut.xml 1563_polearm.cut.xml 2276_herb.cut.xml --out dist/merged.adb
python tools/adb_cut.py apply --skip-stale --report stale.csv --cut ... 2049_hits_from_base.cut.xml --out dist/merged.adb
```
`apply` refuses two cuts that change the same fragment differently, refuses an operation whose expected fragment is not in the file (a stale cut), and verifies
through ElementTree that the result is the game's 6786 fragments with exactly the cuts' changes.

## Results (6 Oct 2026, static)
| Merge | Operations applied | Conflicts | Result |
|---|---|---|---|
| wash + 1563 | add 82, replace 2 | none | 6868 fragments, verified |
| wash + 1563 + 2276 | add 82, replace 33, remove 2 | none | 6866 fragments, verified |
| wash + 1563 + 2276 + 2049 (as made, from the original file) | add 82, replace 194, remove 2 | none between cuts; 163 of the 324 operations of 2049 are stale and were skipped | 6866 fragments, verified |
| wash + 2049 rebased | add 2, replace 307 | none | 6788 fragments, verified; accepted by the game (see the game test) |

## Rebase of 2049 (`adb_cut rebase`)
`python tools/adb_cut.py rebase --cut 2049_hits_from_base.cut.xml --cut-base vanilla:base --onto vanilla:010902 --out 2049_hits_rebased.cut.xml --report 2049_rebase_report.csv`

Three-way merge inside each fragment: the mod's change (original file -> 2049) is applied to the current fragment attribute by attribute, only where the
current attribute still has the value the mod started from. Result for the 324 operations of 2049: **307 kept**.
| Count | What |
|---|---|
| 161 | the fragment is identical in the original and the current game: applied as is |
| 145 | the game's patches added `oppMale+oppFemale` to the fragment's FragTags (same fragment under a longer key): attributes moved onto it |
| 1 | same key, attributes moved |
| 17 | not applied: the game changed the structure of the fragment (CombatBlockBroken 14, LadderGetOff 3) |
| 4 | not applied: the fragment is gone (CombatStealthHitSuccess) |

What 2049 changes in the 146 rebased fragments (`CombatHit` 120, `CombatHitMovement` 13, `CombatStealthHitSuccess` 10, `CombatStealthPutDownSlave` 2, `HitDeath` 1): the hit-reaction parameters inside the procedural layer, for example
`Horizontal` 2 -> 11, `Vertical` 0 -> 4, `XyMove` 0 -> 6, `ZMove` 0 -> 4, `Rotate` 0 -> .42, `Velocity` 0 -> 16, `Inertia` 0 -> 12 (and `Stiffness` in 13 of them).
`2049_rebase_report.csv` has every fragment with its changes.

## Game test (replica, menu stage, 1.9.8)
`tools/harness/build_adbtest.py` installs the test mod `krs_adbtest` (a script that runs `mn_reload` and `mn_listAssets` at `sys_startup/OnEnd` and quits) with a database file;
`tools/harness/run_game_test.ps1` runs it. Logs in `docs/tests/logs/`.
| Run | Database in the test mod | Result |
|---|---|---|
| `adbtest_baseline_1.9.8.log` | none (the game's own) | normal, no animation database message |
| `adbtest_wash_2049rebased_1.9.8.log` | wash cut + rebased 2049 cut (6788 fragments) | **same log as the baseline**: no `Invalid animation DB`, no XML reader error; reached the end marker, game quit by itself |
| `adbtest_broken_control_1.9.8.log` | the same file cut at 3 MB | `XML reader: unclosed token ... (Animations/Mannequin/ADB/kcd_male_database.adb)` and `Invalid animation DB for actor 'DummyTarget'` from startup on; the game never ended (stopped after 300 s) |

The control shows that the game parses the mod's file at startup (actor `DummyTarget`) and logs a malformed one, so the clean log of the merged file means the game accepted it. It does
not show how the animations play: that needs a character in a level.

## Not done yet
- 2294: choose a variant (the four "Polearms-compat" ones carry the 80 polearm fragments with the speed changed; against 1563 that is 18 to 19 different fragments), then cut it.
- The 21 operations of 2049 that did not rebase (14 BlockBroken and 3 LadderGetOff with a changed structure, 4 StealthHitSuccess gone): decide whether to redo them by hand.
- Run the merged database with a character in a level (the menu test only proves that the file is accepted).
- Decide how a merged database is packaged without making every other animation mod collide: an optional file with compatibility variants.
