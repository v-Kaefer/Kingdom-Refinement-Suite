# Where the graded mods intersect (generated)

> **GENERATED** by `tools/mod_intersections.py`: do not edit | **Kind:** review | **Trust:** derived from the read-only analysis (`mod_overlap.csv`, `mod_tables.csv`, `mod_subcategories.csv`; no archive was opened for this file) | **Game version:** 1.9.8

Read on 2026-10-04: the mods graded A to E of [`MOD_SUBCATEGORIES.md`](MOD_SUBCATEGORIES.md). **89 of them write table rows**, and of those **1384 pairs intersect**: 442 pairs write at least one of the same rows, 942 more write into the same table without sharing a row, and 296 of the pairs include a mod that replaces one of those tables whole. Every pair is in `mod_intersections.csv`; the contested rows themselves are in `mod_overlap.csv`.

## What an intersection costs

From the measured rules in [`../engine/ptf-rules.md`](../engine/ptf-rules.md):

| Kind | What the game does | Consequence |
|---|---|---|
| **Same row** | rule 6: a row is replaced whole and the **last mod in `mod_order.txt` wins** | only one of the two mods takes effect on that row; the other's values are undone, silently |
| **Same table, no shared row** | both patches are applied to different rows | they coexist; the risk is only that a later whole-table replacement of that table wipes both |
| **Whole-table replacement** | a file without the `__<modid>` suffix replaces the vanilla table | it overrides **every** patch of **every** other mod on that table, whatever the rows, and also undoes the game's own 1.9.7/1.9.8 changes to it |

Rule 5 makes a shared row worse than it looks: a row that lists only some columns blanks the others, so the mod that wins a contested row can zero columns the other mod never touched.

## The hardest conflicts: most shared rows

| Mod A | Mod B | Shared rows | Where | Kind |
|---|---|---|---|---|
| A 2124 Half-looted Rebalance | A 2299 1403 - Historical Rebalance | 2766 | armor 712, shop_type2item 606, pickable_item 585, combat_action_sync_attack 277, ... | same rows + whole-table replacement |
| A 2299 1403 - Historical Rebalance | A 2340 MatthusTweaks - Equipment and Prog | 1565 | pickable_item 992, armor 298, shop 126, melee_weapon 73, weapon 69, rpg_param 2 | same rows |
| A 883 KingdomCome Rebalancing | A 2299 1403 - Historical Rebalance | 1038 | pickable_item 539, armor 208, shop 154, weapon 76, melee_weapon 46, perk 7 | same rows + whole-table replacement |
| A 1560 Karnages_Durability_Redux | A 2299 1403 - Historical Rebalance | 960 | armor 771, weapon 189 | same rows |
| A 2124 Half-looted Rebalance | A 2340 MatthusTweaks - Equipment and Prog | 846 | pickable_item 357, armor 283, melee_weapon 72, weapon 68, shop 61, rpg_param 3 | same rows + whole-table replacement |
| A 883 KingdomCome Rebalancing | A 2340 MatthusTweaks - Equipment and Prog | 841 | pickable_item 395, armor 202, shop 132, weapon 66, melee_weapon 45, rpg_param 1 | same rows + whole-table replacement |
| A 1560 Karnages_Durability_Redux | A 2124 Half-looted Rebalance | 838 | armor 695, weapon 143 | same rows |
| A 883 KingdomCome Rebalancing | A 2124 Half-looted Rebalance | 777 | pickable_item 359, armor 198, weapon 75, shop 63, melee_weapon 46, equippable_item 19 | same rows + whole-table replacement |
| A 2049 Simple Ragdoll Physics | A 2299 1403 - Historical Rebalance | 412 | combat_action_sync_attack 263, combat_action_attack 100, pickable_item 16, ammo 14, ... | same rows |
| A 2049 Simple Ragdoll Physics | A 2124 Half-looted Rebalance | 347 | combat_action_sync_attack 245, combat_action_attack 76, ammo 12, pickable_item 6, ... | same rows |
| A 1560 Karnages_Durability_Redux | A 2340 MatthusTweaks - Equipment and Prog | 347 | armor 278, weapon 69 | same rows |
| A 883 KingdomCome Rebalancing | A 1560 Karnages_Durability_Redux | 284 | armor 208, weapon 76 | same rows + whole-table replacement |
| A 651 Better Combat and Immersion Compil | A 2124 Half-looted Rebalance | 202 | combat_action_perfect_block 88, food 24, rpg_param 21, armor 17, equippable_item 15, ... | same rows + whole-table replacement |
| B 85 Perkaholic | B 1009 Perkaholic - PTF updated (1.9.4-1. | 192 | buff 59, perk 57, perk_buff 55, perk_buff_override 17, perk2perk_exclusivity 3, skill 1 | same rows + whole-table replacement |
| B 85 Perkaholic | B 770 Perkaholic updated | 186 | buff 57, perk 57, perk_buff 55, perk_buff_override 17 | same rows + whole-table replacement |
| B 770 Perkaholic updated | B 1009 Perkaholic - PTF updated (1.9.4-1. | 186 | buff 57, perk 57, perk_buff 55, perk_buff_override 17 | same rows + whole-table replacement |
| B 2011 Chefs Kiss | A 2299 1403 - Historical Rebalance | 180 | food 149, pickable_item 31 | same rows |
| B 1384 Modified Combat Overhaul - Directi | A 2124 Half-looted Rebalance | 165 | combat_action_perfect_block 148, rpg_param 13, perk_rpg_param_override 4 | same rows |
| A 2188 True Hardcore Economy (PTF) | A 2299 1403 - Historical Rebalance | 159 | shop 80, pickable_item 59, buff 8, sequence 4, food 3, rpg_param 2 | same rows |
| B 2011 Chefs Kiss | A 2124 Half-looted Rebalance | 150 | food 145, pickable_item 5 | same rows |
| A 2124 Half-looted Rebalance | B 2345 Food and Drinks rebalance | 145 | food 145 | same rows + whole-table replacement |
| A 2299 1403 - Historical Rebalance | B 2345 Food and Drinks rebalance | 144 | food 144 | same rows + whole-table replacement |
| B 2011 Chefs Kiss | B 2345 Food and Drinks rebalance | 143 | food 143 | same rows + whole-table replacement |
| B 1112 Combat Overhaul | B 1384 Modified Combat Overhaul - Directi | 141 | combat_action_perfect_block 130, rpg_param 9, perk_rpg_param_override 2 | same rows |
| B 1112 Combat Overhaul | A 2124 Half-looted Rebalance | 140 | combat_action_perfect_block 130, rpg_param 8, perk_rpg_param_override 1, ... | same rows |
| ... | ... | ... | 417 more in `mod_intersections.csv` | |

## Whole-table replacement: one mod overrides the others

These mods ship at least one table file without the PTF suffix. On those tables nothing else survives, so every other mod listed here loses its patches to that table regardless of which rows it writes.

| Mod | Grade | Tables replaced | Other mods overridden | Which tables are contested |
|---|---|---|---|---|
| 883 KingdomCome Rebalancing | A | 398 | 87 | ammo, angriness_enum, anim_fragment, armor, armor2clothing_preset, armor_type, ... |
| 1260 RPG Tweaks | C | 2 | 40 | perk_rpg_param_override, rpg_param |
| 802 Archery for 1.9 | C | 1 | 38 | rpg_param |
| 804 Loose (An Archery Mod) | C | 1 | 38 | rpg_param |
| 1334 Fast Learning Henry | C | 1 | 38 | rpg_param |
| 85 Perkaholic | B | 6 | 28 | buff, perk, perk2perk_exclusivity, perk_buff, perk_buff_override, skill |
| 770 Perkaholic updated | B | 5 | 26 | buff, perk, perk2perk_exclusivity, perk_buff, perk_buff_override |
| 2345 Food and Drinks rebalance | B | 1 | 16 | food |
| 2124 Half-looted Rebalance | A | 3 | 15 | shop, shop_type2item, soul2perk |
| 480 Bed Comfort Restored | C | 1 | 2 | sleeping_spot_type |
| 1062 SIM Camping Mini ML 1.5.1.1 | B | 1 | 2 | sleeping_spot_type |
| 1424 Better Sleep Fixed | C | 1 | 2 | sleeping_spot_type |
| 1629 Exclusive Master Strikes - Make Th | A | 1 | 2 | soul2perk |
| 2299 1403 - Historical Rebalance | A | 1 | 0 | (none: only it writes them) |

## Intersections inside a sub-category

The mods that do the same job. A shared row here means the two are **alternatives, not an addition**: installing both leaves whichever loads last in charge of the contested rows.

### Economy, loot and item stats (89 pairs, 7 of them on the same rows)

| Mod A | Mod B | Shared rows | Where | Kind |
|---|---|---|---|---|
| A 2188 True Hardcore Economy (PTF) | A 2340 MatthusTweaks - Equipment and Prog | 133 | shop 75, pickable_item 56, rpg_param 1, perk_rpg_param_override 1 | same rows |
| C 1914 Weightless Herbs | A 2340 MatthusTweaks - Equipment and Prog | 15 | pickable_item 15 | same rows |
| A 2188 True Hardcore Economy (PTF) | A 2219 True Hardcore Crime (PTF) | 1 | buff 1 | same rows |
| C 1864 Cheap Savior Schnapps - PTF | A 2340 MatthusTweaks - Equipment and Prog | 1 | pickable_item 1 | same rows |
| C 1853 Richer Merchants (PTF) | C 2165 Merchants Richer | 1 | shop_type2item 1 | same rows |
| C 1853 Richer Merchants (PTF) | A 2188 True Hardcore Economy (PTF) | 1 | shop_type2item 1 | same rows |
| C 2165 Merchants Richer | A 2188 True Hardcore Economy (PTF) | 1 | shop_type2item 1 | same rows |
| B 1062 SIM Camping Mini ML 1.5.1.1 | A 2219 True Hardcore Crime (PTF) | - | buff, food, perk, perk_buff, pickable_item | same table only |
| B 1062 SIM Camping Mini ML 1.5.1.1 | C 1195 Get Water | - | item, pickable_item, player_item, questible_item | same table only |
| B 1062 SIM Camping Mini ML 1.5.1.1 | B 1380 Black Items Fix | - | item, pickable_item, player_item, shop_type2item | same table only |
| B 1062 SIM Camping Mini ML 1.5.1.1 | A 2188 True Hardcore Economy (PTF) | - | buff, food, pickable_item, shop_type2item | same table only |
| B 1062 SIM Camping Mini ML 1.5.1.1 | B 2209 Poisonous Enemies - True Hardcore  | - | buff, pickable_item, player_item, shop_type2item | same table only |
| ... | ... | ... | 77 more in `mod_intersections.csv` | |

### Perks, skills and XP (47 pairs, 12 of them on the same rows)

| Mod A | Mod B | Shared rows | Where | Kind |
|---|---|---|---|---|
| B 85 Perkaholic | B 1009 Perkaholic - PTF updated (1.9.4-1. | 192 | buff 59, perk 57, perk_buff 55, perk_buff_override 17, perk2perk_exclusivity 3, skill 1 | same rows + whole-table replacement |
| B 85 Perkaholic | B 770 Perkaholic updated | 186 | buff 57, perk 57, perk_buff 55, perk_buff_override 17 | same rows + whole-table replacement |
| B 770 Perkaholic updated | B 1009 Perkaholic - PTF updated (1.9.4-1. | 186 | buff 57, perk 57, perk_buff 55, perk_buff_override 17 | same rows + whole-table replacement |
| C 1334 Fast Learning Henry | C 1572 Increased Experience Gains | 36 | rpg_param 36 | same rows + whole-table replacement |
| C 1260 RPG Tweaks | C 1334 Fast Learning Henry | 33 | rpg_param 33 | same rows + whole-table replacement |
| C 1260 RPG Tweaks | C 1572 Increased Experience Gains | 28 | rpg_param 28 | same rows + whole-table replacement |
| C 1070 Better Combat | C 1260 RPG Tweaks | 12 | rpg_param 8, perk_rpg_param_override 4 | same rows + whole-table replacement |
| C 1292 Ultimate Repair Kit 2.0 | C 1842 Realistic Repairs | 4 | skill2item_category 2, rpg_param 1, perk_rpg_param_override 1 | same rows |
| C 1260 RPG Tweaks | C 1292 Ultimate Repair Kit 2.0 | 2 | rpg_param 1, perk_rpg_param_override 1 | same rows + whole-table replacement |
| C 1260 RPG Tweaks | C 1842 Realistic Repairs | 2 | rpg_param 1, perk_rpg_param_override 1 | same rows + whole-table replacement |
| B 85 Perkaholic | A 1736 Rogue Life | 1 | buff 1 | same rows + whole-table replacement |
| C 1260 RPG Tweaks | C 1863 Dirty And Charismatic - PTF | 1 | perk_rpg_param_override 1 | same rows + whole-table replacement |
| ... | ... | ... | 35 more in `mod_intersections.csv` | |

### Alchemy, food and survival (47 pairs, 25 of them on the same rows)

| Mod A | Mod B | Shared rows | Where | Kind |
|---|---|---|---|---|
| B 2011 Chefs Kiss | B 2345 Food and Drinks rebalance | 143 | food 143 | same rows + whole-table replacement |
| B 1483 TSM Slower Food Spoil | B 1639 Alternate Food Spoil (2X) | 111 | food 111 | same rows |
| B 1483 TSM Slower Food Spoil | B 2011 Chefs Kiss | 102 | food 102 | same rows |
| B 1483 TSM Slower Food Spoil | B 2345 Food and Drinks rebalance | 102 | food 102 | same rows + whole-table replacement |
| B 1639 Alternate Food Spoil (2X) | B 2011 Chefs Kiss | 102 | food 102 | same rows |
| B 1639 Alternate Food Spoil (2X) | B 2345 Food and Drinks rebalance | 102 | food 102 | same rows + whole-table replacement |
| B 2011 Chefs Kiss | A 2210 True Hardcore Alchemy (PTF) | 24 | food 23, pickable_item 1 | same rows |
| C 1926 Potion no Satiety and ADD Heal plu | B 2011 Chefs Kiss | 22 | food 22 | same rows |
| C 1926 Potion no Satiety and ADD Heal plu | A 2210 True Hardcore Alchemy (PTF) | 20 | food 20 | same rows |
| C 1926 Potion no Satiety and ADD Heal plu | B 2345 Food and Drinks rebalance | 19 | food 19 | same rows + whole-table replacement |
| A 2210 True Hardcore Alchemy (PTF) | B 2345 Food and Drinks rebalance | 19 | food 19 | same rows + whole-table replacement |
| A 2208 Medieval Poisons - True Hardcore C | A 2210 True Hardcore Alchemy (PTF) | 14 | buff 9, food 4, rpg_param 1 | same rows |
| ... | ... | ... | 35 more in `mod_intersections.csv` | |

### Combat mechanics and AI (35 pairs, 28 of them on the same rows)

| Mod A | Mod B | Shared rows | Where | Kind |
|---|---|---|---|---|
| B 1112 Combat Overhaul | B 1384 Modified Combat Overhaul - Directi | 141 | combat_action_perfect_block 130, rpg_param 9, perk_rpg_param_override 2 | same rows |
| A 2049 Simple Ragdoll Physics | A 2294 Faster Combat - Directional Master | 66 | combat_action_attack 66 | same rows |
| B 1112 Combat Overhaul | B 2179 True Hardcore Combat (PTF) | 31 | rpg_param 29, perk_rpg_param_override 2 | same rows |
| B 1384 Modified Combat Overhaul - Directi | B 2179 True Hardcore Combat (PTF) | 29 | rpg_param 17, buff 7, perk_rpg_param_override 5 | same rows |
| A 2049 Simple Ragdoll Physics | B 2179 True Hardcore Combat (PTF) | 27 | ammo 14, pickable_item 13 | same rows |
| B 2179 True Hardcore Combat (PTF) | A 2294 Faster Combat - Directional Master | 11 | rpg_param 10, perk_rpg_param_override 1 | same rows |
| C 1668 Relaxed RPG Params | B 2179 True Hardcore Combat (PTF) | 9 | rpg_param 9 | same rows |
| B 1384 Modified Combat Overhaul - Directi | A 2294 Faster Combat - Directional Master | 7 | rpg_param 6, perk_rpg_param_override 1 | same rows |
| C 1243 Easier Enemies PTF (Dumber Enemies | B 2179 True Hardcore Combat (PTF) | 7 | rpg_param 7 | same rows |
| A 1563 Karnages_Polearm_Restoration 2.0 | A 2294 Faster Combat - Directional Master | 6 | combat_action_attack 6 | same rows |
| B 1112 Combat Overhaul | A 2294 Faster Combat - Directional Master | 6 | rpg_param 6 | same rows |
| C 1243 Easier Enemies PTF (Dumber Enemies | B 1384 Modified Combat Overhaul - Directi | 6 | rpg_param 6 | same rows |
| ... | ... | ... | 23 more in `mod_intersections.csv` | |

### Archery: bows, arrows, aiming (21 pairs, 21 of them on the same rows)

| Mod A | Mod B | Shared rows | Where | Kind |
|---|---|---|---|---|
| C 1419 Immersive Archery | C 1678 Better Archery | 20 | ammo 14, rpg_param 6 | same rows |
| C 1376 Archery mod - Faster arrows (for r | C 1419 Immersive Archery | 14 | ammo 14 | same rows |
| C 1376 Archery mod - Faster arrows (for r | C 1678 Better Archery | 14 | ammo 14 | same rows |
| C 1376 Archery mod - Faster arrows (for r | C 1565 Karnages_Arrow_Balance 2.0 | 12 | ammo 12 | same rows |
| C 1419 Immersive Archery | C 1565 Karnages_Arrow_Balance 2.0 | 12 | ammo 12 | same rows |
| C 1565 Karnages_Arrow_Balance 2.0 | C 1678 Better Archery | 12 | ammo 12 | same rows |
| C 804 Loose (An Archery Mod) | C 1564 Karnages_Rebalanced_Bows 2.0 | 11 | rpg_param 11 | same rows + whole-table replacement |
| C 802 Archery for 1.9 | C 804 Loose (An Archery Mod) | 10 | rpg_param 10 | same rows + whole-table replacement |
| C 802 Archery for 1.9 | C 1564 Karnages_Rebalanced_Bows 2.0 | 10 | rpg_param 10 | same rows + whole-table replacement |
| C 804 Loose (An Archery Mod) | C 1678 Better Archery | 7 | rpg_param 7 | same rows + whole-table replacement |
| C 1564 Karnages_Rebalanced_Bows 2.0 | C 1678 Better Archery | 7 | rpg_param 7 | same rows |
| C 802 Archery for 1.9 | C 1419 Immersive Archery | 6 | rpg_param 6 | same rows + whole-table replacement |
| ... | ... | ... | 9 more in `mod_intersections.csv` | |

### Weapons, armour and durability (11 pairs, 2 of them on the same rows)

| Mod A | Mod B | Shared rows | Where | Kind |
|---|---|---|---|---|
| C 1545 Saddles Have Durability | B 2173 True Hardcore Maintenance (PTF) | 20 | armor 20 | same rows |
| A 1560 Karnages_Durability_Redux | C 1893 Bianca's Ring PTF | 1 | armor 1 | same rows |
| A 1839 Realistic Horses | B 2173 True Hardcore Maintenance (PTF) | - | buff, rpg_param | same table only |
| C 1425 Saving Soles (PTF) | A 1839 Realistic Horses | - | rpg_param | same table only |
| C 1425 Saving Soles (PTF) | B 2173 True Hardcore Maintenance (PTF) | - | rpg_param | same table only |
| C 1545 Saddles Have Durability | A 1560 Karnages_Durability_Redux | - | armor | same table only |
| C 1545 Saddles Have Durability | C 1893 Bianca's Ring PTF | - | armor | same table only |
| A 1560 Karnages_Durability_Redux | B 2173 True Hardcore Maintenance (PTF) | - | armor | same table only |
| C 1782 No more clipping elbows for Andrew | A 1839 Realistic Horses | - | soul | same table only |
| A 1839 Realistic Horses | C 1893 Bianca's Ring PTF | - | equippable_item | same table only |
| C 1893 Bianca's Ring PTF | B 2173 True Hardcore Maintenance (PTF) | - | armor | same table only |

### Multi-system overhaul (10 pairs, 10 of them on the same rows)

| Mod A | Mod B | Shared rows | Where | Kind |
|---|---|---|---|---|
| A 2124 Half-looted Rebalance | A 2299 1403 - Historical Rebalance | 2766 | armor 712, shop_type2item 606, pickable_item 585, combat_action_sync_attack 277, ... | same rows + whole-table replacement |
| A 883 KingdomCome Rebalancing | A 2299 1403 - Historical Rebalance | 1038 | pickable_item 539, armor 208, shop 154, weapon 76, melee_weapon 46, perk 7 | same rows + whole-table replacement |
| A 883 KingdomCome Rebalancing | A 2124 Half-looted Rebalance | 777 | pickable_item 359, armor 198, weapon 75, shop 63, melee_weapon 46, equippable_item 19 | same rows + whole-table replacement |
| A 651 Better Combat and Immersion Compil | A 2124 Half-looted Rebalance | 202 | combat_action_perfect_block 88, food 24, rpg_param 21, armor 17, equippable_item 15, ... | same rows + whole-table replacement |
| A 651 Better Combat and Immersion Compil | A 2299 1403 - Historical Rebalance | 94 | buff 37, food 26, armor 17, rpg_param 11, perk_rpg_param_override 2, pickable_item 1 | same rows |
| A 651 Better Combat and Immersion Compil | A 883 KingdomCome Rebalancing | 35 | equippable_item 14, inventory_preset2item 8, rpg_param 5, buff 4, armor 2, ... | same rows + whole-table replacement |
| B 1558 Karnages_KCD_Essential_Fixes 2.0 | A 2299 1403 - Historical Rebalance | 26 | rpg_param 24, perk_rpg_param_override 2 | same rows |
| B 1558 Karnages_KCD_Essential_Fixes 2.0 | A 2124 Half-looted Rebalance | 24 | rpg_param 18, perk_rpg_param_override 6 | same rows |
| A 651 Better Combat and Immersion Compil | B 1558 Karnages_KCD_Essential_Fixes 2.0 | 21 | rpg_param 15, perk_rpg_param_override 6 | same rows |
| A 883 KingdomCome Rebalancing | B 1558 Karnages_KCD_Essential_Fixes 2.0 | 7 | rpg_param 7 | same rows + whole-table replacement |

### NPCs, quests and world content (1 pair, 0 of them on the same rows)

| Mod A | Mod B | Shared rows | Where | Kind |
|---|---|---|---|---|
| C 1990 Veteran Hunting | B 2343 Ultimate Horse Caparison Fix | - | soul | same table only |

## Intersections across sub-categories

337 pairs write the same rows while sitting in different sub-categories: the mod is not a rival, it just reaches into the same table. These are the ones easy to miss when picking one mod per sub-category.

| Mod A | Mod B | Shared rows | Where | Kind |
|---|---|---|---|---|
| A 2299 1403 - Historical Rebalance | A 2340 MatthusTweaks - Equipment and Prog | 1565 | pickable_item 992, armor 298, shop 126, melee_weapon 73, weapon 69, rpg_param 2 | same rows |
| A 1560 Karnages_Durability_Redux | A 2299 1403 - Historical Rebalance | 960 | armor 771, weapon 189 | same rows |
| A 2124 Half-looted Rebalance | A 2340 MatthusTweaks - Equipment and Prog | 846 | pickable_item 357, armor 283, melee_weapon 72, weapon 68, shop 61, rpg_param 3 | same rows + whole-table replacement |
| A 883 KingdomCome Rebalancing | A 2340 MatthusTweaks - Equipment and Prog | 841 | pickable_item 395, armor 202, shop 132, weapon 66, melee_weapon 45, rpg_param 1 | same rows + whole-table replacement |
| A 1560 Karnages_Durability_Redux | A 2124 Half-looted Rebalance | 838 | armor 695, weapon 143 | same rows |
| A 2049 Simple Ragdoll Physics | A 2299 1403 - Historical Rebalance | 412 | combat_action_sync_attack 263, combat_action_attack 100, pickable_item 16, ammo 14, ... | same rows |
| A 2049 Simple Ragdoll Physics | A 2124 Half-looted Rebalance | 347 | combat_action_sync_attack 245, combat_action_attack 76, ammo 12, pickable_item 6, ... | same rows |
| A 1560 Karnages_Durability_Redux | A 2340 MatthusTweaks - Equipment and Prog | 347 | armor 278, weapon 69 | same rows |
| A 883 KingdomCome Rebalancing | A 1560 Karnages_Durability_Redux | 284 | armor 208, weapon 76 | same rows + whole-table replacement |
| B 2011 Chefs Kiss | A 2299 1403 - Historical Rebalance | 180 | food 149, pickable_item 31 | same rows |
| B 1384 Modified Combat Overhaul - Directi | A 2124 Half-looted Rebalance | 165 | combat_action_perfect_block 148, rpg_param 13, perk_rpg_param_override 4 | same rows |
| A 2188 True Hardcore Economy (PTF) | A 2299 1403 - Historical Rebalance | 159 | shop 80, pickable_item 59, buff 8, sequence 4, food 3, rpg_param 2 | same rows |
| B 2011 Chefs Kiss | A 2124 Half-looted Rebalance | 150 | food 145, pickable_item 5 | same rows |
| A 2124 Half-looted Rebalance | B 2345 Food and Drinks rebalance | 145 | food 145 | same rows + whole-table replacement |
| A 2299 1403 - Historical Rebalance | B 2345 Food and Drinks rebalance | 144 | food 144 | same rows + whole-table replacement |
| B 1112 Combat Overhaul | A 2124 Half-looted Rebalance | 140 | combat_action_perfect_block 130, rpg_param 8, perk_rpg_param_override 1, ... | same rows |
| A 651 Better Combat and Immersion Compil | B 1384 Modified Combat Overhaul - Directi | 117 | combat_action_perfect_block 88, rpg_param 16, buff 8, perk_rpg_param_override 5 | same rows |
| B 1483 TSM Slower Food Spoil | A 2299 1403 - Historical Rebalance | 102 | food 102 | same rows |
| B 1639 Alternate Food Spoil (2X) | A 2299 1403 - Historical Rebalance | 102 | food 102 | same rows |
| B 1483 TSM Slower Food Spoil | A 2124 Half-looted Rebalance | 98 | food 98 | same rows |
| B 1639 Alternate Food Spoil (2X) | A 2124 Half-looted Rebalance | 98 | food 98 | same rows |
| A 2294 Faster Combat - Directional Master | A 2299 1403 - Historical Rebalance | 87 | combat_action_attack 66, combat_action_sync_attack 17, rpg_param 3, ... | same rows |
| A 883 KingdomCome Rebalancing | A 2188 True Hardcore Economy (PTF) | 85 | shop 81, rpg_param 3, perk_rpg_param_override 1 | same rows + whole-table replacement |
| A 651 Better Combat and Immersion Compil | B 1112 Combat Overhaul | 82 | combat_action_perfect_block 70, rpg_param 10, perk_rpg_param_override 2 | same rows |
| A 1148 Combo and Weapon rebalance | C 1559 Karnages_Weapons_Damage_Balance 2. | 77 | melee_weapon 77 | same rows |
| ... | ... | ... | 312 more in `mod_intersections.csv` | |

## The most contested tables and rows

| Table | Rows that two or more mods change |
|---|---|
| pickable_item | 1282 |
| armor | 796 |
| shop_type2item | 623 |
| combat_action_sync_attack | 295 |
| weapon | 190 |
| buff | 184 |
| food | 181 |
| shop | 163 |
| rpg_param | 159 |
| combat_action_perfect_block | 153 |
| combat_action_attack | 106 |
| melee_weapon | 100 |
| perk | 82 |
| perk_buff | 55 |
| recipe | 33 |

| Table | Row | Mods | Ids |
|---|---|---|---|
| rpg_param | CombatAutoSPBWeight | 12 | 284 651 1070 1243 1260 1384 1558 1668 2124 2179 2294 2299 |
| rpg_param | CombatAutoMaxAttackDelay | 11 | 651 1070 1112 1243 1260 1384 1558 1668 2179 2294 2299 |
| rpg_param | CombatAutoAttackDelayIncreasePerAttacker | 10 | 651 883 1070 1243 1260 1558 1668 2124 2179 2299 |
| rpg_param | CombatAutoNormalBWeight | 10 | 651 1070 1112 1243 1260 1384 1558 2124 2179 2299 |
| rpg_param | CombatAutoPBWeight | 10 | 651 1070 1112 1243 1260 1384 1558 2124 2179 2299 |
| rpg_param | MaxPerfectBlockSlotModifier | 10 | 651 1070 1112 1236 1260 1558 1668 2124 2179 2299 |
| rpg_param | MaxSpecialPerfectBlockSlotModifier | 10 | 651 1070 1236 1260 1558 1668 2124 2179 2294 2299 |
| ammo | 13ba7468-11a2-483d-8cb9-25ce36a2d228 | 9 | 1376 1419 1565 1678 2035 2049 2124 2179 2299 |
| ammo | 19df1c5c-3dbf-45c0-ac01-336facf5f741 | 9 | 1376 1419 1565 1678 2035 2049 2124 2179 2299 |
| ammo | 4fd563e5-a44a-4a6e-958d-95bcb196814a | 9 | 1376 1419 1565 1678 2035 2049 2124 2179 2299 |
| ammo | 710e3706-8974-404b-b23a-6f51670ef1ed | 9 | 1376 1419 1565 1678 2035 2049 2124 2179 2299 |
| ammo | 802507e9-d620-47b5-ae66-08fcc314e26a | 9 | 1376 1419 1565 1678 2035 2049 2124 2179 2299 |
| ammo | a5b31bbc-1e11-4831-835b-c06d5b13a7da | 9 | 1376 1419 1565 1678 2035 2049 2124 2179 2299 |
| ammo | c49aa63a-07a6-4417-9f9b-97f2712a4cd0 | 9 | 1376 1419 1565 1678 2035 2049 2124 2179 2299 |
| ammo | d5e6764d-18ba-44cb-8dd0-6640a17785a8 | 9 | 1376 1419 1565 1678 2035 2049 2124 2179 2299 |
| ammo | dfea5d01-b25c-414a-9ab4-6911a5f82118 | 9 | 1376 1419 1565 1678 2035 2049 2124 2179 2299 |
| ammo | e5b3f681-3714-4623-97be-4015fa454797 | 9 | 1376 1419 1565 1678 2035 2049 2124 2179 2299 |
| perk_rpg_param_override | 01c3b32a-5751-4c98-b6ab-258d02370382/MaxPerf | 9 | 651 1070 1112 1260 1384 1558 2124 2179 2299 |
| perk_rpg_param_override | 01c3b32a-5751-4c98-b6ab-258d02370382/MaxSpec | 9 | 651 1070 1260 1384 1558 2124 2179 2294 2299 |
| rpg_param | AimStamCost | 9 | 802 804 1260 1334 1419 1558 1564 1678 2124 |

## Intersections with the KRS modules

25 mods write rows that `modules/krs_items`, `krs_perks` or `krs_qol` also write (55 rows in total). By rule 6 the load order decides, so each of these is a decision for the suite: keep the KRS row, drop it, or ship the mod's value. Source: the *Same rows as KRS* lines of [`MOD_PROFILES.md`](MOD_PROFILES.md); the suite's own claims are in `../data/ownership.csv`.

| Mod | Grade | KRS module | Rows both write |
|---|---|---|---|
| 480 Bed Comfort Restored | C | krs_items | sleeping_spot_type:0; sleeping_spot_type:1; sleeping_spot_type:2; sleeping_spot_type:3 |
| 651 Better Combat and Immersion Compil | A | krs_items | food:73ff1fde-ec8b-41e9-95e3-b5938c715bf1; rpg_param:DigestionSpeed |
| 651 Better Combat and Immersion Compil | A | krs_qol | rpg_param:StrengthToInventoryCapacity |
| 883 KingdomCome Rebalancing | A | krs_qol | rpg_param:RepairPriceModif; rpg_param:StrengthToInventoryCapacity |
| 1260 RPG Tweaks | C | krs_items | rpg_param:ReadingXpPerHour |
| 1260 RPG Tweaks | C | krs_qol | rpg_param:HerbGatherSkillToRadius |
| 1292 Ultimate Repair Kit 2.0 | C | krs_qol | skill2item_category:armor.horse_bridle.*/8; skill2item_category:armor.horse_saddle.*/8 |
| 1334 Fast Learning Henry | C | krs_items | rpg_param:ReadingXpPerHour |
| 1424 Better Sleep Fixed | C | krs_items | sleeping_spot_type:0; sleeping_spot_type:1; sleeping_spot_type:2; sleeping_spot_type:3 |
| 1426 Energy and Hunger Patch for Timesc | C | krs_items | rpg_param:DigestionSpeed |
| 1558 Karnages_KCD_Essential_Fixes 2.0 | B | krs_items | rpg_param:ReadingXpPerHour |
| 1558 Karnages_KCD_Essential_Fixes 2.0 | B | krs_qol | rpg_param:HerbGatherSkillToRadius |
| 1572 Increased Experience Gains | C | krs_items | rpg_param:ReadingXpPerHour |
| 1765 Restore Riposte | C | krs_perks | perk:61e98757-9b32-493b-ad09-0087afdb81be; perk:ec4c5274-50e3-4bbf-9220-823b080647c4 |
| 1839 Realistic Horses | A | krs_qol | rpg_param:StrengthToInventoryCapacity |
| 1842 Realistic Repairs | C | krs_qol | perk_rpg_param_override:01c3b32a-5751-4c98-b6ab-258d02370382/RepairPriceModif; rpg_param:RepairPriceModif; ... |
| 1860 Train More Carry More - PTF | C | krs_qol | rpg_param:StrengthToInventoryCapacity |
| 1926 Potion no Satiety and ADD Heal plu | C | krs_items | food:73ff1fde-ec8b-41e9-95e3-b5938c715bf1 |
| 1938 My Herb Picking Radius | C | krs_qol | rpg_param:HerbGatherSkillToRadius |
| 1950 Skill Books Take Time | C | krs_items | document:0a9b5b2a-2614-4f11-a987-aab64133bea0; document:0defd37d-cfec-446f-b307-e9ef65fea3f3; ... **(the source list is cut at 300 characters: there are more)** |
| 2011 Chefs Kiss | B | krs_items | food:73ff1fde-ec8b-41e9-95e3-b5938c715bf1 |
| 2124 Half-looted Rebalance | A | krs_items | food:73ff1fde-ec8b-41e9-95e3-b5938c715bf1; rpg_param:DigestionSpeed |
| 2173 True Hardcore Maintenance (PTF) | B | krs_qol | perk_rpg_param_override:01c3b32a-5751-4c98-b6ab-258d02370382/RepairPriceModif; rpg_param:RepairPriceModif; ... |
| 2188 True Hardcore Economy (PTF) | A | krs_qol | perk_rpg_param_override:01c3b32a-5751-4c98-b6ab-258d02370382/RepairPriceModif; rpg_param:RepairPriceModif |
| 2210 True Hardcore Alchemy (PTF) | A | krs_items | food:73ff1fde-ec8b-41e9-95e3-b5938c715bf1 |
| 2210 True Hardcore Alchemy (PTF) | A | krs_qol | rpg_param:HerbGatherSkillToRadius |
| 2299 1403 - Historical Rebalance | A | krs_items | food:73ff1fde-ec8b-41e9-95e3-b5938c715bf1 |
| 2299 1403 - Historical Rebalance | A | krs_qol | rpg_param:HerbGatherSkillToRadius |
| 2340 MatthusTweaks - Equipment and Prog | A | krs_qol | perk_rpg_param_override:01c3b32a-5751-4c98-b6ab-258d02370382/RepairPriceModif; rpg_param:RepairPriceModif; ... |
| 2345 Food and Drinks rebalance | B | krs_items | food:73ff1fde-ec8b-41e9-95e3-b5938c715bf1 |

## What intersects with nothing

**1 mod writes table rows that no other mod in this set touches**, and no mod replaces a table they use: 1671. Those can be added without a row decision.

**40 mods change no table row** (Lua, engine config, non-table XML, assets, text, or a patch whose every row is identical to vanilla), so this method cannot compare them with anything: 83, 84, 366, 591, 1040, 1090, 1205, 1323, 1518, 1519, 1520, 1612, 1647, 1652, 1655, 1673, 1743, 1922, 1951, 1991, 1996, 2040, 2066, 2098, 2192, 2194, 2207, 2246, 2276, 2280, 2318, 2323, 2326, 2331, 2332, 2348, 2359, 2362, 2372, 2381. Two Lua mods that hook the same event, or two archives that ship the same texture path, would intersect in the game and are not visible here.

## Limits

- Only table rows are compared. The analysis CSVs count Lua lines, config keys and asset files but do not list their names, so Lua, `.cfg`, UI and asset collisions cannot be derived; re-reading the archives would be needed for that.
- `mod_overlap.csv` holds, by design, only the rows that two or more mods change, which is exactly the intersection set; a row only one mod writes cannot appear and is not missing.
- The four native mods (2246, 2326, 2348, 2359) change rpg params at runtime, not in a table, so an intersection with them cannot be read from files at all.
- Intersections are counted per mod id across all its archives, so a mod whose options are alternatives (1243, 1483, 2294) shows the union of its options.
- Whether an intersection hurts depends on load order, which is a local `mod_order.txt` and not part of this data.
