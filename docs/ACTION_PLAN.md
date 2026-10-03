# Kingdom Refinement Suite - action plan

Status date: 2 Oct 2026. Plan for turning the repo into shippable, tested, Vortex-installable mods. It is ordered by
dependency: nothing in phase 1 or later is worth building until phase 0 makes packaged files actually load.

Effort: S = about half a day, M = 1-2 days, L = several days. Branches follow `docs/OBJECTIVES.md`
(`krs-items`, `krs-qol`, `krs-perks`, `krs-bow`; docs and tools live on `develop`).

## Progress (2 Oct 2026, phases 0-3 executed)

| Phase | State | Evidence |
|---|---|---|
| 0 Packaging | **Done** except 0.5 (branches) | `tools/build_module.py`, `tools/gate.py`, `tools/seed_modules.py`; modules under `modules/`; `docs/tests/gate_*.log` |
| 1 Perks | Built; menu-stage checks pass, perk rows pending a player-stage run | `modules/krs_perks`, `gate_krs_items_krs_perks_krs_qol_tables.log` |
| 2 Items | Built; 66 rows + 5 constants read back in game; sleeping spots pending (level table) | `modules/krs_items`, `gate_krs_items_tables.log` |
| 3 QoL | Built; 3 rpg_param rows read back; override/skill2item rows pending (level tables); repair limits left open | `modules/krs_qol` |

Open because the player stage needs someone to press Continue in the test instance (screen access was not granted
while the author was away): perk rows, `sleeping_spot_type`, `perk_rpg_param_override`, `skill2item_category`, 4.1 bow
live-read. Command for that run: `python tools/gate.py krs_items krs_perks krs_qol --mode full`, then press Continue.
Decisions taken by default (change if wrong): separate mods; Enhanced Eyes left out of the modules; repairs in QoL,
price x2 only; Riposte shipped as `krs_perks` with an "enable only one of them" note.

## What changed the plan (verified in game, `docs/tests/PTF_FINDINGS.md`)

1. Patch files are applied only when their suffix equals the mod id. As packaged today, **no KRS table patch loads**.
2. Rows must be complete and the later mod's row replaces the earlier row entirely.
3. A `.pak` must be a ZIP; the draft `KRS-Items.pak` is 7z.
4. Hidden constants can be set by a plain `rpg_param` row and, at run time, by `RPG.<Key> = value`; 588 constants exist
   (406 hidden), 9 documented ones do not.
5. A test harness can start the game, read tables and constants back, and quit, so every phase below has an automatic gate.

## Phase 0 - make packaging correct (blocks everything) - M

| # | Task | Done when |
|---|---|---|
| 0.1 | Decide module ids: `krs_items`, `krs_qol`, `krs_perks`, `krs_bow` (lowercase and underscore only); set `<modid>` in each `mod.manifest` | `check_patch_names.py` reports no id problem |
| 0.2 | Rename every patch file and inner table name to `table__<modid>` (for example `rpg_param__krs_items.xml`); delete the empty `item.xml` and the `WIP Base` copies from module folders | checker reports 0 problems on all module folders |
| 0.3 | `tools/build_module.py`: source tree (`Data/Libs/Tables/...`, `Localization/...`) to `Data/<id>.pak` (ZIP, deflate) + `mod.manifest`, and a Vortex-ready archive (`<id>/mod.manifest`, `<id>/Data/<id>.pak`). Runs checker, audit and ownership check first and fails on any problem | one command produces an installable archive per module |
| 0.4 | Gate script: build the module, run `harness` in `tables` mode with that module, assert the engine printed `Table ... is patched by ...` for every file and the values read back equal `ownership.csv` targets | gate passes for a module before anything is committed to its branch |
| 0.5 | Branches: merge `develop` docs and tools into each module branch; module sources live under `KRS-<Module>/src/`; the game replica stays ignored; stop tracking generated and scratch files | each branch builds from a clean clone |
| 0.6 | Localization patches: Riposte uses `Localization/<Language>_xml.pak` with `text__<modid>.xml` (the engine logs `Loading localization patch`). The Timed Quest Indicator on `develop` uses `Data/Tables/ui/text_*__KRSPKG1.xml`, which is probably the wrong mechanism: confirm with the harness and fix | one translated quest line shows in game |

Decisions needed before 0.1: one mod or several (recommended: several), Enhanced Eyes out of the suite (recommended: link, do
not ship), repairs in QoL or Items, Perkaholic as a requirement.

## Phase 1 - KRS-Perks - S/M

- Riposte: perk `ec4c5274` level 10 and visible, Master Strike `61e98757` restored, as complete rows in `perk__krs_perks.xml`;
  the four localization paks as ZIP with `text__krs_perks.xml`. Mod id differs from upstream, so the Riposte mod must not be
  enabled at the same time (document it as an incompatibility, or ship as an edit of the upstream mod with permission).
- Test: `perk` and `buff` tables only load with a level, so the gate needs the player stage (see 7.2) or a manual
  check of the perk screen.
- Done when: perk visible at level 10 in game, no duplicate or missing text.

## Phase 2 - KRS-Items - M

- Contents: book reading time (x2.5) and `ReadingXpPerHour` (one owner: Items), sleeping spots, digestion and starvation.
- Resolve the open numbers (reading XP 5 or 10) and delete the duplicate `document` copy in `KingdomRefinementSuite`.
- Test: gate in `tables` mode (values read back) plus a short play test: sleep, eat, read a book, check hunger rate
  over one in-game day.
- Done when: gate passes and the play test notes are in `docs/tests/`.

## Phase 3 - KRS-QoL - M

- Herb radius (0.35), carry capacity (`StrengthToInventoryCapacity`, permission pending), repairs (decision: placement and
  values; remember the `perk_rpg_param_override` values are Hardcore-mode only), Timed Quest Indicator text (EN, CZ, PT).
- Remove the stray `perk_id` rows from `rpg_param`, fix the single-underscore `skill2item_category` name.
- Permission tracking: Realistic Repairs, Train More Carry More, Timed Quest Indicator (`docs/OBJECTIVES.md` section 6).
- Done when: gate passes; bridles are repairable in game.

## Phase 4 - bow mod (branch `krs-bow`) - L

| # | Task | Done when |
|---|---|---|
| 4.1 | **Live-read test**: with a loaded save, draw a bow after `RPG.AimSpreadMax = 40` and after `RPG.BowChargeDurationMax = 40`; also the capacity test in the harness. Two ways: a person does the 5-minute test from `docs/bow/FEASIBILITY.md` section 6, or the player stage of the harness (7.2) | answer recorded in `docs/tests/` |
| 4.2 | If live: prototype as a script-only mod (`Scripts/Startup/`, entity with `OnUpdate`, no Cheat mod) that computes spread, stamina cost and draw time from `GetStatLevel('str'/'agi')` and writes the constants; log values every second | values follow the stats in the log |
| 4.3 | Design the formula in a table (inputs, ranges, outputs) with the real constants from `rpg_constants_runtime.csv`; decide how to handle NPC archers (global constants) | formula table reviewed |
| 4.4 | Find the Lua accessor for the held bow's weight (`player.human:GetItemInHand(0)` returns a handle; resolve it to an item and its weight) or drop the weight input | decision recorded |
| 4.5 | If not live: ship the static version (`rpg_param__krs_bow.xml`, hidden keys) and document that it is not stat-dependent | module builds and passes the gate |
| 4.6 | Package: ZIP pak, mod id `krs_bow`, no dependency on other mods; test together with the common archery mods (Immersive Archery, Persistent Arrows) | no row or constant conflicts in the audit |

## Phase 5 - potions (module `krs_potions`, optional) - L

1. Approve the light-touch method (`docs/potions/ANALYSIS.md` section 6, `SOURCES.md`).
2. Fix the pipeline: base-name mapping, only `refresh_benefit`, complete rows, deltas bounded from vanilla values.
3. Write the rule table (each rule: in-game text it builds on, optional real-world "can help with" note, potions touched,
   delta). Use the 12 template potions first; leave designed potions (Poison, Bane, Water of Life, ...) untouched.
4. Generate rows, run the model check (no designed potion changes), audit overlaps with Food Spoil Faster and
   PotionNoSatietyAndHealEnergy (`tools/audit_tables.py`). Since the later mod wins whole rows, ship as a separate optional
   mod and document the load order.
5. Gate in `tables` mode, then spot-check three potions in game.

## Phase 6 - release and upkeep - M

- README per module (what it changes, dependencies, conflicts), changelog, Nexus text; Vortex archive per module; versions
  and `<supports>` verified (the manifest claims 1.9.4-1.9.6.x, the tests ran on 1.9.6).
- Compatibility matrix: run the gate with the commonly used mods enabled (Perkaholic, Realistic Repairs, Food Spoil Faster,
  Riposte) and keep the "Table ... is patched by" output and the audit as the report.
- Keep `docs/ownership.csv` and `docs/table-audit/TABLE_AUDIT.md` updated in every commit.

## Cross-cutting: test automation (7)

| # | Task | Value |
|---|---|---|
| 7.1 | Wrap the harness as `tools/gate.ps1 <module>`: build, install into a scratch `Mods`, run `tables` mode, assert, uninstall, restore `mod_order.txt` | one command per module |
| 7.2 | Player stage: in the test instance the game stays at the main menu. Options: automate the "Continue" click with computer control (needs your approval of screen access), pass a start argument if one exists, or accept a manual step. Needed for perks, buffs, stats and the bow | in-level tests become repeatable |
| 7.3 | Save safety: the harness never saves; keep a copy of the replica's profile before the first player-stage run | no risk to saves |
| 7.4 | Vortex: the harness mods are not Vortex-managed and are removed after each run; the final archives must install through Vortex without touching `mod_order.txt` by hand | tested on a Vortex profile |

## Risks

| Risk | Mitigation |
|---|---|
| The bow reads constants only once (not live) | static version (4.5); the parameter route still gives a faster/slower draw for everyone |
| Another mod patches the same rows | audit and gate list every overlap; ship fragile parts as optional mods; document load order |
| Published Nexus files differ from the repo | compare with the downloaded archive before replacing anything |
| Permissions (Realistic Repairs, Train More Carry More, Enhanced Eyes) | track in `OBJECTIVES.md` section 6; do not ship files without a yes |
| Patch rules change in a game update | the harness re-checks them in minutes (`PTF_FINDINGS.md` section 4) |

## Suggested order for the next two weeks

1. Phase 0.1 to 0.4 (unblocks everything) and the decisions above.
2. Phase 1 (Perks) as the first module through the gate end to end.
3. 7.2 and 4.1 (the player stage and the live-read test), because the bow and Perks both need it.
4. Phase 2, then Phase 3; Phase 4 and 5 in parallel branches once their gates exist.
