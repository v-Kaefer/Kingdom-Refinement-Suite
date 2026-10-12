#!/usr/bin/env python3
"""
text_cut.py - cut a mod's change to a text file out as a small diff, and apply that diff to the game's own file when the module is built.

    python tools/text_cut.py make  --vanilla "Scripts.pak!Libs/AI/final/so_water_tube.xml" --mod-file FILE --out cut.diff
    python tools/text_cut.py apply --vanilla "Scripts.pak!Libs/AI/final/so_water_tube.xml" --diff cut.diff --out built.xml

`--vanilla` is `<pak under Data>!<member>` in the replica game (or a plain file path). Why not ship the mod's file: it would replace the whole game
file, and any update of the game would be undone. The diff holds only the changed lines plus 3 lines of context; `apply` finds every hunk in the
game's file by its context and refuses (writes nothing) when a hunk is missing, appears twice or the file has already changed there.
Nothing is installed or run.
"""
import argparse
import difflib
import os
import re
import sys
import zipfile

GAME = os.environ.get("KCD_GAME", r"E:\Kingdom-Refinement-Suite\WIP_Mods\KingdomComeDeliverance")
BS = chr(92)


def read_vanilla(spec):
    if "!" not in spec:
        return open(spec, "rb").read()
    pak, member = spec.split("!", 1)
    z = zipfile.ZipFile(os.path.join(GAME, "Data", pak.replace("/", BS)))
    for zi in z.infolist():
        if zi.filename.replace(BS, "/").lower() == member.lower():
            try:
                return z.read(zi)
            except zipfile.BadZipFile:
                zi.orig_filename = zi.filename.replace("/", BS)
                return z.open(zi).read()
    raise KeyError(member)


def lines(b):
    t = b.decode("utf-8")
    nl = "\r\n" if "\r\n" in t else "\n"
    return t.replace("\r\n", "\n").split("\n"), nl


def make(a):
    v, _ = lines(read_vanilla(a.vanilla))
    m, _ = lines(open(a.mod_file, "rb").read())
    d = list(difflib.unified_diff(v, m, "vanilla", "mod", lineterm="", n=3))
    open(a.out, "w", encoding="utf-8", newline="\n").write("\n".join(d) + "\n")
    add = sum(1 for x in d if x.startswith("+") and not x.startswith("+++"))
    rem = sum(1 for x in d if x.startswith("-") and not x.startswith("---"))
    print(f"{a.out}: {sum(1 for x in d if x.startswith('@@'))} hunks, +{add} -{rem}")


def hunks(diff_text):
    """-> list of (old start line, lines)"""
    out, cur = [], None
    for ln in diff_text.split("\n"):
        if ln.startswith("@@"):
            cur = []
            out.append((int(re.match(r"@@ -(\d+)", ln).group(1)) - 1, cur))
        elif cur is not None and ln[:1] in (" ", "+", "-"):
            cur.append(ln)
    return out


def apply(a):
    v, nl = lines(read_vanilla(a.vanilla))
    hs = hunks(open(a.diff, encoding="utf-8").read())
    result, pos, problems = [], 0, []
    for n, (want, h) in enumerate(hs, 1):
        old = [x[1:] for x in h if x[0] in " -"]
        new = [x[1:] for x in h if x[0] in " +"]
        hits = [i for i in range(pos, len(v) - len(old) + 1) if v[i:i + len(old)] == old]
        if not hits:
            problems.append(f"hunk {n}: its context is not in the game file (the file changed or the hunk was already applied)")
            continue
        i = min(hits, key=lambda x: abs(x - want))      # context can repeat in these files: take the place nearest to where the diff was made
        if abs(i - want) > 50:
            problems.append(f"hunk {n}: the nearest match is {abs(i - want)} lines away from where the diff was made")
            continue
        result += v[pos:i] + new
        pos = i + len(old)
    if problems:
        print("NOT WRITTEN:")
        for p in problems:
            print("  -", p)
        return 2
    result += v[pos:]
    open(a.out, "wb").write(nl.join(result).encode("utf-8"))
    print(f"wrote {a.out}: {len(hs)} hunks applied")
    return 0


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    m = sub.add_parser("make")
    m.add_argument("--vanilla", required=True)
    m.add_argument("--mod-file", required=True)
    m.add_argument("--out", required=True)
    p = sub.add_parser("apply")
    p.add_argument("--vanilla", required=True)
    p.add_argument("--diff", required=True)
    p.add_argument("--out", required=True)
    a = ap.parse_args()
    if a.cmd == "make":
        make(a)
        return 0
    return apply(a)


if __name__ == "__main__":
    sys.exit(main())
