# Status

> **Status date:** 2026-10-03 | **Kind:** project | **Trust:** derived | **Game version:** 1.9.6 and 1.9.8

The only file that is edited every session. Stable goals are in `OBJECTIVES.md`, the plan in `ROADMAP.md`, decisions in `DECISIONS.md`, what the engine does in `../engine/`.

## Now

- **Game:** the test install is 1.9.8. The three modules pass the menu-stage gate on 1.9.8 (73/73) and on 1.9.6.
- **Manifests:** list 1.9.6 to 1.9.8; the engine disables mods whose list lacks the running version, and editing the line is enough to load them (`../engine/game-versions.md`).
- **Docs:** reorganized (`DOCS_PLAN.md`); `../../CHANGELOG.md` has the full history.
- **Not verified:** rows of level-only tables (perks, sleeping spots, overrides, `skill2item_category`) and the bow live-read; both need the Continue button in the test game, and on 1.9.8 possibly the new EULA screen.
- **Waiting for the author:** answers in `DECISIONS.md` (open decisions), the missing links for the mod lists, permission replies (`PERMISSIONS.md`), whether to push `dev` and PR #1.

## Progress of phases 0-3 (2 Oct 2026)

| Phase | State | Evidence |
|---|---|---|
| 0 Packaging | **Done** except 0.5 (branches) | `tools/build_module.py`, `tools/gate.py`, `tools/seed_modules.py`; modules under `modules/`; `docs/tests/logs/gate_*.log` |
| 1 Perks | Built; menu-stage checks pass, perk rows pending a player-stage run | `modules/krs_perks`, `gate_krs_items_krs_perks_krs_qol_tables.log` |
| 2 Items | Built; 66 rows + 5 constants read back in game; sleeping spots pending (level table) | `modules/krs_items`, `gate_krs_items_tables.log` |
| 3 QoL | Built; 3 rpg_param rows read back; override/skill2item rows pending (level tables); repair limits left open | `modules/krs_qol` |

Open because the player stage needs someone to press Continue in the test instance (screen access was not granted
while the author was away): perk rows, `sleeping_spot_type`, `perk_rpg_param_override`, `skill2item_category`, 4.1 bow
live-read. Command for that run: `python tools/gate.py krs_items krs_perks krs_qol --mode full`, then press Continue.
Decisions taken by default (change if wrong): separate mods; Enhanced Eyes left out of the modules; repairs in QoL,
price x2 only; Riposte shipped as `krs_perks` with an "enable only one of them" note.


## Snapshot of the first audit (2 Oct 2026, historical)

Most of these findings were resolved by phases 0-3 (repackaged modules under `modules/`). Kept as written for the record.


| Finding | Detail |
|---|---|
| **None of the suite's table patches is applied by the game as packaged today** | `KRS-Items` has mod id `krs_items` but patch suffix `KRS-items`; `KingdomRefinementSuite` has id `kingdom_refinement_suite` but suffix `KRS`; the draft `Para publicar (TEMP)/Data/KRS-Items.pak` is a 7z file, which the game cannot open. The same `KRS-Items` files with the suffix renamed to the id were applied and read back correctly in game (`docs/engine/ptf-rules.md`). The Nexus release may differ |
| Items is the only module with real files | `KRS-Items/Data`: 56 book rows, 5 `rpg_param` rows, 4 sleeping-spot rows, 1 potion row that differs from vanilla |
| Potion rebalance is mostly placeholders (and its pipeline cannot run) | `food__KRS-items.xml` has 34 rows; 33 equal vanilla. Only Aesop Potion differs (nutrition 10 -> 2.5, ratio 0.1 -> 0.5). Planned values live in `Potions_GPT.md`. The formula script crashes and the formula would overwrite designed potions: see `docs/modules/potions/ANALYSIS.md` |
| Possible clash with installed mods | All 34 food rows overlap *Food Spoil Faster* (`decay_time_hours`), 22 overlap *PotionNoSatietyAndHealEnergy*. Measured in game: the later mod's row replaces the whole row, so the clash is real and load order decides who wins (`docs/engine/ptf-rules.md`, rule 6) |
| Reading is set three times | `ReadingXpPerHour`: vanilla 20, `KRS-Items` 5, `KingdomRefinementSuite` 10 (Skill Books Take Time: 10). The 56 book rows are duplicated in `KingdomRefinementSuite` |
| Repairs: four variants, none consistent | The `perk_rpg_param_override` values (vanilla 0.5 / 0.7 / 0.9) belong to the pseudo-perk **"Hardcore Mode - Constants"**, so they only apply in Hardcore mode; normal mode uses the global `rpg_param` (`RepairPriceModif` 0.65). Realistic Repairs sets 0.1 / 0.6 / 1.2, dev branch 0.2 / 0.7 / 1.3. README says "prices doubled" and level-20 repairs down to 20 % |
| Stray `perk_id` in `rpg_param` | `KingdomRefinementSuite/.../rpg_param__KRS.xml` (also in Realistic Repairs itself) puts perk rows in the wrong table. Effect unverified |
| Riposte differs from upstream and vanilla | Vs vanilla: perk `ec4c5274` level 5 -> 10, visibility 0 -> 2; Master Strike perk `61e98757` restored. Upstream (Restore Riposte) used level 8 |
| Riposte file is in the wrong folder | `Data/perk__riposte.xml`; the game reads `Data/Libs/Tables/rpg/perk__riposte.xml` (as the upstream mod ships it) |
| Dangerous empty files | `KRS-Items/Data/Tables/item/item.xml` is an empty full-replace of `item` (would drop 2214 rows if packed); `WIP Base/.../armor.xml` likewise for `armor` |
| Single-underscore table name | `skill2item_category_krspkg1` (also in Realistic Repairs); PTF names use `__`. Effect unverified |
| 9 no-op rows | "Possible variables for my bow mod" in `rpg_param__KRS.xml` equal vanilla |
| Hidden params | Many keys (`DigestionSpeed`, `StrengthToInventoryCapacity`, ...) are not in the vanilla table; their real default comes from the game binary (`Params Reference.md` describes them, with no values) |

