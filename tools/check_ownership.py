#!/usr/bin/env python3
"""
check_ownership.py - keep docs/ownership.csv and the real module files in sync.

Run tools/audit_tables.py first (it writes docs/table-audit/table_audit.json), then:

    python tools/check_ownership.py [--audit docs/table-audit/table_audit.json]
                                    [--ownership docs/ownership.csv]
                                    [--sources REGEX]

Every row a KRS module file changes (status new/changed in the audit) must be listed in
ownership.csv with exactly one owning module. The report lists:

    UNOWNED    a changed row in a KRS source that has no ownership entry
    MISPLACED  an owned row that currently lives outside its module's folder (migration to-do)
    DUPLICATE  the same row is set in more than one KRS source
    VALUE      the current value differs from the `target` in ownership.csv
    MISSING    a shipping entry whose row is not in its module's folder yet
    NO-OP      rows a KRS source repeats with vanilla values (harmless, but noise that can
               overwrite other mods' changes if row-level merging applies)

Exit code 1 when there is any UNOWNED, DUPLICATE, VALUE or MISSING finding.

ownership.csv columns:
    table      vanilla base table (rpg_param, perk, document, food, ...)
    key        key as printed by the audit ("/"-joined key columns); "*" = every row of the table
    module     owning module (KRS-Items, KRS-QoL, KRS-Perks)
    vanilla    vanilla value, for humans
    target     col=value the module must set (empty = not asserted)
    status     shipping | planned | decision | remove
    lives_in   path prefix (path of the patch file) where the row is expected, e.g. KRS-Items/Data
    source     where the idea/values come from
    notes
"""
import argparse
import collections
import csv
import json
import re
import sys


def load_rows(audit, sources):
    rows = collections.defaultdict(list)  # (table, key) -> [(label, kind, row, file)]
    noop = collections.Counter()
    for r in audit["results"]:
        if not r.get("base") or not re.search(sources, r["file"]):
            continue
        base = "text" if r["base"] == "__text__" else r["base"]
        if r.get("details_omitted"):
            print(f"note: details omitted for {r['label']} {r['table']} ({r['rows']} rows)", file=sys.stderr)
        for kind, k, diff, row in r.get("details", []):
            if kind == "same":
                noop[(r["file"], base)] += 1
                continue
            rows[(base, "/".join(k))].append((r["file"], kind, row, r["file"]))
        if r.get("full_replace") and r["rows"] == 0:
            rows[(base, "*EMPTY-FULL-REPLACE*")].append((r["file"], "changed", {}, r["file"]))
    return rows, noop


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--audit", default="docs/table-audit/table_audit.json")
    ap.add_argument("--ownership", default="docs/ownership.csv")
    ap.add_argument("--sources", default=r"^modules/",
                    help="regex of audit labels that count as suite sources (default leaves out scratch folders "
                         "such as 'KRS-Items/WIP Base'; add branch-.* to include other branches)")
    a = ap.parse_args()

    audit = json.load(open(a.audit, encoding="utf-8"))
    own = list(csv.DictReader(open(a.ownership, encoding="utf-8", newline="")))
    rows, noop = load_rows(audit, a.sources)

    exact = {(o["table"], o["key"]): o for o in own if o["key"] != "*"}
    wild = {o["table"]: o for o in own if o["key"] == "*"}
    problems, todo = [], []
    same_dups = collections.Counter()

    def owner_of(table, key):
        return exact.get((table, key)) or wild.get(table)

    for (table, key), occ in sorted(rows.items()):
        o = owner_of(table, key)
        if key == "*EMPTY-FULL-REPLACE*":
            problems.append(f"EMPTY-REPLACE {table}: {occ[0][3]} would wipe the vanilla table if packed")
            continue
        if not o:
            problems.append(f"UNOWNED   {table} {key}  (in {', '.join(sorted({x[0] for x in occ}))})")
            continue
        labels = sorted({x[0] for x in occ})
        if len(labels) > 1:
            per = {l: _val(table, [x for x in occ if x[0] == l][0][2]) for l in labels}
            if len({str(_num(v)) for v in per.values()}) == 1:
                same_dups[(table, tuple(labels))] += 1  # same value twice: summarised below
            else:
                vals = "; ".join(f"{l}={v}" for l, v in per.items())
                problems.append(f"DUPLICATE {table} {key}  owner {o['module']}: {vals}  <- values differ")
        home = [x for x in occ if x[0].startswith(o["lives_in"])]
        if not home:
            todo.append(f"MISPLACED {table} {key}  owner {o['module']} expects {o['lives_in']}, found in {', '.join(labels)}")
        elif o["target"] and o["status"] in ("shipping",):
            col, _, want = o["target"].partition("=")
            got = home[0][2].get(col)
            if got is None or _num(got) != _num(want):
                problems.append(f"VALUE     {table} {key}  target {o['target']} but {home[0][0]} has {col}={got}")

    for o in own:
        if o["key"] == "*" or o["status"] != "shipping":
            continue
        present = [x for x in rows.get((o["table"], o["key"]), []) if x[0].startswith(o["lives_in"])]
        if not present:
            problems.append(f"MISSING   {o['table']} {o['key']}  ({o['module']}, shipping) not found under {o['lives_in']}")
    for o in own:
        if o["key"] == "*" and o["status"] == "shipping":
            if not any(t == o["table"] and any(x[0].startswith(o["lives_in"]) for x in occ)
                       for (t, _), occ in rows.items()):
                problems.append(f"MISSING   {o['table']} *  ({o['module']}, shipping) no rows under {o['lives_in']}")

    for (table, labels), n in sorted(same_dups.items()):
        problems.append(f"DUPLICATE {table}: {n} row(s) set identically in {' and '.join(labels)}; keep only the owner's copy")

    print("== Problems (exit code 1) ==")
    print("\n".join(problems) or "none")
    print("\n== Migration to-do (rows owned by a module but still living elsewhere) ==")
    print("\n".join(todo) or "none")
    print("\n== No-op rows (same as vanilla) ==")
    for (label, base), n in sorted(noop.items()):
        print(f"{label}: {n} row(s) in {base}")
    sys.exit(1 if problems else 0)


def _num(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return str(v)


def _val(table, row):
    for c in ("rpg_param_value", "length_in_game_hours", "sleeping_quality", "level"):
        if c in row:
            return row[c]
    return "row"


if __name__ == "__main__":
    main()
