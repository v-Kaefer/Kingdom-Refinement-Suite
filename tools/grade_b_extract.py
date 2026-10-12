#!/usr/bin/env python3
"""
grade_b_extract.py - READ-ONLY file-by-file inventory and value comparison of the Grade B mods.

    python tools/grade_b_extract.py                 all Grade B mods (list in mod_subcategories.csv)
    python tools/grade_b_extract.py --ids 2011 1483 only these ids
    python tools/grade_b_extract.py --out <folder>  where the CSV/JSON files go (default docs/mods-review)

For every archive of a Grade B mod it lists the archive (7-Zip, nothing extracted), extracts it into a scratch folder, walks EVERY
file (also the members of every .pak, which are ZIPs), compares each file with the unmodified game (the replica install: CRC of every
member of every game pak, tables row by row and cell by cell, localization strings, Lua scripts line by line) and deletes the scratch
folder. Nothing is installed, executed or loaded by the game. The game files are only read.

Writes (GENERATED, docs/mods-review/):
    grade_b_files.csv   one row per file: where it is, size, sha256, role, relation to the game (new / identical / replaces / patches a table)
    grade_b_cells.csv   one row per changed or new table row/cell: table, row key (with the item or perk name), column, old value, new value
    grade_b_text.csv    one row per changed or new localization string
    grade_b_scripts.json  Lua and other text files: line counts against the game's file, the diff and the first lines of new files
    grade_b_summary.json  per mod: counts, tables, whole-table replacements, problems
    grade_b_newrows.json  every new table row with all its attributes
"""
import argparse
import collections
import csv
import difflib
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import zipfile
import zlib
import xml.etree.ElementTree as ET

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import audit_tables as at  # noqa: E402
import audit_mods_deep as amd  # noqa: E402
import paths  # noqa: E402

D = paths.MODS_REVIEW
at.KEYS.setdefault("soul", ["soul_id"])   # the generic key (every *_id column) would turn a changed hair or brain id into a "new" row
GAME = os.environ.get("KCD_GAME", r"E:\Kingdom-Refinement-Suite\WIP_Mods\KingdomComeDeliverance")
WIP = r"E:\Kingdom-Refinement-Suite\WIP_Mods"
SEVENZ = amd.SEVENZ
MAXTEXT = 40 * 1024 * 1024


def norm_path(p):
    return p.replace("\\", "/").lower()


class Game:
    """what the unmodified game ships: CRC index of every pak member, vanilla tables, Lua hashes, names of uuids"""

    def __init__(self):
        self.tables = at.load_vanilla(GAME)
        self.crc = collections.defaultdict(list)    # normalized member path -> [(pak, crc, size)]
        self.lua = {}
        self.eng = {}                               # localization key -> text (English)
        self.names = {}                             # uuid -> internal name
        self._index_paks()
        self._index_names()
        self._index_english()
        self.ref = self._load_reference()

    def _load_reference(self):
        """the 2020 reference tables (Data/Tables_reference.pak): the older state of the game that many mods were made on"""
        out = {}
        p = os.path.join(GAME, "Data", "Tables_reference.pak")
        if not os.path.exists(p):
            return out
        z = zipfile.ZipFile(p)
        for zi in z.infolist():
            if zi.filename.lower().endswith(".xml") and "/reference/" in zi.filename.lower():
                t = at.parse_table(at.read_member(z, zi))
                if t:
                    out[t[0]] = {"cols": t[1], "rows": t[2]}
        return out

    def _index_paks(self):
        for sub in ("Data", "Localization"):
            base = os.path.join(GAME, sub)
            for f in sorted(os.listdir(base)):
                if not f.lower().endswith(".pak"):
                    continue
                try:
                    z = zipfile.ZipFile(os.path.join(base, f))
                except zipfile.BadZipFile:
                    continue
                for zi in z.infolist():
                    if zi.is_dir():
                        continue
                    n = norm_path(zi.filename)
                    self.crc[n].append((f"{sub}/{f}", zi.CRC, zi.file_size))
                    if f.lower().startswith("scripts") and n.endswith(".lua"):
                        self.lua.setdefault(n, (f, z, zi))

    def _index_names(self):
        order = ["item", "perk", "buff", "soul", "food", "recipe"]
        names = {}
        for tname, t in sorted(self.tables.items(), key=lambda kv: (order.index(kv[0]) if kv[0] in order else 99, kv[0])):
            if tname == "__text__":
                continue
            cols = t["cols"]
            namecols = sorted([c for c in cols if (c.endswith("_name") or c == "name") and c not in ("computer_name", "user_name")], key=lambda c: (c != tname + "_name", c))
            idcols = [c for c in cols if c.endswith("_id")]
            if not namecols:
                continue
            for r in t["rows"]:
                nm = r.get(namecols[0], "")
                if not nm:
                    continue
                for c in idcols:
                    v = r.get(c, "")
                    if re.fullmatch(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}", v) and v not in names:
                        names[v] = nm
        self.names = names

    def _index_english(self):
        for r in self.tables["__text__"]["rows"]:
            self.eng[r["key"]] = r["text"]

    def label(self, guid):
        if guid == "00000000-0000-0000-0000-000000000000":
            return "(vazio)"
        n = self.names.get(guid)
        return f"{n} [{guid[:8]}]" if n else guid

    def lua_same(self, path, data):
        n = norm_path(path)
        i = n.find("scripts/")
        key = n[i:] if i >= 0 else n
        h = hashlib.sha256(data).hexdigest()
        v = self.lua.get(key)
        if not v:
            return "new", None
        f, z, zi = v
        vd = at.read_member(z, zi)
        return ("identical" if hashlib.sha256(vd).hexdigest() == h else "differs"), vd

    def relation(self, path, crc):
        """new / identical / replaces, for a file that is not a table patch"""
        n = norm_path(path)
        hits = self.crc.get(n)
        if not hits:
            # try without a leading mod folder: Mods/<id>/Data/<x> or <anything>/Data/<x>
            m = re.search(r"(?:^|/)(libs/|scripts/|textures/|objects/|animations/|sounds/|ui/|config/|engine/|prefabs/|levels/|localization/)(.*)$", n)
            if m:
                hits = self.crc.get(m.group(1) + m.group(2))
        if not hits:
            return "new file (not in the game)", ""
        for pak, c, s in hits:
            if c == crc:
                return "identical to the game's file", pak
        return "replaces the game's file", hits[0][0]


def role_of(path, ext):
    p = norm_path(path)
    base = p.split("/")[-1]
    if base == "mod.manifest":
        return "manifest"
    if ext == ".pak":
        return "container (.pak)"
    if ext == ".xml" and ("libs/tables/" in p or "/tables/" in p or p.startswith("tables/")):
        return "table patch"
    if ext == ".xml" and ("localization" in p or base.startswith("text_") or base.startswith("text__")):
        return "localization"
    if ext == ".lua":
        return "Lua script"
    if ext in (".cfg", ".ini"):
        return "config"
    if ext in (".txt", ".md", ".pdf", ".html", ".htm", ".rtf", ".docx"):
        return "documentation"
    if ext in (".dds", ".png", ".jpg", ".jpeg", ".tga", ".tif", ".bmp", ".gif"):
        return "texture or image"
    if ext in (".cgf", ".cga", ".skin", ".mtl", ".cdf", ".chr", ".dba"):
        return "model or material"
    if ext in (".caf", ".adb", ".img", ".animevents", ".bspace", ".ik"):
        return "animation"
    if ext in (".fsb", ".fev", ".wav", ".ogg", ".mp3"):
        return "audio"
    if ext in (".gfx", ".swf"):
        return "UI (flash)"
    if ext == ".xml":
        return "other xml"
    if ext in (".7z", ".7zip", ".rar", ".zip"):
        return "nested archive"
    if ext in (".dll", ".asi", ".exe", ".bat", ".cmd", ".ps1"):
        return "native or script (risk)"
    return "other"


def read_table_rows(raw):
    p = at.parse_table(raw)
    if not p:
        return None
    tname, cols, rows = p
    if not cols and rows:
        cols = sorted(set().union(*[set(r) for r in rows]))
    return tname, cols, rows


def analyse_archive(mod_id, archive_path, work, game, out):
    """returns summary dict; appends rows to out['files'], out['cells'], out['text'], out['scripts']"""
    name = os.path.basename(archive_path)
    summary = {"id": mod_id, "archive": name, "problems": [], "tables": {}, "files": 0}
    is_dir = os.path.isdir(archive_path)
    scratch = None
    if is_dir:
        root = archive_path
    else:
        entries, info = amd.seven_list(archive_path)
        findings = amd.judge_listing(entries)
        summary["listing_findings"] = [f"{l}: {t}" for l, t in findings]
        scratch = os.path.join(work, f"{mod_id}_{abs(hash(name)) % 100000}")
        shutil.rmtree(scratch, ignore_errors=True)
        os.makedirs(scratch)
        r = subprocess.run([SEVENZ, "x", "-y", "-aoa", "-bd", "-bso0", "-bsp0", "-o" + scratch, archive_path], capture_output=True, text=True, encoding="utf-8", errors="replace")
        if r.returncode not in (0, 1):
            summary["problems"].append(f"7-Zip extract exit {r.returncode}")
        root = scratch
    try:
        files = []
        for dp, dn, fn in os.walk(root):
            for f in sorted(fn):
                p = os.path.join(dp, f)
                files.append((os.path.relpath(p, root).replace("\\", "/"), p))
        for rel, p in sorted(files):
            handle_file(mod_id, name, rel, p, game, out, summary)
    finally:
        if scratch:
            amd.rm_tree(scratch)
    summary["files"] = sum(1 for r in out["files"] if r["id"] == mod_id and r["archive"] == name)
    return summary


def sha_file(p):
    h = hashlib.sha256()
    crc = 0
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
            crc = zlib.crc32(b, crc)
    return h.hexdigest(), crc & 0xFFFFFFFF


def add_file(out, mod_id, archive, container, path, size, sha, role, rel, vpak, note=""):
    out["files"].append({"id": mod_id, "archive": archive, "container": container, "path": path, "bytes": size, "sha256": sha, "role": role,
                         "vs_game": rel, "game_pak": vpak, "note": note})


def handle_file(mod_id, archive, rel, p, game, out, summary):
    ext = os.path.splitext(rel.lower())[1]
    size = os.path.getsize(p)
    sha, crc = sha_file(p)
    role = role_of(rel, ext)
    if role == "container (.pak)":
        add_file(out, mod_id, archive, "", rel, size, sha, role, "container", "")
        handle_pak(mod_id, archive, rel, p, game, out, summary)
        return
    handle_member(mod_id, archive, "", rel, size, sha, crc, role, ext, lambda: open(p, "rb").read(MAXTEXT), game, out, summary)


def handle_pak(mod_id, archive, rel, p, game, out, summary):
    try:
        z = zipfile.ZipFile(p)
    except zipfile.BadZipFile:
        summary["problems"].append(f"{rel}: not a ZIP (the game cannot read it)")
        return
    for zi in z.infolist():
        if zi.is_dir():
            continue
        n = zi.filename.replace("\\", "/")
        ext = os.path.splitext(n.lower())[1]
        role = role_of(n, ext)
        if "localization" in rel.lower() or rel.lower().endswith("_xml.pak"):
            if ext == ".xml" and role not in ("table patch",):
                role = "localization"

        def reader(z=z, zi=zi):
            return at.read_member(z, zi)[:MAXTEXT] if zi.file_size <= MAXTEXT else b""
        data_sha = ""
        try:
            raw = at.read_member(z, zi) if zi.file_size <= MAXTEXT else b""
            data_sha = hashlib.sha256(raw).hexdigest() if raw else ""
        except Exception:  # noqa: BLE001
            raw = b""
        handle_member(mod_id, archive, rel, n, zi.file_size, data_sha, zi.CRC, role, ext, lambda raw=raw: raw, game, out, summary)


def handle_member(mod_id, archive, container, path, size, sha, crc, role, ext, reader, game, out, summary):
    if role == "table patch":
        data = reader()
        handle_table(mod_id, archive, container, path, size, sha, data, game, out, summary)
        return
    if role == "localization" and ext == ".xml":
        data = reader()
        handle_text(mod_id, archive, container, path, size, sha, crc, data, game, out, summary)
        return
    rel, vpak = game.relation(path, crc)
    note = ""
    if role == "Lua script":
        data = reader()
        state, vd = game.lua_same(path, data)
        txt = data.decode("utf-8", "replace")
        entry = {"id": mod_id, "archive": archive, "container": container, "path": path, "lines": txt.count("\n") + 1, "state": state}
        if state == "differs":
            d = list(difflib.unified_diff(vd.decode("utf-8", "replace").splitlines(), txt.splitlines(), "game", "mod", lineterm="", n=2))
            entry["diff_lines"] = len(d)
            entry["added"] = sum(1 for x in d if x.startswith("+") and not x.startswith("+++"))
            entry["removed"] = sum(1 for x in d if x.startswith("-") and not x.startswith("---"))
            entry["diff"] = "\n".join(d[:400])
            rel = "replaces the game's file"
        elif state == "new":
            entry["head"] = "\n".join(txt.splitlines()[:120])
        out["scripts"].append(entry)
        note = f"Lua: {state}"
    elif role in ("other xml", "config", "documentation", "manifest") and ext in (".xml", ".cfg", ".ini", ".txt", ".md", ".manifest"):
        data = reader()
        txt = data.decode("utf-8", "replace")
        entry = {"id": mod_id, "archive": archive, "container": container, "path": path, "lines": txt.count("\n") + 1, "state": rel}
        if role != "documentation":
            entry["head"] = "\n".join(txt.splitlines()[:80])
        else:
            entry["head"] = "\n".join(txt.splitlines()[:60])
        if rel == "replaces the game's file":
            # find the game's version to diff (only xml/cfg inside paks of Data)
            n = norm_path(path)
            hit = None
            for pakname, c, s in game.crc.get(n, [])[:1]:
                zp = zipfile.ZipFile(os.path.join(GAME, pakname.replace("/", os.sep)))
                for zi in zp.infolist():
                    if norm_path(zi.filename) == n:
                        hit = at.read_member(zp, zi)
                        break
            if hit is not None and len(hit) < MAXTEXT:
                d = list(difflib.unified_diff(hit.decode("utf-8", "replace").splitlines(), txt.splitlines(), "game", "mod", lineterm="", n=1))
                entry["added"] = sum(1 for x in d if x.startswith("+") and not x.startswith("+++"))
                entry["removed"] = sum(1 for x in d if x.startswith("-") and not x.startswith("---"))
                entry["diff"] = "\n".join(d[:300])
        out["scripts"].append(entry)
    add_file(out, mod_id, archive, container, path, size, sha, role, rel, vpak, note)


def handle_table(mod_id, archive, container, path, size, sha, data, game, out, summary):
    base = os.path.basename(path)[:-4]
    parsed = read_table_rows(data)
    if not parsed:
        add_file(out, mod_id, archive, container, path, size, sha, "table patch", "not readable", "", "malformed XML or not a table")
        summary["problems"].append(f"{path}: not a readable table")
        return
    tname, cols, rows = parsed
    vb, style = at.base_table(tname or base.split("__")[0], game.tables)
    if vb is None:
        add_file(out, mod_id, archive, container, path, size, sha, "table patch", "table not in the game", "", f"table '{tname}'")
        summary["problems"].append(f"{path}: table '{tname}' is not in the game")
        return
    suffix = base.split("__", 1)[1] if "__" in base else ""
    vcols = game.tables[vb]["cols"]
    extra = [x for x in cols if x not in vcols]
    missing = [x for x in vcols if x not in cols]
    stray = sorted({x for r in rows for x in r if x not in cols})
    if extra or missing or stray:
        msg = f"{path}: " + "; ".join(filter(None, [
            ("header columns not in the game's table: " + ", ".join(extra)) if extra else "",
            ("columns of the game's table missing from the header (rule 5: they are blanked): " + ", ".join(missing)) if missing else "",
            ("row attributes not declared in the header: " + ", ".join(stray)) if stray else ""]))
        summary["problems"].append(msg)
    c = at.classify(vb, game.tables[vb], cols, rows)
    whole = "" if suffix else "replaces the whole game table"
    rel = "patches a game table (suffix __%s)" % suffix if suffix else "replaces the whole game table (no suffix)"
    note = f"{vb}: {c['new']} new, {c['changed']} changed, {c['same']} identical rows" + (f", {c['dropped_vs_vanilla']} game rows dropped" if not suffix else "")
    add_file(out, mod_id, archive, container, path, size, sha, "table patch", rel, "Data/Tables.pak", note)
    ts = summary["tables"].setdefault(vb, {"files": 0, "new": 0, "changed": 0, "same": 0, "dropped": 0, "whole": False, "suffixes": set()})
    ts["files"] += 1
    ts["new"] += c["new"]
    ts["changed"] += c["changed"]
    ts["same"] += c["same"]
    ts["dropped"] += c["dropped_vs_vanilla"] if not suffix else 0
    ts["whole"] = ts["whole"] or not suffix
    ts["suffixes"].add(suffix)
    kc = c["key_cols"]
    ridx = {}
    if vb in game.ref:
        for rr in game.ref[vb]["rows"]:
            ridx.setdefault(tuple(at.norm(rr.get(cc)) for cc in kc), rr)
    for kind, k, diffs, row in c["details"]:
        if kind == "same":
            continue
        keytxt = " / ".join(game.label(v) if re.fullmatch(r"[0-9a-f]{8}-.*", v) else v for v in k)
        if kind == "new":
            out["newrows"].append({"id": mod_id, "archive": archive, "container": container, "table": vb, "key": keytxt, "key_raw": "|".join(k), "row": {c_: row.get(c_, "") for c_ in cols}})
            nm = ""
            for col in cols:
                if (col.endswith("_name") or col == "name") and col not in ("computer_name", "user_name"):
                    nm = row.get(col, "")
                    break
            out["cells"].append({"id": mod_id, "archive": archive, "container": container, "file": path, "table": vb, "key": keytxt, "key_raw": "|".join(k), "kind": "new row", "column": "*",
                                 "old": "", "new": nm or json.dumps({c_: row.get(c_) for c_ in cols if c_ not in kc and row.get(c_) not in (None, "")}, ensure_ascii=False)[:300],
                                 "ref2020": "row exists in the 2020 reference (the game later removed it)" if k in ridx else ("(table not in the reference)" if vb not in game.ref else "row not in the 2020 reference"),
                                 "origin": "restores a removed game row" if k in ridx else "new content"})
        else:
            rr = ridx.get(k)
            for col, (o, n) in diffs.items():
                blank0 = (n == "" and o.strip() in ("0", "0.0")) or (o == "" and n.strip() in ("0", "0.0"))
                if blank0:
                    ref, origin = (at.norm(rr.get(col)) if rr is not None else ""), "blank cell versus 0 (probably the same value: not a real change, unverified)"
                elif rr is None:
                    ref, origin = ("(row not in the 2020 reference)" if vb in game.ref else "(table not in the reference)"), "deliberate change (no older value to compare)"
                else:
                    ref = at.norm(rr.get(col))
                    origin = "stale: equals the 2020 reference, the game changed it later" if ref == at.norm(n) else ("deliberate change" if ref == at.norm(o) else "deliberate change (the game also changed this cell since 2020)")
                out["cells"].append({"id": mod_id, "archive": archive, "container": container, "file": path, "table": vb, "key": keytxt, "key_raw": "|".join(k), "kind": "changed", "column": col,
                                     "old": o, "new": n, "ref2020": ref, "origin": origin})


def handle_text(mod_id, archive, container, path, size, sha, crc, data, game, out, summary):
    rel, vpak = game.relation(path, crc)
    n_new = n_chg = 0
    try:
        root = ET.fromstring(re.sub(r"^\s*<\?xml[^>]*\?>", "", data.decode("utf-8", "replace").lstrip("\ufeff")))
    except ET.ParseError:
        add_file(out, mod_id, archive, container, path, size, sha, "localization", "not readable", "", "malformed XML")
        summary["problems"].append(f"{path}: localization file is not well-formed XML")
        return
    for row in root.iter("Row"):
        cells = [c.text or "" for c in row.findall("Cell")]
        if len(cells) < 2 or not cells[0]:
            continue
        old = game.eng.get(cells[0])
        if old is None:
            n_new += 1
            out["text"].append({"id": mod_id, "archive": archive, "container": container, "file": path, "key": cells[0], "kind": "new string", "old": "", "new": cells[1]})
        elif old != cells[1]:
            n_chg += 1
            out["text"].append({"id": mod_id, "archive": archive, "container": container, "file": path, "key": cells[0], "kind": "changed string", "old": old, "new": cells[1]})
    note = f"{n_chg} strings changed, {n_new} new (compared with the game's English text)"
    add_file(out, mod_id, archive, container, path, size, sha, "localization", "patch of the game's text" if "__" in os.path.basename(path) else rel, vpak, note)


def b_mods():
    return [r for r in csv.DictReader(open(os.path.join(D, "mod_subcategories.csv"), encoding="utf-8")) if r["grade"].startswith("B")]


def find_archive(entry):
    for dp, dn, fn in os.walk(WIP):
        depth = dp[len(WIP):].count(os.sep)
        if "KingdomComeDeliverance" in dp.split(os.sep) or depth > 3:
            dn[:] = []
            continue
        if entry in dn + fn:
            return os.path.join(dp, entry)
    return None


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--ids", nargs="*")
    ap.add_argument("--out", default=D)
    ap.add_argument("--work", default=os.path.join(os.environ.get("TEMP", "."), "gb"))
    a = ap.parse_args()
    if not os.path.exists(SEVENZ):
        raise SystemExit("7-Zip not found")
    amd.rm_tree(a.work)
    os.makedirs(a.work)
    game = Game()
    out = {"files": [], "cells": [], "text": [], "scripts": [], "newrows": []}
    ana = list(csv.DictReader(open(os.path.join(D, "mod_analysis.csv"), encoding="utf-8")))
    wanted = {r["id"] for r in b_mods()}
    if a.ids:
        wanted &= set(a.ids)
    summaries = []
    for r in sorted(ana, key=lambda x: (int(x["id"]), x["entry"])):
        if r["id"] not in wanted:
            continue
        if r["id"] == "1009" and r["kind"].startswith("folder"):
            continue   # the extracted 2024 folder: already judged redundant in Reviewed_Mods/_reviewed.csv
        path = find_archive(r["entry"])
        if not path:
            print("NOT FOUND", r["id"], r["entry"])
            continue
        print("reading", r["id"], r["entry"][:60], flush=True)
        s = analyse_archive(r["id"], path, a.work, game, out)
        s["entry"] = r["entry"]
        summaries.append(s)
    amd.rm_tree(a.work)
    for s in summaries:
        for t in s["tables"].values():
            t["suffixes"] = sorted(t["suffixes"])
    w = lambda name, rows, cols: csv.DictWriter(open(os.path.join(a.out, name), "w", encoding="utf-8", newline=""), fieldnames=cols, lineterminator="\n")  # noqa: E731
    for name, rows, cols in (("grade_b_files.csv", out["files"], ["id", "archive", "container", "path", "bytes", "sha256", "role", "vs_game", "game_pak", "note"]),
                             ("grade_b_cells.csv", out["cells"], ["id", "archive", "container", "file", "table", "key", "key_raw", "kind", "column", "old", "new", "ref2020", "origin"]),
                             ("grade_b_text.csv", out["text"], ["id", "archive", "container", "file", "key", "kind", "old", "new"])):
        with open(os.path.join(a.out, name), "w", encoding="utf-8", newline="") as f:
            dw = csv.DictWriter(f, fieldnames=cols, lineterminator="\n")
            dw.writeheader()
            dw.writerows(rows)
    json.dump(out["scripts"], open(os.path.join(a.out, "grade_b_scripts.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    json.dump(summaries, open(os.path.join(a.out, "grade_b_summary.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    json.dump(out["newrows"], open(os.path.join(a.out, "grade_b_newrows.json"), "w", encoding="utf-8"), ensure_ascii=False)
    print(f"{len(summaries)} archives, {len(out['files'])} files, {len(out['cells'])} cell rows, {len(out['text'])} strings, {len(out['scripts'])} text files; scratch removed: {not os.path.exists(a.work)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
