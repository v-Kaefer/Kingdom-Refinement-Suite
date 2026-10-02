# KRS QoL

Part of the Kingdom Refinement Suite. Small quality-of-life changes.

## What changes
| Area | Change | Vanilla -> KRS |
|---|---|---|
| Herbs | Larger pick radius | `HerbGatherSkillToRadius` 0.25 -> 0.35 |
| Carrying | More capacity per point of strength (hidden constant) | `StrengthToInventoryCapacity` 4 -> 5 (permission pending, do not publish) |
| Repairs | Repairs cost twice as much | `RepairPriceModif` 0.65 -> 1.3 (Hardcore-mode constants 0.9 -> 1.8) |
| Repairs | Bridles and saddles can be repaired with the repair skill | `skill2item_category` armor.horse_bridle / horse_saddle -> skill 8 |
| Quests | Timed quests are marked "(This quest is timed)" in the quest log | 22 quest texts, English, Czech, Portuguese |

Repair kit limits (`RepairKitItemHealthBestLimit`, `DefaultLimit`) are intentionally not changed yet; see `docs/ownership.csv`.

Based on ideas from Realistic Repairs, Herb Picking Radius 2x, Train More Carry More and Timed Quest Indicator (Tyburn).

## Install
Vortex: install `krs_qol-<version>.zip`. Manually: copy the `krs_qol` folder into `Mods/` and add `krs_qol` to `Mods/mod_order.txt`.
