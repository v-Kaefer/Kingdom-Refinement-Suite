# Nexus packages

Each named folder is one Nexus upload. Run `python tools/build_nexus_packages.py`
from the repository root to create its named ZIP. Upload that ZIP as the
mod file and paste `NEXUS_DESCRIPTION.txt` into the Nexus description fields.
The ZIP contains only game-installable mod folders at its root; the large
category folders are for organizing this repository, not for copying to the game.

| Category | Nexus upload | Game mod ids |
|---|---|---|
| KRS-Items | Gluttony Rebalanced | `krs_gluttony`, `krs_skipcost` |
| KRS-Items | Leech & Lore Reworked | `krs_leech_lore` |
| KRS-Items | Realistic Potions | `krs_realistic_potions` |
| KRS-Perks | Perks Reworked | `krs_perks` |
| KRS-QoL | Everyday Tweaks | `krs_qol` |
| KRS-Exploration | Exploration Reworked | `krs_exploration` |

The three KRS-Items uploads split the existing `modules/krs_items` patch rows.
**Do not enable the original `krs_items` beside them:** its rows overlap the
three new ids. The Gluttony ZIP also contains `krs_skipcost`, which can be
disabled separately if desired. `krs_exploration_wash` is deliberately omitted:
its third-party assets cannot be redistributed without permission. The held
better-bed rows are omitted too.

This is a draft release layout. The source modules and their existing test
history remain intact; new split ids and every packaged ZIP need a loaded-save
game check before publication. The permission status for third-party-derived
changes is tracked in `docs/project/PERMISSIONS.md`.
