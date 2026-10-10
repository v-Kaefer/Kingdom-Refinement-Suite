#!/usr/bin/env python3
"""
build_skipcost.py - install the KRS Skip Cost prototype into a KCD install (Mods/krs_skipcost).

    python tools/harness/skipcost/build_skipcost.py --game "<KCD folder>" [--wait 0.75] [--sit 0.5] [--sleep 0.5] [--apply 1] [--remove]

The engine charges no hunger while the clock is skipped (Wait, sleep). This mod takes hunger off after each skip: hours skipped x the
awake hunger rate x a factor chosen by the posture of the player during the skip (--wait standing, --sit sitting, --sleep lying). Vigour and health are untouched.
It logs one line per skip to kcd.log with the prefix KRS_SC. The scripts are krs_skipcost.lua (starter) and krs_skipcost_entity.lua.
"""
import argparse
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import build_harness as bh  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", required=True)
    ap.add_argument("--wait", type=float, default=0.75, help="share of the awake hunger cost charged for a skip made standing (Wait)")
    ap.add_argument("--sit", type=float, default=0.5, help="share charged for a skip made sitting (reading on a bench, Wait on a chair)")
    ap.add_argument("--sleep", type=float, default=0.5, help="share charged for a skip made lying down (sleep, faint) or with vigour rising")
    ap.add_argument("--apply", type=int, default=1, help="0 only logs what would be charged")
    ap.add_argument("--remove", action="store_true")
    a = ap.parse_args()
    folder = os.path.join(a.game, "Mods", "krs_skipcost")
    if a.remove:
        shutil.rmtree(folder, ignore_errors=True)
        print("removed", folder)
        return
    cfg = f"KRS_SC_CFG = {{ wait = {a.wait}, sit = {a.sit}, sleep = {a.sleep}, apply = {a.apply} }}\n"
    files = {
        "Scripts/Startup/krs_skipcost.lua": cfg + open(os.path.join(HERE, "krs_skipcost.lua"), encoding="utf-8").read(),
        "Scripts/Entities/KRSSkipCost.lua": open(os.path.join(HERE, "krs_skipcost_entity.lua"), encoding="utf-8").read(),
        "Entities/KRSSkipCost.ent": '<Entity\n        Name="KRSSkipCost"\n        Script="Scripts/Entities/KRSSkipCost.lua"\n/>\n',
    }
    bh.write_mod(a.game, "krs_skipcost", "krs_skipcost", "KRS Skip Cost", files)


if __name__ == "__main__":
    main()
