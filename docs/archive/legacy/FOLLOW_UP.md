# Follow-Up Notes

Date: 2026-05-18

## Session Resume

Resume code: `KRS-RESUME-20260518-01`

Use this token to continue the folder-by-folder mapping work from the `Mods WIP folder` tree.

## Verified Objective

The repo is a Kingdom Come Deliverance mod suite named **Kingdom Refinement Suite**.
The stated goal is to ship a curated set of non-intrusive PTF tweaks, with the work
currently centered on:

- `KRS-Items` for item, food, sleep, and RPG parameter changes.
- `Realistic Potions` for potion ingredient analysis and generated table patches.
- `KRS-Perks` and `KRS-QoL` as planned modules, now backed by a clearer set of source mods in the WIP folders.

## What Was Completed Today

- Created `FOLLOW_UP.md` at the repo root to capture objective, limits, and research gaps.
- Mapped `Mods WIP folder\Etc` into `Etc_Mod_Mapping.md`.
- Mapped `Mods WIP folder\Items` into `Items_Mod_Mapping.md`.
- Mapped `Mods WIP folder\Player` into `Player_Mod_Mapping.md`.
- Mapped `Mods WIP folder\QoL` into `QoL_Mod_Mapping.md`.
- Mapped `Mods WIP folder\Perks` into `Perks_Mod_Mapping.md`.
- Documented `Mods WIP folder\Tables` as the shared vanilla source workspace in `Tables_Mod_Mapping.md`.

## What I Can Do From This Repo

- Verify the repo layout and identify which folders are active modules versus WIP/reference material.
- Read and summarize the current mod intent from `README.md`, `Requirements.md`, and module manifests.
- Trace the item-module data flow from source notes into generated XML outputs.
- Inspect the potion pipeline scripts and document what they generate.
- Build folder-level mappings for extracted source mods and mark each one as confirmed or inferred.
- Create or update follow-up notes like this one for future work tracking.

## What I Cannot Verify Locally

- In-game behavior, balance, or stability changes.
- Whether the generated `.pak` or XML outputs are correct without running the full KCD mod packaging and game test loop.
- Whether all external mod references are still valid or permitted for reuse.
- Whether the final intended merge policy for `KRS-Perks` and `KRS-QoL` is correct without a human decision on overlap handling.

## What Needs More Research

- The real vanilla extraction/source path expected by the `Realistic Potions` scripts.
- Whether the hardcoded paths in `Realistic Potions/*.py` match the current workspace layout.
- The intended final merge policy for `KRS-Perks` and `KRS-QoL` when multiple overlapping source mods exist.
- Compatibility assumptions around the target KCD version and mod interop.
- Validation of generated XML against the actual game tables and pack format.
- Whether the `.rar` and `.7z` archives in WIP folders should be unpacked in place or mirrored into per-mod staging folders first.

## Current Working Assumptions

- `KRS-Items` is the most complete shipped module in this repo snapshot.
- `Realistic Potions` is a derivation/generation pipeline, not a finalized packaged mod by itself.
- Folder-level markdown maps are the preferred working record for source-mod discovery before integration.
- The worktree was already dirty when inspected, so existing modifications and untracked files should be treated as pre-existing state unless explicitly changed.

