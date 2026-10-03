#!/usr/bin/env python3
"""
analyze_mod_archives.py - read downloaded mod archives (never the network) and record what is really inside.

    python tools/analyze_mod_archives.py --src "<folder with .zip/.7z/.rar>" [--work <scratch folder>] [--max-extract-mb 15]

For every archive:
  * the Nexus id comes from the file name (`Name-<id>-<version>-<timestamp>.ext`)
  * archives up to --max-extract-mb are extracted into the scratch folder (the source folder is only read); bigger ones are
    only listed, and only their manifests are extracted
  * mod.manifest: modid, effective id (modid or lower-cased name with underscores), the <kcd_version> lines, and whether the
    1.9.8 engine would load it (measured rule, docs/engine/game-versions.md: explicit match or wildcard `1.9.*` or no restriction)
  * table patches (loose `Libs/Tables/**` or inside a ZIP pak): file suffix vs mod id, complete rows, whole-table replacement
  * rows that collide with the KRS modules (same table and key as a row in modules/<id>/Data)
Writes docs/mods-review/archive_analysis.csv (GENERATED) and prints a summary.
"""
import argparse
import csv
import os
import re
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET
import zipfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paths  # noqa: E402

SEVENZ = r"C:\Program Files\7-Zip\7z.exe"
KEYS = {
    "rpg_param": ["rpg_param_key"], "sleeping_spot_type": ["sleeping_spot_type_id"], "document": ["item_id"], "food": ["item_id"],
    "perk": ["perk_id"], "perk_rpg_param_override": ["perk_id", "rpg_param_key"], "skill2item_category": ["item_category", "skill_id"],
    "buff": ["buff_id"], "item": ["item_id"], "player_item": ["item_id"], "potion": ["item_id"],
}
NAME = re.compile(r"^(?P<name>.+?)-(?P<id>\d{1,4})-(?:\d|-)")


def engine_loads(versions, target="1.9.8"):
    if not versions:
        return "yes (no version restriction)"
    for v in versions:
        if v == target:
            return "yes (explicit)"
        if v.endswith(".*") and target.startswith(v[:-1]):
            return "yes (wildcard)"
    return "NO (disabled: lists " + ", ".join(versions) + ")"


def rows_of(raw):
    try:
        t = ET.fromstring(re.sub(r"^\s*<\?xml[^>]*\?>", "", raw.decode("utf-8", "replace").lstrip("\ufeff"))).find("table")
        cols = [c.get("name") for c in t.findall("./header/column")]
        return t, cols, [dict(r.attrib) for r in t.findall("./rows/row")]
    except Exception:
        return None, [], []


def krs_rows():
    out = {}
    for m in sorted(os.listdir(paths.MODULES)):
        base = os.path.join(paths.MODULES, m, "Data", "Libs", "Tables")
        for dp, _, fn in os.walk(base):
            for f in fn:
                if not f.endswith(".xml"):
                    continue
                table = f.split("__")[0]
                _, _, rows = rows_of(open(os.path.join(dp, f), "rb").read())
                for r in rows:
                    out[(table, tuple(r.get(k, "") for k in KEYS.get(table, [])))] = m
    return out


def patch_files(folder):
    """yield (label, filename, bytes) for loose table xml files and ZIP paks under folder."""
    for dp, _, fn in os.walk(folder):
        for f in fn:
            p = os.path.join(dp, f)
            low = p.replace("\\", "/").lower()
            if f.lower().endswith(".xml") and "/tables/" in low:
                yield os.path.relpath(p, folder), f, open(p, "rb").read()
            elif f.lower().endswith(".pak"):
                try:
                    z = zipfile.ZipFile(p)
                except zipfile.BadZipFile:
                    yield os.path.relpath(p, folder), None, None
                    continue
                for zi in z.infolist():
                    n = zi.filename.replace("\\", "/")
                    if n.lower().endswith(".xml") and "tables/" in n.lower():
                        try:
                            raw = z.open(zi).read()
                        except zipfile.BadZipFile:
                            zi.orig_filename = zi.filename.replace("/", "\\")
                            raw = z.open(zi).read()
                        yield f"{os.path.relpath(p, folder)}!{n}", os.path.basename(n), raw


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True)
    ap.add_argument("--work", default=os.path.join(os.environ.get("TEMP", "."), "krs_archive_scratch"))
    ap.add_argument("--max-extract-mb", type=int, default=15)
    a = ap.parse_args()
    if not os.path.exists(SEVENZ):
        raise SystemExit("7-Zip not found at " + SEVENZ)
    krs = krs_rows()
    results = []
    for arc in sorted(os.listdir(a.src)):
        p = os.path.join(a.src, arc)
        if not os.path.isfile(p) or not re.search(r"\.(zip|7z|rar|7zip)$", arc, re.I):
            continue
        m = NAME.match(re.sub(r"\.(zip|7z|rar|7zip)$", "", arc, flags=re.I))
        nid = int(m.group("id")) if m else ""
        size = os.path.getsize(p)
        dest = os.path.join(a.work, re.sub(r"[^\w.-]+", "_", arc))
        shutil.rmtree(dest, ignore_errors=True)
        os.makedirs(dest)
        listing = subprocess.run([SEVENZ, "l", "-slt", p], capture_output=True, text=True, encoding="utf-8", errors="replace").stdout
        names = re.findall(r"^Path = (.+)$", listing, re.M)[1:]
        full = size <= a.max_extract_mb * 1024 * 1024
        cmd = [SEVENZ, "x", "-y", "-o" + dest, p] + ([] if full else ["*.manifest", "-r"])
        subprocess.run(cmd, capture_output=True)
        manifests = [os.path.join(dp, f) for dp, _, fn in os.walk(dest) for f in fn if f.lower() == "mod.manifest"]
        info = {"archive": arc, "nexus_id": nid, "size_mb": round(size / 1048576, 1), "files": len(names),
                "extracted": "yes" if full else "manifest only", "manifest_modid": "", "effective_id": "", "supports": "",
                "loads_on_1.9.8": "", "layout": "", "table_patches": "", "suffix_ok": "", "problems": "", "krs_collisions": ""}
        kinds = set()
        for n in names:
            low = n.replace("\\", "/").lower()
            if low.endswith(".pak"):
                kinds.add("pak")
            elif "/tables/" in low and low.endswith(".xml"):
                kinds.add("loose table patch")
            elif low.endswith(".lua"):
                kinds.add("lua")
            elif low.endswith((".dds", ".png", ".jpg", ".tga")):
                kinds.add("textures")
            elif low.endswith((".cgf", ".mtl", ".cdf", ".skin")):
                kinds.add("models/materials")
            elif low.endswith(".cfg"):
                kinds.add("cfg")
            elif low.endswith((".gfx", ".xml")):
                kinds.add("xml/ui")
        info["layout"] = ", ".join(sorted(kinds))
        problems = []
        if manifests:
            text = open(manifests[0], encoding="utf-8", errors="replace").read().lstrip("﻿")
            try:
                root = ET.fromstring(re.sub(r"^\s*<\?xml[^>]*\?>", "", text))
                inf = root.find("info")
                modid = (inf.findtext("modid") or "").strip() if inf is not None else ""
                name = (inf.findtext("name") or "").strip() if inf is not None else ""
                vers = [v.text.strip() for v in root.findall("./supports/kcd_version") if v.text]
            except ET.ParseError as e:
                problems.append(f"mod.manifest is not valid XML ({e}); the engine may reject or misread it")
                g = lambda tag: (re.search(rf"<{tag}>([^<]*)</{tag}>", text) or [None, ""])[1].strip()
                modid, name = g("modid"), g("name")
                vers = [v.strip() for v in re.findall(r"<kcd_version>([^<]*)</kcd_version>", text)]
            eff = modid or re.sub(r"\s+", "_", name.lower())
            info.update(manifest_modid=modid, effective_id=eff, supports=" ".join(vers) or "(none)", **{"loads_on_1.9.8": engine_loads(vers)})
            charset_bad = not re.fullmatch(r"[a-z_]+", eff)   # only matters when the mod carries table patches (checked below)
            moddir = os.path.dirname(manifests[0])
            tables, suffix_bad, hits = [], 0, []
            for label, fname, raw in patch_files(moddir) if full else []:
                if fname is None:
                    inner = subprocess.run([SEVENZ, "l", "-slt", os.path.join(moddir, label)], capture_output=True, text=True,
                                           encoding="utf-8", errors="replace").stdout
                    names7 = [n for n in re.findall(r"^Path = (.+)$", inner, re.M)[1:] if n.lower().endswith(".xml")]
                    note = f"{label}: not a ZIP (the game cannot open it)"
                    if names7:
                        note += "; inner files " + ", ".join(names7[:4]) + ("" if any(x.replace("\\", "/").lower().startswith("libs/") for x in names7) else " (no Libs/ root either)")
                    problems.append(note)
                    continue
                base = fname[:-4]
                table = base.split("__")[0]
                tables.append(table)
                if "__" not in base:
                    problems.append(f"{label}: no suffix: replaces the whole vanilla table")
                elif base.split("__", 1)[1].lower() != eff:
                    suffix_bad += 1
                    problems.append(f"{label}: suffix '{base.split('__', 1)[1]}' != id '{eff}' (ignored by the game)")
                t, cols, rows = rows_of(raw)
                for r in rows:
                    if cols and not set(cols) <= set(r):
                        problems.append(f"{label}: partial rows blank columns")
                        break
                for r in rows:
                    k = (table, tuple(r.get(c, "") for c in KEYS.get(table, [])))
                    if k in krs:
                        hits.append(f"{krs[k]}:{table}:{'/'.join(k[1])}")
            if tables and charset_bad:
                problems.append(f"id '{eff}' has characters other than lowercase letters and underscore (the engine warns; patches may not apply)")
            info["table_patches"] = ", ".join(sorted(set(tables)))
            info["suffix_ok"] = ("no" if suffix_bad else "yes") if tables else ""
            info["krs_collisions"] = "; ".join(sorted(set(hits)))[:300]
        else:
            info["loads_on_1.9.8"] = "no manifest in the archive (legacy install: copy into Data)"
            for label, fname, raw in patch_files(dest) if full else []:
                if fname is None:
                    inner = subprocess.run([SEVENZ, "l", "-slt", os.path.join(dest, label)], capture_output=True, text=True,
                                           encoding="utf-8", errors="replace").stdout
                    names7 = [n for n in re.findall(r"^Path = (.+)$", inner, re.M)[1:] if n.lower().endswith(".xml")]
                    problems.append(f"{label}: not a ZIP (the game cannot open it); inner files " + ", ".join(names7[:4])
                                    + ("" if any(x.replace("\\", "/").lower().startswith("libs/") for x in names7) else " (no Libs/ root either)"))
        info["problems"] = " | ".join(dict.fromkeys(problems))[:400]
        results.append(info)
    out = os.path.join(paths.MODS_REVIEW, "archive_analysis.csv")
    cols = list(results[0].keys())
    with open(out, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols, lineterminator="\n")
        w.writeheader()
        w.writerows(results)
    print(f"{len(results)} archives analysed -> {os.path.relpath(out, paths.ROOT)}")
    for r in results:
        print(f"{r['nexus_id']!s:>5} {r['archive'][:48]:48} {r['loads_on_1.9.8'][:34]:34} {r['table_patches'][:40]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
