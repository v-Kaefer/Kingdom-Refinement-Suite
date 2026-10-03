# Kingdom Refinement Suite - Objectives and Ownership

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
  (`RPG.<Key> = value`). What is proven and what is not is in `docs/bow/FEASIBILITY.md`.

## 2. Principles *(proposed)*

1. **Patch only.** Ship `__suffix` table patches. A file named exactly like a vanilla table (`rpg_param.xml`,
   `armor.xml`, ...) replaces the whole table and is not allowed in a module.
2. **One owner per row.** Every table row or parameter the suite changes is listed in `docs/ownership.csv` with
   exactly one module. Two modules never set the same key.
3. **Only changed rows.** No placeholder rows that repeat vanilla values: if rows are merged as whole rows, they
   can undo another mod's change (see section 5, food).
4. **Independent modules.** Each module has its own `mod.manifest`/`modid` and works alone.
5. **No third-party bytes without permission.** If permission is missing, link the mod as a requirement.
6. **Scripts and assets stay out of the gameplay modules** until proven (Lua experiments, meshes, textures).
7. **Follow the engine's patch rules** (measured in game, `docs/tests/PTF_FINDINGS.md`): the patch file suffix equals the
   mod id (lowercase letters and underscore only), every row lists every column, a `.pak` is a ZIP, and when two mods
   patch the same row the later one wins whole. `tools/check_patch_names.py` checks the first three.
8. **Potions: light touch.** Keep the base game's values and fantasy; make small adjustments that add a little real-world
   plausibility ("can help with", known risks). See `docs/potions/ANALYSIS.md`.

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

- `docs/ownership.csv` - the claim list: table, key, owning module, vanilla value, target value, status, expected
  folder, source, notes.
- `tools/audit_tables.py` - compares every table patch in the project with the vanilla `Tables.pak` and writes
  `docs/table-audit/TABLE_AUDIT.md` (what each mod and each KRS file really changes, parameter conflicts, lint).
- `tools/check_ownership.py` - compares the audit with `ownership.csv` and reports UNOWNED, DUPLICATE, VALUE,
  MISSING, MISPLACED rows and no-op rows. Exit code 1 means the suite is not consistent.

When you change a module:

1. Edit the table file in the module folder.
2. Run the audit, then the checker (commands in section 8).
3. Every changed row must have an `ownership.csv` line. Add or update it in the same commit.
4. Do not mark a line `shipping` until the value is final and tested in game.

## Documents and tools in this folder

| File | Purpose |
|---|---|
| `docs/OBJECTIVES.md`, `docs/ownership.csv` | goals, ownership of every changed row |
| `docs/table-audit/TABLE_AUDIT.md` | generated: what each mod really changes versus vanilla |
| `docs/potions/ANALYSIS.md`, `docs/potions/SOURCES.md`, `docs/potions/claims_ledger.csv`, `docs/potions/*_dataset.csv` | potion formula analysis, real-world sources, claim-by-claim comparison, vanilla dataset |
| `docs/bow/FEASIBILITY.md`, `docs/bow/API_CHECK.md` | what Lua and hidden parameters can do for the bow, and which calls exist |
| `tools/audit_tables.py`, `tools/check_ownership.py` | table audit and ownership check |
| `tools/potion_dataset.py`, `tools/potion_model_check.py` | potion dataset and formula check |
| `tools/lua_api_check.py` | checks that the functions and `RPG.<Key>` names in a Lua mod exist |
| `tools/check_patch_names.py` | pre-flight check of patch names, mod ids, row completeness and pak format |
| `docs/tests/PTF_FINDINGS.md`, `docs/tests/run_*.log` | what the game was observed to do (in-game test results) and the raw logs |
| `docs/params/rpg_constants_runtime.csv` | every rpg constant as the running game reports it (588 exist, 406 hidden, 9 do not exist) |
| `tools/harness/` | builds and runs the in-game test mods (`build_harness.py`, `run_game_test.ps1`, ...) |
| `docs/ACTION_PLAN.md` | the plan for the whole project |

## 5. Where the suite stands today (from the audit)

| Finding | Detail |
|---|---|
| **None of the suite's table patches is applied by the game as packaged today** | `KRS-Items` has mod id `krs_items` but patch suffix `KRS-items`; `KingdomRefinementSuite` has id `kingdom_refinement_suite` but suffix `KRS`; the draft `Para publicar (TEMP)/Data/KRS-Items.pak` is a 7z file, which the game cannot open. The same `KRS-Items` files with the suffix renamed to the id were applied and read back correctly in game (`docs/tests/PTF_FINDINGS.md`). The Nexus release may differ |
| Items is the only module with real files | `KRS-Items/Data`: 56 book rows, 5 `rpg_param` rows, 4 sleeping-spot rows, 1 potion row that differs from vanilla |
| Potion rebalance is mostly placeholders (and its pipeline cannot run) | `food__KRS-items.xml` has 34 rows; 33 equal vanilla. Only Aesop Potion differs (nutrition 10 -> 2.5, ratio 0.1 -> 0.5). Planned values live in `Potions_GPT.md`. The formula script crashes and the formula would overwrite designed potions: see `docs/potions/ANALYSIS.md` |
| Possible clash with installed mods | All 34 food rows overlap *Food Spoil Faster* (`decay_time_hours`), 22 overlap *PotionNoSatietyAndHealEnergy*. Measured in game: the later mod's row replaces the whole row, so the clash is real and load order decides who wins (`docs/tests/PTF_FINDINGS.md`, rule 6) |
| Reading is set three times | `ReadingXpPerHour`: vanilla 20, `KRS-Items` 5, `KingdomRefinementSuite` 10 (Skill Books Take Time: 10). The 56 book rows are duplicated in `KingdomRefinementSuite` |
| Repairs: four variants, none consistent | The `perk_rpg_param_override` values (vanilla 0.5 / 0.7 / 0.9) belong to the pseudo-perk **"Hardcore Mode - Constants"**, so they only apply in Hardcore mode; normal mode uses the global `rpg_param` (`RepairPriceModif` 0.65). Realistic Repairs sets 0.1 / 0.6 / 1.2, dev branch 0.2 / 0.7 / 1.3. README says "prices doubled" and level-20 repairs down to 20 % |
| Stray `perk_id` in `rpg_param` | `KingdomRefinementSuite/.../rpg_param__KRS.xml` (also in Realistic Repairs itself) puts perk rows in the wrong table. Effect unverified |
| Riposte differs from upstream and vanilla | Vs vanilla: perk `ec4c5274` level 5 -> 10, visibility 0 -> 2; Master Strike perk `61e98757` restored. Upstream (Restore Riposte) used level 8 |
| Riposte file is in the wrong folder | `Data/perk__riposte.xml`; the game reads `Data/Libs/Tables/rpg/perk__riposte.xml` (as the upstream mod ships it) |
| Dangerous empty files | `KRS-Items/Data/Tables/item/item.xml` is an empty full-replace of `item` (would drop 2214 rows if packed); `WIP Base/.../armor.xml` likewise for `armor` |
| Single-underscore table name | `skill2item_category_krspkg1` (also in Realistic Repairs); PTF names use `__`. Effect unverified |
| 9 no-op rows | "Possible variables for my bow mod" in `rpg_param__KRS.xml` equal vanilla |
| Hidden params | Many keys (`DigestionSpeed`, `StrengthToInventoryCapacity`, ...) are not in the vanilla table; their real default comes from the game binary (`Params Reference.md` describes them, with no values) |

## 6. Third-party sources and permission

Status is copied from the README and is **not verifiable from the repo**.

| Source | Used for | Status in README |
|---|---|---|
| Restore Riposte (AcSiG, 1765) | KRS-Perks | Permission Granted |
| Immersive Archery (1419) | not used by any suite file yet | Permission Granted |
| Realistic Repairs (1842) | repairs | Requested |
| Train More Carry More | carry capacity | Requested |
| Enhanced Eyes (Grimsy, 969) | 28 `.mtl` + 2 `.dds`, byte-identical to the original | Request Permission |
| Bed Comfort Restored (480), Timed Quest Indicator (1780), Skill Books Take Time (1950), Herb Picking Radius (1938) | inspiration or credit | credited, no permission noted |

Non-table assets are not covered by the audit. Track them by hand: the Enhanced Eyes files above are unmodified copies;
the `generic_eye_v01_lashes_diff.dds` texture is no longer referenced by any vanilla material after the `.mtl` changes
(checked for the human head/character materials).

## 7. Open decisions

1. One combined mod or three separate ones? *(proposed: separate, plus an optional bundle later)*
2. Repairs: Items or QoL, and which values? *(proposed: QoL as one unit including bridles; values: author)*
3. Enhanced Eyes: link as a requirement unless Grimsy agrees to redistribution? *(proposed: yes)*
4. Perkaholic: require it, or copy parts? *(proposed: require)*
5. Reading: keep XP 5 with books x2.5, or XP 10 as in the other copies? *(Items currently says 5)*
6. ~~May a module repeat unchanged columns in a row?~~ **Answered in game:** rows must be complete (a partial row blanks the
   other columns) and the later mod's row replaces the earlier one entirely, so overlapping mods undo each other.
7. Is `Libs/Tables/...` loose, or packed into `Data/<module>.pak`? *(proposed: pack)*
8. Where do the bow mechanics live (KRS-QoL, KRS-Perks, or a new archery module)? They need the in-game test in
   `docs/bow/FEASIBILITY.md` first.
9. Potions: approve the method in `docs/potions/ANALYSIS.md` section 6 (scope, bounded deltas, cited rules) before any
   number is chosen.

## 8. Commands

The worktree does not contain the game replica, so point `--root` at the main checkout.

```bash
python tools/audit_tables.py --root "E:/Kingdom-Refinement-Suite" \
    --game "E:/Kingdom-Refinement-Suite/Mods WIP folder/KingdomComeDeliverance" \
    --out docs/table-audit
python tools/check_ownership.py        # sources default to '^modules/'
```

To include another branch, extract it first and pass it as an extra source:

```bash
git archive dev KingdomRefinementSuite | tar -x -C /tmp/dev
python tools/audit_tables.py ... --extra "branch-dev/KingdomRefinementSuite=/tmp/dev/KingdomRefinementSuite"
python tools/check_ownership.py --sources '^(modules/|branch-dev)'
```

Limits of the audit: vanilla is the replica's `Tables.pak` (game version not recorded in the repo); `.7z`/`.rar`
archives and `KRS-Items.pak` in `Para publicar (TEMP)` could not be read; the in-game results are in `docs/tests/` (`PTF_FINDINGS.md`).
