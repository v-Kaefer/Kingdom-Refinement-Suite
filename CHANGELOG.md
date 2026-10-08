# Changelog

Everything done on the repository by the review and refactoring sessions, newest first. This file is about the project and its
tooling; the changes of each shipped mod are in `modules/<id>/CHANGES.md`. Status of the work: `docs/project/STATUS.md`.

Conventions: **measured** = observed in the running game, **reported** = from a third party, **default** = decided while the author was away and open to reversal.

## 2026-10-08: wash confirmed in game, torch return, Reshield, what was learned

Played by the author in the replica game (1.9.8): the trough wash animation works, gloves come off, the torch comes back, Reshield (2313) and the wash work together.

- `krs_exploration_wash`: the player's torch is put back in hand after the wash (`so_water_tube.diff`). 2372 took it off and only gave the glove back.
- `troughwash.lua` pauses Reshield while the wash runs (`Reshield.enabled`, restored 1.5 s after the wash), so the shield is not put in hand while the torch is off. Reshield's code is not touched.
- `krs-qol`: Reshield documented as an optional companion with the sha256 of the author's two files; `tools/build_qol_reshield.py` reads them from the author's archive. Nothing of the mod is stored in the repository; permission is not asked yet.
- Log check of the play session (`kcd.log`): both packages accepted for 1.9.8, paks opened, init scripts loaded, `shrine and cross XP installed`, `nest XP installed`, no "Invalid animation DB", no Lua error from KRS code. The XP scripts write nothing when they give XP, so their effect is **not** verified yet.

Learned (for the next iterations):
- A mod that unequips something must give it back. Read a mod's behaviour trees for `UnEquipItem` without a matching `EquipItem` (2372 had that bug).
- Do not edit a third-party script to make two mods agree. Look for the switch the script already has (`Reshield.enabled`) and flip it from our own wrapper, with an `if Reshield then` guard so the soft dependency costs nothing when the mod is absent.
- Text changes are kept as unified diffs against the game's own file: apply with `text_cut.py apply`, edit the output, regenerate with `text_cut.py make`. Hand-editing hunk counts is error-prone. Check the result parses (`ElementTree`) before building.
- A menu-stage run (`run_game_test.ps1` with `krs_adbtest`) proves that packages load, the animation database parses and the Lua files compile. It cannot show behaviour that needs a character. `harness done=False` in its report is a known false alarm when the end marker is in the log.
- `python -I` removes the current folder from the path, so relative paths to our own scripts fail inside `-c`; use absolute paths.
- The worktree-isolated session refuses computed paths, heredocs and chained commands: write scripts with the file tool and run plain commands.
- Third-party material stays out of the repository: read from the author's archive at build time, check sha256, mark the package "do not publish" until permission is answered (`docs/project/PERMISSIONS.md`).
- Open: 2294 variant, 21 operations of 2049 that could not be rebased (14 `CombatBlockBroken`, 3 `LadderGetOff` changed in structure, 4 `CombatStealthHitSuccess` gone), XP effect in play, torch lost if the wash is interrupted, permissions for 2372 and Reshield.

## 2026-10-06 (second part): 2049 rebased and run in the replica game

- `tools/adb_cut.py rebase`: three-way merge inside each fragment of a cut made on an older game file. 2049 (built on the original file): 307 of 324 operations kept, 161 identical and 146 moved onto the current fragments (145 of them under a longer key because the game's patches added `oppMale+oppFemale` to FragTags); 21 left out (structure changed by the game 17, fragment gone 4).
- Game test in the replica (`E:\Kingdom-Refinement-Suite\Mods WIP folder\KingdomComeDeliverance`, menu stage, 1.9.8): new `tools/harness/krs_adbtest.lua` and `build_adbtest.py`. Wash + rebased 2049 gives the same log as the baseline; a control file cut at 3 MB gives `XML reader: unclosed token` and `Invalid animation DB for actor 'DummyTarget'` from startup on. Logs in `docs/tests/logs/adbtest_*`. Measured: the game parses a mod's `kcd_male_database.adb` at startup. `krs_adbtest` was removed afterwards and `mod_order.txt` restored.

## 2026-10-06: krs_exploration merge tests

No game run. Archives read through scratch folders that were deleted.

- Branch `krs-exploration-merges` (stacked on `krs-exploration`): cuts of 1563, 2276 and 2049 in `modules/krs_exploration/src/merge_tests/`, with a README of the cuts, the commands and the results. Merging them with the wash cut gives one animation database with no conflict between cuts; 163 of 2049's 324 operations are stale (fragments the game's patches changed) and need an attribute-level rebase; 2294's variant is still to be chosen. 2045 is the same file as 1563 and counts as one.
- `tools/adb_cut.py`: `--skip-stale` and `--report` for cuts made on an older base.

## 2026-10-06: krs_exploration prepared

No game run, no mod run. The Trough Washing Animation archive was listed, its `.pak` extracted to a scratch folder inside `dist/` and deleted.

- New module `modules/krs_exploration` (branch `krs-exploration`): `Scripts/Startup/krs_exploration.lua` with the shrine/cross reading XP and the nest XP (ideas of 1518 and 1519, code written for the module, wrapping `CaptionObject:OnUsed` and `Nest.Client:OnHit`).
- Optional package `krs_exploration_wash` from cuts of 2372 in `src/wash/` (2 animation fragments, 3 text diffs, 1 Lua file, a list of 21 binary assets with sha256). Left out of 2372: 187 crossbow fragments, the crossbow tags, 157 crossbow event blocks, the boiler eating animations.
- New `tools/adb_cut.py` (fragment-level cuts of an animation database, applied to the game's file with a check that the result is the game's fragments plus exactly those changes), `tools/text_cut.py` (diffs applied to the game's own text files; the result reproduces the mod's file byte for byte for so_water_tube and workbehaviors) and `tools/build_exploration.py`.
- `docs/project/PERMISSIONS.md`: 1518, 1519 and 2372 recorded as not requested; the wash package must not be published.

## 2026-10-04 (tenth request): illustrated PDF report

No game run, no mod run, no archive opened, nothing downloaded.

- New `tools/build_report_pdf.py`: builds `docs/mods-review/RELATORIO_MODS_A-E.pdf` (15 pages, Portuguese) from the generated CSVs. Charts and diagrams are inline SVG written by the tool itself (no chart library, no web font, no CDN); the page is printed by the local Edge or Chrome in headless mode, so nothing is installed.
- Contents: cover, executive summary, the method as a pipeline diagram, the A-E grades, the 17 sub-categories stacked by grade, an effect-against-build scatter, PTF patch versus whole-table replacement side by side, the suffix rule with the 1883 case, the four kinds of intersection with the rule-6 load-order diagram, the most contested tables, the 883 replacement case, the KRS collisions drawn on the suite's own real patch file, practical decisions and the limits.
- Code examples are real files, not invented: `modules/krs_qol/Data/Libs/Tables/rpg/rpg_param__krs_qol.xml` and `modules/krs_qol/mod.manifest`. Palette validated with the data-viz checker (adjacent-pair CVD and normal-vision floors pass; the contrast warning is answered by direct labels on every segment).
- Correction while building it: the KRS-shared row count is **55 readable rows**, not 56. The earlier figure counted the item that `MOD_PROFILES.md` cuts in the middle at 300 characters. `MODS_REVIEW.md` section 17, `STATUS.md` and the previous changelog entry were corrected.

## 2026-10-04 (ninth request): where the graded mods intersect

No game run, no mod run, no archive opened: derived from `mod_overlap.csv`, `mod_tables.csv`, `mod_subcategories.csv` and the KRS lines of `MOD_PROFILES.md`.

- New `tools/mod_intersections.py`: crosses the 89 graded mods that write table rows against each other. **1384 pairs intersect**: 442 write at least one of the same rows, 942 more write into the same table without sharing a row, and 296 of the pairs include a mod that replaces one of those tables whole. Generated: `docs/mods-review/MOD_INTERSECTIONS.md`, `mod_intersections.csv` (one row per pair, with the tables and the shared-row count).
- The three kinds are separated because the game treats them differently (`docs/engine/ptf-rules.md`): a shared row is replaced whole and the last mod in `mod_order.txt` wins (rule 6, and rule 5 means it can blank columns the other mod never touched); the same table with different rows coexists; a file without the PTF suffix replaces the table and overrides every other mod on it.
- Listed per sub-category (which mods of one group are strict alternatives), across sub-categories (337 pairs that share rows while doing different jobs), per replacing mod (883 overrides 87 of the other 88 table-writing mods; 1260 overrides 40; 802, 804 and 1334 override 38 each), and per contested row (`CombatAutoSPBWeight` is set by 12 mods, ten `ammo` rows by 9).
- **25 mods write 55 readable rows that `krs_items`, `krs_qol` or `krs_perks` also write** (1950's list is cut at 300 characters in the source, so there are more), listed per module: `RepairPriceModif` (883, 1842, 2173, 2188, 2340), Aqua Vitalis `food` (651, 1926, 2011, 2124, 2210, 2299, 2345), `HerbGatherSkillToRadius` (1260, 1558, 1938, 2210, 2299), `StrengthToInventoryCapacity` (651, 883, 1839, 1860), `ReadingXpPerHour` (1260, 1334, 1558, 1572).
- Conclusions in `docs/mods-review/MODS_REVIEW.md` section 17. Data gap recorded there: `krs_collisions` is not a column of `mod_analysis.csv` and the profiles line is cut at 300 characters, so 1950's KRS list is incomplete until the deep analysis is re-run.

## 2026-10-04 (eighth request): sub-categories of the A-E mods and a ranking inside each

No game run, no mod run, no archive opened: this works only on the CSVs the deep analysis already wrote.

- New `tools/subcategorize_mods.py`: puts each of the **129 mods graded A to E** into one of **17 sub-categories** of mods that write into the same tables (PTF) or the same kind of file, and ranks them inside each of the **33 grade/sub-category groups**. Every changed row is counted towards the system of its table (`rpg_param` is split over the systems of its changed keys; `buff` rows are shared out over the mod's other systems); a mod with no table row is grouped by the file it does change (Lua, .cfg, non-table XML, assets, text). Generated: `docs/mods-review/MOD_SUBCATEGORIES.md`, `mod_subcategories.csv`.
- Two scores, 0 to 100: **effect** (rows, tables, relative size of the change, perceptibility, depth layers, Lua/config size) and **build** (loads on 1.9.8, correct PTF suffixes, patches inside `Libs/Tables`, whole-table replacements, dropped vanilla rows, risk); rank = 0.55 x effect + 0.45 x build. The native mods have no measurable effect and are ranked by build and risk only.
- Two counting corrections against `MOD_ANALYSIS.md` (both counts are kept in the CSV): a patch that an archive ships several times as alternative options (2X/3X/5X folders) counts **once**, and tables are counted as distinct vanilla tables instead of table files. 2294 Faster Combat: 2985 rows in 55 files there, 1300 rows in 10 tables here; 284, 651, 1260, 1334, 1483, 1563, 1736, 1862, 1863 and 2124 are also affected.
- The "suffix is not the mod id" finding is split by evidence: a fault where `mod.manifest` states the id (1883 Better Pickpocket - FIXED, whose patch the game therefore never loads), a doubt to confirm per sub-mod where the deep analysis had to derive the id from the mod name and the archive bundles several sub-mods with one manifest each (284, 1578, 1736, 1893, 2124).
- Conclusions in `docs/mods-review/MODS_REVIEW.md` section 16: the archery group of nine mods that set the same hidden constants, the three unequal Perkaholic packages, the interchangeable merchant mods (1853, 2165), three mods that change nothing readable (1652, 1673, 1996), and the index labels that disagree with the files (2188, 2210, 284, 2338).

## 2026-10-04 (seventh request): branch for the P1/P2 analysis, docs brought up to date

No game run, no mod run.

- Branch `mods-analysis-p1-p2` marks the state after the read-only analysis of the downloaded P1/P2 mods (131 mods; 6 archives quarantined).
- `docs/project/STATUS.md`: mod lists, mod analysis, repository and waiting-for-author bullets brought up to date, and a Branches table. `docs/project/ROADMAP.md`: new phase 8 (use what the analysis showed).

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
