# Realistic Potions - where the formula is, what it does, and how to analyse it properly

Status: analysis of the existing work. No rebalance values are proposed here on purpose: the in-game values are
partly designed and partly arbitrary, so the method has to be fixed before the numbers.

Reproduce everything with:

```bash
python tools/potion_dataset.py --game "<KCD folder>" --out docs/potions       # vanilla dataset
python tools/potion_model_check.py --ingredients "Realistic Potions/ingredients.json"   # the existing formula vs vanilla
```

## 1. Where the formula lives today

| File | What it holds |
|---|---|
| `KRS-Items/Data/Tables/item/Potions.md` | Hand notes: ingredients per potion and desired values (Aesop, Amor), plus the lore reasoning ("Belladonna, no charcoal, so it hurts") |
| `KRS-Items/Data/Tables/item/Potions_GPT.md` | A rule-of-thumb table (nourishment, short-term ratio, energy, alcohol, weight, health) and filled sheets for Aesop and Amor |
| `Realistic Potions/build_ingredients_json.py` | Rules that give each herb a contribution `{nutrition, energy, health}` (regex on the herb name) -> `ingredients.json` |
| `Realistic Potions/XmlFilesAnalyzer_auto.py` | The actual formula |
| `Realistic Potions/RealisticPotions_pipeline.md` | A flowchart of the above |

The formula in `XmlFilesAnalyzer_auto.py`, with `fac` = dilution factor of the alchemy base:

```
nutrition = base.nut + sum(herb.nutrition * qty) * base.fac
refresh   = base.ene + sum(herb.energy    * qty) * base.fac
health    = sum(herb.health * qty) * base.fac        # min(health, -5) if a poisonous herb is used without charcoal
ratio     = base.ratio          alcohol = base.alc
base:  Spirits(fac .25, ratio .50, alc 10, nut 3, ene 4)   Wine(.35, .30, 7, 4, 4)
       Water (fac .50, ratio .15, alc 0, nut 0, ene 0)     Oil (.30, .15, 0, 0, 0)
```

## 2. Technical state

- **The script does not run.** `alchemy_base.ui_name` is `ui_nm_alchemySpiritus`, the script strips `ui_nm_alchemy_`
  (with an underscore), so the base name is wrong and the run ends with `KeyError: 'Ui_nm_alchemywine'`. The names also
  differ (`Spiritus`, not `Spirits`).
- **It writes columns that do not exist.** The vanilla `food` table has `refresh_benefit` (not `energy_benefit`) and no
  `weight`; weight and price live in `pickable_item`. Even if it ran, the output would not be a valid patch.
- **`build_ingredients_json.py`** reads `Realistic Potions/ingredients.json` relative to the current folder and
  hard-codes `E:\...\Mods WIP folder\Tables\Tables`. `ingredients.json` has 17 entries; of the 22 ingredients that recipes
  use, 15 are covered and only **6 have a non-zero contribution**, so the herb term is almost always zero and the result
  is essentially the four base constants.
- **`Potions_GPT.md` quotes some vanilla values wrongly.** Example: Aesop alcohol "10 (vanilla)"; the table says 30.

## 3. What the vanilla data says (61 food rows of type 3, from `Tables.pak`)

| Group | Count |
|---|---:|
| Alchemy products (have a recipe) | 35 |
| ...consumable potions (`max_status` > 1) | 30 |
| ...placeholders (`max_status` 0/1: Abortion, Tideness, Dandelion syrup, Dementia, Fake blood) | 5 |
| Other drinks and props (beer, wine, mead, quest and test items) | 26 |

Findings that matter for the design:

1. **The potion rows are mostly a template.** 12 of 30 consumable potions have exactly nutrition 5 / refresh 4; 15 have
   short-term ratio 0.5 and 10 have 0.1. Only a handful were tuned by hand.
2. **The food columns mirror the potion's buff for the designed potions.** Potion -> buff is `consumable_item`
   -> `buff.params`:

   | Potion | food row | buff params |
   |---|---|---|
   | Water of Life | health 100 | `health+100/t` |
   | Long heal potion | health 200 | `health+200/t` |
   | Marigold decoction | health 30 | `health+30/t` |
   | Poison | health -50, nutrition/refresh -10 | `poi=1,health-50/t` |
   | Bane potion | health -110, nutrition/refresh -20 | `poi=1,LimitRun,health-110/t` |
   | Sleeping potion | refresh -100 | `exhaust-100/s` |

   The real identity of a potion is its buff (`weapon_bow+5`, `vis*1.5,owl+1`, `cha+5`, ...), not the food row.
3. **Alcohol is a 0-100 game scale, not percent.** Wine-based potions are all 20, water/oil 0, spirits 0 to 90, and
   `respec_potion` carries 303 (a hack). Beer is 15, mead 50, wine 40. The engine gives the number a meaning:
   `AlcoholContentFPAntidoteThreshold = 60` - food above 60 acts against food poisoning.
4. **`poisonous` is an in-game flag, not pharmacology.** `herb.poisonous` is true for Paris, Plevelium, Urtica
   (nettle), Atropa (belladonna) and Hyoscyamus (henbane). Nettle is not poisonous in real life, and only two potions
   (Poison, Bane) are harmful to health in vanilla even though 13 of the 30 use a flagged herb.
5. **Health is not an "ingredient sum" in vanilla.** It is 0 for most potions, and a tuned number for a few.

## 4. What the existing formula would do to the 30 potions (`tools/potion_model_check.py`)

| Column | Changed | Mean delta | Largest deltas |
|---|---:|---:|---|
| nutrition | 29/30 | -2.5 | Spirits 20 -> 3; Digestive -20 -> 3 |
| refresh | 23/30 | +1.6 | Sleeping potion -100 -> 0 |
| health | 21/30 | -7.7 | Long heal +200 -> 0; Water of Life +100 -> +5; Poison -50 -> -5; Bane -110 -> -5 |
| alcohol | 13/30 | -16.8 | `respec_potion` 303 -> 10; Spirits 90 -> 10 |
| short-term ratio | 28/29 | -0.1 | Spirits 0.63 -> 0.5 |

The "poisonous herb without charcoal" rule triggers on 11 potions, including Nighthawk, Remedium Savegamium (the
save-game potion), Marigold decoction (a healing potion, flagged only because of nettle) and Witch potion.

Consequences:

- **It overwrites designed values with a template.** Poison and Bane stop being deadly; the healing potions stop
  healing in their food row while the buff still says `health+100/t` - the two would disagree.
- **The alcohol scale is wrong.** Using IRL percentages (Spirits 10, Wine 7) turns the 0-100 game scale into a different
  unit, and Spirits (90) would lose the above-60 antidote effect.
- **Nutrition becomes ~0 for water and oil potions** (vanilla 5), which changes how filling every common potion is.
- Neither the ingredient term nor the lore (for example Aesop being poisonous) can be told apart from the base
  constants, because the ingredient data is mostly zero.

## 5. What is subjective, and what is not

| Input | Evidence class | Comment |
|---|---|---|
| Recipe, base (Aqua/Vinum/Oleum/Spiritus), quantities | **A. game fact** | in the tables |
| Herb effect text, buff params, `poisonous` flag | **A. game fact** | the in-game design intent; wins when it disagrees with real life |
| Real-life pharmacology of a herb (belladonna toxic, charcoal adsorbs) | **B. external knowledge** | needs a cited source per rule; the game's fiction is already a simplified version |
| Per-base constants (`fac`, `nut`, `ene`, `ratio`, `alc`, weight) | **C. arbitrary** | no derivation exists in the repo; `fac` in particular has no meaning in the engine |
| Magnitudes of herb contributions (+1 energy, -10 health, ...) | **C. arbitrary** | same |
| The rule "poisonous without charcoal -> at most -5 HP" | **B + C** | a lore rule with an invented number |

Real life only enters through class B, and every class B rule needs a stated source. Class C numbers should come from the game's own
scale (the vanilla ranges in section 3), not from real-life units.

## 6. Method for a proper analysis *(proposed)*

1. **Scope.** Rebalance only potions whose food row is the template (nutrition 5, refresh 4, health 0). Leave rows that are
   mirrored by a buff (section 3.2), quest/test items (`respec_potion`, `Tournament quest poison potion`, `Test Potion:`
   rows) and placeholders alone.
2. **Express every change as a bounded delta from vanilla** (for example nutrition +-3, health within +-10), never as a new
   absolute value, so a formula error cannot create a Poison or a Water of Life.
3. **Units from the game.** Convert with the engine's own constants: `FoodFull` 100, `FoodOverEat` 120, `DigestionSpeed`,
   `ShortTermNutritionDigestionSpeedMultiplier`, `AlcoholContentFPAntidoteThreshold` 60, and the 0-100 alcohol scale.
   Work out what one nutrition point costs in stomach and time before choosing a magnitude.
4. **One rule = one cited reason.** Each rule names its evidence class (A in-game text / B external, with the source /
   C balance) and the potions it touches. The Aesop reasoning in `Potions.md` is a good template for the lore side.
5. **Make the pipeline reproducible:** fix the base-name mapping, write `refresh_benefit` only, never `weight`, read
   `docs/potions/potion_dataset.csv`, and emit rows with only the changed columns.
6. **Acceptance checks** run on every build: no designed potion changes sign or magnitude; buff and food row agree;
   alcohol stays on the vanilla scale; a diff report (vanilla -> new) is attached to the changelog.
7. **In-game spot check** of three potions (one template, one tuned, one poison) before publishing.

## 7. Not covered here

- No in-game measurement of how the numbers feel, and no simulation of the digestion mechanics.
- No researched real-life sources: this needs a short reference list (belladonna and henbane toxicity, activated charcoal
  adsorption, ethanol content of period spirits and wine) before any class B rule is accepted.
- The buff side (what each buff really does for how long) is listed in `potion_dataset.csv` but not analysed.
