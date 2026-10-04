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
| 6 | Download what is missing | the links are in `downloads_missing.csv`; run step 2 again afterwards | open |
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

## Decisions for the author (step 5)

1. Delete the three `(1)` copies, or leave them? (Left in place by default.)
2. Copy the five batch-0 archives from the Vortex download folder into the review folder, so one folder holds everything? (A copy only; not done.)
3. The 29 batch-2 mods still missing are mostly swords and armor (P3). Download them, or drop them from the list?
4. The five "not in the index" ids: add them to the index (they were downloaded, so someone wanted them), or treat them as wrong links?
