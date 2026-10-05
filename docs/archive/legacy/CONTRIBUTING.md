# Contributing

This repository is a mod suite workspace for Kingdom Come Deliverance.

## Working Rules

- Keep changes scoped to one source folder or one module at a time.
- Prefer folder-level mapping notes before merging a mod into the suite.
- Treat extracted `.pak`, `.zip`, `.rar`, and `.7z` sources as reference material until their contents are inspected.
- Do not overwrite unrelated dirty files in the working tree.
- Preserve the existing mod packaging structure unless a folder is explicitly being normalized.

## Folder Mapping Workflow

1. Inspect the folder contents and identify the mod family.
2. Read the manifest, readme, and any changed XML or script files.
3. Record the purpose, touched tables, and suite fit in a markdown mapping file in that folder.
4. Mark entries as `confirmed` only when the contents were actually inspected.
5. Mark entries as `inferred` when the purpose comes only from archive name or manifest text.

## Integration Notes

- `KRS-Items` is for item, food, sleep, and related player balance changes.
- `KRS-QoL` is for quality-of-life and light gameplay tuning.
- `KRS-Perks` is for perk expansions and perk balance changes.
- Cosmetic-only mods should stay out of gameplay modules unless there is a specific reason to keep them.

## Resume Code

If you are continuing from the latest mapping session, use:

`KRS-RESUME-20260518-01`

codex resume 019e38e9-6f87-73b2-a620-9d3a9b387323