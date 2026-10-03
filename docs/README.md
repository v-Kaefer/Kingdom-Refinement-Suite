# Documentation index

> **Status date:** 2026-10-03 | **Kind:** index | **Trust:** derived | **Game version:** -

Everything about the Kingdom Refinement Suite (KRS) except the shipped mods themselves (`modules/<id>/`). Layout and rules: `project/DOCS_PLAN.md`.

## Reading order

1. `project/OBJECTIVES.md` - what the suite is for and what each module owns.
2. `project/STATUS.md` - where things stand now; `../CHANGELOG.md` - what was done, newest first.
3. `engine/ptf-rules.md` and `engine/game-versions.md` - how the game behaves (measured); read before touching a module.
4. `project/ROADMAP.md` - the phases; `project/DECISIONS.md` - what was decided and what is open.

## Where things are

| Folder | Kind | Contents |
|---|---|---|
| `project/` | stable and dated project text | `OBJECTIVES.md`, `ROADMAP.md`, `STATUS.md` (edited every session), `DECISIONS.md`, `PERMISSIONS.md`, `DOCS_PLAN.md` |
| `engine/` | measured game behaviour | `ptf-rules.md`, `lua-and-constants.md`, `game-versions.md`, `lua-api-check.md` (generated), `rpg_constants_runtime.csv` |
| `modules/` | design notes | `bow/FEASIBILITY.md` (what Lua and hidden constants can do), `potions/ANALYSIS.md` and `potions/SOURCES.md` (formula analysis, real-world sources; datasets and the claims ledger beside them). Items, Perks and QoL are described in `modules/<id>/README.md` at the repo root and in `data/ownership.csv` |
| `mods-review/` | the third-party mod lists | `MODS_REVIEW.md` (conclusions), `mods_index.csv` (generated), `annotations.csv`, `workspace_mods.csv`, `sources/` (the author's lists), `raw/` (notes from another session, incomplete) |
| `data/` | tables the tools read or write | `ownership.csv`, `table-audit/TABLE_AUDIT.md` (generated) |
| `tests/` | evidence | `README.md` (how to run), `results/` (one line per game run), `logs/` (raw) |
| `archive/` | superseded | `legacy/` copies of old documents with a reason each |

Not in `docs/` on purpose: `Params Reference.md` (in the `Mods WIP folder`), the repo-root `README.md`, `Requirements.md`, `CONTRIBUTING.md`, `FOLLOW_UP.md` of the main checkout (the author's files; copies for reference are in `archive/legacy/`).

## Conventions

- Every Markdown file in `docs/` starts with a status block: `Status date`, `Kind`, `Trust` (**measured** in game, **derived** from files, **reported** by a third party, **proposal**), and the game version for engine and test files.
- Generated files say `GENERATED` at the top and are rebuilt by the named tool, never edited by hand.
- A fact has one home; other files link to it. File names: lower-case with hyphens for prose, upper-case for the few anchors.
- Moves are done with `git mv`; `python tools/check_docs.py` checks links, the index and the status blocks.
- Scripts take folder names from `tools/paths.py`.

## Documents and tools

| Tool | Purpose |
|---|---|
| `tools/build_module.py`, `tools/gate.py` | build a module; run it in the test game and read every patched row back |
| `tools/check_patch_names.py` | pre-flight check of patch names, mod ids, row completeness and pak format |
| `tools/audit_tables.py`, `tools/check_ownership.py` | what each patch really changes versus vanilla; ownership consistency |
| `tools/build_mods_index.py`, `tools/scan_workspace_mods.py` | rebuild `mods-review/mods_index.csv`; list the mods found in the workspace |
| `tools/potion_dataset.py`, `tools/potion_model_check.py` | potion dataset and formula check |
| `tools/lua_api_check.py` | checks that the functions and `RPG.<Key>` names in a Lua mod exist |
| `tools/harness/` | the in-game test mods and runner (`build_gate.py`, `build_manifest_probe.py`, `run_game_test.ps1`, ...) |
| `tools/check_docs.py`, `tools/paths.py` | documentation checks; where things live |

## Commands (from the former objectives)

The worktree does not contain the game replica, so point `--root` at the main checkout.

```bash
python tools/audit_tables.py --root "E:/Kingdom-Refinement-Suite" \
    --game "E:/Kingdom-Refinement-Suite/Mods WIP folder/KingdomComeDeliverance" \
    --out docs/data/table-audit
python tools/check_ownership.py        # sources default to '^modules/'
```

To include another branch, extract it first and pass it as an extra source:

```bash
git archive dev KingdomRefinementSuite | tar -x -C /tmp/dev
python tools/audit_tables.py ... --extra "branch-dev/KingdomRefinementSuite=/tmp/dev/KingdomRefinementSuite"
python tools/check_ownership.py --sources '^(modules/|branch-dev)'
```

Limits of the audit: vanilla is the replica's `Tables.pak` (version recorded in `engine/game-versions.md`); `.7z`/`.rar`
archives and `KRS-Items.pak` in `Para publicar (TEMP)` could not be read; the game was run only from 2 Oct 2026; results are in `tests/results/` and the rules in `engine/`.
