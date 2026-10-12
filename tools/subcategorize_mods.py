#!/usr/bin/env python3
"""
subcategorize_mods.py - sub-categories and a ranking inside each of them for the graded mods.

    python tools/subcategorize_mods.py

Reads only what tools/audit_mods_deep.py already wrote (docs/mods-review/mod_analysis.csv,
mod_tables.csv, mod_overlap.csv) plus nexus_metadata.csv: no archive is opened, nothing is
extracted and no network call is made.

Writes docs/mods-review/MOD_SUBCATEGORIES.md and docs/mods-review/mod_subcategories.csv:
every mod graded A to E goes into one sub-category of mods that change the same tables (PTF)
or the same kind of file, and inside each sub-category it gets an effect score, a build score
and a rank.
"""
import collections
import csv
import datetime
import math
import os
import posixpath
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paths  # noqa: E402

D = paths.MODS_REVIEW
GRADES = ["A changes the most", "B large", "C effective (few rows, strong effect)", "D small tweak",
          "E non-perceptive to gameplay (content or text only)",
          "E non-perceptive to gameplay (no effective change found)", "X not analysed"]

# ---------------------------------------------------------------- table families
# Every vanilla table that any of the mods changes, put in the system it belongs to.
FAMILY_TABLES = {
    "combat": """combat_action_attack combat_action_perfect_block combat_action_sync_attack combat_action_sync_hit
        combat_action_sync_pb_hit combat_action_guard_movement combat_action_pose_modifier combat_sync_action_hit
        combat_combo combat_combo_step combat_attack_type combat_weapon_group_to_class combat_action_fragment_id_mapping
        hit_reaction hit_reaction_type anim_fragment weapon_class rpg_movement_type morale_change""",
    "weapons": "weapon melee_weapon weapon2weapon_preset weapon_preset",
    "archery": "ammo missile_weapon",
    "armor": "armor armor_type armor2clothing_preset clothing clothing_preset clothing_raycast body_part equippable_item",
    "perks": """perk perk_buff perk_buff_override perk_rpg_param_override perk2perk_exclusivity perk_soul_ability
        soul_ability skill skill2item_category""",
    "buffs": "buff buff_class",
    "alchemy": "food potion recipe ointment_item divisible_item consumable_item",
    "economy": "shop shop_type2item inventory2item inventory_preset2item money_change gold_dayone_stash_diff quest_reward_item",
    "items": "pickable_item player_item item questible_item pickable_area_desc quest_tracked_asset",
    "npcs": "soul social_class angriness_enum",
    # which perks, skills and archetype a non-player soul gets: the tables NPC-ability mods collide on
    "npcloadout": "soul2perk soul2skill soul_archetype soul_archetype_movement",
    "crime": "reputation_change",
    "survival": "sleeping_spot_type game_mode",
    "content": """sequence topic2sequence TopicToRole dialogue_functions quest_objective random_event achievement
        mn_fragment document document_required_skill character_hair""",
}
TABLE_FAMILY = {t: f for f, ts in FAMILY_TABLES.items() for t in ts.split()}

# rpg_param is the one table every system writes into, so its changed keys are read by name instead.
KEY_FAMILY = [
    ("archery", ("aim", "bow")),
    ("economy", ("barter", "indulgence", "questmoneyreward", "repairprice", "horsewith", "itemhealthprice")),
    ("durability", ("repairkit", "itemhealth", "shoehealth", "damagetoarmorstatus", "weaponstatus", "armorstatus")),
    ("crime", ("pickpocket", "lockpicking", "picklock", "stealth", "jail")),
    ("progression", ("skillxp", "statxp", "xp", "skillcap", "statcap", "secondarystat", "nonskillbook", "reading")),
    ("survival", ("digestion", "exhaustion", "foodheal", "sleep", "herb", "cloth", "jumpcost", "sprintcost")),
    ("horses", ("horse", "dog", "houndmaster")),
    ("hunting", ("hunter",)),
    ("items", ("inventorycapacity", "strengthtoinventory")),
    ("combat", ("combat", "attack", "stam", "maxstat", "minstat", "maxdamage", "perfectblock", "skilltodefense",
                "skilltodmg", "armordefense", "averagearmor", "maxattackspeed")),
]

# The sub-category a family belongs to: broad groups, so that a group has something to rank.
FAMILY_GROUP = {
    "combat": "Combat mechanics and AI",
    "buffs": "Buffs and status effects",
    "weapons": "Weapons, armour and durability",
    "armor": "Weapons, armour and durability",
    "durability": "Weapons, armour and durability",
    "archery": "Archery: bows, arrows, aiming",
    "perks": "Perks, skills and XP",
    "progression": "Perks, skills and XP",
    "alchemy": "Alchemy, food and survival",
    "survival": "Alchemy, food and survival",
    "hunting": "Alchemy, food and survival",
    "economy": "Economy, loot and item stats",
    "items": "Economy, loot and item stats",
    "crime": "Crime, stealth and reputation",
    "horses": "Horses and animals",
    "npcs": "NPCs, quests and world content",
    "content": "NPCs, quests and world content",
    "npcloadout": "NPC perks, skills and archetypes",
    "params": "Global rpg_param tuning",
}
FAMILY_LABEL = {"npcloadout": "NPC loadout", "params": "rpg_param", "npcs": "NPCs", "armor": "armour",
                "perks": "perks and skills", "items": "item stats", "content": "quests and text"}
OVERHAUL = "Multi-system overhaul"
NATIVE = "Native code and external tools"
# Groups for the mods that change no table row: the file they do change is what they have in common.
FILE_GROUPS = {
    "lua": "Lua scripts only",
    "cfg": "Engine config (.cfg) only",
    "xml": "Non-table XML (entities, effects, audio definitions)",
    "assets": "Textures, models and other assets",
    "loc": "UI text and localisation",
    "none": "Nothing readable / no change found",
}
FILE_BASIS = {
    "lua": ("lua_lines", "line of Lua", "lines of Lua"),
    "cfg": ("cfg_keys", "engine config key", "engine config keys"),
    "assets": ("assets", "asset file", "asset files"),
    "loc": ("loc_strings", "text string", "text strings"),
    "xml": (None, "XML that is not a game table, no table row", ""),
    "none": (None, "nothing found that changes a row", ""),
}
PERC = {"high": 1.0, "medium": 0.6, "low": 0.3, "none": 0.0, "unknown": 0.0}


def read_csv(name):
    with open(os.path.join(D, name), encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def num(v, cast=int):
    try:
        return cast(v)
    except (TypeError, ValueError):
        return cast(0)


def key_family(key):
    k = key.lower()
    for fam, prefixes in KEY_FAMILY:
        if any(p in k for p in prefixes):
            return fam
    return "params"


def param_keys():
    """mod id -> rpg_param keys it changes (mod_overlap.csv holds the keys that two or more mods change)."""
    keys = collections.defaultdict(set)
    for r in read_csv("mod_overlap.csv"):
        if r["table"] == "rpg_param":
            for m in r["mod_ids"].split():
                keys[m].add(r["key"])
    return keys


def empty_facts():
    return {"fam": collections.Counter(), "files": 0, "replace": 0, "outside": 0, "mismatch": 0, "dropped": 0,
            "rows": 0, "seen": set(), "repeats": 0, "tables": set()}


def table_facts(rows, keys, modids):
    """Per archive: family weights (changed rows), how the table files are written, dropped vanilla rows."""
    out = collections.defaultdict(empty_facts)
    for r in rows:
        e = out[r["entry"]]
        path = r["file_in_mod"].replace("\\", "/")
        base = posixpath.basename(path)
        name = base[:-4] if base.lower().endswith(".xml") else base
        modid = (modids.get(r["entry"]) or "").lower()
        e["files"] += 1
        if "libs/tables/" not in path.lower():
            e["outside"] += 1
        if r["style"] == "exact" and "__" not in name:
            e["replace"] += 1
            e["dropped"] += num(r["dropped_vs_vanilla"])
        elif "__" in name and modid and name.split("__", 1)[1].lower() != modid:
            e["mismatch"] += 1
        changed = num(r["new"]) + num(r["changed"])
        if changed <= 0:
            continue
        # One archive often ships the same patch several times as alternative options (2X / 3X / 5X folders).
        # Only one of them can be installed, so an identical patch counts once.
        sig = (r["table"], r["new"], r["changed"], r["rows"], r["changed_columns"])
        if sig in e["seen"]:
            e["repeats"] += 1
            continue
        e["seen"].add(sig)
        e["rows"] += changed
        e["tables"].add(r["vanilla_table"])
        fam = TABLE_FAMILY.get(r["vanilla_table"], "content")
        if r["vanilla_table"] == "rpg_param":
            ks = keys.get(r["id"], set())
            if ks:
                for k in ks:                       # split the rows over the systems those keys belong to
                    e["fam"][key_family(k)] += changed / len(ks)
                continue
            fam = "params"
        e["fam"][fam] += changed
    return out


def spread_buffs(fam):
    """buff rows support whatever the mod's own systems are, so they are shared out over them."""
    if "buffs" not in fam or len(fam) == 1:
        return fam
    out = collections.Counter({f: n for f, n in fam.items() if f != "buffs"})
    rest = sum(out.values())
    for f in list(out):
        out[f] += fam["buffs"] * out[f] / rest
    return out


def subcategory(a, fam, layers, replaced, tables):
    """-> (sub-category, the footprint that put it there)"""
    if "D4" in layers:
        return NATIVE, "native code or an external tool"
    if fam:
        fam = spread_buffs(fam)
        total = sum(fam.values())
        groups = collections.Counter()
        for f, n in fam.items():
            groups[FAMILY_GROUP.get(f, "Global rpg_param tuning")] += n
        wide = [f for f, n in fam.items() if n >= 10]
        rank = lambda d: sorted(d.items(), key=lambda kv: (-kv[1], kv[0]))     # noqa: E731 - ties by name, so stable
        label = lambda fs: ", ".join(FAMILY_LABEL.get(f, f) for f, _ in fs)    # noqa: E731
        if replaced >= 20 or len(wide) >= 6 or (len(wide) >= 4 and tables >= 15):
            return OVERHAUL, f"{len(fam)} systems: {label(rank(fam)[:5])}"
        name, n = rank(groups)[0]
        return name, f"{n / total:.0%} in {label(rank(fam)[:3])}"
    kind = ("lua" if num(a["lua_lines"]) else "cfg" if num(a["cfg_keys"]) else
            "assets" if num(a["assets"]) else "loc" if num(a["loc_strings"]) else
            "xml" if "other xml (data)" in a["areas"] else "none")
    field, one, many = FILE_BASIS[kind]
    if field:
        n = num(a[field])
        basis = f"{n} {one if n == 1 else many}, no table row"
    else:
        basis = one
    if kind == "none" and "tables (PTF)" in a["areas"]:
        basis = "has table files, but no row differs from vanilla"
    return FILE_GROUPS[kind], basis


def effect_score(a, layers, rows, tables):
    """How much of the game it measurably changes, 0 to 100 (same scale for every mod)."""
    vol = math.log1p(rows) / math.log1p(25000)
    breadth = min(tables, 30) / 30
    intensity = min(num(a["median_rel_change"], float), 2.0) / 2
    perc = PERC.get(a["perceptibility"], 0.0)
    layer = len(layers) / 4
    script = max(min(num(a["lua_lines"]), 3000) / 3000, min(num(a["cfg_keys"]), 40) / 40,
                 1.0 if "D4" in layers else 0.0)
    s = 100 * (0.28 * vol + 0.14 * breadth + 0.18 * intensity + 0.20 * perc + 0.10 * layer + 0.10 * script)
    return round(min(s, 100.0), 1)


def build_score(a, t, variants):
    """How well the archive is made, 0 to 100: starts at 100, faults subtract, care adds."""
    s, why = 100.0, []
    # A suffix that is not the mod id is never loaded (ptf-rules.md rule 1). Counted here only when mod.manifest
    # states the id; when the deep analysis had to derive the id from the mod name it is reported as a doubt instead,
    # because an archive that bundles several sub-mods has one manifest per sub-mod and only one was compared.
    derived = "!= id" in a["problems_text"] and not a["manifest_modid"]
    if "not a ZIP" in a["problems_text"]:
        s -= 40
        why.append("a pak is not a ZIP: the game cannot read it")
    if t["outside"]:
        s -= 30
        why.append(f"{t['outside']} table patches outside Libs/Tables (never loaded)")
    if t["mismatch"]:
        s -= 30
        n = t["mismatch"]
        why.append(f"{n} table file{'' if n == 1 else 's'} whose suffix is not the mod id of its manifest "
                   f"(the game ignores {'it' if n == 1 else 'them'})")
    elif derived:
        s -= 12
        why.append("the deep analysis found a table file whose suffix is not the mod id it derived from the mod name "
                   "(no modid in the manifest): to be confirmed per sub-mod")
    if a["loads_on_1_9_8"].startswith("NO"):
        s -= 35
        why.append("the manifest does not allow 1.9.8")
    elif a["loads_on_1_9_8"].startswith("no manifest"):
        s -= 10
        why.append("no mod.manifest: legacy loose pak")
    if t["replace"]:
        share = t["replace"] / max(t["files"], 1)
        s -= 25 * share
        if t["files"] == 1:
            why.append("its only table file replaces a whole vanilla table instead of patching it: collides with "
                       "every other mod on that table")
        else:
            why.append(f"{t['replace']} of {t['files']} table files replace a whole vanilla table ({share:.0%}): "
                       "collides with every other mod on those tables")
        if t["dropped"]:
            s -= min(15, 5 * math.log10(1 + t["dropped"]))
            why.append(f"those replacements drop {t['dropped']} vanilla rows")
    if a["risk"] == "HIGH":
        s -= 25
        why.append("HIGH risk in the scan (quarantined)")
    elif a["risk"] == "MEDIUM":
        s -= 10
        why.append("MEDIUM risk in the scan")
    if t["files"] and not (t["replace"] or t["outside"] or t["mismatch"]):
        s += 5
        why.append("every table file is a correctly suffixed PTF patch")
    if num(a["loc_strings"]):
        s += 4
        why.append("ships its own text strings")
    if "docs:" in a["areas"]:
        s += 3
        why.append("ships a readme")
    if variants > 1:
        s += 3
        why.append(f"{variants} archives: optional variants")
    return round(max(0.0, min(s, 100.0)), 1), why


def collect():
    analysis = read_csv("mod_analysis.csv")
    modids = {r["entry"]: r["manifest_modid"] for r in analysis}
    tables = table_facts(read_csv("mod_tables.csv"), param_keys(), modids)
    summaries = {r["id"]: r["summary"] for r in read_csv("nexus_metadata.csv")}
    by_id = collections.defaultdict(list)
    for r in analysis:
        by_id[r["id"]].append(r)

    mods = []
    for mid, archives in by_id.items():
        # the mod's main archive: highest grade, then the one the game would load, then the one that changes most
        archives.sort(key=lambda r: (GRADES.index(r["grade"]), r["loads_on_1_9_8"].startswith("NO"),
                                     -(num(r["rows_new"]) + num(r["rows_changed"]))))
        a = archives[0]
        if a["grade"].startswith("X"):
            continue
        t = tables.get(a["entry"], empty_facts())
        layers = [p.strip()[:2] for p in a["depth"].split(";") if p.strip().startswith("D")]
        rows = t["rows"] if t["files"] else num(a["rows_new"]) + num(a["rows_changed"])
        n_tables = len(t["tables"]) if t["files"] else num(a["tables_touched"])
        group, basis = subcategory(a, t["fam"], layers, t["replace"], n_tables)
        eff = effect_score(a, layers, rows, n_tables)
        bld, why = build_score(a, t, len(archives))
        if t["repeats"]:
            why.append(f"{t['repeats']} table files are a repeat of another one in the same archive "
                       "(alternative options), counted once here")
        mods.append({
            "id": mid, "name": a["name"], "grade": a["grade"], "subcategory": group, "footprint": basis,
            "effect_measurable": "no" if group == NATIVE else "yes",
            "effect": eff, "build": bld, "overall": round(0.55 * eff + 0.45 * bld, 1),
            "rows_changed_or_new": rows, "rows_in_mod_analysis": num(a["rows_new"]) + num(a["rows_changed"]),
            "tables_touched": n_tables, "tables_in_mod_analysis": num(a["tables_touched"]),
            "median_rel_change": a["median_rel_change"], "perceptibility": a["perceptibility"], "depth": a["depth"],
            "lua_lines": num(a["lua_lines"]), "cfg_keys": num(a["cfg_keys"]), "assets": num(a["assets"]),
            "loc_strings": num(a["loc_strings"]), "loads_on_1_9_8": a["loads_on_1_9_8"], "risk": a["risk"],
            "whole_table_replacements": t["replace"], "table_files": t["files"], "dropped_vanilla_rows": t["dropped"],
            "variants": len(archives), "entry": a["entry"], "category_in_index": a["category"],
            "tables_list": a["tables_list"], "build_notes": "; ".join(why), "nexus_summary": summaries.get(mid, ""),
            "families": ", ".join(f"{f} {n:.0f}" for f, n in t["fam"].most_common(6)),
        })

    for g in GRADES:
        for sub in sorted({m["subcategory"] for m in mods if m["grade"] == g}):
            group = [m for m in mods if m["grade"] == g and m["subcategory"] == sub]
            if sub == NATIVE:                               # no measurable effect: rank by how safe and well built
                group.sort(key=lambda m: (-m["build"], -m["effect"]))
                score = lambda m: (m["build"], m["effect"])  # noqa: E731
            else:
                group.sort(key=lambda m: -m["overall"])
                score = lambda m: m["overall"]               # noqa: E731
            rank = 1
            for i, m in enumerate(group):                   # equal scores share a rank
                if i and score(m) != score(group[i - 1]):
                    rank = i + 1
                m["rank"], m["of"] = rank, len(group)
    return mods


COLS = ["id", "name", "grade", "subcategory", "rank", "of", "overall", "effect", "build", "effect_measurable",
        "footprint", "families", "rows_changed_or_new", "rows_in_mod_analysis", "tables_touched", "tables_in_mod_analysis", "median_rel_change", "perceptibility",
        "depth", "lua_lines", "cfg_keys", "assets", "loc_strings", "loads_on_1_9_8", "risk",
        "whole_table_replacements", "table_files", "dropped_vanilla_rows", "variants", "entry",
        "category_in_index", "tables_list", "build_notes", "nexus_summary"]


def write_csv(mods):
    p = os.path.join(D, "mod_subcategories.csv")
    with open(p, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=COLS, extrasaction="ignore")
        w.writeheader()
        for m in sorted(mods, key=lambda m: (GRADES.index(m["grade"]), m["subcategory"], m["rank"])):
            w.writerow(m)
    return p


def esc(t):
    return str(t).replace("|", "/").replace("\n", " ")


def loads_short(v):
    return "no" if v.startswith("NO") else "legacy" if v.startswith("no manifest") else "yes"


def changes(m):
    if m["tables_touched"]:
        rows, tables = m["rows_changed_or_new"], m["tables_touched"]
        return (f"{rows} row{'' if rows == 1 else 's'} in {tables} table{'' if tables == 1 else 's'} - "
                f"{esc(m['footprint'])}")
    return esc(m["footprint"])


def md_table(group):
    out = ["| # | Id | Mod | Area in the index | Overall | Effect | Build | 1.9.8 | What it changes | Build notes |",
           "|---|---|---|---|---|---|---|---|---|---|"]
    for m in group:
        eff = "n/a" if m["effect_measurable"] == "no" else f"{m['effect']:.0f}"
        out.append(f"| {m['rank']} | {m['id']} | {esc(m['name'])[:46]} | {esc(m['category_in_index'])} | "
                   f"{m['overall']:.0f} | {eff} | {m['build']:.0f} | {loads_short(m['loads_on_1_9_8'])} | "
                   f"{changes(m)} | {esc(m['build_notes']) or 'nothing against it'} |")
    return out


def id_list(mods, pick):
    return ", ".join(sorted((m["id"] for m in mods if pick(m)), key=int)) or "none"


def write_md(mods):
    today = datetime.date.today().isoformat()
    recounted = id_list(mods, lambda m: m["rows_changed_or_new"] != m["rows_in_mod_analysis"]
                        or m["tables_touched"] != m["tables_in_mod_analysis"])
    doubt = id_list(mods, lambda m: "derived from the mod name" in m["build_notes"])
    fault = id_list(mods, lambda m: "of its manifest" in m["build_notes"])
    out = ["# Sub-categories of the graded mods, and the ranking inside each one (generated)", "",
           "> **GENERATED** by `tools/subcategorize_mods.py`: do not edit | **Kind:** review | **Trust:** derived from "
           "the read-only analysis in `docs/mods-review/mod_analysis.csv` (no archive was opened for this file) | "
           "**Game version:** 1.9.8", "",
           f"Read on {today}: the **{len(mods)} mods graded A to E** in [`MOD_ANALYSIS.md`](MOD_ANALYSIS.md). Each one is "
           "put in a sub-category of mods that change the same tables (PTF) or the same kind of file, and inside that "
           "sub-category it is ranked. Per-mod detail: [`MOD_PROFILES.md`](MOD_PROFILES.md); the table behind this file: "
           "`mod_subcategories.csv`.", "",
           "## How a mod lands in a sub-category", "",
           "The sub-category is **the files a mod writes into, not what its page calls it**: two mods in the same "
           "sub-category patch the same tables, so they also collide with each other and can be compared row for row. "
           "The *Area in the index* column keeps the thematic label from `mods_index.csv` beside it, and the two "
           "sometimes disagree (a horse mod whose rows are all perks and buffs lands with the perk mods).", "",
           "A mod is one row here; when it ships several archives (options or add-ons), the one measured is of the "
           "highest grade, then the one the game would load on 1.9.8, then the one that changes the most; the "
           "`variants` count in the CSV says how many there are.", "",
           "1. **Native code or an external tool** (depth D4) goes in its own sub-category: what it does cannot be read "
           "from the files.",
           "2. Otherwise, every changed or new table row is counted towards the system its table belongs to "
           "(`weapon` -> weapons, `shop_type2item` -> economy, `soul2perk` -> NPC loadout, ...). `rpg_param` is the one "
           "table every system writes into, so its rows are split over the systems its changed keys belong to "
           "(`Aim*`/`Bow*` -> archery, `*XP*` -> progression, `Pickpocketing*` -> crime, ...). `buff` rows support "
           "whatever else the mod changes, so they are shared out over its other systems.",
           "3. A mod is a **multi-system overhaul** when it replaces 20 or more whole vanilla tables, or has 10 or more "
           "rows in six or more systems, or in four or more systems while touching 15 or more tables. Otherwise it goes "
           "to the sub-category of the system that holds most of its rows.",
           "4. A mod that changes **no table row** is grouped by the file it does change: Lua, engine config, non-table "
           "XML, assets, or text.", "",
           "## How the ranking is computed", "",
           "Two scores, both 0 to 100, on the same scale for every mod, so they also compare across sub-categories.", "",
           "Rows and tables are counted **once per distinct patch and once per vanilla table**: when one archive ships "
           "the same table three times as 2X, 3X and 5X option folders, only one of them can be installed, so it "
           "counts once. `MOD_ANALYSIS.md` adds the files up instead and counts table *files*, which is why its "
           f"numbers are higher for {recounted} (2294: 2985 rows in 55 files against 1300 rows in 10 tables). Both "
           "counts are in `mod_subcategories.csv`.", "",
           "**Effect** - how much of the game it measurably changes: 28 % volume of changed rows (log scale), "
           "14 % how many tables, 18 % median relative change of a changed cell, 20 % perceptibility from "
           "`MOD_ANALYSIS.md`, 10 % how many depth layers (D0 to D4), 10 % size of its Lua or config change.", "",
           "**Build** - how well the archive is made. Starts at 100, then: -40 a pak that is not a ZIP, -35 a manifest "
           "that does not allow 1.9.8, -30 table patches outside `Libs/Tables` (never loaded), -30 a file suffix that "
           "is not the mod id its own manifest states (the game ignores the file), -12 the same when the deep analysis "
           "had to derive the id from the mod name, up to -25 for replacing whole vanilla tables instead of writing PTF "
           "patches (scaled by the share of its table files), up to -15 for vanilla rows those replacements drop, -25 "
           "HIGH risk, -10 MEDIUM risk, -10 no manifest; +5 every table file a correctly suffixed patch, +4 own text "
           "strings, +3 a readme, +3 optional variants.", "",
           "The two weights for the same fault are deliberate: the suffix rule (`../engine/ptf-rules.md` rule 1) is "
           "measured, but an archive that bundles several sub-mods has one `mod.manifest` per sub-mod and the deep "
           "analysis compared every file against one derived id, so there the finding is a doubt to confirm per "
           f"sub-mod, not a fault ({doubt}). Where the manifest states the id, it is a fault ({fault}).", "",
           "**Overall** = 0.55 x effect + 0.45 x build, and that is the rank. In *Native code and external tools* there "
           "is nothing to measure, so the rank there is build first.", "",
           "### What these numbers do not say", "",
           "- No mod was installed or run, and no game test was made: this is what the files say, not how the mod plays.",
           "- A high effect score is not an endorsement: it means the mod changes a lot, not that the change is good or "
           "balanced.",
           "- Non-table XML (entities, particles, audio definitions), native code and assets cannot be compared with "
           "vanilla by this method, so mods made of those get a low effect score even when they work perfectly. In their "
           "sub-categories the ranking is about how well the archive is made.",
           "- Nexus endorsements, versions and update dates are not in the data (`mods_triage.csv` has them for only a "
           "few mods), so popularity and how recently a mod was updated are not part of the score.", ""]

    counts = collections.Counter(m["grade"] for m in mods)
    out += ["## Sub-categories per grade", "", "| Grade | Mods | Sub-categories |", "|---|---|---|"]
    for g in GRADES:
        if not counts.get(g):
            continue
        subs = collections.Counter(m["subcategory"] for m in mods if m["grade"] == g)
        out.append(f"| {esc(g)} | {counts[g]} | " + "; ".join(f"{s} ({n})" for s, n in subs.most_common()) + " |")
    out.append("")

    for g in GRADES:
        group_all = [m for m in mods if m["grade"] == g]
        if not group_all:
            continue
        out += [f"## {g} ({len(group_all)} mods)", ""]
        subs = collections.Counter(m["subcategory"] for m in group_all)
        for sub, n in sorted(subs.items(), key=lambda kv: (-kv[1], kv[0])):
            group = sorted([m for m in group_all if m["subcategory"] == sub], key=lambda m: m["rank"])
            out += [f"### {g[0]} - {sub} ({n})", ""]
            if n == 1:
                m = group[0]
                eff = "not measurable" if m["effect_measurable"] == "no" else f"{m['effect']:.0f}"
                out += [f"Only one mod of this grade changes this: **{m['id']} {esc(m['name'])}** "
                        f"({esc(m['category_in_index'])}; effect {eff}, build {m['build']:.0f}; {changes(m)}). "
                        "Nothing to rank it against in this grade; the cross-grade table at the end of this file says "
                        "which other grades hold the same sub-category."
                        + (f" Notes: {esc(m['build_notes'])}." if m["build_notes"] else ""), ""]
                continue
            out += md_table(group) + [""]
            best = group[0]
            eff = max(group, key=lambda m: m["effect"])
            bld = max(group, key=lambda m: m["build"])
            flat = len({m["effect"] for m in group}) == 1
            if sub == FILE_GROUPS["none"]:
                line = ("**Nothing to pick:** no mod here was found to change a single game row, so there is nothing to "
                        "rank. Read their own pages before keeping any of them.")
            elif flat and eff["effect"] <= 10:               # assets, text, non-table XML: nothing to measure
                tied = [m for m in group if m["rank"] == 1]
                line = ("**No pick on effect:** this method cannot measure what these change, so the order is how well "
                        "the archive is made only. Best made: "
                        + ", ".join(f"{m['id']} {esc(m['name'])}" for m in tied)
                        + f" (build {tied[0]['build']:.0f}).")
            else:
                line = f"**Pick:** {best['id']} {esc(best['name'])}."
                if flat:
                    line += " Every mod here has the same effect score, so the order is the build score."
                if eff["id"] != best["id"] and not flat:
                    line += f" Changes the most: {eff['id']} {esc(eff['name'])} (effect {eff['effect']:.0f})."
                if bld["id"] != best["id"]:
                    line += f" Best made: {bld['id']} {esc(bld['name'])} (build {bld['build']:.0f})."
            broken = [m for m in group if loads_short(m["loads_on_1_9_8"]) == "no"]
            if broken:
                line += " Does not load on 1.9.8: " + ", ".join(f"{m['id']}" for m in broken) + "."
            out += [line, ""]

    out += ["## The same sub-categories across the grades", "",
            "Which grades a sub-category appears in, best-ranked mod of each grade first.", "",
            "| Sub-category | Mods | By grade | Top of each grade |", "|---|---|---|---|"]
    for sub in sorted({m["subcategory"] for m in mods}):
        group = [m for m in mods if m["subcategory"] == sub]
        per = collections.Counter(m["grade"][0] for m in group)
        tops = [sorted([m for m in group if m["grade"] == g], key=lambda m: m["rank"])[0]
                for g in GRADES if any(m["grade"] == g for m in group)]
        out.append(f"| {sub} | {len(group)} | " + " ".join(f"{k}x{v}" for k, v in sorted(per.items())) + " | "
                   + "; ".join(f"{m['grade'][0]}: {m['id']} {esc(m['name'])[:34]}" for m in tops) + " |")
    out.append("")

    p = os.path.join(D, "MOD_SUBCATEGORIES.md")
    with open(p, "w", encoding="utf-8") as f:
        f.write("\n".join(out))
    return p


def main():
    mods = collect()
    c = write_csv(mods)
    m = write_md(mods)
    subs = {(x["grade"], x["subcategory"]) for x in mods}
    print(f"{len(mods)} mods graded A to E, {len({x['subcategory'] for x in mods})} sub-categories, "
          f"{len(subs)} grade/sub-category groups")
    for p in (m, c):
        print("wrote", os.path.relpath(p, paths.ROOT).replace("\\", "/"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
