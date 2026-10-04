# Mod triage (generated)

> **GENERATED** by `tools/triage_mods.py`: do not edit | **Kind:** review | **Trust:** rules applied to titles, search summaries and 26 archives read locally | **Game version:** 1.9.8

365 mods. Rules and evidence classes are in the header of `tools/triage_mods.py`; the per-mod table is `mods_triage.csv`. This is a repeatable sort, not a verdict: only the rows marked evidence **A** (archive read) are measured.

## Counts

| Priority | Mods | Meaning |
|---|---|---|
| P1 | 3 | act now |
| P2 | 129 | compare or check before combining |
| P3 | 181 | optional or not mapped |
| P4 | 52 | outside the suite's scope |

| Evidence | Mods |
|---|---|
| A archive | 18 |
| N Nexus API | 347 |

## Actions

| Priority | Action | Mods |
|---|---|---|
| P1 | Replace the published release | 1 |
| P1 | Resolve the measured row collision | 2 |
| P2 | Check on 1.9.8 whether the fix is still needed | 10 |
| P2 | Compare tables | 93 |
| P2 | Disabled on 1.9.8 by its manifest: edit the version line | 1 |
| P2 | Study the rows and compare | 25 |
| P3 | Classify by hand | 3 |
| P3 | Optional companion: outside the PTF scope, check version support | 101 |
| P3 | Review: gameplay mod not mapped to a KRS module | 77 |
| P4 | Optional visual: no table overlap expected | 46 |
| P4 | Out of scope | 4 |
| P4 | Removed or hidden on Nexus: drop it or find a replacement | 2 |

## P1 and the archive-measured mods

| Id | Mod | Finding |
|---|---|---|
| 1639 | Alternate Food Spoil (2X) | AlternateFoodSpoil2X-1639-1-0-1715: yes (no version restriction) | id 'alternatefoodspoil2x' has characters other than lowercase letters and underscore (the engine warns; patche | collides krs_items:food:73ff1fde-ec8b-41e9-95e3-b5938c715bf1 |
| 1765 | Restore Riposte | Riposte-1765-1-0-2-1735871267.zip: NO (disabled: lists 1.9.6) | collides krs_perks:perk:61e98757-9b32-493b-ad09-0087afdb81be; krs_perks:perk:ec4c5274-50e3-4bbf-9220-823b080647c4 |
| 2017 | Realistic Items | KRS-Items-2017-1-0-0-1749069665.7z: NO (disabled: lists 1.9.x) | Data\krs-items.pak: not a ZIP (the game cannot open it); inner files Tables\item\document__KRS-items.xml, Tabl; KRS-Items-2017-1-1-1-1749401836.7z: no manifest in the archive (legacy install: copy into Data) | KRS-Items\Data\KRS-Items.pak: not a ZIP (the game cannot open it); inner files Tables\item\document__KRS-items |
| 83 | More Responsive Targeting | More Responsive Targeting-83-1-04-: no manifest in the archive (legacy install: copy into Data) |
| 390 | Stay Clean Longer - Get Dirty Gradually | MGs Stay Clean Longer - Get Dirty : yes (no version restriction) |
| 591 | Bushes- Collision Remover | Bushes.Only_Collision.Remover-591-: yes (no version restriction) |
| 1090 | Colored Arrows | Colored Arrows and Feathers - Whit: yes (wildcard) |
| 1730 | Drink Sound Effects | Drink Sound Effects 1.1-1730-1-1-1: NO (disabled: lists 1.9.6) |
| 1743 | Persistent Arrows | Persistentarrows-1743-1-2-17295683: yes (wildcard) |
| 726 | Early Bird NPC Schedules | Early Bird NPC rescheduler-726-2-1: yes (no version restriction) |
| 771 | Hoods Over Helmats Removed Clipping Helm | Hoods Over Helmets Remove Kettle H: yes (no version restriction) | Data\Hoods Over Helmets.pak!Libs/Tables/item/ammo.xml: no suffix: replaces the whole vanilla table | Data\Hood |
| 1218 | Lartigue's Upscale Project 2.0 - Upscale | LartiguesUpscaleProject2.1-1218-2-: yes (no version restriction); LartiguesUpscaleProject2.1.1-1218-: yes (no version restriction) |
| 1485 | SOLID HELMET VISORS | SOLID HELMET VISORS-1485-1-2-17374: yes (no version restriction) |
| 1605 | Formidable Runt | Formidable Runt-1605-1-4-171120139: yes (no version restriction) |
| 1618 | HD Clock Retexture - Inventory Clock Upd | Time-HD-updated v1.2.zip-1618-1-2-: yes (no version restriction) |
| 1723 | Intimidation Stat In Inventory | IntimidationStat-1723-1-1-17282176: yes (no version restriction) |
| 800 | Volumetric Fog Shadows | VolumetricFogShadows-800-1-1-15637: yes (wildcard) |
| 1227 | 30 FPS Cutscene Fix V3 | 30 FPSCutscene Fix V2-1227-2-0-172: yes (no version restriction) |

## Overlap with the KRS modules (P2, by module)

### krs_perks: 60 mods (20 with measured or likely collision)

| Id | Mod | Why | Updated |
|---|---|---|---|
| 1765 | Restore Riposte | measured: krs_perks:perk:61e98757-9b32-493b-ad09-0087afdb81be; krs_perks:perk:ec4c5274-50e3-4bbf-9220-823b0806 | Restore Riposte for player use.Pick up your weapons and get a head start on adapting to the new combat system before KCD2 comes! |  |
| 85 | Perkaholic | likely: evidence names the same values | Adds additional perks to existing perk lists as well as adding perks to the Bow, Polearm and Unarmed skills. |  |
| 765 | Poison Overhaul | likely: evidence names the same values | Buffs or fixes some potions and adds a perk so poisons are useful (formerly Alchemical Warfare); users report it works on 1.9.6 and later Pr | 2022-07-09 |
| 770 | Perkaholic updated | likely: evidence names the same values | Adds additional perks to existing perk lists as well as adding perks to the Bow, Polearm and Unarmed skills. Updated for 1.9.* (All credits  |  |
| 883 | KingdomCome Rebalancing | likely: evidence names the same values | This Mod changes:- Weapons (mostly Swords)- Armor (Weight, Denfenserating, Prices, ...)- Skills/Perks (Lvl up slower, other Levels required  |  |
| 1009 | Perkaholic - PTF updated (1.9.4-1.9.8) | likely: evidence names the same values | Adds additional perks to existing perk lists as well as adding perks to the Bow, Polearm and Unarmed skills. 56 in total. |  |
| 1260 | RPG Tweaks | likely: evidence names the same values | Clean tweak of the rpg_param XML: stay clean longer; slightly bigger herb radius; lower stamina costs; easier sharpening; carry weight +60%; | 2021-07-26 |
| 1292 | Ultimate Repair Kit 2.0 | likely: evidence names the same values | This mod aims to recreate the experience of Ultimate Repair Kit that will actually work with the new version of the game, be compatible with |  |
| 1334 | Fast Learning Henry | likely: evidence names the same values | XP tables about 5x faster; version 1 raises every skill cap to 25; was not compatible with other mods that modify RPG_PARAMS I decided to ma | 2022-02-12 |
| 1375 | No Aim Spread (Bow sway disabler) | likely: evidence names the same values | Adds a perk (True Shot) that removes bow sway for the player only; variant 2.1b has two stat-gated perks (Forceful Grip: Strength min 10; Ra |  |
| 1572 | Increased Experience Gains | likely: evidence names the same values | Changes rpg_param to raise XP gain 1.5x / 2x / 5x; optional herb picking and auto brewing Increases experience gain by 1.5, 2x or 5x | 2023-11-27 |
| 1668 | Relaxed RPG Params | likely: evidence names the same values | Pack of rpg_param values: inventory x3 (horse x4); riding XP +25%; bow aim spread -33%; stamina regen delay -33%; sprint/jump cost -15%; les | 2024-06-21 |
| 1736 | Rogue Life | likely: evidence names the same values | Adds perks to the Stealth, Alchemy, Speech, Drinking and Bow trees and adjusts vanilla perks; recommends Perkaholic A collection of modules  | 2025-02-17 |
| 1860 | Train More Carry More - PTF | likely: evidence names the same values | Carry capacity scales with strength (x1.25 or x1.5) without changing the base carry weight; PTF. The suite's krs_qol carry value derives fro | 2025-02-14 |
| 1990 | Veteran Hunting | likely: evidence names the same values | Hunting overhaul: gives the player a perk with a custom buff that makes animals skittish; changes animal soul hearing parameters Started as  | 2025-04-25 |
| 2210 | True Hardcore Alchemy (PTF) | likely: evidence names the same values | Reduces the error tolerance of alchemy, rebalances potions and alchemy perks, and removes the exploit that allows a single potion to be appl |  |
| 2219 | True Hardcore Crime (PTF) | likely: evidence names the same values | Fragile lockpicks, tougher pickpocketing, increased noise, harsher punishments, unforgiving reputation, a perk overhaul, and more. More deta |  |
| 2246 | Console Editable RpgParams | likely: evidence names the same values | Makes rpg parameters editable from the console at any time; the search returned the KCD2 page, so the KCD1 page is unconfirmed Expose rpgpar |  |
| 2338 | Horse Collision Mod | likely: evidence names the same values | Horse collision reactions by speed; no vanilla file replaced This mod adds animations and physical reactions with immersive detail when Henr |  |
| 2362 | Better Perk Descriptions | likely: evidence names the same values | Changes the perk descriptions to include precise information about the perk. Finally you can make informed choices! |  |

Title-based only: 83, 284, 651, 1040, 1070, 1112, 1148, 1236, 1243, 1384, 1518, 1519, 1520, 1563, 1569, 1612, 1629, 1647, 1655, 1671, 1673, 1863, 1950, 2045, 2049, 2124, 2179, 2188, 2192, 2194, 2208, 2209, 2256, 2294, 2299, 2318, 2326, 2340, 2359, 2381.

### krs_items: 45 mods (16 with measured or likely collision)

| Id | Mod | Why | Updated |
|---|---|---|---|
| 1639 | Alternate Food Spoil (2X) | measured: krs_items:food:73ff1fde-ec8b-41e9-95e3-b5938c715bf1 | Doubles the time it takes for food to spoil. |  |
| 366 | First-person Herb Picking | likely: evidence names the same values | Forces the game to stay in first-person-view when picking herbs. |  |
| 765 | Poison Overhaul | likely: evidence names the same values | Buffs or fixes some potions and adds a perk so poisons are useful (formerly Alchemical Warfare); users report it works on 1.9.6 and later Pr | 2022-07-09 |
| 1260 | RPG Tweaks | likely: evidence names the same values | Clean tweak of the rpg_param XML: stay clean longer; slightly bigger herb radius; lower stamina costs; easier sharpening; carry weight +60%; | 2021-07-26 |
| 1266 | Stronger drinks - PTF Edition | likely: evidence names the same values | Raises the alcohol percentage of drinks (beer 8, moonshine 53, wine 18, mead 25 ...) in the food table; incompatible with mods that override | 2021-07-23 |
| 1572 | Increased Experience Gains | likely: evidence names the same values | Changes rpg_param to raise XP gain 1.5x / 2x / 5x; optional herb picking and auto brewing Increases experience gain by 1.5, 2x or 5x | 2023-11-27 |
| 1668 | Relaxed RPG Params | likely: evidence names the same values | Pack of rpg_param values: inventory x3 (horse x4); riding XP +25%; bow aim spread -33%; stamina regen delay -33%; sprint/jump cost -15%; les | 2024-06-21 |
| 1736 | Rogue Life | likely: evidence names the same values | Adds perks to the Stealth, Alchemy, Speech, Drinking and Bow trees and adjusts vanilla perks; recommends Perkaholic A collection of modules  | 2025-02-17 |
| 1914 | Weightless Herbs | likely: evidence names the same values | Makes alchemy herbs weightless |  |
| 1938 | My Herb Picking Radius | likely: evidence names the same values | Double the herb picking radius. |  |
| 1990 | Veteran Hunting | likely: evidence names the same values | Hunting overhaul: gives the player a perk with a custom buff that makes animals skittish; changes animal soul hearing parameters Started as  | 2025-04-25 |
| 1996 | Alcohol Is Not Food Anymore | likely: evidence names the same values | Exactly as the title says Alcohol Is Not Food Anymore. |  |
| 2011 | Chefs Kiss | likely: evidence names the same values | UI supported - New rules for foods, drinks, potions, poisons, health regen, stamina regen, weapon and stat buffs, nutrition, energy, starvat |  |
| 2207 | Findable Herbs HD | likely: evidence names the same values | Makes hard to find herbs less hard to find by changing their visuals. |  |
| 2210 | True Hardcore Alchemy (PTF) | likely: evidence names the same values | Reduces the error tolerance of alchemy, rebalances potions and alchemy perks, and removes the exploit that allows a single potion to be appl |  |
| 2276 | Instant Herb and faster Alchemy Merger | likely: evidence names the same values | Mods that change animations usually conflict in KCD. This is T0rvadaL's instant herb picking with faster alchemy animations thrown in by me. |  |

Title-based only: 311, 390, 480, 1062, 1105, 1195, 1424, 1426, 1483, 1518, 1652, 1660, 1730, 1862, 1864, 1883, 1922, 1926, 1950, 1951, 1991, 2098, 2208, 2209, 2280, 2323, 2345, 2372, 2381.

### krs_qol: 22 mods (13 with measured or likely collision)

| Id | Mod | Why | Updated |
|---|---|---|---|
| 366 | First-person Herb Picking | likely: evidence names the same values | Forces the game to stay in first-person-view when picking herbs. |  |
| 883 | KingdomCome Rebalancing | likely: evidence names the same values | This Mod changes:- Weapons (mostly Swords)- Armor (Weight, Denfenserating, Prices, ...)- Skills/Perks (Lvl up slower, other Levels required  |  |
| 1260 | RPG Tweaks | likely: evidence names the same values | Clean tweak of the rpg_param XML: stay clean longer; slightly bigger herb radius; lower stamina costs; easier sharpening; carry weight +60%; | 2021-07-26 |
| 1292 | Ultimate Repair Kit 2.0 | likely: evidence names the same values | This mod aims to recreate the experience of Ultimate Repair Kit that will actually work with the new version of the game, be compatible with |  |
| 1572 | Increased Experience Gains | likely: evidence names the same values | Changes rpg_param to raise XP gain 1.5x / 2x / 5x; optional herb picking and auto brewing Increases experience gain by 1.5, 2x or 5x | 2023-11-27 |
| 1839 | Realistic Horses | likely: evidence names the same values | Reduce horse carrying capacity to add realism and inventory management |  |
| 1860 | Train More Carry More - PTF | likely: evidence names the same values | Carry capacity scales with strength (x1.25 or x1.5) without changing the base carry weight; PTF. The suite's krs_qol carry value derives fro | 2025-02-14 |
| 1914 | Weightless Herbs | likely: evidence names the same values | Makes alchemy herbs weightless |  |
| 1938 | My Herb Picking Radius | likely: evidence names the same values | Double the herb picking radius. |  |
| 2021 | Repair Kits - Balanced and Scaled PTF | likely: evidence names the same values | Rescales armourer, blacksmith, tailor and cobbler kit efficiency (small and large); normal and Hardcore modes. Same area as krs_qol repairs  | 2025-06-10 |
| 2173 | True Hardcore Maintenance (PTF) | likely: evidence names the same values | Rebalances repair kits, makes you pay full repair costs at shops, and removes repair kits from enemy inventories and camps. More details bel |  |
| 2207 | Findable Herbs HD | likely: evidence names the same values | Makes hard to find herbs less hard to find by changing their visuals. |  |
| 2276 | Instant Herb and faster Alchemy Merger | likely: evidence names the same values | Mods that change animations usually conflict in KCD. This is T0rvadaL's instant herb picking with faster alchemy animations thrown in by me. |  |

Title-based only: 1425, 1483, 1545, 1560, 1578, 1842, 1853, 2165, 2348.

### krs_bow (planned): 32 mods (12 with measured or likely collision)

| Id | Mod | Why | Updated |
|---|---|---|---|
| 85 | Perkaholic | likely: evidence names the same values | Adds additional perks to existing perk lists as well as adding perks to the Bow, Polearm and Unarmed skills. |  |
| 770 | Perkaholic updated | likely: evidence names the same values | Adds additional perks to existing perk lists as well as adding perks to the Bow, Polearm and Unarmed skills. Updated for 1.9.* (All credits  |  |
| 802 | Archery for 1.9 | likely: evidence names the same values | An update of archery variables 'rpg_param,xml' for 1.9 |  |
| 1009 | Perkaholic - PTF updated (1.9.4-1.9.8) | likely: evidence names the same values | Adds additional perks to existing perk lists as well as adding perks to the Bow, Polearm and Unarmed skills. 56 in total. |  |
| 1100 | Faster archery - PTF Edition | likely: evidence names the same values | Sets BowChargeDurationMax (1.00 hard / 1.25 normal / 1.50 easy) through rpg_param; aim spread unchanged. Shows that a published mod already  |  |
| 1260 | RPG Tweaks | likely: evidence names the same values | Clean tweak of the rpg_param XML: stay clean longer; slightly bigger herb radius; lower stamina costs; easier sharpening; carry weight +60%; | 2021-07-26 |
| 1292 | Ultimate Repair Kit 2.0 | likely: evidence names the same values | This mod aims to recreate the experience of Ultimate Repair Kit that will actually work with the new version of the game, be compatible with |  |
| 1375 | No Aim Spread (Bow sway disabler) | likely: evidence names the same values | Adds a perk (True Shot) that removes bow sway for the player only; variant 2.1b has two stat-gated perks (Forceful Grip: Strength min 10; Ra |  |
| 1419 | Immersive Archery | likely: evidence names the same values | Draw speed to about 16 arrows per minute; arrow speed x1.7; lower stamina drain; arrow damage x1.2. The suite alters this mod (permission gr | 2022-10-13 |
| 1668 | Relaxed RPG Params | likely: evidence names the same values | Pack of rpg_param values: inventory x3 (horse x4); riding XP +25%; bow aim spread -33%; stamina regen delay -33%; sprint/jump cost -15%; les | 2024-06-21 |
| 1678 | Better Archery | likely: evidence names the same values | Faster arrows, shorter draw, lower stamina drain, less aim spread, rebalanced damage; three variants (a no-OP variant added 2025-01-07) PTF. | 2025-01-07 |
| 1736 | Rogue Life | likely: evidence names the same values | Adds perks to the Stealth, Alchemy, Speech, Drinking and Bow trees and adjusts vanilla perks; recommends Perkaholic A collection of modules  | 2025-02-17 |

Title-based only: 84, 651, 804, 1084, 1090, 1205, 1376, 1519, 1520, 1559, 1564, 1565, 1743, 1893, 2035, 2040, 2179, 2192, 2294, 2381.

## Mods that state a game version (from search summaries or archives)

| Id | Mod | Version statement |
|---|---|---|
| 1639 | Alternate Food Spoil (2X) | yes (no version restriction) |
| 1765 | Restore Riposte | NO (disabled: lists 1.9.6) |
| 2017 | Realistic Items | NO (disabled: lists 1.9.x) |
| 83 | More Responsive Targeting | no manifest in the archive (legacy install: copy into Data) |
| 390 | Stay Clean Longer - Get Dirty Gradually | yes (no version restriction) |
| 591 | Bushes- Collision Remover | yes (no version restriction) |
| 1009 | Perkaholic - PTF updated (1.9.4-1.9.8) | states 1.9.8 (page summary) |
| 1090 | Colored Arrows | yes (wildcard) |
| 1100 | Faster archery - PTF Edition | states 1.9.6-404-504 FINAL (page summary) |
| 1323 | Skalitz Shield Fix AWL | states 1.9.8 (page summary) |
| 1572 | Increased Experience Gains | states 1.9.6 (page summary) |
| 1693 | Ravens beak and Spiked warhammer icon swap | states 1.9.8 (page summary) |
| 1730 | Drink Sound Effects | NO (disabled: lists 1.9.6) |
| 1743 | Persistent Arrows | yes (wildcard) |
| 2040 | Polymorphic Projectiles Arrow Overhaul | states 1.9.8 (page summary) |
| 2124 | Half-looted Rebalance | states 1.9.8 (page summary) |
| 2179 | True Hardcore Combat (PTF) | states 1.9.8 (page summary) |
| 2208 | Medieval Poisons - True Hardcore Compatibili | states 1.9.8 (page summary) |
| 2210 | True Hardcore Alchemy (PTF) | states 1.9.8 (page summary) |
| 2219 | True Hardcore Crime (PTF) | states 1.9.8 (page summary) |
| 2331 | Bushes Collision Remover Redux | states 1.9.8 (page summary) |
| 2359 | KCD Kombat Tune | states Steam 1.9.7-404-504czj4 only (page summary) |
| 726 | Early Bird NPC Schedules | yes (no version restriction) |
| 771 | Hoods Over Helmats Removed Clipping Helmets  | yes (no version restriction) |
| 796 | Miller Guild Items | states 1.9 (page summary) |
| 1218 | Lartigue's Upscale Project 2.0 - Upscaled UI | yes (no version restriction) |
| 1485 | SOLID HELMET VISORS | yes (no version restriction) |
| 1605 | Formidable Runt | yes (no version restriction) |
| 1618 | HD Clock Retexture - Inventory Clock Updated | yes (no version restriction) |
| 1723 | Intimidation Stat In Inventory | yes (no version restriction) |
| 2079 | Thin The Herd - Immersive Hunting and Realis | states 1.9.6 (page summary) |
| 2244 | Kingdom Come Script Extender | states 1.9.8 (page summary) |
| 2273 | Address Library For KCSE | states 1.9.8 (page summary) |
| 800 | Volumetric Fog Shadows | yes (wildcard) |
| 1227 | 30 FPS Cutscene Fix V3 | yes (no version restriction) |

## Nexus API (tools/nexus_metadata.py, run by the author)

Status of the 365 ids: published 363, removed 1, removed_by_staff 1.

Not published: 1131 SPOA SILVER KNIGHT ARMOR for KCD - DELET (removed_by_staff), 1296 Kingdom Come Enhanced Edition 2.0 - DELE (removed).

Flagged adult by Nexus: 1045 MORE BLOOD, 1900 Jiggle Physics, 2304 Female Nudity.

File lists and versions were not fetched yet (`python tools/nexus_metadata.py --files`).


## Still to identify or classify by hand

Ids without a usable name: none.

Ids no rule classified: 837, 2100, 2365.
