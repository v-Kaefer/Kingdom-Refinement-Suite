# Player Folder Mod Mapping

Date: 2026-05-18

This is a first-pass mapping of the mods and support files found in `Mods WIP folder\Player`.
Entries are marked by confidence:

- `confirmed` means the contents were opened and inspected.
- `inferred` means the purpose is based on the archive name or readme only.
- `support` means the file is not a standalone mod but a helper/resource artifact.

## Mod Families

| Source | Type | Purpose | Files / Tables Touched | KRS Fit | Confidence |
| --- | --- | --- | --- | --- | --- |
| `5.5-6 Nourishment and 4 Energy lost per hour-311-1-0` | extracted folder | Hunger/fatigue rebalance. The readme says it makes nourishment and energy drain more lifelike and the XML adds `DigestionSpeed` and `ExhaustionSpeed` changes. | `Libs/Tables/rpg/rpg_param.xml`, `rpg_param.tbl`, `Readme.txt` | `KRS-Items` | confirmed |
| `5.5-6 Nourishment and 4 Energy lost per hour-311-1-0.7z` | archive | Same hunger/fatigue rebalance family as the extracted folder. | archive only; not unpacked here | `KRS-Items` | inferred |

## Key Gameplay Changes

- `DigestionSpeed` is set to `0.0015`.
- `ExhaustionSpeed` is set to `0.0015`.
- The readme frames the mod as making food choice matter more and increasing the need to manage sleep.

## Suite-Integration Notes

- This is a direct `KRS-Items` candidate because it edits core `rpg_param` values that align with the suite’s hunger/fatigue balance work.
- The archive copy appears to be the packaged source of the extracted folder, so the extracted folder is the better source for integration work.

