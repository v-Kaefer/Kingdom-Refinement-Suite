#!/usr/bin/env python3
"""
potion_dataset.py - join the vanilla alchemy tables into one reproducible dataset.

Reads the vanilla tables straight from the game's Tables.pak and Localization/English_xml.pak and writes
    <out>/potion_dataset.csv      one line per potion/drink in the vanilla `food` table (food_type_id 3)
    <out>/ingredient_dataset.csv  one line per herb/ingredient used by a recipe

Nothing is guessed: every column is a vanilla value, a join of vanilla values, or a count derived from them.
The analysis (docs/modules/potions/ANALYSIS.md) and any rebalance formula must start from this file.

    python tools/potion_dataset.py --game "E:/Kingdom-Refinement-Suite/Mods WIP folder/KingdomComeDeliverance" \
                                   --out docs/modules/potions
"""
import argparse
import collections
import csv
import os
import re
import xml.etree.ElementTree as ET
import zipfile


def read_member(z, zi):
    try:
        return z.open(zi).read()
    except zipfile.BadZipFile:  # KCD paks keep backslash names in the local headers
        zi.orig_filename = zi.filename.replace("/", "\\")
        return z.open(zi).read()


def parse(data):
    text = re.sub(r"^\s*<\?xml[^>]*\?>", "", data.decode("utf-8", "replace"))
    return ET.fromstring(text)


def load_tables(game):
    z = zipfile.ZipFile(os.path.join(game, "Data", "Tables.pak"))
    out = {}
    for zi in z.infolist():
        n = zi.filename
        if (n.lower().startswith("libs/tables/item/") or n.lower() == "libs/tables/rpg/buff.xml") and n.lower().endswith(".xml"):
            t = parse(read_member(z, zi)).find("table")
            out[t.get("name")] = [dict(r.attrib) for r in t.findall("./rows/row")]
    return out


def load_text(game):
    z = zipfile.ZipFile(os.path.join(game, "Localization", "English_xml.pak"))
    text = {}
    for zi in z.infolist():
        if zi.filename.endswith(".xml"):
            try:
                root = parse(read_member(z, zi))
            except ET.ParseError:
                continue
            for row in root.iter("Row"):
                c = [x.text or "" for x in row.findall("Cell")]
                if len(c) >= 2:
                    text[c[0]] = c[1]
    return text


def num(v, default=""):
    try:
        f = float(v)
        return int(f) if f == int(f) else f
    except (TypeError, ValueError):
        return default


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", required=True)
    ap.add_argument("--out", default="docs/modules/potions")
    a = ap.parse_args()

    T = load_tables(a.game)
    text = load_text(a.game)
    item = {r["item_id"]: r for r in T["item"]}
    food = {r["item_id"]: r for r in T["food"]}
    herb = {r["item_id"]: r for r in T["herb"]}
    bases = {r["item_id"]: re.sub(r"^ui_nm_alchemy", "", r["ui_name"]) for r in T["alchemy_base"]}
    buffs = {r["buff_id"]: r for r in T["buff"]}
    item_buff = {r["item_id"]: r["buff_id"] for r in T["consumable_item"]}
    recipe_by_product = {}
    for r in T["recipe"]:
        recipe_by_product[r["product_item_id"]] = r
    ing = collections.defaultdict(list)
    for r in T["recipe_ingredient"]:
        ing[r["recipe_id"]].append(r)

    def nm(iid):
        return item.get(iid, {}).get("item_name", iid[:8])

    os.makedirs(a.out, exist_ok=True)

    # ingredient dataset ------------------------------------------------------------------------
    uses = collections.Counter()
    for rid, lst in ing.items():
        for r in lst:
            uses[r["item_id"]] += 1
    with open(os.path.join(a.out, "ingredient_dataset.csv"), "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["item_id", "name", "is_herb", "poisonous", "element1", "element2", "recipes_using", "in_game_effect_text"])
        for iid, n in sorted(uses.items(), key=lambda x: nm(x[0])):
            h = herb.get(iid)
            eff = text.get(h["ui_effect"], "") if h else ""
            w.writerow([iid, nm(iid), bool(h), (h or {}).get("poisonous", ""), (h or {}).get("element1_id", ""),
                        (h or {}).get("element2_id", ""), n, eff])

    # potion dataset ------------------------------------------------------------------------------
    cols = ["item_id", "name", "has_recipe", "recipe_id", "base", "n_ingredient_kinds", "n_ingredient_units",
            "n_poisonous_kinds", "ingredients", "food_subtype_id", "alcohol_content", "nutrition_benefit",
            "refresh_benefit", "health_benefit", "short_term_ratio", "max_status", "decay_time_hours", "buff_name",
            "buff_params"]
    rows = []
    for iid, f in food.items():
        if f.get("food_type_id") != "3":
            continue
        r = recipe_by_product.get(iid)
        lst = ing.get(r["recipe_id"], []) if r else []
        pk = sum(1 for x in lst if herb.get(x["item_id"], {}).get("poisonous") == "True")
        rows.append([iid, nm(iid), bool(r), r["recipe_id"] if r else "", bases.get(r["base_material_id"], "") if r else "",
                     len(lst), sum(int(x.get("quantity", 1)) for x in lst), pk,
                     "; ".join(f"{nm(x['item_id'])} x{x.get('quantity', 1)}" for x in lst),
                     f.get("food_subtype_id", ""), num(f.get("alcohol_content")), num(f.get("nutrition_benefit")),
                     num(f.get("refresh_benefit")), num(f.get("health_benefit")),
                     num(f.get("short_term_nutrition_benefit_ratio")), num(f.get("max_status")),
                     num(f.get("decay_time_hours")),
                     buffs.get(item_buff.get(iid, ""), {}).get("buff_name", ""),
                     buffs.get(item_buff.get(iid, ""), {}).get("params", "")])
    rows.sort(key=lambda r: (not r[2], r[4], r[1]))
    with open(os.path.join(a.out, "potion_dataset.csv"), "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(cols)
        w.writerows(rows)
    print(f"wrote {len(rows)} potions/drinks and {len(uses)} ingredients to {a.out}")


if __name__ == "__main__":
    main()
