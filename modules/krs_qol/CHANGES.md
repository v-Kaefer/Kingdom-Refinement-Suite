# krs_qol changes

## 1.0.0
- New module id `krs_qol` with patches `rpg_param__krs_qol.xml`, `perk_rpg_param_override__krs_qol.xml`, `skill2item_category__krs_qol.xml` (all complete rows, suffix = id).
- The stray `perk_id` rows in `rpg_param` and the bow experiment constants of the old file are not carried over (the bow moves to its own module).
- Repairs: global price x2 (normal mode) and x2 in the Hardcore constants. Limits left untouched until tested in game.
- Quest texts moved from `Tables/ui/text_*__KRSPKG1.xml` (a mechanism the game does not use for text) to `Localization/<Language>_xml.pak` with `text__krs_qol.xml`; the engine loads the patch (log line `Loading localization patch`).
- Checked in game at the main menu: the three `rpg_param` rows and the constants. The override and `skill2item_category` rows need a level.
