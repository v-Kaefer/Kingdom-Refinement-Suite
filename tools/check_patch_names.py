#!/usr/bin/env python3
"""
check_patch_names.py - pre-flight check for KCD table-patch (PTF) mods, based on what the game was observed to do
(docs/engine/ptf-rules.md):

  1. the suffix of every patch file (`table__SUFFIX.xml`) must equal the mod id, otherwise the engine silently ignores it
  2. a mod id may only contain lowercase letters and underscores (no digits, no hyphens)
  3. a row that does not list every column of the table header blanks the missing columns (it does not merge)
  4. a patch file named exactly like a vanilla table (no `__suffix`) replaces the whole table
  5. a .pak must be a ZIP archive; a 7z archive renamed to .pak fails with 'Failed to open the pak'

The mod id is the <modid> element of mod.manifest, or the lower-cased <name> with spaces turned into underscores.

    python tools/check_patch_names.py <folder> [<folder> ...]

Every folder that contains a mod.manifest (searched recursively) is checked; patch files are looked for loose
(Data/**) and inside Data/*.pak. Exit code 1 when something would not work in game.
"""
import os
import re
import sys
import xml.etree.ElementTree as ET
import zipfile


def mod_id(manifest):
    root = ET.parse(manifest).getroot()
    info = root.find("info")
    modid = (info.findtext("modid") or "").strip() if info is not None else ""
    name = (info.findtext("name") or "").strip() if info is not None else ""
    return modid, name, (modid or re.sub(r"\s+", "_", name.lower()))


def patch_files(mod_dir):
    """yield (label, filename, bytes) for every xml table file in the mod's Data folder and paks."""
    data = os.path.join(mod_dir, "Data")
    for dp, dn, fn in os.walk(data):
        for f in fn:
            p = os.path.join(dp, f)
            if f.lower().endswith(".xml") and re.search(r"[/\\]Tables[/\\]", p):
                yield os.path.relpath(p, mod_dir), f, open(p, "rb").read()
            elif f.lower().endswith(".pak"):
                try:
                    z = zipfile.ZipFile(p)
                except zipfile.BadZipFile:
                    yield os.path.relpath(p, mod_dir), None, None   # not readable
                    continue
                for zi in z.infolist():
                    if zi.filename.lower().endswith(".xml") and "tables/" in zi.filename.lower():
                        try:
                            raw = z.open(zi).read()
                        except zipfile.BadZipFile:
                            zi.orig_filename = zi.filename.replace("/", "\\")
                            raw = z.open(zi).read()
                        yield f"{os.path.relpath(p, mod_dir)}!{zi.filename}", os.path.basename(zi.filename), raw


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    problems = 0
    for top in sys.argv[1:]:
        for dp, dn, fn in os.walk(top):
            if "mod.manifest" not in fn or ".claude" in dp or "KingdomComeDeliverance" in dp:
                continue
            try:
                modid, name, effective = mod_id(os.path.join(dp, "mod.manifest"))
            except ET.ParseError as e:
                print(f"[{dp}] manifest unreadable: {e}")
                problems += 1
                continue
            print(f"\n== {dp}   name='{name}' modid='{modid}' -> effective id '{effective}'")
            if not re.fullmatch(r"[a-z_]+", effective):
                print(f"   PROBLEM id '{effective}' has characters other than lowercase letters and underscore")
                problems += 1
            seen = 0
            for label, fname, raw in patch_files(dp):
                if fname is None:
                    print(f"   PROBLEM {label}: not a zip file (a 7z archive renamed .pak is not opened by the game: "
                          "'Failed to open the pak'). Create it with 7-Zip as format 'zip'")
                    problems += 1
                    continue
                seen += 1
                base = fname[:-4]
                if "__" not in base:
                    print(f"   PROBLEM {label}: no '__suffix' - this REPLACES the whole vanilla table")
                    problems += 1
                    continue
                suffix = base.split("__", 1)[1]
                if suffix.lower() != effective:
                    print(f"   PROBLEM {label}: suffix '{suffix}' != mod id '{effective}' - the game will ignore this file")
                    problems += 1
                try:
                    t = ET.fromstring(re.sub(r"^\s*<\?xml[^>]*\?>", "", raw.decode("utf-8", "replace"))).find("table")
                    cols = {c.get("name") for c in t.findall("./header/column")}
                    short = [r for r in t.findall("./rows/row") if not cols <= set(r.attrib)]
                    if short:
                        print(f"   PROBLEM {label}: {len(short)} row(s) do not list every column ({', '.join(sorted(cols - set(short[0].attrib)))}...): "
                              "missing columns are blanked, not merged")
                        problems += 1
                except Exception as e:  # noqa: BLE001
                    print(f"   NOTE   {label}: could not parse ({e})")
            if not seen:
                print("   no table patches found")
    print("\nproblems:", problems)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
