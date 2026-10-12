#!/usr/bin/env python3
"""
build_timeprobe.py - install the KRS time probe mod into a KCD install (Mods/krs_timeprobe).

    python tools/harness/build_timeprobe.py --game "<KCD folder>" [--remove]

The probe logs the world clock, the clock ratio and the hunger state to kcd.log (prefix KRS_TP) while the game runs, tries once to set
the world time ratio to 2/3 and puts it back, and quits. Run it with tools/harness/run_time_probe.ps1, which also stamps every log line
with the real time it appeared. Nothing is saved.
"""
import argparse
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build_harness as bh  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", required=True)
    ap.add_argument("--remove", action="store_true")
    ap.add_argument("--mode", choices=["time", "eat", "skip"], default="time", help="time: clock and ratio test; eat: set hunger once and log every change (eat, sleep or wait by hand)")
    ap.add_argument("--hunger", type=float, default=60.0)
    ap.add_argument("--run-s", type=int, default=480)
    ap.add_argument("--apply", type=int, default=1, help="skip mode: 1 takes hunger off after a time skip, 0 only logs")
    ap.add_argument("--set-delay", type=int, default=20, help="skip mode: seconds after a save loads before the hunger is set")
    ap.add_argument("--bed-at", type=int, default=0, help="skip mode: seconds after the hunger is set when the nearest bed is asked to put the player to sleep (0 = never)")
    ap.add_argument("--f-sleep", type=float, default=0.5)
    ap.add_argument("--f-wait", type=float, default=0.75)
    a = ap.parse_args()
    folder = os.path.join(a.game, "Mods", "krs_timeprobe")
    if a.remove:
        shutil.rmtree(folder, ignore_errors=True)
        print("removed", folder)
        return
    files = {
        "Scripts/Startup/krs_timeprobe.lua": f'KRS_TP_MODE = "{a.mode}"\nKRS_TP_HUNGER = {a.hunger}\nKRS_TP_RUN_S = {a.run_s}\nKRS_TP_APPLY = {a.apply}\nKRS_TP_FSLEEP = {a.f_sleep}\nKRS_TP_FWAIT = {a.f_wait}\nKRS_TP_SETDELAY = {a.set_delay}\nKRS_TP_BEDAT = {a.bed_at}\n' + open(os.path.join(HERE, "krs_timeprobe.lua"), encoding="utf-8").read(),
        "Scripts/Entities/KRSTimeProbe.lua": open(os.path.join(HERE, "krs_timeprobe_entity.lua"), encoding="utf-8").read(),
        "Entities/KRSTimeProbe.ent": '<Entity\n        Name="KRSTimeProbe"\n        Script="Scripts/Entities/KRSTimeProbe.lua"\n/>\n',
    }
    bh.write_mod(a.game, "krs_timeprobe", "krs_timeprobe", "KRS Time Probe", files)


if __name__ == "__main__":
    main()
