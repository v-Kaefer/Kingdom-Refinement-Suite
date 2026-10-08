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

Repair kit limits (`RepairKitItemHealthBestLimit`, `DefaultLimit`) are intentionally not changed yet; see `docs/data/ownership.csv`.

Based on ideas from Realistic Repairs, Herb Picking Radius 2x, Train More Carry More and Timed Quest Indicator (Tyburn).

## Install
Vortex: install `krs_qol-<version>.zip`. Manually: copy the `krs_qol` folder into `Mods/` and add `krs_qol` to `Mods/mod_order.txt`.

## Optional: Reshield (Nexus 2313, by Conway)
Puts the shield back when the torch is put away. It is a Lua script in a pak, not a table patch, so it is **not** part of the `krs_qol` zip. It is installed as the author's own mod (`reshield`, version 2.0), unchanged, and goes after `krs_qol` in `mod_order.txt`.

| File in the author's archive | sha256 |
|---|---|
| `Reshield/Data/reshield.pak` | `4134e5531fa87eceef5464722d34cc01d5ffa90eaa323274a1f35df0bd804b7f` |
| `Reshield/mod.manifest` | `1da90973688458ac9ba8ad279b8d9cf6c1490db4b702cd7ad9c22693af90dbe8` |

- Permission to include it in a KRS package has not been asked, so nothing of it is stored here; see `docs/project/PERMISSIONS.md` on `develop`.
- Works with `krs_exploration_wash`: the wash pauses Reshield through Reshield's own `enabled` flag while it runs (the wash takes the torch off and gives it back by itself), then puts the flag back. Without Reshield installed the wash does nothing extra.
- Console commands of the mod: `rs_status`, `rs_dump`, `rs_off`, `rs_on`, `rs_debug`.

Build the companion from the author's archive (checks the hashes above, writes `dist/reshield`; `--install` also copies it into a game folder and adds it to `mod_order.txt`):

    python tools/build_qol_reshield.py --from "<Reshield 2313 ... .zip>" [--install "<KCD folder>"]

Played together with `krs_exploration_wash` in the test game (2026-10-08): the torch returns after the wash, Reshield returns the shield when the torch is put away, and both work together.
