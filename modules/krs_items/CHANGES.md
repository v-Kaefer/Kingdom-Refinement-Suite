# krs_items changes

## 2.0.0
- Repackaged: mod id `krs_items`, every table patch named `<table>__krs_items.xml` (the game ignores patches whose suffix is not the mod id), pak is a real ZIP.
- Rows are complete (all columns) so nothing is blanked.
- The 33 potion rows that equalled vanilla were dropped; only the Aesop potion row stays.
- The ground sleeping spot row (equal to vanilla) was dropped.
- The empty `item.xml` and the scratch folders `WIP Base` are gone from the module.
- Checked in game: all 66 rows and 5 constants read back as in the patch files (`docs/tests/gate_krs_items_tables.log`). Sleeping spots only exist inside a level and are pending a player-stage run.

## 1.1.x (legacy, not reproducible)
Earlier Nexus releases; the published files were not compared with this version.
