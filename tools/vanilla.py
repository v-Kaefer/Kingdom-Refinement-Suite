#!/usr/bin/env python3
"""
vanilla.py - read tables of the unmodified game (Data/Tables.pak) and build complete patch rows from them.

    python tools/vanilla.py <table path in the pak, e.g. rpg/perk> [key=value ...] [--game "<KCD folder>"]

Prints the header and the rows whose attributes match every key=value (all rows when none are given, first 40 shown).
Used as a library by tools/build_module.py (`complete_row`, `patch_xml`).
"""
import os
import re
import sys
import xml.etree.ElementTree as ET
import zipfile

DEFAULT_GAME = os.environ.get("KCD_GAME", r"E:\Kingdom-Refinement-Suite\WIP_Mods\KingdomComeDeliverance")


def read_member(z, zi):
    try:
        return z.open(zi).read()
    except zipfile.BadZipFile:
        zi.orig_filename = zi.filename.replace("/", "\\")
        return z.open(zi).read()


def load(table, game=DEFAULT_GAME):
    """table is 'rpg/perk' -> (columns [(name, type)], rows [dict])."""
    z = zipfile.ZipFile(os.path.join(game, "Data", "Tables.pak"))
    raw = read_member(z, z.getinfo(f"Libs/Tables/{table}.xml")).decode("utf-8", "replace")
    t = ET.fromstring(re.sub(r"^\s*<\?xml[^>]*\?>", "", raw)).find("table")
    cols = [(c.get("name"), c.get("type")) for c in t.findall("./header/column")]
    rows = [dict(r.attrib) for r in t.findall("./rows/row")]
    return cols, rows


def complete_row(cols, vanilla_row, **changes):
    """a patch row with every column of the table: vanilla values, then the changes."""
    row = {c: vanilla_row.get(c, "") for c, _ in cols}
    for k, v in changes.items():
        if k not in row:
            raise KeyError(f"column {k} is not in the table header")
        row[k] = str(v)
    return row


def patch_xml(table_name, cols, rows, comments=None):
    """xml text of a patch file. `rows` are dicts with every column; `comments` maps row index -> comment text."""
    esc = lambda s: str(s).replace("&", "&amp;").replace('"', "&quot;").replace("<", "&lt;").replace(">", "&gt;")
    out = ['<?xml version="1.0" encoding="us-ascii"?>', '<database name="hammerheart">',
           f'  <table name="{table_name}" version="1">', "    <header>"]
    out += [f'      <column name="{n}" type="{t}" />' for n, t in cols]
    out += ["    </header>", "    <rows>"]
    for i, r in enumerate(rows):
        if comments and i in comments:
            out.append(f"      <!-- {comments[i]} -->")
        out.append("      <row " + " ".join(f'{c}="{esc(r.get(c, ""))}"' for c, _ in cols) + " />")
    out += ["    </rows>", "  </table>", "</database>", ""]
    return "\n".join(out)


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--game")]
    game = DEFAULT_GAME
    for i, a in enumerate(sys.argv):
        if a == "--game":
            game = sys.argv[i + 1]
            args = [x for x in args if x != game]
    if not args:
        print(__doc__)
        return 2
    cols, rows = load(args[0], game)
    flt = dict(a.split("=", 1) for a in args[1:])
    hit = [r for r in rows if all(r.get(k) == v for k, v in flt.items())]
    print("columns:", ", ".join(f"{n}:{t}" for n, t in cols))
    print(f"{len(hit)} of {len(rows)} rows")
    for r in hit[:40]:
        print(r)
    return 0


if __name__ == "__main__":
    sys.exit(main())
