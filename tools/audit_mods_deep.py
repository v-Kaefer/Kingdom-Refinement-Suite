#!/usr/bin/env python3
"""
audit_mods_deep.py - READ-ONLY analysis of the downloaded P1/P2 mods: what they change, how, where, how much, and whether they carry risk.

    python tools/audit_mods_deep.py --src "<downloads folder>"                 analyse every P1/P2 mod that is in the folder
    python tools/audit_mods_deep.py --src "<folder>" --ids 85 1009             only these mod ids
    python tools/audit_mods_deep.py --src "<folder>" --no-quarantine           report risks but move nothing

SAFETY (the archives are untrusted, see docs/mods-review/DOWNLOADS_PLAN.md):
  * Nothing is installed, loaded by the game, or executed. No file taken out of an archive is ever opened by anything but this script's
    own readers (7-Zip to extract, Python to read bytes and text). There is no subprocess call on any extracted file.
  * Each archive is first LISTED (7z l): path traversal, absolute paths, encrypted entries, nested archives, executables, scripts and
    decompression bombs are judged from the listing alone. Archives that fail that judgement are not extracted.
  * The others are extracted into a scratch folder (default %TEMP%\\krs_audit_scratch), read, and the scratch folder of that mod is
    deleted before the next one. Folders and loose .pak files that are already in the downloads folder are read in place and never modified.
  * Risk scan on every file, also inside .pak files (they are ZIPs): native code by magic bytes (MZ, ELF) or extension, scripts and shortcuts
    (.bat .cmd .ps1 .vbs .lnk ...), dangerous Lua calls (os.execute, io.popen, package.loadlib ...), downloader/obfuscation strings in scripts,
    nested archives, symlinks. HIGH risk archives are moved to <src>/_quarantine/ (a move, undoable with the manifest there).
  * The vanilla tables are read from the game's Tables.pak (read only) to measure what each table patch changes.

Outputs (docs/mods-review/, GENERATED): mod_analysis.csv, mod_tables.csv, mod_overlap.csv, risk_scan.csv, MOD_ANALYSIS.md, MOD_PROFILES.md, QUARANTINE.md.
"""
import argparse
import collections
import csv
import datetime
import hashlib
import os
import re
import shutil
import statistics
import subprocess
import sys
import zipfile
import xml.etree.ElementTree as ET

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import audit_tables as at  # noqa: E402
import analyze_mod_archives as ama  # noqa: E402
import paths  # noqa: E402

D = paths.MODS_REVIEW
SEVENZ = ama.SEVENZ
GAME = os.environ.get("KCD_GAME", r"E:\Kingdom-Refinement-Suite\Mods WIP folder\KingdomComeDeliverance")
MAX_EXTRACT_MB = 400          # larger archives: only text-like files and small paks are extracted
MAX_PAK_MB = 200
MAX_MEMBER = 6 * 1024 * 1024  # bytes read from one text file
BOMB_RATIO = 300

NATIVE_EXT = {".exe", ".dll", ".asi", ".scr", ".sys", ".com", ".msi", ".cpl", ".ocx", ".drv"}
SCRIPT_EXT = {".bat", ".cmd", ".ps1", ".psm1", ".vbs", ".vbe", ".wsf", ".wsh", ".hta", ".lnk", ".jar", ".py", ".sh", ".reg", ".js", ".jse",
              ".url", ".application", ".gadget", ".inf"}
ARCHIVE_EXT = {".zip", ".7z", ".rar", ".gz", ".tar", ".cab", ".iso", ".7zip"}
TEXT_EXT = {".xml", ".lua", ".cfg", ".txt", ".md", ".json", ".ini", ".manifest", ".csv", ".html", ".htm", ".readme", ".log", ".bat", ".cmd",
            ".ps1", ".vbs", ".js", ".py", ".sh", ".inf", ".reg", ".url", ".lnk"}
DOC_EXT = {".txt", ".md", ".html", ".htm", ".readme", ".pdf", ".rtf"}
LUA_BAD = [
    (r"\bos\.execute\b", "os.execute"), (r"\bio\.popen\b", "io.popen"), (r"\bpackage\.loadlib\b", "package.loadlib"),
    (r"\bos\.(remove|rename|exit|tmpname|getenv)\b", "os.remove/rename/exit/getenv"), (r"\bio\.open\b", "io.open"),
    (r"\bloadstring\b|\bloadfile\b|\bdofile\b", "loadstring/loadfile/dofile"), (r"\bstring\.dump\b", "string.dump"),
    (r"\bffi\.", "ffi"), (r"\bdebug\.(sethook|getinfo|setmetatable|getregistry)\b", "debug.*"),
]
SCRIPT_STR = re.compile(r"powershell|cmd\.exe|wscript|cscript|mshta|certutil|bitsadmin|invoke-expression|invoke-webrequest|downloadstring|"
                        r"frombase64string|regsvr32|rundll32|schtasks|reg add|net user|taskkill|\bwget\b|\bcurl\b", re.I)
URL = re.compile(r"https?://[^\s\"'<>)\]]+", re.I)
URL_OK = re.compile(r"nexusmods|github\.com|discord|patreon|ko-fi|buymeacoffee|youtube|youtu\.be|steamcommunity|store\.steampowered|"
                    r"warhorsestudios|kingdomcomerpg|w3\.org|schemas|moddb|paypal\.me|crowdin|imgur|reddit", re.I)
B64 = re.compile(r"[A-Za-z0-9+/]{240,}={0,2}")
REQ_WORDS = [("kcse", "KCSE (script extender, native)"), ("script extender", "script extender"), ("asi loader", "ASI loader"), ("ultimate asi", "ASI loader"),
             ("address library", "Address Library"), ("vortex", "Vortex"), ("reshade", "ReShade"), ("requires", "states requirements"),
             ("required", "states requirements"), ("dependency", "states a dependency"), ("tables.pak", "mentions Tables.pak"),
             ("user.cfg", "user.cfg"), ("autoexec", "autoexec.cfg"), ("repack", "repack"), ("unpack", "unpack"), ("mod order", "mod order")]
CORE_TABLES = ("rpg_param", "perk", "skill", "buff", "weapon", "melee", "armor", "item", "food", "potion", "ammo", "herb", "document",
               "combat", "attack", "damage", "stat", "sleeping", "merchant", "price", "craft", "recipe", "loot", "horse", "crime", "ai", "noble",
               "alchemy", "repair", "durability", "fatigue", "hunger", "xp", "level", "reward")
UI_WORDS = ("ui", "text", "icon", "sound", "music", "audio", "loading", "font", "map")


def rm_tree(path):
    """delete a scratch folder; a long-path prefix lets Windows remove paths longer than 260 characters"""
    p = os.path.abspath(path)
    if os.path.exists(p):
        shutil.rmtree("\\\\?\\" + p, ignore_errors=True)
    if os.path.exists(p):
        shutil.rmtree(p, ignore_errors=True)
    if os.path.exists(p):   # names with trailing dots or spaces: only the shell's rmdir removes them (it deletes a folder, it runs nothing in it)
        subprocess.run(["cmd", "/c", "rmdir", "/s", "/q", "\\\\?\\" + p], capture_output=True)


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def seven_list(path):
    """-> (entries [{path,size,packed,encrypted,folder}], archive info dict); nothing is extracted."""
    out = subprocess.run([SEVENZ, "l", "-slt", "-sccUTF-8", path], capture_output=True, text=True, encoding="utf-8", errors="replace").stdout
    head, _, body = out.partition("----------")
    info = dict(re.findall(r"^(\w[\w ]*?) = (.*)$", head, re.M))
    entries = []
    for block in body.strip().split("\n\n"):
        kv = dict(re.findall(r"^(\w[\w ]*?) = (.*)$", block, re.M))
        if "Path" in kv:
            entries.append({"path": kv["Path"], "size": int(kv.get("Size") or 0), "packed": int(kv.get("Packed Size") or 0),
                            "encrypted": kv.get("Encrypted", "-") == "+", "folder": kv.get("Folder", "-") == "+",
                            "attr": kv.get("Attributes", "")})
    return entries, info


def judge_listing(entries):
    """risk findings from the file list alone: [(level, text)]"""
    f = []
    total = sum(e["size"] for e in entries)
    packed = sum(e["packed"] for e in entries) or 1
    if total > 2 * 1024 ** 3 or (total > 50 * 1024 ** 2 and total / packed > BOMB_RATIO):
        f.append(("MEDIUM", f"decompression-bomb shape: {total // 1048576} MB from {packed // 1048576} MB (not extracted)"))
    for e in entries:
        p = e["path"].replace("\\", "/")
        low = p.lower()
        ext = os.path.splitext(low)[1]
        if e["folder"]:
            continue
        if ".." in p.split("/") or re.match(r"^([a-z]:|/)", p, re.I):
            f.append(("HIGH", f"path traversal or absolute path: {p}"))
        if ":" in p.split("/")[-1]:
            f.append(("HIGH", f"alternate data stream or colon in name: {p}"))
        if e["encrypted"]:
            f.append(("HIGH", f"encrypted entry (cannot be read): {p}"))
        if ext in NATIVE_EXT:
            f.append(("HIGH", f"native code file: {p}"))
        elif ext in SCRIPT_EXT:
            f.append(("HIGH", f"script or shortcut file: {p}"))
        elif ext in ARCHIVE_EXT:
            f.append(("MEDIUM", f"nested archive: {p}"))
        base = os.path.basename(low)
        if re.search(r"\.(jpg|png|dds|txt|xml|pdf|doc)\.(exe|bat|cmd|scr|lnk|js|vbs)$", base) or base != base.rstrip(". "):
            f.append(("HIGH", f"disguised file name: {p}"))
    return f


SUSPICIOUS_STR = [b"WinExec", b"CreateProcess", b"ShellExecute", b"URLDownloadToFile", b"InternetOpen", b"InternetReadFile", b"WinHttp", b"WSAStartup",
                  b"WriteProcessMemory", b"CreateRemoteThread", b"VirtualAllocEx", b"SetWindowsHookEx", b"GetAsyncKeyState", b"RegSetValue",
                  b"CryptEncrypt", b"CreateService", b"http://", b"https://", b".onion", b"webhook", b"pastebin", b"powershell", b"cmd.exe", b"schtasks"]
GAME_STR = re.compile(rb"kcd|rpg|perk|henry|attack|param|master|strike|riposte|durab|repair|lua|\.ini|\.cfg|\.xml|hook|patch|config|horse|combat|tune|plugin", re.I)


def native_strings(path):
    """static reading of a native file's printable strings: suspicious API or URL strings, and game-related ones that show what it hooks"""
    raw = open(path, "rb").read(12 * 1024 * 1024)
    strs = re.findall(rb"[\x20-\x7e]{6,}", raw)
    sus = sorted({k.decode() for k in SUSPICIOUS_STR if any(k.lower() in s.lower() for s in strs)})
    game = []
    for s_ in strs:
        if GAME_STR.search(s_) and len(s_) < 90:
            t = s_.decode()
            if t not in game:
                game.append(t)
        if len(game) >= 14:
            break
    return "suspicious strings: " + (", ".join(sus) or "none") + "; game-related strings: " + " / ".join(game[:14])


VANILLA_LUA = {}   # lower-case path from "scripts/" on -> sha256 of the vanilla script (Scripts.pak), to tell mod scripts from vanilla copies


def load_vanilla_lua(game):
    out = {}
    z = zipfile.ZipFile(os.path.join(game, "Data", "Scripts.pak"))
    for zi in z.infolist():
        n = zi.filename.replace("\\", "/").lower()
        if n.endswith(".lua") and not zi.is_dir():
            out[n] = hashlib.sha256(at.read_member(z, zi)).hexdigest()
    return out


def lua_is_vanilla(vp, raw):
    low = vp.lower().replace("\\", "/").split("!")[-1]
    i = low.find("scripts/")
    return i >= 0 and VANILLA_LUA.get(low[i:]) == hashlib.sha256(raw).hexdigest()


class Source:
    """the readable content of one mod: virtual files (real files and members of .pak ZIPs) with lazy readers."""

    def __init__(self):
        self.files = []            # (vpath, size, reader or None)
        self.notes = []            # reading problems
        self.findings = []         # (level, text)
        self.native_sha = {}       # vpath -> sha256 of native files
        self.native_info = {}      # vpath -> text about suspicious imports/strings and game-related strings

    def add_tree(self, root):
        for dp, dn, fn in os.walk(root):
            for name in fn:
                p = os.path.join(dp, name)
                rel = os.path.relpath(p, root).replace("\\", "/")
                try:
                    if os.path.islink(p) or (getattr(os.stat(p), "st_file_attributes", 0) & 0x400):
                        self.findings.append(("HIGH", f"symbolic link or reparse point: {rel}"))
                        continue
                    self.add_file(p, rel)
                except OSError as e:
                    self.notes.append(f"{rel}: {e}")

    def add_file(self, p, rel):
        size = os.path.getsize(p)
        ext = os.path.splitext(rel.lower())[1]
        with open(p, "rb") as f:
            magic = f.read(4)
        if magic[:2] == b"MZ" or magic[:4] == b"\x7fELF":
            self.findings.append(("HIGH", f"native binary by magic bytes: {rel}"))
            self.native_sha[rel] = sha256(p)
            self.native_info[rel] = native_strings(p)
        elif magic[:4] == b"L\x00\x00\x00" and ext != ".dds":
            self.findings.append(("HIGH", f"Windows shortcut by magic bytes: {rel}"))
        elif magic[:2] == b"#!":
            self.findings.append(("HIGH", f"shebang script: {rel}"))
        if ext in ARCHIVE_EXT:
            self.findings.append(("MEDIUM", f"nested archive (not readable by the game): {rel}"))
        self.files.append((rel, size, lambda p=p: open(p, "rb").read(MAX_MEMBER)))
        if ext == ".pak":
            self.add_pak(p, rel, size)

    def add_pak(self, p, rel, size):
        try:
            z = zipfile.ZipFile(p)
        except zipfile.BadZipFile:
            self.notes.append(f"{rel}: not a ZIP (the game cannot read it either)")
            return
        for zi in z.infolist():
            if zi.is_dir():
                continue
            n = zi.filename.replace("\\", "/")
            vp = f"{rel}!{n}"
            ext = os.path.splitext(n.lower())[1]
            if ".." in n.split("/") or re.match(r"^([a-z]:|/)", n, re.I):
                self.findings.append(("HIGH", f"path traversal inside pak: {vp}"))
            if ext in NATIVE_EXT or ext in SCRIPT_EXT:
                self.findings.append(("HIGH", f"{'native code' if ext in NATIVE_EXT else 'script'} file inside pak: {vp}"))
            if zi.flag_bits & 1:
                self.findings.append(("HIGH", f"encrypted entry inside pak: {vp}"))
                continue
            self.files.append((vp, zi.file_size, lambda z=z, zi=zi: at.read_member(z, zi)[:MAX_MEMBER] if zi.file_size <= MAX_MEMBER * 4 else b""))


def text_of(raw):
    return raw.decode("utf-8", "replace").lstrip("\ufeff")


def scan_text_risks(src):
    """Lua, config and script content: dangerous calls, downloader strings, URLs, base64 blobs."""
    lua_use = collections.Counter()
    for vp, size, rd in src.files:
        ext = os.path.splitext(vp.lower().split("!")[-1])[1]
        if ext not in TEXT_EXT or size > MAX_MEMBER * 4:
            continue
        try:
            t = text_of(rd())
        except Exception as e:  # noqa: BLE001
            src.notes.append(f"{vp}: unreadable ({e})")
            continue
        if ext == ".lua" and lua_is_vanilla(vp, rd()):
            continue   # byte-identical to the game's own script: not the mod's code
        if ext == ".lua":
            for pat, label in LUA_BAD:
                if re.search(pat, t):
                    lua_use[label] += 1
                    lvl = "HIGH" if label in ("os.execute", "io.popen", "package.loadlib", "ffi", "string.dump") else "MEDIUM"
                    src.findings.append((lvl, f"Lua {label} in {vp}"))
        if ext == ".lua":   # comments are not code: URLs and words inside them do not count
            t = re.sub(r"--\[\[.*?\]\]", "", t, flags=re.S)
            t = re.sub(r"--[^\n]*", "", t)
        if ext not in DOC_EXT and SCRIPT_STR.search(t):
            src.findings.append(("HIGH" if ext in (".lua", ".bat", ".cmd", ".ps1", ".vbs", ".js") else "MEDIUM", f"command or downloader string in {vp}: {SCRIPT_STR.search(t).group(0)}"))
        if ext not in DOC_EXT:
            bad_urls = [u for u in URL.findall(t) if not URL_OK.search(u)]
            if bad_urls and ext in (".lua", ".bat", ".cmd", ".ps1", ".vbs", ".js", ".py"):
                src.findings.append(("HIGH", f"URL in script {vp}: {bad_urls[0][:80]}"))
            elif bad_urls and ext not in (".xml", ".manifest"):
                src.findings.append(("LOW", f"URL in {vp}: {bad_urls[0][:80]}"))
            if B64.search(t) and "libs/tables/" not in vp.lower().replace("\\", "/"):
                src.findings.append(("MEDIUM", f"long base64-like blob in {vp}"))
    if lua_use.get("loadstring/loadfile/dofile") and lua_use.get("io.open"):
        src.findings.append(("HIGH", "mod Lua loads code dynamically (loadstring/loadfile) and opens files (io.open): a script framework, not a data tweak"))


ID_COL = re.compile(r"(_id|_ids|ui_order|ui_visibility\w*|sort\w*|_order)$", re.I)


def rel_change(old, new):
    try:
        a, b = float(old), float(new)
    except (TypeError, ValueError):
        return None
    if a == b:
        return 0.0
    if a == 0:
        return 1.0
    return min(abs(b - a) / abs(a), 10.0)


def analyse_tables(src, vanilla, krs_keys, eff_id):
    """-> (per-table rows list, set of changed keys, highlights list, relative-change list, problems)"""
    tables, keys, hl, rels, problems = [], set(), [], [], []
    for vp, size, rd in src.files:
        low = vp.lower()
        lowp = low.replace("\\", "/").split("!")[-1]
        if not (lowp.endswith(".xml") and ("libs/tables/" in lowp or lowp.startswith("tables/") or "/tables/" in lowp)):
            continue
        if "libs/tables/" not in lowp:
            problems.append(f"{vp}: table patch outside Libs/Tables (the game looks for Libs/Tables only)")
        raw = rd()
        p = at.parse_table(raw)
        fname = os.path.basename(vp.split("!")[-1])[:-4]
        if not p:
            problems.append(f"{vp}: not a readable table")
            continue
        tname, cols, rows = p
        base, style = at.base_table(tname if tname else fname.split("__")[0], vanilla)
        if base is None:
            base, style = at.base_table(fname, vanilla)
        if base is None:
            tables.append({"vpath": vp, "table": tname or fname, "base": "?", "style": "unknown table", "rows": len(rows), "new": 0, "changed": len(rows), "same": 0,
                           "dropped": 0, "cols": ""})
            problems.append(f"{vp}: table '{tname}' is not in the vanilla game")
            continue
        if style == "exact" and "__" not in fname:
            problems.append(f"{vp}: no suffix: replaces the whole vanilla table")
        elif "__" in fname and eff_id and fname.split("__", 1)[1].lower() != eff_id:
            problems.append(f"{vp}: suffix '{fname.split('__', 1)[1]}' != id '{eff_id}' (the game ignores it)")
        c = at.classify(base, vanilla[base], cols, rows)
        tables.append({"vpath": vp, "table": tname, "base": base, "style": style, "rows": len(rows), "new": c["new"], "changed": c["changed"],
                       "same": c["same"], "dropped": c["dropped_vs_vanilla"], "cols": ",".join(sorted(c["changed_columns"]))[:120]})
        for kind, k, diffs, row in c["details"]:
            if kind == "same":
                continue
            keys.add((base, k))
            if kind == "changed":
                best = None
                for col, (o, n) in diffs.items():
                    rc = None if ID_COL.search(col) else rel_change(o, n)   # identifier and ordering columns are not magnitudes
                    if rc is not None:
                        rels.append(rc)
                        if best is None or rc > best[0]:
                            best = (rc, col, o, n)
                if best:
                    hl.append((best[0], f"{base}:{'/'.join(k)} {best[1]} {best[2]}->{best[3]}"))
                else:
                    col, (o, n) = next(iter(diffs.items()))
                    hl.append((0.05, f"{base}:{'/'.join(k)} {col} {str(o)[:20]}->{str(n)[:20]}"))
            else:
                hl.append((1.0, f"{base}:{'/'.join(k)} NEW row"))
    return tables, keys, hl, rels, problems


def parse_manifest(src):
    for vp, size, rd in src.files:
        if vp.lower().endswith("mod.manifest") and "!" not in vp:
            text = text_of(rd())
            try:
                root = ET.fromstring(re.sub(r"^\s*<\?xml[^>]*\?>", "", text))
                inf = root.find("info")
                modid = (inf.findtext("modid") or "").strip() if inf is not None else ""
                name = (inf.findtext("name") or "").strip() if inf is not None else ""
                ver = (inf.findtext("version") or "").strip() if inf is not None else ""
                vers = [v.text.strip() for v in root.findall("./supports/kcd_version") if v.text]
            except ET.ParseError:
                g = lambda tag: (re.search(rf"<{tag}>([^<]*)</{tag}>", text) or [None, ""])[1].strip()  # noqa: E731
                modid, name, ver = g("modid"), g("name"), g("version")
                vers = [v.strip() for v in re.findall(r"<kcd_version>([^<]*)</kcd_version>", text)]
            eff = modid or re.sub(r"\s+", "_", name.lower())
            return vp, modid, name, ver, vers, eff
    return None


def categorize_paths(src):
    """what kinds of game files the mod carries: (counter by area, lua stats, cfg keys, loc stats, requirements)"""
    area = collections.Counter()
    lua_files, lua_lines, lua_api, lua_same = 0, 0, collections.Counter(), 0
    cfg = []
    loc_rows = []
    reqs = set()
    for vp, size, rd in src.files:
        low = vp.lower().replace("\\", "/").split("!")[-1]
        ext = os.path.splitext(low)[1]
        if low.endswith("mod.manifest"):
            area["manifest"] += 1
        elif ("libs/tables/" in low or "/tables/" in low or low.startswith("tables/")) and ext == ".xml":
            area["tables (PTF)"] += 1
        elif "localization/" in low or re.search(r"text__|text_ui|_xml\.pak", low):
            area["localization"] += 1
            if ext == ".xml":
                loc_rows.append(rd)
        elif ext == ".lua":
            area["scripts (Lua)"] += 1
            lua_files += 1
            try:
                raw = rd()
                if lua_is_vanilla(vp, raw):
                    lua_same += 1
                    continue
                t = text_of(raw)
                lua_lines += t.count("\n") + 1
                lua_api.update(m.group(0) for m in re.finditer(r"\b(?:Events|Script|System|Game|player|entity|XGenAIModule|Console|CPPAPI|Database|RPG)\.[A-Za-z_]+", t))
            except Exception:  # noqa: BLE001
                pass
        elif ext == ".cfg":
            area["config (.cfg)"] += 1
            try:
                for line in text_of(rd()).splitlines():
                    m = re.match(r"^\s*([A-Za-z_][\w.]*)\s*=\s*(\S+)", line)
                    if m and not line.lstrip().startswith(("--", "//", ";")):
                        cfg.append(f"{m.group(1)}={m.group(2)}")
            except Exception:  # noqa: BLE001
                pass
        elif ext in (".dds", ".png", ".jpg", ".tga", ".tif"):
            area["textures"] += 1
        elif ext in (".cgf", ".cga", ".skin", ".mtl", ".cdf", ".chr", ".caf", ".adb", ".bspace", ".ik", ".dba"):
            area["models/animations/materials"] += 1
        elif ext in (".fsb", ".fev", ".wav", ".ogg", ".mp3", ".snd"):
            area["audio"] += 1
        elif ext in (".gfx", ".swf") or "/ui/" in low:
            area["ui"] += 1
        elif ext in (".pak",):
            area["pak (container)"] += 1
        elif ext in (".bat", ".cmd", ".exe", ".dll", ".asi", ".ps1"):
            area["executables/scripts"] += 1
        elif ext in DOC_EXT:
            area["docs"] += 1
            try:
                t = text_of(rd())[:6000].lower()
                for w, label in REQ_WORDS:
                    if w in t:
                        reqs.add(label)
            except Exception:  # noqa: BLE001
                pass
        elif ext == ".xml":
            area["other xml (data)"] += 1
        else:
            area["other"] += 1
    area["lua identical to vanilla"] = lua_same
    return area, lua_files, lua_lines, lua_api, cfg, loc_rows, reqs


def loc_stats(loc_readers, vanilla):
    """how many strings the mod's localization files add or change against the vanilla English text"""
    vt = {r["key"]: r["text"] for r in vanilla["__text__"]["rows"]}
    new = changed = 0
    for rd in loc_readers:
        try:
            root = ET.fromstring(re.sub(r"^\s*<\?xml[^>]*\?>", "", text_of(rd())))
        except ET.ParseError:
            continue
        for row in root.iter("Row"):
            cells = [c.text or "" for c in row.findall("Cell")]
            if len(cells) > 1 and cells[0]:
                if cells[0] not in vt:
                    new += 1
                elif vt[cells[0]] != cells[1]:
                    changed += 1
    return new, changed


def is_core(base):
    return any(base.startswith(w) or w in base for w in CORE_TABLES) and not any(base.startswith(u) for u in ("text", "ui_", "sound"))


def grade(m):
    """returns (grade, perceptibility, why) from the measured numbers; the rules are written out in MOD_ANALYSIS.md"""
    R, T, med = m["rows_changed_or_new"], m["tables_touched"], m["median_rel_change"]
    native = m["native_files"] > 0 or m["needs_external"]
    lua_lines = m["lua_lines"]
    core_rows = m["core_rows"]
    big_core = m["core_rows_ge20pct"]
    if m["readable"] == "no":
        return "X not analysed", "unknown", "nothing readable (see problems)"
    # perceptibility
    if big_core >= 1 or R >= 30 or lua_lines >= 150:
        perc = "high"
    elif R >= 5 or m["cfg_keys"] >= 3 or lua_lines >= 30 or core_rows >= 1:
        perc = "medium"
    elif R >= 1 or m["assets"] > 0 or m["loc_strings"] > 0:
        perc = "low"
    else:
        perc = "none"
    if native or R >= 400 or T >= 15 or lua_lines >= 3000:
        g = "A changes the most"
    elif R >= 100 or T >= 6 or lua_lines >= 600:
        g = "B large"
    elif R >= 1 and perc == "high":
        g = "C effective (few rows, strong effect)"
    elif R >= 1 or lua_lines >= 1 or m["cfg_keys"] >= 1:
        g = "D small tweak"
    elif m["assets"] > 0 or m["loc_strings"] > 0:
        g = "E non-perceptive to gameplay (content or text only)"
    else:
        g = "E non-perceptive to gameplay (no effective change found)"
    return g, perc, f"R={R} T={T} median_rel={med:.2f} lua_lines={lua_lines} cfg={m['cfg_keys']} assets={m['assets']} loc={m['loc_strings']} native={'yes' if native else 'no'}"


def depth_layers(m):
    L = []
    if m["assets"] or m["loc_strings"] or m["ui_files"]:
        L.append("D0 content/text")
    if m["tables_touched"] or m["table_files"]:
        L.append("D1 data tables (PTF)")
    if m["cfg_keys"]:
        L.append("D2 engine config")
    if m["lua_files"]:
        L.append("D3 Lua scripts")
    if m["native_files"] or m["needs_external"]:
        L.append("D4 native/external")
    return "; ".join(L) or "none found"


def install_layout(entries_paths, has_manifest, pakish):
    tops = collections.Counter(p.replace("\\", "/").split("/")[0].lower() for p in entries_paths if p)
    if has_manifest:
        return "Mods/<mod folder> with mod.manifest (Vortex or manual)"
    if "mods" in tops:
        return "Mods/ folder inside the archive"
    if "data" in tops:
        return "legacy: files go into the game's Data folder"
    if "bin" in tops:
        return "legacy: files go into the game's Bin folder"
    if pakish:
        return "loose .pak (legacy: copy into Data)"
    if "libs" in tops or "localization" in tops or "scripts" in tops:
        return "legacy: archive root is the Data folder"
    return "unclear: read the archive's own instructions"


def analyse_entry(rec, src_root, work, vanilla, krs_keys, args):
    """rec: one row of downloads_inventory.csv. returns the analysis dict (or None)."""
    entry, folder, kind = rec["entry"], rec["folder"], rec["kind"]
    path = os.path.join(src_root, folder, entry)
    res = {"id": int(rec["id"]), "entry": entry, "sub_folder": folder, "kind": kind, "size_mb": 0, "sha256": rec.get("sha256", ""),
           "listing_findings": [], "problems": [], "readable": "yes", "extracted": ""}
    src = Source()
    scratch = None
    entries_paths = []
    if kind.startswith("folder"):
        src.add_tree(path)
        res["extracted"] = "read in place (already extracted by the author)"
        entries_paths = [r[0] for r in src.files]
    elif kind == "loose file":
        src.add_file(path, entry)
        res["extracted"] = "read in place"
        res["size_mb"] = round(os.path.getsize(path) / 1048576, 1)
        entries_paths = [entry]
    else:
        res["size_mb"] = round(os.path.getsize(path) / 1048576, 2)
        entries, info = seven_list(path)
        if not entries:
            res["readable"] = "no"
            res["problems"].append("7-Zip could not list the archive: " + (info.get("Type", "unknown type")))
        res["listing_findings"] = judge_listing(entries)
        entries_paths = [e["path"] for e in entries if not e["folder"]]
        total = sum(e["size"] for e in entries)
        block = any(l == "HIGH" and ("traversal" in t or "absolute" in t or "encrypted" in t or "alternate" in t) for l, t in res["listing_findings"]) \
            or any("bomb" in t for l, t in res["listing_findings"])
        if entries and not block:
            scratch = os.path.join(work, f"{rec['id']}_{abs(hash(entry)) % 100000}")
            rm_tree(scratch)
            os.makedirs(scratch)
            cmd = [SEVENZ, "x", "-y", "-aoa", "-bd", "-bso0", "-bsp0", "-o" + scratch, path]
            if total > MAX_EXTRACT_MB * 1048576:
                sel = [e["path"] for e in entries if not e["folder"] and (os.path.splitext(e["path"].lower())[1] in TEXT_EXT | NATIVE_EXT | SCRIPT_EXT
                                                                          or (e["path"].lower().endswith(".pak") and e["size"] <= MAX_PAK_MB * 1048576))]
                lst = os.path.join(work, f"{rec['id']}_list.txt")
                open(lst, "w", encoding="utf-8").write("\n".join(sel))
                cmd = [SEVENZ, "x", "-y", "-aoa", "-bd", "-bso0", "-bsp0", "-spd", "-o" + scratch, path, "-i@" + lst]
                res["extracted"] = f"partial (archive {total // 1048576} MB: text, scripts and small paks only)"
            else:
                res["extracted"] = "full (scratch, deleted after reading)"
            r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
            if r.returncode not in (0, 1):
                res["problems"].append(f"7-Zip extract exit {r.returncode}: {(r.stderr or r.stdout)[:120]}")
            src.add_tree(scratch)
        elif block:
            res["extracted"] = "NOT extracted (listing failed the safety judgement)"
            res["readable"] = "no"
    scan_text_risks(src)
    # manifest
    man = parse_manifest(src)
    eff = ""
    if man:
        _, modid, mname, mver, vers, eff = man
        res.update(manifest_modid=modid, manifest_name=mname, manifest_version=mver, supports=" ".join(vers) or "(none)",
                   loads_on_1_9_8=ama.engine_loads(vers))
    else:
        res.update(manifest_modid="", manifest_name="", manifest_version="", supports="", loads_on_1_9_8="no manifest (legacy install)")
    area, lua_files, lua_lines, lua_api, cfg, loc_readers, reqs = categorize_paths(src)
    tables, keys, hl, rels, tprob = analyse_tables(src, vanilla, krs_keys, eff)
    res["problems"] += tprob
    loc_new, loc_changed = loc_stats(loc_readers, vanilla)
    R = sum(t["new"] + t["changed"] for t in tables)
    core = [(t, (t["new"] + t["changed"])) for t in tables if is_core(t["base"])]
    core_rows = sum(n for _, n in core)
    # share of core rows with a >=20% relative change: recount from highlights of core tables
    big_core = sum(1 for rc, txt in hl if rc >= 0.2 and is_core(txt.split(":", 1)[0]))
    nat = sum(1 for l, t in src.findings + res["listing_findings"] if l == "HIGH" and ("native" in t or "magic" in t))
    ext_files = area.get("executables/scripts", 0)
    requires_external = any("KCSE" in r or "ASI" in r or "Address" in r or "ReShade" in r for r in reqs)
    m = {"rows_changed_or_new": R, "tables_touched": len([t for t in tables if t["new"] + t["changed"] > 0]), "table_files": len(tables),
         "median_rel_change": statistics.median(rels) if rels else 0.0, "lua_files": lua_files, "lua_lines": lua_lines, "cfg_keys": len(set(cfg)),
         "assets": area.get("textures", 0) + area.get("models/animations/materials", 0) + area.get("audio", 0), "loc_strings": loc_new + loc_changed,
         "ui_files": area.get("ui", 0), "native_files": nat + ext_files, "needs_external": requires_external, "core_rows": core_rows,
         "core_rows_ge20pct": big_core, "readable": res["readable"]}
    if res["readable"] == "yes" and not src.files:
        m["readable"] = "no"
        res["problems"].append("no readable file in the archive")
    res["problems"] += [n for n in src.notes if "not a ZIP" in n]
    if not tables and not lua_files and any("not a ZIP" in n for n in src.notes):
        m["readable"] = "no"
    g, perc, why = grade(m)
    hl.sort(key=lambda x: -(x[0] + (10 if is_core(x[1].split(":", 1)[0]) else 0)))   # core-gameplay tables first
    findings = src.findings + res["listing_findings"]
    level = "HIGH" if any(l == "HIGH" for l, _ in findings) else "MEDIUM" if any(l == "MEDIUM" for l, _ in findings) else "LOW" if findings else "none"
    res.update(m)
    res.update(grade=g, perceptibility=perc, grade_basis=why, depth=depth_layers(m),
               layout=install_layout(entries_paths, bool(man), kind == "loose file" or any(p.lower().endswith(".pak") for p in entries_paths)),
               areas="; ".join(f"{k}: {v}" for k, v in area.most_common()), tables_list=", ".join(sorted({t["base"] for t in tables if t["new"] + t["changed"] > 0}))[:300],
               rows_new=sum(t["new"] for t in tables), rows_changed=sum(t["changed"] for t in tables), rows_same=sum(t["same"] for t in tables),
               rows_dropped=sum(t["dropped"] for t in tables), highlights=" | ".join(x[1] for x in hl[:8]), lua_api=", ".join(f"{k}x{v}" for k, v in lua_api.most_common(6)),
               cfg_sample=", ".join(sorted(set(cfg))[:8]), loc_new=loc_new, loc_changed=loc_changed, requires=", ".join(sorted(reqs)),
               risk=level, risk_findings=" | ".join(dict.fromkeys(f"{l}: {t}" for l, t in sorted(findings, key=lambda x: ("HIGH", "MEDIUM", "LOW").index(x[0]))))[:1200], read_notes=" | ".join(src.notes)[:300],
               native_sha=" ".join(f"{k}={v[:16]}" for k, v in src.native_sha.items())[:300],
               native_info=" || ".join(f"{k}: {v}" for k, v in src.native_info.items())[:900], problems_text=" | ".join(dict.fromkeys(res["problems"]))[:600])
    res["_tables"] = tables
    res["_keys"] = keys
    if scratch:
        rm_tree(scratch)
    return res


def krs_row_keys(vanilla):
    out = {}
    for mod in sorted(os.listdir(paths.MODULES)):
        base = os.path.join(paths.MODULES, mod, "Data", "Libs", "Tables")
        for dp, _, fn in os.walk(base):
            for f in fn:
                if f.endswith(".xml"):
                    p = at.parse_table(open(os.path.join(dp, f), "rb").read())
                    if not p:
                        continue
                    b, _ = at.base_table(p[0], vanilla)
                    if not b:
                        continue
                    kc = at.key_cols(b, vanilla[b]["cols"], p[1])
                    for r in p[2]:
                        out[(b, tuple(at.norm(r.get(c)) for c in kc))] = mod
    return out


def targets(src_root, only):
    inv = list(csv.DictReader(open(os.path.join(D, "downloads_inventory.csv"), encoding="utf-8", newline="")))
    tri = {int(r["id"]): r for r in csv.DictReader(open(os.path.join(D, "mods_triage.csv"), encoding="utf-8", newline=""))}
    out = []
    for r in inv:
        if not r["id"] or r["kind"] == "incomplete download":
            continue
        i = int(r["id"])
        if only and i not in only:
            continue
        if not only and tri.get(i, {}).get("priority") not in ("P1", "P2"):
            continue
        out.append((r, tri.get(i, {})))
    return sorted(out, key=lambda x: (int(x[0]["id"]), x[0]["entry"]))


def write_all(results, tri_by_id, quarantined):
    cols = ["id", "name", "priority", "category", "entry", "sub_folder", "kind", "size_mb", "grade", "perceptibility", "depth", "layout", "loads_on_1_9_8",
            "supports", "manifest_modid", "tables_list", "rows_new", "rows_changed", "rows_same", "rows_dropped", "tables_touched", "median_rel_change",
            "lua_files", "lua_lines", "cfg_keys", "assets", "loc_strings", "requires", "risk", "highlights", "areas", "grade_basis", "problems_text", "extracted"]
    for r in results:
        t = tri_by_id.get(r["id"], {})
        r["name"], r["priority"], r["category"] = t.get("name", ""), t.get("priority", ""), t.get("category", "")
        r["median_rel_change"] = round(r["median_rel_change"], 3)
    with open(os.path.join(D, "mod_analysis.csv"), "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore", lineterminator="\n")
        w.writeheader()
        w.writerows(results)
    with open(os.path.join(D, "mod_tables.csv"), "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["id", "entry", "file_in_mod", "table", "vanilla_table", "style", "rows", "new", "changed", "same", "dropped_vs_vanilla", "changed_columns"])
        for r in results:
            for t in r["_tables"]:
                w.writerow([r["id"], r["entry"], t["vpath"], t["table"], t["base"], t["style"], t["rows"], t["new"], t["changed"], t["same"], t["dropped"], t["cols"]])
    owners = collections.defaultdict(set)
    for r in results:
        for k in r["_keys"]:
            owners[k].add(r["id"])
    with open(os.path.join(D, "mod_overlap.csv"), "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["table", "key", "mods_changing_it", "mod_ids"])
        for (b, k), ids in sorted(owners.items(), key=lambda x: (-len(x[1]), x[0])):
            if len(ids) > 1:
                w.writerow([b, "/".join(k), len(ids), " ".join(map(str, sorted(ids)))])
    with open(os.path.join(D, "risk_scan.csv"), "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["id", "name", "entry", "risk", "findings", "native_sha256", "action"])
        for r in results:
            w.writerow([r["id"], r["name"], r["entry"], r["risk"], r["risk_findings"], (r["native_sha"] + " " + r["native_info"]).strip(), "quarantined" if r["entry"] in quarantined else "kept"])
    return owners


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--src", required=True)
    ap.add_argument("--ids", nargs="*", type=int)
    ap.add_argument("--work", default=os.path.join(os.environ.get("TEMP", "."), "ka"))
    ap.add_argument("--no-quarantine", action="store_true")
    a = ap.parse_args()
    if not os.path.exists(SEVENZ):
        raise SystemExit("7-Zip not found at " + SEVENZ)
    rm_tree(a.work)
    os.makedirs(a.work)
    vanilla = at.load_vanilla(GAME)
    VANILLA_LUA.update(load_vanilla_lua(GAME))
    krs = krs_row_keys(vanilla)
    tri = {int(r["id"]): r for r in csv.DictReader(open(os.path.join(D, "mods_triage.csv"), encoding="utf-8", newline=""))}
    results = []
    tg = targets(a.src, set(a.ids or []))
    print(f"{len(tg)} entries of {len({int(r['id']) for r, _ in tg})} mods to read")
    for n, (rec, t) in enumerate(tg, 1):
        try:
            res = analyse_entry(rec, a.src, a.work, vanilla, krs, a)
        except Exception as e:  # noqa: BLE001
            print(f"  ! {rec['id']} {rec['entry'][:50]}: {type(e).__name__}: {e}")
            continue
        results.append(res)
        print(f"{n:>3}/{len(tg)} {res['id']:>5} {res['grade'][:22]:22} {res['risk']:6} {res['entry'][:52]}")
    # KRS collisions and overlap
    for r in results:
        hit = sorted({f"{krs[k]}:{k[0]}:{'/'.join(k[1])}" for k in r["_keys"] if k in krs})
        r["krs_collisions"] = "; ".join(hit)[:300]
    quarantined = set()
    if not a.no_quarantine:
        qdir = os.path.join(a.src, "_quarantine")
        manifest = os.path.join(qdir, "_quarantine_manifest.csv")
        for r in results:
            if r["risk"] == "HIGH":
                src_p = os.path.join(a.src, r["sub_folder"], r["entry"])
                dst_dir = qdir
                os.makedirs(dst_dir, exist_ok=True)
                dst = os.path.join(dst_dir, r["entry"])
                if r["sub_folder"] == "_quarantine":
                    quarantined.add(r["entry"])   # moved by an earlier run
                elif os.path.exists(src_p) and not os.path.exists(dst):
                    os.rename(src_p, dst)
                    new = not os.path.exists(manifest)
                    with open(manifest, "a", encoding="utf-8", newline="") as f:
                        w = csv.writer(f, lineterminator="\n")
                        if new:
                            w.writerow(["from", "to", "id", "reason"])
                        w.writerow([os.path.join(r["sub_folder"], r["entry"]), os.path.join("_quarantine", r["entry"]), r["id"], r["risk_findings"][:300]])
                    quarantined.add(r["entry"])
    owners = write_all(results, tri, quarantined)
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import audit_mods_report as rep  # noqa: E402
    rep.write_reports(results, tri, owners, quarantined)
    rm_tree(a.work)
    print("scratch folder removed:", not os.path.exists(a.work))
    print(f"{len(results)} entries analysed; quarantined {len(quarantined)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
