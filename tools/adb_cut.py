#!/usr/bin/env python3
"""
adb_cut.py - cut the animation changes out of a mod's kcd_male_database.adb and apply cuts to the game's file.

A mod that ships the whole .adb replaces the game's file, so two such mods can never be active together. This tool works at the level of
fragments instead: `make` writes only what a mod changed (its "cut"), `apply` builds one database from the game's file plus any number of cuts,
and checks that the result is exactly the game's fragments with those changes and nothing else.

    python tools/adb_cut.py make  --mod 2372 --mod-adb FILE [--base vanilla:010902|FILE] [--fid REGEX] [--tags REGEX] [--exclude REGEX]
                                  [--ops add,replace,remove] --out cut.xml [--note TEXT]
    python tools/adb_cut.py apply --cut cut1.xml [cut2.xml ...] [--base vanilla:010902|FILE] --out merged.adb
    python tools/adb_cut.py list  --cut cut.xml

`vanilla:<level>` reads the game's own file from the replica (levels: base, 010300 ... 010902); the default base of `apply` is the newest, 010902.
A fragment key is (fragment id element, Tags, FragTags). Text surgery keeps the rest of the file byte for byte (CRLF, indentation).
`replace` and `remove` carry the md5 of the fragment they expect; if the file they are applied to has a different one the cut is stale and the
tool reports it instead of guessing. Two cuts that touch the same fragment conflict unless they produce the same result.
Nothing is installed or run: files are read and one file is written.
"""
import argparse
import collections
import hashlib
import os
import re
import sys
import zipfile
import xml.etree.ElementTree as ET

GAME = os.environ.get("KCD_GAME", r"E:\Kingdom-Refinement-Suite\Mods WIP folder\KingdomComeDeliverance")
ADB = "Animations/Mannequin/ADB/kcd_male_database.adb"
BS = chr(92)
LEVELS = {"base": "Animations-part1.pak", "010300": "patch/ipl_patch_010300.pak", "010400": "patch/ipl_patch_010400.pak", "010500": "patch/ipl_patch_010500.pak",
          "010600": "patch/ipl_patch_010600.pak", "010700b": "patch/ipl_patch_010700b.pak", "010800": "patch/ipl_patch_010800.pak",
          "010900": "patch/ipl_patch_010900.pak", "010902": "patch/ipl_patch_010902.pak"}


def read_member(pak, name):
    z = zipfile.ZipFile(pak)
    for zi in z.infolist():
        if zi.filename.replace(BS, "/").lower() == name.lower():
            try:
                return z.read(zi)
            except zipfile.BadZipFile:
                zi.orig_filename = zi.filename.replace("/", BS)
                return z.open(zi).read()
    raise KeyError(name)


def load(spec, game=GAME):
    if spec.startswith("vanilla:"):
        return read_member(os.path.join(game, "Data", LEVELS[spec[8:]].replace("/", BS)), ADB).decode("utf-8")
    return open(spec, "rb").read().decode("utf-8")


def canon(raw):
    return re.sub(r"\s+", "", ET.tostring(ET.fromstring(raw), encoding="unicode"))


def digest(raw):
    return hashlib.md5(canon(raw).encode()).hexdigest()[:12]


def region(text):
    return text.index("<FragmentList>"), text.index("</FragmentList>")


def parse_text(text):
    """-> list of dicts: fid, tags, fragtags, raw, md5, start, end (offsets in text).
    The file is read with a real XML parser that reports where every <Fragment> starts and ends, so fragments written on one line, with other
    indentation or self-closing are found like the others (mods are made with different tools). The surrounding whole lines belong to the fragment."""
    import xml.parsers.expat as expat
    if not text.isascii():
        raise SystemExit("the animation database is expected to be ASCII")
    data = text.encode("ascii")
    out, stack, cur = [], [], {}
    p = expat.ParserCreate()

    def start(name, attrs):
        stack.append(name)
        if len(stack) == 4 and stack[1] == "FragmentList" and name == "Fragment":
            st = p.CurrentByteIndex
            tag_end = data.index(b">", st) + 1
            cur["f"] = dict(fid=stack[2], tags=attrs.get("Tags", ""), fragtags=attrs.get("FragTags", ""), start=st, selfclosing=data[tag_end - 2:tag_end] == b"/>", tag_end=tag_end)

    def end(name):
        if len(stack) == 4 and name == "Fragment" and "f" in cur:
            f = cur.pop("f")
            s = f["start"]
            e = f["tag_end"] if f["selfclosing"] else data.index(b">", p.CurrentByteIndex) + 1      # end of a self-closing tag, or of the end tag
            ls = data.rfind(b"\n", 0, s) + 1
            if data[ls:s].strip() == b"":
                s = ls
            nl = data.find(b"\n", e)
            if nl != -1 and data[e:nl].strip() == b"":
                e = nl + 1
            f["start"], f["end"] = s, e
            f["raw"] = text[s:e]
            f["md5"] = digest(f["raw"])
            out.append(f)
        stack.pop()
    p.StartElementHandler, p.EndElementHandler = start, end
    p.Parse(data, True)
    return out


def et_multiset(text):
    """independent of the offsets above: fragments counted through ElementTree (used to verify a merged file)"""
    root = ET.fromstring(re.sub(r"^\s*<\?xml[^>]*\?>", "", text))
    c = collections.Counter()
    for fl in root.findall("FragmentList"):
        for fid in fl:
            for fr in fid:
                if fr.tag == "Fragment":
                    c[(fid.tag, fr.get("Tags", ""), fr.get("FragTags", ""), hashlib.md5(re.sub(r"\s+", "", ET.tostring(fr, encoding="unicode")).encode()).hexdigest()[:12])] += 1
    return c


def multiset(frs):
    return collections.Counter((f["fid"], f["tags"], f["fragtags"], f["md5"]) for f in frs)


# ------------------------------------------------------------------------------------------------------------------------------ make
def make(a):
    base = parse_text(load(a.base))
    mod = parse_text(load(a.mod_adb))
    bm, mm = multiset(base), multiset(mod)
    fid_re = re.compile(a.fid) if a.fid else None
    tag_re = re.compile(a.tags) if a.tags else None
    exc_re = re.compile(a.exclude) if a.exclude else None
    want = set(a.ops.split(","))

    def keep(k):
        return (not fid_re or fid_re.search(k[0])) and (not tag_re or tag_re.search(k[1] + " " + k[2])) and not (exc_re and exc_re.search(k[1] + " " + k[2]))
    added, removed = mm - bm, bm - mm
    by_add, by_rem = collections.defaultdict(list), collections.defaultdict(list)
    for k, n in sorted(added.items()):          # a fragment can occur several times with the same content: keep every occurrence
        by_add[k[:3]].extend([k] * n)
    for k, n in sorted(removed.items()):
        by_rem[k[:3]].extend([k] * n)
    raw_of = {(f["fid"], f["tags"], f["fragtags"], f["md5"]): f["raw"] for f in mod}
    ops = []
    for key, adds in by_add.items():
        if not keep(key):
            continue
        rems = by_rem.get(key, [])
        for old, new in zip(rems, adds):
            if "replace" in want:
                ops.append(("replace", key, old[3], raw_of[new]))
        for new in adds[len(rems):]:
            if "add" in want:
                ops.append(("add", key, "", raw_of[new]))
        for old in rems[len(adds):]:
            if "remove" in want:
                ops.append(("remove", key, old[3], ""))
    for key, rems in by_rem.items():
        if key in by_add or not keep(key) or "remove" not in want:
            continue
        for old in rems:
            ops.append(("remove", key, old[3], ""))
    root = ET.Element("adbcut", mod=a.mod, base=a.base, note=a.note or "")
    for typ, (fid, tags, ft), old, raw in sorted(ops, key=lambda o: (o[1], o[0], o[2])):
        e = ET.SubElement(root, "op", type=typ, fid=fid, tags=tags, fragtags=ft)
        if old:
            e.set("old", old)
        if raw:
            e.set("new", digest(raw))
            e.text = "\n" + raw.replace("\r\n", "\n")
    ET.indent(root, space="  ")
    ET.ElementTree(root).write(a.out, encoding="utf-8", xml_declaration=True)
    print(f"cut {a.out}: {dict(collections.Counter(o[0] for o in ops))} (mod {a.mod}, relative to {a.base})")


# ------------------------------------------------------------------------------------------------------------------------------ cuts
def read_cut(path):
    root = ET.parse(path).getroot()
    ops = []
    for e in root.findall("op"):
        raw = e.text or ""
        raw = raw[1:] if raw.startswith("\n") else raw
        ops.append(dict(type=e.get("type"), fid=e.get("fid"), tags=e.get("tags") or "", fragtags=e.get("fragtags") or "", old=e.get("old") or "", new=e.get("new") or "", raw=raw,
                        cut=os.path.basename(path), mod=root.get("mod")))
    return root.get("mod"), root.get("base"), ops


def list_cut(a):
    mod, base, ops = read_cut(a.cut[0])
    print(f"mod {mod}, relative to {base}: {len(ops)} operations")
    for o in ops:
        print(f"  {o['type']:8s} {o['fid']:22s} Tags={o['tags'][:50]!r} FragTags={o['fragtags'][:50]!r}")


def apply(a):
    text = load(a.base)
    nl = "\r\n" if "\r\n" in text else "\n"
    base_frs = parse_text(text)
    expected = et_multiset(text)      # verification below uses ElementTree on both sides, independent of the offset parser
    if sum(expected.values()) != len(base_frs):
        raise SystemExit(f"the offset parser found {len(base_frs)} fragments, ElementTree {sum(expected.values())}: not safe to edit this file")
    allops, problems, seen, skipped = [], [], {}, []
    for c in a.cut:
        _, _, ops = read_cut(c)
        for o in ops:
            k = (o["fid"], o["tags"], o["fragtags"], o["old"] or ("add:" + o["new"]))
            ident = (o["type"], o["new"])
            if k in seen and seen[k][1] == o["cut"]:      # the same cut lists the same change twice: two copies of one fragment, both are applied
                allops.append(o)
                continue
            if k in seen:
                if seen[k][0] == ident:
                    print(f"  same change in {seen[k][1]} and {o['cut']} ({o['type']} {o['fid']}): applied once")
                    continue
                problems.append(f"conflict: {o['cut']} and {seen[k][1]} change {o['fid']} Tags={o['tags']!r} FragTags={o['fragtags']!r} differently")
                continue
            seen[k] = (ident, o["cut"])
            allops.append(o)
    edits, stats, claimed = [], collections.Counter(), set()
    for o in allops:
        cands = [f for f in base_frs if (f["fid"], f["tags"], f["fragtags"]) == (o["fid"], o["tags"], o["fragtags"])]
        raw = o["raw"].replace("\n", nl)
        if o["type"] in ("replace", "remove"):
            hit = [f for f in cands if f["md5"] == o["old"] and f["start"] not in claimed]
            if not hit:
                state = "already changed" if o["type"] == "replace" and any(f["md5"] == o["new"] for f in cands) else "stale (the file has a different fragment)"
                msg = f"{o['type']} {o['fid']} Tags={o['tags']!r} FragTags={o['fragtags']!r} from {o['cut']}: {state}"
                if a.skip_stale:
                    skipped.append((o["cut"], o["type"], o["fid"], o["tags"], o["fragtags"], state))
                else:
                    problems.append(msg)
                continue
            f = hit[0]
            claimed.add(f["start"])
            edits.append((f["start"], f["end"], raw if o["type"] == "replace" else ""))
            expected[(f["fid"], f["tags"], f["fragtags"], f["md5"])] -= 1
            if o["type"] == "replace":
                expected[(o["fid"], o["tags"], o["fragtags"], digest(raw))] += 1
        else:
            if any(f["md5"] == o["new"] for f in cands):
                stats["already present"] += 1
                continue
            blocks = [f for f in base_frs if f["fid"] == o["fid"]]
            if blocks:
                pos = max(f["end"] for f in blocks)
                edits.append((pos, pos, raw))
            else:
                pos = text.rindex("  </FragmentList>")
                edits.append((pos, pos, f"    <{o['fid']}>{nl}{raw}    </{o['fid']}>{nl}"))
            expected[(o["fid"], o["tags"], o["fragtags"], digest(raw))] += 1
        stats[o["type"]] += 1
    if skipped:
        print(f"  skipped {len(skipped)} operation(s) that do not fit the file (--skip-stale): " + ", ".join(f"{n} {st}" for st, n in collections.Counter((x[5], x[0]) for x in skipped).items()))
        if a.report:
            import csv
            with open(a.report, "w", newline="", encoding="utf-8") as fh:
                w = csv.writer(fh)
                w.writerow(["cut", "op", "fid", "tags", "fragtags", "why_skipped"])
                w.writerows(skipped)
    if problems:
        print("NOT WRITTEN, problems:")
        for p in problems:
            print("  -", p)
        return 2
    out = text
    for _, (s, e, new) in sorted(enumerate(edits), key=lambda x: (x[1][0], x[1][1], x[0]), reverse=True):
        out = out[:s] + new + out[e:]
    got = et_multiset(out)
    expected = +expected
    if got != expected:
        print("VERIFICATION FAILED: merged file differs from 'game file + cuts' in", sum(((got - expected) + (expected - got)).values()), "fragments; not written")
        return 3
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    open(a.out, "wb").write(out.encode("utf-8"))
    print(f"wrote {a.out}: {dict(stats)}; verified (ElementTree): the game's {len(base_frs)} fragments with exactly these changes ({sum(got.values())} now)")
    return 0


# ------------------------------------------------------------------------------------------------------------------------------ rebase
GAME_ADDED_TAGS = {"oppMale", "oppFemale", "stealthFront", "stealthBehind"}   # tags the game's patches appended to existing fragments' FragTags


def skeleton(el):
    return (el.tag, tuple(skeleton(c) for c in el))


def walk(el, path=()):
    yield path, el
    for i, c in enumerate(el):
        yield from walk(c, path + (i,))


def node_at(el, path):
    for i in path:
        el = el[i]
    return el


def attr_changes(b, t):
    """attribute differences between two fragments with the same structure: [(path, tag, attribute, old, new)]; None when the structure differs"""
    if skeleton(b) != skeleton(t):
        return None
    out = []
    for (path, be), (_, te) in zip(walk(b), walk(t)):
        for k in sorted(set(be.attrib) | set(te.attrib)):
            if be.get(k) != te.get(k):
                out.append((path, be.tag, k, be.get(k), te.get(k)))
    return out


def rebase(a):
    """Move a cut made on an older game file onto the current one, attribute by attribute (a 3-way merge inside each fragment)."""
    base = parse_text(load(a.cut_base))
    onto = parse_text(load(a.onto))
    mod, cbase, ops = read_cut(a.cut)
    by_key_base, by_key_onto = collections.defaultdict(list), collections.defaultdict(list)
    for f in base:
        by_key_base[(f["fid"], f["tags"], f["fragtags"])].append(f)
    for f in onto:
        by_key_onto[(f["fid"], f["tags"], f["fragtags"])].append(f)
    by_fid_onto = collections.defaultdict(list)
    for f in onto:
        by_fid_onto[f["fid"]].append(f)
    used = set()
    new_ops, report, per_attr = [], [], collections.Counter()
    status = collections.Counter()
    for o in ops:
        key = (o["fid"], o["tags"], o["fragtags"])
        if o["type"] != "replace":
            new_ops.append(o)
            status["not a replace: copied"] += 1
            continue
        cur = [f for f in by_key_onto[key] if f["start"] not in used]
        direct = [f for f in cur if f["md5"] == o["old"]]
        if direct:
            used.add(direct[0]["start"])
            new_ops.append(o)
            status["direct (the fragment is the same in the current game)"] += 1
            continue
        bfr = [f for f in by_key_base[key] if f["md5"] == o["old"]]
        if not bfr:
            report.append((o["fid"], o["tags"], o["fragtags"], "lost", "", "the cut's own base fragment was not found"))
            status["lost"] += 1
            continue
        B = ET.fromstring(bfr[0]["raw"])
        T = ET.fromstring(o["raw"])
        changes = attr_changes(B, T)
        if changes is None:
            report.append((o["fid"], o["tags"], o["fragtags"], "conflict", "", "the mod changed the structure of the fragment (children added or removed)"))
            status["conflict: structure changed by the mod"] += 1
            continue
        targets, how = [f for f in cur if skeleton(ET.fromstring(f["raw"])) == skeleton(B)], "same key"
        if not cur:
            # the game's patches added opponent tags to the fragment's FragTags (oppMale+oppFemale, and a stealthFront/stealthBehind split):
            # the same fragment under a longer key. Every longer key that only ADDS those tags is the same fragment.
            bt = set(o["fragtags"].split("+")) if o["fragtags"] else set()
            more = [f for f in by_fid_onto[o["fid"]] if f["tags"] == o["tags"] and f["start"] not in used and bt <= set(f["fragtags"].split("+"))
                    and (set(f["fragtags"].split("+")) - bt) <= GAME_ADDED_TAGS]
            targets, how = [f for f in more if skeleton(ET.fromstring(f["raw"])) == skeleton(B)], "same fragment under a longer key (the game added opponent tags)"
            cur = more
        if not targets:
            report.append((o["fid"], o["tags"], o["fragtags"], "conflict", "", "the game changed the structure of this fragment" if cur else "the fragment no longer exists in the current game"))
            status["conflict: structure changed by the game" if cur else "conflict: fragment gone"] += 1
            continue
        for f in targets:
            C = ET.fromstring(f["raw"])
            applied, clashes = [], []
            for path, tag, attr, old, new in changes:
                node = node_at(C, path)
                cur_val = node.get(attr)
                where = f"{tag}[{'/'.join(map(str, path))}]@{attr}"
                if cur_val == old:
                    if new is None:
                        del node.attrib[attr]
                    else:
                        node.set(attr, new)
                    applied.append(f"{where}: {old} -> {new}")
                    per_attr[(tag, attr)] += 1
                elif cur_val == new:
                    applied.append(f"{where}: already {new} in the game")
                else:
                    clashes.append(f"{where}: base {old}, game now {cur_val}, mod {new}")
            used.add(f["start"])
            real = [x for x in applied if "already" not in x]
            if not real and not clashes:
                status["already in the game"] += 1
                report.append((f["fid"], f["tags"], f["fragtags"], "already", "; ".join(applied), ""))
                continue
            if not real:
                report.append((f["fid"], f["tags"], f["fragtags"], "conflict", "", "; ".join(clashes)))
                status["conflict: every changed attribute was also changed by the game"] += 1
                continue
            ET.indent(C, space="  ", level=3)
            raw = "      " + ET.tostring(C, encoding="unicode").strip() + "\n"
            new_ops.append(dict(type="replace", fid=f["fid"], tags=f["tags"], fragtags=f["fragtags"], old=f["md5"], new=digest(raw), raw=raw, cut=o["cut"], mod=o["mod"]))
            tag_note = "" if how == "same key" else f" [{how}: was FragTags {o['fragtags']!r}]"
            if clashes:
                status["rebased, some attributes left out (the game changed them too)"] += 1
                report.append((f["fid"], f["tags"], f["fragtags"], "partial", "; ".join(applied) + tag_note, "; ".join(clashes)))
            else:
                status["rebased" + ("" if how == "same key" else " onto the longer key") + " (every attribute applied to the current fragment)"] += 1
                report.append((f["fid"], f["tags"], f["fragtags"], "rebased", "; ".join(applied) + tag_note, ""))
    root = ET.Element("adbcut", mod=mod, base=a.onto, note=f"rebased from {cbase} onto {a.onto} attribute by attribute (adb_cut rebase)")
    for o in new_ops:
        e = ET.SubElement(root, "op", type=o["type"], fid=o["fid"], tags=o["tags"], fragtags=o["fragtags"])
        if o["old"]:
            e.set("old", o["old"])
        if o["raw"]:
            e.set("new", digest(o["raw"]))
            e.text = "\n" + o["raw"].replace("\r\n", "\n")
    ET.indent(root, space="  ")
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    ET.ElementTree(root).write(a.out, encoding="utf-8", xml_declaration=True)
    print(f"rebased cut {a.out}: {len(new_ops)} of {len(ops)} operations kept")
    for k, n in status.most_common():
        print(f"  {n:4d}  {k}")
    if per_attr:
        print("  attributes moved onto the current fragments:", ", ".join(f"{t}.{at} x{n}" for (t, at), n in per_attr.most_common(8)))
    if a.report:
        import csv
        with open(a.report, "w", newline="", encoding="utf-8") as fh:
            w = csv.writer(fh)
            w.writerow(["fid", "tags", "fragtags", "status", "applied_changes", "left_out_or_reason"])
            w.writerows(report)


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("rebase")
    r.add_argument("--cut", required=True)
    r.add_argument("--cut-base", required=True, help="the game file the cut was made against, e.g. vanilla:base")
    r.add_argument("--onto", default="vanilla:010902")
    r.add_argument("--out", required=True)
    r.add_argument("--report")
    m = sub.add_parser("make")
    m.add_argument("--mod", required=True)
    m.add_argument("--mod-adb", required=True)
    m.add_argument("--base", default="vanilla:010902")
    m.add_argument("--fid")
    m.add_argument("--tags")
    m.add_argument("--exclude")
    m.add_argument("--ops", default="add,replace,remove")
    m.add_argument("--note")
    m.add_argument("--out", required=True)
    p = sub.add_parser("apply")
    p.add_argument("--cut", nargs="+", required=True)
    p.add_argument("--base", default="vanilla:010902")
    p.add_argument("--out", required=True)
    p.add_argument("--skip-stale", action="store_true", help="drop replace/remove operations whose expected fragment is not in the file (a cut made on an older base) and report them")
    p.add_argument("--report", help="CSV of the skipped operations")
    ls = sub.add_parser("list")
    ls.add_argument("--cut", nargs=1, required=True)
    a = ap.parse_args()
    if a.cmd == "make":
        make(a)
        return 0
    if a.cmd == "rebase":
        rebase(a)
        return 0
    if a.cmd == "list":
        list_cut(a)
        return 0
    return apply(a)


if __name__ == "__main__":
    sys.exit(main())
