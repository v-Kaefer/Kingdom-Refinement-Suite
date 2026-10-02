# What the game was observed to do (in-game test results)

Tested on the replica in `Mods WIP folder/KingdomComeDeliverance` (build `1.9.6-404-504czj3`, launched through
`Bin\win64releasedll\kingdomcome.exe` with only the test mods enabled, no Cheat mod). The harness mods are built by
`tools/harness/build_harness.py` and `tools/harness/build_krs_conformance.py` and run by
`tools/harness/run_game_test.ps1`; the extracted game logs are the `run_*.log` files in this folder. Everything below was
read back from the running game (`Database` and `RPG` Lua APIs, or the engine's own "Table ... is patched by" log line),
not inferred.

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
Limits of this statement: it is about the files in the repo; the Nexus release could have been packaged differently,
and its `.pak` could not be opened (7z).

## 3. Lua and parameters (`run_full_api_stats_constants.log`)

| Observation | Result |
|---|---|
| The harness mod's `Scripts/Startup/*.lua`, a spawned entity and a UIAction listener run **without the Cheat mod** | works; `cheat` is `nil` |
| `Script.SetTimer` called from a startup script | **never fired** (use the listener / entity pattern) |
| `System.GetEntityByClass`, `System.IsDevMode`, `Script.SetUpdateFunction`, `Game.SetRPGParam`, `Game.GetPlayer` | `nil` (matches `docs/bow/API_CHECK.md`) |
| Global `player` (table with `soul`, `human`) and `g_localActor` | present once a save is loaded |
| `player.soul:GetStatLevel('agi'/'str'/'vit'/'spc'/'cou')`, `GetDerivedStat('cha'/'bad'/'mor'/'cap'/'ble')`, `GetState('health')` | work (test save: 15 / 13 / 9 / 14 / 16; capacity 153) |
| `player.human:GetItemInHand(0)` | callable; returns an empty handle when nothing is held |
| `RPG.AimSpreadMax = 40` and `RPG.BowChargeDurationMax = 40` | read back 40, restore worked |
| `RPG.ThisKeyDoesNotExist = 1` | no Lua error, but the engine logs `no such rpg constant` |
| 597 keys read from `Params Reference.md` + the vanilla table | **588 exist, 9 do not**: `AlcoholPerkLooseTongueSpcChaModif`, `AlcoholismTickInterval`, `DistanceCheckInterval`, `FoodTickInterval`, `ReadingRestEffectiveness`, `ReadingRestUpperLimit`, `TreasureItemPricee`, `UnarmedAttackBase`, `VigourTickInterval`. 406 of the 588 are hidden (not in the vanilla `rpg_param` table). Full list with real values: `docs/params/rpg_constants_runtime.csv` |

## 3b. Not tested yet

- Whether the bow reads `AimSpreadMax`, `AimStamCost` and the `BowCharge*` constants **live** when aiming (needs a person
  or an automated input to load a save, equip a bow and draw). A first test of this kind (capacity changes when
  `StrengthToInventoryCapacity` is written) is in the harness but the instance stopped at the main menu in the last runs.
- Effects on NPC archers.
- Perk and buff tables (they are only loaded together with a level).

## 4. How to repeat it

```bash
python tools/harness/build_harness.py --game "<KCD folder>" --params-ref "Params Reference.md" --mode tables
```
```powershell
tools\harness\run_game_test.ps1 -GameDir "<KCD folder>" -OutFile result.log -Mods 'krs_harness','krs_harness_b'
```
The runner backs up `Mods\mod_order.txt`, loads only the listed mods, starts the game, waits for the harness line
`KRS_HARNESS end`, stops the game if needed and restores `mod_order.txt`. Remove the test mods from `Mods` afterwards.
Side effects: each run creates a new `kcd.log` and moves the previous one into `logbackups/`; the game does not save.

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

