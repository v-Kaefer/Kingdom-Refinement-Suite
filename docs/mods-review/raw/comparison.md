### Author series

| Author | Mods | Note |
|---|---|---|
| DreamMora | 2190, 2191, 2192, 2194, 2196, 2199, 2206 | KCD2-port series, last updated March-September 2026 |
| Nfrog2swamp1 | 2179, 2188, 2209, 2210 (+ 2208) | "True Hardcore" PTF series with compatibility patches |
| MayDayU1A | 2103, 2108, 2147 | UI series; 2147 includes the pickpocket window that 2103 replaces |
| Diaz Dizazter | 2040, 2046, 2049 | Weapons, arrows and ragdolls |
| TyburnKetch | 1736, 1780 | Also author of Medieval Poisons, required by 2208 |
| JerryYOJ | 2244, 2255 | Script extender plus a plugin that needs it |

## 3. Version watchlist

KRS's `mod.manifest` lists support for **1.9.4, 1.9.5 and 1.9.6.x**, and your tested list is headed "1.9.6". Several 2026 mods target newer versions:

| Mod | Version statement |
|---|---|
| 2244 KCSE | Only 1.9.8.0 currently |
| 2040 Polymorphic Projectiles | Requires 1.9.7 or higher |
| 2331 Bushes Redux | Designed for 1.9.7 |
| 2208, 2210 | Made and tested on 1.9.8 |
| 2124 Half-looted | Made for 1.9.6, compatible with 1.9.7 |
| 1009 Perkaholic PTF | 1.9.4 to 1.9.8 |
| 1873 | Comments report problems on the latest version |

KRS's manifest may need new `kcd_version` entries if you target 1.9.7 or 1.9.8.

## 4. What lines up with KRS

KRS's `Requirements.md` names four required mods and two altered ones. This is the closest comparable in these lists for each area:

| KRS area | Comparable in the lists |
|---|---|
| Riposte (altered: Restore Riposte, minimum level 8 to 10) | 1629 recommends using it with Restore Riposte; 2294 (directional master strikes); 2179 |
| Archery (altered: Immersive Archery) | 1678 Better Archery is the closest; 2040 changes arrow damage values |
| Persistent arrows (required) | 1743 is the required mod itself; 2206 overlaps |
| Stay clean (required: MGsStayClean...) | 2218 (visual), 1260, 651 |
| Perk table (KRS edits a perk row) | 1009, 1736, 1990, 765, 2210 all touch perks |
| Localization paks (KRS ships four languages) | 797, 2203, 2204, 808 rename text and carry the same per-language upkeep |
| 30 FPS cutscene fix (required) | Not among the identified mods (71 IDs are unidentified, so it could still be one of them); the search surfaced 1227 "30 FPS Cutscene Fix V3" |
| Early bird NPC (required) | Not among the identified mods, same caveat |

**PTF examples worth studying for approach** (self-described PTF): 1009, 1423, 1870, 1873, 2022, 2045, 2046, 2158, 2171, 2174, 2179, 2188, 2208, 2209, 2210, 2340.

## 5. Where the approach could be improved

All from descriptions, none from source.

| ID | Observation | Possible improvement |
|---|---|---|
| 1332 | Replaces a whole vanilla Lua script (`camerashake.lua`) loose under `data/scripts/entities/other`; page says it may take minutes to apply | Ship as a manifest-based Mods-folder script override, or change only the shake values if they live in a table |
| 754 | Legacy dual-copy install (`Data` and `Data\_fastload`) | Mods-folder package with a manifest |
| 1309, 1327, 2333, 1723, 2317 | Replace a whole shared file (`random_event.xml`, a mission file, `q_returnToSkalitz.xml`, `Inventory.gfx`, `HUD.gfx`) and list conflicts | PTF-style row patch where the format allows; HUD changes cannot use PTF, so conflicts will persist |
| 1873, 1460 | Large flat multipliers on merchant gold | Per-merchant scaling tied to an in-game rule |
| 2171 | Misses pickpocketed items | Combine with the 2158 parameter approach |
| 2323 | Moves items between stashes, horse and pockets | Transactional move with rollback; test save safety |
| 2276 | Speed constant is edited by hand | Expose it in a config file |
| 2040 | Real arrow balance mixed with novelty arrows | Split balance and cosmetics into separate optional packages |
| 797, 2203, 2204, 808 | Name changes must be done per language | Generate localized text from one source |
| 651, 1260, 2124, 2299, 2340 | Large bundles | Split into optional modules (2340 already offers modular files) |
| 2216 | Repairs other mods' manifests on the fly | Back up before editing; test before trusting |
| 2244, 2255, 2348 | Native or version-locked code | Add game-version checks and fail loudly |
| 1972, 2180, 2243, 2153 | Hardware-specific cfg values published as general | Tiered presets with documented variables and measured results |

## 6. Adjacent mods surfaced by the search (not in your lists)

Seen while looking up the others; none were reviewed. Listed because they sit next to what you are building.

| ID | Name |
|---|---|
| 1040 | Disable Combat Slowmotion |
| 1227 | 30 FPS Cutscene Fix V3 |
| 1236 | Easy Combat PTF (easy parry and master strike) |
| 1296 | Kingdom Come Enhanced Edition 2.0 |
| 1334 | Fast Learning Henry |
| 1416 | Toxic Green Armor - PTF Standalone |
| 1689 | Playable Daggers |
| 1797 | Nighttime Nighthawk |
| 2119 | KCD Mod Manager |

Your README also names 1765 (Restore Riposte) and 1419 (Immersive Archery); neither was in the lists reviewed here.