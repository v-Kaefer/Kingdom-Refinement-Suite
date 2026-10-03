#!/usr/bin/env python3
"""
build_harness.py - create the KRS in-game test mods inside a KCD install.

    python tools/harness/build_harness.py --game "<KCD folder>" [--params-ref "Params Reference.md"] [--mode tables|full]

Writes two mods under <game>/Mods:
    krs_harness/    Scripts/Startup/krs_harness.lua + an entity (the test code) and table patches on `food`
    krs_harness_b/   a second patch mod on `food`, used to see how two mods that touch the same row combine

FINDING (see docs/engine/ptf-rules.md): the engine only applies a table patch whose file suffix equals the mod id
(`food__krs_harness.xml` for modid `krs_harness`). Both mods therefore name their patch after their own modid.

Patches (vanilla `food` table):
    krs_harness  : Aesop, full row, nutrition 10 -> 2.5 and ratio 0.1 -> 0.5            (what KRS-Items does today)
                   Aqua Vitalis, PARTIAL row (item_id + refresh_benefit only)
    krs_harness_b : Aesop, full row, decay_time_hours 0 -> 123                            (what Food Spoil Faster does to a row)
                   Antidote, PARTIAL row inside a table named food__krs_harness_b (suffix style of the table name)

Remove the folders to uninstall (tools/harness/run_game_test.ps1 -Cleanup does this).
"""
import argparse
import os
import re
import xml.etree.ElementTree as ET
import zipfile

AESOP = "73ff1fde-ec8b-41e9-95e3-b5938c715bf1"
AQUA_VITALIS = "850d28d9-9d0a-4b2e-9feb-e6c48c5f1aad"
ANTIDOTE = "8b713d0c-9a04-4354-a53f-ffd384057fa6"

MANIFEST = """<?xml version="1.0" encoding="utf-8"?>
<kcd_mod>
  <info>
    <name>{name}</name>
    <description>Test harness for the Kingdom Refinement Suite. Logs results to kcd.log and quits.</description>
    <author>KRS</author>
    <version>0.0.1</version>
    <created_on>02/10/2026</created_on>
    <modid>{modid}</modid>
    <modifies_level>false</modifies_level>
  </info>
  <supports>
    <kcd_version>1.9.6</kcd_version>
    <kcd_version>1.9.7</kcd_version>
    <kcd_version>1.9.8</kcd_version>
  </supports>
</kcd_mod>
"""


def read_member(z, zi):
    try:
        return z.open(zi).read()
    except zipfile.BadZipFile:
        zi.orig_filename = zi.filename.replace("/", "\\")
        return z.open(zi).read()


def vanilla_table(game, member):
    z = zipfile.ZipFile(os.path.join(game, "Data", "Tables.pak"))
    data = read_member(z, z.getinfo(member)).decode("utf-8", "replace")
    root = ET.fromstring(re.sub(r"^\s*<\?xml[^>]*\?>", "", data))
    t = root.find("table")
    cols = [(c.get("name"), c.get("type")) for c in t.findall("./header/column")]
    rows = {r.get("item_id"): dict(r.attrib) for r in t.findall("./rows/row")}
    return cols, rows


def patch_xml(table_name, cols, rows):
    out = ['<?xml version="1.0" encoding="us-ascii"?>', '<database name="hammerheart">',
           f'  <table name="{table_name}" version="1">', "    <header>"]
    out += [f'      <column name="{n}" type="{t}" />' for n, t in cols]
    out += ["    </header>", "    <rows>"]
    for r in rows:
        out.append("      <row " + " ".join(f'{k}="{v}"' for k, v in r.items()) + " />")
    out += ["    </rows>", "  </table>", "</database>", ""]
    return "\n".join(out)


def entry(name, is_dir):
    """zip entry with the attributes of 7-Zip-made paks (what Vortex installs)."""
    zi = zipfile.ZipInfo(name, date_time=(2026, 10, 2, 0, 0, 0))
    zi.create_system = 0
    zi.external_attr = 16 if is_dir else 32
    zi.compress_type = zipfile.ZIP_STORED if is_dir else zipfile.ZIP_DEFLATED
    return zi


def write_mod(game, folder, modid, name, files):
    mod = os.path.join(game, "Mods", folder)
    os.makedirs(os.path.join(mod, "Data"), exist_ok=True)
    open(os.path.join(mod, "mod.manifest"), "w", encoding="utf-8", newline="\n").write(MANIFEST.format(name=name, modid=modid))
    with zipfile.ZipFile(os.path.join(mod, "Data", f"{folder}.pak"), "w") as zf:
        dirs = set()
        for n in files:
            parts = n.split("/")[:-1]
            for k in range(1, len(parts) + 1):
                dirs.add("/".join(parts[:k]) + "/")
        for d in sorted(dirs):
            zf.writestr(entry(d, True), "")
        for n, text in files.items():
            zf.writestr(entry(n, False), text)
    print(f"built {mod}: {len(files)} files")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", required=True)
    ap.add_argument("--params-ref", default="Params Reference.md")
    ap.add_argument("--mode", choices=["tables", "full"], default="full",
                    help="tables: read tables/constants at the main menu and quit; full: also wait for the player")
    a = ap.parse_args()

    cols, food = vanilla_table(a.game, "Libs/Tables/item/food.xml")
    h1 = dict(food[AESOP]); h1.update(nutrition_benefit="2.5", short_term_nutrition_benefit_ratio="0.5")
    h2 = dict(food[AESOP]); h2.update(decay_time_hours="123")
    h3 = {"item_id": AQUA_VITALIS, "refresh_benefit": "9"}
    h4 = {"item_id": ANTIDOTE, "health_benefit": "7"}

    # parameter keys to read: Params Reference + vanilla rpg_param
    keys = set()
    if os.path.exists(a.params_ref):
        for line in open(a.params_ref, encoding="utf-8", errors="replace"):
            m = re.match(r"^([A-Z][a-z0-9]+(?:[A-Z][A-Za-z0-9]*)+)\b", line)
            if m:
                keys.add(m.group(1))
    z = zipfile.ZipFile(os.path.join(a.game, "Data", "Tables.pak"))
    root = ET.fromstring(re.sub(r"^\s*<\?xml[^>]*\?>", "", read_member(z, z.getinfo("Libs/Tables/rpg/rpg_param.xml")).decode("utf-8", "replace")))
    keys |= {r.get("rpg_param_key") for r in root.iter("row")}
    keys = sorted(keys)

    wanted = ["nutrition_benefit", "short_term_nutrition_benefit_ratio", "decay_time_hours", "refresh_benefit",
              "health_benefit", "alcohol_content", "max_status"]
    checks = [
        ("Aesop: mod1 nutrition 2.5 / ratio 0.5 ; mod2 decay 123 (vanilla 10 / 0.1 / 0)", "food", "item_id", AESOP, wanted),
        ("Aqua Vitalis: mod1 PARTIAL row refresh 9 (vanilla 5/4/0/0.5/100/0)", "food", "item_id", AQUA_VITALIS, wanted),
        ("Antidote: mod2 PARTIAL row health 7 (vanilla 5/4/0/0.5/100/0)", "food", "item_id", ANTIDOTE, wanted),
        ("Book 0a9b5b2a: reading time (vanilla 6 h, KRS-Items 15 h)", "document", "item_id", "0a9b5b2a-2614-4f11-a987-aab64133bea0", ["length_in_game_hours"]),
        ("Beer: item category 5 in vanilla", "item", "item_id", "52afd6fa-9377-457c-83a2-b5b39321a4dc", ["item_category_id", "item_name"]),
    ]
    header = ['KRS = { mode = "%s", keys = {' % a.mode + ", ".join('"%s"' % k for k in keys) + "}, food_checks = {"]
    for label, tbl, key, iid, ws in checks:
        header.append('  { label = "%s", table = "%s", key = "%s", id = "%s", cols = {%s} },'
                      % (label, tbl, key, iid, ", ".join('"%s"' % w for w in ws)))
    header.append("} }")
    here = os.path.dirname(os.path.abspath(__file__))
    lua = "\n".join(header) + "\n" + open(os.path.join(here, "krs_harness.lua"), encoding="utf-8").read()

    files1 = {
        "Libs/Tables/item/food__krs_harness.xml": patch_xml("food", cols, [h1, h3]),
        "Scripts/Startup/krs_harness.lua": lua,
        "Scripts/Entities/KRSHarness.lua": open(os.path.join(here, "krs_harness_entity.lua"), encoding="utf-8").read(),
        "Entities/KRSHarness.ent": '<Entity\n        Name="KRSHarness"\n        Script="Scripts/Entities/KRSHarness.lua"\n/>\n',
    }
    pcols = [("item_id", "uuid"), ("weapon_buff_id", "uuid")]
    # probe: does a hyphen in the file suffix match an underscore in the mod id?
    files1["Libs/Tables/item/potion__krs-harness.xml"] = patch_xml(
        "potion", pcols, [{"item_id": "f0f0f0f0-0000-4000-8000-000000000001", "weapon_buff_id": ""}])
    files2 = {"Libs/Tables/item/food__krs_harness_b.xml": patch_xml("food__krs_harness_b", cols, [h2, h4])}
    write_mod(a.game, "krs_harness", "krs_harness", "KRS Test Harness", files1)
    write_mod(a.game, "krs_harness_b", "krs_harness_b", "KRS Test Harness B", files2)
    print(f"{len(keys)} parameter keys; mode {a.mode}")


if __name__ == "__main__":
    main()
