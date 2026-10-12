# Sub-categories of the graded mods, and the ranking inside each one (generated)

> **GENERATED** by `tools/subcategorize_mods.py`: do not edit | **Kind:** review | **Trust:** derived from the read-only analysis in `docs/mods-review/mod_analysis.csv` (no archive was opened for this file) | **Game version:** 1.9.8

Read on 2026-10-04: the **129 mods graded A to E** in [`MOD_ANALYSIS.md`](MOD_ANALYSIS.md). Each one is put in a sub-category of mods that change the same tables (PTF) or the same kind of file, and inside that sub-category it is ranked. Per-mod detail: [`MOD_PROFILES.md`](MOD_PROFILES.md); the table behind this file: `mod_subcategories.csv`.

## How a mod lands in a sub-category

The sub-category is **the files a mod writes into, not what its page calls it**: two mods in the same sub-category patch the same tables, so they also collide with each other and can be compared row for row. The *Area in the index* column keeps the thematic label from `mods_index.csv` beside it, and the two sometimes disagree (a horse mod whose rows are all perks and buffs lands with the perk mods).

A mod is one row here; when it ships several archives (options or add-ons), the one measured is of the highest grade, then the one the game would load on 1.9.8, then the one that changes the most; the `variants` count in the CSV says how many there are.

1. **Native code or an external tool** (depth D4) goes in its own sub-category: what it does cannot be read from the files.
2. Otherwise, every changed or new table row is counted towards the system its table belongs to (`weapon` -> weapons, `shop_type2item` -> economy, `soul2perk` -> NPC loadout, ...). `rpg_param` is the one table every system writes into, so its rows are split over the systems its changed keys belong to (`Aim*`/`Bow*` -> archery, `*XP*` -> progression, `Pickpocketing*` -> crime, ...). `buff` rows support whatever else the mod changes, so they are shared out over its other systems.
3. A mod is a **multi-system overhaul** when it replaces 20 or more whole vanilla tables, or has 10 or more rows in six or more systems, or in four or more systems while touching 15 or more tables. Otherwise it goes to the sub-category of the system that holds most of its rows.
4. A mod that changes **no table row** is grouped by the file it does change: Lua, engine config, non-table XML, assets, or text.

## How the ranking is computed

Two scores, both 0 to 100, on the same scale for every mod, so they also compare across sub-categories.

Rows and tables are counted **once per distinct patch and once per vanilla table**: when one archive ships the same table three times as 2X, 3X and 5X option folders, only one of them can be installed, so it counts once. `MOD_ANALYSIS.md` adds the files up instead and counts table *files*, which is why its numbers are higher for 284, 651, 1260, 1334, 1483, 1563, 1736, 1862, 1863, 2124, 2294 (2294: 2985 rows in 55 files against 1300 rows in 10 tables). Both counts are in `mod_subcategories.csv`.

**Effect** - how much of the game it measurably changes: 28 % volume of changed rows (log scale), 14 % how many tables, 18 % median relative change of a changed cell, 20 % perceptibility from `MOD_ANALYSIS.md`, 10 % how many depth layers (D0 to D4), 10 % size of its Lua or config change.

**Build** - how well the archive is made. Starts at 100, then: -40 a pak that is not a ZIP, -35 a manifest that does not allow 1.9.8, -30 table patches outside `Libs/Tables` (never loaded), -30 a file suffix that is not the mod id its own manifest states (the game ignores the file), -12 the same when the deep analysis had to derive the id from the mod name, up to -25 for replacing whole vanilla tables instead of writing PTF patches (scaled by the share of its table files), up to -15 for vanilla rows those replacements drop, -25 HIGH risk, -10 MEDIUM risk, -10 no manifest; +5 every table file a correctly suffixed patch, +4 own text strings, +3 a readme, +3 optional variants.

The two weights for the same fault are deliberate: the suffix rule (`../engine/ptf-rules.md` rule 1) is measured, but an archive that bundles several sub-mods has one `mod.manifest` per sub-mod and the deep analysis compared every file against one derived id, so there the finding is a doubt to confirm per sub-mod, not a fault (284, 1578, 1736, 1893, 2124). Where the manifest states the id, it is a fault (1883).

**Overall** = 0.55 x effect + 0.45 x build, and that is the rank. In *Native code and external tools* there is nothing to measure, so the rank there is build first.

### What these numbers do not say

- No mod was installed or run, and no game test was made: this is what the files say, not how the mod plays.
- A high effect score is not an endorsement: it means the mod changes a lot, not that the change is good or balanced.
- Non-table XML (entities, particles, audio definitions), native code and assets cannot be compared with vanilla by this method, so mods made of those get a low effect score even when they work perfectly. In their sub-categories the ranking is about how well the archive is made.
- Nexus endorsements, versions and update dates are not in the data (`mods_triage.csv` has them for only a few mods), so popularity and how recently a mod was updated are not part of the score.

## Sub-categories per grade

| Grade | Mods | Sub-categories |
|---|---|---|
| A changes the most | 22 | Multi-system overhaul (4); Combat mechanics and AI (4); Native code and external tools (4); Economy, loot and item stats (3); Weapons, armour and durability (2); Perks, skills and XP (2); Alchemy, food and survival (2); NPC perks, skills and archetypes (1) |
| B large | 21 | Economy, loot and item stats (5); Alchemy, food and survival (4); Perks, skills and XP (3); Combat mechanics and AI (3); NPCs, quests and world content (2); Lua scripts only (2); Multi-system overhaul (1); Weapons, armour and durability (1) |
| C effective (few rows, strong effect) | 49 | Alchemy, food and survival (11); Perks, skills and XP (10); Archery: bows, arrows, aiming (9); Economy, loot and item stats (7); Weapons, armour and durability (5); Combat mechanics and AI (4); NPCs, quests and world content (2); Crime, stealth and reputation (1) |
| D small tweak | 14 | Lua scripts only (9); Engine config (.cfg) only (2); Perks, skills and XP (1); NPCs, quests and world content (1); Economy, loot and item stats (1) |
| E non-perceptive to gameplay (content or text only) | 13 | Textures, models and other assets (9); UI text and localisation (4) |
| E non-perceptive to gameplay (no effective change found) | 10 | Non-table XML (entities, effects, audio definitions) (7); Nothing readable / no change found (3) |

## A changes the most (22 mods)

### A - Combat mechanics and AI (4)

| # | Id | Mod | Area in the index | Overall | Effect | Build | 1.9.8 | What it changes | Build notes |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 1148 | Combo and Weapon rebalance | Combat / AI | 78 | 59 | 100 | yes | 674 rows in 2 tables - 89% in combat, weapons | every table file is a correctly suffixed PTF patch |
| 2 | 2294 | Faster Combat - Directional Master Strikes - B | Combat / AI | 76 | 56 | 100 | yes | 1300 rows in 10 tables - 100% in combat, perks and skills | every table file is a correctly suffixed PTF patch; ships a readme; 32 table files are a repeat of another one in the same archive (alternative options), counted once here |
| 3 | 1563 | Karnages_Polearm_Restoration 2.0 | Weapons / armor / items | 74 | 52 | 100 | yes | 159 rows in 18 tables - 43% in combat, weapons, economy | every table file is a correctly suffixed PTF patch; ships its own text strings; 9 table files are a repeat of another one in the same archive (alternative options), counted once here |
| 4 | 2049 | Simple Ragdoll Physics | Combat / AI | 69 | 71 | 67 | no | 1659 rows in 11 tables - 97% in combat, archery, item stats | the manifest does not allow 1.9.8; MEDIUM risk in the scan; every table file is a correctly suffixed PTF patch; ships its own text strings; ships a readme |

**Pick:** 1148 Combo and Weapon rebalance. Changes the most: 2049 Simple Ragdoll Physics (effect 71). Does not load on 1.9.8: 2049.

### A - Multi-system overhaul (4)

| # | Id | Mod | Area in the index | Overall | Effect | Build | 1.9.8 | What it changes | Build notes |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 2299 | 1403 - Historical Rebalance | Progression / XP / perks | 87 | 77 | 100 | yes | 8518 rows in 33 tables - 16 systems: item stats, economy, armour, combat, NPCs | 1 of 33 table files replace a whole vanilla table (3%): collides with every other mod on those tables; those replacements drop 14 vanilla rows; ships its own text strings; ships a readme |
| 2 | 651 | Better Combat and Immersion Compilation | Combat / AI | 78 | 60 | 100 | yes | 444 rows in 14 tables - 11 systems: combat, armour, economy, alchemy, NPCs | every table file is a correctly suffixed PTF patch; ships its own text strings; ships a readme |
| 3 | 2124 | Half-looted Rebalance | Progression / XP / perks | 63 | 79 | 44 | no | 22619 rows in 35 tables - 13 systems: NPC loadout, economy, armour, combat, item stats | the deep analysis found a table file whose suffix is not the mod id it derived from the mod name (no modid in the manifest): to be confirmed per sub-mod; the manifest does not allow 1.9.8; 3 of 58 table files replace a whole vanilla table (5%): collides with every other mod on those tables; those replacements drop 3344 vanilla rows; ships its own text strings; ships a readme |
| 4 | 883 | KingdomCome Rebalancing | Progression / XP / perks | 61 | 63 | 59 | legacy | 16869 rows in 17 tables - 11 systems: quests and text, economy, item stats, armour, weapons | no mod.manifest: legacy loose pak; 399 of 400 table files replace a whole vanilla table (100%): collides with every other mod on those tables; those replacements drop 121 vanilla rows; ships its own text strings |

**Pick:** 2299 1403 - Historical Rebalance. Changes the most: 2124 Half-looted Rebalance (effect 79). Does not load on 1.9.8: 2124.

### A - Native code and external tools (4)

| # | Id | Mod | Area in the index | Overall | Effect | Build | 1.9.8 | What it changes | Build notes |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 2326 | Permanent Death | Progression / XP / perks | 58 | n/a | 82 | yes | native code or an external tool | HIGH risk in the scan (quarantined); ships its own text strings; ships a readme |
| 2 | 2348 | KCD Zero Durability Repair | Weapons / armor / items | 41 | n/a | 75 | yes | native code or an external tool | HIGH risk in the scan (quarantined) |
| 2 | 2359 | KCD Kombat Tune | Combat / AI | 41 | n/a | 75 | yes | native code or an external tool | HIGH risk in the scan (quarantined) |
| 4 | 2246 | Console Editable RpgParams | Progression / XP / perks | 36 | n/a | 65 | legacy | native code or an external tool | no mod.manifest: legacy loose pak; HIGH risk in the scan (quarantined) |

**Pick:** 2326 Permanent Death.

### A - Economy, loot and item stats (3)

| # | Id | Mod | Area in the index | Overall | Effect | Build | 1.9.8 | What it changes | Build notes |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 2219 | True Hardcore Crime (PTF) | Crime / stealth / loot | 83 | 68 | 100 | yes | 544 rows in 8 tables - 84% in item stats, crime, perks and skills | every table file is a correctly suffixed PTF patch; ships its own text strings |
| 2 | 2188 | True Hardcore Economy (PTF) | Combat / AI | 81 | 66 | 100 | yes | 456 rows in 12 tables - 92% in economy, item stats, quests and text | every table file is a correctly suffixed PTF patch; ships its own text strings |
| 3 | 2340 | MatthusTweaks - Equipment and Progression Over | Progression / XP / perks | 74 | 54 | 100 | yes | 1632 rows in 12 tables - 72% in item stats, armour, weapons | every table file is a correctly suffixed PTF patch; 3 archives: optional variants |

**Pick:** 2219 True Hardcore Crime (PTF).

### A - Alchemy, food and survival (2)

| # | Id | Mod | Area in the index | Overall | Effect | Build | 1.9.8 | What it changes | Build notes |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 2210 | True Hardcore Alchemy (PTF) | Combat / AI | 79 | 62 | 100 | yes | 222 rows in 5 tables - 99% in alchemy, survival, item stats | every table file is a correctly suffixed PTF patch; ships its own text strings |
| 2 | 2208 | Medieval Poisons - True Hardcore Compatibility | Combat / AI | 76 | 57 | 100 | yes | 41 rows in 6 tables - 81% in alchemy, quests and text, economy | every table file is a correctly suffixed PTF patch; ships its own text strings |

**Pick:** 2210 True Hardcore Alchemy (PTF).

### A - Perks, skills and XP (2)

| # | Id | Mod | Area in the index | Overall | Effect | Build | 1.9.8 | What it changes | Build notes |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 2338 | Horse Collision Mod | Horses | 70 | 46 | 100 | yes | 11 rows in 4 tables - 100% in perks and skills | every table file is a correctly suffixed PTF patch; ships its own text strings; ships a readme |
| 2 | 1736 | Rogue Life | Progression / XP / perks | 62 | 60 | 65 | no | 62 rows in 7 tables - 77% in perks and skills, crime, quests and text | the deep analysis found a table file whose suffix is not the mod id it derived from the mod name (no modid in the manifest): to be confirmed per sub-mod; the manifest does not allow 1.9.8; every table file is a correctly suffixed PTF patch; ships its own text strings; ships a readme; 7 table files are a repeat of another one in the same archive (alternative options), counted once here |

**Pick:** 2338 Horse Collision Mod. Changes the most: 1736 Rogue Life (effect 60). Does not load on 1.9.8: 1736.

### A - Weapons, armour and durability (2)

| # | Id | Mod | Area in the index | Overall | Effect | Build | 1.9.8 | What it changes | Build notes |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 1560 | Karnages_Durability_Redux | Weapons / armor / items | 78 | 60 | 100 | yes | 964 rows in 2 tables - 100% in armour, weapons | every table file is a correctly suffixed PTF patch |
| 2 | 1839 | Realistic Horses | Horses | 65 | 52 | 80 | yes | 27 rows in 4 tables - 91% in armour, item stats, NPCs | HIGH risk in the scan (quarantined); every table file is a correctly suffixed PTF patch |

**Pick:** 1560 Karnages_Durability_Redux.

### A - NPC perks, skills and archetypes (1)

Only one mod of this grade changes this: **1629 Exclusive Master Strikes - Make Them Reasonable** (Combat / AI; effect 56, build 42; 2424 rows in 2 tables - 100% in NPC loadout, perks and skills). Nothing to rank it against in this grade; the cross-grade table at the end of this file says which other grades hold the same sub-category. Notes: the manifest does not allow 1.9.8; 1 of 2 table files replace a whole vanilla table (50%): collides with every other mod on those tables; those replacements drop 4692 vanilla rows; ships its own text strings.

## B large (21 mods)

### B - Economy, loot and item stats (5)

| # | Id | Mod | Area in the index | Overall | Effect | Build | 1.9.8 | What it changes | Build notes |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 1062 | SIM Camping Mini ML 1.5.1.1 | Alchemy / food / survival | 75 | 55 | 100 | yes | 51 rows in 11 tables - 76% in item stats, economy, alchemy | 1 of 11 table files replace a whole vanilla table (9%): collides with every other mod on those tables; ships its own text strings |
| 2 | 2045 | Polearms Unleashed Rebalanced Lite Edition PTF | Weapons / armor / items | 72 | 48 | 100 | yes | 106 rows in 12 tables - 38% in combat, economy, weapons | every table file is a correctly suffixed PTF patch |
| 3 | 2209 | Poisonous Enemies - True Hardcore Compatibilit | Combat / AI | 68 | 42 | 100 | yes | 36 rows in 6 tables - 88% in economy, armour, item stats | every table file is a correctly suffixed PTF patch; ships its own text strings |
| 4 | 1380 | Black Items Fix | Weapons / armor / items | 67 | 40 | 100 | yes | 59 rows in 8 tables - 68% in item stats, armour, economy | every table file is a correctly suffixed PTF patch; ships its own text strings |
| 5 | 2035 | Ordinance an Archery Overhaul | Archery / arrows | 55 | 40 | 73 | no | 58 rows in 8 tables - 38% in item stats, archery, weapons | the manifest does not allow 1.9.8; every table file is a correctly suffixed PTF patch; ships a readme |

**Pick:** 1062 SIM Camping Mini ML 1.5.1.1. Does not load on 1.9.8: 2035.

### B - Alchemy, food and survival (4)

| # | Id | Mod | Area in the index | Overall | Effect | Build | 1.9.8 | What it changes | Build notes |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 1483 | TSM Slower Food Spoil | Alchemy / food / survival | 75 | 54 | 100 | yes | 111 rows in 1 table - 100% in alchemy | every table file is a correctly suffixed PTF patch; ships a readme; 2 table files are a repeat of another one in the same archive (alternative options), counted once here |
| 2 | 1639 | Alternate Food Spoil (2X) | Alchemy / food / survival | 70 | 45 | 100 | yes | 111 rows in 1 table - 100% in alchemy | every table file is a correctly suffixed PTF patch |
| 3 | 2011 | Chefs Kiss | Alchemy / food / survival | 64 | 53 | 77 | no | 323 rows in 7 tables - 82% in alchemy, item stats | the manifest does not allow 1.9.8; every table file is a correctly suffixed PTF patch; ships its own text strings; ships a readme |
| 4 | 2345 | Food and Drinks rebalance | Alchemy / food / survival | 56 | 41 | 75 | yes | 155 rows in 1 table - 100% in alchemy | its only table file replaces a whole vanilla table instead of patching it: collides with every other mod on that table |

**Pick:** 1483 TSM Slower Food Spoil. Does not load on 1.9.8: 2011.

### B - Combat mechanics and AI (3)

| # | Id | Mod | Area in the index | Overall | Effect | Build | 1.9.8 | What it changes | Build notes |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 2179 | True Hardcore Combat (PTF) | Combat / AI | 72 | 49 | 100 | yes | 220 rows in 11 tables - 39% in combat, NPCs, archery | every table file is a correctly suffixed PTF patch; ships its own text strings |
| 2 | 1112 | Combat Overhaul | Combat / AI | 70 | 45 | 100 | yes | 243 rows in 5 tables - 81% in combat, perks and skills, progression | every table file is a correctly suffixed PTF patch |
| 3 | 1384 | Modified Combat Overhaul - Directional Combat  | Combat / AI | 66 | 43 | 95 | legacy | 181 rows in 4 tables - 97% in combat, perks and skills, durability | no mod.manifest: legacy loose pak; every table file is a correctly suffixed PTF patch |

**Pick:** 2179 True Hardcore Combat (PTF).

### B - Perks, skills and XP (3)

| # | Id | Mod | Area in the index | Overall | Effect | Build | 1.9.8 | What it changes | Build notes |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 1009 | Perkaholic - PTF updated (1.9.4-1.9.8) | Progression / XP / perks | 70 | 45 | 100 | yes | 194 rows in 6 tables - 100% in perks and skills | every table file is a correctly suffixed PTF patch; ships its own text strings; 2 archives: optional variants |
| 2 | 770 | Perkaholic updated | Progression / XP / perks | 48 | 44 | 54 | yes | 186 rows in 4 tables - 100% in perks and skills | 5 of 5 table files replace a whole vanilla table (100%): collides with every other mod on those tables; HIGH risk in the scan (quarantined); ships its own text strings |
| 3 | 85 | Perkaholic | Progression / XP / perks | 42 | 47 | 36 | no | 274 rows in 6 tables - 100% in perks and skills | the manifest does not allow 1.9.8; 6 of 6 table files replace a whole vanilla table (100%): collides with every other mod on those tables; those replacements drop 156 vanilla rows; ships its own text strings; ships a readme |

**Pick:** 1009 Perkaholic - PTF updated (1.9.4-1.9.8). Changes the most: 85 Perkaholic (effect 47). Does not load on 1.9.8: 85.

### B - Lua scripts only (2)

| # | Id | Mod | Area in the index | Overall | Effect | Build | 1.9.8 | What it changes | Build notes |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 2318 | Visual Combo Helper | Combat / AI | 63 | 33 | 100 | yes | 2388 lines of Lua, no table row | ships a readme |
| 2 | 2323 | Alchemy Stash Link | Alchemy / food / survival | 59 | 26 | 100 | yes | 1052 lines of Lua, no table row | nothing against it |

**Pick:** 2318 Visual Combo Helper.

### B - NPCs, quests and world content (2)

| # | Id | Mod | Area in the index | Overall | Effect | Build | 1.9.8 | What it changes | Build notes |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 2343 | Ultimate Horse Caparison Fix | Horses | 66 | 38 | 100 | yes | 6 rows in 2 tables - 100% in NPCs, quests and text | every table file is a correctly suffixed PTF patch; ships a readme |
| 2 | 1105 | Service Prices | Economy / merchants | 64 | 34 | 100 | yes | 6 rows in 1 table - 100% in quests and text | every table file is a correctly suffixed PTF patch |

**Pick:** 2343 Ultimate Horse Caparison Fix.

### B - Multi-system overhaul (1)

Only one mod of this grade changes this: **1558 Karnages_KCD_Essential_Fixes 2.0** (Fix bundle; effect 47, build 100; 155 rows in 3 tables - 11 systems: quests and text, progression, combat, perks and skills, crime). Nothing to rank it against in this grade; the cross-grade table at the end of this file says which other grades hold the same sub-category. Notes: every table file is a correctly suffixed PTF patch; ships a readme.

### B - Weapons, armour and durability (1)

Only one mod of this grade changes this: **2173 True Hardcore Maintenance (PTF)** (Repair / durability; effect 48, build 100; 48 rows in 8 tables - 56% in armour, item stats, perks and skills). Nothing to rank it against in this grade; the cross-grade table at the end of this file says which other grades hold the same sub-category. Notes: every table file is a correctly suffixed PTF patch; ships its own text strings.

## C effective (few rows, strong effect) (49 mods)

### C - Alchemy, food and survival (11)

| # | Id | Mod | Area in the index | Overall | Effect | Build | 1.9.8 | What it changes | Build notes |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 1660 | Double Brew Yield | Alchemy / food / survival | 68 | 42 | 100 | yes | 35 rows in 1 table - 100% in alchemy | every table file is a correctly suffixed PTF patch |
| 2 | 2021 | Repair Kits - Balanced and Scaled PTF | Weapons / armor / items | 66 | 38 | 100 | yes | 8 rows in 1 table - 100% in alchemy | every table file is a correctly suffixed PTF patch |
| 3 | 1266 | Stronger drinks - PTF Edition | Alchemy / food / survival | 64 | 34 | 100 | yes | 9 rows in 1 table - 100% in alchemy | every table file is a correctly suffixed PTF patch |
| 3 | 1938 | My Herb Picking Radius | Alchemy / food / survival | 64 | 34 | 100 | yes | 1 row in 1 table - 100% in survival | every table file is a correctly suffixed PTF patch |
| 5 | 390 | Stay Clean Longer - Get Dirty Gradually | Alchemy / food / survival | 62 | 36 | 95 | yes | 2 rows in 2 tables - 50% in perks and skills, survival | MEDIUM risk in the scan; every table file is a correctly suffixed PTF patch |
| 6 | 765 | Poison Overhaul | Alchemy / food / survival | 62 | 52 | 74 | no | 15 rows in 4 tables - 60% in alchemy, perks and skills | the manifest does not allow 1.9.8; every table file is a correctly suffixed PTF patch; ships its own text strings |
| 7 | 1730 | Drink Sound Effects | Alchemy / food / survival | 60 | 32 | 95 | legacy | 18 rows in 2 tables - 50% in alchemy, item stats | no mod.manifest: legacy loose pak; every table file is a correctly suffixed PTF patch |
| 8 | 1426 | Energy and Hunger Patch for Timescale Mods (PT | Alchemy / food / survival | 59 | 26 | 100 | yes | 2 rows in 1 table - 100% in survival | every table file is a correctly suffixed PTF patch |
| 9 | 1926 | Potion no Satiety and ADD Heal plus Energy | Alchemy / food / survival | 54 | 41 | 70 | no | 22 rows in 1 table - 100% in alchemy | the manifest does not allow 1.9.8; every table file is a correctly suffixed PTF patch |
| 10 | 480 | Bed Comfort Restored | Alchemy / food / survival | 52 | 33 | 75 | yes | 5 rows in 1 table - 100% in survival | its only table file replaces a whole vanilla table instead of patching it: collides with every other mod on that table |
| 11 | 1424 | Better Sleep Fixed | Alchemy / food / survival | 40 | 40 | 40 | no | 5 rows in 1 table - 100% in survival | the manifest does not allow 1.9.8; its only table file replaces a whole vanilla table instead of patching it: collides with every other mod on that table |

**Pick:** 1660 Double Brew Yield. Changes the most: 765 Poison Overhaul (effect 52). Does not load on 1.9.8: 765, 1926, 1424.

### C - Perks, skills and XP (10)

| # | Id | Mod | Area in the index | Overall | Effect | Build | 1.9.8 | What it changes | Build notes |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 1572 | Increased Experience Gains | Progression / XP / perks | 66 | 38 | 100 | yes | 39 rows in 1 table - 76% in progression, crime, durability | every table file is a correctly suffixed PTF patch |
| 2 | 1863 | Dirty And Charismatic - PTF | Progression / XP / perks | 65 | 36 | 100 | yes | 3 rows in 1 table - 100% in perks and skills | every table file is a correctly suffixed PTF patch |
| 3 | 1842 | Realistic Repairs | Weapons / armor / items | 64 | 35 | 100 | yes | 8 rows in 3 tables - 62% in perks and skills, durability, economy | every table file is a correctly suffixed PTF patch |
| 4 | 1334 | Fast Learning Henry | Progression / XP / perks | 63 | 54 | 75 | yes | 96 rows in 1 table - 62% in progression, crime, combat | 2 of 2 table files replace a whole vanilla table (100%): collides with every other mod on those tables |
| 5 | 1862 | Faster Inury Regeneration - PTF | Alchemy / food / survival | 62 | 30 | 100 | yes | 2 rows in 1 table - 100% in perks and skills | every table file is a correctly suffixed PTF patch |
| 6 | 1292 | Ultimate Repair Kit 2.0 | Weapons / armor / items | 61 | 28 | 100 | yes | 4 rows in 3 tables - 75% in perks and skills, durability | every table file is a correctly suffixed PTF patch |
| 7 | 1070 | Better Combat | Combat / AI | 55 | 40 | 73 | no | 32 rows in 2 tables - 53% in perks and skills, combat, archery | the manifest does not allow 1.9.8; every table file is a correctly suffixed PTF patch; ships a readme |
| 8 | 1375 | No Aim Spread (Bow sway disabler) | Archery / arrows | 51 | 32 | 74 | no | 5 rows in 5 tables - 50% in perks and skills, NPC loadout, survival | the manifest does not allow 1.9.8; every table file is a correctly suffixed PTF patch; ships its own text strings |
| 9 | 1260 | RPG Tweaks | Progression / XP / perks | 51 | 41 | 63 | yes | 95 rows in 2 tables - 48% in progression, perks and skills, combat | 3 of 3 table files replace a whole vanilla table (100%): collides with every other mod on those tables; those replacements drop 249 vanilla rows |
| 10 | 1765 | Restore Riposte | Combat / AI | 48 | 36 | 64 | no | 2 rows in 1 table - 100% in perks and skills | the manifest does not allow 1.9.8; MEDIUM risk in the scan; every table file is a correctly suffixed PTF patch; ships its own text strings |

**Pick:** 1572 Increased Experience Gains. Changes the most: 1334 Fast Learning Henry (effect 54). Does not load on 1.9.8: 1070, 1375, 1765.

### C - Archery: bows, arrows, aiming (9)

| # | Id | Mod | Area in the index | Overall | Effect | Build | 1.9.8 | What it changes | Build notes |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 1565 | Karnages_Arrow_Balance 2.0 | Archery / arrows | 66 | 39 | 100 | yes | 12 rows in 1 table - 100% in archery | every table file is a correctly suffixed PTF patch |
| 2 | 1419 | Immersive Archery | Archery / arrows | 65 | 37 | 100 | yes | 20 rows in 2 tables - 100% in archery | every table file is a correctly suffixed PTF patch |
| 3 | 1678 | Better Archery | Archery / arrows | 65 | 36 | 100 | yes | 21 rows in 2 tables - 100% in archery | every table file is a correctly suffixed PTF patch |
| 4 | 1564 | Karnages_Rebalanced_Bows 2.0 | Archery / arrows | 64 | 35 | 100 | yes | 30 rows in 2 tables - 100% in archery | every table file is a correctly suffixed PTF patch |
| 5 | 1084 | Overpowered Bows - PTF Edition | Archery / arrows | 62 | 31 | 100 | yes | 2 rows in 1 table - 100% in archery | every table file is a correctly suffixed PTF patch |
| 6 | 1100 | Faster archery - PTF Edition | Archery / arrows | 60 | 27 | 100 | yes | 3 rows in 1 table - 100% in archery | every table file is a correctly suffixed PTF patch |
| 7 | 1376 | Archery mod - Faster arrows (for real) | Archery / arrows | 52 | 38 | 70 | no | 14 rows in 1 table - 100% in archery | the manifest does not allow 1.9.8; every table file is a correctly suffixed PTF patch |
| 8 | 804 | Loose (An Archery Mod) | Archery / arrows | 51 | 32 | 75 | yes | 11 rows in 1 table - 100% in archery | its only table file replaces a whole vanilla table instead of patching it: collides with every other mod on that table |
| 9 | 802 | Archery for 1.9 | Archery / arrows | 48 | 34 | 65 | legacy | 10 rows in 1 table - 100% in archery | no mod.manifest: legacy loose pak; its only table file replaces a whole vanilla table instead of patching it: collides with every other mod on that table |

**Pick:** 1565 Karnages_Arrow_Balance 2.0. Does not load on 1.9.8: 1376.

### C - Economy, loot and item stats (7)

| # | Id | Mod | Area in the index | Overall | Effect | Build | 1.9.8 | What it changes | Build notes |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 1864 | Cheap Savior Schnapps - PTF | Economy / merchants | 75 | 54 | 100 | yes | 89 rows in 3 tables - 99% in economy, alchemy, item stats | every table file is a correctly suffixed PTF patch |
| 2 | 1853 | Richer Merchants (PTF) | Economy / merchants | 74 | 53 | 100 | yes | 78 rows in 1 table - 100% in economy | every table file is a correctly suffixed PTF patch |
| 2 | 2165 | Merchants Richer | Economy / merchants | 74 | 53 | 100 | yes | 79 rows in 1 table - 100% in economy | every table file is a correctly suffixed PTF patch |
| 4 | 1914 | Weightless Herbs | Alchemy / food / survival | 67 | 40 | 100 | yes | 17 rows in 1 table - 100% in item stats | every table file is a correctly suffixed PTF patch |
| 5 | 1578 | Weighed Groschen - PTF Version | Economy / merchants | 60 | 34 | 93 | yes | 1 row in 1 table - 100% in item stats | the deep analysis found a table file whose suffix is not the mod id it derived from the mod name (no modid in the manifest): to be confirmed per sub-mod; every table file is a correctly suffixed PTF patch |
| 6 | 1860 | Train More Carry More - PTF | Progression / XP / perks | 59 | 25 | 100 | yes | 1 row in 1 table - 100% in item stats | every table file is a correctly suffixed PTF patch |
| 7 | 1195 | Get Water | Alchemy / food / survival | 52 | 34 | 74 | no | 4 rows in 4 tables - 100% in item stats | the manifest does not allow 1.9.8; every table file is a correctly suffixed PTF patch; ships its own text strings |

**Pick:** 1864 Cheap Savior Schnapps - PTF. Does not load on 1.9.8: 1195.

### C - Weapons, armour and durability (5)

| # | Id | Mod | Area in the index | Overall | Effect | Build | 1.9.8 | What it changes | Build notes |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 1559 | Karnages_Weapons_Damage_Balance 2.0 | Weapons / armor / items | 73 | 51 | 100 | yes | 77 rows in 1 table - 100% in weapons | every table file is a correctly suffixed PTF patch |
| 2 | 1545 | Saddles Have Durability | Weapons / armor / items | 67 | 40 | 100 | yes | 20 rows in 1 table - 100% in armour | every table file is a correctly suffixed PTF patch |
| 3 | 1425 | Saving Soles (PTF) | Weapons / armor / items | 64 | 34 | 100 | yes | 1 row in 1 table - 100% in durability | every table file is a correctly suffixed PTF patch |
| 4 | 1893 | Bianca's Ring PTF | Weapons / armor / items | 61 | 36 | 93 | yes | 2 rows in 2 tables - 100% in armour | the deep analysis found a table file whose suffix is not the mod id it derived from the mod name (no modid in the manifest): to be confirmed per sub-mod; every table file is a correctly suffixed PTF patch |
| 5 | 1782 | No more clipping elbows for Andrew | World / weather / visuals | 61 | 28 | 100 | yes | 5 rows in 2 tables - 80% in armour, NPCs | every table file is a correctly suffixed PTF patch |

**Pick:** 1559 Karnages_Weapons_Damage_Balance 2.0.

### C - Combat mechanics and AI (4)

| # | Id | Mod | Area in the index | Overall | Effect | Build | 1.9.8 | What it changes | Build notes |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 1236 | Easy Combat PTF (easy parry and master strike) | Combat / AI | 69 | 44 | 100 | yes | 2 rows in 1 table - 50% in combat, progression | every table file is a correctly suffixed PTF patch |
| 2 | 284 | No Mo' Slow Mo - Configurable Perfect Block Sl | Crime / stealth / loot | 67 | 44 | 96 | yes | 2 rows in 1 table - 100% in combat | the deep analysis found a table file whose suffix is not the mod id it derived from the mod name (no modid in the manifest): to be confirmed per sub-mod; every table file is a correctly suffixed PTF patch; ships a readme; 1 table files are a repeat of another one in the same archive (alternative options), counted once here |
| 3 | 1668 | Relaxed RPG Params | Progression / XP / perks | 66 | 37 | 100 | yes | 33 rows in 1 table - 25% in combat, durability, horses | every table file is a correctly suffixed PTF patch |
| 4 | 1243 | Easier Enemies PTF (Dumber Enemies) | Combat / AI | 64 | 35 | 100 | yes | 8 rows in 1 table - 100% in combat | every table file is a correctly suffixed PTF patch; 2 archives: optional variants |

**Pick:** 1236 Easy Combat PTF (easy parry and master strike).

### C - NPCs, quests and world content (2)

| # | Id | Mod | Area in the index | Overall | Effect | Build | 1.9.8 | What it changes | Build notes |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 1950 | Skill Books Take Time | Progression / XP / perks | 69 | 44 | 100 | yes | 57 rows in 2 tables - 98% in quests and text, progression | every table file is a correctly suffixed PTF patch |
| 2 | 1990 | Veteran Hunting | Alchemy / food / survival | 58 | 45 | 74 | no | 11 rows in 4 tables - 78% in NPCs, perks and skills | the manifest does not allow 1.9.8; every table file is a correctly suffixed PTF patch; ships its own text strings |

**Pick:** 1950 Skill Books Take Time. Changes the most: 1990 Veteran Hunting (effect 45). Does not load on 1.9.8: 1990.

### C - Crime, stealth and reputation (1)

Only one mod of this grade changes this: **1883 Better Pickpocket - FIXED** (Crime / stealth / loot; effect 42, build 70; 17 rows in 1 table - 100% in crime). Nothing to rank it against in this grade; the cross-grade table at the end of this file says which other grades hold the same sub-category. Notes: 1 table file whose suffix is not the mod id of its manifest (the game ignores it).

## D small tweak (14 mods)

### D - Lua scripts only (9)

| # | Id | Mod | Area in the index | Overall | Effect | Build | 1.9.8 | What it changes | Build notes |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 1520 | Shooting Archery Targets Gives XP | Progression / XP / perks | 58 | 23 | 100 | yes | 232 lines of Lua, no table row | nothing against it |
| 2 | 1519 | Shooting Nests Gives XP | Progression / XP / perks | 58 | 23 | 100 | yes | 179 lines of Lua, no table row | nothing against it |
| 3 | 2194 | ENHANCED Easy FREE Combat Target Overhaul v3.0 | Combat / AI | 58 | 23 | 100 | yes | 158 lines of Lua, no table row | nothing against it |
| 4 | 2372 | Trough Washing Animation | Alchemy / food / survival | 54 | 17 | 100 | yes | 30 lines of Lua, no table row | nothing against it |
| 5 | 1655 | Save Me Henry | Progression / XP / perks | 53 | 15 | 100 | yes | 137 lines of Lua, no table row | nothing against it |
| 6 | 1518 | Waystones Give XP | Progression / XP / perks | 53 | 15 | 100 | yes | 67 lines of Lua, no table row | nothing against it |
| 6 | 2192 | ENHANCED Toggle Aim Overhaul v2.0 KCD I | Combat / AI | 53 | 15 | 100 | yes | 63 lines of Lua, no table row | nothing against it |
| 8 | 1647 | Slo Mo Begone | Combat / AI | 46 | 3 | 100 | yes | 21 lines of Lua, no table row | nothing against it |
| 9 | 1040 | Disable Combat Slowmotion | Combat / AI | 31 | 2 | 65 | no | 3 lines of Lua, no table row | the manifest does not allow 1.9.8 |

**Pick:** 1520 Shooting Archery Targets Gives XP. Does not load on 1.9.8: 1040.

### D - Engine config (.cfg) only (2)

| # | Id | Mod | Area in the index | Overall | Effect | Build | 1.9.8 | What it changes | Build notes |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 83 | More Responsive Targeting | Combat / AI | 51 | 18 | 90 | legacy | 16 engine config keys, no table row | no mod.manifest: legacy loose pak |
| 2 | 1612 | Remove Auto Camera Lock In Combat | Combat / AI | 49 | 16 | 90 | legacy | 4 engine config keys, no table row | no mod.manifest: legacy loose pak |

**Pick:** 83 More Responsive Targeting.

### D - Economy, loot and item stats (1)

Only one mod of this grade changes this: **1693 Ravens beak and Spiked warhammer icon swap** (Weapons / armor / items; effect 18, build 70; 2 rows in 1 table - 100% in item stats). Nothing to rank it against in this grade; the cross-grade table at the end of this file says which other grades hold the same sub-category. Notes: the manifest does not allow 1.9.8; every table file is a correctly suffixed PTF patch.

### D - NPCs, quests and world content (1)

Only one mod of this grade changes this: **1671 Angriness Begone** (Combat / AI; effect 30, build 100; 7 rows in 1 table - 100% in NPCs). Nothing to rank it against in this grade; the cross-grade table at the end of this file says which other grades hold the same sub-category. Notes: every table file is a correctly suffixed PTF patch.

### D - Perks, skills and XP (1)

Only one mod of this grade changes this: **1569 Karnages_Shield_Restoration** (Weapons / armor / items; effect 17, build 100; 1 row in 1 table - 100% in perks and skills). Nothing to rank it against in this grade; the cross-grade table at the end of this file says which other grades hold the same sub-category. Notes: every table file is a correctly suffixed PTF patch.

## E non-perceptive to gameplay (content or text only) (13 mods)

### E - Textures, models and other assets (9)

| # | Id | Mod | Area in the index | Overall | Effect | Build | 1.9.8 | What it changes | Build notes |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 366 | First-person Herb Picking | Alchemy / food / survival | 50 | 8 | 100 | yes | 2 asset files, no table row | nothing against it |
| 1 | 1090 | Colored Arrows | Archery / arrows | 50 | 8 | 100 | yes | 11 asset files, no table row | nothing against it |
| 1 | 1323 | Skalitz Shield Fix AWL | Weapons / armor / items | 50 | 8 | 100 | yes | 7 asset files, no table row | ships a readme |
| 1 | 2207 | Findable Herbs HD | Alchemy / food / survival | 50 | 8 | 100 | yes | 1 asset file, no table row | nothing against it |
| 1 | 2276 | Instant Herb and faster Alchemy Merger | Alchemy / food / survival | 50 | 8 | 100 | yes | 4 asset files, no table row | nothing against it |
| 1 | 2331 | Bushes Collision Remover Redux | World / weather / visuals | 50 | 8 | 100 | yes | 26 asset files, no table row | ships a readme |
| 7 | 591 | Bushes- Collision Remover | World / weather / visuals | 45 | 8 | 90 | legacy | 26 asset files, no table row | no mod.manifest: legacy loose pak |
| 8 | 1205 | ETSGF - Easy to see glowing Arrow feathers  -  | Archery / arrows | 35 | 8 | 68 | no | 10 asset files, no table row | the manifest does not allow 1.9.8; 2 archives: optional variants |
| 9 | 1991 | BCAIC - Restore Hunting Spots - Patch | Alchemy / food / survival | 34 | 8 | 65 | no | 2 asset files, no table row | the manifest does not allow 1.9.8 |

**No pick on effect:** this method cannot measure what these change, so the order is how well the archive is made only. Best made: 366 First-person Herb Picking, 1090 Colored Arrows, 1323 Skalitz Shield Fix AWL, 2207 Findable Herbs HD, 2276 Instant Herb and faster Alchemy Merger, 2331 Bushes Collision Remover Redux (build 100). Does not load on 1.9.8: 1205, 1991.

### E - UI text and localisation (4)

| # | Id | Mod | Area in the index | Overall | Effect | Build | 1.9.8 | What it changes | Build notes |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 1922 | No Prefixes in Alchemy Book | Alchemy / food / survival | 50 | 8 | 100 | yes | 378 text strings, no table row | ships its own text strings |
| 1 | 2362 | Better Perk Descriptions | Progression / XP / perks | 50 | 8 | 100 | yes | 26 text strings, no table row | ships its own text strings |
| 3 | 2098 | Medieval Poisons - spolszczenie | Alchemy / food / survival | 47 | 8 | 94 | legacy | 175 text strings, no table row | no mod.manifest: legacy loose pak; ships its own text strings |
| 4 | 2040 | Polymorphic Projectiles Arrow Overhaul | Archery / arrows | 37 | 8 | 72 | no | 11 text strings, no table row | the manifest does not allow 1.9.8; ships its own text strings; ships a readme |

**No pick on effect:** this method cannot measure what these change, so the order is how well the archive is made only. Best made: 1922 No Prefixes in Alchemy Book, 2362 Better Perk Descriptions (build 100). Does not load on 1.9.8: 2040.

## E non-perceptive to gameplay (no effective change found) (10 mods)

### E - Non-table XML (entities, effects, audio definitions) (7)

| # | Id | Mod | Area in the index | Overall | Effect | Build | 1.9.8 | What it changes | Build notes |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 1743 | Persistent Arrows | Archery / arrows | 45 | 0 | 100 | yes | XML that is not a game table, no table row | nothing against it |
| 1 | 2066 | Distant Smoke and Fire | World / weather / visuals | 45 | 0 | 100 | yes | XML that is not a game table, no table row | nothing against it |
| 1 | 2280 | Remove Artemisia (Wormwood) Potion Visual Effe | Alchemy / food / survival | 45 | 0 | 100 | yes | XML that is not a game table, no table row | nothing against it |
| 1 | 2332 | Baptism of Fire Fix Redux | Quests / lore / content | 45 | 0 | 100 | yes | XML that is not a game table, no table row | ships a readme |
| 1 | 2381 | Nest of Vipers Stealth | Crime / stealth / loot | 45 | 0 | 100 | yes | XML that is not a game table, no table row | ships a readme |
| 6 | 84 | Archery - Realistic Arrow Flight | Archery / arrows | 40 | 0 | 90 | legacy | XML that is not a game table, no table row | no mod.manifest: legacy loose pak |
| 6 | 1951 | Baths dont affect energy and nourishment | Alchemy / food / survival | 40 | 0 | 90 | legacy | XML that is not a game table, no table row | no mod.manifest: legacy loose pak |

**No pick on effect:** this method cannot measure what these change, so the order is how well the archive is made only. Best made: 1743 Persistent Arrows, 2066 Distant Smoke and Fire, 2280 Remove Artemisia (Wormwood) Potion Visual Effect Overlay, 2332 Baptism of Fire Fix Redux, 2381 Nest of Vipers Stealth (build 100).

### E - Nothing readable / no change found (3)

| # | Id | Mod | Area in the index | Overall | Effect | Build | 1.9.8 | What it changes | Build notes |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 1996 | Alcohol Is Not Food Anymore | Alchemy / food / survival | 46 | 2 | 100 | yes | has table files, but no row differs from vanilla | every table file is a correctly suffixed PTF patch |
| 2 | 1652 | Catches the Worm | Alchemy / food / survival | 45 | 0 | 100 | yes | has table files, but no row differs from vanilla | nothing against it |
| 2 | 1673 | Combat musics tweak | Combat / AI | 45 | 0 | 100 | yes | nothing found that changes a row | 2 archives: optional variants |

**Nothing to pick:** no mod here was found to change a single game row, so there is nothing to rank. Read their own pages before keeping any of them.

## The same sub-categories across the grades

Which grades a sub-category appears in, best-ranked mod of each grade first.

| Sub-category | Mods | By grade | Top of each grade |
|---|---|---|---|
| Alchemy, food and survival | 17 | Ax2 Bx4 Cx11 | A: 2210 True Hardcore Alchemy (PTF); B: 1483 TSM Slower Food Spoil; C: 1660 Double Brew Yield |
| Archery: bows, arrows, aiming | 9 | Cx9 | C: 1565 Karnages_Arrow_Balance 2.0 |
| Combat mechanics and AI | 11 | Ax4 Bx3 Cx4 | A: 1148 Combo and Weapon rebalance; B: 2179 True Hardcore Combat (PTF); C: 1236 Easy Combat PTF (easy parry and ma |
| Crime, stealth and reputation | 1 | Cx1 | C: 1883 Better Pickpocket - FIXED |
| Economy, loot and item stats | 16 | Ax3 Bx5 Cx7 Dx1 | A: 2219 True Hardcore Crime (PTF); B: 1062 SIM Camping Mini ML 1.5.1.1; C: 1864 Cheap Savior Schnapps - PTF; D: 1693 Ravens beak and Spiked warhammer i |
| Engine config (.cfg) only | 2 | Dx2 | D: 83 More Responsive Targeting |
| Lua scripts only | 11 | Bx2 Dx9 | B: 2318 Visual Combo Helper; D: 1520 Shooting Archery Targets Gives XP |
| Multi-system overhaul | 5 | Ax4 Bx1 | A: 2299 1403 - Historical Rebalance; B: 1558 Karnages_KCD_Essential_Fixes 2.0 |
| NPC perks, skills and archetypes | 1 | Ax1 | A: 1629 Exclusive Master Strikes - Make Th |
| NPCs, quests and world content | 5 | Bx2 Cx2 Dx1 | B: 2343 Ultimate Horse Caparison Fix; C: 1950 Skill Books Take Time; D: 1671 Angriness Begone |
| Native code and external tools | 4 | Ax4 | A: 2326 Permanent Death |
| Non-table XML (entities, effects, audio definitions) | 7 | Ex7 | E: 1743 Persistent Arrows |
| Nothing readable / no change found | 3 | Ex3 | E: 1996 Alcohol Is Not Food Anymore |
| Perks, skills and XP | 16 | Ax2 Bx3 Cx10 Dx1 | A: 2338 Horse Collision Mod; B: 1009 Perkaholic - PTF updated (1.9.4-1.; C: 1572 Increased Experience Gains; D: 1569 Karnages_Shield_Restoration |
| Textures, models and other assets | 9 | Ex9 | E: 366 First-person Herb Picking |
| UI text and localisation | 4 | Ex4 | E: 1922 No Prefixes in Alchemy Book |
| Weapons, armour and durability | 8 | Ax2 Bx1 Cx5 | A: 1560 Karnages_Durability_Redux; B: 2173 True Hardcore Maintenance (PTF); C: 1559 Karnages_Weapons_Damage_Balance 2. |
