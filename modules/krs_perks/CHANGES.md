# krs_perks changes

## 1.0.0
- New module id `krs_perks`; `perk__krs_perks.xml` with complete rows (the upstream rows left out the `autolearnable` and `exclude_in_game_mode` columns, which blanks them).
- Localization: `Localization/<Language>_xml.pak` (ZIP) with `text__krs_perks.xml` for 14 languages. The engine logs `Loading localization patch 'Localization\text__krs_perks.xml'` (checked in game).
- Checked together with the upstream Riposte mod: krs_perks loaded after it reported `modified: 1, equal: 1` (the level changes, Master Strike is identical).
- Not yet checked: the perk tables only exist inside a level, so the perk rows themselves are read back by `python tools/gate.py krs_perks --mode full` after pressing Continue.
