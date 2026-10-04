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

## 12. Consolidation of the Vivaldi tabs and the history list (3 Oct 2026)

The author's browser held 180 Nexus tabs (`sources/nexusmods_abas_vivaldi.csv`, names included) and a second session, "New mods lists review",
merged them with the titles of the history screenshots into a 290-mod title list, an analysis and a verification of the earlier review
(`raw/new-mods-lists-review/`: `id_titles.csv`, `analysis.md`, `verification.md`, kept exactly as written). This section folds that work into the project.
Nexus pages were not opened (HTTP 403), so everything about these mods is **title-based**: names are reliable, categories are keyword-based
with manual fixes, verdicts do not exist yet.

### 12.1 What the index now holds (`mods_index.csv`, 365 rows)

| Group | Ids | Note |
|---|---|---|
| In the author's two text lists | 201 | 161 have a title (130 from the history screenshots, the rest from Vivaldi tabs), 40 have none (see 12.7) |
| Vivaldi tabs | 180 | **56 are in the text lists, 124 are not** |
| New: in the Vivaldi tabs or screenshots but in neither text list | 129 | 124 from Vivaldi plus 5 only in the screenshots |
| Workspace or Vortex only | 24 | section 11.4 |
| Found while checking | 11 | outside every list |

Columns added: `name` (exact tab title where one exists), `category`, `ptf`, `triage`, `in_vivaldi_tabs`, `in_history_screenshots`, `fix_type`, `list_review_note`.
`triage` is a mechanical sort from the category and the KRS area (rules in `tools/build_mods_index.py`), **not a verdict**:
"overlap check needed" means the mod edits something KRS also edits and must be compared at table level; "visual only", "UI or maps", "tool", "outside the PTF scope" mean the opposite.

| Triage (all 365 rows) | Rows |
|---|---|
| gameplay, no KRS area flagged, still check tables | 85, plus 18 PTF-titled |
| gameplay, overlap check needed (Archery 14, Combat/riposte 14, Perk/RPG tables 10, Localization 2, Stay-clean 1) | 41, plus 9 PTF-titled |
| visual only (26 Reshade/ENB presets, 19 `user.cfg` mods) | 45 |
| UI or maps (replace `.gfx` and map files) | 34 |
| world or weather 25, content 14, animations/audio 3 | 42 |
| tool or reference | 12 |
| out of scope (adult content: 1818, 1900, 2196, 2304) | 4 |
| unsorted (in the text lists but without a title yet) | 75 |

### 12.2 Categories of the 290 titled mods (from `analysis.md`)

Weapons, armor, items 36 | Maps, UI, HUD 34 | Reshade, ENB, visual presets 26 | World, weather, visuals 25 | Alchemy, food, survival 24 | Combat, AI 23 | Graphics config 19 | Progression, XP, perks 17 | Archery, arrows 15 | Quests, lore, content 14 | Economy, merchants 14 | Crime, stealth, loot 13 | Tools, reference 12 | Horses 8 | Adult 4 | Animations, audio 3 | Other 2 | Fix bundle 1. Of the 290, 28 carry "PTF" in the title (20 from Vivaldi). 26 ids are below 1000 (old uploads): the likeliest to predate the Mods-folder format, so also the likeliest to be disabled on 1.9.8 if their manifest lists only old versions (section 11.3).

### 12.3 Overlap clusters (title-evident, not measured)

| Cluster | Ids | Concern |
|---|---|---|
| Archery and arrows | 802, 804, 1084, 1100, 1205, 1090, 1375, 1376, 1419, 1564, 1565, 1678, 1743, 2035, 2040 | All edit bow or arrow values; the suite alters 1419 and requires 1743 |
| Karnages series (12) | 1558-1563, 1564, 1565, 1566, 1568, 1569, 1570 | One author, many tables: weapons, polearms, arrows, shop prices, durability, `user.cfg` |
| Combat overhauls | 1070, 1112, 1384, 651, 2256, 2179, 2294, 1629, 1148, 2359, 2192, 2194, 1243, 1612, 1647, 883 | Combat, master-strike and AI tables; **highest conflict risk for `krs_perks`** (Riposte rows) |
| Weapon and polearm balance | 1088, 2045, 1562, 1563, 1559, 1148, 2046, 1636, 1153, 883 | Same weapon stat tables |
| Merchants, prices, money | 829, 1105, 1308, 1460, 1548, 2279, 1568, 1578, 1861, 1870, 1873, 1981, 2188 | 1460 (x3 money) and 1873 push the same way and stack |
| XP and progression | 1518, 1519, 1520, 1572, 1860, 1334, 2340, 1668, 2246, 883, 1009, 2299 | XP, perks and `rpg_param`: the same table as `krs_items` (`ReadingXpPerHour`) and `krs_qol` |
| Repair and durability | 1292, 1842, 2021, 2348, 1560, 1545, 2173 | The same area as `krs_qol` (`RepairPriceModif`, bridles and saddles) |
| Helmets | 1337, 1907, 1909, 2081 | Helmet and vision rows |
| Horses | 129, 1510, 2174, 2223, 2224, 2270, 2271, 2343 | Horse behaviour and caparisons |
| Weather and sky | 879, 1114, 1193, 1327, 1410, 1982 | Several weather systems |
| Graphics cfg | 800, 1342, 1367, 1526, 1527, 1528, 1538, 1552, 1561, 1646, 1720, 1972, 2106, 2153, 2180, 2243, 2353 | Same `user.cfg` variables, the last one wins, hardware-specific |
| Reshade and ENB presets | 26 mods | One at a time; they replace each other rather than conflict with data |
| Maps | 827, 1182, 1281, 2384, 2156, 955 | Map replacers and overlays |
| HUD and UI | 978, 1063, 1218, 1956, 2030, 2108, 2147, 2293, 2103, 1723, 2317, 1719, 1780 | `.gfx` files cannot be PTF: conflicts persist |
| KCD1 Reborn series | 1918, 1927, 1964 | Terrain, vegetation, faces |
| Sorting and language | 2203, 2204, 2374, 1779, 1479, 797 | Per-language item names; 2374 is the Ukrainian version of 2204 |
| Translation families | 491 / 2316 (Japanese), 651 / 2256 (Chinese), 2204 / 2374 (Ukrainian) | Count each family as one mod |

### 12.4 Where the new mods meet the KRS modules

| KRS area | Module | Mods on the lists | What to check |
|---|---|---|---|
| Perk rows `ec4c5274`, `61e98757` (Riposte, Master Strike) | `krs_perks` | combat overhauls 1070, 1112, 1384, 1148, 2359, 1243, 1612; perk mods 1009, 1736, 1860, 1334, 1572 | Whether they patch the `perk` rows above; the later mod in `mod_order.txt` wins the whole row (measured). Restore Riposte (1765) itself is disabled on 1.9.8 as shipped (`../engine/game-versions.md`) |
| `ReadingXpPerHour`, books, digestion, starvation, sleeping spots, Aesop potion | `krs_items` | XP mods 1518, 1519, 1520, 2340, 1668, 2246, 883; 1424 sleep, 1426 energy/hunger patch; the potion mods of the Alchemy cluster (8 new) | `rpg_param` key by key (only a shared key collides); `food` rows as whole rows |
| Herb radius, carry capacity, repair price, bridles, timed-quest text | `krs_qol` | repair cluster (1292, 1842, 2021, 2348, 1560, 1545, 2173); 1938 (herb radius, in the workspace); text renamers 2203, 2204, 2374, 797 | `RepairPriceModif`, `StrengthToInventoryCapacity`, the 22 quest text keys |
| Archery | future `krs_bow` | the 15 archery mods; the suite alters 1419 and requires 1743 | `AimSpreadMax`, `Bow*` constants, arrow rows |
| Required mods | none | 2218 Clean Gear, 1863 Dirty And Charismatic (PTF), 1062 camping next to the MGs Stay Clean requirement; 1227 for the 30 FPS fix | the 1227 page title now says "V3"; the installed file and `Requirements.md` say V2 (note in `annotations.csv`) |

All of this is inference from titles. The way to turn it into fact is unchanged (section 7): download the archives, run `tools/audit_tables.py` and `tools/check_patch_names.py` on them, then `tools/gate.py ... --with <mod folders>`.

### 12.5 Fix-type mods added (candidates for the "fixed" check, sections 6 and 11.1)

| Id | Mod (title) | Note |
|---|---|---|
| 2332 | Baptism of Fire Fix Redux | The 1.9.7 notes list a Baptism of Fire crash fix: check whether it is now obsolete |
| 1558 | Karnages_KCD_Essential_Fixes 2.0 | A bundle; each fix needs its own check |
| 1782, 2343 | elbow clipping; horse caparison fix | Look like vanilla defects: candidates for 1.9.8 |
| 1227 | 30 FPS Cutscene Fix (page title "V3") | Game-side defect; installed file and `Requirements.md`: V2 |
| 1424, 1426, 2279, 1991 | Better Sleep Fixed; Energy and Hunger Patch (PTF); Immersive Economy FIXED; a patch for another mod | Not game fixes (they fix other mods) |
| 1380 | Black Items Fix | Title now known; still not checked |

### 12.6 Outside the suite's scope, and tools

- **Not aligned with "non-intrusive PTF tweaks":** adult content (1818, 1900, 2196, 2304); large content or world replacements (1918, 1927, 1964, 1327, 1356 fan side quest, 1535, 1683).
- **Tools and reference (12):** 864 Official Modding Tools, 867 APEX Realistic Modding Guide, 1059 Icon ID Resource, 1110 AI Standalone Library, 1479, 1594, 1779, 1829 Mod Order Tool, 2119 KCD Mod Manager, 2216 Mod Organizer Plugin, 2244 KCSE (2255 and 2277 need it; 1.9.8.0 only).

### 12.7 Corrections from the verification session, and what is still open

Applied in `annotations.csv` and the index: 2372 and 2381 now have titles (Trough Washing Animation; Nest of Vipers Stealth; 2366, 2367, 2369, 2371, 2384 are still unresolved); the PTF-titled 1860-1864, 1893, 2005, 2021 are added to the PTF examples; 2035 sits next to 1678 and 2040 as a direct comparable for 1419; translation families (2316, 2256, 2374); hardware-specific cfg 1720 and 2353; 2277 needs KCSE; 1327's "mission file" claim is not supported by its title.
Corrections to the text above (not edited in place): the project names Restore Riposte (1765) and Immersive Archery (1419) as altered mods in `Requirements.md`, not in the README (section 9). The first review's catalog (130 mods), `unverified.md` and `mods.csv` are still missing and were not recreated.

Still open: **40 ids of the text lists have no title** (284, 708, 754, 762, 765, 770, 795, 796, 797, 840, 891, 892, 905, 913, 915, 942, 958, 966, 1093, 1131, 1203, 1259, 1260, 1374, 1483, 1577, 1904, 2061, 2079, 2084, 2098, 2100, 2132, 2152, 2297, 2330, 2338, 2345, 2362, 2365). 26 of them have the author's own label in `Kingdom Come Mods.txt`; 14 have no name at all. The "Realism & Immersion 2026" collection that the lists probably came from is a possible cross-check source. Every verdict still needs a mod page or an archive.

## 13. New review and triage of all 365 mods (3 Oct 2026)

Result files: [`TRIAGE.md`](TRIAGE.md) (generated summary), `mods_triage.csv` (one row per mod: category, KRS modules, evidence class, 1.9.8 load status, collision, priority, action, reason),
`archive_analysis.csv` (26 archives read), `search_evidence.csv` (what 42 search results established). Tools: `tools/triage_mods.py`, `tools/analyze_mod_archives.py`, `tools/build_mods_index.py`.
The rules live in `tools/triage_mods.py`, not in this text; change a rule and rerun.

### 13.1 Method and what each evidence class is worth

| Class | Mods | Basis | Trust |
|---|---|---|---|
| A: archive read | 18 ids (26 archives) | Files from the author's own Vortex download folder, extracted to a scratch folder and read; nothing was downloaded from the network | **measured** (manifest, paks, patch rows) |
| B: search result | 41 | A Nexus search result whose URL id matched the title; version, date and a one-line description from its summary | reported; summaries sometimes contradict themselves (see 13.5) |
| C: title only | 299 | Browser tab title or the author's label, keyword rules | weakest; names are reliable, categories are keyword-based |
| D: id only | 7 | 2100, 2132, 2297, 2330, 2345, 2362, 2365: search could not resolve them (2345 returned a KCD2 mod) | none |

Priorities: **P1** 3 (act now), **P2** 113 (compare or check before combining), **P3** 199 (optional or not mapped), **P4** 50 (adult content, visual presets). P2 splits into 15 where the evidence names the same values as a KRS row ("likely"), 2 measured, and the rest title-based ("possible").

### 13.2 What reading the archives showed (measured)

- **The published KRS-Items releases do nothing.** Both Nexus files in the Vortex downloads (1.0.0 and 1.1.1) contain `Data/*.pak` that is a 7z archive renamed `.pak` (not a ZIP: the game cannot open it); inside, the files sit under `Tables\...` without the `Libs\` root; the file suffix is `KRS-items` while the mod id is `krs_items`; 1.0.0 lists `1.9.x`, which the 1.9.8 engine rejects, and 1.1.1 has no `mod.manifest`. Any one of these stops the patch; together they confirm that the published mod never applied. `modules/krs_items` replaces them.
- **Disabled on 1.9.8 as shipped (manifest lists only 1.9.6):** Restore Riposte (1765) and Drink Sound Effects (1730), matching the engine log; the Nexus KRS-Items 1.0.0 (`1.9.x`).
- **Row collisions with the KRS modules (same table and key):** Alternate Food Spoil 2X (1639) patches the Aesop potion row of `krs_items` (a complete row: whichever loads last wins it whole); Restore Riposte (1765) patches both `krs_perks` rows.
- **Whole-table replacement:** Hoods Over Helmets (771, a 2019 mod) ships 15 tables as full files named like the vanilla tables, with no suffix (item tables such as `armor.xml` 494 KB and `item.xml` 256 KB, `shop_type2item.xml`, a 385-byte `rpg_param.xml` and an 8.9 MB `soul.xml`). A full file replaces the table, so mods loaded before it are lost for those tables, and it collides with Early Bird (`soul`) and with every `rpg_param` patch by load order.
- **Malformed manifest:** Clean Items In Trough (1691) has a `mod.manifest` that is not valid XML (mismatched tag); it lists `1.*`, a form that was not tested (only `1.9.*` was).
- **Id characters:** ids with digits or hyphens (`alternatefoodspoil2x`, `time-hd`, `fpsfixv2`) are only a risk for mods that carry table patches; the table mods in the folder (food, perk, soul, item, potion) match their suffix to the id.
- **Large packs not extracted** (only manifests read): Lartigue's Upscale Project (two versions, 851 MB and 312 MB) and Solid Helmet Visors (69 MB).

### 13.3 Findings from search summaries (reported) that touch the KRS modules

| Area | Mods | Why it matters |
|---|---|---|
| Carry capacity (`StrengthToInventoryCapacity`) | 1860 Train More Carry More PTF (tempbito, scales with strength, x1.25/x1.5, leaves the base weight alone), 1668 Relaxed RPG Params (inventory x3, horse x4), 1260 RPG Tweaks (+60 %) | `krs_qol` sets 4 to 5 for the same key; the three set it differently, so only one can win. 1860 is the source the suite credits and still has "permission requested" |
| Repairs | 2021 Repair Kits Balanced and Scaled PTF (kit efficiency), 2173 True Hardcore Maintenance, 1292 Ultimate Repair Kit | `krs_qol` repair price and bridle rows; check which keys each touches |
| Herb picking | 1260 (herb radius), 1572 Increased Experience Gains (optional herb picking), 366 First-person Herb Picking | `HerbGatherSkillToRadius` |
| Food, alcohol, potions | 1266 Stronger drinks PTF (alcohol percentages in the `food` table; incompatible with whole-file `food.xml` mods), 1483 TSM Slower Food Spoil (x2/3/5), 1639, 765 Poison Overhaul (potions and a new perk), 2208-2210 | `krs_items` Aesop row and the future potion module; complete rows, last wins |
| XP and reading | 1572 (rpg_param, 1.5x/2x/5x), 1334 Fast Learning Henry (XP x5; was incompatible with other `RPG_PARAMS` mods), 1518-1520 | `ReadingXpPerHour` in `krs_items` |
| Perk rows | 1009, 1736 Rogue Life (perks in five trees), 1990 Veteran Hunting (adds a perk and a perk buff), 765, 1375 | the two Riposte rows of `krs_perks` only collide if one of them patches the same `perk_id`; unknown until the files are read |
| Combat | 1629 Exclusive Master Strikes (same author as Restore Riposte, 2025-01-28), 2294 Faster Combat, 1384, 1112, 1070, 651, 2359 | Master-strike rules; 2359 needs an ASI loader and states "Steam 1.9.7-404-504czj4 only" |
| Shops and soul table | 2061 Meticulously Edited Shops and Services (edits `shop_type2item.xml` and `soul.xml`; "conflicts with mods that change soul.xml": Early Bird patches `soul`) | A conflict inside the author's current setup (726) |

### 13.4 Bow findings that change the plan (reported, untested in game)

- **1100 Faster archery PTF** (DanishPagan, tested on 1.9.6-404-504) sets the hidden constant `BowChargeDurationMax` (1.00, 1.25, 1.50) with a plain `rpg_param` patch and says aim spread is unchanged. A published, widely used mod therefore already does what `docs/engine/ptf-rules.md` measured (hidden constants can be set by a patch row): the static route of the draw-speed idea is established. 1668 and 1260 set the aim spread the same way.
- **1375 No Aim Spread v2.1** removes bow sway for the **player only** by adding a **perk**, and its variant 2.1b uses two **stat-gated perks** (Strength 10, Agility 8). That points to a route with no script: a perk whose `perk_rpg_param_override` rows carry the constants, unlocked by a stat threshold (vanilla uses `perk_rpg_param_override` for the "Hardcore Mode - Constants" pseudo-perk). It would give stat-dependent steps for the player only, not a smooth formula. **Hypothesis, not tested**: added to the roadmap (`../project/ROADMAP.md`, 4.7).
- 1419 Immersive Archery (draw to about 16 arrows a minute, arrow speed x1.7, stamina drain lower, damage x1.2) and 1678 Better Archery change draw, speed and stamina together; they are the comparison points for any `krs_bow` values.

### 13.5 Limits and cautions

- Search summaries are model-written. Examples of unreliable ones: for 1483 the summary also named an unrelated title; for 1131 it said the page was removed and named another mod; for 2345 the search returned a KCD2 mod; 2246 returned the KCD2 page. Only the title in the result list (its URL id matched) was accepted as a name; descriptions are "reported".
- "Overlap" in the triage means topic or named values, not a read table row, except where evidence class A says so.
- Mod 2359's page calls build `404-504czj4` "1.9.7" while the engine reports 1.9.8 for the same build: version labels differ between authors and the engine.

### 13.6 Can the mods be downloaded for the author?

Not from this environment, and not by working around it:
- `www.nexusmods.com` and its CDN return HTTP 403 to this machine's requests; `api.nexusmods.com` returns 401 (it needs the author's personal API key, and direct links need a Premium account or a click on the site). Signing in, entering a key or accepting the site's terms on the author's behalf is not something the session may do, and a download needs the author's explicit yes per file.
- What works: (1) the author downloads through Vortex or the browser as usual; (2) the archives already in the Vortex download folder (26 for KCD) are read in place by `tools/analyze_mod_archives.py` without any download; (3) any further archives dropped into one folder are analysed with the same command, which writes `archive_analysis.csv` and feeds the triage (class A).
- Suggested order for class A: the P2 mods with "likely" collision (1860, 2021, 1266, 1668, 1260, 1572, 1334, 765, 1990, 1736, 1375, 1100, 1419, 1678, 2246), then the combat group (1629, 2294, 1384, 1112, 1070, 651), then 2061 and 2173.

### 13.7 Update after the author supplied the Nexus API spec (3 Oct 2026)

`openapi.yaml` (Nexus API 3.0.0) shows what an authorised client can read: a mod's name, summary and **status** (`published`, `not_published`, `hidden`, `under_moderation`, `removed`, `removed_by_staff`), its mod files with last upload dates, and every file version with its version string, category (`main`, `update`, `optional`, `old_version`, `archived`, `removed`) and upload date. That answers exactly the open questions of this review (removed pages such as 1131, which mods were updated after the 13 Feb 2026 patch, whether a 1.9.8-ready file exists) without any download. `tools/nexus_metadata.py` implements those read-only calls (it has a `--selftest` that runs against a fake server and checks that no download endpoint is touched); the author runs it with a personal key in an environment variable and `tools/triage_mods.py` adds `nexus_status`, `nexus_latest_version` and `updated_since_1.9.7`. A key that was pasted into the chat was **not** used by the session (credentials are not handled by it); it should be revoked at the Nexus API-keys page and replaced. The spec also lists a `download-repacked` endpoint; nothing in this repository calls it.

## 14. Nexus API results (author's run of `tools/nexus_metadata.py`, 3 Oct 2026)

The author ran the read-only metadata tool with a personal key (the session never handled it). `nexus_metadata.csv` holds name, summary, status and adult flag of all 365 ids; this replaces the search summaries as the source of names and descriptions (evidence class **N**, see below). It supersedes the cautions of 13.5 for the fields it covers.

| Result | Detail |
|---|---|
| Status | 363 published; **1296** Kingdom Come Enhanced Edition 2.0 removed ("DELETED"); **1131** removed by staff ("SPOA SILVER KNIGHT ARMOR for KCD - DELETED", the author's "silver armor") |
| Adult flag | 1045 More Blood, 1900 Jiggle Physics, 2304 Female Nudity (the triage already put the adult-content titles out of scope) |
| The 7 ids no search could name | 2100 Diseases - spolszczenie; **2132 MOD file override conflicts and PTF patch detection** (a conflict checker, same job as `tools/check_patch_names.py`); 2297 Ultimate Loadingscreen Artwork Overhaul; 2330 Compass and Map Upgrades - Wayfinder; **2345 Food and Drinks rebalance** (area of `krs_items`); **2362 Better Perk Descriptions** (area of `krs_perks`); 2365 KCDT |
| Page titles that differ from names used earlier in this review | 84 Archery - Realistic Arrow Flight (was the file name "Near Perfect Arrows"); 85 Perkaholic; 311 O' Hungry Henry; 390 Stay Clean Longer - Get Dirty Gradually; 483 and 791 and 1386 (Hoods ... UP variants); 1089 Overpowered Swords - PTF Edition; 1618 HD Clock Retexture; 1938 My Herb Picking Radius; 2079 Thin The Herd - Immersive Hunting and Realistic Animal Loot |

Effect on the triage (`TRIAGE.md`, `mods_triage.csv`): every mod now has an API name and description (**N**: 347, **A** archive read: 18; the former classes B, C, D no longer occur), keyword rules read the API description too, so the counts moved to P1 3, P2 129, P3 181, P4 52 and "likely collision" from 15 to 34 (for example 1996 Alcohol Is Not Food Anymore, 2011 Chefs Kiss, 1914 Weightless Herbs, 2207 Findable Herbs HD, 2276 Instant Herb and faster Alchemy Merger, 1292 Ultimate Repair Kit, 2362, 2345). The two removed pages go to P4. File lists and versions (`--files`, for "updated since the 1.9.7 patch") were not in the output yet.

**Is there a download script?** No. Nothing in the repository, the `Mods WIP folder` sources or the tools downloads a mod file, and `tools/nexus_metadata.py` calls no download endpoint (its self-test asserts it). The API does list a `download-repacked` endpoint, but a script using it would need the author's key and a decision per file; none was written. [`DOWNLOAD_SHORTLIST.md`](DOWNLOAD_SHORTLIST.md) lists the 51 published mods worth reading as archives next, with page and Files-tab links for a manual or Vortex download; the archives are then read with `tools/analyze_mod_archives.py`.


## 15. Read-only deep analysis of the P1/P2 mods (4 Oct 2026)

The author declared the downloaded mods the definitive list and asked for a read-only analysis of every P1 and P2 mod: what it changes, how, where, and how much, with no game run and no mod run. `tools/audit_mods_deep.py` did it for **138 archives, folders and loose files of 131 mods**. Everything below is **measured by reading** (evidence class A+); nothing was played.

**Safety.** Windows Security had recorded no threat detection (real-time protection on, signatures current). Each archive was listed with 7-Zip 26.03, judged from the list, extracted to a scratch folder, read with Python, and the folder was deleted (verified empty at the end). No file from an archive was executed, loaded or opened by anything but the reader. Vanilla tables were read from the game's `Tables.pak` and vanilla scripts from `Scripts.pak`, read-only.

**Risk result.** 128 clean, 4 kept with a note (a `.7zip` the game cannot read: 390, 1009, 1765; engine-config installer and a `loadstring` script: 2049), **6 quarantined** (moved to `Installed_to_review/_quarantine/`, nothing deleted): 770 Perkaholic 1.07 (pak entries that climb out of the pak with `../../../`), 1839 Realistic Horses (bundles the whole cheat-console framework and an `autocheat.lua` that removes and adds a perk at every start, beside its small horse-carrying-capacity data part), and four native plugins that cannot be verified by reading: 2246 Console Editable RpgParams (KCSE DLL), 2326 Permadeath (DLL plus `.cmd` installers), 2348 Zero Durability Repair (ASI), 2359 KcdCombatTune (two ASI). Static strings of the native files show no network, process-launch or downloader APIs, but that is not a safety proof. Per-case assessment: [`QUARANTINE.md`](QUARANTINE.md), `risk_notes.csv`.

**Grades** (rules in [`MOD_ANALYSIS.md`](MOD_ANALYSIS.md)): A changes the most 22, B large 22, C effective (few rows, strong effect) 52, D small tweak 14, E non-perceptive to gameplay 25, X not analysable 3 (two paks that are not ZIPs: 311 and the author's own early KRS-Items files under 2017).

**What the reading showed**
- **Whole-table replacement is common:** 426 table files in 14 archives have no suffix and replace a vanilla table outright (85, 480, 770, 802, 804, 883, 1062, 1260, 1334, 1424, 1629, 2124, 2299, 2345; 883 ships a full copy of the tables). Those overwrite the 1.9.7 table changes and win over every PTF patch that loads before them. **6 patch files of the old extracted Perkaholic folder (1009) sit outside `Libs/Tables`** and are never loaded; the `.rar` of 1009 is the working version.
- **1.9.8 manifest rule:** 101 archives load, **24 would be disabled** (the manifest lists only older versions: 85, 765, 1009, 1070, 1195, 1375, 1376, 1424, 1926, 1990, 2011, 2035, 2124 and others), 13 have no manifest (legacy copy into `Data`). Only the version label, not a compatibility test.
- **Bow mods all set hidden constants as new `rpg_param` rows** (`BowChargeDurationMin/Max`, `BowPowerToChargeDuration` in 802, 1100, 1419, 1564, 1678; the `Aim*` constants in 802, 804, 1419, 1564, 1678), which confirms the rule in `docs/engine/ptf-rules.md`. **1375 No Aim Spread takes the other route** (a new perk plus buff, perk_buff and soul2perk rows), which is the "perk" route of roadmap item 4.7, now seen in a published mod.
- **Combat AI is tuned through `CombatAuto*` and perfect-block `rpg_param` rows** (284, 1070, 1236, 1243 and others); `CombatAutoSPBWeight` alone is set by 12 of the 131 mods.
- **Contested rows:** 4605 table rows are changed by two or more mods (`mod_overlap.csv`); the biggest overlaps are among 2124, 2299, 883, 2340 and 1560 (the broad rebalances). **25 archives set rows that a KRS module also sets** (480, 651, 883, 1260, 1292, 1334, 1424, 1426, 1558, 1572, 1765, 1839, 1842, 1860, 1926, 1938, 1950, 2011, 2124, 2173, 2188, 2210, 2299, 2340, 2345): the later mod wins the whole row.
- **Small and strong:** the C list is where the project learns most per row: one-row mods such as 1425 (`ShoeHealthDecrease` 0.001 to 0), 1860 (`StrengthToInventoryCapacity`), 1938 (herb radius 0.25 to 0.5), 1578 (groschen weight 0 to 0.0005), 1426 (digestion and exhaustion speed for timescale mods).
- **Native route exists for runtime parameter work:** 2246 registers the rpg params as console variables (its strings), which the PTF route cannot do; it stays quarantined until a scan.

Files (generated): [`MOD_ANALYSIS.md`](MOD_ANALYSIS.md) (method, grading, ranking, overlaps), [`MOD_PROFILES.md`](MOD_PROFILES.md) (one section per archive), [`QUARANTINE.md`](QUARANTINE.md), `mod_analysis.csv`, `mod_tables.csv`, `mod_overlap.csv`, `risk_scan.csv`.
