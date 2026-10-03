#!/usr/bin/env python3
"""
build_gate.py - install KRS modules into a KCD folder together with the test mod `krs_gate`.

    python tools/harness/build_gate.py --game "<KCD folder>" --dist dist krs_items krs_perks [--mode tables|full]

1. copies dist/<id>/ to <game>/Mods/<id>/ for every module (what Vortex would do),
2. reads every patch row of the module sources (modules/<id>/Data/Libs/Tables/**) and writes the Lua check list
   that tools/harness/krs_gate.lua runs in game: every column of every row must read back as in the patch file,
   and every rpg_param row must read back through RPG.<key>,
3. builds <game>/Mods/krs_gate (startup script + spawned entity) that runs the checks and quits the game.

Remove with:  python tools/harness/build_gate.py --game "<KCD folder>" --remove krs_items krs_perks
"""
import argparse
import os
import re
import shutil
import sys
import xml.etree.ElementTree as ET

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
from build_harness import write_mod  # noqa: E402

KEYS = {
    "rpg_param": ["rpg_param_key"],
    "sleeping_spot_type": ["sleeping_spot_type_id"],
    "document": ["item_id"],
    "food": ["item_id"],
    "perk": ["perk_id"],
    "perk_rpg_param_override": ["perk_id", "rpg_param_key"],
    "skill2item_category": ["item_category", "skill_id"],
    "buff": ["buff_id"],
    "item": ["item_id"],
}


def lua_str(s):
    return '"' + str(s).replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n") + '"'


def patch_rows(mod_id):
    base = os.path.join(ROOT, "modules", mod_id, "Data", "Libs", "Tables")
    for dp, _, fn in os.walk(base):
        for f in sorted(fn):
            if not f.endswith(".xml"):
                continue
            table = f.split("__")[0]
            raw = open(os.path.join(dp, f), encoding="utf-8").read()
            t = ET.fromstring(re.sub(r"^\s*<\?xml[^>]*\?>", "", raw)).find("table")
            for r in t.findall("./rows/row"):
                yield mod_id, table, dict(r.attrib)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", required=True)
    ap.add_argument("--dist", default=os.path.join(ROOT, "dist"))
    ap.add_argument("--mode", choices=["tables", "full"], default="tables")
    ap.add_argument("--remove", action="store_true")
    ap.add_argument("--extra-lua", help="Lua file appended to the harness (defines KRS.extra_player ...)")
    ap.add_argument("modules", nargs="+")
    a = ap.parse_args()

    mods_dir = os.path.join(a.game, "Mods")
    if a.remove:
        for m in a.modules + ["krs_gate"]:
            shutil.rmtree(os.path.join(mods_dir, m), ignore_errors=True)
        print("removed", ", ".join(a.modules + ["krs_gate"]))
        return 0

    rows, consts = [], []
    for m in a.modules:
        src = os.path.join(a.dist, m)
        if not os.path.isdir(src):
            raise SystemExit(f"{src} is missing: run tools/build_module.py {m} first")
        target = os.path.join(mods_dir, m)
        shutil.rmtree(target, ignore_errors=True)
        shutil.copytree(src, target)
        for mod_id, table, row in patch_rows(m):
            keys = KEYS.get(table)
            if not keys:
                raise SystemExit(f"no key columns known for table {table}; add it to KEYS in build_gate.py")
            label = f"{mod_id} {table} " + "/".join(row.get(k, "") for k in keys)
            rows.append((label, table, keys, row))
            if table == "rpg_param":
                consts.append((row["rpg_param_key"], row["rpg_param_value"]))

    out = ['KRS = { mode = "%s", keys = {}, food_checks = {} }' % a.mode, "KRS.gate_rows = {"]
    for label, table, keys, row in rows:
        k = ", ".join("{%s, %s}" % (lua_str(c), lua_str(row.get(c, ""))) for c in keys)
        w = ", ".join("[%s] = %s" % (lua_str(c), lua_str(v)) for c, v in row.items())
        out.append("  { label = %s, table = %s, keys = {%s}, want = {%s} }," % (lua_str(label), lua_str(table), k, w))
    out += ["}", "KRS.gate_consts = {"]
    out += ["  { key = %s, want = %s }," % (lua_str(k), lua_str(v)) for k, v in consts]
    out += ["}"]
    lua = "\n".join(out) + "\n" + open(os.path.join(HERE, "krs_harness.lua"), encoding="utf-8").read() + "\n" \
        + open(os.path.join(HERE, "krs_gate.lua"), encoding="utf-8").read()
    if a.extra_lua:
        lua += "\n" + open(a.extra_lua, encoding="utf-8").read()
    files = {
        "Scripts/Startup/krs_gate.lua": lua,
        "Scripts/Entities/KRSHarness.lua": open(os.path.join(HERE, "krs_harness_entity.lua"), encoding="utf-8").read(),
        "Entities/KRSHarness.ent": '<Entity\n        Name="KRSHarness"\n        Script="Scripts/Entities/KRSHarness.lua"\n/>\n',
    }
    write_mod(a.game, "krs_gate", "krs_gate", "KRS Gate", files)
    print(f"{len(rows)} row checks, {len(consts)} constant checks for {', '.join(a.modules)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
