#!/usr/bin/env python3
"""
params_runtime_csv.py - turn a harness log into the reference table of rpg constants as the running game reports them.

    python tools/harness/params_runtime_csv.py --log docs/tests/logs/run_full_api_stats_constants.log --game "<KCD folder>" \
        --params-ref "Params Reference.md" --out docs/engine/rpg_constants_runtime.csv

Columns: key, runtime value, exists in the engine, present in the vanilla rpg_param table (and its value),
present in Params Reference.md (and its section).
"""
import argparse
import csv
import os
import re
import xml.etree.ElementTree as ET
import zipfile


def read_member(z, zi):
    try:
        return z.open(zi).read()
    except zipfile.BadZipFile:
        zi.orig_filename = zi.filename.replace("/", "\\")
        return z.open(zi).read()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--log", required=True)
    ap.add_argument("--game", required=True)
    ap.add_argument("--params-ref", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()

    text = open(a.log, encoding="utf-8", errors="replace").read()
    missing = set(re.findall(r"no such rpg constant '([^']+)'", text))
    vals = {}
    for line in text.split("\n"):
        m = re.match(r"KRS_HARNESS CONST (\S+) = (.*)$", line)
        if m:
            vals[m.group(1)] = m.group(2).strip()

    z = zipfile.ZipFile(os.path.join(a.game, "Data", "Tables.pak"))
    root = ET.fromstring(re.sub(r"^\s*<\?xml[^>]*\?>", "", read_member(z, z.getinfo("Libs/Tables/rpg/rpg_param.xml")).decode("utf-8", "replace")))
    vanilla = {r.get("rpg_param_key"): r.get("rpg_param_value") for r in root.iter("row")}

    ref, section, sec = set(), {}, None
    for line in open(a.params_ref, encoding="utf-8", errors="replace"):
        h = re.match(r"^##\s*-*\s*([^-]+?)\s*-*\s*$", line)
        if h:
            sec = h.group(1).strip()
        m = re.match(r"^([A-Z][a-z0-9]+(?:[A-Z][A-Za-z0-9]*)+)\b", line)
        if m:
            ref.add(m.group(1))
            section.setdefault(m.group(1), sec)

    os.makedirs(os.path.dirname(a.out) or ".", exist_ok=True)
    n_exist = n_hidden = 0
    with open(a.out, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["key", "runtime_value", "exists_in_engine", "in_vanilla_rpg_param", "vanilla_table_value",
                    "in_params_reference", "params_reference_section"])
        for k in sorted(vals):
            exists = k not in missing and vals[k] != "nil"
            n_exist += exists
            n_hidden += exists and k not in vanilla
            w.writerow([k, vals[k] if exists else "", "yes" if exists else "NO", "yes" if k in vanilla else "",
                        vanilla.get(k, ""), "yes" if k in ref else "", section.get(k, "")])
    print(f"{len(vals)} keys tested: {n_exist} exist ({n_hidden} hidden = not in the vanilla table), {len(vals) - n_exist} do not exist")


if __name__ == "__main__":
    main()
