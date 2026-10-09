# krs_exploration changes

## Unreleased (2026-10-09)
- Better beds: `Data/Libs/Tables/rpg/sleeping_spot_type__krs_exploration.xml` (4 complete rows: exceptional 1.0 -> 1.2, high 0.7 -> 0.955, low 0.3 -> 0.325, medium 0.5 -> 0.65). Moved here from `krs_items` by the author's decision; the rows are unchanged and the patch suffix now equals this module's id. Derived from Bed Comfort Restored (480), whose values differ. Not yet read back in game: sleeping spots only exist inside a level (player-stage run pending, as before). Not part of the v1.0.0 that was played.

## 1.0.0 (2026-10-08, v1 of krs_exploration)
Declared v1 by the author after the wash, the torch return and Reshield were played together in the test game. Contents: the two XP scripts and the optional wash package, as listed below. The XP scripts are installed without error (log) but their XP gain has not been seen in play yet. Kept for the next iteration, not part of v1: the animation cuts of 1563 (also 2045), 2276, 2294 and 2049 (`src/merge_tests/`, no conflict with the wash in the menu-stage test).

## 0.0.1 (prepared, not yet run in the game)
- Module id `krs_exploration`, manifest listing game versions 1.9.6, 1.9.7, 1.9.8.
- `Data/Scripts/Startup/krs_exploration.lua`: +1 `reading` XP for a shrine or cross read for the first time (wraps `CaptionObject:OnUsed`) and +1 `weapon_bow` XP for a nest shot down (wraps `Nest.Client:OnHit`). Installed at script load and again when the loading screen ends.
- `src/wash/`: cuts of Trough Washing Animation (2372) for the optional package `krs_exploration_wash` (see README). Built by `tools/build_exploration.py` with `tools/adb_cut.py` and `tools/text_cut.py`. Binary assets are not stored.
- `src/wash/so_water_tube.diff`: the player's torch (item class 4cea28a0) is put back in hand after the wash, the same way the glove already was. Trough Washing Animation (2372) unequipped it and never returned it. The torch variable is cleared at the start of each wash, so a torch put away earlier is not brought back. Menu-level test with `reshield` loaded: accepted, no script errors; the torch return itself needs a play test.
- `src/wash/troughwash.lua` + `so_water_tube.diff`: while the wash runs, Reshield (2313, when present) is paused through its own `Reshield.enabled` flag and put back as it was 1.5 s after the wash ends, so it does not put the shield in hand while the torch is off. Reshield's code is not changed. Menu-level test: troughwash.lua loads, no Lua error; the pause needs a play test (torch + shield in inventory).
