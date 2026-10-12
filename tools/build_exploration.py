#!/usr/bin/env python3
"""
build_exploration.py - build the two installable parts of krs_exploration.

    python tools/build_exploration.py core                              krs_exploration: the two XP scripts (no animation file, cannot conflict)
    python tools/build_exploration.py wash --assets-from ARCHIVE        krs_exploration_wash: optional file with the trough wash
    python tools/build_exploration.py wash --no-assets                  same without the binary assets (structure check only; the animation cannot play)
                                           [--cut EXTRA.cut.xml ...]    more animation cuts to merge into the database (merge tests)

The wash part is assembled from small cuts kept in modules/krs_exploration/src/wash/ (animation fragments, three text diffs, one Lua file) applied
to the game's OWN files in the replica game at build time, so no game file is stored in the repository and a game update is never undone.
The binary assets (the animation index, the wash animation, the splash materials and textures, 21 files, 71 MB) are third-party and are not in the
repository: they are read from the mod archive named with --assets-from, checked against the sha256 in assets.csv, and packed into the build only.
That archive is listed first (nothing executable, no path traversal, no nested archive) and extracted to a scratch folder that is deleted.
The result is for testing: permission to redistribute those assets is pending (docs/project/PERMISSIONS.md).
"""
import argparse
import csv
import hashlib
import os
import re
import shutil
import subprocess
import sys
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import build_module as bm  # noqa: E402

SEVENZ = os.environ.get("KRS_7Z", r"C:\Program Files\7-Zip\7z.exe")
SRC = os.path.join(ROOT, "modules", "krs_exploration")
WASH = os.path.join(SRC, "src", "wash")
BS = chr(92)


def run(args):
    r = subprocess.run([sys.executable] + args, capture_output=True, text=True)
    print(r.stdout.strip())
    if r.returncode:
        print(r.stderr.strip())
        raise SystemExit(f"step failed: {' '.join(args[:3])}")


def safe_assets(archive, scratch):
    """extract the paks of the archive after judging its listing; return {path in pak: bytes} for the files named in assets.csv"""
    lst = subprocess.run([SEVENZ, "l", "-slt", archive], capture_output=True, text=True).stdout
    paths = [l[7:] for l in lst.splitlines() if l.startswith("Path = ")][1:]
    bad = [p for p in paths if re.search(r"\.(exe|dll|bat|cmd|ps1|vbs|lnk|asi|7z|zip|rar)$", p, re.I) or ".." in p.split(BS) or os.path.isabs(p)]
    if bad:
        raise SystemExit(f"archive refused, suspicious entries: {bad[:3]}")
    shutil.rmtree(scratch, ignore_errors=True)
    os.makedirs(scratch)
    subprocess.run([SEVENZ, "x", "-y", "-aoa", "-bd", "-bso0", "-bsp0", "-o" + scratch, archive, "-i!*.pak", "-r"], check=True)
    wanted = {r["path_in_pak"]: r["sha256"] for r in csv.DictReader(open(os.path.join(WASH, "assets.csv"), encoding="utf-8"))}
    found = {}
    try:
        for dp, _, fn in os.walk(scratch):
            for f in fn:
                if not f.lower().endswith(".pak"):
                    continue
                with zipfile.ZipFile(os.path.join(dp, f)) as z:      # closed before the scratch folder is deleted (Windows locks open files)
                    for zi in z.infolist():
                        name = zi.filename.replace(BS, "/")
                        if name in wanted:
                            try:
                                data = z.read(zi)
                            except zipfile.BadZipFile:
                                zi.orig_filename = zi.filename.replace("/", BS)
                                data = z.open(zi).read()
                            if hashlib.sha256(data).hexdigest() != wanted[name]:
                                raise SystemExit(f"asset {name} differs from the recorded sha256: wrong archive or version")
                            found[name] = data
    finally:
        full = os.path.abspath(scratch)
        shutil.rmtree("\\\\?\\" + full, ignore_errors=True)
        shutil.rmtree(full, ignore_errors=True)
        if os.path.exists(full):   # names with trailing dots or spaces: only the shell's rmdir removes them (it deletes folders, it runs nothing in them)
            subprocess.run(["cmd", "/c", "rmdir", "/s", "/q", "\\\\?\\" + full], capture_output=True)
        if os.path.exists(full):
            print("WARNING: scratch folder not removed:", full)
    missing = sorted(set(wanted) - set(found))
    if missing:
        raise SystemExit(f"assets missing from the archive: {missing[:3]}")
    return found


def wash(a, out_root):
    work = os.path.join(out_root, "_work")
    os.makedirs(work, exist_ok=True)
    cuts = [os.path.join(WASH, "adb_wash.cut.xml")] + (a.cut or [])
    run([os.path.join(HERE, "adb_cut.py"), "apply", "--cut"] + cuts + ["--out", os.path.join(work, "kcd_male_database.adb")])
    run([os.path.join(HERE, "text_cut.py"), "apply", "--vanilla", "Scripts.pak!Libs/AI/final/so_water_tube.xml", "--diff", os.path.join(WASH, "so_water_tube.diff"),
         "--out", os.path.join(work, "so_water_tube.xml")])
    run([os.path.join(HERE, "text_cut.py"), "apply", "--vanilla", "GameData.pak!Libs/Particles/workbehaviors.xml", "--diff", os.path.join(WASH, "workbehaviors.diff"),
         "--out", os.path.join(work, "workbehaviors.xml")])
    run([os.path.join(HERE, "text_cut.py"), "apply", "--vanilla", "patch/ipl_patch_010900.pak!Animations/humans/male/male.animevents", "--diff", os.path.join(WASH, "male_animevents.diff"),
         "--out", os.path.join(work, "male.animevents")])
    files = {
        "Animations/Mannequin/ADB/kcd_male_database.adb": open(os.path.join(work, "kcd_male_database.adb"), "rb").read(),
        "Libs/AI/final/so_water_tube.xml": open(os.path.join(work, "so_water_tube.xml"), "rb").read(),
        "Libs/Particles/workbehaviors.xml": open(os.path.join(work, "workbehaviors.xml"), "rb").read(),
        "Animations/humans/male/male.animevents": open(os.path.join(work, "male.animevents"), "rb").read(),
        "Scripts/Startup/troughwash.lua": open(os.path.join(WASH, "troughwash.lua"), "rb").read(),
    }
    note = "structure only, no binary assets: the animation cannot play"
    if a.assets_from:
        assets = safe_assets(a.assets_from, os.path.join(out_root, "_scratch"))
        files.update(assets)
        note = f"{len(assets)} binary assets from {os.path.basename(a.assets_from)}"
    elif not a.no_assets:
        raise SystemExit("give --assets-from ARCHIVE (the Trough Washing Animation archive) or --no-assets")
    dist = os.path.join(out_root, "krs_exploration_wash")
    shutil.rmtree(dist, ignore_errors=True)
    os.makedirs(dist)
    shutil.copy(os.path.join(WASH, "mod.manifest"), dist)
    bm.make_pak(os.path.join(dist, "Data", "krs_exploration_wash.pak"), files)
    shutil.rmtree(work, ignore_errors=True)
    print(f"krs_exploration_wash: {len(files)} files in the pak ({note}) -> {dist}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("part", choices=["core", "wash"])
    ap.add_argument("--assets-from")
    ap.add_argument("--no-assets", action="store_true")
    ap.add_argument("--cut", nargs="*")
    ap.add_argument("--out", default=os.path.join(ROOT, "dist"))
    a = ap.parse_args()
    if a.part == "core":
        return 0 if bm.build("krs_exploration", a.out) else 1
    wash(a, a.out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
