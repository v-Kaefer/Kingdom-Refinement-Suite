| 71 IDs with no usable result | Listed with reasons in [unverified.md](unverified.md) |

## Files

| File | What it is |
|---|---|
| [catalog.md](catalog.md) | The 130 identified mods grouped into 15 main categories, with method, files touched, description and verdict |
| [comparison.md](comparison.md) | Slop vs substance, overlap clusters, conflict groups, KRS alignment, improvement opportunities |
| [fixed.md](fixed.md) | Fix-type mods that *might* be obsolete, why none is confirmed, how to check |
| [unverified.md](unverified.md) | The 71 IDs that could not be identified, with the reason for each |
| [mods.csv](mods.csv) | The full dataset behind the catalog (one row per ID, including unresolved ones) |

## Limits

1. **Nexus Mods and Steam are blocked in this environment.** Fetching `www.nexusmods.com` and `store.steampowered.com` returned an egress-policy denial, and the proxy documentation says not to work around that. So no mod page, file list or changelog was opened, and the official patch notes could not be read.
2. **Everything comes from web-search summaries.** Search can return a mod's title and a short description, but not its file list. Because of that, "which `.pak` it changes" is stated only where the page text names a path (for example `Libs\UI\Inventory.gfx`, `camerashake.lua`, `random_event.xml`, `Data\_fastload`) and is otherwise inferred from behaviour.
3. **Search was capped at 200 queries.** 7 IDs (2366, 2367, 2369, 2371, 2372, 2381, 2384) were never looked up.
4. **A page was accepted only if a returned URL matched `/kingdomcomedeliverance/mods/<id>` with a title.** Many IDs also exist on the Deliverance II site, and the summarizer sometimes invented an answer (for example it called 1131 "Playable Daggers", which is really 1689). Those answers were rejected and the ID went to [unverified.md](unverified.md). The rule was applied to every row; 1093 (Fishing in Bohemia), 1900 and 2359 are kept as title-only rows marked *Unverified*.
5. **Verdicts are opinions on evidence that is thin.** "Slop-risk" means concrete warning signs on the page (see [comparison.md](comparison.md)), not a finding that the author's work is bad.

## What was deduplicated

209 links across your two files became 201 unique IDs:

- Repeated inside `mods_to_verify.txt`: 2021, 2174, 2175, 2191, 2206, 2348.
- In both files: 1330, 1337.

Your second file (`Kingdom_Come_Mods.txt`) is headed "Working 1.9.6". Those mods are marked † in the catalog and in the CSV column `in_your_tested_1.9.6_list`.

## Legend

**Install method** (taken from page text where possible):

| Code | Meaning |
|---|---|
| PTF | Self-described PTF: a partial table file that carries only the changed rows. KRS's own `Data/perk__riposte.xml` is this shape (two perk rows, not the whole perk table). Two mod pages expand PTF as "Patched Table Files"; one says "Packed Table File". The expansion is unconfirmed, and the behaviour is the same in all descriptions |
| STD | Standard Mods-folder mod with a `mod.manifest`; the pak/loose layout inside was **not** inspected |
| LEG | Legacy install: copy a `.pak` into `Data\` and `Data\_fastload` (one mod, 754) |
| LUA | Replaces a vanilla Lua file loose (one mod, 1332) |
| CFG | `user.cfg` / `autoexec.cfg` / `system.cfg` console variables |
| RSH | ReShade or ENB preset, runs through an external injector |
| KCSE | Needs the Kingdom Come Script Extender (2244) |
| ASI | Needs Ultimate ASI Loader (native plugin) |
| DEV | Needs the game started in dev mode (958) |
| EXT / REF | Runs outside the game / nothing is installed into the game |

**Files touched:** **(S)** = the page states it, **(I)** = I inferred it from the described behaviour, **(?)** = unknown. Typical KCD1 data packs (to confirm against your install): `Tables.pak` (XML tables such as perk, item, rpg_param), `Scripts.pak` (Lua), `Libs.pak` (UI `.gfx`, AI and quest XML), `Localization\*_xml.pak` (per-language text). Only `Scripts.pak` appears in the KRS README; the rest is from general KCD modding knowledge.

**Verdict:**

| Verdict | Meaning |
|---|---|
| Substantive | Changes one clear thing, explains how, and the approach looks sound from the description |
| Mixed | Useful but with a flagged concern: overlap, scope creep, whole-file replacement, conflict-prone, hardware-specific, or beta |
| Slop-risk | Concrete warning signs: lore-breaking novelty, unverifiable claims, borrowed values |
| Tool/Reference | Not a gameplay mod (framework, tool, spreadsheet, modder reference) |
| Unverified | Name known, nothing else |

## Closing the gaps

To make the "which pak" column real, the mod archives have to be opened. A quick procedure, once you have them (it mirrors what your README already does with 7-Zip):

1. `7z l <archive>`: note whether the mod ships `Data/*.pak`, `Mods/<id>/Data/*.pak`, or loose `Libs/`, `Scripts/`, `Localization/` folders.
2. Read `mod.manifest`: `supports` versions, `modid`, `modifies_level`.
3. `7z l` each inner `.pak` and record the entry paths. Two mods that contain the same path conflict.
4. PTF check: files named `<table>__<suffix>.xml` that contain only changed rows.
5. For anything flagged "whole-file" in the catalog (1309, 1327, 2333, 1723, 2317), diff the shipped file against vanilla to see how many rows really changed.

Alternatively, allow `www.nexusmods.com` in the environment's network policy and the file lists can be read directly.