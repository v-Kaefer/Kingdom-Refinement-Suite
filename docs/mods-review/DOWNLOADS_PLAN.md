# Plan: identify the downloaded mods, find the missing ones, sort them

> **Status date:** 2026-10-04 | **Kind:** plan | **Trust:** the first three steps were carried out on 4 Oct 2026 (names, sizes and hashes only); the rest is not done | **Game version:** 1.9.8

The author downloaded about 200 archives into `Mods WIP folder/Installed_to_review` from the 200 pages opened in two batches (and the earlier pilot). Some links pointed at other mods than listed, so the folder has to be reconciled with the list of what was asked for.

## Safety rule for this stage

The archives are untrusted (the author received malware warnings while downloading). Until the author says otherwise:

- nothing is installed, extracted, opened with Vortex or the game, and nothing inside an archive is listed or run;
- the only things read are **file names, sizes and a SHA-256 of the bytes**; the only change made to the folder is **moving entries into sub-folders** (undoable, nothing deleted);
- `tools/analyze_mod_archives.py` **extracts** archives, so it is **not run** until the author approves it. A safer path for that later step: run Windows Security's custom scan on the folder first, then analyse a copy in a scratch folder (the tool already extracts to `%TEMP%`, writes nothing back and never executes a file).

## Steps

| # | Step | How | State |
|---|---|---|---|
| 1 | What was asked for | `download_batches.csv`: batch 0 (already had), 1 and 2 (tabs opened), 3 (shortlist only), with the shortlist flag | done (212 ids) |
| 2 | What is in the folder | `tools/inventory_downloads.py`: mod id from the Nexus file name (old shape `name-id-version-epoch`, new shape `name id version date hash`); a loose `.pak` is matched by name against the Vortex download folder and the index; the epoch or date in the name gives the upload date | done: `downloads_inventory.csv` |
| 3 | Reconcile | asked-for minus found = missing; found minus asked-for = extras; id not in the index = misleading link; identical SHA-256 = duplicate copy; `.crdownload` = unfinished | done: `DOWNLOADS_STATUS.md`, `downloads_missing.csv` |
| 4 | Sort into sub-folders | `--sort --apply`: `c_<triage category>/`, `_unmatched/`, `_incomplete/`; every move is recorded in `_sort_manifest.csv`, `--undo` puts everything back | done (204 moves) |
| 5 | The author's decisions | see below | open |
| 6 | Download what is missing (30 left) | the links are in `downloads_missing.csv`; run step 2 again afterwards | open |
| 7 | Scan | Windows Security custom scan of the folder, by the author (a scan can quarantine files, so it is the author's call) | open |
| 8 | Read the archives | `tools/analyze_mod_archives.py --src <folder>` (it walks the sub-folders), then `tools/triage_mods.py`; start with batch 0 to 1 and the P1/P2 mods | not before 7 |

## Result of step 3 (4 Oct 2026)

- 204 entries: 189 archives, 9 folders that were already extracted (not opened), 5 loose files, 1 unfinished download. 186 distinct mod ids.
- **Missing: 35 ids.** 5 are batch 0 and sit in the Vortex download folder, not in this folder (83, 1090, 1639, 1743, 2017); 1 is from batch 1 (1084 Overpowered Bows - PTF Edition); 29 are from batch 2, nearly all P3 (swords, armor, maps, fonts) plus 2256, 2280 and 2323 (P2). The list with links is `downloads_missing.csv`.
- **Not in the index (5), likely misleading links:** 660 Apex ENB, 502 CLAM, 611 Dice (`Dice.pak`), 1733 Medieval Poisons, 1807 Poisonous Enemies. All are in `_unmatched/`. Two of them (1733, 1807) look like the originals of the mods the index lists as the "True Hardcore" patches (2208, 2209), so the link or the title was probably mixed up.
- **Downloaded but not asked for (4):** 2273 Address Library For KCSE, 2244 KCSE, 1723 Intimidation Stat, 800 Volumetric Fog Shadows (dependencies and extras; they are sorted by their category).
- **No id (3):** `Exact money display/` (probably 613), `Food Spoil faster/`, `zzz_Clean_Items_In_Trough.pak` (probably 1691): folders and loose files extracted earlier, left in `_unmatched/`.
- **Duplicates by hash (3 pairs):** 651 Better Combat and Immersion Compilation, 491 JCD_LootInfo, 106 cheat, each downloaded twice (`(1)` copy). Nothing was deleted.
- 44 archives carry an upload date after the 1.9.7 patch (13 Feb 2026), read from the file name. That is a hint of freshness, not of compatibility.

## Names against links, and the excluded mods (4 Oct 2026)

The author saw pages of swords, armor, maps and the KCD modding tools in the opened tabs and asked to check the list names against the pages. Result: **no link points at the wrong mod.** The name of every id was compared across all sources (Vivaldi tab, the 290-title list, the author's labels of the "working on 1.9.6" list, search titles) with the Nexus API name: 545 comparisons, 6 differ, and all 6 are the author's short labels (`sorting mod` for 797 Inventoried, `no mo slo mo` for 284, `richer merchants` for 1460, `lost weapon pack` for 1566) or a longer page title (1131 removed, 2079). The archive file names against the page names of the 190 downloaded ids showed no mismatch either. So there was no link to remove; the pages are the right ones for the ids, but the mods are **not wanted**: 11 come from the "working out of the box" list (already in use), 4 are older or similar versions of mods already in use, the rest are models, maps and tools.

The 20 are in [`excluded_mods.csv`](excluded_mods.csv) (1416, 1386, 1374, 1281, 1203, 1182, 1089, 958, 942, 915, 913, 905, 891, 864, 827, 795, 791, 762, 708, 129). The triage puts them at P4 "Excluded by the author", the archives shortlist skips them and `tools/inventory_downloads.py` never reports them as missing. **No page of them is opened again.** My own selection rule was the cause: batches 2 and 3 were filled in triage order, which reaches P3/P4 (models, maps, HUD, reshades, tools) after the 129 P2 mods. **All P2 mods have been asked for; no further batch will be filled by triage order.** More pages are opened only from a list the author gives.

## Decisions of the author (step 5, answered 4 Oct 2026)

1. **Duplicates:** the three `(1)` copies were deleted (after checking again that their SHA-256 equals the original; they went to the Recycle Bin, not removed permanently).
2. **Batch 0:** copied from the Vortex download folder into the review folder (a copy; the Vortex originals are untouched): 83, 1090, 1639, 1743 and two archives of 2017. Note: the Vortex files of 2017 are named `KRS-Items-2017-...` (2.6 and 2.7 KB), not "Realistic Items"; the id and the name do not agree and the contents were not looked at.
3. **Missing batch 2 (29) and 1084:** open (30 ids in `downloads_missing.csv`).
4. **Ids not in the index:** listed in `DOWNLOADS_STATUS.md` (6 ids: 502 CLAM, 611 Dice, 660 Apex ENB, 1691 Clean Items In Trough, 1733 Medieval Poisons, 1807 Poisonous Enemies); not yet added to the index.
