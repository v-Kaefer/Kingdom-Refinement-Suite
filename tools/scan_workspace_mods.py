#!/usr/bin/env python3
"""
scan_workspace_mods.py - list the mods that physically exist in the workspace, by Nexus id.

    python tools/scan_workspace_mods.py [--wip "E:/Kingdom-Refinement-Suite/WIP_Mods"]

Sources (the id is the number in Nexus's download names, e.g. `Bed Comfort Restored-480-1-0`):
    * every file or folder in the category folders of `Mods WIP folder` (Archery, Etc, Items, Perks, Player, QoL, Tables,
      User Interface, Installed to be verified), two levels deep; the replica `KingdomComeDeliverance` is skipped
    * the mods Vortex deployed into the replica (`Mods/vortex.deployment.json`)
Writes docs/mods-review/workspace_mods.csv (id, name, where). Mods whose names carry no id (loose .pak files) are listed in the
`unnamed` section of the console output so they can be identified by hand.
"""
import argparse
import csv
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paths  # noqa: E402

ROOT = paths.ROOT
ID_IN_NAME = re.compile(r"^(?P<name>.+?)[-_ ]+(?P<id>\d{2,4})-(?:\d+|-)")


def parse(name):
    stem = re.sub(r"\.(zip|7z|7zip|rar|pak|lua|md)$", "", name, flags=re.I)
    m = ID_IN_NAME.match(stem)
    return (m.group("name").strip(" -_."), int(m.group("id"))) if m else (None, None)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--wip", default=r"E:\Kingdom-Refinement-Suite\WIP_Mods")
    a = ap.parse_args()
    rows, unnamed = {}, []

    def add(i, name, where):
        rows.setdefault(i, {"id": i, "name": name, "where": []})["where"].append(where)

    for cat in sorted(os.listdir(a.wip)):
        top = os.path.join(a.wip, cat)
        if cat in ("KingdomComeDeliverance", "new_mods_review") or not os.path.isdir(top):
            continue
        for entry in sorted(os.listdir(top)):
            name, i = parse(entry)
            if i:
                add(i, name, f"{cat}/{entry}")
            elif re.search(r"\.(zip|7z|7zip|rar|pak)$", entry, re.I) or os.path.isdir(os.path.join(top, entry)):
                unnamed.append(f"{cat}/{entry}")

    dep = os.path.join(a.wip, "KingdomComeDeliverance", "Mods", "vortex.deployment.json")
    if os.path.exists(dep):
        seen = set()
        for f in json.load(open(dep, encoding="utf-8"))["files"]:
            if f["source"] in seen:
                continue
            seen.add(f["source"])
            name, i = parse(f["source"])
            if i:
                add(i, name, f"installed in the test game via Vortex (Mods/{f['target']})")

    out = os.path.join(paths.MODS_REVIEW, "workspace_mods.csv")
    with open(out, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["id", "name", "where"])
        for i in sorted(rows):
            w.writerow([i, rows[i]["name"], " | ".join(rows[i]["where"])])
    print(f"{len(rows)} mods with a Nexus id written to {os.path.relpath(out, ROOT)}")
    print("without an id in the name (identify by hand):")
    for u in unnamed:
        print("  ", u)


if __name__ == "__main__":
    sys.exit(main())
