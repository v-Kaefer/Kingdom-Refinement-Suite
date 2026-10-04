# Changelog

Everything done on the repository by the review and refactoring sessions, newest first. This file is about the project and its
tooling; the changes of each shipped mod are in `modules/<id>/CHANGES.md`. Status of the work: `docs/project/STATUS.md`.

Conventions: **measured** = observed in the running game, **reported** = from a third party, **default** = decided while the author was away and open to reversal.

## 2026-10-04 (eighth request): docs for both branches, push

No game run, no mod run.

- STATUS (mod lists, mod analysis, repository, waiting-for-author, a Branches table) and ROADMAP (phase 8, use what the analysis showed) brought up to date on `mods-analysis-p1-p2` and on `mods-analysis-p3-p4` (which contains the former). Both branches pushed to `origin`.

## 2026-10-04 (seventh request): branches, and the P3, P4 and unlisted mods read

Branches: `mods-analysis-p1-p2` marks the P1/P2 analysis (cc65109); this work is on `mods-analysis-p3-p4` (pushed in the eighth request). No game run, no mod run.

- `tools/audit_mods_deep.py` gained `--priorities`, `--include-unlisted` and `--tag` (separate output files), visual impact and domain columns, ReShade/ENB/SweetFX and game-data XML detection, paks up to 2.6 GB, tables up to 32 MB, header-less patches, closing of pak handles before the scratch delete, and a single `QUARANTINE.md` built from every `risk_scan*.csv`. `.bin` is no longer treated as native code (1410 and 2273 restored from quarantine); "curl" in dialog text no longer counts.
- Read 227 entries of 208 mods (P3, P4, 17 unlisted downloads): results in `MOD_ANALYSIS_P3_P4.md`, `MOD_PROFILES_P3_P4.md`, `*_p3_p4.csv`; conclusions in `MODS_REVIEW.md` section 16. P1/P2 were re-run with the same tool (A 23, B 22, C 53, D 22, E 15, X 3).
- 17 more mods quarantined (19 archives): the cheat framework (106, 771, 1193), KCSE and its plugins (2244, 2255, 2270, 2277), ASI plugins (2261, 2365, 2366), Let Me Loot (972), four ReShade/ENB packages with `dxgi.dll` (1074, 1394, 1403, 1702), Mod Order Tool (1829), a Mod Organizer plugin (2216). 23 mods in quarantine in all.
- `risk_notes.csv` now has an assessment for every quarantined and flagged mod.

## 2026-10-04 (sixth request): read-only deep analysis of the P1/P2 mods

No game run, no mod run: the archives are untrusted, so they were only listed, extracted to a scratch folder, read and deleted.

- New `tools/audit_mods_deep.py` (and `tools/audit_mods_report.py`): for each of the 138 archives of the 131 downloaded P1/P2 mods it judges the file list, scans for native code, scripts, shortcuts, dangerous Lua (comments excluded, scripts identical to vanilla ignored), path traversal and encrypted entries (also inside paks), reads the table patches against the vanilla `Tables.pak` (new, changed, identical rows; relative size of the changes), Lua and config use, text strings, install layout and 1.9.8 manifest rule, and grades each mod (A changes the most to E non-perceptive). The scratch folder is deleted (long-path safe).
- Results (generated, `docs/mods-review/`): `MOD_ANALYSIS.md`, `MOD_PROFILES.md`, `QUARANTINE.md`, `mod_analysis.csv`, `mod_tables.csv`, `mod_overlap.csv`, `risk_scan.csv`; hand notes in `risk_notes.csv`; conclusions in `MODS_REVIEW.md` section 15.
- **6 archives quarantined** (moved to `Installed_to_review/_quarantine/`, with `_quarantine_manifest.csv`): 770, 1839, 2246, 2326, 2348, 2359. Windows Security had no recorded detection. 4 more are kept with a note.
- `tools/inventory_downloads.py` and `tools/analyze_mod_archives.py` know the `_quarantine` folder.

## 2026-10-04 (fifth request): 49 pages opened from the author's list

- Opened the 49 ids the author listed (random 1.5-2.2 s apart): 47 low-priority mods of the author's own lists plus 129, 1904 and 1296 (1296 is a deleted page). 129 and 1904 were taken out of `excluded_mods.csv` (35 ids now) because the author asked for them again. The ids are batch 5 in `download_batches.csv`; they show as missing (49) until downloaded.

## 2026-10-04 (fourth request): the 365 against the folder

- `tools/inventory_downloads.py` also writes `docs/mods-review/list_vs_downloads.csv`: one row per mod of `mods_index.csv` with in-folder yes/no, the archive names, the sub-folder and the reason when it is not there. Result: 280 of 365 in the folder (279 with an archive, 1131 through its replacement 2068), 85 not: 37 excluded by the author, 47 low-priority mods of the author's lists, 1 deleted page (1296).

## 2026-10-04 (third request): 17 more removed, 1131 superseded

- The 17 undownloaded pages of the third batch were added to `excluded_mods.csv` (37 ids). New `superseded_mods.csv`: 1131 (SPOA Silver Knight Armor, deleted on Nexus) is replaced by 2068, which the author already has. `tools/inventory_downloads.py` writes the generated `NOT_DOWNLOADED.md` (85 of 365 mods by reason); the 47 low-priority mods are the author's own list members, only no page of them was opened. Missing against what was asked for: 0.

## 2026-10-04 (second request): names checked against links, 20 mods excluded

- Compared the name of every id in all lists with the Nexus API name (545 comparisons) and the downloaded file names with the page names: no wrong id; the only differences are the author's short labels. Details in `docs/mods-review/DOWNLOADS_PLAN.md`.
- New `docs/mods-review/excluded_mods.csv` (20 mods the author does not want: models, maps, tools, older variants). `tools/triage_mods.py` sets them to P4 "Excluded by the author" and leaves them out of the archives shortlist; `tools/inventory_downloads.py` never lists them as missing. Missing is now 79 (the third batch not yet downloaded).
- Rule change: no more batches in triage order; pages are opened only from a list the author gives.

## 2026-10-04: downloads reconciled and sorted (nothing opened)

No game run. The ~200 downloaded archives are untrusted (malware warnings), so nothing was extracted, installed or run.

- New `tools/inventory_downloads.py`: reads only file names, sizes and SHA-256; compares the folder with `docs/mods-review/download_batches.csv` (the 212 ids asked for: pilot, two batches of 100 tabs, shortlist). Outputs `downloads_inventory.csv`, `downloads_missing.csv`, `DOWNLOADS_STATUS.md`. Result: 204 entries, 186 mod ids, 35 missing (5 only in the Vortex folder, 1 from batch 1, 29 from batch 2), 5 ids not in the index, 3 duplicate pairs, 1 unfinished download.
- Sorted the 204 entries into `c_<category>/`, `_unmatched/` and `_incomplete/` inside `Installed_to_review` (move only, undo with `--undo`, manifest `_sort_manifest.csv`).
- `tools/analyze_mod_archives.py` now also walks those sub-folders (not run: it extracts).
- Plan and open decisions: `docs/mods-review/DOWNLOADS_PLAN.md`.
- Opened the second batch of 100 Nexus pages (2.5 s apart) before this.
- Opened 130 Nexus pages (1.5 s apart): the 30 still-missing ids plus a third batch of 100 (P3 and P4, ids not yet asked for); the third batch is `4 tabs opened, third batch` in `download_batches.csv`.
- Author's answers: the three `(1)` duplicates were moved to the Recycle Bin (SHA-256 re-checked); the five batch-0 mods were copied from the Vortex download folder (6 archives, 2017 has two). The inventory now also lists the downloaded mods that are not among the 365 (6 ids) and matches loose files by name in both directions; missing is down to 30.

## 2026-10-03 (sixth request): Nexus API results folded in, download question

No game run in this request.

- The author ran `tools/nexus_metadata.py`: 365 ids, 363 published, 1296 removed, 1131 removed by staff; the 7 nameless ids now have names (including 2345 Food and Drinks rebalance and 2362 Better Perk Descriptions). `docs/mods-review/nexus_metadata.csv` is committed; `build_mods_index.py` takes names, status and a summary from it; `triage_mods.py` reads the descriptions (new evidence class N: 347 mods, A: 18) and moves removed pages to P4. Counts now P1 3, P2 129, P3 181, P4 52; likely collisions 34.
- Checked for a download script: none exists in the repository or its tools (`MODS_REVIEW.md` section 14). New generated `docs/mods-review/DOWNLOAD_SHORTLIST.md`: 51 published mods to read as archives next, with page and Files links; no download is automated.

## 2026-10-03 (fifth request): SteamDB changed files, Nexus API tool

No game run in this request.

- SteamDB pages for 1.9.7 and 1.9.8 (saved as PDF by the author) read with `pdftotext`: `docs/engine/game-versions.md` section 4 now lists the changed files per build. 1.9.7 (build 21751157) modified `Tables.pak`, `Scripts.pak`, all localization paks and the binaries (`WHGame.dll` +1.09 MiB); 1.9.8 (build 22623230) modified only `pak.cfg` and `ipl_patch_010903.pak`. So table and script data are the same on 1.9.7 and 1.9.8, and the hidden `rpg` constant defaults (read on 1.9.6) should be re-read on 1.9.8.
- `openapi.yaml` (Nexus API 3.0.0) read. New `tools/nexus_metadata.py`: read-only calls for mod name, status, file list, versions and upload dates; no download endpoint is used; `--selftest` runs against a fake server. The author runs it with a personal key in `NEXUS_API_KEY`; `tools/triage_mods.py` adds `nexus_status`, `nexus_latest_version`, `updated_since_1.9.7` when its output exists. A personal API key pasted into the chat was not used and appears in no file; it should be revoked and replaced. `.gitignore` now ignores `.env` and `*.apikey`.
- `docs/project/DECISIONS.md` records the credentials decision; `MODS_REVIEW.md` section 13.7 explains what the API can answer.

## 2026-10-03 (fourth request): patch notes, local archives, triage of all mods

No game run in this request.

### Patch notes
- SteamDB returned HTTP 403, so the official 1.9.7 and 1.9.8 announcements were read from Steam's public news feed instead. `docs/engine/game-versions.md` section 4 now rests on them: 1.9.7 (13 Feb 2026) lists vegetation-system crash fixes and the Quilted Vest transparent-arms fix; the 1.9.8 release (14 Apr 2026) is a small bug-fix and HD-sound patch. Neither mentions modding, tables, bush collision, shield textures, icons or particles. Earlier secondary summaries are kept below the primary text.

### Mods: reading what is already on the machine
- Nexus (site, CDN and API) cannot be reached from here (403, 401) and downloading is not possible for the session; the author's Vortex download folder already holds 26 KCD archives, which were read in place (nothing downloaded).
- New `tools/analyze_mod_archives.py` writes `docs/mods-review/archive_analysis.csv`: manifest id and versions, whether the 1.9.8 engine loads it, patch suffix vs id, whole-table replacement, non-ZIP paks, collisions with the rows of `modules/*`.
- Measured: both published Nexus KRS-Items releases (1.0.0, 1.1.1) are 7z archives renamed `.pak`, with the files under `Tables\` instead of `Libs\Tables\`, suffix `KRS-items` against id `krs_items`, and `1.9.x` (1.0.0) or no manifest (1.1.1): they never applied (`docs/engine/ptf-rules.md`, `MODS_REVIEW.md` 13.2). Alternate Food Spoil 2X (1639) collides with the Aesop row of `krs_items`, Restore Riposte (1765) with both `krs_perks` rows; Hoods Over Helmets (771) ships 15 whole tables; Clean Items In Trough (1691) has an invalid manifest; Drink Sound Effects and Restore Riposte are disabled on 1.9.8.

### Triage of all 365 mods
- New `tools/triage_mods.py` (rules in the file) writes `docs/mods-review/mods_triage.csv` and the generated `TRIAGE.md`: category, KRS modules touched, evidence class (A archive read 18, B search result 41, C title 299, D id only 7), 1.9.8 load status, row collision (measured / likely / possible / none), priority (P1 3, P2 113, P3 199, P4 50), action and reason.
- `docs/mods-review/search_evidence.csv`: 42 mods whose Nexus search result title matched the id, with version, date and a one-line description (author, tested version). Resolved 7 of the 14 nameless ids (1904, 2061, 2079, 2084, 2098, 2152, 2338); 7 remain (2100, 2132, 2297, 2330, 2345, 2362, 2365).
- `MODS_REVIEW.md` section 13: method, measured findings, findings that touch `krs_qol`, `krs_items`, `krs_perks`, bow findings, cautions about unreliable summaries, and the download answer.
- Bow: published evidence that a plain `rpg_param` patch sets `BowChargeDurationMax` (mod 1100) and that a perk can carry a player-only bow change with stat-gated variants (mod 1375). New roadmap task 4.7 tests the perk route (stat-gated perk plus `perk_rpg_param_override`, no script).
- `tools/build_mods_index.py` now also takes names from the search results; `docs/README.md` indexes the new files.

## 2026-10-03 (third request): all mod lists merged

No game run in this request.

### Mod lists
- The author's browser tabs (180 Nexus mods, with names: `docs/mods-review/sources/nexusmods_abas_vivaldi.csv` and `.md`) and the notes of the session "New mods lists review" (`docs/mods-review/raw/new-mods-lists-review/`: a 290-mod title list `id_titles.csv`, `analysis.md`, `verification.md`) were copied into the repository exactly as written. The two text lists (`mods_to_verify.txt`, `Kingdom Come Mods.txt`) are unchanged.
- Finding: of the 180 Vivaldi tabs only 56 were in the two text lists; **124 mods were missing from the project**. With the 5 further ids that only appear in the screenshots and the workspace and checking finds, `docs/mods-review/mods_index.csv` now has **365 rows** (201 from the text lists, 129 new, 24 workspace-only, 11 found while checking), with exact tab titles as names, a keyword category, the PTF flag, a mechanical `triage` column and the reviewing session's note per mod.
- `tools/build_mods_index.py` rewritten to read every list (text lists, Vivaldi tabs, title list, workspace, annotations); names prefer the exact tab title.
- `docs/mods-review/MODS_REVIEW.md` section 12: counts, triage table, categories, overlap clusters, where the new mods meet `krs_perks`, `krs_items`, `krs_qol` and archery, fix candidates (new: 2332, 1558, 1782, 2343; not game fixes: 1424, 1426, 2279, 1991), out-of-scope and tools, and the open items (40 text-list ids still without a title, 5 still unresolved ids). Nothing was removed from earlier sections.
- The corrections of the verification session were applied in `annotations.csv` (titles for 2372 and 2381, PTF examples 1860-1864, 1893, 2005, 2021, translation families, cfg and KCSE notes, a note that the 1227 page is now titled "V3" while the installed file and `Requirements.md` say V2).
- Everything about these mods is **title-based**: Nexus pages return HTTP 403 and no archives are available, so no verdict exists. The first review's catalog (130 mods), `unverified.md` and `mods.csv` remain missing.

### Other
- Reported by the author, not yet tried: the 1.9.8 EULA screen can be passed with `Q` (`docs/engine/game-versions.md`, `docs/tests/README.md`).
- `tools/check_docs.py` skips `mods-review/sources/`.
- **Repository state found:** the remote moved while the branch was being worked on (PR #1, PR #2 "Document test install update to KCD 1.9.8" and PR #3 develop into main are merged; `dev` was renamed `develop`; `docs/CI_PLAN.md` exists on `claude/compassionate-proskuriakova-002ee9`). This branch still holds the old layout on the remote. Merging `origin/develop` into the branch was attempted and blocked by the session's permission check, so it was **not done**; the local commits (`5d581d9`, `b0a4cc9` and this request's) are unpushed.

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
