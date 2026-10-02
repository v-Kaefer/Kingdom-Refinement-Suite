#!/usr/bin/env python3
"""
lua_api_check.py - check whether the functions and RPG parameters a Lua mod uses actually exist in KCD 1.9.6.

For every call `Obj.Func(...)` / `Obj:Method(...)` and every `RPG.<Key>` access in the given Lua files it looks for
evidence in three places and reports the strongest one:

    GAME   the same Obj.Func / Obj:Method appears in the game's own scripts (Scripts*.pak)         -> exists
    DUMP   it is listed in the live Lua table dump shipped with the Cheat mod (table_dump.txt)     -> exists
    SEEN   the name appears in game scripts, but on another object                                -> unverified
    NONE   no trace anywhere                                                                        -> very likely does not exist
    CONST  (RPG.<Key>) the key is a known rpg constant (Params Reference, vanilla rpg_param, dumps) -> valid parameter name
    NOCONST (RPG.<Key>) unknown key                                                                 -> RPG.<Key> would raise 'no such rpg constant'

    python tools/lua_api_check.py --game "<KCD folder>" --params-ref "Params Reference.md" \
        --out docs/bow/API_CHECK.md  mod1.lua mod2.lua ...

Limits: a textual check. A method found on another object (SEEN) may still not exist on yours, and a method that is
only provided by a mod (for example the Cheat mod's `cheat:` functions) is reported by the dump if the dump was made
with that mod loaded.
"""
import argparse
import collections
import glob
import os
import re
import zipfile
import xml.etree.ElementTree as ET

LUA_STD = {"math", "string", "table", "os", "io", "pairs", "ipairs", "type", "tostring", "tonumber", "print", "pcall",
           "select", "setmetatable", "getmetatable", "unpack", "assert", "error", "next", "rawget", "rawset"}
CALL = re.compile(r"\b([A-Za-z_][A-Za-z0-9_]*(?:\.[A-Za-z_][A-Za-z0-9_]*)*)\s*([.:])\s*([A-Za-z_][A-Za-z0-9_]*)\s*\(")
RPGKEY = re.compile(r"\bRPG\.([A-Za-z_][A-Za-z0-9_]*)\b(?!\s*\()")
DEFS = re.compile(r"\bfunction\s+(?:[A-Za-z_][A-Za-z0-9_.]*[.:])?([A-Za-z_][A-Za-z0-9_]*)\s*\(")


def read_member(z, zi):
    try:
        return z.open(zi).read()
    except zipfile.BadZipFile:
        zi.orig_filename = zi.filename.replace("/", "\\")
        return z.open(zi).read()


def strip_comments(src):
    src = re.sub(r"--\[\[.*?\]\]", "", src, flags=re.S)
    return re.sub(r"--[^\n]*", "", src)


def load_game_corpus(game):
    texts = []
    for p in glob.glob(os.path.join(game, "Data", "Scripts*.pak")):
        z = zipfile.ZipFile(p)
        for zi in z.infolist():
            if zi.filename.lower().endswith((".lua", ".xml")):
                try:
                    texts.append(read_member(z, zi).decode("utf-8", "replace"))
                except Exception:
                    pass
    return "\n".join(texts)


def load_dump(game):
    members = collections.defaultdict(set)
    path = os.path.join(game, "Mods", "Cheat", "Data", "Docs", "table_dump.txt")
    if not os.path.exists(path):
        return members
    cur = None
    for line in open(path, encoding="utf-8", errors="replace"):
        line = line.rstrip("\n").strip()
        m = re.match(r"\[TABLE\] TABLE:\s*(\S+)", line)
        if m:
            cur = m.group(1)
        elif line and cur:
            members[cur].add(line)
    return members


def load_constants(game, params_ref):
    keys = set()
    if params_ref and os.path.exists(params_ref):
        for line in open(params_ref, encoding="utf-8", errors="replace"):
            m = re.match(r"^([A-Z][A-Za-z0-9_]+)\b", line)
            if m:
                keys.add(m.group(1))
    z = zipfile.ZipFile(os.path.join(game, "Data", "Tables.pak"))
    for zi in z.infolist():
        if zi.filename.lower() == "libs/tables/rpg/rpg_param.xml":
            root = ET.fromstring(re.sub(r"^\s*<\?xml[^>]*\?>", "", read_member(z, zi).decode("utf-8", "replace")))
            keys |= {r.get("rpg_param_key") for r in root.iter("row")}
    return keys


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", required=True)
    ap.add_argument("--params-ref", default="Params Reference.md")
    ap.add_argument("--out", default="docs/bow/API_CHECK.md")
    ap.add_argument("files", nargs="+")
    a = ap.parse_args()

    corpus = load_game_corpus(a.game)
    dump = load_dump(a.game)
    consts = load_constants(a.game, a.params_ref)
    rows = []
    for f in a.files:
        src = strip_comments(open(f, encoding="utf-8", errors="replace").read())
        own = set(DEFS.findall(src))
        seen = set()
        for obj, sep, meth in CALL.findall(src):
            last = obj.split(".")[-1]
            if last in LUA_STD or meth in own or (last, sep, meth) in seen:
                continue
            seen.add((last, sep, meth))
            exact = len(re.findall(re.escape(last) + r"\s*[.:]\s*" + re.escape(meth) + r"\b", corpus))
            anyobj = len(re.findall(r"[.:]\s*" + re.escape(meth) + r"\s*\(", corpus))
            indump = meth in dump.get(last, set()) or any(meth in v for k, v in dump.items() if k.lower() == last.lower())
            status = "GAME" if exact else "DUMP" if indump else "SEEN" if anyobj else "NONE"
            rows.append((os.path.basename(f), f"{obj}{sep}{meth}()", status, exact, anyobj))
        for key in sorted(set(RPGKEY.findall(src))):
            rows.append((os.path.basename(f), f"RPG.{key}", "CONST" if key in consts else "NOCONST", "", ""))

    order = {"NONE": 0, "NOCONST": 0, "SEEN": 1, "DUMP": 2, "GAME": 3, "CONST": 3}
    rows.sort(key=lambda r: (order[r[2]], r[0], r[1]))
    out = ["# Lua API check", "",
           "Generated by `tools/lua_api_check.py`. `NONE`/`NOCONST` = no trace in the game scripts, the Cheat-mod dump or the "
           "parameter lists (very likely does not exist); `SEEN` = the name exists only on another object; "
           "`DUMP`/`GAME`/`CONST` = exists.", "",
           "| File | Call | Status | exact uses in game scripts | uses of the name on any object |", "|---|---|---|---:|---:|"]
    for r in rows:
        out.append("| %s | `%s` | **%s** | %s | %s |" % r)
    os.makedirs(os.path.dirname(a.out) or ".", exist_ok=True)
    open(a.out, "w", encoding="utf-8").write("\n".join(out) + "\n")
    c = collections.Counter(r[2] for r in rows)
    print(dict(c))


if __name__ == "__main__":
    main()
