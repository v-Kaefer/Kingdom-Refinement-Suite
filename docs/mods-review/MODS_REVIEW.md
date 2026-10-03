# Mod lists review - consolidated

> **Status date:** 2026-10-03 | **Kind:** review | **Trust:** reported and inferred (no mod page or archive was opened) | **Game version:** 1.9.6 and 1.9.8

Status date: 3 Oct 2026. This merges the author's two Nexus lists with the review notes that arrived in
`Mods WIP folder/new_mods_review/` into one place, and ties them to the three KRS modules. Machine-readable version:
[`mods_index.csv`](mods_index.csv) (one row per mod id), rebuilt by `python tools/build_mods_index.py`.

## 1. What was available and what was not

| Item | State |
|---|---|
| `mods_to_verify.txt` (author's long list) | Present, copied to `sources/`. 176 links, 170 unique ids |
| `Kingdom Come Mods.txt` ("Working 1.9.6", 33 entries with the author's own labels) | Present, copied to `sources/tested_1.9.6_list.txt` |
| Review notes `README.md`, `comparison.md`, `fixed.md` | Present, copied unchanged to `source_review/`. **Incomplete**: the README starts mid-table (its summary counts are missing) and `comparison.md` starts at "Author series" (its sections 1-2, the slop-vs-substance verdicts and the overlap clusters, are missing) |
| `catalog.md` (130 identified mods, 15 categories), `unverified.md` (71 ids), `mods.csv` | **Not found** anywhere on the machine, although the README links them. The per-mod descriptions, verdicts and "files touched" columns therefore could not be consolidated |

Counts (computed from the lists, they agree with the review README):

- 209 links in the two files -> **201 unique ids**.
- Repeated inside `mods_to_verify.txt`: 2021, 2174, 2175, 2191, 2206, 2348. In both files: 1330, 1337.
- Of the 201 ids, **91 have some review text** (name, series, version, fix status or observation) and **110 have none** in the files that exist.
  The review itself says 71 ids could not be identified and 7 were never looked up (2366, 2367, 2369, 2371, 2372, 2381, 2384).
- 11 more ids are named by the review or by the project README but are outside the lists (adjacent mods, Restore Riposte 1765, Immersive Archery 1419).

## 2. How far to trust the review

- Nexus and Steam were blocked for its author; **everything is from web-search summaries**, no mod page, file list or patch note was opened.
  I tried a Nexus page from this session too and got HTTP 403, so the gap cannot be closed from here either.
- "Files touched" is stated only where a page named a path; otherwise inferred. Verdicts ("slop-risk", "mixed") are opinions on thin evidence.
- It caught one search error (1131 is the author's "silver armor", not "Playable Daggers", which is 1689). Other ids could carry similar errors.
- Nothing in the review was measured in game. What this project measured is in `docs/engine/ptf-rules.md`; where the two meet it is flagged below.

## 3. Install methods seen (from page text)

| Code | Meaning | Ids named |
|---|---|---|
| PTF | Table patch with only the changed rows | 1009, 1423, 1870, 1873, 2022, 2045, 2046, 2158, 2171, 2174, 2179, 2188, 2208, 2209, 2210, 2340, 1416, 1236 |
| LEG | Legacy: `.pak` copied into `Data` and `Data\_fastload` | 754 |
| LUA | Replaces a vanilla Lua file loose | 1332 |
| CFG | Console variables in `user.cfg`/`system.cfg` | 1972, 2180, 2153, 2243 |
| KCSE / native | Needs the script extender (1.9.8.0 only) or native code | 2244, 2255, 2348 |
| DEV | Needs the game in dev mode | 958 |

A correction to the legend based on measurements: "PTF carries only the changed rows" is true, but **each row has to be complete**. A row that
lists only some columns blanks the others (measured), and a patch is ignored unless its file suffix equals the mod id. Any PTF mod on these lists
that does not follow both rules is silently doing nothing or damaging rows; checking the archives with `tools/check_patch_names.py` would show it.

## 4. Clusters

| Cluster | Ids | Note |
|---|---|---|
| Author series | DreamMora 2190, 2191, 2192, 2194, 2196, 2199, 2206 (KCD2 ports); Nfrog2swamp1 2179, 2188, 2209, 2210, 2208 (True Hardcore PTF series); MayDayU1A 2103, 2108, 2147 (UI); Diaz Dizazter 2040, 2046, 2049; TyburnKetch 1736, 1780; JerryYOJ 2244, 2255 | Series are meant to be used together, so their rows overlap on purpose |
| Whole-file replacements (conflict-prone) | 1309, 1327, 2333, 1723, 2317 | `random_event.xml`, a mission file, `Inventory.gfx`, `HUD.gfx`. UI files cannot use PTF, so conflicts persist |
| Large bundles | 651, 1260, 2124, 2299, 2340 | 2340 already ships modular files |
| Merchant gold multipliers | 1460, 1873 | Flat multipliers |
| Per-language text renames | 797, 2203, 2204, 808 | Same upkeep problem as the KRS localization paks |
| Hardware-specific cfg | 1972, 2180, 2243, 2153 | Published as general values |

## 5. Game version watchlist

The project's manifests (`modules/*/mod.manifest`) say `1.9.6` and all tests ran on a 1.9.6 build (`1.9.6-404`). The review's pages mention newer builds:

| Id | Statement |
|---|---|
| 2244 KCSE | 1.9.8.0 only |
| 2040 Polymorphic Projectiles | 1.9.7 or higher |
| 2331 Bushes Redux | designed for 1.9.7 |
| 2208, 2210 | made and tested on 1.9.8 |
| 2124 Half-looted | made for 1.9.6, compatible with 1.9.7 |
| 1009 Perkaholic PTF | 1.9.4 to 1.9.8 |
| 1873 | comments report problems on the latest version |

Consequence for KRS: if your Steam install is 1.9.7 or 1.9.8, re-run `python tools/gate.py ...` there before publishing and add the version to `<supports>`.
The harness prints the engine's own line (`supports game version '1.9.6' explicitly, it will be enabled`), so a mismatch would show.

## 6. Fixes that might be obsolete

None is confirmed fixed by an official patch (patch notes unreadable). Candidates to check on a clean install of the current version:

| Id | Mod | Defect | Last update | Status |
|---|---|---|---|---|
| 591 | Bushes - Collision Remover | Invisible collision on bushes | 2018-08 | Likely still needed (2331 was rebuilt for 1.9.7) |
| 2331 | Bushes Collision Remover Redux | Same, 26 models | 2026-08 | Current |
| 1323 | Skalitz Shield Fix AWL | Blurry shield | 2022-01 | Check patch notes |
| 1577 | Invisible hands FIX | Forearms invisible with sleeveless clothes | 2023-12 | Check patch notes |
| 1693 | Ravens beak / Spiked warhammer icon swap | Two icons mismatched | 2024-12 | Check patch notes |
| 2066 | Distant Smoke and Fire | Smoke/flame pop-in | 2025-08 | Check patch notes |
| 1380 | Black Items Fix | Unknown (page not resolved) | n/a | Resolve first |

Not candidates: 1883 (fixes another mod), 1259 and 1327 (fix their own bugs), 1671, 1951, 1647, 284, 2158, 2171 (behaviour preferences). Bundled fixes not worth separate checks: 1566, 796, 2243.
To move one to "fixed": read the 1.9.7/1.9.8 notes, reproduce the symptom on an unmodded current install, then record the patch note line.

## 7. How the lists relate to the KRS modules

What the review says lines up with the project's `Requirements.md`: Riposte (1629, 2294, 2179), archery (1678, 2040), persistent arrows (1743 is the required mod, 2206 overlaps),
stay clean (2218, 1260, 651), perk table (1009, 1736, 1990, 765, 2210), localization (797, 2203, 2204, 808). The "30 FPS cutscene fix" and "Early bird NPC" requirements are not
in the identified part of the lists (1227 "30 FPS Cutscene Fix V3" turned up as an adjacent mod).

Overlap risk with the three modules, **inferred from names and the review's table list, not measured** (no archive was opened):

| KRS module / rows | Mods on the lists that probably patch the same table | What it means in game (measured rule: later mod in `mod_order.txt` wins the whole row) |
|---|---|---|
| `krs_perks`: `perk` rows `ec4c5274` (Riposte), `61e98757` (Master Strike) | 1009 and 770 (Perkaholic), 1736, 1990, 765, 2210, 2179, 2294, 1236 (Easy Combat PTF) | Whoever loads last decides level and visibility. Measured only against the upstream Restore Riposte (1765): `krs_perks` after it gives `modified 1, equal 1` |
| `krs_items`: `food` row Aesop, `document` (56 books), `rpg_param` (reading XP, digestion, starvation), `sleeping_spot_type` | 1483 (slower food spoil), 765 (poison overhaul), 1260 (rpg tweaks), 1460, 1873 (merchants), 1334 (fast learning, adjacent) | `rpg_param` rows are per key, so only a shared key collides; the 34 food rows collide with any potion/food mod, as the earlier audit found for Food Spoil Faster |
| `krs_qol`: `rpg_param` (herb radius, carry capacity, repair price), `skill2item_category`, quest text | 1260, 651 (bundles), 797, 2203, 2204, 808 (text renames) | Text patches are per key; a renaming mod that also edits the 22 timed-quest keys would win or lose by load order |

How to turn this from inference into fact once the archives are downloaded (all existing tools):

1. Put the archives (or their extracted folders) into a folder and run `python tools/audit_tables.py --root <folder> --out docs/data/table-audit` to list the tables and rows each mod really changes; `python tools/check_patch_names.py <folder>` flags patches the engine would ignore.
2. Add the ids to a `--with` run of `python tools/gate.py krs_items krs_perks krs_qol --with <mod folders>`: the log shows `Table 'X' is patched by ...` in load order and whether the KRS rows still read back.
3. Fill the `krs_area` and `observation` columns in `annotations.csv` from the result and rebuild the index.

## 8. Improvement observations from the review (descriptions only, none from source)

| Ids | Observation | Possible improvement |
|---|---|---|
| 1332 | Whole Lua script replaced loose; may take minutes to apply | Mods-folder override or edit the shake values only |
| 754 | Legacy dual-copy install | Mods-folder package with a manifest |
| 1309, 1327, 2333, 1723, 2317 | Whole shared file replaced | Row patch where the format allows; UI files cannot |
| 1873, 1460 | Large flat merchant gold multipliers | Per-merchant scaling |
| 2171 | Misses pickpocketed items | Combine with the 2158 parameter approach |
| 2323 | Moves items between stashes, horse and pockets | Transactional move with rollback; test save safety |
| 2276 | Speed constant edited by hand | Config file |
| 2040 | Arrow balance mixed with novelty arrows | Split into optional packages |
| 797, 2203, 2204, 808 | Per-language renames | Generate text from one source (relevant to KRS: `modules/*/Localization/<Language>/`) |
| 651, 1260, 2124, 2299, 2340 | Large bundles | Optional modules |
| 2216 | Repairs other mods' manifests on the fly | Back up first; test |
| 2244, 2255, 2348 | Native or version-locked code | Version checks that fail loudly |
| 1972, 2180, 2243, 2153 | Hardware-specific cfg published as general | Tiered presets with measured results |

## 9. Adjacent mods (outside the lists, not reviewed)

1040 Disable Combat Slowmotion; 1227 30 FPS Cutscene Fix V3; 1236 Easy Combat PTF; 1296 Kingdom Come Enhanced Edition 2.0; 1334 Fast Learning Henry;
1416 Toxic Green Armor PTF Standalone; 1689 Playable Daggers; 1797 Nighttime Nighthawk; 2119 KCD Mod Manager. Also named by the project README: 1765 Restore Riposte, 1419 Immersive Archery.

## 10. Open items

1. Re-send or regenerate `catalog.md`, `unverified.md` and `mods.csv` (and the missing top of the README and comparison); they hold the per-mod verdicts. Once they are in `source_review/`, the annotations can be filled from them.
2. Download the archives of the mods that overlap the KRS tables (section 7) so the audit can replace the inferences.
3. Decide the target game version (1.9.6 vs 1.9.7/1.9.8) before the review's version watchlist is acted on.
4. The seven ids never looked up, and the 71 unidentified ones, need a manual pass or an allowed Nexus fetch.

## 11. Re-check against game version 1.9.8 (3 Oct 2026)

Nothing above was removed; this section adds what the 1.9.8 install and the official patch notes show. Per-mod detail is in
`mods_index.csv` (columns `check_1.9.8`, `check_source`). Evidence labels: **measured** = read from the 1.9.8 install or its log,
**official** = patch notes (summaries; the full texts could not be fetched, `../engine/game-versions.md` section 4),
**page** = Nexus page summary from a web search (pages themselves are blocked, HTTP 403).

### 11.1 Section 6 (fixes that might be obsolete)

The official 1.9.7 and 1.9.8 notes mention none of: bush collision, the Skalitz shield, weapon icons, smoke and fire. They do list one fix in this area: **Quilted Vest transparent arms** (1.9.7).

| Id | Verdict on 1.9.8 | Basis |
|---|---|---|
| 591 Bushes - Collision Remover | **Still applicable, not obsolete.** All 26 models it replaces are byte-identical in every game pak up to 1.9.8, so no patch touched them. 2331 is the rebuilt version (1.9.7 assets); prefer 2331. Collision itself was not inspected | measured + official |
| 2331 Bushes Collision Remover Redux | Current; no 1.9.8 statement on the page | page |
| 1323 Skalitz Shield Fix AWL | **Unconfirmed.** No evidence of an official fix; last update 2022-01-19; needs A Woman's Lot. Check the shield in game | page + official |
| 1577 Invisible hands FIX | **Partly overlapped.** The 1.9.7 note fixes one item (Quilted Vest); the mod fixes the body material's `alphaTest` for all sleeveless clothes (last update 2023-12-13). Keep until tested with another sleeveless item | page + official |
| 1693 Ravens beak / Spiked warhammer icons | **Still needed.** Current `Tables.pak` still has icon 152 on the Raven's beak and 150 on the spiked warhammer; the mod sets them the other way round. Its manifest lists only 1.9.6, so the 1.9.8 engine disables it until the line is edited | measured |
| 2066 Distant Smoke and Fire | **Not verifiable here.** Replaces `libs\particles\wh_particels.xml` as a whole file (conflicts with other mods editing it); notes silent on particles; v0.2, 2025-08-22 | page + official |
| 1380 Black Items Fix | Unresolved (page not identified) | - |

### 11.2 Section 5 (version watchlist) against 1.9.8

| Id | Finding | Worth updating? |
|---|---|---|
| 2244 KCSE | v3 matches 1.9.8.0 only; a companion Address Library (2273) is also 1.9.8 only | Yes if the install stays on 1.9.8; useless on older builds |
| 2040 Polymorphic Projectiles | States 1.9.7+, updated 2026-03-24; needs the "Loot Info" mod for multi-damage arrows | Compatible by its statement |
| 2331 Bushes Redux | Built on 1.9.7 assets; no 1.9.8 statement | Likely fine (assets unchanged in 1.9.8 data) |
| 2208, 2210 (True Hardcore series) | Made and tested on 1.9.8; the series also has 2179 Combat, 2188 Economy, 2219 Crime, 2173 Maintenance, 2209 Poisonous Enemies | Current; 2173 touches repairs, compare with `krs_qol` |
| 2124 Half-looted Rebalance | Made for 1.9.6, "compatible with 1.9.7"; no 1.9.8 statement found | Check before use; it is a large bundle |
| 1009 Perkaholic PTF | v1.2.3 lists 1.9.4 to 1.9.8 | Already current (older ids 85 and 770 are previous versions) |
| 1873 Daily Restock And Rich Merchants - PTF | v1.0 by tempbito, no version statement found; the review's "problems on the latest version" is unconfirmed | Unknown; alternatives 1853, 2165, 1460 |
| 2255, 2348 | Nothing found | - |

### 11.3 The author's own installed mods on 1.9.8 (measured, `../tests/logs/gate_compat_user_mods_1.9.8_tables.log`)

- **Disabled by the engine because their manifest lists only an older version:** Restore Riposte (1765), Drink Sound Effects (1730). Editing that one line loads them (measured with a copy of Riposte and with synthetic mods; `../engine/game-versions.md` section 2). Whether they then behave correctly in a level was not tested.
- Enabled: Persistent Arrows (1743) and Volumetric Fog Shadows (800) through `1.9.*`; Cheat, Solid Helmet Visors, Time HD, MGs Stay Clean, 30 FPS Cutscene Fix, More Responsive Targeting and Early Bird NPC have no version restriction.
- The same disabling would hit any mod from the lists whose manifest says `1.9.6` or `1.9.x` (the only working wildcard is `1.9.*`).

### 11.4 Mods added to the index

`mods_index.csv` now has 248 rows: the 201 ids of the two lists plus
- **32 mods that exist in the workspace or in the Vortex deployment but were not in either list** (for example 1227 30 FPS Cutscene Fix, 1419 Immersive Archery, 1765 Restore Riposte, 1950 Skill Books Take Time 2x, 1938 Herb Picking Radius 2x, 1839 Realistic Horses; the CSV column `scope` marks each row); found by `tools/scan_workspace_mods.py` from the folder names under `Mods WIP folder` and `vortex.deployment.json`. About 30 further entries (loose `.pak` files such as `Dice.pak` and `earlybird.pak`, and folders such as `Food Spoil faster` or `trainmorecarrymore`) have no id in their name and need to be identified by hand (the scanner prints them),
- **15 mods outside the lists and the workspace**: the 8 adjacent mods of section 9 (1040, 1236, 1296, 1334, 1416, 1689, 1797, 2119) and 7 found while checking (667, 1853, 1882, 2165, 2173, 2219, 2273: series members and alternatives).

The author said more links were brought than the lists in the repository contain; if some are still missing, send them and they go into `mods-review/sources/` and the index.
