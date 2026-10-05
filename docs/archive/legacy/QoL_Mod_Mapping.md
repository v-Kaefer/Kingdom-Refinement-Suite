# QoL Folder Mod Mapping

Date: 2026-05-18

This is a first-pass mapping of the mods and support files found in `Mods WIP folder\QoL`.
Entries are marked by confidence:

- `confirmed` means the contents were opened and inspected.
- `inferred` means the purpose is based on the archive name, manifest, or readme only.
- `support` means the file is not a standalone mod but a helper/resource artifact.

## Mod Families

| Source | Type | Purpose | Files / Tables Touched | KRS Fit | Confidence |
| --- | --- | --- | --- | --- | --- |
| `trainmorecarrymore` | extracted folder | Carry-capacity rebalance that increases carry capacity as Strength rises. | `Data/Libs/Tables/rpg/rpg_param__trainmorecarrymore.xml`, `mod.manifest` | `KRS-Items` / player balance | confirmed |
| `hoskope_hgrx2` | extracted folder | Herb gathering radius x2. | `Data/Libs/Tables/rpg/rpg_param__hoskope_hgrx2.xml`, `mod.manifest` | `KRS-QoL` | confirmed |
| `TimedQuestIndicator` | extracted folder | Quest timer indicator/translations. The readme says it adds the line “This quest is timed” for timed quests. | `English/TyburnTimedQuestIndicator/*`, `Czech/TyburnTimedQuestIndicator/*`, `ReadMe.txt` | `KRS-QoL` | confirmed |
| `Skill Books Take Time 2x-1950-1-0-1742313588` | extracted folder | Reading-time rebalance for books. The XML cuts `ReadingXpPerHour` to 10 and changes book document durations. | `hoskope-skillbookstaketime/Data/Libs/Tables/rpg/rpg_param__hoskope-skillbookstaketime.xml`, `item/document__hoskope-skillbookstaketime.xml`, `mod.manifest` | `KRS-Items` / `KRS-QoL` | confirmed |
| `Realistic_Repairs` | extracted folder | Repair-mechanics rebalance. The manifest says repairs are more expensive, Henry can repair items before they are too damaged, and horse bridles are fixable. | `Data/Tables/rpg/rpg_param__RR.xml`, `perk_rpg_param_override__RR.xml`, `skill2item_category__RR.xml`, `Data/Realistic_Repairs.pak`, `mod.manifest` | `KRS-QoL` / `KRS-Items` | confirmed |
| `Realistic_Horse` | extracted folder | Horse/player carrying-capacity reduction mod. | `Data/Realistic_Horse.pak`, `mod.manifest` | likely separate balance pack, not a direct KRS merge target | confirmed |
| `EnhancedEyesByGrimsy` | extracted folder | Cosmetic eye and eyelash visual mod. | `Data/Objects/...` textures/materials, `Data/EnhancedEyes.7zip`, `mod.manifest` | not a suite target; cosmetic reference | confirmed |
| `MagusRespawnYears20-1665-Years20-1718483997.7z` | archive | World respawn tuning, likely setting respawn time to 20 years. | archive only; not unpacked here | possible world-balance / survival tuning | inferred |
| `MagusDespawnYears20-1665-Years20-1718643655.7z` | archive | World despawn tuning, likely setting despawn time to 20 years. | archive only; not unpacked here | possible world-balance / survival tuning | inferred |

## Suite-Integration Notes

- `trainmorecarrymore`, `hoskope_hgrx2`, `TimedQuestIndicator`, `Skill Books Take Time 2x`, and `Realistic_Repairs` are the clearest suite candidates.
- `Realistic_Horse` overlaps conceptually with `trainmorecarrymore`, but in the opposite direction. It should stay separate unless you want an explicit horse-balance branch.
- `EnhancedEyesByGrimsy` is cosmetic only and should not be merged into the gameplay suite.

