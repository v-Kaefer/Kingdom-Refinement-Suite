#!/usr/bin/env python3
"""
analyze_perk_mods.py - read every Perkaholic / Riposte instance in the Perks workbench and say
what each one implements and whether it is implemented in a way the game actually loads.

    python tools/analyze_perk_mods.py
    python tools/analyze_perk_mods.py --workbench "<folder>" --game "<KCD folder>"

Reads the already-extracted copies under <workbench>/extracted and <workbench>/_sources, compares
every table against the unmodified game tables, and writes <workbench>/notes/analysis.json plus a
summary on screen. Nothing is installed or executed; the archives are only read.

Checked per table file, from the measured rules in docs/engine/ptf-rules.md:
  - is it inside Libs/Tables (rule: the game looks there only)
  - does the file suffix equal the mod id (rule 1; the id is <modid>, or the lower-cased <name>
    with spaces as underscores when the manifest has none - rule 2)
  - does it patch rows or replace the whole vanilla table (no suffix at all)
  - is every row complete (rule 5: a row that lists only some columns blanks the others)
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
GAME_VERSION = "1.9.8"
# the key column of each table we care about
KEY = {"perk": ["perk_id"], "buff": ["buff_id"], "perk_buff": ["buff_id", "perk_id"],
       "perk2perk_exclusivity": ["first_perk_id", "second_perk_id"], "skill": ["skill_id"],
       "perk_buff_override": ["perk_id", "source_buff_id", "target_buff_id"]}


def parse_table(path):
    """-> (table name, declared columns, rows) or None."""
    try:
        raw = open(path, encoding="utf-8", errors="replace").read()
    except OSError:
        return None
    try:
        root = ET.fromstring(re.sub(r"^\s*<\?xml[^>]*\?>", "", raw).strip())
    except ET.ParseError:
        return None
    t = root.find("table") if root.tag != "table" else root
    if t is None:
        return None
    cols = [c.get("name") for c in t.findall("./header/column")]
    rows = [dict(r.attrib) for r in t.findall("./rows/row")]
    return t.get("name"), cols, rows


def row_key(table, row):
    return tuple(row.get(k, "") for k in KEY.get(table, sorted(row)[:1]))


_PATHS = {}


def vanilla_path(table):
    """'perk' -> 'rpg/perk': the tables sit in several folders of Tables.pak."""
    if not _PATHS:
        import zipfile
        with zipfile.ZipFile(os.path.join(ARGS.game, "Data", "Tables.pak")) as z:
            for n in z.namelist():
                n = n.replace("\\", "/")
                if n.lower().startswith("libs/tables/") and n.lower().endswith(".xml"):
                    rel = n[len("Libs/Tables/"):-4]
                    _PATHS[os.path.basename(rel).lower()] = rel
    return _PATHS.get(table.lower())


def compare(table, rows):
    """-> dict with new / changed / identical / dropped and the incomplete rows."""
    table = table.split("__", 1)[0]                      # the file/table name carries the mod suffix
    path = vanilla_path(table)
    if not path:
        return None
    try:
        vcols, vrows = vanilla.load(path, game=ARGS.game)
    except Exception:
        return None
    names = [c for c, _ in vcols]
    index = {row_key(table, r): r for r in vrows}
    new, changed, same, incomplete = [], [], 0, []
    for r in rows:
        k = row_key(table, r)
        missing = [c for c in names if c not in r]
        if missing:
            incomplete.append({"key": "/".join(k), "missing": missing})
        v = index.get(k)
        if v is None:
            new.append({"key": "/".join(k), "name": r.get("perk_name") or r.get("buff_name") or ""})
        else:
            diff = {c: [v.get(c, ""), r.get(c, "")] for c in names
                    if c in r and str(r.get(c, "")) != str(v.get(c, ""))}
            if diff:
                changed.append({"key": "/".join(k), "name": r.get("perk_name") or v.get("perk_name")
                                or r.get("buff_name") or v.get("buff_name") or "", "diff": diff})
            else:
                same += 1
    present = {row_key(table, r) for r in rows}
    dropped = [k for k in index if k not in present]
    return {"vanilla_rows": len(vrows), "vanilla_columns": names, "rows": len(rows),
            "new": new, "changed": changed, "identical": same, "dropped": len(dropped),
            "incomplete": incomplete}


def manifest_facts(path):
    if not os.path.exists(path):
        return {"found": False}
    raw = open(path, encoding="utf-8", errors="replace").read()
    def tag(t):
        m = re.search(rf"<{t}>(.*?)</{t}>", raw, re.S)
        return m.group(1).strip() if m else ""
    versions = re.findall(r"<kcd_version>\s*([^<]+?)\s*</kcd_version>", raw)
    modid = tag("modid")
    name = tag("name")
    effective = (modid or name.lower().replace(" ", "_")).lower()
    if versions:
        loads = any(v == GAME_VERSION or v.endswith("*") or v == "*" for v in versions)
        why = ("lista " + ", ".join(versions)) if not loads else ("lista " + ", ".join(versions))
    else:
        loads, why = True, "sem bloco <supports>: nenhuma restrição de versão"
    return {"found": True, "name": name, "author": tag("author"), "version": tag("version"),
            "modid": modid, "effective_id": effective, "versions": versions, "loads": loads,
            "why": why, "xml_decl_ok": raw.lstrip().startswith('<?xml version="1.0"')}


def scan_instance(inst, folder, blocked):
    """Every table file of one instance, with how the game would treat it."""
    out = {"id": inst["id"], "label": inst["label"], "source": inst["source"], "files": [],
           "blocked_entries": blocked.get(inst["id"], [])}
    out["manifest"] = manifest_facts(os.path.join(folder, inst["manifest"]))
    eff = out["manifest"].get("effective_id", "")
    for base in inst["scan"]:
        root = os.path.join(folder, base)
        for dp, _, fn in os.walk(root):
            for f in sorted(fn):
                if not f.lower().endswith(".xml"):
                    continue
                p = os.path.join(dp, f)
                rel = os.path.relpath(p, folder).replace("\\", "/")
                if "localization" in rel.lower():
                    continue
                parsed = parse_table(p)
                if not parsed:
                    continue
                tname, dcols, rows = parsed
                stem = f[:-4]
                suffix = stem.split("__", 1)[1].lower() if "__" in stem else None
                in_libs = "libs/tables/" in rel.lower()
                in_pak = "/_pak/" in rel.lower() or rel.lower().startswith("_pak/")
                if suffix is None:
                    verdict, how = "replace", "substitui a tabela vanilla inteira"
                elif suffix != eff:
                    verdict, how = "ignored", f"sufixo '{suffix}' != id '{eff}'"
                elif not in_libs:
                    verdict, how = "ignored", "fora de Libs/Tables"
                elif not in_pak:
                    verdict, how = "loose", "solto, fora de um .pak"
                else:
                    verdict, how = "patch", "patch PTF correto"
                cmp_ = compare((tname or stem).split("__", 1)[0], rows)
                out["files"].append({"path": rel, "table": tname, "declared_columns": dcols,
                                     "suffix": suffix, "in_libs_tables": in_libs, "in_pak": in_pak,
                                     "verdict": verdict, "how": how, "compare": cmp_})
    return out


INSTANCES = [
    {"id": "85", "label": "Perkaholic 1.05", "source": "Nexus 85 (Xylozi)",
     "manifest": "extracted/85_perkaholic-1.05/Mods/perkaholic/mod.manifest",
     "scan": ["extracted/85_perkaholic-1.05"]},
    {"id": "770", "label": "Perkaholic 1.07", "source": "Nexus 770 (quarentena)",
     "manifest": "extracted/770_perkaholic-1.07/Perkaholic/mod.manifest",
     "scan": ["extracted/770_perkaholic-1.07"]},
    {"id": "1009r", "label": "Perkaholic PTF (.rar, 2026)", "source": "Nexus 1009 (DarkDevil428)",
     "manifest": "extracted/1009_perkaholic-ptf_rar/Perkaholic/mod.manifest",
     "scan": ["extracted/1009_perkaholic-ptf_rar"]},
    {"id": "1009f", "label": "Perkaholic PTF (pasta, 2024)", "source": "Nexus 1009, cópia antiga",
     "manifest": "_sources/1009_perkaholic-ptf_folder/mod.manifest",
     "scan": ["_sources/1009_perkaholic-ptf_folder", "extracted/1009_perkaholic-ptf_folder"]},
    {"id": "1765", "label": "Restore Riposte", "source": "Nexus 1765 (AcSiG)",
     "manifest": "_sources/1765_restore-riposte/mod.manifest",
     "scan": ["_sources/1765_restore-riposte", "extracted/1765_restore-riposte"]},
    {"id": "1563", "label": "Karnages Polearm Restoration 2.0", "source": "Nexus 1563",
     "manifest": "extracted/1563_karnages-polearm/Karnages_Polearm_Restoration 2.0/mod.manifest",
     "scan": ["extracted/1563_karnages-polearm"]},
    {"id": "1569", "label": "Karnages Shield Restoration", "source": "Nexus 1569",
     "manifest": "extracted/1569_karnages-shield/Karnages_Shield_Restoration/mod.manifest",
     "scan": ["extracted/1569_karnages-shield"]},
    {"id": "1629", "label": "Exclusive Master Strikes", "source": "Nexus 1629",
     "manifest": "extracted/1629_exclusive-masterstrikes/MakeThemReasonable/mod.manifest",
     "scan": ["extracted/1629_exclusive-masterstrikes"]},
    {"id": "1990", "label": "Veteran Hunting", "source": "Nexus 1990",
     "manifest": "extracted/1990_veteran-hunting/VeteranHunting/mod.manifest",
     "scan": ["extracted/1990_veteran-hunting"]},
    {"id": "1375", "label": "No Aim Spread", "source": "Nexus 1375",
     "manifest": "extracted/1375_no-aim-spread/NoAimSpread/mod.manifest",
     "scan": ["extracted/1375_no-aim-spread"]},
]
BLOCKED = {"770": ["../../../Data/Libs/Tables/rpg/buff.tbl",
                   "../../../Data/Libs/Tables/rpg/perk.tbl",
                   "../../../Data/Libs/Tables/rpg/perk2perk_exclusivity.tbl",
                   "../../../Data/Libs/Tables/rpg/perk_buff.tbl",
                   "../../../Data/Libs/Tables/rpg/perk_buff_override.tbl"]}


def main():
    global ARGS
    ap = argparse.ArgumentParser()
    ap.add_argument("--workbench", default=WORKBENCH)
    ap.add_argument("--game", default=vanilla.DEFAULT_GAME)
    ARGS = ap.parse_args()
    data = [scan_instance(i, ARGS.workbench, BLOCKED) for i in INSTANCES]
    out = os.path.join(ARGS.workbench, "notes", "analysis.json")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=1, ensure_ascii=False)

    for inst in data:
        m = inst["manifest"]
        print(f"\n=== {inst['id']}  {inst['label']}  ({inst['source']})")
        print(f"    manifest: id efetivo '{m.get('effective_id')}' | versão {m.get('version')} | "
              f"carrega em {GAME_VERSION}: {'SIM' if m.get('loads') else 'NÃO'} ({m.get('why')})")
        if inst["blocked_entries"]:
            print(f"    !! {len(inst['blocked_entries'])} entradas saem da pasta (path traversal)")
        for fl in inst["files"]:
            c = fl["compare"] or {}
            print(f"    [{fl['verdict']:7s}] {fl['table'] or '?':24s} {len(c.get('new', [])):4d} novas "
                  f"{len(c.get('changed', [])):4d} alteradas {c.get('identical', 0):4d} iguais "
                  f"{c.get('dropped', 0):5d} ausentes  {fl['how']}")
            if c.get("incomplete"):
                print(f"              {len(c['incomplete'])} linhas incompletas (regra 5)")
    print("\nwrote", out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
