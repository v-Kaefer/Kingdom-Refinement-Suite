# Tables Workspace Mapping

Date: 2026-05-18

This folder is not a standalone mod family. It is the shared extracted game-data workspace used as source material for multiple KCD mods in this repo.

## What This Workspace Contains

- `Tables/Tables/...`:
  - the extracted vanilla-style table tree used as reference input
  - includes `item`, `rpg`, `quest`, `combat`, `inventory`, `ui`, `ai`, and related subtrees
- `Tables/Scripts/...`:
  - the extracted script/reference tree used by the Lua and XML tooling
- `Tables/Scripts.pak`:
  - packaged script archive counterpart to the extracted script tree

## Why It Matters

- `Realistic Potions` reads directly from this workspace layout.
- Several `KRS-Items`, `KRS-QoL`, and `KRS-Perks` experiments appear to use it as a source baseline.
- It is the repo’s closest thing to a canonical vanilla reference dump.

## Integration Use

Use this workspace to:

- compare values against vanilla
- extract target XML rows for PTF patching
- validate whether a candidate mod is changing item, rpg, quest, combat, or script data

## Confidence

- This mapping is `confirmed` at the structural level, but it is intentionally high level.
- The tree is too broad to treat as a single mod package.

