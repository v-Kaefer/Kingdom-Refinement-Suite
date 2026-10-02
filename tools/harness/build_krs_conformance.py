#!/usr/bin/env python3
"""
build_krs_conformance.py - package the table patches of a KRS module exactly as they are in the repo and install them
as a test mod, to see whether the game really applies them.

    python tools/harness/build_krs_conformance.py --game "<KCD folder>" --src "KRS-Items/Data/Tables" \
        --modid krs_items --name "KRS Items"  [--rename-suffix krs_items_fixed]

Without --rename-suffix the files are packaged unchanged (hyphenated suffix, like the repo). With it, every
`__<old suffix>` in file names and table names is replaced by the new suffix and the mod id is set to it, which is the
rule the engine enforces (patch suffix == mod id, lowercase letters and underscore only).
"""
import argparse
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_harness import write_mod  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", required=True)
    ap.add_argument("--src", required=True, help="folder with item/ rpg/ ... sub folders holding table__suffix.xml files")
    ap.add_argument("--modid", required=True)
    ap.add_argument("--name", required=True)
    ap.add_argument("--rename-suffix", help="replace the suffix of every patch with this one and use it as mod id")
    a = ap.parse_args()

    files = {}
    for dp, dn, fn in os.walk(a.src):
        for f in fn:
            if "__" not in f or not f.lower().endswith(".xml"):
                continue                       # only table patches; whole-table files (item.xml ...) are not PTF
            sub = os.path.relpath(dp, a.src).replace("\\", "/")
            text = open(os.path.join(dp, f), encoding="utf-8", errors="replace").read()
            name = f
            if a.rename_suffix:
                old = f.rsplit("__", 1)[1][:-4]
                name = f.rsplit("__", 1)[0] + "__" + a.rename_suffix + ".xml"
                text = re.sub(r'(<table name="[^"_]+(?:_[^"_]+)*)__' + re.escape(old) + '"', r'\1__' + a.rename_suffix + '"', text, flags=re.I)
            files[f"Libs/Tables/{sub}/{name}"] = text
    modid = a.rename_suffix or a.modid
    write_mod(a.game, modid, modid, a.name, files)
    print("packaged:", ", ".join(sorted(files)))


if __name__ == "__main__":
    main()
