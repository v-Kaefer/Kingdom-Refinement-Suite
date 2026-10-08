#!/usr/bin/env python3
"""
build_qol_reshield.py - assemble the optional Reshield (Nexus 2313, Conway) companion of krs_qol from the author's own archive.

    python tools/build_qol_reshield.py --from "<Reshield 2313 ... .zip>" [--install "<KCD folder>"]

Nothing of the mod is stored in the repository: the two files are read from the archive, checked against the sha256 in modules/krs_qol/README.md,
and written unchanged to dist/reshield (and to <KCD folder>/Mods/reshield with --install, which also adds `reshield` to Mods/mod_order.txt).
Only those two members are read; nothing is run. For testing: permission to include Reshield in a KRS package is not asked yet, do not publish dist/reshield.
"""
import argparse
import hashlib
import os
import zipfile

WANT = {
    "Reshield/Data/reshield.pak": ("Data/reshield.pak", "4134e5531fa87eceef5464722d34cc01d5ffa90eaa323274a1f35df0bd804b7f"),
    "Reshield/mod.manifest": ("mod.manifest", "1da90973688458ac9ba8ad279b8d9cf6c1490db4b702cd7ad9c22693af90dbe8"),
}
HERE = os.path.dirname(os.path.abspath(__file__))


def write_all(dest, data):
    for rel, blob in data.items():
        p = os.path.join(dest, *rel.split("/"))
        os.makedirs(os.path.dirname(p), exist_ok=True)
        open(p, "wb").write(blob)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--from", dest="src", required=True)
    ap.add_argument("--install")
    a = ap.parse_args()
    data = {}
    with zipfile.ZipFile(a.src) as z:
        for member, (rel, sha) in WANT.items():
            blob = z.read(member)
            if hashlib.sha256(blob).hexdigest() != sha:
                raise SystemExit(f"{member}: sha256 differs from the one recorded in the README; not using this archive")
            data[rel] = blob
    out = os.path.join(os.path.dirname(HERE), "dist", "reshield")
    write_all(out, data)
    print("wrote", out)
    if a.install:
        mods = os.path.join(a.install, "Mods")
        write_all(os.path.join(mods, "reshield"), data)
        order = os.path.join(mods, "mod_order.txt")
        lines = [l.strip() for l in open(order, encoding="utf-8").read().splitlines() if l.strip()]
        if "reshield" not in lines:
            lines.append("reshield")
            open(order, "w", encoding="utf-8", newline="\r\n").write("\r\n".join(lines) + "\r\n")
        print("installed in", mods)


if __name__ == "__main__":
    main()
