# Analysis of the added Vivaldi-tab mods

**Scope:** the 180 mods from `nexusmods_abas_vivaldi.csv` were added to the review list and merged with the 135 mods from the history screenshots. The merged list is [id_titles.csv](id_titles.csv): **290 unique mods** (155 only in the Vivaldi tabs, 110 only in the screenshots, 25 in both).

**Limits (read first):**
1. Nexus returned HTTP 403 when I tried to open a mod page, so no page, file list, changelog or date was read. I did not try to work around it.
2. Everything below comes from **mod titles**, the PTF tag, ID order, and the notes already in the review files. A "verdict" would be a guess, so every row is `Unverified (title only)`.
3. Categories are keyword-based with manual fixes; a few will be wrong. The mod ID and title are the reliable columns.

## 1. Breakdown by category (all 290)

| Category | All | Newly added from Vivaldi |
|---|---|---|
| Weapons / armor / items | 36 | 20 |
| Maps / UI / HUD | 34 | 16 |
| Reshade / ENB / visual preset | 26 | 23 |
| World / weather / visuals | 25 | 16 |
| Alchemy / food / survival | 24 | 9 |
| Combat / AI | 23 | 16 |
| Graphics config (cfg) | 19 | 16 |
| Progression / XP / perks | 17 | 13 |
| Archery / arrows | 15 | 12 |
| Quests / lore / content | 14 | 8 |
| Economy / merchants | 14 | 9 |
| Crime / stealth / loot | 13 | 6 |
| Tools / reference | 12 | 8 |
| Horses | 8 | 1 |
| Adult / nudity | 4 | 3 |
| Animations / audio | 3 | 3 |
| Other | 2 | 0 |
| Fix bundle | 1 | 1 |

PTF-titled mods: 28 in total (20 from Vivaldi). IDs below 1000 (26 mods) are old uploads and are the most likely to predate the current game version or the Mods-folder format.

## 2. Overlap clusters (title-evident)

Mods in a cluster do the same job or edit the same tables or files. Pick one per cluster, or test the pair before combining.

| Cluster | Mods | Concern |
|---|---|---|
| Archery / arrows | 802, 804, 1084, 1100, 1205, 1090, 1375, 1376, 1419, 1564, 1565, 1678, 1743, 2035, 2040 | All edit bow or arrow values. KRS alters 1419 and requires 1743, so any other archery mod can overwrite the same rows |
| Karnages series (12) | 1558, 1559, 1560, 1561, 1562, 1563, 1564, 1565, 1566, 1568, 1569, 1570 | One author, many tables: overlaps weapons, polearms (1088, 2045), arrows, shop prices (1105, 829, 1308), durability (2348, 1842, 2021) and cfg (1561) |
| Combat overhauls | 1070, 1112, 1384, 651, 2256, 2179, 2294, 1629, 1148, 2359, 2192, 2194, 1243, 1612, 1647, 883 | Overlap on combat, master-strike and AI tables. KRS alters Restore Riposte (1765), so this is the highest-conflict group for it |
| Weapon / polearm balance | 1088, 2045, 1562, 1563, 1559, 1148, 2046, 1636, 1153, 883 | Same weapon stat tables |
| Merchants / prices / money | 829, 1105, 1308, 1460, 1548, 2279, 1568, 1578, 1861, 1870, 1873, 1981, 2188 | Overlap on shop-price and merchant-money tables. 1460 (x3 money) and 1873 (rich merchants) push in the same direction and stack |
| XP / progression | 1518, 1519, 1520, 1572, 1860, 1334, 2340, 1668, 2246, 883, 1009, 2299 | Overlap on XP gain, perks and RPG parameters; KRS edits a perk row |
| Repair / durability | 1292, 1842, 2021, 2348, 1560, 1545 | Same repair and durability tables |
| Helmets | 1337, 1907, 1909, 2081 | Helmet and vision changes may touch the same item rows |
| Horses | 129, 1510, 2174, 2223, 2224, 2270, 2271, 2343 | Horse behaviour and caparison items |
| Weather / sky | 879, 1114, 1193, 1327, 1410, 1982 | Several weather systems; 1327 is also flagged as a whole-file replacer |
| Graphics cfg | 800, 1342, 1367, 1526, 1527, 1528, 1538, 1552, 1561, 1646, 1720, 1972, 2106, 2153, 2180, 2243, 2353 | Same user.cfg variables; the last one loaded wins and values are often hardware-specific |
| Reshade / ENB presets | 844, 975, 994, 1046, 1074, 1080, 1196, 1256, 1258, 1283, 1291, 1314, 1349, 1394, 1403, 1414, 1428, 1511, 1544, 1589, 1603, 1702, 1800, 1875, 2031, 2175 | Only one preset at a time; they replace each other rather than conflict with data |
| Maps (hi-res) | 827, 1182, 1281, 2384, 2156, 955 | Several map replacers and map overlays |
| HUD / UI | 978, 1063, 1218, 1956, 2030, 2108, 2147, 2293, 2103, 1723, 2317, 1719, 1780 | Replace .gfx and inventory files; conflicts will persist because UI cannot be a PTF |
| KCD1 Reborn series | 1918, 1927, 1964 | One author: terrain, vegetation and faces |
| Inventory sorting / language | 2203, 2204, 2374, 1779, 1479 | Rename or sort items per language |
| Translations of one mod | 491, 2316, 651, 2256, 2204, 2374 | Count each pair as one mod when comparing |

## 3. Where the added mods meet KRS

KRS requires EarlyBirdNPC, 30FPSCutsceneFixV2, MGsStayCleanLongerGetDirtyGradually and Persistentarrows, alters Restore Riposte (1765) and Immersive Archery (1419), and edits a perk row.

| KRS area | Added mods that touch it |
|---|---|
| Immersive Archery (1419, now in the list) | 802, 804, 1084, 1100, 1375, 1376, 1564, 1565, 1520, 1205, 1090 |
| Persistent arrows (1743) | 1090 Colored Arrows, 1205 glowing feathers, 1564 and 1565: visual and balance changes to arrows |
| Restore Riposte (1765, not in any list) | 1070, 1112, 1384, 1148, 2359, 1243, 1612 |
| Perk row | 1009 (already PTF), 1736, 1860, 1334, 1572 |
| Stay-clean mod | 2218 Clean Gear, 1863 Dirty And Charismatic (PTF), 1062 camping |
| 30 FPS cutscene fix | 1227 is V3, KRS requires V2. Compare before switching |

## 4. Fix-type mods added (candidates for fixed.md)

| ID | Mod | Note |
|---|---|---|
| 2332 | Baptism of Fire Fix Redux | Redux of a quest fix; check whether the quest bug is still present |
| 1558 | Karnages_KCD_Essential_Fixes 2.0 | A bug-fix bundle; each fix needs its own check |
| 1424 | Better Sleep Fixed | May fix another mod's sleep change rather than the game |
| 1426 | Energy and Hunger Patch for Timescale Mods (PTF) | A patch for other mods, not a game fix |
| 1227 | 30 FPS Cutscene Fix V3 | Game-side defect; KRS requires V2 |
| 1380 | Black Items Fix | Now has a real title (it was unresolved) |
| 1782, 2343, 2279, 1991 | From the earlier screenshots | See verification.md |

## 5. Not aligned with "non-intrusive PTF tweaks"

Adult-content mods: 1818, 1900, 2196, 2304. Large content or world replacements: 1918, 1927, 1964 (KCD1 Reborn), 1327, 1356 (fan side quest), 1535, 1683 (event/NPC content). These change the experience more than they refine it.

## 6. Tools and reference (not gameplay)


864 Official Kingdom Come Deliverance Modding Tools, 867 APEX Realistic Modding Guide tweaks and fixes, 1059 Icon ID Resource, 1110 AI Standalone Library, 1479 Batch files for all items sorted and easy to read, 1594 Having trouble with old mods (Question Mark), 1779 Semi Sorted soul XML, 1829 Mod Order Tool 1.2, 2119 KCD Mod Manager, 2216 KCD Mod Organizer Plugin (Steam - GOG - Epic), 2244 Kingdom Come Script Extender

2277 and 2255 need KCSE (2244), which supports 1.9.8.0 only per the review.

## 7. Recommended next steps

1. Allow www.nexusmods.com for this environment, or give me the archives; then each row can get a real file list and verdict.
2. Until then, review by cluster: pick the mod in each cluster that matches KRS (PTF-shaped, small scope) and test the pairs.
3. Resolve the 11 IDs still not found in any source: 284, 754, 765, 796, 797, 958, 1093, 1131, 1259, 1260, 1577.
