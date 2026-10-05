#!/usr/bin/env python3
"""
mod_intersections.py - where the graded mods intersect: same row, same table, or a whole-table replacement.

    python tools/subcategorize_mods.py && python tools/mod_intersections.py

Reads only generated files (docs/mods-review/mod_overlap.csv, mod_tables.csv, mod_analysis.csv,
mod_subcategories.csv and the KRS collision lines of MOD_PROFILES.md): no archive is opened,
nothing is extracted and no network call is made.

Writes docs/mods-review/MOD_INTERSECTIONS.md and docs/mods-review/mod_intersections.csv.

Why it matters (docs/engine/ptf-rules.md, measured): rule 6 - a row is replaced whole and the last
mod in mod_order.txt wins, so two mods that write the same row cannot both take effect; rule 5 - a
row that lists only some columns blanks the others. A file without the PTF suffix replaces the whole
vanilla table, so it overrides every patch of every other mod on that table.
"""
import collections
import csv
import datetime
import itertools
import os
import posixpath
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paths  # noqa: E402

D = paths.MODS_REVIEW
GRADES = ["A changes the most", "B large", "C effective (few rows, strong effect)", "D small tweak",
          "E non-perceptive to gameplay (content or text only)",
          "E non-perceptive to gameplay (no effective change found)", "X not analysed"]


def read_csv(name):
    with open(os.path.join(D, name), encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def num(v):
    try:
        return int(v)
    except (TypeError, ValueError):
        return 0


def esc(t):
    return str(t).replace("|", "/").replace("\n", " ")


def changed_tables():
    """mod id -> {vanilla table it changes a row in}, and mod id -> {table it replaces whole}."""
    touch, replace = collections.defaultdict(set), collections.defaultdict(set)
    for r in read_csv("mod_tables.csv"):
        base = posixpath.basename(r["file_in_mod"].replace("\\", "/"))
        name = base[:-4] if base.lower().endswith(".xml") else base
        if r["style"] == "exact" and "__" not in name:
            replace[r["id"]].add(r["vanilla_table"])
        if num(r["new"]) + num(r["changed"]) > 0:
            touch[r["id"]].add(r["vanilla_table"])
    return dict(touch), dict(replace)


def shared_rows():
    """(a, b) -> {table: shared rows}, from the rows that two or more mods change."""
    pairs = collections.defaultdict(collections.Counter)
    rows = read_csv("mod_overlap.csv")
    for r in rows:
        ids = sorted(set(r["mod_ids"].split()), key=int)
        for a, b in itertools.combinations(ids, 2):
            pairs[(a, b)][r["table"]] += 1
    return pairs, rows


def krs_rows():
    """mod id -> ({krs module: {table:key}}, the mods whose list is cut), from the generated profiles.

    audit_mods_report.py cuts that line at 300 characters, so a long list ends mid-token: the partial
    last item is dropped and the mod is marked as cut instead of a row being invented for it.
    """
    p = os.path.join(D, "MOD_PROFILES.md")
    out, cut = collections.defaultdict(lambda: collections.defaultdict(set)), set()
    for section in re.split(r"(?m)^## ", open(p, encoding="utf-8").read())[1:]:
        head = section.split("\n")[0]
        m = re.match(r"(\d+) ", head)
        line = re.search(r"(?m)^- \*\*Same rows as KRS:\*\* (.+)$", section)
        if not (m and line):
            continue
        items = [i.strip() for i in line.group(1).split(";")]
        if len(line.group(1)) >= 300:
            cut.add(m.group(1))
            items = items[:-1]
        for item in items:
            part = item.split(":", 1)
            if len(part) == 2:
                out[m.group(1)][part[0]].add(part[1])
    return out, cut


def collect():
    sub_file = os.path.join(D, "mod_subcategories.csv")
    if not os.path.exists(sub_file):
        sys.exit("run tools/subcategorize_mods.py first: mod_subcategories.csv is missing")
    mods = {r["id"]: r for r in read_csv("mod_subcategories.csv")}
    touch, replace = changed_tables()
    rowpairs, overlap = shared_rows()

    pairs = []
    seen = set(rowpairs)
    for a, b in itertools.combinations(sorted(touch, key=int), 2):
        both = touch[a] & touch[b]
        if not both and (a, b) not in seen:
            continue
        rows = rowpairs.get((a, b), collections.Counter())
        # a file without a suffix replaces the whole table, so it overrides the other mod's patches there
        over_ab = sorted(replace.get(a, set()) & touch[b])
        over_ba = sorted(replace.get(b, set()) & touch[a])
        if rows and (over_ab or over_ba):
            kind = "same rows + whole-table replacement"
        elif rows:
            kind = "same rows"
        elif over_ab or over_ba:
            kind = "whole-table replacement"
        else:
            kind = "same table only"
        pairs.append({
            "mod_a": a, "name_a": mods.get(a, {}).get("name", ""), "grade_a": mods.get(a, {}).get("grade", "")[:1],
            "mod_b": b, "name_b": mods.get(b, {}).get("name", ""), "grade_b": mods.get(b, {}).get("grade", "")[:1],
            "kind": kind, "shared_rows": sum(rows.values()), "shared_tables": len(both),
            "tables_with_shared_rows": ", ".join(f"{t} {n}" for t, n in rows.most_common(6)),
            "shared_tables_list": ", ".join(sorted(both))[:200],
            "subcategory_a": mods.get(a, {}).get("subcategory", ""),
            "subcategory_b": mods.get(b, {}).get("subcategory", ""),
            "same_subcategory": "yes" if (mods.get(a, {}).get("subcategory")
                                          == mods.get(b, {}).get("subcategory")) else "no",
            "replaces_whole_table": ("; ".join(filter(None, [
                f"{a} replaces " + ", ".join(over_ab) if over_ab else "",
                f"{b} replaces " + ", ".join(over_ba) if over_ba else ""])))[:200],
        })
    pairs.sort(key=lambda p: (-p["shared_rows"], -p["shared_tables"], int(p["mod_a"]), int(p["mod_b"])))
    return mods, touch, replace, pairs, overlap


COLS = ["mod_a", "name_a", "grade_a", "mod_b", "name_b", "grade_b", "kind", "shared_rows", "shared_tables",
        "tables_with_shared_rows", "shared_tables_list", "same_subcategory", "subcategory_a", "subcategory_b",
        "replaces_whole_table"]


def write_csv(pairs):
    p = os.path.join(D, "mod_intersections.csv")
    with open(p, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=COLS, extrasaction="ignore")
        w.writeheader()
        w.writerows(pairs)
    return p


def clip(text, n=90):
    """Cut a separated list to whole items, so no id is shown half."""
    text = esc(text)
    if len(text) <= n:
        return text
    sep = "; " if "; " in text else ", "
    cut = text[:n].rsplit(sep, 1)[0]
    return cut + sep + "..."


def pair_table(pairs, limit=None, note=True):
    out = ["| Mod A | Mod B | Shared rows | Where | Kind |", "|---|---|---|---|---|"]
    for p in pairs[:limit]:
        where = p["tables_with_shared_rows"] or p["shared_tables_list"]
        out.append(f"| {p['grade_a']} {p['mod_a']} {esc(p['name_a'])[:34]} | {p['grade_b']} {p['mod_b']} "
                   f"{esc(p['name_b'])[:34]} | {p['shared_rows'] or '-'} | {clip(where)} | {p['kind']} |")
    if note and limit and len(pairs) > limit:
        out.append(f"| ... | ... | ... | {len(pairs) - limit} more in `mod_intersections.csv` | |")
    return out


def write_md(mods, touch, replace, pairs, overlap):
    today = datetime.date.today().isoformat()
    hard = [p for p in pairs if p["shared_rows"]]
    soft = [p for p in pairs if not p["shared_rows"]]
    repl = [p for p in pairs if "whole-table replacement" in p["kind"]]
    krs, krs_cut = krs_rows()
    no_tables = sorted((m for m in mods if m not in touch), key=int)
    lonely = sorted((m for m in touch if not any(p["mod_a"] == m or p["mod_b"] == m for p in pairs)), key=int)

    out = ["# Where the graded mods intersect (generated)", "",
           "> **GENERATED** by `tools/mod_intersections.py`: do not edit | **Kind:** review | **Trust:** derived from "
           "the read-only analysis (`mod_overlap.csv`, `mod_tables.csv`, `mod_subcategories.csv`; no archive was "
           "opened for this file) | **Game version:** 1.9.8", "",
           f"Read on {today}: the mods graded A to E of [`MOD_SUBCATEGORIES.md`](MOD_SUBCATEGORIES.md). "
           f"**{len(touch)} of them write table rows**, and of those **{len(pairs)} pairs intersect**: "
           f"{len(hard)} pairs write at least one of the same rows, {len(soft)} more write into the same table "
           f"without sharing a row, and {len(repl)} of the pairs include a mod that replaces one of those tables "
           f"whole. Every pair is in `mod_intersections.csv`; the contested rows themselves are in `mod_overlap.csv`.",
           "",
           "## What an intersection costs", "",
           "From the measured rules in [`../engine/ptf-rules.md`](../engine/ptf-rules.md):", "",
           "| Kind | What the game does | Consequence |", "|---|---|---|",
           "| **Same row** | rule 6: a row is replaced whole and the **last mod in `mod_order.txt` wins** | only one "
           "of the two mods takes effect on that row; the other's values are undone, silently |",
           "| **Same table, no shared row** | both patches are applied to different rows | they coexist; the risk is "
           "only that a later whole-table replacement of that table wipes both |",
           "| **Whole-table replacement** | a file without the `__<modid>` suffix replaces the vanilla table | it "
           "overrides **every** patch of **every** other mod on that table, whatever the rows, and also undoes the "
           "game's own 1.9.7/1.9.8 changes to it |", "",
           "Rule 5 makes a shared row worse than it looks: a row that lists only some columns blanks the others, so "
           "the mod that wins a contested row can zero columns the other mod never touched.", "",
           "## The hardest conflicts: most shared rows", ""]
    out += pair_table(hard, 25) + [""]

    out += ["## Whole-table replacement: one mod overrides the others", "",
            "These mods ship at least one table file without the PTF suffix. On those tables nothing else survives, "
            "so every other mod listed here loses its patches to that table regardless of which rows it writes.", "",
            "| Mod | Grade | Tables replaced | Other mods overridden | Which tables are contested |",
            "|---|---|---|---|---|"]
    rep_rows = []
    for m, ts in replace.items():
        victims = {o for t in ts for o in touch if o != m and t in touch[o]}
        contested = sorted({t for t in ts if any(t in touch[o] for o in touch if o != m)})
        rep_rows.append((len(victims), m, ts, victims, contested))
    for n, m, ts, victims, contested in sorted(rep_rows, reverse=True, key=lambda x: (x[0], len(x[2]))):
        out.append(f"| {m} {esc(mods.get(m, {}).get('name', ''))[:34]} | {mods.get(m, {}).get('grade', '')[:1]} | "
                   f"{len(ts)} | {n} | {clip(', '.join(contested), 80) or '(none: only it writes them)'} |")
    out.append("")

    out += ["## Intersections inside a sub-category", "",
            "The mods that do the same job. A shared row here means the two are **alternatives, not an addition**: "
            "installing both leaves whichever loads last in charge of the contested rows.", ""]
    bysub = collections.defaultdict(list)
    for p in pairs:
        if p["same_subcategory"] == "yes":
            bysub[p["subcategory_a"]].append(p)
    for sub in sorted(bysub, key=lambda s: -len(bysub[s])):
        group = bysub[sub]
        h = [p for p in group if p["shared_rows"]]
        out += [f"### {sub} ({len(group)} pair{'' if len(group) == 1 else 's'}, "
                f"{len(h)} of them on the same rows)", ""]
        out += pair_table(sorted(group, key=lambda p: -p["shared_rows"]), 12) + [""]

    cross = [p for p in pairs if p["same_subcategory"] == "no" and p["shared_rows"]]
    out += ["## Intersections across sub-categories", "",
            f"{len(cross)} pairs write the same rows while sitting in different sub-categories: the mod is not a "
            "rival, it just reaches into the same table. These are the ones easy to miss when picking one mod per "
            "sub-category.", ""]
    out += pair_table(cross, 25) + [""]

    tables = collections.Counter()
    for r in overlap:
        tables[r["table"]] += 1
    out += ["## The most contested tables and rows", "",
            "| Table | Rows that two or more mods change |", "|---|---|"]
    for t, n in tables.most_common(15):
        out.append(f"| {t} | {n} |")
    out += ["", "| Table | Row | Mods | Ids |", "|---|---|---|---|"]
    for r in sorted(overlap, key=lambda r: -num(r["mods_changing_it"]))[:20]:
        out.append(f"| {r['table']} | {esc(r['key'])[:44]} | {r['mods_changing_it']} | {esc(r['mod_ids'])[:70]} |")
    out.append("")

    out += ["## Intersections with the KRS modules", "",
            f"{len(krs)} mods write rows that `modules/krs_items`, `krs_perks` or `krs_qol` also write "
            f"({sum(len(v) for t in krs.values() for v in t.values())} rows in total). By rule 6 the load order "
            "decides, so each of these is a decision for the suite: keep the KRS row, drop it, or ship the mod's "
            "value. Source: the *Same rows as KRS* lines of [`MOD_PROFILES.md`](MOD_PROFILES.md); the suite's own "
            "claims are in `../data/ownership.csv`.", "",
            "| Mod | Grade | KRS module | Rows both write |", "|---|---|---|---|"]
    for m in sorted(krs, key=int):
        for module, keys in sorted(krs[m].items()):
            shown = clip("; ".join(sorted(keys)), 110)
            if m in krs_cut:
                shown += " **(the source list is cut at 300 characters: there are more)**"
            out.append(f"| {m} {esc(mods.get(m, {}).get('name', ''))[:34]} | {mods.get(m, {}).get('grade', '')[:1]} | "
                       f"{module} | {shown} |")
    out.append("")

    out += ["## What intersects with nothing", "",
            f"**{len(lonely)} mod{'' if len(lonely) == 1 else 's'} "
            f"{'writes' if len(lonely) == 1 else 'write'} table rows that no other mod in this set touches**, and no "
            f"mod replaces a table they use: {', '.join(lonely) if lonely else 'none'}. Those can be added without a "
            "row decision.", "",
            f"**{len(no_tables)} mods change no table row** (Lua, engine config, non-table XML, assets, text, or a "
            "patch whose every row is identical to vanilla), so this method cannot compare them with anything: "
            f"{', '.join(no_tables)}. Two Lua mods that hook the same event, or two archives that ship the same "
            "texture path, would intersect in the game and are not visible here.", "",
            "## Limits", "",
            "- Only table rows are compared. The analysis CSVs count Lua lines, config keys and asset files but do "
            "not list their names, so Lua, `.cfg`, UI and asset collisions cannot be derived; re-reading the archives "
            "would be needed for that.",
            "- `mod_overlap.csv` holds, by design, only the rows that two or more mods change, which is exactly the "
            "intersection set; a row only one mod writes cannot appear and is not missing.",
            "- The four native mods (2246, 2326, 2348, 2359) change rpg params at runtime, not in a table, so an "
            "intersection with them cannot be read from files at all.",
            "- Intersections are counted per mod id across all its archives, so a mod whose options are alternatives "
            "(1243, 1483, 2294) shows the union of its options.",
            "- Whether an intersection hurts depends on load order, which is a local `mod_order.txt` and not part of "
            "this data.", ""]

    p = os.path.join(D, "MOD_INTERSECTIONS.md")
    with open(p, "w", encoding="utf-8") as f:
        f.write("\n".join(out))
    return p


def main():
    mods, touch, replace, pairs, overlap = collect()
    md = write_md(mods, touch, replace, pairs, overlap)
    cs = write_csv(pairs)
    hard = sum(1 for p in pairs if p["shared_rows"])
    print(f"{len(pairs)} intersecting pairs ({hard} on the same rows), {len(replace)} mods replace a whole table")
    for p in (md, cs):
        print("wrote", os.path.relpath(p, paths.ROOT).replace("\\", "/"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
