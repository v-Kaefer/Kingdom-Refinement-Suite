# Perks Folder Mod Mapping

Date: 2026-05-18

This is a first-pass mapping of the mods and support files found in `Mods WIP folder\Perks`.
Entries are marked by confidence:

- `confirmed` means the contents were opened and inspected.
- `inferred` means the purpose is based on the archive name or readme only.
- `support` means the file is not a standalone mod but a helper/resource artifact.

## Mod Families

| Source | Type | Purpose | Files / Tables Touched | KRS Fit | Confidence |
| --- | --- | --- | --- | --- | --- |
| `Perkaholic` | extracted folder | Perk expansion for Bow, Polearm, Unarmed, and other perk lines. The perk table adds new perks and perk exclusivity links. | `Data/Libs/Tables/rpg/perk__perkaholic.xml`, `perk_buff__perkaholic.xml`, `perk_buff_override__perkaholic.xml`, `perk2perk_exclusivity__perkaholic.xml`, `skill__perkaholic.xml`, localization packs, `mod.manifest` | `KRS-Perks` | confirmed |
| `Mods/perkaholic` | extracted folder | Older/alternate Perkaholic packaging for the same perk-expansion family. | `Data/Libs/Tables/rpg/{perk,perk_buff,perk_buff_override,perk2perk_exclusivity,skill}.{xml,tbl}`, `Data/Libs/Localization/localization.xml`, `mod.manifest`, `mod.cfg`, `readme.txt`, `changelog.txt` | `KRS-Perks` | confirmed |
| `Perkaholic 1.05-85-1-05.zip` | archive | Older Perkaholic release archive. | archive only; not unpacked here | `KRS-Perks` | inferred |
| `Perkaholic PTF-1009-1-2-3-1714642782.7zip` | archive | PTF-era Perkaholic package. | archive only; not unpacked here | `KRS-Perks` | inferred |

## Key Gameplay Changes

- Adds new perks to existing lines.
- Adds perk support for Bow, Polearm, and Unarmed skills.
- Adds or updates perk-buff rules and perk exclusivity relationships.

## Suite-Integration Notes

- This is the clearest `KRS-Perks` seed in the repo.
- The `Perkaholic` extracted folder is the best source of truth for integration because it is already organized as a PTF-style mod package.
- The older `Mods/perkaholic` packaging should be treated as a reference variant, not as a separate design target.

