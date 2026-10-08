#!/usr/bin/env python3
"""
build_adbtest.py - install the test mod `krs_adbtest` into a KCD install (the replica, never the Steam copy).

    python tools/harness/build_adbtest.py --game "<KCD folder>" [--adb merged.adb] [--remove]

Without --adb the mod carries only the test script (baseline run). With --adb it also carries that file as
Animations/Mannequin/ADB/kcd_male_database.adb, which overrides the game's own. Run it with
    powershell -File tools/harness/run_game_test.ps1 -GameDir "<KCD folder>" -Mods krs_adbtest -Harness krs_adbtest -OutFile out.log
and read <game>/kcd.log afterwards (copy it before the next run: the next start moves it to logbackups/). --remove uninstalls.
"""
import argparse
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import build_module as bm  # noqa: E402

MANIFEST = """<?xml version="1.0" encoding="utf-8"?>
<kcd_mod>
  <info>
    <name>krs_adbtest</name>
    <description>Test mod of the Kingdom Refinement Suite: reloads the animation databases at the main menu and quits.</description>
    <author>KRS</author>
    <version>0.0.1</version>
    <created_on>06/10/2026</created_on>
    <modid>krs_adbtest</modid>
    <modifies_level>false</modifies_level>
  </info>
</kcd_mod>
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", required=True)
    ap.add_argument("--adb")
    ap.add_argument("--remove", action="store_true")
    a = ap.parse_args()
    dest = os.path.join(a.game, "Mods", "krs_adbtest")
    if a.remove:
        shutil.rmtree(dest, ignore_errors=True)
        print("removed", dest)
        return 0
    shutil.rmtree(dest, ignore_errors=True)
    os.makedirs(os.path.join(dest, "Data"))
    open(os.path.join(dest, "mod.manifest"), "w", encoding="utf-8").write(MANIFEST)
    files = {"Scripts/Startup/krs_adbtest.lua": open(os.path.join(HERE, "krs_adbtest.lua"), "rb").read()}
    if a.adb:
        files["Animations/Mannequin/ADB/kcd_male_database.adb"] = open(a.adb, "rb").read()
    bm.make_pak(os.path.join(dest, "Data", "krs_adbtest.pak"), files)
    print(f"installed {dest} with {len(files)} file(s)" + (f" (ADB {os.path.getsize(a.adb)} bytes)" if a.adb else " (baseline: no ADB)"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
