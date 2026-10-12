# KRS Items

Part of the Kingdom Refinement Suite. Makes food, sleep and reading matter a little more, without making them a chore.

## What changes

| Area | Change | Vanilla -> KRS |
|---|---|---|
| Books | Reading takes 2.5x longer (56 skill books) | 4 / 6 / 8 / 10 h -> 10 / 15 / 20 / 25 h |
| Books | Reading XP per hour lowered to match | 20 -> 5 |
| Hunger | Food is digested faster (hidden constant `DigestionSpeed`) | 0.000579 -> 0.001302 |
| Hunger | Starvation effects start earlier and bite harder | `StarvationPlayerEffectMinMin` 90 -> 95, `MaxMax` 75 -> 65, `MinMax` 45 -> 25 |
| Potions | Aesop potion feeds less (single row, a first taste of the potion rebalance) | nutrition 10 -> 2.5, short-term ratio 0.1 -> 0.5 |

Exact rows: `Data/Libs/Tables/**` in the source tree (`modules/krs_items`), tracked in `docs/data/ownership.csv`.

## Install

Vortex: install the archive `krs_items-<version>.zip` and enable it. Manually: copy the folder `krs_items` into
`KingdomComeDeliverance/Mods/` and add `krs_items` to `Mods/mod_order.txt`.
Safe to add or remove at any time; it only changes tables, never saves.

## Compatibility

Patches are complete rows, and when two mods change the same row the later mod in `mod_order.txt` wins the whole row.
Mods that touch the same rows: Skill Books Take Time 2x (documents), Food Spoil
Faster and PotionNoSatietyAndHealEnergy (food row of the Aesop potion). Load krs_items last if you want its values.

Author: Kaleb. Book timing derived from "Skill Books Take Time 2x" by hoskope. The better beds are not part of the module: they were held out on 2026-10-10 (sleep recovery stays as in the game); the rows wait in `krs_exploration/src/held/`.
