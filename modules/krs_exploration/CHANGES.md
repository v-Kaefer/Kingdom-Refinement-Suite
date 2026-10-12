# krs_exploration changes

## Unreleased (2026-10-10)
- The better beds (`sleeping_spot_type`, 4 rows from Bed Comfort Restored 480) are **held out** of the module by the author's decision: the recovery of sleep stays as in the game (8 hours is the perfect sleep; less or more has its adverse effects). The file is kept as `src/held/sleeping_spot_type__krs_exploration.xml`, outside `Data`, so it is not packaged. `docs/data/ownership.csv` marks the four rows as `held`.

## 1.0.0 (2026-10-08, v1 of krs_exploration)
Declared v1 by the author after the wash, the torch return and Reshield were played together in the test game. Contents: the two XP scripts and the optional wash package, as listed below. The XP scripts are installed without error (log) but their XP gain has not been seen in play yet. Kept for the next iteration, not part of v1: the animation cuts of 1563 (also 2045), 2276, 2294 and 2049 (`src/merge_tests/`, no conflict with the wash in the menu-stage test).

## 0.0.1 (prepared, not yet run in the game)
- Module id `krs_exploration`, manifest listing game versions 1.9.6, 1.9.7, 1.9.8.
- `Data/Scripts/Startup/krs_exploration.lua`: +1 `reading` XP for a shrine or cross read for the first time (wraps `CaptionObject:OnUsed`) and +1 `weapon_bow` XP for a nest shot down (wraps `Nest.Client:OnHit`). Installed at script load and again when the loading screen ends.
- `src/wash/`: cuts of Trough Washing Animation (2372) for the optional package `krs_exploration_wash` (see README). Built by `tools/build_exploration.py` with `tools/adb_cut.py` and `tools/text_cut.py`. Binary assets are not stored.
- `src/wash/so_water_tube.diff`: the player's torch (item class 4cea28a0) is put back in hand after the wash, the same way the glove already was. Trough Washing Animation (2372) unequipped it and never returned it. The torch variable is cleared at the start of each wash, so a torch put away earlier is not brought back. Menu-level test with `reshield` loaded: accepted, no script errors; the torch return itself needs a play test.
- `src/wash/troughwash.lua` + `so_water_tube.diff`: while the wash runs, Reshield (2313, when present) is paused through its own `Reshield.enabled` flag and put back as it was 1.5 s after the wash ends, so it does not put the shield in hand while the torch is off. Reshield's code is not changed. Menu-level test: troughwash.lua loads, no Lua error; the pause needs a play test (torch + shield in inventory).
