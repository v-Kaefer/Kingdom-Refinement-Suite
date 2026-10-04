#!/usr/bin/env python3
"""
triage_mods.py - classify and triage every mod of docs/mods-review/mods_index.csv with explicit, repeatable rules.

    python tools/triage_mods.py       writes docs/mods-review/mods_triage.csv and docs/mods-review/TRIAGE.md (GENERATED)

Evidence classes (what the row stands on, strongest first):
    A  the archive was read (tools/analyze_mod_archives.py, docs/mods-review/archive_analysis.csv)
    N  the Nexus API (docs/mods-review/nexus_metadata.csv, written by tools/nexus_metadata.py): name, status and the author's own summary
    B  a Nexus search result whose URL id matched the title (docs/mods-review/search_evidence.csv)
    C  the title only (browser tab title, author label)
    D  nothing but the id
Priority:  P1 act now (our own published files; measured collision with a KRS row)
           P2 compare or check before combining (overlaps a KRS module, possible fix of a game bug, disabled on 1.9.8)
           P3 optional or unmapped (no table overlap expected, or no KRS area flagged)
           P4 outside the suite's scope (adult content, visual presets)
The rules are in this file on purpose (functions `classify`, `modules_for`, `decide`): change them and rerun, nothing is hand-edited.
No mod page or archive beyond the ones listed above was read; Nexus returns HTTP 403 from this environment.
"""
import collections
import csv
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paths  # noqa: E402

D = paths.MODS_REVIEW

CATEGORY_KEYWORDS = [  # applied to the name when the title list gave no category
    (r"reshade|enb\b|preset", "Reshade / ENB / visual preset"),
    (r"\bmap\b|maps\b|hud|\bui\b|icon|font|compass|inventor", "Maps / UI / HUD"),
    (r"weather|sky|fog|cloud|snow|rain|texture|hair|face|upscale|grass|tree|vegetation|shadow", "World / weather / visuals"),
    (r"tool|guide|manager|extender|library|resource|mod order|editor|organizer", "Tools / reference"),
    (r"dice|animation|sound|music|audio|loading ?screen", "Animations / audio"),
    (r"merchant|money|price|shop|groschen|trade|economy", "Economy / merchants"),
    (r"arrow|archery|\bbow", "Archery / arrows"),
    (r"xp|experience|perk|skill|rpg", "Progression / XP / perks"),
    (r"poison|potion|alchemy|food|drink|spoil|hunger|sleep|herb|brew|schnapps", "Alchemy / food / survival"),
    (r"crime|steal|stealth|loot|pickpocket|lock", "Crime / stealth / loot"),
    (r"combat|master strike|parry|riposte|enemies|\bai\b", "Combat / AI"),
    (r"horse|caparison|mount", "Horses"),
    (r"encounter|quest|story|castle|fan |lore|npc|henry ", "Quests / lore / content"),
    (r"sword|dagger|armor|armour|\bset\b|helm|waffenrock|kilij|joyeuse|baselard|hounskull|axe|mace|shield|weapon|ring\b|cuirass|outfit|clothes|hood", "Weapons / armor / items"),
    (r"\bfix\b|fixed|patch", "Fix bundle"),
    (r"maintenance|repair|durab|sharpen|armourer", "Repair / durability"),
    (r"nourishment|energy|\bbed\b|stay clean|dirty|dirt\b|camping|hungry|spoil", "Alchemy / food / survival"),
    (r"slo mo|slow ?mo|targeting|auto ?lock|tackle", "Combat / AI"),
    (r"sorting|sorted|labelled|labeled|strings|parameters plus|easyedit|cheat|mod manager|referenced", "Tools / reference"),
    (r"assassin|sneak|knock", "Crime / stealth / loot"),
    (r"architect|fishing|enhanced edition|encounter", "Quests / lore / content"),
    (r"guild items|eyes|time-?hd|headbob|camera", "World / weather / visuals"),
]
MODULE_KEYWORDS = {  # topical words in the NAME and the search summary (word boundaries: "already" must not match "read")
    "krs_perks": r"\bperks?\b|riposte|master ?strikes?|\bparry|\bparries|\bxp\b|experience|\bskills?\b",
    "krs_items": r"\bfood|spoil|potion|poison|alchem|\bdrinks?\b|hunger|nourish|\bsleep|\bbeds?\b|\bbooks?\b|\breading\b|\benergy\b|nutrition|schnapps|\bbrew|alcohol|digest",
    "krs_qol": r"\bcarry|\bweight|repair|\bkits?\b|durab|\bherbs?\b|harvest|timed quest|quest indicator|groschen",
    "krs_bow (planned)": r"\barrows?\b|archery|\bbows?\b|\baim|\bdraw\b|quiver",
}
# the category alone already places a mod in a KRS area
CATEGORY_MODULE = {
    "Combat / AI": ["krs_perks"], "Progression / XP / perks": ["krs_perks"], "Archery / arrows": ["krs_bow (planned)"],
    "Alchemy / food / survival": ["krs_items"], "Repair / durability": ["krs_qol"],
}
# words that make a collision with a KRS row likely when the search summary or the name contains them
SAME_TABLE_WORDS = r"rpg_param|rpg param|\bcarry|\bherb|aim spread|aim shake|repair kit|repair price|alcohol|\bperks?\b|xp gain|xp tables|bowcharge|\bstamina"
OUT_OF_SCOPE = ("Adult",)
VISUAL = ("Reshade", "Graphics config")
OPTIONAL = ("Maps / UI", "World", "Quests", "Animations", "Tools")


def classify(row):
    cat = row.get("category", "")
    if cat:
        return cat, "title list"
    name = row.get("name", "")
    for pat, c in CATEGORY_KEYWORDS:
        if re.search(pat, name, re.I):
            return c, "name keywords"
    return "(unclassified)", "no rule matched"


def modules_for(row, cat, ev, arc):
    text = " ".join([row.get("name", ""), row.get("krs_area", ""), ev.get("summary", "") if ev else ""]).lower()   # not the category name
    mods = [m for m, pat in MODULE_KEYWORDS.items() if re.search(pat, text)]
    for m in CATEGORY_MODULE.get(cat, []):
        if m not in mods:
            mods.append(m)
    if arc and arc.get("krs_collisions"):
        for m in {c.split(":")[0] for c in arc["krs_collisions"].split("; ")}:
            if m not in mods:
                mods.append(m)
    # a module name only counts for gameplay categories; presets, maps and tools never touch the tables
    if any(cat.startswith(x) for x in VISUAL + OPTIONAL + OUT_OF_SCOPE):
        mods = []
    return sorted(mods)


def decide(row, cat, mods, ev, arc):
    """-> (priority, action, reason)"""
    i = int(row["id"])
    ptf = row.get("ptf") == "PTF" or "PTF" in row.get("install", "") or "PTF" in row.get("name", "")
    fix = (row.get("fix_status", "") + " " + row.get("fix_type", "")).lower()
    if i == 2017:
        return "P1", "Replace the published release", "archive read: 7z renamed .pak, no Libs/ root, suffix != id, manifest 1.9.x"
    if arc and arc.get("krs_collisions"):
        return "P1", "Resolve the measured row collision with a KRS module", "same table and key as " + arc["krs_collisions"].split("; ")[0]
    if arc and arc.get("loads_on_1.9.8", "").startswith("NO"):
        return "P2", "Disabled on 1.9.8 by its manifest: edit the version line (author) and retest", arc["loads_on_1.9.8"]
    if any(cat.startswith(x) for x in OUT_OF_SCOPE):
        return "P4", "Out of scope", "adult content"
    if any(cat.startswith(x) for x in VISUAL):
        return "P4", "Optional visual: no table overlap expected", cat
    if "candidate" in fix or ("bug fix" in fix and "another" not in fix):
        return "P2", "Check on 1.9.8 whether the fix is still needed", row.get("fix_status") or row.get("fix_type")
    if mods:
        likely = ev and re.search(SAME_TABLE_WORDS, (ev.get("summary", "") + " " + row.get("name", "")).lower())
        reason = "evidence names the same values" if likely else "title-based area match"
        if ptf:
            return "P2", "Study the rows and compare with " + ", ".join(mods) + " (PTF-shaped)", reason
        return "P2", "Compare tables with " + ", ".join(mods) + " before combining", reason
    if any(cat.startswith(x) for x in OPTIONAL):
        return "P3", "Optional companion: outside the PTF scope, check version support", cat
    if cat == "(unclassified)":
        return "P3", "Classify by hand (no title rule matched)", "name: " + row.get("name", "")[:40]
    return "P3", "Review: gameplay mod not mapped to a KRS module", cat


def main():
    rows = list(csv.DictReader(open(os.path.join(D, "mods_index.csv"), encoding="utf-8", newline="")))
    arcs = {}
    p = os.path.join(D, "archive_analysis.csv")
    if os.path.exists(p):
        for a in csv.DictReader(open(p, encoding="utf-8", newline="")):
            arcs.setdefault(int(a["nexus_id"]), []).append(a)
    evs = {int(e["id"]): e for e in csv.DictReader(open(os.path.join(D, "search_evidence.csv"), encoding="utf-8", newline=""))}
    for e in evs.values():
        e["summary"] = e.get("summary", "")
    # optional: files written by tools/nexus_metadata.py when the author runs it with a personal API key
    nm = {}
    p = os.path.join(D, "nexus_metadata.csv")
    if os.path.exists(p):
        nm = {int(x["id"]): x for x in csv.DictReader(open(p, encoding="utf-8", newline="")) if x["id"]}
    for i, m in nm.items():   # the API summary is the mod author's own short description: it joins the evidence text
        e = evs.get(i) or {"id": str(i), "title_seen": m["name"], "author": "", "version": "", "updated": "", "tested_on": "", "summary": ""}
        e["summary"] = (e.get("summary", "") + " " + m.get("summary", "")).strip()
        e["_api"] = True
        evs[i] = e
    excluded = {}   # docs/mods-review/excluded_mods.csv: mods the author does not want (id, name, reason, decided)
    p = os.path.join(D, "excluded_mods.csv")
    if os.path.exists(p):
        excluded = {int(x["id"]): x for x in csv.DictReader(open(p, encoding="utf-8", newline=""))}
    nf = collections.defaultdict(list)
    p = os.path.join(D, "nexus_files.csv")
    if os.path.exists(p):
        for x in csv.DictReader(open(p, encoding="utf-8", newline="")):
            nf[int(x["id"])].append(x)

    out = []
    for r in rows:
        i = int(r["id"])
        arc_list = arcs.get(i, [])
        arc = next((a for a in arc_list if a.get("krs_collisions")), None) or next((a for a in arc_list if a["loads_on_1.9.8"].startswith("NO")), None) \
            or (arc_list[0] if arc_list else None)
        ev = evs.get(i)
        cat, cat_src = classify(r)
        mods = modules_for(r, cat, ev, arc)
        prio, action, reason = decide(r, cat, mods, ev, arc)
        meta = nm.get(i, {})
        if meta.get("status") in ("removed", "removed_by_staff", "hidden", "under_moderation", "not_published") and prio != "P1":
            prio, action, reason = "P4", "Removed or hidden on Nexus: drop it or find a replacement", "Nexus API status: " + meta["status"]
        if i in excluded:
            prio, action, reason = "P4", "Excluded by the author: do not download or review", excluded[i]["reason"]
        uploads = sorted(x["uploaded_at"] for x in nf.get(i, []) if x.get("uploaded_at") and x.get("category") not in ("removed", "archived"))
        last_up = uploads[-1][:10] if uploads else ""
        latest = next((x["version"] for x in sorted(nf.get(i, []), key=lambda y: y.get("uploaded_at", ""), reverse=True)
                       if x.get("category") not in ("removed", "archived")), "")
        evidence = "A archive" if arc_list else ("N Nexus API" if ev and ev.get("_api") else ("B search result" if ev else ("C title" if r["name"] else "D id only")))
        if arc_list:
            load = arc["loads_on_1.9.8"]
        elif re.search(r"1\.9\.8", r.get("versions", "") + r.get("check_1.9.8", "") + (ev["version"] if ev else "")):
            load = "states 1.9.8 (page summary)"
        elif ev and ev.get("tested_on"):
            load = "states " + ev["tested_on"] + " (page summary)"
        else:
            load = "unknown (manifest not seen)"
        collision = ("measured: " + arc["krs_collisions"]) if arc and arc.get("krs_collisions") else \
            ("likely: evidence names the same values" if mods and ev and re.search(SAME_TABLE_WORDS, (ev["summary"] + " " + r["name"]).lower())
             else ("possible: title-based" if mods else "none expected"))
        out.append({
            "id": i, "name": r["name"], "scope": r["scope"], "category": cat, "category_source": cat_src, "ptf": r["ptf"],
            "krs_modules": " ".join(mods), "evidence": evidence, "load_on_1.9.8": load, "row_collision": collision,
            "priority": prio, "action": action, "reason": reason,
            "last_updated": last_up or (ev["updated"] if ev else ""), "author": (ev["author"] if ev and ev["author"] else r.get("author_or_series", "")),
            "nexus_status": meta.get("status", ""), "nexus_latest_version": latest,
            "updated_since_1.9.7": ("yes" if last_up >= "2026-02-13" else "no") if last_up else "",
            "evidence_summary": (ev["summary"][:300] if ev else ""),
        })
    out.sort(key=lambda x: (x["priority"], x["id"]))
    cols = list(out[0].keys())
    with open(os.path.join(D, "mods_triage.csv"), "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols, lineterminator="\n")
        w.writeheader()
        w.writerows(out)

    # ---------------------------------------------------------------- TRIAGE.md
    pr = collections.Counter(o["priority"] for o in out)
    ev_c = collections.Counter(o["evidence"] for o in out)
    act = collections.Counter((o["priority"], o["action"].split(" with ")[0].split(" (")[0]) for o in out)
    L = ["# Mod triage (generated)", "",
         "> **GENERATED** by `tools/triage_mods.py`: do not edit | **Kind:** review | **Trust:** rules applied to titles, search summaries and 26 archives read locally | **Game version:** 1.9.8", "",
         f"{len(out)} mods. Rules and evidence classes are in the header of `tools/triage_mods.py`; the per-mod table is `mods_triage.csv`. "
         "This is a repeatable sort, not a verdict: only the rows marked evidence **A** (archive read) are measured.", "",
         "## Counts", "", "| Priority | Mods | Meaning |", "|---|---|---|"]
    meaning = {"P1": "act now", "P2": "compare or check before combining", "P3": "optional or not mapped", "P4": "outside the suite's scope"}
    for k in sorted(pr):
        L.append(f"| {k} | {pr[k]} | {meaning[k]} |")
    L += ["", "| Evidence | Mods |", "|---|---|"] + [f"| {k} | {v} |" for k, v in sorted(ev_c.items())]
    L += ["", "## Actions", "", "| Priority | Action | Mods |", "|---|---|---|"]
    for (p_, a_), n in sorted(act.items()):
        L.append(f"| {p_} | {a_} | {n} |")

    L += ["", "## P1 and the archive-measured mods", "",
          "| Id | Mod | Finding |", "|---|---|---|"]
    for o in out:
        if o["evidence"] == "A archive" or o["priority"] == "P1":
            a = (arcs.get(o["id"]) or [{}])
            fa = "; ".join(f"{x.get('archive','')[:34]}: {x.get('loads_on_1.9.8','')}" + (f" | {x['problems'][:110]}" if x.get("problems") else "")
                           + (f" | collides {x['krs_collisions']}" if x.get("krs_collisions") else "") for x in a)
            L.append(f"| {o['id']} | {o['name'][:40]} | {fa} |")

    L += ["", "## Overlap with the KRS modules (P2, by module)", ""]
    for m in ("krs_perks", "krs_items", "krs_qol", "krs_bow (planned)"):
        sel = [o for o in out if m in o["krs_modules"].split(" ") or (m == "krs_bow (planned)" and "krs_bow" in o["krs_modules"])]
        sel = [o for o in out if (m.split(" ")[0] in o["krs_modules"])]
        likely = [o for o in sel if o["row_collision"].startswith(("measured", "likely"))]
        L += [f"### {m}: {len(sel)} mods ({len(likely)} with measured or likely collision)", ""]
        if likely:
            L += ["| Id | Mod | Why | Updated |", "|---|---|---|---|"]
            for o in likely:
                L.append(f"| {o['id']} | {o['name'][:46]} | {o['row_collision'][:110]} {('| ' + o['evidence_summary'][:140]) if o['evidence_summary'] else ''} | {o['last_updated']} |")
            L.append("")
        rest = [o for o in sel if o not in likely]
        L.append("Title-based only: " + (", ".join(f"{o['id']}" for o in rest) or "none") + ".")
        L.append("")

    L += ["## Mods that state a game version (from search summaries or archives)", "", "| Id | Mod | Version statement |", "|---|---|---|"]
    for o in out:
        if o["load_on_1.9.8"] != "unknown (manifest not seen)":
            L.append(f"| {o['id']} | {o['name'][:44]} | {o['load_on_1.9.8']} |")

    if nm:
        stat = collections.Counter(m["status"] for m in nm.values())
        L += ["", "## Nexus API (tools/nexus_metadata.py, run by the author)", "",
              "Status of the " + str(len(nm)) + " ids: " + ", ".join(f"{k} {v}" for k, v in sorted(stat.items())) + ".", "",
              "Not published: " + (", ".join(f"{i} {m['name'][:40]} ({m['status']})" for i, m in sorted(nm.items()) if m["status"] != "published") or "none") + ".", "",
              "Flagged adult by Nexus: " + (", ".join(f"{i} {m['name'][:28]}" for i, m in sorted(nm.items()) if m.get("adult") == "True") or "none") + ".", ""]
        up = [o for o in out if o["updated_since_1.9.7"] == "yes"]
        if nf:
            L += [f"File lists were fetched for {len(nf)} mods; {len(up)} of them have a file uploaded on or after 2026-02-13 (the 1.9.7 patch): "
                  + (", ".join(f"{o['id']}" for o in up) or "none") + ".", ""]
        else:
            L += ["File lists and versions were not fetched yet (`python tools/nexus_metadata.py --files`).", ""]

    # mods worth reading as archives next: likely or measured collision and not read yet, plus PTF-shaped gameplay in a KRS area
    todo = [o for o in out if o["evidence"] != "A archive" and o["nexus_status"] in ("", "published") and o["id"] not in excluded
            and (o["row_collision"].startswith("likely") or (o["priority"] == "P2" and "Study" in o["action"]))]
    S = ["# Archives to read next (generated)", "",
         "> **GENERATED** by `tools/triage_mods.py`: do not edit | **Kind:** review | **Trust:** triage rules plus Nexus API names and status | **Game version:** 1.9.8", "",
         f"{len(todo)} published mods whose Nexus description names the same values as a KRS row (\"likely\") or that are PTF-shaped gameplay mods in a KRS area, "
         "and whose archive has not been read. Download them the usual way (Vortex or the browser: the page link, tab Files) and put the archives in one folder, then run "
         "`python tools/analyze_mod_archives.py --src <folder>` and `python tools/triage_mods.py`. No script in this repository downloads mod files.", "",
         "| Id | Mod | KRS modules | Why | Page | Files |", "|---|---|---|---|---|---|"]
    for o in sorted(todo, key=lambda x: (not x["row_collision"].startswith("likely"), x["id"])):
        base = f"https://www.nexusmods.com/kingdomcomedeliverance/mods/{o['id']}"
        S.append(f"| {o['id']} | {o['name'][:46]} | {o['krs_modules']} | {o['row_collision'].split(':')[0]} | [page]({base}) | [files]({base}?tab=files) |")
    open(os.path.join(D, "DOWNLOAD_SHORTLIST.md"), "w", encoding="utf-8", newline="\n").write("\n".join(S) + "\n")

    L += ["", "## Still to identify or classify by hand", "",
          "Ids without a usable name: " + (", ".join(str(o["id"]) for o in out if not o["name"]) or "none") + ".", "",
          "Ids no rule classified: " + (", ".join(str(o["id"]) for o in out if o["category"] == "(unclassified)" and o["name"]) or "none") + "."]
    open(os.path.join(D, "TRIAGE.md"), "w", encoding="utf-8", newline="\n").write("\n".join(L) + "\n")
    print(dict(pr), dict(ev_c))
    print("wrote mods_triage.csv and TRIAGE.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
