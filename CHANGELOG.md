# Changelog

Everything done on the repository by the review and refactoring sessions, newest first. This file is about the project and its
tooling; the changes of each shipped mod are in `modules/<id>/CHANGES.md`. Status of the work: `docs/project/STATUS.md`.

Conventions: **measured** = observed in the running game, **reported** = from a third party, **default** = decided while the author was away and open to reversal.

## 2026-10-03 (second session): 1.9.8, mod review, docs reorganization

### Game version 1.9.8
- The test install was updated to 1.9.8. The module gate **passes on 1.9.8**: 73 of 73 reachable checks, 8 of 8 patch files applied (`docs/tests/logs/gate_manifest_probe_1.9.8_tables.log`). Nothing is lost by the update for the three modules.
- **Measured:** the engine disables a mod whose manifest lists only older versions (`doesn't support game version '1.9.8', it will be disabled`); changing that line is enough for it to load and patch (tested with five synthetic mods and a copy of Restore Riposte with only the version line edited); a manifest without `<supports>` always loads; of the wildcards only `1.9.*` matched, `1.9.x` did not. Full table in `docs/engine/game-versions.md`.
- **Measured:** on 1.9.8 the author's Vortex mods Restore Riposte (1765) and Drink Sound Effects are disabled by their manifests; Persistent Arrows and Volumetric Fog Shadows (`1.9.*`) and the mods without restriction load.
- **Measured:** `mm_main/OnStart` is no longer sent on 1.9.8 (new EULA and account screens). The harness now also starts its table stage on `sys_startup/OnEnd` (`tools/harness/krs_harness.lua`).
- Module manifests now list 1.9.6, 1.9.7 and 1.9.8 (`modules/*/mod.manifest`, `tools/seed_modules.py`, `tools/harness/build_harness.py`). The legacy KRS-Items manifest value `1.9.x` would have been disabled on 1.9.8.
- New `tools/harness/build_manifest_probe.py`: installs the manifest probe mods (and optionally a Riposte copy) and removes them.
- Game runs: the earlier request on 1.9.8 used 3 (manifest block, second attempt, interrupted); this request allowed 5 and used 2 (the probe run and a check that the gate still works after the reorganization). See `docs/tests/results/README.md`. Every run restored `Mods/mod_order.txt` and removed the test mods; no save was touched.

### Mod lists and review
- `docs/mods-review/MODS_REVIEW.md` section 11: the section 6 fix candidates and the section 5 version watchlist re-checked against 1.9.8. Measured: the Raven's beak / spiked warhammer icons are still swapped in the current tables (mod 1693 still needed); the 26 bush models of mod 591 are byte-identical in every pak up to 1.9.8. Reported: official 1.9.7 notes fix Quilted Vest transparent arms; the 1.9.7/1.9.8 notes mention nothing else relevant. Nexus pages themselves are blocked (HTTP 403); mod facts come from search summaries.
- `tools/scan_workspace_mods.py` and `docs/mods-review/workspace_mods.csv`: 41 mods found in the workspace folders and the Vortex deployment by Nexus id; 32 of them were not in either list.
- `docs/mods-review/mods_index.csv` rebuilt by `tools/build_mods_index.py`: 248 rows (201 from the two lists, 32 workspace-only, 15 outside both: the 8 adjacent mods of the review and 7 found while checking) with new columns `scope`, `in_workspace`, `check_1.9.8`, `check_source`; `annotations.csv` extended (names, authors, versions, 1.9.8 verdicts for 18 mods).

### Documentation reorganized (plan: `docs/project/DOCS_PLAN.md`)
- New layout: `docs/project/`, `engine/`, `modules/`, `mods-review/`, `data/`, `tests/{results,logs}`, `archive/legacy/`, with an index in `docs/README.md`. Files moved with `git mv`; `PTF_FINDINGS.md` split into `engine/ptf-rules.md` and `engine/lua-and-constants.md`; `OBJECTIVES.md` split into objectives, `STATUS.md`, `DECISIONS.md`, `PERMISSIONS.md`; the roadmap lost its progress table to `STATUS.md`.
- Every Markdown file in `docs/` has a status block (date, kind, trust, game version); generated files carry a GENERATED marker (`tools/audit_tables.py` and `tools/lua_api_check.py` now write it).
- `tools/paths.py` (folder names in one place) used by `gate.py`, `build_mods_index.py`, `scan_workspace_mods.py`, `check_docs.py`; the other scripts keep literal paths, updated to the new layout.
- `tools/check_docs.py`: broken links, missing paths, missing status blocks, files missing from the index, stale `STATUS.md`.
- Legacy documents of the main checkout copied (not moved) into `docs/archive/legacy/`. The main checkout, its root files and `Mods WIP folder` were not modified. All test logs were kept.
- `.gitignore`: `docs/data/table-audit/table_audit.json`, `dist/`.
- This file added.

## 2026-10-02 (first session): objectives, tools, in-game tests, modules

### Commits
`ab95924`, `f028457`, `935a2af` on `dev` (not pushed); `b5a48d9` and `5d581d9` on the branch of draft PR #1 (the PR was opened, the second commit is not pushed). Branches `krs-perks`, `krs-qol`, `krs-bow` were moved to `dev`; `krs-items` was left alone (checked out with uncommitted changes in the main checkout).

### Analysis and documents
- Reviewed every non-replica file; wrote the objectives, principles and module scope that nothing stated in one place, and the ownership table (`docs/data/ownership.csv`, one owner per changed row).
- `tools/audit_tables.py` (compares every table patch with the vanilla `Tables.pak`), `tools/check_ownership.py`, `tools/check_patch_names.py`.
- Potions: dataset, formula check, analysis (the old pipeline crashes and would overwrite designed potions), 33 real-world sources with read status, 29-claim ledger. Scope set by the author: light touch on top of the base game (`docs/modules/potions/`).
- Bow: feasibility study of what Lua and hidden constants can do, API existence check (`docs/modules/bow/FEASIBILITY.md`, `docs/engine/lua-api-check.md`); the Cheat mod is not needed. Draw speed from Strength and Agility is possible in principle; the live read of the constants during a bow draw is **untested**.
- `docs/project/ROADMAP.md`: phases 0 to 6.

### In-game harness and measured rules (1.9.6)
- `tools/harness/` builds test mods and a runner that starts the game, reads tables and constants back through Lua, and stops it; it restores `mod_order.txt`.
- Ten measured table-patch rules, among them: patch file suffix must equal the mod id; a partial row blanks the other columns; the later mod's row replaces the whole row; a `.pak` must be a ZIP; hidden constants can be set by an `rpg_param` row and by `RPG.<Key> = value` (`docs/engine/ptf-rules.md`).
- 588 of 597 documented constants exist (406 hidden), 9 do not (`docs/engine/rpg_constants_runtime.csv`).
- Finding: none of the repository's table patches loaded as packaged (suffix and id mismatch, a 7z archive renamed `.pak`); the same files with the suffix renamed did.

### Modules (phases 0 to 3)
- `modules/krs_items` 2.0.0, `krs_perks` 1.0.0, `krs_qol` 1.0.0 built from the legacy files by `tools/seed_modules.py` (complete rows, no-op rows dropped, localization paks); `tools/build_module.py` builds the mod folders and Vortex-ready archives.
- `tools/gate.py` + `tools/harness/build_gate.py` + `krs_gate.lua`: install, start the game, read every patched row back, assert. On 1.9.6: 73 of 73 reachable checks passed, alone and on top of the author's Vortex mod list. 9 rows in level-only tables (perks, sleeping spots, overrides, `skill2item_category`) are **not yet verified**: they need Continue pressed (`--mode full`).
- Defaults chosen while the author was away: separate modules; Enhanced Eyes left out; repairs in QoL with the price doubled (1.3, Hardcore 1.8) and the repair-kit limits untouched; reading XP stays 5; Riposte shipped as `krs_perks`; carry capacity 4 to 5 (permission still pending, do not publish).

### Not done
- Bow live-read test and the player-stage tests (need a loaded save; screen control was declined or unavailable).
- Potion rebalance numbers (method awaits approval); module READMEs in other languages; pushing `dev`; release packaging (phase 6).
