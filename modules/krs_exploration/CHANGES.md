# krs_exploration changes

## 0.0.1 (prepared, not yet run in the game)
- Module id `krs_exploration`, manifest listing game versions 1.9.6, 1.9.7, 1.9.8.
- `Data/Scripts/Startup/krs_exploration.lua`: +1 `reading` XP for a shrine or cross read for the first time (wraps `CaptionObject:OnUsed`) and +1 `weapon_bow` XP for a nest shot down (wraps `Nest.Client:OnHit`). Installed at script load and again when the loading screen ends.
- `src/wash/`: cuts of Trough Washing Animation (2372) for the optional package `krs_exploration_wash` (see README). Built by `tools/build_exploration.py` with `tools/adb_cut.py` and `tools/text_cut.py`. Binary assets are not stored.
