# krs_exploration changes

## 0.0.1 (prepared, not yet run in the game)
- Module id `krs_exploration`, manifest listing game versions 1.9.6, 1.9.7, 1.9.8.
- `Data/Scripts/Startup/krs_exploration.lua`: +1 `reading` XP for a shrine or cross read for the first time (wraps `CaptionObject:OnUsed`) and +1 `weapon_bow` XP for a nest shot down (wraps `Nest.Client:OnHit`). Installed at script load and again when the loading screen ends.
- `src/wash/`: cuts of Trough Washing Animation (2372) for the optional package `krs_exploration_wash` (see README). Built by `tools/build_exploration.py` with `tools/adb_cut.py` and `tools/text_cut.py`. Binary assets are not stored.
- `src/wash/so_water_tube.diff`: the player's torch (item class 4cea28a0) is put back in hand after the wash, the same way the glove already was. Trough Washing Animation (2372) unequipped it and never returned it. The torch variable is cleared at the start of each wash, so a torch put away earlier is not brought back. Menu-level test with `reshield` loaded: accepted, no script errors; the torch return itself needs a play test.
- `src/wash/troughwash.lua` + `so_water_tube.diff`: while the wash runs, Reshield (2313, when present) is paused through its own `Reshield.enabled` flag and put back as it was 1.5 s after the wash ends, so it does not put the shield in hand while the torch is off. Reshield's code is not changed. Menu-level test: troughwash.lua loads, no Lua error; the pause needs a play test (torch + shield in inventory).
