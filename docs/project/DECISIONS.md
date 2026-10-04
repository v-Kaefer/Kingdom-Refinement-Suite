# Decisions

> **Status date:** 2026-10-03 | **Kind:** project | **Trust:** derived | **Game version:** -

Log of decisions and open questions. Newest first. A decision taken by default while the author was away says so and can be reversed.

## Log

| Date | Decision | Why | By |
|---|---|---|---|
| 2026-10-03 | Docs reorganized as in `DOCS_PLAN.md`; the root files of the main checkout (`README.md`, `Requirements.md`, `CONTRIBUTING.md`, `FOLLOW_UP.md`) and `Mods WIP folder` are left untouched; legacy docs are copied into `../archive/legacy/` | the author's main checkout has uncommitted edits there | default (author away) |
| 2026-10-04 | Downloaded archives may be extracted to a scratch folder to be read, then the folder is deleted; nothing from them is run, installed or loaded by the game. An archive with a HIGH finding (native code, scripts, dangerous Lua, path traversal, encrypted entries) is moved to `_quarantine/` (a move, undoable), not deleted, and documented in `docs/mods-review/QUARANTINE.md` | the author: possible viruses, read the code only; 6 archives moved on the first pass | author |
| 2026-10-03 | Personal API keys (Nexus) are not handled by the sessions: a key pasted into the chat was not used. Metadata is fetched by `tools/nexus_metadata.py`, run by the author with the key in an environment variable; no tool in the repository downloads mod files | credentials rule; the key in the transcript should be revoked and a new one created | author's key, session declined |
| 2026-10-03 | All test logs are kept (moved to `tests/logs/`); nothing trimmed | no deletion without a request | default |
| 2026-10-03 | Module manifests list 1.9.6, 1.9.7, 1.9.8 | the 1.9.8 engine disables a mod whose list lacks the running version (`../engine/game-versions.md`) | default |
| 2026-10-02 | Separate modules `krs_items`, `krs_perks`, `krs_qol`; Enhanced Eyes left out; repairs in QoL (price x2 only); Riposte shipped as `krs_perks` | recommendations in the plan, author said to proceed | default |
| 2026-10-02 | Potions are a light touch on top of the base game | author's clarification | author |

## Open decisions (as listed on 2 Oct 2026)

1. One combined mod or three separate ones? *(proposed: separate, plus an optional bundle later)*
2. Repairs: Items or QoL, and which values? *(proposed: QoL as one unit including bridles; values: author)*
3. Enhanced Eyes: link as a requirement unless Grimsy agrees to redistribution? *(proposed: yes)*
4. Perkaholic: require it, or copy parts? *(proposed: require)*
5. Reading: keep XP 5 with books x2.5, or XP 10 as in the other copies? *(Items currently says 5)*
6. ~~May a module repeat unchanged columns in a row?~~ **Answered in game:** rows must be complete (a partial row blanks the
   other columns) and the later mod's row replaces the earlier one entirely, so overlapping mods undo each other.
7. Is `Libs/Tables/...` loose, or packed into `Data/<module>.pak`? *(proposed: pack)*
8. Where do the bow mechanics live (KRS-QoL, KRS-Perks, or a new archery module)? They need the in-game test in
   `docs/modules/bow/FEASIBILITY.md` first.
9. Potions: approve the method in `docs/modules/potions/ANALYSIS.md` section 6 (scope, bounded deltas, cited rules) before any
   number is chosen.

