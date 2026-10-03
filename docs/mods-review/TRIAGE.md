# Mod triage (generated)

> **GENERATED** by `tools/triage_mods.py`: do not edit | **Kind:** review | **Trust:** rules applied to titles, search summaries and 26 archives read locally | **Game version:** 1.9.8

365 mods. Rules and evidence classes are in the header of `tools/triage_mods.py`; the per-mod table is `mods_triage.csv`. This is a repeatable sort, not a verdict: only the rows marked evidence **A** (archive read) are measured.

## Counts

| Priority | Mods | Meaning |
|---|---|---|
| P1 | 3 | act now |
| P2 | 113 | compare or check before combining |
| P3 | 199 | optional or not mapped |
| P4 | 50 | outside the suite's scope |

| Evidence | Mods |
|---|---|
| A archive | 18 |
| B search result | 41 |
| C title | 299 |
| D id only | 7 |

## Actions

| Priority | Action | Mods |
|---|---|---|
| P1 | Replace the published release | 1 |
| P1 | Resolve the measured row collision | 2 |
| P2 | Check on 1.9.8 whether the fix is still needed | 10 |
| P2 | Compare tables | 82 |
| P2 | Disabled on 1.9.8 by its manifest: edit the version line | 1 |
| P2 | Study the rows and compare | 20 |
| P3 | Classify by hand | 8 |
| P3 | Optional companion: outside the PTF scope, check version support | 102 |
| P3 | Review: gameplay mod not mapped to a KRS module | 89 |
| P4 | Optional visual: no table overlap expected | 46 |
| P4 | Out of scope | 4 |

## P1 and the archive-measured mods

| Id | Mod | Finding |
|---|---|---|
| 1639 | Alternate Food Spoil (2X) | AlternateFoodSpoil2X-1639-1-0-1715: yes (no version restriction) | id 'alternatefoodspoil2x' has characters other than lowercase letters and underscore (the engine warns; patche | collides krs_items:food:73ff1fde-ec8b-41e9-95e3-b5938c715bf1 |
| 1765 | Restore Riposte | Riposte-1765-1-0-2-1735871267.zip: NO (disabled: lists 1.9.6) | collides krs_perks:perk:61e98757-9b32-493b-ad09-0087afdb81be; krs_perks:perk:ec4c5274-50e3-4bbf-9220-823b080647c4 |
| 2017 | Realistic Items | KRS-Items-2017-1-0-0-1749069665.7z: NO (disabled: lists 1.9.x) | Data\krs-items.pak: not a ZIP (the game cannot open it); inner files Tables\item\document__KRS-items.xml, Tabl; KRS-Items-2017-1-1-1-1749401836.7z: no manifest in the archive (legacy install: copy into Data) | KRS-Items\Data\KRS-Items.pak: not a ZIP (the game cannot open it); inner files Tables\item\document__KRS-items |
| 83 | More Responsive Targeting | More Responsive Targeting-83-1-04-: no manifest in the archive (legacy install: copy into Data) |
| 390 | MGs Stay Clean Longer - Get Dirty Gradua | MGs Stay Clean Longer - Get Dirty : yes (no version restriction) |
| 591 | Bushes- Collision Remover | Bushes.Only_Collision.Remover-591-: yes (no version restriction) |
| 1090 | Colored Arrows | Colored Arrows and Feathers - Whit: yes (wildcard) |
| 1730 | Drink Sound Effects | Drink Sound Effects 1.1-1730-1-1-1: NO (disabled: lists 1.9.6) |
| 1743 | Persistent Arrows | Persistentarrows-1743-1-2-17295683: yes (wildcard) |
| 726 | Early Bird NPC rescheduler | Early Bird NPC rescheduler-726-2-1: yes (no version restriction) |
| 771 | Hoods Over Helmets Remove Kettle Helmets | Hoods Over Helmets Remove Kettle H: yes (no version restriction) | Data\Hoods Over Helmets.pak!Libs/Tables/item/ammo.xml: no suffix: replaces the whole vanilla table | Data\Hood |
| 1218 | Lartigue's Upscale Project 2.0 - Upscale | LartiguesUpscaleProject2.1-1218-2-: yes (no version restriction); LartiguesUpscaleProject2.1.1-1218-: yes (no version restriction) |
| 1485 | SOLID HELMET VISORS | SOLID HELMET VISORS-1485-1-2-17374: yes (no version restriction) |
| 1605 | Formidable Runt | Formidable Runt-1605-1-4-171120139: yes (no version restriction) |
| 1618 | Time-HD-updated v1.2.zip | Time-HD-updated v1.2.zip-1618-1-2-: yes (no version restriction) |
| 1723 | Intimidation Stat In Inventory | IntimidationStat-1723-1-1-17282176: yes (no version restriction) |
| 800 | Volumetric Fog Shadows | VolumetricFogShadows-800-1-1-15637: yes (wildcard) |
| 1227 | 30 FPS Cutscene Fix V3 | 30 FPSCutscene Fix V2-1227-2-0-172: yes (no version restriction) |

## Overlap with the KRS modules (P2, by module)

### krs_perks: 52 mods (11 with measured or likely collision)

| Id | Mod | Why | Updated |
|---|---|---|---|
| 1765 | Restore Riposte | measured: krs_perks:perk:61e98757-9b32-493b-ad09-0087afdb81be; krs_perks:perk:ec4c5274-50e3-4bbf-9220-823b0806  |  |
| 765 | Poison Overhaul | likely: evidence names the same values | Buffs or fixes some potions and adds a perk so poisons are useful (formerly Alchemical Warfare); users report it works on 1.9.6 and later | 2022-07-09 |
| 1260 | RPG Tweaks | likely: evidence names the same values | Clean tweak of the rpg_param XML: stay clean longer; slightly bigger herb radius; lower stamina costs; easier sharpening; carry weight +60%; | 2021-07-26 |
| 1334 | Fast Learning Henry | likely: evidence names the same values | XP tables about 5x faster; version 1 raises every skill cap to 25; was not compatible with other mods that modify RPG_PARAMS | 2022-02-12 |
| 1375 | No Aim Spread (Bow sway disabler) | likely: evidence names the same values | Adds a perk (True Shot) that removes bow sway for the player only; variant 2.1b has two stat-gated perks (Forceful Grip: Strength min 10; Ra |  |
| 1572 | Increased Experience Gains | likely: evidence names the same values | Changes rpg_param to raise XP gain 1.5x / 2x / 5x; optional herb picking and auto brewing | 2023-11-27 |
| 1668 | Relaxed RPG Params | likely: evidence names the same values | Pack of rpg_param values: inventory x3 (horse x4); riding XP +25%; bow aim spread -33%; stamina regen delay -33%; sprint/jump cost -15%; les | 2024-06-21 |
| 1736 | Rogue Life | likely: evidence names the same values | Adds perks to the Stealth, Alchemy, Speech, Drinking and Bow trees and adjusts vanilla perks; recommends Perkaholic | 2025-02-17 |
| 1860 | Train More Carry More - PTF | likely: evidence names the same values | Carry capacity scales with strength (x1.25 or x1.5) without changing the base carry weight; PTF. The suite's krs_qol carry value derives fro | 2025-02-14 |
| 1990 | Veteran Hunting | likely: evidence names the same values | Hunting overhaul: gives the player a perk with a custom buff that makes animals skittish; changes animal soul hearing parameters | 2025-04-25 |
| 2246 | Console Editable RpgParams | likely: evidence names the same values | Makes rpg parameters editable from the console at any time; the search returned the KCD2 page, so the KCD1 page is unconfirmed |  |

Title-based only: 83, 85, 284, 651, 770, 883, 1009, 1040, 1070, 1112, 1148, 1236, 1243, 1384, 1518, 1519, 1520, 1612, 1629, 1647, 1655, 1671, 1673, 1863, 1950, 2049, 2124, 2179, 2188, 2192, 2194, 2208, 2209, 2210, 2256, 2294, 2299, 2318, 2326, 2340, 2359.

### krs_items: 40 mods (8 with measured or likely collision)

| Id | Mod | Why | Updated |
|---|---|---|---|
| 1639 | Alternate Food Spoil (2X) | measured: krs_items:food:73ff1fde-ec8b-41e9-95e3-b5938c715bf1  |  |
| 765 | Poison Overhaul | likely: evidence names the same values | Buffs or fixes some potions and adds a perk so poisons are useful (formerly Alchemical Warfare); users report it works on 1.9.6 and later | 2022-07-09 |
| 1260 | RPG Tweaks | likely: evidence names the same values | Clean tweak of the rpg_param XML: stay clean longer; slightly bigger herb radius; lower stamina costs; easier sharpening; carry weight +60%; | 2021-07-26 |
| 1266 | Stronger drinks - PTF Edition | likely: evidence names the same values | Raises the alcohol percentage of drinks (beer 8, moonshine 53, wine 18, mead 25 ...) in the food table; incompatible with mods that override | 2021-07-23 |
| 1572 | Increased Experience Gains | likely: evidence names the same values | Changes rpg_param to raise XP gain 1.5x / 2x / 5x; optional herb picking and auto brewing | 2023-11-27 |
| 1668 | Relaxed RPG Params | likely: evidence names the same values | Pack of rpg_param values: inventory x3 (horse x4); riding XP +25%; bow aim spread -33%; stamina regen delay -33%; sprint/jump cost -15%; les | 2024-06-21 |
| 1736 | Rogue Life | likely: evidence names the same values | Adds perks to the Stealth, Alchemy, Speech, Drinking and Bow trees and adjusts vanilla perks; recommends Perkaholic | 2025-02-17 |
| 1990 | Veteran Hunting | likely: evidence names the same values | Hunting overhaul: gives the player a perk with a custom buff that makes animals skittish; changes animal soul hearing parameters | 2025-04-25 |

Title-based only: 311, 366, 390, 480, 1062, 1195, 1424, 1426, 1483, 1652, 1660, 1730, 1862, 1864, 1914, 1922, 1926, 1938, 1950, 1951, 1991, 1996, 2011, 2098, 2207, 2208, 2209, 2210, 2276, 2280, 2323, 2372.

### krs_qol: 17 mods (4 with measured or likely collision)

| Id | Mod | Why | Updated |
|---|---|---|---|
| 1260 | RPG Tweaks | likely: evidence names the same values | Clean tweak of the rpg_param XML: stay clean longer; slightly bigger herb radius; lower stamina costs; easier sharpening; carry weight +60%; | 2021-07-26 |
| 1572 | Increased Experience Gains | likely: evidence names the same values | Changes rpg_param to raise XP gain 1.5x / 2x / 5x; optional herb picking and auto brewing | 2023-11-27 |
| 1860 | Train More Carry More - PTF | likely: evidence names the same values | Carry capacity scales with strength (x1.25 or x1.5) without changing the base carry weight; PTF. The suite's krs_qol carry value derives fro | 2025-02-14 |
| 2021 | Repair Kits - Balanced and Scaled PTF | likely: evidence names the same values | Rescales armourer, blacksmith, tailor and cobbler kit efficiency (small and large); normal and Hardcore modes. Same area as krs_qol repairs | 2025-06-10 |

Title-based only: 366, 1292, 1483, 1545, 1560, 1578, 1842, 1914, 1938, 2173, 2207, 2276, 2348.

### krs_bow (planned): 22 mods (7 with measured or likely collision)

| Id | Mod | Why | Updated |
|---|---|---|---|
| 1100 | Faster archery - PTF Edition | likely: evidence names the same values | Sets BowChargeDurationMax (1.00 hard / 1.25 normal / 1.50 easy) through rpg_param; aim spread unchanged. Shows that a published mod already  |  |
| 1260 | RPG Tweaks | likely: evidence names the same values | Clean tweak of the rpg_param XML: stay clean longer; slightly bigger herb radius; lower stamina costs; easier sharpening; carry weight +60%; | 2021-07-26 |
| 1375 | No Aim Spread (Bow sway disabler) | likely: evidence names the same values | Adds a perk (True Shot) that removes bow sway for the player only; variant 2.1b has two stat-gated perks (Forceful Grip: Strength min 10; Ra |  |
| 1419 | Immersive Archery | likely: evidence names the same values | Draw speed to about 16 arrows per minute; arrow speed x1.7; lower stamina drain; arrow damage x1.2. The suite alters this mod (permission gr | 2022-10-13 |
| 1668 | Relaxed RPG Params | likely: evidence names the same values | Pack of rpg_param values: inventory x3 (horse x4); riding XP +25%; bow aim spread -33%; stamina regen delay -33%; sprint/jump cost -15%; les | 2024-06-21 |
| 1678 | Better Archery | likely: evidence names the same values | Faster arrows, shorter draw, lower stamina drain, less aim spread, rebalanced damage; three variants (a no-OP variant added 2025-01-07) | 2025-01-07 |
| 1736 | Rogue Life | likely: evidence names the same values | Adds perks to the Stealth, Alchemy, Speech, Drinking and Bow trees and adjusts vanilla perks; recommends Perkaholic | 2025-02-17 |

Title-based only: 84, 802, 804, 1084, 1090, 1205, 1376, 1520, 1564, 1565, 1743, 2035, 2040, 2192, 2294.

## Mods that state a game version (from search summaries or archives)

| Id | Mod | Version statement |
|---|---|---|
| 1639 | Alternate Food Spoil (2X) | yes (no version restriction) |
| 1765 | Restore Riposte | NO (disabled: lists 1.9.6) |
| 2017 | Realistic Items | NO (disabled: lists 1.9.x) |
| 83 | More Responsive Targeting | no manifest in the archive (legacy install: copy into Data) |
| 390 | MGs Stay Clean Longer - Get Dirty Gradually  | yes (no version restriction) |
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
| 2331 | Bushes Collision Remover Redux | states 1.9.8 (page summary) |
| 2359 | KCD Kombat Tune | states Steam 1.9.7-404-504czj4 only (page summary) |
| 726 | Early Bird NPC rescheduler | yes (no version restriction) |
| 771 | Hoods Over Helmets Remove Kettle Helmets NPC | yes (no version restriction) |
| 796 | Miller Guild Items | states 1.9 (page summary) |
| 1218 | Lartigue's Upscale Project 2.0 - Upscaled UI | yes (no version restriction) |
| 1485 | SOLID HELMET VISORS | yes (no version restriction) |
| 1605 | Formidable Runt | yes (no version restriction) |
| 1618 | Time-HD-updated v1.2.zip | yes (no version restriction) |
| 1723 | Intimidation Stat In Inventory | yes (no version restriction) |
| 2079 | Thin The Herd - Realistic Animal Drops - Rea | states 1.9.6 (page summary) |
| 2219 | True Hardcore Crime (PTF) | states 1.9.8 (page summary) |
| 2244 | Kingdom Come Script Extender | states 1.9.8 (page summary) |
| 2273 | Address Library For KCSE | states 1.9.8 (page summary) |
| 800 | Volumetric Fog Shadows | yes (wildcard) |
| 1227 | 30 FPS Cutscene Fix V3 | yes (no version restriction) |

## Still to identify or classify by hand

Ids without a usable name: 2100, 2132, 2297, 2330, 2345, 2362, 2365.

Ids no rule classified: 1131.
