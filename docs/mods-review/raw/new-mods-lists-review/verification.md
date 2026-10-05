# Verification of the new_mods_review set

Checked against: `README.md`, `comparison.md`, `fixed.md` (the only files present), the repo's `Requirements.md` and `mod.manifest`, and the browser-history titles captured in [id_titles.csv](id_titles.csv).

## 1. Missing or truncated content

| File | Problem |
|---|---|
| `catalog.md`, `unverified.md`, `mods.csv` | Linked from README but not in the folder. The 130-mod catalog and the 71 unresolved IDs cannot be checked |
| `README.md` | Starts mid-table at "71 IDs with no usable result"; title, summary and the first rows are gone |
| `comparison.md` | Starts at "### Author series"; the next heading is "## 3". Sections 1 and 2 (slop vs substance, overlap clusters, conflict groups) are missing |

## 2. Checks that pass

- Dedup arithmetic: 209 links - 6 repeats inside one file (2021, 2174, 2175, 2191, 2206, 2348) - 2 in both files (1330, 1337) = 201 = 130 identified + 71 unresolved.
- KRS facts match the repo: `Requirements.md` lists 4 required and 2 altered mods (1765, 1419) and the riposte level change 8 -> 10; `mod.manifest` supports 1.9.4, 1.9.5, 1.9.6.x.
- Version watchlist in `comparison.md` agrees with `fixed.md` (1.9.7: 2331, 2040, 2124; 1.9.8: 2208, 2210, 1009).
- Titles agree with the review's descriptions for: 1723 (Inventory.gfx), 2317 (HUD.gfx), 1309 (random_event.xml), 591, 1323, 1693, 2066, 1883, 1671, 1951, 1647, 1743, 2218, 2294, 1629, 2216, 2276, 2323; DreamMora "KCD I" ports (2191, 2196, 2199, 2206); MayDayU1A UI series (2103, 2108, 2147).

## 3. Errors and gaps found

| # | Where | Finding | Suggested fix |
|---|---|---|---|
| 1 | README, limit 3 | 2372 and 2381 are listed as never looked up; titles are now known (Trough Washing Animation; Nest of Vipers Stealth). 2366, 2367, 2369, 2371, 2384 are still unresolved | Add titles; keep the other five as unresolved |
| 2 | `comparison.md` s.4, PTF examples | Missing PTF-titled mods: 1860, 1861, 1862, 1863, 1864, 1893, 2005, 2021 | Add to the list |
| 3 | `comparison.md` s.4, Archery | 2035 "Ordinance an Archery Overhaul" is a direct comparable for Immersive Archery but is not listed | Add next to 1678 and 2040 |
| 4 | `fixed.md` candidates | Not considered: 1782 (elbow clipping) and 2343 (horse caparison fix) look like vanilla defects; 2279 "Immersive Economy FIXED" is probably a fix of another mod; 1991 is a patch for another mod. Applies only if they are in the lists | Add 1782 and 2343 as candidates; add 2279 and 1991 to "Not candidates" |
| 5 | `comparison.md` s.4, Localization | 2316 (translation of 491), 2256 (translation of 651) and 2374 (translation of 2204) are language variants of the same mod; the cluster lists only 797, 2203, 2204, 808 | Treat each pair as one mod family; add 2374, 2316, 2256 |
| 6 | `comparison.md` s.5, hardware-specific cfg | 1720 "Performance Configuration (Mid-High End)" and 2353 "Ultimate Graphics Adjustment" (and possibly 2106) fit the group with 1972, 2180, 2243, 2153 | Add 1720, 2353 |
| 7 | `comparison.md` s.5, native/version-locked | 2277 "Toggle Hud - KCSE" needs 2244 but is not mentioned | Add 2277 |
| 8 | `comparison.md` s.5 | 1327 (Weather Overhaul) is listed as replacing "a mission file"; the title does not support that | Confirm against the mod's files |
| 9 | `comparison.md` s.6 | Says "Your README also names 1765 and 1419"; the links are in `Requirements.md`, not `README.md` | Correct the file name |
| 10 | `fixed.md` | 1380 "Black Items Fix" is still unresolved (not in the history titles either) | Resolve the page |
| 11 | General | The "Realism & Immersion 2026" collection (nyp4ak) is probably where the lists came from; the review never mentions it | Use it as a cross-check source |

## 4. Still unverified

Nothing here was checked on Nexus or Steam. Mod dates, versions and "likely still needed" statements come from the review's own search summaries and are unconfirmed. Browser-history titles confirm names only.
