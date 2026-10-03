#!/usr/bin/env python3
"""
build_mods_index.py - merge the author's mod lists with the review annotations into one table.

    python tools/build_mods_index.py            writes docs/mods-review/mods_index.csv and prints the counts

Inputs (docs/mods-review/):
    sources/mods_to_verify.txt        the long list of Nexus links to verify (repeats are kept in the count)
    sources/tested_1.9.6_list.txt     the author's "working on 1.9.6" list; the label after "N)" is the author's own name for the mod
    annotations.csv                   one row per mod the review documents say something about (hand-maintained)
    workspace_mods.csv                mods found in the workspace and the Vortex deployment (tools/scan_workspace_mods.py)

When a list changes, copy it over the file in sources/ and run this again. IDs without an annotation stay in the index with an
empty review column, so the table shows what still has to be looked at.
"""
import collections
import csv
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paths  # noqa: E402

D = paths.MODS_REVIEW
ID = re.compile(r"nexusmods\.com/kingdomcomedeliverance/mods/(\d+)")


def read_lists():
    verify = collections.Counter()
    for line in open(os.path.join(D, "sources", "mods_to_verify.txt"), encoding="utf-8", errors="replace"):
        m = ID.search(line)
        if m:
            verify[int(m.group(1))] += 1
    tested, label = collections.OrderedDict(), {}
    lines = open(os.path.join(D, "sources", "tested_1.9.6_list.txt"), encoding="utf-8", errors="replace").read().splitlines()
    for i, line in enumerate(lines):
        m = re.match(r"\[\]\s*\d+\)\s*(.+)$", line)
        if m and i + 1 < len(lines):
            u = ID.search(lines[i + 1])
            if u:
                tested[int(u.group(1))] = True
                label[int(u.group(1))] = m.group(1).strip()
    return verify, tested, label


def main():
    verify, tested, label = read_lists()
    ann = {int(r["id"]): r for r in csv.DictReader(open(os.path.join(D, "annotations.csv"), encoding="utf-8", newline=""))}
    wpath = os.path.join(D, "workspace_mods.csv")
    work = {int(r["id"]): r for r in csv.DictReader(open(wpath, encoding="utf-8", newline=""))} if os.path.exists(wpath) else {}
    ids = sorted(set(verify) | set(tested) | set(ann) | set(work))
    cols = ["id", "url", "in_mods_to_verify", "times_in_verify_list", "in_tested_1.9.6_list", "in_workspace", "author_label", "name",
            "name_source", "author_or_series", "versions", "install", "krs_area", "fix_status", "check_1.9.8", "check_source",
            "observation", "scope", "review_coverage"]
    out = os.path.join(D, "mods_index.csv")
    in_lists = [i for i in ids if i in verify or i in tested]
    with open(out, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(cols)
        for i in ids:
            a = ann.get(i, {})
            listed = i in verify or i in tested
            scope = "in the author's lists" if listed else ("workspace/installed only" if i in work else "found while checking (outside the lists)")
            cover = "described in review" if a else "no text in the review files"
            w.writerow([i, f"https://www.nexusmods.com/kingdomcomedeliverance/mods/{i}", "yes" if i in verify else "",
                        verify.get(i, ""), "yes" if i in tested else "", work.get(i, {}).get("where", ""), label.get(i, ""),
                        a.get("name") or work.get(i, {}).get("name", ""), a.get("name_source") or ("workspace file name" if i in work else ""),
                        a.get("author_or_series", ""), a.get("versions", ""), a.get("install", ""), a.get("krs_area", ""),
                        a.get("fix_status", ""), a.get("check_1.9.8", ""), a.get("check_source", ""), a.get("observation", ""),
                        scope, cover])
    dup = sorted(i for i, n in verify.items() if n > 1)
    both = sorted(set(verify) & set(tested))
    print(f"links in mods_to_verify.txt: {sum(verify.values())}; unique ids: {len(verify)}; repeated inside it: {dup}")
    print(f"tested list: {len(tested)} ids; in both lists: {both}")
    print(f"unique ids across both lists: {len(in_lists)}")
    print(f"with review text: {sum(1 for i in in_lists if i in ann)}; without: {sum(1 for i in in_lists if i not in ann)}")
    only_ws = sorted(i for i in work if i not in in_lists)
    print(f"workspace/installed mods not in the lists: {len(only_ws)} {only_ws}")
    print(f"annotated ids outside the lists and the workspace: {sorted(i for i in ann if i not in in_lists and i not in work)}")
    print("checked against 1.9.8:", sum(1 for i in ann if ann[i].get('check_1.9.8')))
    print(f"total rows: {len(ids)}")
    print("wrote", os.path.relpath(out, ROOT))


if __name__ == "__main__":
    sys.exit(main())
