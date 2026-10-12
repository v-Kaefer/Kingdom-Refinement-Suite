# KRS Exploration

Part of the Kingdom Refinement Suite. Small rewards for exploring. **Status: v1.0.0** (branch `krs-exploration`). The wash and the torch return were played in the test game; the XP scripts load without error but their XP gain has not been seen in play yet. The animation cuts of 1563/2045, 2276, 2294 and 2049 (`src/merge_tests/`) are kept for the next iteration and are not part of v1.

## What it contains (author's decision of 2026-10-06)
| Part | Package | Idea from | What | How |
|---|---|---|---|---|
| Shrine and cross XP | `krs_exploration` | Waystones Give XP (1518, CrEaToXx) | +1 `reading` XP the first time a wayside shrine or cross (`CaptionObject`) is read | `Data/Scripts/Startup/krs_exploration.lua` wraps `CaptionObject:OnUsed`; the game's script is not replaced |
| Nest XP | `krs_exploration` | Shooting Nests Gives XP (1519, CrEaToXx) | +1 `weapon_bow` XP when a nest is shot down | same file, wraps `Nest.Client:OnHit` (XP on the change of `shotDown` from 0 to 1) |
| Better beds (held) | none | Bed Comfort Restored (480) | held out of v1: sleep recovery stays as in the game | the 4 rows wait in `src/held/` and are not packaged |
| Trough washing | `krs_exploration_wash` (optional file) | Trough Washing Animation (2372, TofuDieb) | the player washes at a water trough with an animation, water splash and drops on the screen, instead of a fade to black | cuts of the mod's changes, applied to the game's own files at build time (`src/wash/`) |

The amounts (1 XP) are provisional and depend on the suite's XP curve. The code of the two XP parts is written for this module (the ideas come from the two mods, which replace whole game scripts to change 2 to 8 lines). The wash part is the third-party work of TofuDieb reduced to the pieces the wash needs; its binary assets (animation index, wash animation, splash materials and textures) come from the mod's own archive at build time and are **not in the repository**. No permission is recorded for any of the three mods (`docs/project/PERMISSIONS.md`): **do not publish the wash part until it is granted**.

## Why two packages
The wash needs a changed animation database (`kcd_male_database.adb`), and a mod that ships that file collides with every other animation mod. Keeping it out of the core package means the core can never collide with them, and the wash can have compatibility variants later (branch `krs-exploration-merges`).

## Build and install
```bash
python tools/build_exploration.py core
python tools/build_exploration.py wash --assets-from "<path of the Trough Washing Animation archive>"
```
Output in `dist/` (ignored by git): `krs_exploration/` and `krs_exploration_wash/`. Copy them into `Mods/` of the test game and list them in `Mods/mod_order.txt`. `--no-assets` builds the structure without the binary assets (the animation cannot play).

## What is cut and from where (`src/wash/`)
| File | What | Applied to |
|---|---|---|
| `adb_wash.cut.xml` | the two player fragments `WashFace` (`washFaceTub`), made by `tools/adb_cut.py` | the game's `kcd_male_database.adb` (patch 010902) |
| `so_water_tube.diff` | 3 hunks (+51 -8): the player's wash behaviour at the trough | `Scripts.pak` `Libs/AI/final/so_water_tube.xml` |
| `workbehaviors.diff` | the splash particle effect `bathhouse.splash_3` (+28) | `GameData.pak` `Libs/Particles/workbehaviors.xml` |
| `male_animevents.diff` | the events (sounds, splash) of the wash animation (+22) | patch 010900 `male.animevents` |
| `troughwash.lua` | the screen drops (30 lines) | new file |
| `assets.csv` | the 21 binary assets with sha256, not in the repository | from the mod archive |

Left out on purpose: 187 crossbow fragments, the crossbow tags and 157 crossbow event blocks, the boiler eating animations and their fragments, and the replacement of the whole `male.animevents`.

## Open work
- Run in the replica game (`E:\Kingdom-Refinement-Suite\Mods WIP folder\KingdomComeDeliverance`): the entity tables exist at startup and can be wrapped; the XP is given; the wash plays without freezing the input and the torch comes back (the original does not re-equip it).
- Try the game's own `wash_face_tub_01/02` for the player (would remove the need for the binary assets).
- Merge tests with cuts of other animation mods: branch `krs-exploration-merges`.
