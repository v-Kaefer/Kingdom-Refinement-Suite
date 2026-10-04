"""Reports of tools/audit_mods_deep.py: MOD_ANALYSIS.md (summary), MOD_PROFILES.md (one section per mod), QUARANTINE.md. Generated files."""
import collections
import datetime
import os

import paths

D = paths.MODS_REVIEW
GRADES = ["A changes the most", "B large", "C effective (few rows, strong effect)", "D small tweak",
          "E visual, audio or UI only (no gameplay change)", "E text only (no gameplay change)",
          "E non-perceptive to gameplay (no effective change found)", "X not analysed"]
GRADE_NOTE = {
    "A changes the most": "native code or an external tool, or 400+ rows, or 15+ tables, or 3000+ lines of Lua",
    "B large": "100+ rows, or 6+ tables, or 600+ lines of Lua",
    "C effective (few rows, strong effect)": "1 to 39 rows, but at least one core-gameplay row changes by 20 % or more (or 30+ rows / 150+ lines of Lua reach 'high' perceptibility)",
    "D small tweak": "some rows, config keys or script lines, none of them a large change in a core table",
    "E visual, audio or UI only (no gameplay change)": "textures, models, ReShade/ENB presets, audio, UI or graphics config (r_, e_, sys_ cvars) only; no data row or script changes. Not imperceptible: see the visual impact column",
    "E text only (no gameplay change)": "only changed or new text strings",
    "E non-perceptive to gameplay (no effective change found)": "nothing found that changes the game (empty, no-op rows, or unreadable pak)",
    "X not analysed": "nothing readable (damaged, encrypted, not a ZIP, or refused by the safety judgement)",
}
HEAD = "> **GENERATED** by `tools/audit_mods_deep.py`: do not edit | **Kind:** review | **Trust:** archives read statically (listed, extracted to a scratch folder, read, deleted); nothing was installed or run | **Game version:** 1.9.8"


def read_notes():
    p = os.path.join(D, "risk_notes.csv")
    if not os.path.exists(p):
        return {}
    import csv
    return {int(r["id"]): r["assessment"] for r in csv.DictReader(open(p, encoding="utf-8", newline=""))}


def esc(t):
    return str(t).replace("|", "/").replace("\n", " ")


def short(h, n=3):
    return "; ".join(h.split(" | ")[:n])


def write_reports(results, tri, owners, quarantined, tag="", scope="P1/P2"):
    sfx = "_" + tag.upper() if tag else ""
    today = datetime.date.today().isoformat()
    csfx = "_" + tag if tag else ""
    by_grade = collections.defaultdict(list)
    for r in results:
        by_grade[r["grade"]].append(r)
    mods = {r["id"] for r in results}
    risk = collections.Counter(r["risk"] for r in results)
    loads = collections.Counter(("NO" if r["loads_on_1_9_8"].startswith("NO") else "yes" if r["loads_on_1_9_8"].startswith("yes") else "no manifest") for r in results)
    layout = collections.Counter(r["layout"] for r in results)
    prob = collections.Counter()
    for r in results:
        tf = r["_tables"]
        nosuf = [t for t in tf if "__" not in os.path.basename(t["vpath"].split("!")[-1]) and t["base"] != "?"]
        if nosuf:
            prob["archives with table files without a suffix (they replace whole vanilla tables)"] += 1
            prob["table files without a suffix, in total"] += len(nosuf)
        out = [t for t in tf if "libs/tables" not in t["vpath"].lower().replace("\\", "/")]
        if out:
            prob["archives with patch files outside Libs/Tables (never loaded)"] += 1
            prob["patch files outside Libs/Tables, in total"] += len(out)
        if any("not a ZIP" in p for p in r["problems_text"].split(" | ")):
            prob["archives whose pak is not a ZIP (not readable by the game)"] += 1
        if any("suffix" in p and "ignored" in p for p in r["problems_text"].split(" | ")):
            prob["archives with a suffix that differs from the mod id (patch ignored)"] += 1
    L = [f"# Mod analysis: what the {scope} mods change (generated)", "", HEAD, "",
         f"Read on {today}: **{len(results)} archives, folders and loose files of {len(mods)} mods** (all {scope} mods that are in the downloads folder). "
         "Method: each archive is listed with 7-Zip (nothing extracted yet) and judged for risk; the safe ones are extracted to a scratch folder, read with Python "
         "(file names, magic bytes, XML tables compared with the vanilla `Tables.pak`, Lua and config text), and the scratch folder is deleted. "
         f"No file was executed, installed or loaded by the game; no game run was made. Per-mod detail: [`MOD_PROFILES{sfx}.md`](MOD_PROFILES{sfx}.md); tables: `mod_analysis{csfx}.csv`, `mod_tables{csfx}.csv`, `mod_overlap{csfx}.csv`, `risk_scan{csfx}.csv`.", "",
         "## Risk result", "", "| Level | Archives |", "|---|---|"]
    for k in ("HIGH", "MEDIUM", "LOW", "none"):
        L.append(f"| {k} | {risk.get(k, 0)} |")
    L += ["", f"HIGH means native code, scripts or shortcuts, dangerous Lua calls, path traversal or encrypted entries: those archives were moved to `_quarantine/` ({len(quarantined)} moved). "
          "Details and how to restore them: [`QUARANTINE.md`](QUARANTINE.md).", "",
          "## How the mods are graded", "",
          "Each mod gets a **grade** (how much it changes the game), a **perceptibility** (would a player notice) and the **depth** of the change.", "",
          "| Grade | Rule |", "|---|---|"]
    for g in GRADES:
        L.append(f"| {g} | {GRADE_NOTE[g]} |")
    L += ["", "Perceptibility: **high** = a core gameplay row (rpg_param, perk, skill, buff, weapon, item, food, ...) changes by 20 % or more, or 30+ rows, or 150+ Lua lines; "
          "**medium** = 5+ rows, 3+ config keys, 30+ Lua lines or any core row; **low** = few rows, or only assets or text; **none** = nothing.", "",
          "Depth layers: D0 content or text, D1 data tables (PTF), D2 engine config (.cfg), D3 Lua scripts, D4 native code or an external tool. "
          "\"Relative change\" is |new - old| / |old| of a changed numeric cell against the vanilla value (a new row counts as 1.0, capped at 10).", "",
          "## Result", "", "| Grade | Archives | Mods |", "|---|---|---|"]
    for g in GRADES:
        if g in by_grade:
            L.append(f"| {g} | {len(by_grade[g])} | {len({r['id'] for r in by_grade[g]})} |")
    L += ["", f"Loads on 1.9.8 by the manifest rule (docs/engine/game-versions.md): yes {loads['yes']}, NO {loads['NO']}, no manifest (legacy install) {loads['no manifest']}.", "",
          "How the mods install: " + "; ".join(f"{v} x {k}" for k, v in layout.most_common()) + ".", ""]
    if prob:
        L += ["Layout problems found (each makes the mod do nothing or something other than intended): " + "; ".join(f"{k}: {v}" for k, v in prob.most_common()) + ".", ""]
    for g in GRADES:
        rows = sorted(by_grade.get(g, []), key=lambda r: (-r["rows_changed_or_new"], r["id"]))
        if not rows:
            continue
        L += [f"## {g} ({len(rows)})", "", "| Id | Mod | Domain | Rows (new / changed) | Tables | Median rel. | Gameplay / visual | Highlights | Risk |", "|---|---|---|---|---|---|---|---|---|"]
        for r in rows:
            L.append(f"| {r['id']} | {esc(r['name'])[:48]} | {esc(r.get('domain', ''))[:46]} | {r['rows_new']} / {r['rows_changed']} | {r['tables_touched']} | "
                     f"{r['median_rel_change']} | {r['perceptibility']} / {r.get('visual_impact', '-')} | {esc(short(r['highlights'], 2) or r['areas'])[:150]} | {r['risk']} |")
        L.append("")
    ov = [(k, v) for k, v in owners.items() if len(v) > 1]
    L += ["## Overlap between the analysed mods", "",
          f"{len(ov)} table rows are changed by two or more of the {len(mods)} mods (`mod_overlap.csv`). Most contested: " +
          "; ".join(f"{b}:{'/'.join(k)[:40]} ({len(v)} mods)" for (b, k), v in sorted(ov, key=lambda x: -len(x[1]))[:8]) + ".", ""]
    pairs = collections.Counter()
    for (b, k), v in owners.items():
        if 1 < len(v) <= 8:
            ids = sorted(v)
            for i, a_ in enumerate(ids):
                for b_ in ids[i + 1:]:
                    pairs[(a_, b_)] += 1
    names = {r["id"]: r["name"] for r in results}
    if pairs:
        L += ["Pairs of mods that change the most rows in common (rows shared by 2 to 8 mods; the later one in load order wins each row):", "",
              "| Mod A | Mod B | Shared rows |", "|---|---|---|"]
        L += [f"| {a_} {esc(names[a_])[:40]} | {b_} {esc(names[b_])[:40]} | {n} |" for (a_, b_), n in pairs.most_common(15)]
        L.append("")
    kc = [r for r in results if r.get("krs_collisions")]
    L += [f"{len(kc)} archives change rows that a KRS module also sets (the later mod in load order wins the whole row): " +
          ", ".join(f"{r['id']}" for r in kc) + ".", ""]
    ext = [r for r in results if r["needs_external"] or r["requires"]]
    L += ["## Needs something outside the game files", "",
          "; ".join(f"{r['id']} ({r['requires']})" for r in ext if r["requires"]) or "none found", ""]
    open(os.path.join(D, f"MOD_ANALYSIS{sfx}.md"), "w", encoding="utf-8", newline="\n").write("\n".join(L))

    P = [f"# Mod profiles: {scope} (generated)", "", HEAD, "",
         f"One section per archive of the {scope} mods, best first by grade. What it changes, how it is installed, where the data lives, how much it changes (against the vanilla tables), "
         f"what it needs, and the risk result. See [`MOD_ANALYSIS{sfx}.md`](MOD_ANALYSIS{sfx}.md) for the grading rules.", ""]
    order = {g: i for i, g in enumerate(GRADES)}
    for r in sorted(results, key=lambda r: (order.get(r["grade"], 9), -r["rows_changed_or_new"], r["id"])):
        P += [f"## {r['id']} {esc(r['name'])} ({r['priority']}, {r['category']})", "",
              f"- **What the author says (Nexus summary):** {esc(tri.get(r['id'], {}).get('evidence_summary', '')) or '-'}",
              f"- **File:** `{r['entry']}` ({r['kind']}, {r['size_mb']} MB, `{r['sub_folder']}`), {r['extracted']}",
              f"- **Grade:** {r['grade']} | **gameplay perceptibility:** {r['perceptibility']} | **visual/audio impact:** {r.get('visual_impact', '-')} | **layers:** {r['depth']} | **domain:** {r.get('domain', '-')}",
              f"- **How it installs:** {r['layout']}; manifest id `{r['manifest_modid'] or '-'}`, supports `{r['supports'] or '-'}`, loads on 1.9.8: {r['loads_on_1_9_8']}",
              f"- **Where it changes things:** {r['areas'] or 'nothing recognised'}"]
        if r["tables_list"]:
            P.append(f"- **Tables:** {r['tables_list']} ({r['rows_new']} new rows, {r['rows_changed']} changed, {r['rows_same']} identical to vanilla"
                     f"{', ' + str(r['rows_dropped']) + ' vanilla rows dropped by a whole-table replace' if r['rows_dropped'] else ''}); median relative change {r['median_rel_change']}")
        if r["highlights"]:
            P.append("- **Largest changes:** " + esc(r["highlights"].replace(" | ", "; "))[:700])
        if r["lua_files"]:
            P.append(f"- **Lua:** {r['lua_files']} files, {r['lua_lines']} lines; API used: {r['lua_api'] or '-'}")
        if r["cfg_keys"]:
            P.append(f"- **Config:** {r['cfg_keys']} keys, e.g. {r['cfg_sample']}")
        if r["loc_new"] or r["loc_changed"]:
            P.append(f"- **Text:** {r['loc_changed']} strings changed, {r['loc_new']} new")
        if r["requires"]:
            P.append(f"- **Mentions:** {r['requires']}")
        if r.get("krs_collisions"):
            P.append(f"- **Same rows as KRS:** {r['krs_collisions']}")
        if r["problems_text"]:
            P.append(f"- **Problems:** {esc(r['problems_text'])}")
        if r.get("native_info"):
            P.append(f"- **Native file, read statically (never run):** {esc(r['native_sha'])} | {esc(r['native_info'])[:700]}")
        P.append(f"- **Risk:** {r['risk']}" + (f": {esc(r['risk_findings'])[:500]}" if r["risk_findings"] else "") + (" (quarantined)" if r["entry"] in quarantined else ""))
        P.append("")
    open(os.path.join(D, f"MOD_PROFILES{sfx}.md"), "w", encoding="utf-8", newline="\n").write("\n".join(P))

    write_quarantine()


def write_quarantine():
    """one register for every run: reads all risk_scan*.csv"""
    import csv
    import glob
    notes = read_notes()
    rows = []
    for f in sorted(glob.glob(os.path.join(D, "risk_scan*.csv"))):
        rows += list(csv.DictReader(open(f, encoding="utf-8", newline="")))
    Q = ["# Quarantine and risk register (generated)", "", HEAD, "",
         "Archives with a HIGH finding are **moved** (not deleted) to `Mods WIP folder/Installed_to_review/_quarantine/`; the move is listed in `_quarantine_manifest.csv` "
         "in that folder. To restore one, move it back to the sub-folder named in the manifest. Nothing in quarantine was run, installed or opened by anything but the reader of the tool. "
         "The register covers every run (`risk_scan*.csv`).", ""]
    qr = [x for x in rows if x["action"] == "quarantined"]
    Q += [f"## Quarantined ({len(qr)})", ""]
    if qr:
        Q += ["| Id | Mod | File | Assessment | Findings | Native file read statically |", "|---|---|---|---|---|---|"]
        Q += [f"| {x['id']} | {esc(x['name'])} | `{x['entry']}` | {esc(notes.get(int(x['id']), ''))} | {esc(x['findings'])[:400]} | {esc(x['native_sha256'])[:600]} |" for x in qr]
    else:
        Q.append("none")
    mr = [x for x in rows if x["risk"] in ("MEDIUM", "LOW") and x["action"] != "quarantined"]
    Q += ["", f"## Kept, with a note ({len(mr)})", ""]
    if mr:
        Q += ["| Id | Mod | File | Level | Assessment | Findings |", "|---|---|---|---|---|---|"]
        Q += [f"| {x['id']} | {esc(x['name'])} | `{x['entry']}` | {x['risk']} | {esc(notes.get(int(x['id']), ''))} | {esc(x['findings'])[:400]} |" for x in mr]
    else:
        Q.append("none")
    Q += ["", "## What was checked", "",
          "Archive listing: path traversal, absolute paths, alternate data streams, encrypted entries, nested archives, native code and script extensions, disguised double extensions, decompression-bomb shape. "
          "Extracted content: magic bytes of every file (MZ, ELF, shortcut, shebang), symbolic links, every ZIP-based `.pak` member list, Lua calls (os.execute, io.popen, package.loadlib, ffi, loadstring, io.open ...), "
          "command and downloader strings, URLs in scripts, long base64 blobs. A clean result means none of these patterns was found; it is not a guarantee, and no antivirus engine of this tool's own was used "
          "(see `docs/mods-review/DOWNLOADS_PLAN.md` for the Windows Security status).", ""]
    open(os.path.join(D, "QUARANTINE.md"), "w", encoding="utf-8", newline="\n").write("\n".join(Q))
