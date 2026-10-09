# krs_items changes

## Unreleased (2026-10-09)
- The sleeping spot rows (better beds, derived from Bed Comfort Restored 480) moved to `krs_exploration` by the author's decision. `krs_items` no longer patches `sleeping_spot_type`; `docs/data/ownership.csv` follows. Remaining content: books (56 rows), `ReadingXpPerHour`, `DigestionSpeed`, three `StarvationPlayerEffect*` constants, and the Aesop potion row.

## 2.0.0
- Manifest lists game versions 1.9.6, 1.9.7, 1.9.8 (the 1.9.8 engine disables a mod that does not list the running version); the legacy `1.9.x` value would have been disabled. Gate passed on 1.9.8 (73/73 menu-stage checks together with the other modules).
- Repackaged: mod id `krs_items`, every table patch named `<table>__krs_items.xml` (the game ignores patches whose suffix is not the mod id), pak is a real ZIP.
- Rows are complete (all columns) so nothing is blanked.
- The 33 potion rows that equalled vanilla were dropped; only the Aesop potion row stays.
- The ground sleeping spot row (equal to vanilla) was dropped.
- The empty `item.xml` and the scratch folders `WIP Base` are gone from the module.
- Checked in game: all 66 rows and 5 constants read back as in the patch files (`docs/tests/logs/gate_krs_items_tables.log`). Sleeping spots only exist inside a level and are pending a player-stage run.

## 1.1.x (legacy, not reproducible)
Earlier Nexus releases; the published files were not compared with this version.
