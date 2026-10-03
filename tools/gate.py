#!/usr/bin/env python3
"""
gate.py - build KRS modules, run them in the test game and assert that every patched value is what the game reports.

    python tools/gate.py krs_items [krs_perks krs_qol]  [--mode tables|full] [--with MOD ...] [--log docs/tests/logs/gate_<name>.log]
                          [--game "<KCD folder>"] [--timeout 300] [--extra-lua FILE]

tables  (default) starts the game, waits for the main menu, checks every table that is loaded there and quits by itself.
full              also waits for the player: someone has to press Continue in the test instance (rows of the perk and
                  buff tables only exist once a level is loaded). The check list is the same; unchecked rows fail.

What is asserted (rules measured in docs/engine/ptf-rules.md):
  1. the engine logged "Table 'T' is patched by 'T__<id>'" for every patch file of every module
  2. every column of every patch row reads back from the game's database as in the patch file
  3. every rpg_param row reads back through RPG.<key>
  4. no 'Failed to open the pak', no Lua error from a KRS script, and no missing localization file for the module id
The script installs the modules into <game>/Mods, loads only them (plus --with mods), restores Mods/mod_order.txt and
removes what it installed. Exit code 0 = gate passed.
"""
import argparse
import datetime
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import paths  # noqa: E402

ROOT = os.path.dirname(HERE)
DEFAULT_GAME = os.environ.get("KCD_GAME", r"E:\Kingdom-Refinement-Suite\Mods WIP folder\KingdomComeDeliverance")


def run(cmd, **kw):
    print("$", " ".join(str(c) for c in cmd))
    return subprocess.run(cmd, **kw)


def patch_files(mod):
    base = os.path.join(ROOT, "modules", mod, "Data", "Libs", "Tables")
    for dp, _, fn in os.walk(base):
        for f in fn:
            if f.endswith(".xml"):
                yield f[:-4]                      # table__modid


def has_localization(mod):
    return os.path.isdir(os.path.join(ROOT, "modules", mod, "Localization"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("modules", nargs="+")
    ap.add_argument("--mode", choices=["tables", "full"], default="tables")
    ap.add_argument("--with", dest="with_mods", nargs="*", default=[], help="other mods (folder names in Mods) to load before the modules")
    ap.add_argument("--game", default=DEFAULT_GAME)
    ap.add_argument("--timeout", type=int, default=300)
    ap.add_argument("--log")
    ap.add_argument("--extra-lua")
    ap.add_argument("--keep", action="store_true", help="leave the installed mods in Mods afterwards")
    a = ap.parse_args()
    log = a.log or os.path.join(paths.TEST_LOGS, f"gate_{'_'.join(a.modules)}_{a.mode}_{datetime.datetime.now():%Y%m%d-%H%M}.log")   # never overwrite an older log

    if run([sys.executable, os.path.join(HERE, "build_module.py"), *a.modules]).returncode:
        print("GATE FAILED: build")
        return 1
    bg = [sys.executable, os.path.join(HERE, "harness", "build_gate.py"), "--game", a.game, "--mode", a.mode]
    if a.extra_lua:
        bg += ["--extra-lua", a.extra_lua]
    if run(bg + a.modules).returncode:
        print("GATE FAILED: install")
        return 1
    try:
        order = [*a.with_mods, *a.modules, "krs_gate"]
        ps = ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", os.path.join(HERE, "harness", "run_game_test.ps1"),
              "-GameDir", a.game, "-OutFile", log, "-Harness", "krs_gate", "-TimeoutSec", str(a.timeout), "-Mods", ",".join(order)]
        run(ps)
    finally:
        if not a.keep:
            run([sys.executable, os.path.join(HERE, "harness", "build_gate.py"), "--game", a.game, "--remove", *a.modules])

    text = open(log, encoding="utf-8", errors="replace").read() if os.path.exists(log) else ""
    problems, notes = [], []
    if "KRS_HARNESS end" not in text:
        problems.append("the harness did not finish (no 'KRS_HARNESS end' line)")

    patched = {}
    for m in re.finditer(r"Table '([^']+)' is patched by '([^']+)'(?:, lines added: (\d+), modified: (\d+), equal: (\d+))?", text):
        patched[m.group(2).lower()] = m.group(0)
    for mod in a.modules:
        for pf in patch_files(mod):
            if pf.lower() in patched:
                notes.append(patched[pf.lower()])
            elif a.mode == "full" or not re.match(r"(perk|buff)", pf):
                problems.append(f"patch {pf} was not applied (no 'is patched by' line)")
            else:
                notes.append(f"patch {pf}: table is loaded with a level, not checked in tables mode")
        if has_localization(mod) and re.search(r"Can't open file \(Localization\\text__%s\.xml\)" % mod, text):
            problems.append(f"{mod}: localization file text__{mod}.xml was not found for the game language")
    for line in text.splitlines():
        if "Failed to open the pak" in line and re.search("krs", line, re.I):
            problems.append(line.strip())
        if re.search(r"Lua Error|[Ss]cript error", line) and re.search("krs", line, re.I):
            problems.append(line.strip())
        if "KRS_GATE" in line and ("FAIL" in line):
            problems.append(line.split("KRS_GATE ", 1)[-1].strip())
    stages = re.findall(r"KRS_GATE STAGE (\w+) pass=(\d+) fail=(\d+) pending=(\d+)", text)
    if not stages:
        problems.append("no gate result in the log")
    else:
        stage, ok, bad, pending = stages[-1]
        notes.append(f"last stage '{stage}': {ok} checks passed, {bad} failed, {pending} pending")
        if int(pending) and a.mode == "full":
            problems.append(f"{pending} row check(s) were never reached (their tables did not load)")
        elif int(pending):
            notes.append(f"{pending} check(s) pending: tables that only exist inside a level (run with --mode full)")

    print("\n".join(f"  {n}" for n in notes))
    if problems:
        print("\nGATE FAILED")
        print("\n".join(f"  - {p}" for p in problems))
        return 1
    print("\nGATE PASSED:", ", ".join(a.modules), f"({a.mode})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
