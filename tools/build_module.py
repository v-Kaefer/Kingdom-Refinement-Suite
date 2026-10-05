#!/usr/bin/env python3
"""
build_module.py - build an installable KRS module from its source tree.

    python tools/build_module.py krs_items [krs_perks ...]      (or --all)   [--out dist]

Source tree (modules/<id>/):
    mod.manifest                       <modid> must equal the folder name (lowercase letters and underscore only)
    Data/**                            becomes Data/<id>.pak (a ZIP; the game cannot open 7z renamed to .pak)
    Localization/<Language>/*.xml      becomes Localization/<Language>_xml.pak (one ZIP per language)
    README.md, CHANGES.md              copied into the archive for the Nexus page

Output:
    dist/<id>/                         what goes into <game>/Mods/<id>/ (also what Vortex installs)
    dist/<id>-<version>.zip            Vortex-ready archive (the folder <id>/ at its root)

The patch rules the build enforces come from the in-game tests in docs/engine/ptf-rules.md:
    suffix of every `table__suffix.xml` == mod id, rows complete, no whole-table replacement, ZIP paks.
The build fails (exit 1) when tools/check_patch_names.py reports a problem, before and after packing.
"""
import argparse
import os
import re
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET
import zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HERE = os.path.dirname(os.path.abspath(__file__))
DATE = (2026, 10, 2, 0, 0, 0)          # fixed time stamp: the same sources always give the same bytes


def entry(name, is_dir):
    """zip entry with the attributes of 7-Zip made paks (these are the ones the engine was tested with)."""
    zi = zipfile.ZipInfo(name, date_time=DATE)
    zi.create_system = 0
    zi.external_attr = 16 if is_dir else 32
    zi.compress_type = zipfile.ZIP_STORED if is_dir else zipfile.ZIP_DEFLATED
    return zi


def make_pak(out_path, files):
    """files: {zip path: bytes}. Directory entries are added like 7-Zip does."""
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    dirs = set()
    for n in files:
        parts = n.split("/")[:-1]
        for k in range(1, len(parts) + 1):
            dirs.add("/".join(parts[:k]) + "/")
    with zipfile.ZipFile(out_path, "w") as z:
        for d in sorted(dirs):
            z.writestr(entry(d, True), b"")
        for n in sorted(files):
            z.writestr(entry(n, False), files[n])


def collect(folder):
    out = {}
    for dp, _, fn in os.walk(folder):
        for f in fn:
            p = os.path.join(dp, f)
            out[os.path.relpath(p, folder).replace("\\", "/")] = open(p, "rb").read()
    return out


def manifest(src):
    info = ET.parse(os.path.join(src, "mod.manifest")).getroot().find("info")
    return (info.findtext("modid") or "").strip(), (info.findtext("version") or "0").strip()


def check(path):
    r = subprocess.run([sys.executable, os.path.join(HERE, "check_patch_names.py"), path], capture_output=True, text=True)
    if r.returncode:
        print(r.stdout)
    return r.returncode == 0


def build(mod_id, out_root):
    src = os.path.join(ROOT, "modules", mod_id)
    if not os.path.isdir(src):
        print(f"{mod_id}: no source folder {src}")
        return False
    modid, version = manifest(src)
    if modid != mod_id or not re.fullmatch(r"[a-z_]+", modid):
        print(f"{mod_id}: manifest modid '{modid}' must equal the folder name and use only lowercase letters and underscore")
        return False
    if not check(src):
        print(f"{mod_id}: source check failed")
        return False

    dist = os.path.join(out_root, mod_id)
    if os.path.isdir(dist):
        shutil.rmtree(dist)
    os.makedirs(dist)
    shutil.copy(os.path.join(src, "mod.manifest"), dist)
    for doc in ("README.md", "CHANGES.md"):
        if os.path.exists(os.path.join(src, doc)):
            shutil.copy(os.path.join(src, doc), dist)

    data = collect(os.path.join(src, "Data")) if os.path.isdir(os.path.join(src, "Data")) else {}
    if data:
        make_pak(os.path.join(dist, "Data", f"{mod_id}.pak"), data)
    loc = os.path.join(src, "Localization")
    languages = sorted(d for d in os.listdir(loc)) if os.path.isdir(loc) else []
    for lang in languages:
        make_pak(os.path.join(dist, "Localization", f"{lang}_xml.pak"), collect(os.path.join(loc, lang)))

    if not check(dist):
        print(f"{mod_id}: packed result failed the check")
        return False

    archive = os.path.join(out_root, f"{mod_id}-{version}.zip")
    with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as z:
        for dp, _, fn in os.walk(dist):
            for f in sorted(fn):
                p = os.path.join(dp, f)
                z.write(p, os.path.join(mod_id, os.path.relpath(p, dist)).replace("\\", "/"))
    print(f"{mod_id} {version}: {len(data)} data file(s), {len(languages)} language(s) -> {dist} and {archive}")
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("modules", nargs="*")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--out", default=os.path.join(ROOT, "dist"))
    a = ap.parse_args()
    mods = a.modules
    if a.all:
        mods = sorted(d for d in os.listdir(os.path.join(ROOT, "modules")) if os.path.isfile(os.path.join(ROOT, "modules", d, "mod.manifest")))
    if not mods:
        print(__doc__)
        return 2
    ok = all([build(m, a.out) for m in mods])
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
