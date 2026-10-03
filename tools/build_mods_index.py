#!/usr/bin/env python3
"""
build_mods_index.py - merge the author's mod lists with the review annotations into one table.

    python tools/build_mods_index.py            writes docs/mods/mods_index.csv and prints the counts

Inputs (docs/mods/):
    sources/mods_to_verify.txt        the long list of Nexus links to verify (repeats are kept in the count)
    sources/tested_1.9.6_list.txt     the author's "working on 1.9.6" list; the label after "N)" is the author's own name for the mod
    annotations.csv                   one row per mod the review documents say something about (hand-maintained)

When a list changes, copy it over the file in sources/ and run this again. IDs without an annotation stay in the index with an
empty review column, so the table shows what still has to be looked at.
"""
import collections
import csv
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(ROOT, "docs", "mods")
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
    ids = sorted(set(verify) | set(tested) | set(ann))
    cols = ["id", "url", "in_mods_to_verify", "times_in_verify_list", "in_tested_1.9.6_list", "author_label", "name", "name_source",
            "author_or_series", "versions", "install", "krs_area", "fix_status", "observation", "review_coverage"]
    out = os.path.join(D, "mods_index.csv")
    with open(out, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(cols)
        for i in ids:
            a = ann.get(i, {})
            in_lists = i in verify or i in tested
            w.writerow([i, f"https://www.nexusmods.com/kingdomcomedeliverance/mods/{i}", "yes" if i in verify else "",
                        verify.get(i, ""), "yes" if i in tested else "", label.get(i, ""), a.get("name", ""), a.get("name_source", ""),
                        a.get("author_or_series", ""), a.get("versions", ""), a.get("install", ""), a.get("krs_area", ""),
                        a.get("fix_status", ""), a.get("observation", ""),
                        ("described in review" if a else "no text in the review files") if in_lists else "outside the lists (named in review/README)"])
    in_lists = [i for i in ids if i in verify or i in tested]
    dup = sorted(i for i, n in verify.items() if n > 1)
    both = sorted(set(verify) & set(tested))
    print(f"links in mods_to_verify.txt: {sum(verify.values())}; unique ids: {len(verify)}; repeated inside it: {dup}")
    print(f"tested list: {len(tested)} ids; in both lists: {both}")
    print(f"unique ids across both lists: {len(in_lists)}")
    print(f"with review text: {sum(1 for i in in_lists if i in ann)}; without: {sum(1 for i in in_lists if i not in ann)}")
    print(f"annotated ids outside the lists: {sorted(i for i in ann if i not in in_lists)}")
    print("wrote", os.path.relpath(out, ROOT))


if __name__ == "__main__":
    sys.exit(main())
