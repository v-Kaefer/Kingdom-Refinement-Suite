#!/usr/bin/env python3
"""
build_manifest_probe.py - install mods that differ only in their <supports> block, to see what the engine does with it.

    python tools/harness/build_manifest_probe.py --game "<KCD folder>" [--riposte "<Mods/Riposte... folder>"]
    python tools/harness/build_manifest_probe.py --game "<KCD folder>" --remove

Each probe mod patches one different, harmless `food` row (complete row, suffix == mod id), so the engine's line
"Table 'food' is patched by 'food__<id>'" proves the mod really ran:

    krs_probe_blocked   supports 1.9.6 only          (expected on 1.9.8: disabled)
    krs_probe_edited    the same, manifest says 1.9.8 (the author's claim: now it loads)
    krs_probe_range     lists 1.9.6, 1.9.7, 1.9.8
    krs_probe_wild      supports 1.9.x                (wildcard)
    krs_probe_none      no <supports> block at all    (expected: enabled)

With --riposte a real third-party mod is copied twice into Mods: `krs_probe_riposte_as_is` (manifest untouched) and
`krs_probe_riposte_edited` (only the <kcd_version> line changed to 1.9.8). Riposte has no modid, so its id is derived from
its name ("riposte") and its patch is `perk__riposte` in both copies; load only one of them per run.
"""
import argparse
import os
import re
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(ROOT, "tools"))
sys.path.insert(0, HERE)
import vanilla  # noqa: E402
from build_harness import write_mod  # noqa: E402

MANIFEST = """<?xml version="1.0" encoding="utf-8"?>
<kcd_mod>
  <info>
    <name>{name}</name>
    <description>Manifest probe for the Kingdom Refinement Suite tests.</description>
    <author>KRS</author>
    <version>0.0.1</version>
    <created_on>03/10/2026</created_on>
    <modid>{modid}</modid>
    <modifies_level>false</modifies_level>
  </info>
{supports}</kcd_mod>
"""

PROBES = {
    "krs_probe_blocked": "  <supports>\n    <kcd_version>1.9.6</kcd_version>\n  </supports>\n",
    "krs_probe_edited": "  <supports>\n    <kcd_version>1.9.8</kcd_version>\n  </supports>\n",
    "krs_probe_range": "  <supports>\n    <kcd_version>1.9.6</kcd_version>\n    <kcd_version>1.9.7</kcd_version>\n    <kcd_version>1.9.8</kcd_version>\n  </supports>\n",
    "krs_probe_wild": "  <supports>\n    <kcd_version>1.9.x</kcd_version>\n  </supports>\n",
    "krs_probe_none": "",
}
COPIES = ("krs_probe_riposte_as_is", "krs_probe_riposte_edited")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", required=True)
    ap.add_argument("--riposte")
    ap.add_argument("--remove", action="store_true")
    a = ap.parse_args()
    mods = os.path.join(a.game, "Mods")
    if a.remove:
        for m in list(PROBES) + list(COPIES):
            shutil.rmtree(os.path.join(mods, m), ignore_errors=True)
        print("removed probe mods")
        return 0

    cols, rows = vanilla.load("item/food", a.game)
    pool = [r for r in rows if r.get("food_type_id") == "3"][:len(PROBES)]
    for (mod_id, supports), row in zip(PROBES.items(), pool):
        changed = dict(row)
        changed["refresh_benefit"] = str(int(float(row.get("refresh_benefit") or 0)) + 1)
        xml = vanilla.patch_xml("food", cols, [changed])
        write_mod(a.game, mod_id, mod_id, mod_id, {f"Libs/Tables/item/food__{mod_id}.xml": xml})
        mf = os.path.join(mods, mod_id, "mod.manifest")
        open(mf, "w", encoding="utf-8", newline="\n").write(MANIFEST.format(name=mod_id, modid=mod_id, supports=supports))

    if a.riposte:
        for copy in COPIES:
            dest = os.path.join(mods, copy)
            shutil.rmtree(dest, ignore_errors=True)
            shutil.copytree(a.riposte, dest)
            for junk in ("__folder_managed_by_vortex",):
                for dp, _, fn in os.walk(dest):
                    if junk in fn:
                        os.remove(os.path.join(dp, junk))
        mf = os.path.join(mods, "krs_probe_riposte_edited", "mod.manifest")
        text = open(mf, encoding="utf-8").read()
        new = re.sub(r"<kcd_version>[^<]*</kcd_version>", "<kcd_version>1.9.8</kcd_version>", text)
        assert new != text, "the Riposte manifest has no <kcd_version> line to edit"
        open(mf, "w", encoding="utf-8", newline="\n").write(new)
    print("installed", ", ".join(list(PROBES) + (list(COPIES) if a.riposte else [])))
    return 0


if __name__ == "__main__":
    sys.exit(main())
