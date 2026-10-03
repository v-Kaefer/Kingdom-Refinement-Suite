#!/usr/bin/env python3
"""
seed_modules.py - one-off migration: turn the legacy mod files of the repo into the module source trees under modules/.

    python tools/seed_modules.py [--main "E:/Kingdom-Refinement-Suite"] [--game "<KCD folder>"]

What it does (everything it decides is written down in modules/<id>/CHANGES.md by hand afterwards):
  * every patch row is made COMPLETE (all columns of the vanilla table; a partial row blanks the others in game)
  * rows that equal vanilla are dropped (they change nothing, but a later mod's complete row replaces an earlier one,
    so a no-op row could silently undo another mod's change)
  * patch files are named `<table>__<modid>.xml` (the engine only applies a patch whose suffix equals the mod id)
  * localization goes to modules/<id>/Localization/<Language>/text__<modid>.xml

Sources: working tree of the main checkout (KRS-Items, KingdomRefinementSuite) and branch `develop` (QoL files; named `dev` before 3 Oct 2026).
Re-running overwrites the generated files; nothing outside modules/ is touched.
"""
import argparse
import os
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
import zipfile
from xml.sax.saxutils import escape

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import vanilla  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KEYS = {
    "rpg/rpg_param": ["rpg_param_key"],
    "rpg/sleeping_spot_type": ["sleeping_spot_type_id"],
    "item/document": ["item_id"],
    "item/food": ["item_id"],
    "rpg/perk": ["perk_id"],
    "rpg/perk_rpg_param_override": ["perk_id", "rpg_param_key"],
    "rpg/skill2item_category": ["item_category", "skill_id"],
}

MANIFEST = """<?xml version="1.0" encoding="utf-8"?>
<kcd_mod>
  <info>
    <name>{name}</name>
    <description>{description}</description>
    <author>Kaleb</author>
    <version>{version}</version>
    <created_on>{created}</created_on>
    <modid>{modid}</modid>
    <modifies_level>false</modifies_level>
  </info>
  <supports>
    <kcd_version>1.9.6</kcd_version>
  </supports>
</kcd_mod>
"""

LANGUAGES = ["Chineses", "Czech", "English", "French", "German", "Italian", "Japanese", "Korean", "Polish", "Portuguese",
             "Russian", "Spanish", "Turkish", "Ukrainian"]          # file names of the game's Localization/<Language>_xml.pak


def read_text(path):
    return open(path, encoding="utf-8", errors="replace").read()


def git_show(ref_path):
    return subprocess.run(["git", "show", ref_path], cwd=ROOT, capture_output=True, check=True).stdout.decode("utf-8", "replace")


def parse_rows(text):
    t = ET.fromstring(re.sub(r"^\s*<\?xml[^>]*\?>", "", text.lstrip("\ufeff"))).find("table")
    return [dict(r.attrib) for r in t.findall("./rows/row")]


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


def build_patch(game, module, table, legacy_rows, comments=None, note=None):
    """complete the legacy rows against vanilla, drop no-ops, write modules/<module>/Data/Libs/Tables/<table>__<module>.xml."""
    cols, vrows = vanilla.load(table, game)
    keycols = KEYS[table]
    vindex = {tuple(r.get(k, "") for k in keycols): r for r in vrows}
    rows, kept_comments, dropped = [], {}, 0
    for i, lr in enumerate(legacy_rows):
        key = tuple(lr.get(k, "") for k in keycols)
        base = vindex.get(key, {})
        row = {c: lr.get(c, base.get(c, "")) for c, _ in cols}
        if base and all(row[c] == base.get(c, "") or _same_num(row[c], base.get(c, "")) for c, _ in cols):
            dropped += 1
            continue
        if comments and i in comments:
            kept_comments[len(rows)] = comments[i]
        rows.append(row)
    out = os.path.join(ROOT, "modules", module, "Data", "Libs", "Tables", table.split("/")[0], f"{table.split('/')[1]}__{module}.xml")
    write(out, vanilla.patch_xml(table.split("/")[1], cols, rows, kept_comments))
    print(f"{module}: {table}: {len(rows)} row(s) written, {dropped} row(s) equal to vanilla dropped")
    return rows


def _same_num(a, b):
    try:
        return float(a) == float(b)
    except ValueError:
        return False


def text_xml(rows):
    out = ["<Table>"]
    for key, text, shown in rows:
        out.append(f"<Row><Cell>{escape(key)}</Cell><Cell>{escape(text)}</Cell><Cell>{escape(shown)}</Cell></Row>")
    out.append("</Table>")
    return "\n".join(out) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--main", default=r"E:\Kingdom-Refinement-Suite")
    ap.add_argument("--game", default=vanilla.DEFAULT_GAME)
    a = ap.parse_args()
    items = os.path.join(a.main, "KRS-Items", "Data", "Tables")

    # ---------------------------------------------------------------- krs_items
    m = "krs_items"
    write(os.path.join(ROOT, "modules", m, "mod.manifest"), MANIFEST.format(
        name="KRS Items", modid=m, version="2.0.0", created="04/06/2025",
        description="Kingdom Refinement Suite - items: slower book reading, hunger and fatigue that matter, better beds."))
    build_patch(a.game, m, "rpg/rpg_param", parse_rows(read_text(os.path.join(items, "rpg", "rpg_param__KRS-items.xml"))))
    build_patch(a.game, m, "rpg/sleeping_spot_type", parse_rows(read_text(os.path.join(items, "rpg", "sleeping_spot_type__KRS-items.xml"))))
    build_patch(a.game, m, "item/document", parse_rows(read_text(os.path.join(items, "item", "document__KRS-items.xml"))))
    build_patch(a.game, m, "item/food", parse_rows(read_text(os.path.join(items, "item", "food__KRS-items.xml"))),
                comments={0: "Aesop Potion (drink): nutrition 10 -> 2.5, short-term ratio 0.1 -> 0.5"})

    # ---------------------------------------------------------------- krs_perks
    m = "krs_perks"
    write(os.path.join(ROOT, "modules", m, "mod.manifest"), MANIFEST.format(
        name="KRS Perks", modid=m, version="1.0.0", created="02/10/2026",
        description="Kingdom Refinement Suite - perks: Riposte and Master Strike are back (Riposte unlocks at level 10)."))
    legacy = parse_rows(read_text(os.path.join(a.main, "KingdomRefinementSuite", "Data", "perk__riposte.xml")))
    build_patch(a.game, m, "rpg/perk", legacy)
    loc = os.path.join(a.main, "KingdomRefinementSuite", "Localization")
    english = None
    texts = {}
    for lang in LANGUAGES:
        p = os.path.join(loc, f"{lang}_xml.pak")
        if os.path.exists(p):
            texts[lang] = zipfile.ZipFile(p).read("text__riposte.xml")
    english = texts["English"]
    for lang in LANGUAGES:
        write_bytes = texts.get(lang, english)       # languages the upstream mod did not translate show the English text
        path = os.path.join(ROOT, "modules", m, "Localization", lang, f"text__{m}.xml")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        open(path, "wb").write(write_bytes)
    print(f"{m}: localization for {len(LANGUAGES)} languages ({len(texts)} translated upstream, rest English)")

    # ---------------------------------------------------------------- krs_qol
    m = "krs_qol"
    write(os.path.join(ROOT, "modules", m, "mod.manifest"), MANIFEST.format(
        name="KRS QoL", modid=m, version="1.0.0", created="02/10/2026",
        description="Kingdom Refinement Suite - quality of life: bigger herb pick radius, more carry capacity, pricier but wider repairs, timed-quest marker."))
    herb = {"rpg_param_key": "HerbGatherSkillToRadius", "rpg_param_value": "0.35"}
    carry = {"rpg_param_key": "StrengthToInventoryCapacity", "rpg_param_value": "5"}
    price = {"rpg_param_key": "RepairPriceModif", "rpg_param_value": "1.3"}
    build_patch(a.game, m, "rpg/rpg_param", [carry, herb, price])
    hardcore = "01c3b32a-5751-4c98-b6ab-258d02370382"
    build_patch(a.game, m, "rpg/perk_rpg_param_override",
                [{"perk_id": hardcore, "rpg_param_key": "RepairPriceModif", "rpg_param_value": "1.8"}],
                comments={0: "Hardcore Mode constants only: vanilla 0.9, doubled like the global 0.65 -> 1.3"})
    build_patch(a.game, m, "rpg/skill2item_category",
                [{"item_category": "armor.horse_bridle.*", "skill_id": "8"}, {"item_category": "armor.horse_saddle.*", "skill_id": "8"}])
    names = {"english": "English", "czech": "Czech", "portuguese": "Portuguese"}
    for low, lang in names.items():
        t = git_show(f"develop:KingdomRefinementSuite/Data/Tables/ui/text_{low}__KRSPKG1.xml")
        rows = [(r["key"], r["text"], r["markup"]) for r in parse_rows(t)]
        write(os.path.join(ROOT, "modules", m, "Localization", lang, f"text__{m}.xml"), text_xml(rows))
        print(f"{m}: {lang}: {len(rows)} text rows")


if __name__ == "__main__":
    main()
