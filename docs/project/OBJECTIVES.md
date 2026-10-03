# Kingdom Refinement Suite - Objectives and Ownership

> **Status date:** 2026-10-03 | **Kind:** project | **Trust:** proposal (draft for the author to correct) | **Game version:** 1.9.6 target, 1.9.8 supported

**Status: DRAFT for the author to correct.** Nothing in the repo stated the objectives in one place, so this file
rebuilds them from `README.md`, `Requirements.md`, `CONTRIBUTING.md`, `FOLLOW_UP.md`, the `*_Mod_Mapping.md` files
and the actual table contents. Lines marked *(proposed)* are recommendations, not decisions.

## 1. Goal

> "A curated set of non-intrusive PTF tweaks to polish your journey through Bohemia."
> (`README.md`, `mod.manifest`)

- Target: Kingdom Come: Deliverance 1.9.6 (the manifest also claims 1.9.4, 1.9.5 and 1.9.6.x - untested here).
- PTF = table patches (`table__suffix.xml`) that add or override rows instead of replacing whole tables.
- **Hidden parameters are central to the suite.** Many keys exist only inside the engine (`AimSpreadMax`-style
  constants; `Params Reference.md`) and can still be set by a PTF `rpg_param` row or, at run time, by Lua
  (`RPG.<Key> = value`). What is proven and what is not is in `docs/modules/bow/FEASIBILITY.md`.

## 2. Principles *(proposed)*

1. **Patch only.** Ship `__suffix` table patches. A file named exactly like a vanilla table (`rpg_param.xml`,
   `armor.xml`, ...) replaces the whole table and is not allowed in a module.
2. **One owner per row.** Every table row or parameter the suite changes is listed in `docs/data/ownership.csv` with
   exactly one module. Two modules never set the same key.
3. **Only changed rows.** No placeholder rows that repeat vanilla values: if rows are merged as whole rows, they
   can undo another mod's change (see section 5, food).
4. **Independent modules.** Each module has its own `mod.manifest`/`modid` and works alone.
5. **No third-party bytes without permission.** If permission is missing, link the mod as a requirement.
6. **Scripts and assets stay out of the gameplay modules** until proven (Lua experiments, meshes, textures).
7. **Follow the engine's patch rules** (measured in game, `docs/engine/ptf-rules.md`): the patch file suffix equals the
   mod id (lowercase letters and underscore only), every row lists every column, a `.pak` is a ZIP, and when two mods
   patch the same row the later one wins whole. `tools/check_patch_names.py` checks the first three.
8. **Potions: light touch.** Keep the base game's values and fantasy; make small adjustments that add a little real-world
   plausibility ("can help with", known risks). See `docs/modules/potions/ANALYSIS.md`.

## 3. Modules

| Module | In scope (target) | Source ideas |
|---|---|---|
| **KRS-Items** | Sleeping spots, nourishment / digestion / starvation, potion and food values, book reading time and XP | Realistic Items 1.1.x, Bed Comfort Restored, Skill Books Take Time, Potions.md |
| **KRS-QoL** | Herb radius, carry capacity, repairs *(placement undecided)*, Timed Quest Indicator text (EN/CZ/PT) | hoskope_hgrx2, Train More Carry More, Realistic Repairs, Timed Quest Indicator |
| **KRS-Perks** | Riposte at level 10 (Master Strike restored); Perkaholic is a *requirement*, not copied | Restore Riposte (1765), Perkaholic |
| Outside the suite | Hoods, "more historically accurate item stats", Realistic Horses, Enhanced Eyes | cosmetic or intrusive (`CONTRIBUTING.md`: cosmetic mods stay out of gameplay modules) |

**Where the module code lives (since phases 0-3):** `modules/<id>/` with ids `krs_items`, `krs_qol`, `krs_perks`
(`krs_bow` and `krs_potions` come later). Build with `python tools/build_module.py --all` (output in `dist/`, ignored by git),
test in game with `python tools/gate.py <ids>`. The old folders `KRS-Items/`, `KingdomRefinementSuite/` of the main branch are
the legacy sources (see `tools/seed_modules.py` for how they were converted). Patch suffix must equal the module id.

Required external mods (`Requirements.md`): EarlyBirdNPC, 30FPSCutsceneFixV2, MGsStayCleanLongerGetDirtyGradually,
Persistentarrows. Table footprint of the ones that were audited: EarlyBird patches `soul` (2390 rows); MGs Stay Clean
patches `FullClothDirtyingOnFullSpeed` in `rpg_param` and `perk_rpg_param_override`. Neither collides with a suite row.

## 4. Ownership: how it is tracked

- `docs/data/ownership.csv` - the claim list: table, key, owning module, vanilla value, target value, status, expected
  folder, source, notes.
- `tools/audit_tables.py` - compares every table patch in the project with the vanilla `Tables.pak` and writes
  `docs/data/table-audit/TABLE_AUDIT.md` (what each mod and each KRS file really changes, parameter conflicts, lint).
- `tools/check_ownership.py` - compares the audit with `ownership.csv` and reports UNOWNED, DUPLICATE, VALUE,
  MISSING, MISPLACED rows and no-op rows. Exit code 1 means the suite is not consistent.

When you change a module:

1. Edit the table file in the module folder.
2. Run the audit, then the checker (commands in section 8).
3. Every changed row must have an `ownership.csv` line. Add or update it in the same commit.
4. Do not mark a line `shipping` until the value is final and tested in game.


## Where the rest went

| Topic | Now in |
|---|---|
| Documents and tools index, commands | `../README.md` |
| Where the suite stands, audit findings | `STATUS.md` |
| Third-party sources and permission | `PERMISSIONS.md` |
| Open decisions | `DECISIONS.md` |
