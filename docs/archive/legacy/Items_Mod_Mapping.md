# Items Folder Mod Mapping

Date: 2026-05-18

This is a first-pass mapping of the mods and support files found in `Mods WIP folder\Items`.
Entries are marked by confidence:

- `confirmed` means the contents were opened and inspected.
- `inferred` means the purpose is based on the archive name, manifest, or readme only.
- `support` means the file is not a standalone mod but a helper/resource artifact.

## Mod Families

| Source | Type | Purpose | Files / Tables Touched | KRS Fit | Confidence |
| --- | --- | --- | --- | --- | --- |
| `Bed Comfort Restored-480-1-0` | extracted folder | Restores sleeping spot comfort values. The XML shows `sleeping_spot_type.xml` changes only. | `Data/Libs/Tables/rpg/sleeping_spot_type.xml`, `sleeping_spot_type.tbl`, `Bed_Comfort.7zip`, `mod.manifest` | `KRS-Items` / sleep tuning | confirmed |
| `PotionNoSatietyAndHealEnergy` | extracted folder | Potion food-table override that removes satiety and boosts healing/energy behavior. The XML is a custom `food__alternatefoodspoil` table with potion rows set to `nutrition=0` and `refresh=100`. | `Data/Tables/item/food__PotionNoSatietyAndHealEnergy.xml`, `mod.manifest`, nested `PotionNoSatietyAndHealEnergy.7zip` | `KRS-Items` | confirmed |
| `More historically accurate item stats` | extracted folder | Broad weapon/armor stat rebalance. The manifest says “Weapon and armour total rebalanced,” and the folder contains item tables for weapons, armor, ammo, and equippables. | `Data/Libs/Tables/item/{weapon,missile_weapon,melee_weapon,equippable_item,armor,ammo}.{xml,tbl}`, `mod.manifest` | `KRS-Items` | confirmed |
| `HoodsUp` | extracted folder | Hood-up behavior mod. The log says it makes all hoods go up and references manual `armor.xml`/`clothingpreset.xml` editing. | `Data/HoodsUp.pak`, `mod.manifest`, `Log.md` | likely separate hood module or `KRS-Items` clothing support | confirmed |
| `HoodsUpStandalone` | extracted folder | Standalone hood-up/down copy mod. The log says it provides a standalone copy of 43 hoods/scarfs with hoods up. | `Data/hoods_up_standalone.pak`, `Localization/English_xml.pak`, `Localization/Czech_xml.pak`, `mod.manifest`, `Log.md` | likely separate hood module or `KRS-Items` clothing support | confirmed |
| `Dynamic Hoods and Scarfs up and down-483-1-9-1590343806.zip` | archive | Dynamic hood/scarf toggle mod. The packaged mod name and install note show it is the “Hoods and Scarfs UP (dynamic)” release. | `zzz Hoods and Scarfs UP (dynamic)/Data/Hoods and Scarfs UP (dynamic).pak`, `mod.manifest`, install note | likely separate hood module or `KRS-Items` clothing support | confirmed |
| `Hoods Over Helmets Remove Kettle Helmets NPC-771-1-1-1562422310` | extracted folder | Hood/helmet merge pack plus cheat/autocheat wiring and manual hotkey support. The readme explicitly describes hoods over helmets and related cheats. | `Data/autocheat.txt`, `mods/Hoods Over Helmets/Data/Hoods Over Helmets.pak`, `mods/Hoods Over Helmets/mod.manifest`, cheat-code text files, user.cfg reference | likely separate hood module or `KRS-Items` clothing support | confirmed |
| `Hoods Over Helmets Remove Kettle Helmets NPC-771-1-1-1562422310.7z` | archive | Same hood-over-helmet family as the extracted folder, likely the original package. | archive only; not unpacked here | likely separate hood module or `KRS-Items` clothing support | inferred |
| `All Hoods Up-791-1-1-1562185697.7zip` | archive | Older hoods-up archive, likely related to the standalone hood set. | archive only; not unpacked here | likely separate hood module or `KRS-Items` clothing support | inferred |
| `HoodsUpStandalone - PTF-1386-1-0-1654827508.7zip` | archive | Standalone PTF hood-up archive. The extracted `HoodsUpStandalone` folder and its log confirm this family is the standalone version. | archive only; not unpacked here | likely separate hood module or `KRS-Items` clothing support | inferred |
| `mod-1153-1-0-0-1605526312.zip` | archive | Another hood-up archive that matches the standalone hood family. | `Data/mod.pak`, `mod.manifest` | likely separate hood module or `KRS-Items` clothing support | inferred |

## Support Files In This Folder

| File | Purpose | Notes |
| --- | --- | --- |
| `Changelog.md` | local working notes | Mentions items still to identify and mods still to evaluate. |

## Suite-Integration Notes

- `Bed Comfort Restored`, `PotionNoSatietyAndHealEnergy`, and `More historically accurate item stats` are the clearest `KRS-Items` candidates.
- The hood-related mods likely belong in a separate clothing/hood submodule or as a dedicated optional pack, because they all touch overlapping armor/clothing tables and are likely to conflict if merged naively.
- The hood archives were not unpacked in this pass when they were `.7z` / `.7zip`, so those entries remain name-based unless their extracted folder already exists in the repo.

