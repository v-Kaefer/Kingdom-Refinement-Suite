#!/usr/bin/env python3
"""
perk_balance.py - join Perkaholic's perks with the effects they grant, for the balance review.

    python tools/perk_balance.py

Reads the already-extracted 1009 (.rar) patch of the Perks workbench and the unmodified game
tables, and writes <workbench>/notes/perkaholic_balance.json:

  new_perks      every perk the mod adds, with the buff params it grants and, when the perk is a
                 higher tier of an existing one, the value it replaces (perk_buff_override)
  changed_perks  perks of the game whose row the mod rewrites
  changed_buffs  effects of the game whose row the mod rewrites, with the vanilla value beside it
  overrides      the raw perk_buff_override rows

No archive is opened here: the workbench copy is read as plain files.
"""
import argparse
import collections
import json
import os
import re
import sys
import xml.etree.ElementTree as ET

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paths  # noqa: E402
import vanilla  # noqa: E402

WORKBENCH = r"E:\Kingdom-Refinement-Suite\Mods WIP folder\Perks\perkaholic-riposte-workbench"
PATCH = os.path.join("extracted", "1009_perkaholic-ptf_rar", "_pak", "Libs", "Tables", "rpg")
SK = {"23": "Armas de haste", "18": "Arco", "24": "Desarmado", "17": "Machado", "21": "Maça",
      "15": "Defesa", "2": "Esgrima", "": "Atributo / geral"}


def rows(folder, name):
    raw = open(os.path.join(folder, name), encoding="utf-8").read()
    t = ET.fromstring(re.sub(r"^\s*<\?xml[^>]*\?>", "", raw).strip()).find("table")
    return [dict(r.attrib) for r in t.findall("./rows/row")]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--workbench", default=WORKBENCH)
    ap.add_argument("--game", default=vanilla.DEFAULT_GAME)
    args = ap.parse_args()
    folder = os.path.join(args.workbench, PATCH)

    perks = rows(folder, "perk__perkaholic.xml")
    mod_buffs = rows(folder, "buff__perkaholic.xml")
    pbuff = rows(folder, "perk_buff__perkaholic.xml")
    over = rows(folder, "perk_buff_override__perkaholic.xml")

    _, vp = vanilla.load("rpg/perk", game=args.game)
    van_perk = {r["perk_id"]: r for r in vp}
    _, vb = vanilla.load("rpg/buff", game=args.game)
    van_buff = {r["buff_id"]: r for r in vb}

    buff = {b["buff_id"]: b for b in mod_buffs}          # the mod's value wins where both exist
    for b in vb:
        buff.setdefault(b["buff_id"], b)

    link = collections.defaultdict(list)
    for r in pbuff:
        link[r["perk_id"]].append(r["buff_id"])
    # a perk that is a higher tier carries an override: source is the tier below, target is its own
    replaces = collections.defaultdict(list)
    for o in over:
        replaces[o["perk_id"]].append((o["source_buff_id"], o["target_buff_id"]))

    def params(bid):
        return (buff.get(bid) or {}).get("params", "")

    new_perks, changed_perks = [], []
    for p in perks:
        bids = list(link.get(p["perk_id"], []))
        for _src, tgt in replaces.get(p["perk_id"], []):
            if tgt not in bids:                          # an override can be the only link
                bids.append(tgt)
        effects = [{"buff_id": b, "buff_name": (buff.get(b) or {}).get("buff_name", ""),
                    "params": params(b), "new_buff": b in buff and b not in van_buff}
                   for b in bids if buff.get(b)]
        steps = [{"from_buff": (buff.get(s) or {}).get("buff_name", ""), "from": params(s),
                  "to_buff": (buff.get(t) or {}).get("buff_name", ""), "to": params(t)}
                 for s, t in replaces.get(p["perk_id"], [])]
        item = {"perk_id": p["perk_id"], "name": p.get("perk_name", ""),
                "skill": SK.get(p.get("skill_selector", ""), p.get("skill_selector", "")),
                "level": p.get("level", ""), "effects": effects, "replaces": steps}
        if p["perk_id"] in van_perk:
            v = van_perk[p["perk_id"]]
            item["was"] = {k: v.get(k, "") for k in ("perk_name", "level", "perk_ui_desc")}
            changed_perks.append(item)
        else:
            new_perks.append(item)

    changed_buffs = []
    for b in mod_buffs:
        v = van_buff.get(b["buff_id"])
        if not v:
            continue
        diff = {k: [v.get(k, ""), b.get(k, "")] for k in v if str(b.get(k, "")) != str(v.get(k, ""))}
        if diff:
            changed_buffs.append({"buff_id": b["buff_id"], "name": b.get("buff_name", ""),
                                  "diff": diff})

    out = {"new_perks": new_perks, "changed_perks": changed_perks, "changed_buffs": changed_buffs,
           "overrides": over}
    dest = os.path.join(args.workbench, "notes", "perkaholic_balance.json")
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    with open(dest, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=1, ensure_ascii=False)
    tiers = sum(1 for p in new_perks if p["replaces"])
    print(f"{len(new_perks)} perks novos ({tiers} são upgrade de outro), "
          f"{len(changed_perks)} perks alterados, {len(changed_buffs)} efeitos alterados")
    print("wrote", dest)
    return 0


if __name__ == "__main__":
    sys.exit(main())
