# How the game applies table patches (measured)

> **Status date:** 2026-10-03 | **Kind:** engine | **Trust:** measured | **Game version:** 1.9.6 (suffix rule re-observed on 1.9.8)

Tested on the replica in `Mods WIP folder/KingdomComeDeliverance`, first on build `1.9.6` (2 Oct 2026) and from 3 Oct on `1.9.8`.
Everything below was read back from the running game (`Database` and `RPG` Lua APIs, or the engine's own "Table ... is patched by" log line), not inferred. Differences between game versions are in `game-versions.md`.

## 1. Rules for table patches (PTF)

| # | Observation | Evidence |
|---|---|---|
| 1 | **The patch file suffix must equal the mod id**, otherwise the engine silently ignores the file. `food__krs_harness.xml` in mod `krs_harness` was applied (`Table 'food' is patched by 'food__krs_harness', lines added: 0, modified: 2`); the same content with other suffixes was never picked up (several variants tried, including a byte-for-byte copy of a working mod's pak and paks with 7-Zip attributes) | `run_ptf_suffix_equals_modid.log` |
| 2 | The mod id is the `<modid>` of `mod.manifest`, or the lower-cased `<name>` with spaces turned into underscores when there is no `<modid>` (log: `Loading lua init script for mod krs_test_harness`) | session logs |
| 3 | A **hyphen in the suffix does not match an underscore in the id**: `potion__krs-harness.xml` for mod `krs_harness` was ignored | `run_ptf_overlap_partial_hyphen.log` |
| 4 | The manifest log warns that a mod id accepts **only lowercase letters and underscore**; a mod called `krs_harness2` was not patched until it was renamed `krs_harness_b` | `run_ptf_suffix_equals_modid.log`, `..._overlap_partial_hyphen.log` |
| 5 | A **row that lists only some columns blanks the others**: Aqua Vitalis patched with `item_id` + `refresh_benefit` became `nutrition 0, ratio 0, alcohol 0, max_status 0, refresh 9` (vanilla 5 / 0.5 / 0 / 100 / 4). Rows must be complete | `run_ptf_overlap_partial_hyphen.log` |
| 6 | **Rows are replaced whole, last mod wins**: mod 1 set Aesop nutrition 2.5 / ratio 0.5, mod 2 (later in `mod_order.txt`) set decay 123 with all other columns vanilla; the result was nutrition **10**, ratio **0.1**, decay 123. The first mod's change was undone | same log |
| 7 | Full rows that equal vanilla are counted as `equal` and do not change anything on their own (KRS-Items food: `modified: 1, equal: 33`) | `run_krs_items_as_is_vs_fixed.log` |
| 8 | Only mods listed in `Mods/mod_order.txt` are loaded (`Loading mods from mods/mod_order.txt`) | session logs |
| 9 | A `.pak` must be a **ZIP**. A 7z archive renamed `.pak` fails with `Failed to open the pak` (seen 9x for `dynamic_bow_stats.pak` and 7x for `MinimalModTools.pak` in the logs; the copies of those two paks on branch `dev` and `KRS-Items/Para publicar (TEMP)/Data/KRS-Items.pak` start with the 7z signature) | `kcd.log`, `logbackups/` |
| 10 | Patches added to a hidden constant work: a new `rpg_param` row `DigestionSpeed` was reported as `added: 1` and the game then returned `RPG.DigestionSpeed = 0.00130208` | `run_krs_items_as_is_vs_fixed.log` |


## 2. The suite's own files today

`tools/check_patch_names.py` applies rules 1, 2, 5 and 9 to the repo (report: `check_patch_names_report.txt`).
Packaged exactly as they are in the repo, `KRS-Items` was **not applied at all** (`modid krs_items` but suffix
`KRS-items`), and `KingdomRefinementSuite` (`kingdom_refinement_suite` vs suffix `KRS`) would not be either. The same
files with the suffix renamed to the mod id **were applied and read back correctly**: `rpg_param` added 1 / modified 4,
`sleeping_spot_type` modified 4, `food` modified 1 (+33 equal), `document` modified 56, and in game
`ReadingXpPerHour = 5`, `StarvationPlayerEffectMinMin = 95`, a book's reading time 15 h (vanilla 6 h).
Update 3 Oct 2026: the two published Nexus releases (KRS-Items 1.0.0 and 1.1.1, read from the Vortex download folder) show the same and more: the `.pak` is a 7z archive renamed `.pak`, the files inside sit under `Tables\...` without the `Libs\` root, the suffix is `KRS-items` against the id `krs_items`, 1.0.0 lists `1.9.x` (rejected by the 1.9.8 engine) and 1.1.1 has no manifest (`../mods-review/MODS_REVIEW.md` section 13.2). Limits of the earlier statement: it was about the files in the repo; the Nexus release could have been packaged differently,
and its `.pak` could not be opened (7z).


## 5. Module gate results (phases 0-3)

Run by `tools/gate.py` (builds the module, installs it with the `krs_gate` test mod, reads every patched row back through
the Lua `Database` API and every `rpg_param` row through `RPG.<key>`). Logs: `gate_*.log` in this folder.

| Observation | Evidence |
|---|---|
| With the suffix equal to the id, all 8 patch files of `krs_items`, `krs_perks`, `krs_qol` were applied (`modified`/`added` counts match the rows) and 73 of 73 reachable checks (65 rows + 8 constants) read back as in the files | `gate_krs_items_krs_perks_krs_qol_tables.log` |
| Same result with the author's current Vortex mod list loaded before them (Riposte, Stay Clean, Early Bird, Drink Sound Effects, ...) | `gate_compat_user_mods_tables.log` |
| `krs_perks` after the upstream Riposte mod: `perk modified: 1, equal: 1` (level changes, Master Strike identical), i.e. the later mod's rows win | same |
| Localization: a `Localization/<Language>_xml.pak` inside the mod with `text__<modid>.xml` is picked up (`[Mod] Loading localization patch 'Localization	ext__krs_perks.xml'`); a mod without it only logs `Can't open file (Localization	ext__<id>.xml)`, which is harmless | gate logs |
| The test instance starts in the main-menu scene (level `rataje`); `mm_main/OnStart` arrives after that scene is loaded. At that point `perk`, `buff` and `sleeping_spot_type` have 0 lines; `food`, `item`, `document`, `rpg_param`, `potion` are loaded. A player needs the Continue button | `gate_krs_items_tables.log`, `gate_krs_items_full.log` (full mode waited 6 min at the menu) |
| The database reports an empty cell as `0`, `-1`, `nil` or an all-zero uuid, depending on the column type | gate log (first run) |
| Manifest `<kcd_version>1.9.6</kcd_version>` gives `supports game version '1.9.6' explicitly, it will be enabled` | gate logs |
| Other mods already in the author's list patch `potion` (Drink Sound Effects, 9 rows added), `item` (9 rows) and `soul` (Early Bird, 2390 rows): relevant for the potion module | compat log |

How to repeat: `python tools/gate.py krs_items krs_perks krs_qol` (menu stage, about 3 minutes, no input needed) or `--mode full` and press Continue
when the main menu appears.

