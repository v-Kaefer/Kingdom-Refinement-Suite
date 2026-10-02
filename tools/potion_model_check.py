#!/usr/bin/env python3
"""
potion_model_check.py - evaluate the formula in "Realistic Potions/XmlFilesAnalyzer_auto.py" against vanilla.

The original script cannot run (it maps alchemy_base names with a wrong prefix and crashes with a KeyError), and it
writes columns the vanilla `food` table does not have (`energy_benefit`, `weight`). This tool re-implements the same
arithmetic on top of docs/potions/potion_dataset.csv so the effect of the formula can be inspected before anything
is written into a mod:

    nutrition = base.nut + sum(ingredient.nutrition * qty) * base.fac
    refresh   = base.ene + sum(ingredient.energy    * qty) * base.fac      (script calls it "energy")
    health    = sum(ingredient.health * qty) * base.fac ; if a poisonous herb and no charcoal: min(health, -5)
    ratio     = base.ratio ; alcohol = base.alc

    python tools/potion_model_check.py --dataset docs/potions/potion_dataset.csv \
        --ingredients "Realistic Potions/ingredients.json" [--csv out.csv]
"""
import argparse
import csv
import json
import statistics

# Copied verbatim from XmlFilesAnalyzer_auto.py (keys renamed Spirits -> Spiritus to match alchemy_base).
BASE_TABLE = {
    "Spiritus": {"fac": 0.25, "ratio": 0.50, "alc": 10, "nut": 3, "ene": 4, "weight": 0.25},
    "Wine": {"fac": 0.35, "ratio": 0.30, "alc": 7, "nut": 4, "ene": 4, "weight": 0.40},
    "Water": {"fac": 0.50, "ratio": 0.15, "alc": 0, "nut": 0, "ene": 0, "weight": 0.50},
    "Oil": {"fac": 0.30, "ratio": 0.15, "alc": 0, "nut": 0, "ene": 0, "weight": 0.50},
}


def f(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dataset", default="docs/potions/potion_dataset.csv")
    ap.add_argument("--ingredients", default="Realistic Potions/ingredients.json")
    ap.add_argument("--ingredient-dataset", default="docs/potions/ingredient_dataset.csv")
    ap.add_argument("--csv")
    a = ap.parse_args()

    ING = json.load(open(a.ingredients, encoding="utf-8"))
    ing_name = {r["name"]: r for r in csv.DictReader(open(a.ingredient_dataset, encoding="utf-8"))}
    contrib_by_name = {ing_name[n]["name"]: ING.get(ing_name[n]["item_id"]) for n in ing_name}
    covered = sum(1 for v in contrib_by_name.values() if v is not None)
    nonzero = sum(1 for v in contrib_by_name.values() if v and any(v.values()))
    print(f"ingredients used by recipes: {len(contrib_by_name)}; with an entry in ingredients.json: {covered}; "
          f"with a non-zero entry: {nonzero}")

    out = []
    for r in csv.DictReader(open(a.dataset, encoding="utf-8")):
        if r["has_recipe"] != "True" or r["max_status"] in ("0", "1"):
            continue  # placeholder rows (max_status 0/1) are not consumable potions
        b = BASE_TABLE[r["base"]]
        tot = {"nutrition": 0, "energy": 0, "health": 0}
        charcoal = False
        poisonous = False
        for part in r["ingredients"].split("; "):
            name, _, qty = part.rpartition(" x")
            qty = int(qty or 1)
            c = contrib_by_name.get(name) or {}
            for k in tot:
                tot[k] += c.get(k, 0) * qty
            charcoal |= name.lower() == "charcoal"
            poisonous |= ing_name.get(name, {}).get("poisonous") == "True"
        nut = round(b["nut"] + tot["nutrition"] * b["fac"], 1)
        ref = round(b["ene"] + tot["energy"] * b["fac"])
        hp = round(tot["health"] * b["fac"])
        if poisonous and not charcoal:
            hp = min(hp, -5)
        out.append({
            "name": r["name"], "base": r["base"],
            "nut_v": f(r["nutrition_benefit"]), "nut_m": nut,
            "ref_v": f(r["refresh_benefit"]), "ref_m": ref,
            "hp_v": f(r["health_benefit"]), "hp_m": hp,
            "alc_v": f(r["alcohol_content"]), "alc_m": b["alc"],
            "rat_v": f(r["short_term_ratio"]), "rat_m": b["ratio"],
            "poisonous_no_charcoal": poisonous and not charcoal,
        })

    print(f"\npotions evaluated: {len(out)} (recipe potions with max_status > 1)")
    for k, label in (("nut", "nutrition"), ("ref", "refresh (energy)"), ("hp", "health"), ("alc", "alcohol"), ("rat", "short-term ratio")):
        diffs = [(o[k + "_m"] - o[k + "_v"]) for o in out if o[k + "_v"] is not None]
        changed = sum(1 for d in diffs if abs(d) > 1e-9)
        print(f"{label:18s} changed {changed:2d}/{len(diffs)}   mean delta {statistics.mean(diffs):+7.2f}   "
              f"min {min(diffs):+7.1f}  max {max(diffs):+7.1f}")
    pen = [o["name"] for o in out if o["poisonous_no_charcoal"]]
    print(f"\n'poisonous herb without charcoal' rule triggers on {len(pen)} potions: {', '.join(pen)}")
    print("\nper potion (vanilla -> model): nutrition / refresh / health / alcohol / ratio")
    for o in out:
        print(f"{o['name'][:24]:24s} {o['base'][:7]:7s} {o['nut_v']!s:>5}->{o['nut_m']!s:<5} {o['ref_v']!s:>5}->{o['ref_m']!s:<4} "
              f"{o['hp_v']!s:>5}->{o['hp_m']!s:<5} {o['alc_v']!s:>4}->{o['alc_m']!s:<3} {o['rat_v']!s:>5}->{o['rat_m']!s}")
    if a.csv:
        with open(a.csv, "w", encoding="utf-8", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=list(out[0]))
            w.writeheader()
            w.writerows(out)


if __name__ == "__main__":
    main()
