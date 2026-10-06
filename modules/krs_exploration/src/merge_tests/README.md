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
| wash + 1563 + 2276 + 2049 | add 82, replace 194, remove 2 | none between cuts; **163 of the 324 operations of 2049 are stale** | 6866 fragments, verified |

The 163 stale operations of 2049 (`2049_stale_report.csv`: CombatHit 120, CombatBlockBroken 14, CombatHitMovement 13, CombatStealthHitSuccess 10, others 6) are fragments the
game's own patches changed after the original file, so 2049's change cannot be pasted over them. They need a rebase at attribute level (apply only what 2049 changed
inside the fragment, when those attributes are unchanged in the current fragment). The other 161 operations apply because their fragments are identical in the original and
the current game.

## Not done yet
- 2294: choose a variant (the four "Polearms-compat" ones carry the 80 polearm fragments with the speed changed; against 1563 that is 18 to 19 different fragments), then cut it.
- Attribute-level rebase of the 2049 cut for the 163 stale fragments.
- Run a merged database in the replica game (menu stage proves that it loads; effects need a character).
- Decide how a merged database is packaged without making every other animation mod collide: an optional file with compatibility variants.
