#!/usr/bin/env python3
"""
build_mods_index.py - merge every mod list of the project into one table.

    python tools/build_mods_index.py            writes docs/mods-review/mods_index.csv and prints the counts

Inputs (docs/mods-review/):
    sources/mods_to_verify.txt            the long list of Nexus links to verify (repeats are kept in the count)
    sources/tested_1.9.6_list.txt         the author's "working on 1.9.6" list; the label after "N)" is the author's own name for the mod
    sources/nexusmods_abas_vivaldi.csv    the 180 Nexus tabs open in the author's browser (id, name, link)
    raw/new-mods-lists-review/id_titles.csv   merged title list of the "New mods lists review" session (290 mods: Vivaldi tabs plus
                                          browser-history screenshots): title, keyword category, PTF flag, fix type, KRS area
    workspace_mods.csv                    mods found in the workspace and the Vortex deployment (tools/scan_workspace_mods.py)
    annotations.csv                       one row per mod the review documents say something about (hand-maintained)

Every id from every input gets a row. The `triage` column is a mechanical sort, not a verdict: it is derived from the keyword
category of id_titles.csv and the KRS area, so the author can see at a glance which mods need a table-overlap check against the
KRS modules and which can be ignored for that purpose (visual presets, tools, adult content). No mod page or archive was read.

When a list changes, copy it over the file in sources/ and run this again.
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

TRIAGE = [  # (category keyword, triage)
    ("Adult", "out of scope: adult content"),
    ("Reshade", "visual only: preset (no table overlap)"),
    ("Graphics config", "visual only: user.cfg values (hardware-specific)"),
    ("Tools", "tool or reference (not gameplay)"),
    ("Maps / UI", "UI or maps: replaces files, conflicts with other UI mods"),
    ("World", "world or weather: large content, outside the PTF scope"),
    ("Quests", "content: outside the PTF scope"),
    ("Animations", "animations or audio: outside table scope"),
]


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


def read_csv(path, enc="utf-8-sig"):
    return list(csv.DictReader(open(path, encoding=enc, newline=""))) if os.path.exists(path) else []


def triage(row, ann):
    cat, area = row.get("category", ""), row.get("krs_area", "") or ann.get("krs_area", "")
    prefix = "PTF reference; " if row.get("ptf") == "PTF" else ""
    if not cat:
        return "unsorted (no category yet)"
    for key, t in TRIAGE:
        if key in cat:
            return t
    if area:
        return f"{prefix}gameplay: overlap check needed ({area.split(' (')[0]})"
    return f"{prefix}gameplay: no KRS area flagged, still check tables"


def main():
    verify, tested, label = read_lists()
    ann = {int(r["id"]): r for r in read_csv(os.path.join(D, "annotations.csv"), "utf-8")}
    work = {int(r["id"]): r for r in read_csv(os.path.join(D, "workspace_mods.csv"), "utf-8")}
    viv = {int(r["id"]): r for r in read_csv(os.path.join(D, "sources", "nexusmods_abas_vivaldi.csv"))}
    titles = {int(r["id"]): r for r in read_csv(os.path.join(D, "raw", "new-mods-lists-review", "id_titles.csv"))}
    evid = {int(r["id"]): r for r in read_csv(os.path.join(D, "search_evidence.csv"), "utf-8")}
    api = {int(r["id"]): r for r in read_csv(os.path.join(D, "nexus_metadata.csv"), "utf-8") if r.get("id")}   # tools/nexus_metadata.py
    ids = sorted(set(verify) | set(tested) | set(ann) | set(work) | set(viv) | set(titles) | set(evid) | set(api))
    cols = ["id", "url", "name", "name_source", "scope", "in_mods_to_verify", "times_in_verify_list", "in_tested_1.9.6_list",
            "in_vivaldi_tabs", "in_history_screenshots", "in_workspace", "author_label", "category", "ptf", "triage",
            "author_or_series", "versions", "install", "krs_area", "fix_type", "fix_status", "check_1.9.8", "check_source",
            "observation", "list_review_note", "nexus_status", "nexus_summary", "review_coverage"]
    out = os.path.join(D, "mods_index.csv")
    rows_out, lists_scope = [], {}
    with open(out, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(cols)
        for i in ids:
            a, t = ann.get(i, {}), titles.get(i, {})
            in_lists = i in verify or i in tested
            in_new = i in viv or i in titles
            if in_lists:
                scope = "in the author's lists"
            elif in_new:
                scope = "new: Vivaldi tabs or screenshots only"
            elif i in work:
                scope = "workspace/installed only"
            else:
                scope = "found while checking (outside the lists)"
            lists_scope[i] = scope
            # browser titles are the exact page titles; annotation names (search summaries, author labels) come after them
            seen = evid.get(i, {}).get("title_seen", "")
            name = api.get(i, {}).get("name") or viv.get(i, {}).get("nome") or t.get("title") or seen or a.get("name") or work.get(i, {}).get("name", "") or label.get(i, "")
            src = ("Nexus API" if api.get(i, {}).get("name") else "") or ("Vivaldi tab" if i in viv else "") or ("id_titles.csv" if t.get("title") else "") \
                or ("search result title" if seen else "") or (a.get("name_source") if a.get("name") else "") or ("workspace file name" if i in work else "") or ("author label" if i in label else "")
            src_t = t.get("source", "")
            cover = "described in review" if a else ("title list only" if t else "no text in the review files")
            w.writerow([i, f"https://www.nexusmods.com/kingdomcomedeliverance/mods/{i}", name, src, scope,
                        "yes" if i in verify else "", verify.get(i, ""), "yes" if i in tested else "",
                        "yes" if i in viv else "", "yes" if src_t in ("screenshots", "both") else "",
                        work.get(i, {}).get("where", ""), label.get(i, ""), t.get("category", ""), t.get("ptf", ""),
                        triage(t, a) if (t or a) else "unsorted (no category yet)", a.get("author_or_series", ""),
                        a.get("versions", ""), a.get("install", ""), a.get("krs_area", "") or t.get("krs_area", ""),
                        t.get("fix_type", ""), a.get("fix_status", ""), a.get("check_1.9.8", ""), a.get("check_source", ""),
                        a.get("observation", ""), t.get("review_note", ""), api.get(i, {}).get("status", ""),
                        api.get(i, {}).get("summary", "")[:300], cover])
            rows_out.append(i)
    dup = sorted(i for i, n in verify.items() if n > 1)
    print(f"links in mods_to_verify.txt: {sum(verify.values())}; unique ids: {len(verify)}; repeated inside it: {dup}")
    print(f"tested list: {len(tested)} ids; in both lists: {sorted(set(verify) & set(tested))}")
    print(f"Vivaldi tabs: {len(viv)} ids; id_titles.csv: {len(titles)} ids")
    c = collections.Counter(lists_scope.values())
    for k, v in sorted(c.items()):
        print(f"  scope '{k}': {v}")
    print(f"total rows: {len(ids)}")
    print(f"with a category: {sum(1 for i in ids if i in titles)}; checked against 1.9.8: {sum(1 for i in ann if ann[i].get('check_1.9.8'))}")
    print("wrote", os.path.relpath(out, ROOT))


if __name__ == "__main__":
    sys.exit(main())
