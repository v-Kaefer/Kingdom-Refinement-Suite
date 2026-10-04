#!/usr/bin/env python3
"""
inventory_downloads.py - which of the listed mods were downloaded, which are missing, and sort the downloads into sub-folders.

    python tools/inventory_downloads.py --src "<folder with the downloaded archives>"            inventory only (writes the CSVs, moves nothing)
    python tools/inventory_downloads.py --src "<folder>" --sort                                  dry run: prints where every entry would go
    python tools/inventory_downloads.py --src "<folder>" --sort --apply                          moves the entries into sub-folders
    python tools/inventory_downloads.py --src "<folder>" --undo                                  moves everything back (uses _sort_manifest.csv)

SAFETY: the downloads are untrusted. This tool never opens, extracts, lists the inside of or runs an archive. It reads only file
NAMES, sizes and a SHA-256 of the bytes (to find identical copies), and it only renames (moves) entries on the same drive when
--sort --apply is given. Nothing is deleted. Folders that already exist inside the source are moved as they are, not read.

The mod id is read from the Nexus file name. Two shapes exist:
    old    <name>-<id>-<version parts>-<upload epoch>.<ext>          (the epoch is the upload time)
    new    <name> <id> <version> <upload date as 2026-07-30T00-33Z> <hash>.<ext>
Files without an id (a loose .pak that Vortex unpacked, a renamed file) are matched by name against the Vortex download folder
and against the mod names of the index; what cannot be matched goes to the folder _unmatched for a person to look at.

Inputs:  docs/mods-review/download_batches.csv (the ids that were asked for: batch 0 already had, 1 and 2 tabs opened, 3 shortlist only),
         docs/mods-review/mods_triage.csv (name, category, priority, KRS modules), the Vortex download folder (read-only listing).
Outputs: docs/mods-review/downloads_inventory.csv (one row per entry), docs/mods-review/downloads_missing.csv (asked for, not found),
         docs/mods-review/DOWNLOADS_STATUS.md (generated summary).
"""
import argparse
import collections
import csv
import datetime
import hashlib
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paths  # noqa: E402

D = paths.MODS_REVIEW
PATCH_1_9_7 = int(datetime.datetime(2026, 2, 13, tzinfo=datetime.timezone.utc).timestamp())
VORTEX = os.path.join(os.environ.get("APPDATA", ""), "Vortex", "downloads", "kingdomcomedeliverance")
ARCH_EXT = (".zip", ".7z", ".rar", ".7zip")
OLD = re.compile(r"^(?P<name>.+?)-(?P<id>\d{1,4})-(?P<rest>[^/\\]*?)(?:-(?P<ts>\d{10}))?(?: \(\d+\))?$")
NEW = re.compile(r"^(?P<name>.+?) (?P<id>\d{1,4}) (?P<ver>\S+) (?P<date>\d{4}-\d\d-\d\dT\d\d-\d\dZ) (?P<hash>\w+)$")
SKIP_DIRS = {"_unmatched", "_incomplete"}


def is_sort_folder(name):
    return name in SKIP_DIRS or name.startswith("c_")


def slug(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def parse(name):
    """-> (id or None, uploaded date or '', epoch or 0, is a copy such as 'name (1).zip')"""
    stem = name
    for e in ARCH_EXT + (".pak",):
        if stem.lower().endswith(e):
            stem = stem[:-len(e)]
            break
    copy = bool(re.search(r" \(\d+\)$", stem))
    m = NEW.match(re.sub(r" \(\d+\)$", "", stem))
    if m:
        d = datetime.datetime.strptime(m.group("date"), "%Y-%m-%dT%H-%MZ").replace(tzinfo=datetime.timezone.utc)
        return int(m.group("id")), d.strftime("%Y-%m-%d"), int(d.timestamp()), copy
    m = OLD.match(stem)
    if m:
        ts = int(m.group("ts")) if m.group("ts") else 0
        up = datetime.datetime.fromtimestamp(ts, datetime.timezone.utc).strftime("%Y-%m-%d") if ts else ""
        return int(m.group("id")), up, ts, copy
    return None, "", 0, copy


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def norm(text):
    return re.sub(r"[^a-z0-9]+", "", text.lower())


def read_csv(path):
    return list(csv.DictReader(open(path, encoding="utf-8", newline=""))) if os.path.exists(path) else []


def vortex_names():
    """stem (without extension) of every file in the Vortex download folder -> id; names only, nothing is opened"""
    out = {}
    if os.path.isdir(VORTEX):
        for n in os.listdir(VORTEX):
            i, _, _, _ = parse(n)
            if i:
                out[norm(os.path.splitext(n)[0])] = i
    return out


def match_without_id(name, vortex, mods):
    """a loose file such as Dice.pak or earlybird.pak: try the Vortex download names, then the Nexus mod names (exact or contained)"""
    key = norm(os.path.splitext(name)[0])
    if len(key) < 4:
        return None, ""
    hits = [i for k, i in vortex.items() if key in k]
    if len(set(hits)) == 1:
        return hits[0], "matched by name in the Vortex download folder"
    hits = [int(r["id"]) for r in mods.values() if key and (key == norm(r["name"]) or (len(key) >= 6 and key in norm(r["name"])))]
    if len(set(hits)) == 1:
        return hits[0], "matched by name in the index"
    return None, ""


def inventory(src):
    mods = {int(r["id"]): r for r in read_csv(os.path.join(D, "mods_triage.csv"))}
    batches = {int(r["id"]): r for r in read_csv(os.path.join(D, "download_batches.csv"))}
    vortex = vortex_names()
    rows = []   # (sort folder or "", entry name, is a directory); the inside of an entry is never listed
    for n in sorted(os.listdir(src)):
        p = os.path.join(src, n)
        if n == "_sort_manifest.csv":
            continue
        if os.path.isdir(p) and is_sort_folder(n):
            rows += [(n, c, os.path.isdir(os.path.join(p, c))) for c in sorted(os.listdir(p))]
        else:
            rows.append(("", n, os.path.isdir(p)))
    out = []
    for folder, n, is_dir in rows:
        p = os.path.join(src, folder, n)
        kind = "folder (already extracted)" if is_dir else ("incomplete download" if n.endswith(".crdownload") else
               "archive" if n.lower().endswith(ARCH_EXT) else "loose file")
        nid, up, ts, copy = parse(n)
        how = "file name" if nid else ""
        if nid is None and kind != "incomplete download":
            nid, how = match_without_id(n, vortex, mods)
        size = "" if is_dir else os.path.getsize(p)
        out.append({"entry": n, "folder": folder, "kind": kind, "size_bytes": size,
                    "sha256": "" if is_dir or kind == "incomplete download" else sha256(p),
                    "id": nid or "", "id_from": how, "copy_of_name": "yes" if copy else "", "uploaded": up,
                    "uploaded_after_1.9.7": ("yes" if ts >= PATCH_1_9_7 else "no") if ts else ""})
    by_hash = collections.defaultdict(list)
    for r in out:
        if r["sha256"]:
            by_hash[r["sha256"]].append(r)
    for r in out:
        t = mods.get(r["id"] and int(r["id"]), {})
        b = batches.get(r["id"] and int(r["id"]), {})
        twins = [x["entry"] for x in by_hash.get(r["sha256"], []) if x is not r] if r["sha256"] else []
        r.update({"mod": t.get("name", ""), "category": t.get("category", ""), "priority": t.get("priority", ""),
                  "krs_modules": t.get("krs_modules", ""), "nexus_status": t.get("nexus_status", ""),
                  "batch": b.get("batch", "not asked for") if r["id"] else "", "identical_to": " | ".join(twins)})
        if r["kind"] == "incomplete download":
            r["status"] = "incomplete: download again"
        elif not r["id"]:
            r["status"] = "no mod id: look at it by hand"
        elif not t:
            r["status"] = "id is not in the index (a misleading link?)"
        elif not b:
            r["status"] = "downloaded, but not in any batch asked for"
        else:
            r["status"] = "ok"
    return out, mods, batches


def destination(r):
    if r["kind"] == "incomplete download":
        return "_incomplete"
    if r["status"].startswith(("no mod id", "id is not")):
        return "_unmatched"
    return "c_" + (slug(r["category"]) or "unclassified")


def write_outputs(out, mods, batches, src):
    cols = ["entry", "folder", "kind", "size_bytes", "sha256", "id", "id_from", "mod", "category", "priority", "krs_modules",
            "nexus_status", "batch", "uploaded", "uploaded_after_1.9.7", "copy_of_name", "identical_to", "status"]
    with open(os.path.join(D, "downloads_inventory.csv"), "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore", lineterminator="\n")
        w.writeheader()
        w.writerows(sorted(out, key=lambda r: (int(r["id"]) if r["id"] else 99999, r["entry"])))
    have = {int(r["id"]) for r in out if r["id"] and r["kind"] != "incomplete download"}
    vortex_ids = set(vortex_names().values())
    missing = []
    for i, b in sorted(batches.items(), key=lambda kv: (kv[1]["batch"], kv[0])):
        if i in have:
            continue
        t = mods.get(i, {})
        note = "in the Vortex download folder" if i in vortex_ids else ""
        missing.append({"id": i, "mod": t.get("name", ""), "batch": b["batch"], "priority": t.get("priority", ""),
                        "category": t.get("category", ""), "krs_modules": t.get("krs_modules", ""),
                        "in_shortlist": b["in_shortlist"], "nexus_status": t.get("nexus_status", ""), "note": note,
                        "url": f"https://www.nexusmods.com/kingdomcomedeliverance/mods/{i}?tab=files"})
    with open(os.path.join(D, "downloads_missing.csv"), "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(missing[0]) if missing else ["id"], lineterminator="\n")
        w.writeheader()
        w.writerows(missing)

    cnt = collections.Counter(r["status"] for r in out)
    kinds = collections.Counter(r["kind"] for r in out)
    ids = {int(r["id"]) for r in out if r["id"]}
    mb = collections.Counter(m["batch"] for m in missing)
    asked = collections.Counter(b["batch"] for b in batches.values())
    L = ["# Downloads status", "",
         "> **GENERATED** by `tools/inventory_downloads.py`: do not edit | **Kind:** status | **Trust:** file names, sizes and hashes only (no archive was opened) | **Game version:** 1.9.8", "",
         f"Read on {datetime.date.today().isoformat()} from the downloads folder. Nothing was extracted or run; entries were only counted, hashed and, if `--sort --apply` was used, moved.", "",
         "## Counts", "", "| What | Number |", "|---|---|",
         f"| Entries in the folder | {len(out)} ({', '.join(f'{v} {k}' for k, v in sorted(kinds.items()))}) |",
         f"| Distinct mod ids found | {len(ids)} |"]
    L += [f"| {k} | {v} |" for k, v in sorted(cnt.items())]
    L += ["", "## Asked for versus found", "", "| Batch | Asked for | Missing |", "|---|---|---|"]
    for b in sorted(asked):
        L.append(f"| {b} | {asked[b]} | {mb.get(b, 0)} |")
    L += ["", f"Missing list with links: [`downloads_missing.csv`](downloads_missing.csv) ({len(missing)} ids). Full inventory: [`downloads_inventory.csv`](downloads_inventory.csv).", ""]
    ident = [r for r in out if r["identical_to"]]
    if ident:
        L += ["## Identical copies (same SHA-256)", ""] + [f"- `{r['entry']}` = {r['identical_to']}" for r in ident] + [""]
    odd = [r for r in out if r["status"] != "ok"]
    if odd:
        L += ["## To look at by hand", "", "| Entry | Status | Id | Mod |", "|---|---|---|---|"]
        L += [f"| `{r['entry']}` | {r['status']} | {r['id']} | {r['mod']} |" for r in odd]
        L.append("")
    after = [r for r in out if r["uploaded_after_1.9.7"] == "yes"]
    L += ["## Uploaded after the 1.9.7 patch (13 Feb 2026)", "",
          f"{len(after)} of the archives carry an upload date later than the patch (read from the name). An upload date is not a compatibility test.", ""]
    open(os.path.join(D, "DOWNLOADS_STATUS.md"), "w", encoding="utf-8", newline="\n").write("\n".join(L))
    print(f"{len(out)} entries; ids found {len(ids)}; missing {len(missing)}; status {dict(cnt)}")


def sort_entries(out, src, apply):
    manifest = os.path.join(src, "_sort_manifest.csv")
    moves = []
    for r in out:
        dest = destination(r)
        if r["folder"] == dest:
            continue
        moves.append((os.path.join(r["folder"], r["entry"]), os.path.join(dest, r["entry"])))
    per = collections.Counter(os.path.dirname(b) for _, b in moves)
    for k, v in sorted(per.items()):
        print(f"  {k}: {v}")
    if not apply:
        print(f"dry run: {len(moves)} moves; add --apply to do them")
        return
    done = []
    for a, b in moves:
        pa, pb = os.path.join(src, a), os.path.join(src, b)
        if os.path.exists(pb):
            print("skip (target exists):", b)
            continue
        os.makedirs(os.path.dirname(pb), exist_ok=True)
        os.rename(pa, pb)
        done.append((a, b))
    old = [tuple(r) for r in csv.reader(open(manifest, encoding="utf-8"))][1:] if os.path.exists(manifest) else []
    with open(manifest, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["from", "to"])
        w.writerows(old + done)
    print(f"moved {len(done)} entries; undo with --undo")


def undo(src):
    manifest = os.path.join(src, "_sort_manifest.csv")
    if not os.path.exists(manifest):
        raise SystemExit("no _sort_manifest.csv: nothing to undo")
    rows = [tuple(r) for r in csv.reader(open(manifest, encoding="utf-8"))][1:]
    n = 0
    for a, b in reversed(rows):
        pa, pb = os.path.join(src, a), os.path.join(src, b)
        if os.path.exists(pb) and not os.path.exists(pa):
            os.makedirs(os.path.dirname(pa) or src, exist_ok=True)
            os.rename(pb, pa)
            n += 1
    os.remove(manifest)
    for d in os.listdir(src):
        p = os.path.join(src, d)
        if os.path.isdir(p) and is_sort_folder(d) and not os.listdir(p):
            os.rmdir(p)
    print(f"moved back {n} entries")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--src", required=True)
    ap.add_argument("--sort", action="store_true")
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--undo", action="store_true")
    a = ap.parse_args()
    if a.undo:
        undo(a.src)
        return 0
    out, mods, batches = inventory(a.src)
    write_outputs(out, mods, batches, a.src)
    if a.sort:
        sort_entries(out, a.src, a.apply)
    return 0


if __name__ == "__main__":
    sys.exit(main())
