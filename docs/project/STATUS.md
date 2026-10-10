# Status

> **Status date:** 2026-10-06 | **Kind:** project | **Trust:** derived | **Game version:** 1.9.6 and 1.9.8

The only file that is edited every session. Stable goals are in `OBJECTIVES.md`, the plan in `ROADMAP.md`, decisions in `DECISIONS.md`, what the engine does in `../engine/`.

## Now

- **Game:** the test install is 1.9.8. The three modules pass the menu-stage gate on 1.9.8 (73/73) and on 1.9.6.
- **Manifests:** list 1.9.6 to 1.9.8; the engine disables mods whose list lacks the running version, and editing the line is enough to load them (`../engine/game-versions.md`).
- **Docs:** reorganized (`DOCS_PLAN.md`); `../../CHANGELOG.md` has the full history.
- **Mod triage:** every mod is classified and prioritized (`../mods-review/TRIAGE.md`, `mods_triage.csv`); 26 local archives were read (measured), 42 mods have search evidence, the rest is title-based. The published KRS-Items releases on Nexus never applied; they must be replaced by `modules/krs_items`.
- **Mod analysis (4 Oct 2026):** the downloaded P1/P2 mods (131 mods, 138 archives) were read statically (listed, extracted to a scratch folder, read, deleted; nothing run), graded (A 22, B 22, C 52, D 14, E 25, X 3) and risk-scanned; 6 archives are quarantined (`../mods-review/MOD_ANALYSIS.md`, `MOD_PROFILES.md`, `QUARANTINE.md`, `MODS_REVIEW.md` section 15). No game run was made. P3 and P4 follow on branch `mods-analysis-p3-p4`.
- **Mod sub-categories (4 Oct 2026):** the 129 mods graded A to E are grouped into 17 sub-categories of mods that write into the same tables or the same kind of file, and ranked inside each of the 33 grade/sub-category groups by an effect and a build score (`../mods-review/MOD_SUBCATEGORIES.md`, `mod_subcategories.csv`, `MODS_REVIEW.md` section 16; tool: `tools/subcategorize_mods.py`). Read-only: no archive was opened again. It also corrects two counts of `MOD_ANALYSIS.md` (repeated option patches, table files versus distinct tables) and found one mod whose patch the game never loads (1883) and three that change nothing readable (1652, 1673, 1996).
- **Mod intersections (4 Oct 2026):** 1384 pairs of the graded mods intersect (442 on the same rows, 942 on the same table only, 296 involving a whole-table replacement), and 25 mods write 55 readable rows that a KRS module also writes (1950's list is cut in the source) (`../mods-review/MOD_INTERSECTIONS.md`, `mod_intersections.csv`, `MODS_REVIEW.md` section 17; tool: `tools/mod_intersections.py`). 883 alone overrides 87 of the other 88 table-writing mods. Each KRS-shared row is an open decision for the suite.
- **Grade B first pass (8 Oct 2026):** the 21 Grade B mods were read file by file and cell by cell against game 1.9.8 and the 2020 reference tables (nothing run, nothing moved to `Reviewed_Mods`): 8 sub-categories, ranking, 20 balance articles, 78 measured pairs, 18 open questions (`../mods-review/GRADE_B.md`, `GRADE_B_REVIEW.html`, `grade_b_*.csv`; tools: `tools/grade_b_extract.py`, `tools/build_grade_b_page.py`). Decisions on Q1 to Q18 wait for the author.
- **Gluttony skip cost (10 Oct 2026):** the engine charges no hunger during Wait or sleep (measured); the module `modules/krs_skipcost` (prototype in `tools/harness/skipcost/`) charges rate x hours x factor by posture (standing 0.75, sitting 0.5, lying 0.5) and was checked for Wait in game; sleep, reading and fainting are untested with the mod; now the module `modules/krs_skipcost` 0.1.0 (Gluttony Rebalanced package).
- **Gluttony eating and waiting measured (10 Oct 2026):** `max_status` is not a ceiling; eating adds the whole nutrition at once; waiting 8 h costs no hunger or energy; sleeping still unmeasured; KRS Items hunger parameters kept, beds held out of v1.
- **Gluttony Rebalanced v1 direction (10 Oct 2026):** day stays at 96 min, sleep untouched, hunger every 4 to 6 world hours; candidate `DigestionSpeed` x1.05 to x1.57 of the game with a threshold of 64 to 67; five in-game tests (E1 to E5) before fixing values; the beds of Exploration Reworked vs untouched sleep is open.
- **Gluttony Rebalanced, world hour of 6 real minutes (10 Oct 2026):** the day was measured in game: ratio 15, 96 real minutes (hour = 4 minutes); the plan compensates x1.5 for an hour of 6 minutes (ratio 10, day 144 min); `Calendar.SetWorldTimeRatio` works from a script. Open: the hunger bar thresholds and targets in real minutes, and whether a set ratio survives loading, sleeping and dialogue.
- **Gluttony Rebalanced base analysis (9 Oct 2026):** hunger, shelf life and a 4 to 6 minute day against the game's values (`../modules/gluttony/ANALISE_BASE.html`); nothing tested in game; the day length and whether `Calendar.SetWorldTimeRatio` persists are the open points.
- **KRS-Items scope (9 Oct 2026):** the better beds moved to `krs_exploration` (unreleased, not yet read back in game); `krs_items` keeps books, reading XP, digestion, starvation and the Aesop potion. Realistic Items (Nexus 2017) copied to `Mods WIP folder/Items/Realistic_Items_2017/` with a workbench of the digestion and Aesop rows (`KRS-Items_workbench/`).
- **Grade B batch 1 (9 Oct 2026):** second pass on 1483, 1639, 2011, 2345 and 1105 (food spoilage, nutrition, snack buffs, service prices) with four decisions for the author (`../mods-review/GRADE_B_LOTE1.html`, `grade_b_lote1_food.csv`; tool `tools/build_grade_b_lote1.py`). 85, 770 and 1009 were moved to `Mods WIP folder/Perks` (770 into `Perks/_quarantine`).
- **Illustrated report (4 Oct 2026):** `../mods-review/RELATORIO_MODS_A-E.pdf`, 15 pages in Portuguese, generated by `tools/build_report_pdf.py` from the CSVs (inline SVG charts, printed by a local headless Edge/Chrome; no library installed, no network).
- **krs_exploration (6 Oct 2026, branch `krs-exploration`):** new module prepared, not yet run in the game: core package with two XP scripts (shrine/cross reading XP, nest XP; ideas of 1518 and 1519, own code) and an optional package `krs_exploration_wash` assembled from cuts of Trough Washing Animation (2372) applied to the game's own files at build time (`modules/krs_exploration/README.md`, `tools/build_exploration.py`, `tools/adb_cut.py`, `tools/text_cut.py`). The wash is permission-pending and must not be published. Merge tests with cuts of other animation mods continue on branch `krs-exploration-merges`.
- **krs_exploration merge tests (6 Oct 2026, branch `krs-exploration-merges`):** cuts of 1563 (also stands for 2045), 2276 and 2049 on top of the wash cut build one animation database without conflicts. 2049, built on the original game file, was rebased onto the current one attribute by attribute (`tools/adb_cut.py rebase`): 307 of its 324 operations kept (161 identical, 146 moved), 21 left out. Wash + rebased 2049 was run in the replica game at the menu stage: accepted, same log as the baseline, while a truncated control file is rejected at startup with `Invalid animation DB`; how the animations play still needs a character in a level. 2294 variant to be chosen (`modules/krs_exploration/src/merge_tests/README.md`).
- **krs_exploration v1.0.0 (8 Oct 2026):** declared v1 by the author; 1563/2045, 2276, 2294 and 2049 are for the next iteration.
- **krs_exploration in game (8 Oct 2026):** the author confirmed the wash animation, the torch return and Reshield (2313) together; the log shows both packages and both XP scripts installed with no KRS error. XP gain itself, an interrupted wash and the unrebased 2049 operations are not verified. `krs-qol` documents Reshield as an optional companion. Details in `../../CHANGELOG.md`.
- **Mod lists:** all lists are merged into `../mods-review/mods_index.csv` (365 mods). The mods in `Mods WIP folder/Installed_to_review` are the author's definitive list (4 Oct 2026): 280 of the 365 are there (279 archives plus 1131 through its replacement 2068), 37 are excluded by the author, 47 low-priority ones were not downloaded, and 17 downloads are outside the index (`../mods-review/list_vs_downloads.csv`, `NOT_DOWNLOADED.md`, `DOWNLOADS_PLAN.md`).
- **Repository:** the remote moved while this work was done (PRs #1 to #3 are merged and `develop` replaced `dev`); these branches still have the old docs layout and are not merged with `origin/develop`. See Branches below.
- **Not verified:** rows of level-only tables (perks, sleeping spots, overrides, `skill2item_category`) and the bow live-read; both need the Continue button in the test game, and on 1.9.8 possibly the new EULA screen.
- **Waiting for the author:** answers in `DECISIONS.md` (open decisions); what to do with the quarantined native mods (`../mods-review/QUARANTINE.md`: scan, restore or drop); whether the unlisted downloads join the index; permission replies (`PERMISSIONS.md`).

## Branches

| Branch | Holds | State |
|---|---|---|
| `claude/review-project-mods-03fe7c` | phases 0-3 modules, docs reorganization, mod lists, triage, downloads inventory | pushed earlier (draft PR); the base of the two below |
| `mods-analysis-p1-p2` | read-only analysis of the downloaded P1/P2 mods, quarantine of 6 archives, docs | marks the P1/P2 state; pushed |
| `mods-analysis-p3-p4` | everything of `mods-analysis-p1-p2` plus P3, P4 and unlisted downloads, the visual/domain grading, 17 more quarantined mods, P1/P2 re-run with the same tool | pushed; the branch to continue from |

Order of merging: `mods-analysis-p1-p2` is contained in `mods-analysis-p3-p4`, so merging the latter brings both. Neither is merged with `origin/develop`.

## Progress of phases 0-3 (2 Oct 2026)

| Phase | State | Evidence |
|---|---|---|
| 0 Packaging | **Done** except 0.5 (branches) | `tools/build_module.py`, `tools/gate.py`, `tools/seed_modules.py`; modules under `modules/`; `docs/tests/logs/gate_*.log` |
| 1 Perks | Built; menu-stage checks pass, perk rows pending a player-stage run | `modules/krs_perks`, `gate_krs_items_krs_perks_krs_qol_tables.log` |
| 2 Items | Built; 66 rows + 5 constants read back in game; sleeping spots pending (level table) | `modules/krs_items`, `gate_krs_items_tables.log` |
| 3 QoL | Built; 3 rpg_param rows read back; override/skill2item rows pending (level tables); repair limits left open | `modules/krs_qol` |

Open because the player stage needs someone to press Continue in the test instance (screen access was not granted
while the author was away): perk rows, `sleeping_spot_type`, `perk_rpg_param_override`, `skill2item_category`, 4.1 bow
live-read. Command for that run: `python tools/gate.py krs_items krs_perks krs_qol --mode full`, then press Continue.
Decisions taken by default (change if wrong): separate mods; Enhanced Eyes left out of the modules; repairs in QoL,
price x2 only; Riposte shipped as `krs_perks` with an "enable only one of them" note.


## Snapshot of the first audit (2 Oct 2026, historical)

Most of these findings were resolved by phases 0-3 (repackaged modules under `modules/`). Kept as written for the record.


| Finding | Detail |
|---|---|
| **None of the suite's table patches is applied by the game as packaged today** | `KRS-Items` has mod id `krs_items` but patch suffix `KRS-items`; `KingdomRefinementSuite` has id `kingdom_refinement_suite` but suffix `KRS`; the draft `Para publicar (TEMP)/Data/KRS-Items.pak` is a 7z file, which the game cannot open. The same `KRS-Items` files with the suffix renamed to the id were applied and read back correctly in game (`docs/engine/ptf-rules.md`). The Nexus release may differ |
| Items is the only module with real files | `KRS-Items/Data`: 56 book rows, 5 `rpg_param` rows, 4 sleeping-spot rows, 1 potion row that differs from vanilla |
| Potion rebalance is mostly placeholders (and its pipeline cannot run) | `food__KRS-items.xml` has 34 rows; 33 equal vanilla. Only Aesop Potion differs (nutrition 10 -> 2.5, ratio 0.1 -> 0.5). Planned values live in `Potions_GPT.md`. The formula script crashes and the formula would overwrite designed potions: see `docs/modules/potions/ANALYSIS.md` |
| Possible clash with installed mods | All 34 food rows overlap *Food Spoil Faster* (`decay_time_hours`), 22 overlap *PotionNoSatietyAndHealEnergy*. Measured in game: the later mod's row replaces the whole row, so the clash is real and load order decides who wins (`docs/engine/ptf-rules.md`, rule 6) |
| Reading is set three times | `ReadingXpPerHour`: vanilla 20, `KRS-Items` 5, `KingdomRefinementSuite` 10 (Skill Books Take Time: 10). The 56 book rows are duplicated in `KingdomRefinementSuite` |
| Repairs: four variants, none consistent | The `perk_rpg_param_override` values (vanilla 0.5 / 0.7 / 0.9) belong to the pseudo-perk **"Hardcore Mode - Constants"**, so they only apply in Hardcore mode; normal mode uses the global `rpg_param` (`RepairPriceModif` 0.65). Realistic Repairs sets 0.1 / 0.6 / 1.2, dev branch 0.2 / 0.7 / 1.3. README says "prices doubled" and level-20 repairs down to 20 % |
| Stray `perk_id` in `rpg_param` | `KingdomRefinementSuite/.../rpg_param__KRS.xml` (also in Realistic Repairs itself) puts perk rows in the wrong table. Effect unverified |
| Riposte differs from upstream and vanilla | Vs vanilla: perk `ec4c5274` level 5 -> 10, visibility 0 -> 2; Master Strike perk `61e98757` restored. Upstream (Restore Riposte) used level 8 |
| Riposte file is in the wrong folder | `Data/perk__riposte.xml`; the game reads `Data/Libs/Tables/rpg/perk__riposte.xml` (as the upstream mod ships it) |
| Dangerous empty files | `KRS-Items/Data/Tables/item/item.xml` is an empty full-replace of `item` (would drop 2214 rows if packed); `WIP Base/.../armor.xml` likewise for `armor` |
| Single-underscore table name | `skill2item_category_krspkg1` (also in Realistic Repairs); PTF names use `__`. Effect unverified |
| 9 no-op rows | "Possible variables for my bow mod" in `rpg_param__KRS.xml` equal vanilla |
| Hidden params | Many keys (`DigestionSpeed`, `StrengthToInventoryCapacity`, ...) are not in the vanilla table; their real default comes from the game binary (`Params Reference.md` describes them, with no values) |

