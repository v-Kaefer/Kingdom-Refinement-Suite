#!/usr/bin/env python3
"""
build_krs_perks.py - merge the Perkaholic content into modules/krs_perks, with the author's
balance corrections applied.

    python tools/build_krs_perks.py            (writes the tables and the English text)
    python tools/build_krs_perks.py --dry-run  (prints what would change, writes nothing)

Source: the workbench copy of Perkaholic 1009 (.rar), the only instance that loads on 1.9.8 and
patches correctly. Every row is rebuilt with the complete column set of the vanilla table
(ptf-rules.md rule 5: a column left out is blanked), and every file gets the `__krs_perks`
suffix (rule 1).

The CORRECTIONS table below is the whole balance policy, in one place: what the mod shipped, what
this module ships instead, and why. Anything with include=False stays visible here but is not
written, so a decision can be reversed by flipping one flag.
"""
import argparse
import collections
import os
import re
import shutil
import sys
import xml.etree.ElementTree as ET

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paths  # noqa: E402
import vanilla  # noqa: E402

WORKBENCH = r"E:\Kingdom-Refinement-Suite\Mods WIP folder\Perks\perkaholic-riposte-workbench"
SRC = os.path.join("extracted", "1009_perkaholic-ptf_rar", "_pak", "Libs", "Tables", "rpg")
LOC_SRC = os.path.join("extracted", "1009_perkaholic-ptf_rar", "Perkaholic", "Localization")
MODULE = os.path.join(paths.MODULES, "krs_perks")
SUFFIX = "krs_perks"

HIGHBORN = "f19f542a-979a-4627-8d1c-9038f7dfc7be"
LOWBORN = "84c272a9-d81f-4e7b-bee9-0142bdb7a116"
LIKE_A_FEATHER = "010b08c7-5346-402c-a7cb-a084d624b62e"    # vanilla perk the mod renamed
FEATHER_II = "010b08c8-5346-402c-a7cb-a084d624b62e"
FEATHER_III = "010b08c9-5346-402c-a7cb-a084d624b62e"
TOWNSMAN = "010b0811-5346-402c-a7cb-a084d624b62e"
KNOCK_II = "010b0812-5346-402c-a7cb-a084d624b62e"
KNOCK_III = "010b0813-5346-402c-a7cb-a084d624b62e"
YOKEL = "010b0810-5346-402c-a7cb-a084d624b62e"

# ---------------------------------------------------------------- balance policy
# key -> (include, what the author decided, the value to ship)
BUFF_RULES = {
    "perk_heavy_swing":      (True,  "o +20% do Perkaholic é forte demais; +7% confirmado",
                              "wat*1.07,wac*1.1"),
    "perk_like_a_feather":   (False, "degrau I fica o do jogo: fdm*0.7 = 30% menos dano de "
                              "queda, o número final que o autor fixou. Não enviar a linha", None),
    "perk_like_a_feather_2": (True,  "segundo degrau (o mod trazia 0.5)", "fdm*0.60"),
    "perk_like_a_feather_3": (True,  "terceiro degrau (o mod trazia 0.25)", "fdm*0.45"),
    "perk_reading_Cushion":  (False, "revertido ao valor do jogo: não enviar a linha", None),
    "perk_art_admirer_reward": (False, "NÃO CONFIRMADO: o mod dobra o carisma (cha+1 -> cha+2); "
                                "fora até você decidir", None),
    "perk_against_all_odds": (False, "NÃO CONFIRMADO: só ícone e ordem de interface; fora até "
                              "você decidir", None),
}
# perks of the game whose row the mod rewrites: none is shipped unless listed here
PERK_ROW_RULES = {
    LIKE_A_FEATHER: (False, "revertido: o jogo mantém 'Like a feather', nível 4"),
}
# new perks that need a change against what the mod shipped
PERK_FIXES = {
    FEATHER_II:  {"perk_name": "Like a Feather II"},
    FEATHER_III: {"perk_name": "Like a Feather III"},
    KNOCK_II:    {"perk_name": "Knock Knock II"},
    KNOCK_III:   {"perk_name": "Knock Knock III"},
    TOWNSMAN:    {"parent_id": HIGHBORN},
    YOKEL:       {"parent_id": LOWBORN},
}
# display text to replace in every language (the mod's own keys)
# A name is one string for every language (that is how the game ships proper nouns too).
TEXT_FIXES = {
    "perk_featherweight_1_name": None,                      # tier I reverts to the game's text
    "perk_featherweight_1_desc": None,
    "perk_featherweight_2_name": "Like a Feather II",
    "perk_featherweight_3_name": "Like a Feather III",
    "perk_film_grip_name": "Knock Knock I",                 # the game's "Firm hand", renamed
    "perk_like_a_feather_name": "Like a Feather I",         # the game shows "Featherweight"
    "perk_firm_grip_2_name": "Knock Knock II",
    "perk_firm_grip_3_name": "Knock Knock III",
}

# A description must not be flattened to English, so only the wrong number is replaced and every
# translation is left alone. key -> (as the mod wrote it, what the buff really does).
# The mod's Like a Feather text claims the opposite of its own formula: fdm*0.60 is 40% less fall
# damage, not 50%, and fdm*0.45 is 55%, not 75%.
# Keys inherited from mod 1765 carried its author's "ex" namespace. They are ours now, so they
# carry ours. Renaming a key means renaming it in the language files and in the perk rows that
# point at it, which KEY_RENAMES does in one pass.
KEY_RENAMES = {
    "perk_ex_riposte_name":    "perk_krs_riposte_name",
    "perk_ex_riposte_desc":    "perk_krs_riposte_desc",
    "perk_ex_ripo_text_sword": "perk_krs_ripo_text_sword",
    "perk_ex_ripo_text_desc":  "perk_krs_ripo_text_desc",
}

NL = chr(10)
ROW = NL.join(["<Row>", "<Cell>{k}</Cell>", "<Cell>{v}</Cell>", "<Cell>{v}</Cell>",
               "</Row>"])

TEXT_NUMBER_FIXES = {
    "perk_featherweight_2_desc": ("50", "40"),
    "perk_featherweight_3_desc": ("75", "55"),
}


def read_rows(folder, name):
    raw = open(os.path.join(folder, name), encoding="utf-8").read()
    t = ET.fromstring(re.sub(r"^\s*<\?xml[^>]*\?>", "", raw).strip()).find("table")
    return [dict(r.attrib) for r in t.findall("./rows/row")]


def existing_rows(path, table):
    """Rows already in the module's own patch, so the Riposte work is kept."""
    if not os.path.exists(path):
        return []
    return read_rows(os.path.dirname(path), os.path.basename(path))


def build(args):
    src = os.path.join(args.workbench, SRC)
    out_dir = os.path.join(MODULE, "Data", "Libs", "Tables", "rpg")
    report = collections.OrderedDict()

    van = {}
    for t in ("perk", "buff", "perk_buff", "perk_buff_override", "perk2perk_exclusivity", "skill"):
        van[t] = vanilla.load(f"rpg/{t}", game=args.game)

    # ---------------------------------------------------------------- perk
    vcols, vrows = van["perk"]
    van_perk = {r["perk_id"]: r for r in vrows}
    keep = existing_rows(os.path.join(out_dir, f"perk__{SUFFIX}.xml"), "perk")
    # a row written by an earlier build is kept as it is, but a later decision in PERK_FIXES still
    # has to reach it - otherwise a rename only ever applies to rows written for the first time
    for r in keep:
        r.update(PERK_FIXES.get(r["perk_id"], {}))
    kept_ids = {r["perk_id"] for r in keep}
    perk_rows, skipped = list(keep), []
    for r in read_rows(src, "perk__perkaholic.xml"):
        pid = r["perk_id"]
        if pid in kept_ids:
            continue
        if pid in van_perk:
            include, why = PERK_ROW_RULES.get(pid, (False, "linha do jogo alterada pelo mod: "
                                                          "fora até ser confirmada"))
            if not include:
                skipped.append((r.get("perk_name", pid), why))
                continue
        fixed = dict(r)
        fixed.update(PERK_FIXES.get(pid, {}))
        base = van_perk.get(pid, {})
        perk_rows.append(vanilla.complete_row(vcols, base, **{k: v for k, v in fixed.items()
                                                              if k in dict(vcols)}))
    report["perk"] = (len(perk_rows), skipped)

    # ---------------------------------------------------------------- buff
    vcols_b, vrows_b = van["buff"]
    van_buff = {r["buff_id"]: r for r in vrows_b}
    buff_rows, buff_skipped, buff_changed = [], [], []
    for r in read_rows(src, "buff__perkaholic.xml"):
        name = r.get("buff_name", "")
        if r["buff_id"] in van_buff:                       # a buff of the game the mod rewrites
            include, why, value = BUFF_RULES.get(name, (False, "alteração não confirmada", None))
            if not include:
                buff_skipped.append((name, why))
                continue
            row = dict(r)
            if value is not None:
                row["params"] = value
                buff_changed.append((name, van_buff[r["buff_id"]].get("params", ""), value, why))
            buff_rows.append(vanilla.complete_row(vcols_b, van_buff[r["buff_id"]],
                                                  **{k: v for k, v in row.items()
                                                     if k in dict(vcols_b)}))
        else:
            row = dict(r)
            rule = BUFF_RULES.get(name)
            if rule and rule[0] and rule[2] is not None:
                buff_changed.append((name, r.get("params", ""), rule[2], rule[1]))
                row["params"] = rule[2]
            buff_rows.append(vanilla.complete_row(vcols_b, {}, **{k: v for k, v in row.items()
                                                                  if k in dict(vcols_b)}))
    report["buff"] = (len(buff_rows), buff_skipped)

    # ---------------------------------------------------------------- the plain link tables
    simple = {}
    for table, fname in (("perk_buff", "perk_buff__perkaholic.xml"),
                         ("perk_buff_override", "perk_buff_override__perkaholic.xml"),
                         ("perk2perk_exclusivity", "perk2perk_exclusivity__perkaholic.xml"),
                         ("skill", "skill__perkaholic.xml")):
        cols, rws = van[table]
        index = {}
        key = [c for c, _ in cols]
        for r in rws:
            index[tuple(r.get(k, "") for k in key[:2])] = r
        rows_out, noop = [], []
        for r in read_rows(src, fname):
            base = index.get(tuple(r.get(k, "") for k in key[:2]), {})
            row = vanilla.complete_row(cols, base, **{k: v for k, v in r.items()
                                                      if k in dict(cols)})
            # rule 7: a row that equals the game's own changes nothing, and only widens the
            # surface this module shares with other mods
            if base and all((base.get(c, "") or "") == (row.get(c, "") or "") for c, _ in cols):
                noop.append(tuple(row.get(k, "") for k in key[:2]))
                continue
            rows_out.append(row)
        simple[table] = rows_out
        report[table] = (len(rows_out), [(f"{a}/{b}", "idêntica ao jogo: não enviada")
                                         for a, b in noop])

    if args.dry_run:
        return report, buff_changed, skipped, buff_skipped

    os.makedirs(out_dir, exist_ok=True)
    files = {"perk": (vcols, perk_rows), "buff": (vcols_b, buff_rows)}
    for t, rws in simple.items():
        files[t] = (van[t][0], rws)
    for table, (cols, rws) in files.items():
        p = os.path.join(out_dir, f"{table}__{SUFFIX}.xml")
        with open(p, "w", encoding="ascii", errors="xmlcharrefreplace") as f:
            f.write(vanilla.patch_xml(f"{table}__{SUFFIX}", cols, rws))
    merge_text(args)
    return report, buff_changed, skipped, buff_skipped


def merge_text(args):
    """Add the mod's own strings to every language file the module already has."""
    import zipfile
    loc_src = os.path.join(args.workbench, LOC_SRC)
    for pak in sorted(os.listdir(loc_src)):
        lang = pak.replace("_xml.pak", "")
        dest_dir = os.path.join(MODULE, "Localization", lang)
        if not os.path.isdir(dest_dir):
            continue
        dest = os.path.join(dest_dir, f"text__{SUFFIX}.xml")
        have = open(dest, encoding="utf-8").read() if os.path.exists(dest) else "<Table>\n</Table>"
        keys = set(re.findall(r"<Cell>([^<]*)</Cell>", have)[::3])
        add = []
        with zipfile.ZipFile(os.path.join(loc_src, pak)) as z:
            for n in z.namelist():
                if not n.lower().endswith(".xml"):
                    continue
                text = z.read(n).decode("utf-8", "replace")
                for m in re.finditer(r"<Row>\s*<Cell>([^<]*)</Cell>\s*<Cell>([^<]*)</Cell>\s*"
                                     r"<Cell>([^<]*)</Cell>\s*</Row>", text, re.S):
                    k, a, b = (x.strip() for x in m.groups())
                    if k in TEXT_FIXES:
                        new = TEXT_FIXES[k]
                        if new is None:
                            continue
                        a = b = new
                    if k in keys:
                        continue
                    add.append(f"<Row>\n<Cell>{k}</Cell>\n<Cell>{a}</Cell>\n<Cell>{b}</Cell>\n</Row>")
        if add:
            with open(dest, "w", encoding="utf-8") as f:
                f.write(have.rstrip().removesuffix("</Table>").rstrip() + "\n"
                        + "\n".join(add) + "\n</Table>\n")
    out = fix_text()
    out.update(rename_keys())
    return out


def rename_keys():
    """Apply KEY_RENAMES to the module's language files and to the perk rows that reference them."""
    changed = collections.Counter()
    base = os.path.join(MODULE, "Localization")
    for lang in sorted(os.listdir(base)):
        dest = os.path.join(base, lang, f"text__{SUFFIX}.xml")
        if not os.path.exists(dest):
            continue
        text = before = open(dest, encoding="utf-8").read()
        for old_k, new_k in KEY_RENAMES.items():
            text = text.replace(f"<Cell>{old_k}</Cell>", f"<Cell>{new_k}</Cell>")
        if text != before:
            open(dest, "w", encoding="utf-8").write(text)
            changed["localização:" + lang] += 1
    table = os.path.join(MODULE, "Data", "Libs", "Tables", "rpg", f"perk__{SUFFIX}.xml")
    if os.path.exists(table):
        text = before = open(table, encoding="utf-8").read()
        for old_k, new_k in KEY_RENAMES.items():
            text = text.replace(f'"{old_k}"', f'"{new_k}"')
        if text != before:
            open(table, "w", encoding="utf-8").write(text)
            changed["perk__krs_perks.xml"] += 1
    return changed


def fix_text():
    """Apply TEXT_FIXES and TEXT_NUMBER_FIXES to the rows already in the module's language files.

    merge_text only adds keys that are not there yet, so a decision taken after the first build
    would never reach the files without this pass.
    """
    changed = collections.Counter()
    base = os.path.join(MODULE, "Localization")
    for lang in sorted(os.listdir(base)):
        dest = os.path.join(base, lang, f"text__{SUFFIX}.xml")
        if not os.path.exists(dest):
            continue
        text = before = open(dest, encoding="utf-8").read()
        for key, new in TEXT_FIXES.items():
            if new is None:
                continue
            text = re.sub(r"(<Cell>" + re.escape(key) + r"</Cell>\s*)<Cell>.*?</Cell>\s*<Cell>.*?</Cell>",
                          lambda m: f"{m.group(1)}<Cell>{new}</Cell><Cell>{new}</Cell>",
                          text, flags=re.S)
        for key, (wrong, right) in TEXT_NUMBER_FIXES.items():
            def swap(m, wrong=wrong, right=right):
                return m.group(1) + m.group(2).replace(wrong, right)
            text = re.sub(r"(<Cell>" + re.escape(key) + r"</Cell>\s*)((?:<Cell>.*?</Cell>\s*){1,2})",
                          swap, text, flags=re.S)
        # a name we decide to override may not be among the mod's own keys at all
        add = [ROW.format(k=k, v=v) for k, v in TEXT_FIXES.items()
               if v is not None and f"<Cell>{k}</Cell>" not in text]
        if add:
            body = text.rstrip().removesuffix("</Table>").rstrip()
            text = NL.join([body] + add + ["</Table>", ""])
        if text != before:
            open(dest, "w", encoding="utf-8").write(text)
            changed[lang] += 1
    return changed


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--workbench", default=WORKBENCH)
    ap.add_argument("--game", default=vanilla.DEFAULT_GAME)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    report, changed, perk_skipped, buff_skipped = build(args)

    print("linhas escritas por tabela:")
    for t, (n, _) in report.items():
        print(f"   {t:24s} {n}")
    print("\nvalores de balanceamento aplicados:")
    for name, before, after, why in changed:
        print(f"   {name:26s} {before or '(novo)':18s} -> {after:18s}  {why}")
    print("\nlinhas do jogo NÃO enviadas (ficam como o jogo tem):")
    for name, why in perk_skipped + buff_skipped:
        print(f"   {name:26s} {why}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
