#!/usr/bin/env python3
"""
audit_tables.py - report which game tables each mod source really changes.

For every table-patch XML found in the project (loose files and inside
.zip/.pak/.7zip archives that are zip-compatible), the rows are compared with
the vanilla table in the game's Tables.pak and classified as:

    new        key does not exist in vanilla
    changed    key exists, at least one column differs
    same       key exists and every column is identical (a no-op row)

Files that carry the same name as a vanilla table (no "__suffix") replace the
whole table; those are flagged FULL-REPLACE and the vanilla rows they drop are
counted.

Usage (from anywhere):
    python tools/audit_tables.py --root "E:/Kingdom-Refinement-Suite" \
        --game "E:/Kingdom-Refinement-Suite/Mods WIP folder/KingdomComeDeliverance" \
        --out docs/table-audit [--extra LABEL=PATH ...]

Writes <out>/TABLE_AUDIT.md and <out>/table_audit.json.
Archives in real 7z/rar format cannot be read; they are listed as "not inspected".
"""
import argparse
import collections
import hashlib
import json
import os
import re
import sys
import zipfile
import xml.etree.ElementTree as ET

SKIP_DIRS = {".git", ".claude", "dist", ".embold", ".qodo", "KingdomComeDeliverance", "Knox's Labelled Items (XML)",
             "Knox's Labelled Items (XML) - Version 1.0.2", "Knox's Labelled Items (XML)-326-1-0-2"}
ARCHIVE_EXT = (".zip", ".pak", ".7zip", ".7z", ".rar")

# Primary-key columns for tables where "all *_id columns" is not right.
KEYS = {
    "rpg_param": ["rpg_param_key"],
    "perk_rpg_param_override": ["perk_id", "rpg_param_key"],
    "skill2item_category": ["item_category", "skill_id"],
    "sleeping_spot_type": ["sleeping_spot_type_id"],
    "perk": ["perk_id"],
    "buff": ["buff_id"],
    "skill": ["skill_id"],
    "perk_buff": ["perk_id", "buff_id"],
    "document": ["item_id"],
    "food": ["item_id"],
}
TEXT_PREFIX = "text_"

# Tables that are listed row-by-row in the report (small and meaningful).
DETAIL_TABLES = {"rpg_param", "perk_rpg_param_override", "sleeping_spot_type", "perk", "skill2item_category",
                 "perk2perk_exclusivity", "skill", "buff", "perk_buff", "perk_buff_override"}


def read_member(z, zi):
    """Read an archive member; KCD paks store backslash names in local headers."""
    try:
        return z.open(zi).read()
    except zipfile.BadZipFile:
        zi.orig_filename = zi.filename.replace("/", "\\")
        return z.open(zi).read()


def parse_table(data):
    """Return (table_name, columns, rows) or None if the data is not a table patch."""
    text = data.decode("utf-8", "replace")
    text = re.sub(r"^\s*<\?xml[^>]*\?>", "", text)
    try:
        root = ET.fromstring(text)
    except ET.ParseError:
        return None
    t = root.find("table") if root.tag == "database" else None
    if t is None:
        return None
    cols = [c.get("name") for c in t.findall("./header/column")]
    rows = [dict(r.attrib) for r in t.findall("./rows/row")]
    return t.get("name"), cols, rows


def load_vanilla(game):
    """name -> {'file': path, 'cols': [...], 'rows': [...]} from Tables.pak (+ English text)."""
    out = {}
    pak = os.path.join(game, "Data", "Tables.pak")
    z = zipfile.ZipFile(pak)
    for zi in z.infolist():
        n = zi.filename
        if n.lower().startswith("libs/tables/") and n.lower().endswith(".xml"):
            p = parse_table(read_member(z, zi))
            if p:
                out[p[0]] = {"file": n, "cols": p[1], "rows": p[2]}
    tz = os.path.join(game, "Localization", "English_xml.pak")
    out["__text__"] = {"file": "English_xml.pak", "cols": ["key", "text", "markup"], "rows": []}
    if os.path.exists(tz):
        z = zipfile.ZipFile(tz)
        for zi in z.infolist():
            if not zi.filename.lower().endswith(".xml"):
                continue
            text = read_member(z, zi).decode("utf-8", "replace")
            text = re.sub(r"^\s*<\?xml[^>]*\?>", "", text)
            try:
                root = ET.fromstring(text)
            except ET.ParseError:
                continue
            for row in root.iter("Row"):
                cells = [c.text or "" for c in row.findall("Cell")]
                if cells:
                    out["__text__"]["rows"].append(
                        {"key": cells[0], "text": cells[1] if len(cells) > 1 else "",
                         "markup": cells[2] if len(cells) > 2 else ""})
    return out


def base_table(name, vanilla):
    """Map a patch table name to (vanilla base name, suffix-style)."""
    n = name.lower()
    if n.startswith(TEXT_PREFIX):
        return "__text__", "text"
    if n in vanilla:
        return n, "exact"
    if "__" in n and n.split("__")[0] in vanilla:
        return n.split("__")[0], "ptf"
    # single underscore suffix (seen in some mods) - best effort
    best = None
    for v in vanilla:
        if n.startswith(v + "_") and (best is None or len(v) > len(best)):
            best = v
    if best:
        return best, "single-underscore"
    return None, "unknown"


def key_cols(base, vanilla_cols, mod_cols):
    if base == "__text__":
        return ["key"]
    if base in KEYS:
        return KEYS[base]
    cols = [c for c in vanilla_cols if c in mod_cols]
    if "item_id" in cols:
        return ["item_id"]
    ids = [c for c in cols if c.endswith("_id")]
    return ids or cols


def norm(v):
    """Normalise a cell so that '0.10' and '0.1' compare equal."""
    if v is None:
        return ""
    v = str(v).strip()
    try:
        f = float(v)
        return str(int(f)) if f == int(f) else repr(f)
    except (ValueError, OverflowError):
        return v


def classify(base, vtab, cols, rows):
    kc = key_cols(base, vtab["cols"], cols)
    vidx = collections.defaultdict(list)
    for r in vtab["rows"]:
        vidx[tuple(norm(r.get(c)) for c in kc)].append(r)
    new, changed, same, details = 0, 0, 0, []
    colhist = collections.Counter()
    seen = set()
    for r in rows:
        k = tuple(norm(r.get(c)) for c in kc)
        seen.add(k)
        v = vidx.get(k)
        if not v:
            new += 1
            details.append(("new", k, {c: norm(r.get(c)) for c in cols if c not in kc}, dict(r)))
            continue
        diffs = {}
        best = None
        for cand in v:
            d = {c: (norm(cand.get(c)), norm(r.get(c))) for c in cols
                 if c not in kc and norm(cand.get(c)) != norm(r.get(c))}
            if best is None or len(d) < len(best):
                best = d
        diffs = best or {}
        if diffs:
            changed += 1
            colhist.update(diffs.keys())
            details.append(("changed", k, diffs, dict(r)))
        else:
            same += 1
            details.append(("same", k, {}, dict(r)))
    dropped = [k for k in vidx if k not in seen]
    return {"key_cols": kc, "new": new, "changed": changed, "same": same,
            "dropped_vs_vanilla": len(dropped), "changed_columns": dict(colhist), "details": details}


def relp(path, root):
    try:
        return os.path.relpath(path, root).replace("\\", "/")
    except ValueError:  # different drive (e.g. scratch copy of another branch)
        return path.replace("\\", "/")


def label_for(root, path):
    rel = os.path.relpath(path, root).replace("\\", "/")
    parts = rel.split("/")
    if parts[0].startswith("KRS-") and len(parts) > 2:
        return parts[0] + "/" + parts[1]  # e.g. KRS-Items/Data vs KRS-Items/WIP Base
    if parts[0] == "Mods WIP folder" and len(parts) > 2:
        return "/".join(parts[1:3]) if not parts[2].lower().endswith(ARCHIVE_EXT) else "/".join(parts[1:2] + [os.path.splitext(parts[2])[0]])
    return parts[0] if len(parts) > 1 else rel


def iter_sources(root, extras):
    """Yield (label, origin, name, bytes) for every candidate XML, and (label, origin) for opaque archives."""
    opaque = []
    roots = [(root, None)] + [(p, lab) for lab, p in extras]
    for base, forced in roots:
        for dp, dn, fn in os.walk(base):
            dn[:] = [d for d in dn if d not in SKIP_DIRS and not (d == "Tables" and "Mods WIP folder" in dp and dp.endswith("Mods WIP folder"))]
            for f in fn:
                p = os.path.join(dp, f)
                lab = forced or label_for(root, p)
                fl = f.lower()
                if fl.endswith(".xml"):
                    try:
                        yield lab, p, f, open(p, "rb").read()
                    except OSError:
                        pass
                elif fl.endswith(ARCHIVE_EXT):
                    try:
                        z = zipfile.ZipFile(p)
                    except zipfile.BadZipFile:
                        opaque.append((lab, p))
                        continue
                    for zi in z.infolist():
                        if zi.filename.lower().endswith(".xml"):
                            try:
                                yield lab, p + "!" + zi.filename, zi.filename, read_member(z, zi)
                            except Exception:
                                pass
    for o in opaque:
        yield o[0], o[1], None, None


def lint(rec, cols, rows, vanilla):
    """Cheap structural checks that catch rows the game would ignore or misread."""
    out = []
    stray = sorted({a for r in rows for a in r if a not in cols})
    if stray:
        out.append(f"row attributes not declared in the table header: {', '.join(stray)} "
                   f"(effect unverified: the attribute is probably ignored; published mods such as Restore "
                   f"Riposte and Realistic Repairs carry the same pattern)")
    base = rec["base"]
    if base and base != "__text__":
        extra = [c for c in cols if c not in vanilla[base]["cols"]]
        if extra:
            out.append(f"header columns not in the vanilla table: {', '.join(extra)}")
    if rec.get("key_cols") and (base in KEYS or rec["key_cols"] == ["item_id"] or base == "__text__"):
        kc = rec["key_cols"]
        keys = collections.Counter(tuple(norm(r.get(c)) for c in kc) for r in rows)
        dups = [k for k, n in keys.items() if n > 1]
        if dups:
            out.append(f"{len(dups)} duplicated key(s) inside the file, e.g. {'/'.join(dups[0])}")
    if rec.get("full_replace") and rec["rows"] == 0 and rec["base"]:
        out.append("empty FULL-REPLACE file: would wipe the whole vanilla table if packed")
    if rec["style"] == "single-underscore":
        out.append("table name uses a single-underscore suffix; PTF tables use '__suffix'")
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--game", required=True)
    ap.add_argument("--out", default="docs/table-audit")
    ap.add_argument("--extra", action="append", default=[], help="LABEL=PATH")
    ap.add_argument("--lint-labels", default=r"KRS|Kingdom|branch-", help="regex of source labels to lint")
    a = ap.parse_args()
    extras = [e.split("=", 1) for e in a.extra]

    vanilla = load_vanilla(a.game)
    print(f"vanilla tables loaded: {len(vanilla)}", file=sys.stderr)

    seen_hash = {}
    results, opaque, notable = [], [], []
    for lab, origin, name, data in iter_sources(a.root, extras):
        if data is None:
            opaque.append({"label": lab, "archive": relp(origin, a.root)})
            continue
        p = parse_table(data)
        if not p:
            continue
        tname, cols, rows = p
        h = hashlib.md5(data).hexdigest()
        key = (tname, h)
        rel = relp(origin.split("!")[0], a.root) + (
            "!" + origin.split("!", 1)[1] if "!" in origin else "")
        if key in seen_hash:
            seen_hash[key]["also_in"].append(lab)
            continue
        base, style = base_table(tname, vanilla)
        rec = {"label": lab, "file": rel, "table": tname, "base": base, "style": style,
               "rows": len(rows), "also_in": []}
        fname = os.path.basename(name).lower()
        if base and base != "__text__":
            vfile = os.path.basename(vanilla[base]["file"]).lower()
            rec["full_replace"] = (fname == vfile)
            rec.update({k: v for k, v in classify(base, vanilla[base], cols, rows).items()})
        elif base == "__text__":
            rec["full_replace"] = False
            rec.update(classify("__text__", vanilla["__text__"], cols, rows))
        else:
            rec["full_replace"] = False
            rec.update({"new": 0, "changed": 0, "same": 0, "dropped_vs_vanilla": 0, "details": [], "changed_columns": {}})
        rec["lint"] = lint(rec, cols, rows, vanilla)
        seen_hash[key] = rec
        results.append(rec)

    os.makedirs(a.out, exist_ok=True)
    write_md(a, results, opaque, vanilla)
    slim = []
    for r in results:
        if r["base"] and not r["new"] and not r["changed"] and not r["dropped_vs_vanilla"] and r["rows"] == r["same"]:
            continue  # identical to vanilla: nothing to track
        r = dict(r)
        if r["base"] not in ("rpg_param", "perk_rpg_param_override") and r["rows"] > 300:
            r["details"] = []  # keep the JSON small; counts and changed columns stay
            r["details_omitted"] = True
        slim.append(r)
    with open(os.path.join(a.out, "table_audit.json"), "w", encoding="utf-8") as f:
        json.dump({"results": slim, "opaque_archives": opaque}, f, ensure_ascii=False, default=list)
    print(f"wrote {a.out}", file=sys.stderr)


def fmt_kv(d):
    return ", ".join(f"{c}: {v[0]}->{v[1]}" if isinstance(v, tuple) else f"{c}={v}" for c, v in d.items())


def write_md(a, results, opaque, vanilla):
    L = []
    L.append("# Table audit\n")
    L.append("_Generated by `tools/audit_tables.py`. Compares every table-patch XML found in the project with the vanilla "
             "tables in the game's `Tables.pak`. Re-run it after changing any module._\n")
    L.append("`new` = key not in vanilla, `changed` = key in vanilla with different values, `same` = no-op row, "
             "`dropped` = vanilla rows missing from a FULL-REPLACE file.\n")
    by_label = collections.defaultdict(list)
    identical = collections.Counter()
    for r in results:
        if r["base"] and not r["new"] and not r["changed"] and not r["dropped_vs_vanilla"] and r["rows"] == r["same"]:
            identical[r["label"]] += 1  # whole table equals vanilla: packaging noise, not a change
            continue
        by_label[r["label"]].append(r)

    L.append("\n## 1. What each source touches\n")
    L.append("| Source | Table (vanilla base) | Style | Rows | new | changed | same | Note |")
    L.append("|---|---|---|---:|---:|---:|---:|---|")
    for lab in sorted(by_label):
        for r in sorted(by_label[lab], key=lambda x: x["table"]):
            note = []
            if r.get("full_replace"):
                note.append(f"**FULL-REPLACE** (drops {r.get('dropped_vs_vanilla', 0)} vanilla rows)")
            if r["style"] in ("single-underscore", "unknown"):
                note.append(r["style"])
            if r["also_in"]:
                note.append("also in " + ", ".join(sorted(set(r["also_in"]))))
            L.append(f"| {lab} | `{r['table']}` ({r['base'] or '?'}) | {r['style']} | {r['rows']} | "
                     f"{r.get('new', '')} | {r.get('changed', '')} | {r.get('same', '')} | {'; '.join(note)} |")

    if identical:
        L.append("\nTables whose content equals vanilla (ignored above, packaging noise): "
                 + "; ".join(f"{k}: {v}" for k, v in sorted(identical.items())) + "\n")

    # parameter matrix
    L.append("\n## 2. Parameter-level view (`rpg_param` and `perk_rpg_param_override`)\n")
    L.append("Every key set by more than one source is marked **CONFLICT**.\n")
    params = collections.defaultdict(list)
    for r in results:
        if r["base"] in ("rpg_param", "perk_rpg_param_override") and not r.get("full_replace"):
            for kind, k, d, row in r["details"]:
                if r["base"] == "rpg_param":
                    pkey, perk = k[0], ""
                else:
                    perk, pkey = k[0], k[1]
                params[(r["base"], perk, pkey)].append((r["label"], kind, row.get("rpg_param_value", "?")))
    vr = {}
    for r in vanilla["rpg_param"]["rows"]:
        vr[r.get("rpg_param_key")] = r.get("rpg_param_value")
    vo = {}
    for r in vanilla["perk_rpg_param_override"]["rows"]:
        vo[(r.get("perk_id"), r.get("rpg_param_key"))] = r.get("rpg_param_value")
    L.append("| Table | Param key | Vanilla | Source: value (status) | |")
    L.append("|---|---|---|---|---|")
    for (b, perk, pkey), lst in sorted(params.items(), key=lambda x: (x[0][0], x[0][2])):
        vals = []
        for lab, kind, v in lst:
            vals.append(f"{lab}: {v} ({kind})")
        flag = "**CONFLICT**" if len({x[0] for x in lst}) > 1 else ""
        vv = vr.get(pkey, "hidden") if b == "rpg_param" else vo.get((perk, pkey), "hidden")
        pk = f" perk `{perk[:8]}`" if perk else ""
        L.append(f"| {b} | `{pkey}`{pk} | {vv} | {' ; '.join(vals)} | {flag} |")

    L.append("\n## 3. Row-level detail for small tables\n")
    for lab in sorted(by_label):
        for r in by_label[lab]:
            if r["base"] in DETAIL_TABLES and r["base"] not in ("rpg_param", "perk_rpg_param_override") and not r.get("full_replace"):
                L.append(f"### {lab} - `{r['table']}`")
                L.append(f"`{r['file']}`  key = {r['key_cols']}\n")
                for kind, k, d, _ in r["details"][:40]:
                    L.append(f"- {kind}: {'/'.join(k)} {fmt_kv(d)[:200]}")
                if len(r["details"]) > 40:
                    L.append(f"- ... {len(r['details']) - 40} more")
                L.append("")

    L.append("\n## 4. Changed columns for large tables\n")
    for lab in sorted(by_label):
        for r in by_label[lab]:
            if r["base"] and r["base"] not in DETAIL_TABLES and r.get("changed_columns"):
                cc = ", ".join(f"{c} x{n}" for c, n in sorted(r["changed_columns"].items()))
                L.append(f"- **{lab}** `{r['table']}`: changed columns - {cc}")

    L.append("\n## 5. Lint findings\n")
    L.append(f"_Shown for sources matching `{a.lint_labels}` (change with --lint-labels). Third-party mods are listed "
             "in section 1 only; several of them carry the same quirks and still work in game._\n")
    for r in results:
        if r.get("lint") and re.search(a.lint_labels, r["label"]):
            L.append(f"- **{r['label']}** `{r['file']}`")
            for m in r["lint"]:
                L.append(f"  - {m}")

    L.append("\n## 6. Archives not inspected (not zip-compatible)\n")
    for o in sorted(opaque, key=lambda x: x["archive"]):
        L.append(f"- {o['archive']}  ({o['label']})")
    with open(os.path.join(a.out, "TABLE_AUDIT.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(L) + "\n")


if __name__ == "__main__":
    main()
