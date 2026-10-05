# Etc Folder Mod Mapping

Date: 2026-05-18

This is a first-pass mapping of the mods and support files found in `Mods WIP folder\Etc`.
Entries are marked by confidence:

- `confirmed` means the contents were opened and inspected.
- `inferred` means the purpose is based on the archive name and manifest only.
- `support` means the file is not a standalone mod but a helper/resource artifact.

## Mod Families

| Source | Type | Purpose | Files / Tables Touched | KRS Fit | Confidence |
| --- | --- | --- | --- | --- | --- |
| `EasyEdit` | extracted folder | Food table tuning pack. The inspected XML is `rpg/food.xml`, so this is a food/nutrition rebalance rather than a broad gameplay overhaul. | `Data/Libs/Tables/rpg/food.xml`, `food.tbl`, `EasyEdit.pak`, nested `EasyEdit.7zip` | `KRS-Items` | confirmed |
| `EasyEdit-837--1-1567314659.zip` | archive | Same mod family as the extracted `EasyEdit` folder, packaged as a mod archive. | `Data/EasyEdit.pak` | `KRS-Items` | confirmed |
| `Knox's Labelled Items (XML) - Version 1.0.2` | extracted folder | XML labeling resource for faster item editing. Adds readable item names in comments for common item tables. | `ammo.xml`, `armor.xml`, `equippable_item.xml`, `food.xml`, `melee_weapon.xml`, `missile_weapon.xml`, `pickable_item.xml`, `player_item.xml`, `weapon.xml` | support/reference | confirmed |
| `Knox's Labelled Items (XML)-326-1-0-2.zip` | archive | Same label-resource mod as the extracted folder. | same XML set as above | support/reference | confirmed |
| `Parameters Plus-554-1-5-1562283931` | extracted folder | Large `rpg_param` rebalance. The inspected XML changes reading XP, digestion, starvation, repair, combat, perception, skills, and related RPG systems. | `ParametersPlus/rpg_param.xml`, `ParametersPlus.pak`, `mod.manifest` | `KRS-Items` / possible `KRS-QoL` support | confirmed |
| `Parameters Plus-554-1-5-1562283931.zip` | archive | Same RPG-parameter mod as the extracted folder. | `ParametersPlus/rpg_param.xml`, `ParametersPlus.pak` | `KRS-Items` / possible `KRS-QoL` support | confirmed |
| `cheat-106-1-58-1732985419.zip` | archive | Cheat/debug utility mod. Manifest confirms the mod name; package includes data and localization archives. | `Data/data.pak`, `Localization/English_xml.pak`, `Localization/German_xml.pak`, `mod.manifest` | not a suite target; utility/reference | confirmed |
| `Enhanced Eyes 1.1-969-1-1-1585051202.zip` | archive | Cosmetic eye/eyelash visual mod. Manifest says it makes characters' eyes and eyelashes look more natural and colorful. | `EnhancedEyesByGrimsy/Data/EnhancedEyes.pak`, `mod.manifest` | not a suite target; cosmetic reference | confirmed |
| `Herb Picking Radius 2x-1938-1-0-1742117458.zip` | archive | QoL mod that likely doubles herb pickup radius. | archive only; not unpacked here | likely `KRS-QoL` | inferred |
| `Icon ID Resource-1059-1-0-1592792055.rar` | archive | Resource package for icon IDs. Likely a dependency/reference pack rather than a gameplay change. | archive only; not unpacked here | support/reference | inferred |
| `Realistic Horses-1839-1-0-1739145195.rar` | archive | Horse realism tweak package. Likely changes horse handling, stats, or immersion settings. | archive only; not unpacked here | possible `KRS-QoL` / separate horse module | inferred |
| `Realistic Repairs 1.1-1842-1-1-1739569897.rar` | archive | Repair-mechanics rebalance. This matches the suite notes about repair thresholds and repair-price changes. | archive only; not unpacked here | likely `KRS-Items` / `KRS-QoL` | inferred |
| `souls_sorted_v1.2-1779-1-2-1736773918.zip` | archive | Sorted soul table resource. The zip contains a single `souls_sorted_v2.xml` with `table name="soul"`, so this is a data/reference sort rather than a direct gameplay mod. | `souls_sorted_v2.xml` | support/reference | confirmed |
| `TimedQuestIndicator-1780-V1-1-1736764991.7zip` | archive | Timed quest indicator UI/QoL mod. The file signature is 7z and the name matches the known timed quest tracker. | archive only; not unpacked here | likely `KRS-QoL` | inferred |

## Support Files In This Folder

| File | Purpose | Notes |
| --- | --- | --- |
| `kcd_stats_minimal.lua` | Player stats reader helper | Standalone Lua helper for reading player stats. Likely belongs with the cheat/debug tooling rather than being a suite module on its own. |
| `Banner_Concept.jpg` | Artwork | Non-mod asset. Keep it out of module mapping. |

## Notes

- The extracted folders are more useful than the archives for immediate suite integration work.
- ZIP archives were inspected directly without renaming them to `.zip`; that was enough to read the contents already stored in the archive.
- `.rar` and `.7zip` archives were not unpacked in this pass, so those entries remain name-based unless noted otherwise.

