# KRS Items

Part of the Kingdom Refinement Suite. Makes food, sleep and reading matter a little more, without making them a chore.

## What changes

| Area | Change | Vanilla -> KRS |
|---|---|---|
| Books | Reading takes 2.5x longer (56 skill books) | 4 / 6 / 8 / 10 h -> 10 / 15 / 20 / 25 h |
| Books | Reading XP per hour lowered to match | 20 -> 5 |
| Hunger | Food is digested faster (hidden constant `DigestionSpeed`) | 0.000579 -> 0.001302 |
| Hunger | Starvation effects start earlier and bite harder | `StarvationPlayerEffectMinMin` 90 -> 95, `MaxMax` 75 -> 65, `MinMax` 45 -> 25 |
| Sleep | Better beds are worth more, the ground stays poor | exceptional 1.0 -> 1.2, high 0.7 -> 0.955, low 0.3 -> 0.325, medium 0.5 -> 0.65 |
| Potions | Aesop potion feeds less (single row, a first taste of the potion rebalance) | nutrition 10 -> 2.5, short-term ratio 0.1 -> 0.5 |

Exact rows: `Data/Libs/Tables/**` in the source tree (`modules/krs_items`), tracked in `docs/data/ownership.csv`.

## Install

Vortex: install the archive `krs_items-<version>.zip` and enable it. Manually: copy the folder `krs_items` into
`KingdomComeDeliverance/Mods/` and add `krs_items` to `Mods/mod_order.txt`.
Safe to add or remove at any time; it only changes tables, never saves.

## Compatibility

Patches are complete rows, and when two mods change the same row the later mod in `mod_order.txt` wins the whole row.
Mods that touch the same rows: Skill Books Take Time 2x (documents), Bed Comfort Restored (sleeping spots), Food Spoil
Faster and PotionNoSatietyAndHealEnergy (food row of the Aesop potion). Load krs_items last if you want its values.

Author: Kaleb. Book timing derived from "Skill Books Take Time 2x" by hoskope; bed values from "Bed Comfort Restored".
