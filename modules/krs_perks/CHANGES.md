# krs_perks changes

## 1.0.0
- Manifest lists game versions 1.9.6, 1.9.7, 1.9.8. Gate passed on 1.9.8 (menu stage); the perk rows themselves still need a level (`--mode full`).
- New module id `krs_perks`; `perk__krs_perks.xml` with complete rows (the upstream rows left out the `autolearnable` and `exclude_in_game_mode` columns, which blanks them).
- Localization: `Localization/<Language>_xml.pak` (ZIP) with `text__krs_perks.xml` for 14 languages. The engine logs `Loading localization patch 'Localization\text__krs_perks.xml'` (checked in game).
- Checked together with the upstream Riposte mod: krs_perks loaded after it reported `modified: 1, equal: 1` (the level changes, Master Strike is identical).
- Not yet checked: the perk tables only exist inside a level, so the perk rows themselves are read back by `python tools/gate.py krs_perks --mode full` after pressing Continue.

## 1.1.0 (6 Oct 2026) - usable for a test session
- `tools/check_patch_names.py`: 0 problems. Complete column set on every row, no dangling reference, every UI key resolves in the module's own localization (116 of 116), every icon is one a vanilla perk already uses (39 of 39). Open points for the test are in `NOTES.md`; still not run in game.
- The 56 Perkaholic perks merged in, with the author's balance corrections. Two rows change the game rather than adding to it: `perk_heavy_swing` (`wat*1.03,wac*1.1` -> `wat*1.07,wac*1.1`) and the skill row that un-hides skill 23 (Long Weapon), where the module itself puts 10 perks.
- **Fall-damage ladder**: tier I stays the game's own `fdm*0.7` (30% less) - the row is no longer shipped. Tiers II and III are `fdm*0.60` (40%) and `fdm*0.45` (55%), delivered by `perk_buff_override`. The mod's own descriptions claimed 50% and 75%, which contradicted its own formulas; corrected in all 13 languages by replacing the number only, so each translation is kept.
- **Block-cost ladder** renamed from Firm Grip to **Knock Knock I / II / III**. Tier I is the game's "Firm hand" (`osb*1.15`), whose displayed name the module overrides; the row itself is untouched.
- The game's "Like a feather" perk now displays as **Like a Feather I** (it shows "Featherweight" in vanilla), so all three rungs of the ladder read the same name.
- Localization keys inherited from mod 1765 moved from its author's `perk_ex_*` namespace to ours: `perk_krs_riposte_name`, `perk_krs_riposte_desc`, `perk_krs_ripo_text_sword`, `perk_krs_ripo_text_desc`. Renamed in all 14 language files and in the perk rows that point at them.
- A link row identical to a row the game already has is no longer written (rule 7): it changed nothing and only widened the surface shared with other mods. One row dropped, in `perk_buff`.
- `tools/build_krs_perks.py` gained three things so a decision taken after the first build still reaches the files: `fix_text()` (rewrites text already written, and adds a name override the mod never shipped), `rename_keys()`, and `PERK_FIXES` now also applies to rows kept from an earlier build.
