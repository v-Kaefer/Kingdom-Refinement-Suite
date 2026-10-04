#!/usr/bin/env python3
"""
nexus_metadata.py - read mod METADATA from the Nexus Mods API v3 (names, status, file lists, versions, upload dates).
It never downloads a mod file: the download endpoints of the API are not used anywhere in this script.

    set NEXUS_API_KEY=<your personal key>        (Windows cmd)   /   $env:NEXUS_API_KEY="<key>"   (PowerShell)
    python tools/nexus_metadata.py                      names and status of every id of docs/mods-review/mods_index.csv
    python tools/nexus_metadata.py --files              also the file list and versions of the P1/P2 mods of mods_triage.csv
    python tools/nexus_metadata.py --ids 1860 2021 --files
    python tools/nexus_metadata.py --selftest           no network, no key: checks the script against a fake server

The key is read only from the environment variable, is sent only to https://api.nexusmods.com and is never written to a file,
a log or the output. Run this yourself: the session that wrote it does not handle your key. Create or revoke keys at
https://www.nexusmods.com/settings/api-keys.

Endpoints used (spec: openapi.yaml, Nexus Mods API 3.0.0, all read-only):
    GET  /games/{game_domain}/mods/{game_scoped_id}   -> game id (needed to build the composite ids)
    POST /mods/batch                                  -> name, summary, status, adult flag for up to 500 ids per call
    GET  /mods/{id}/files                             -> mod files with last upload date and version counts
    GET  /mod-files/{id}/versions                     -> version string, category and upload date of each version
Composite mod id = (game_id << 32) | game_scoped_id (the spec's "composite mod UID").

Writes docs/mods-review/nexus_metadata.csv and, with --files, docs/mods-review/nexus_files.csv. tools/triage_mods.py picks both up.
"""
import argparse
import csv
import json
import os
import sys
import time
import urllib.error
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paths  # noqa: E402

BASE = "https://api.nexusmods.com/v3"
GAME = "kingdomcomedeliverance"
UA = "KRS-review/1.0 (metadata only; github.com/v-Kaefer/Kingdom-Refinement-Suite)"


class Client:
    def __init__(self, key, transport=None, max_requests=600, pause=0.25):
        self.key, self.transport, self.max_requests, self.pause, self.count = key, transport, max_requests, pause, 0

    def call(self, method, path, body=None):
        if self.count >= self.max_requests:
            raise SystemExit(f"stopped after {self.count} requests (--max-requests); rerun later or raise the limit")
        self.count += 1
        if self.transport:
            return self.transport(method, path, body)
        data = json.dumps(body).encode() if body is not None else None
        req = urllib.request.Request(BASE + path, data=data, method=method, headers={
            "apikey": self.key, "Accept": "application/json", "Content-Type": "application/json", "User-Agent": UA,
            "Application-Name": "KRS-review"})
        for attempt in range(3):
            try:
                with urllib.request.urlopen(req, timeout=30) as r:
                    return json.loads(r.read().decode("utf-8"))
            except urllib.error.HTTPError as e:
                if e.code == 429:
                    wait = int(e.headers.get("Retry-After", "10"))
                    print(f"rate limited (429); waiting {wait}s", file=sys.stderr)
                    time.sleep(wait)
                    continue
                if e.code in (401, 403):
                    raise SystemExit(f"HTTP {e.code} from {path}: the key was refused or lacks access (check NEXUS_API_KEY)")
                if e.code == 404:
                    return None
                raise SystemExit(f"HTTP {e.code} from {path}")
            finally:
                time.sleep(self.pause)
        raise SystemExit("rate limit did not clear; try again later")


def read_ids(args):
    if args.ids:
        return sorted(set(args.ids))
    rows = list(csv.DictReader(open(os.path.join(paths.MODS_REVIEW, "mods_index.csv"), encoding="utf-8", newline="")))
    return sorted({int(r["id"]) for r in rows})


def priority_ids():
    p = os.path.join(paths.MODS_REVIEW, "mods_triage.csv")
    if not os.path.exists(p):
        return []
    return sorted({int(r["id"]) for r in csv.DictReader(open(p, encoding="utf-8", newline="")) if r["priority"] in ("P1", "P2")})


def run(client, ids, with_files, out_dir, game=GAME):
    first = client.call("GET", f"/games/{game}/mods/{ids[0]}")
    if not first or "data" not in first:
        raise SystemExit("could not read the game id from the first mod; pass --ids with a mod that exists")
    game_id = int(first["data"]["game_id"])
    composite = {i: (game_id << 32) | i for i in ids}
    by_uid = {str(v): k for k, v in composite.items()}
    rows = []
    uids = list(by_uid)
    for n in range(0, len(uids), 500):
        resp = client.call("POST", "/mods/batch", {"mod_ids": uids[n:n + 500]})
        for m in ((resp or {}).get("data") or {}).get("mods", []):
            rows.append({"id": by_uid.get(str(m["id"]), ""), "name": m.get("name", ""), "summary": (m.get("summary") or "").replace("\n", " "),
                         "status": m.get("status", ""), "adult": m.get("adult_content", "")})
    seen = {r["id"] for r in rows}
    rows += [{"id": i, "name": "", "summary": "", "status": "not returned (unknown id or no access)", "adult": ""} for i in ids if i not in seen]
    rows.sort(key=lambda r: int(r["id"]))
    with open(os.path.join(out_dir, "nexus_metadata.csv"), "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["id", "name", "summary", "status", "adult"], lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    print(f"{len(rows)} mods -> nexus_metadata.csv; statuses:", {s: sum(1 for r in rows if r['status'] == s) for s in sorted({r['status'] for r in rows})})

    if with_files:
        wanted = [i for i in priority_ids() if i in composite] if with_files == "priority" else ids
        frows = []
        for i in wanted:
            resp = client.call("GET", f"/mods/{composite[i]}/files")
            for mf in ((resp or {}).get("data") or {}).get("mod_files", []):
                vers = client.call("GET", f"/mod-files/{mf['id']}/versions")
                versions = ((vers or {}).get("data") or {}).get("versions", [])
                if not versions:
                    frows.append({"id": i, "file": mf.get("name", ""), "version": "", "category": "", "uploaded_at": mf.get("last_file_uploaded_at", ""),
                                  "primary": "", "file_active": mf.get("is_active", "")})
                for v in versions:
                    frows.append({"id": i, "file": mf.get("name", ""), "version": v.get("version", ""), "category": v.get("category", ""),
                                  "uploaded_at": v.get("uploaded_at", ""), "primary": v.get("is_primary", ""), "file_active": mf.get("is_active", "")})
        with open(os.path.join(out_dir, "nexus_files.csv"), "w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=["id", "file", "version", "category", "uploaded_at", "primary", "file_active"], lineterminator="\n")
            w.writeheader()
            w.writerows(frows)
        print(f"{len(frows)} file versions of {len(wanted)} mods -> nexus_files.csv")
    print(f"{client.count} requests used")


def selftest():
    import tempfile
    calls = []

    def fake(method, path, body):
        calls.append((method, path))
        if path.startswith("/games/"):
            return {"data": {"id": "7", "game_scoped_id": "1860", "game_id": "42", "name": "x"}}
        if path == "/mods/batch":
            return {"data": {"mods": [{"id": body["mod_ids"][0], "name": "Fake mod", "summary": "line1\nline2", "status": "published",
                                       "adult_content": False}]}}
        if path.endswith("/files"):
            return {"data": {"mod_files": [{"id": "9", "name": "Main", "is_active": True, "last_file_uploaded_at": "2026-01-01T00:00:00Z"}]}}
        if path.endswith("/versions"):
            return {"data": {"versions": [{"version": "1.1", "category": "main", "uploaded_at": "2026-01-01T00:00:00Z", "is_primary": True}]}}
        return None

    with tempfile.TemporaryDirectory() as d:
        run(Client("none", transport=fake, pause=0), [1860, 2021], "all", d)
        a = open(os.path.join(d, "nexus_metadata.csv"), encoding="utf-8").read()
        b = open(os.path.join(d, "nexus_files.csv"), encoding="utf-8").read()
    assert "1860,Fake mod" in a and "2021" in a and "not returned" in a, a
    assert "1860,Main,1.1,main" in b, b
    assert not any("download" in p for _, p in calls), calls
    print("selftest ok:", len(calls), "fake calls, no download endpoint touched, key not used")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--ids", nargs="*", type=int)
    ap.add_argument("--files", action="store_true", help="also fetch file lists and versions (P1/P2 mods, or --ids)")
    ap.add_argument("--max-requests", type=int, default=600)
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        selftest()
        return 0
    key = os.environ.get("NEXUS_API_KEY", "").strip()
    if not key:
        raise SystemExit("set the NEXUS_API_KEY environment variable first (see the header of this file)")
    ids = read_ids(a)
    run(Client(key, max_requests=a.max_requests), ids, ("all" if a.ids else "priority") if a.files else None, paths.MODS_REVIEW)
    return 0


if __name__ == "__main__":
    sys.exit(main())
