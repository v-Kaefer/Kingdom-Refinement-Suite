#!/usr/bin/env python3
"""Build the named Nexus uploads in nexus/ from the maintained module sources.

The historical krs_items source contains three unrelated areas. This builder
separates its complete PTF rows into three independent mod ids without changing
that source. It then combines installable module folders into named uploads.
"""
from __future__ import annotations

import copy
from pathlib import Path
import tempfile
import xml.etree.ElementTree as ET
import zipfile

import build_module as bm

ROOT = Path(__file__).resolve().parent.parent
NEXUS = ROOT / "nexus"
ITEMS = ROOT / "modules" / "krs_items"

SPLITS = {
    "krs_gluttony": {
        "name": "Gluttony Rebalanced - Hunger",
        "version": "1.0.0",
        "description": "Faster digestion and stronger starvation effects.",
        "files": {
            "rpg/rpg_param": {"DigestionSpeed", "StarvationPlayerEffectMinMin", "StarvationPlayerEffectMaxMax", "StarvationPlayerEffectMinMax"},
        },
    },
    "krs_leech_lore": {
        "name": "Leech and Lore Reworked - Reading",
        "version": "1.0.0",
        "description": "Longer skill-book reading and adjusted reading experience.",
        "files": {
            "item/document": None,
            "rpg/rpg_param": {"ReadingXpPerHour"},
        },
    },
    "krs_realistic_potions": {
        "name": "Realistic Potions - Aesop",
        "version": "1.0.0",
        "description": "A focused nourishment adjustment for Aesop Potion.",
        "files": {"item/food": None},
    },
}

UPLOADS = {
    "KRS-Items/Gluttony Rebalanced": ("Gluttony-Rebalanced-1.0.0.zip", ("krs_gluttony", "krs_skipcost")),
    "KRS-Items/Leech & Lore Reworked": ("Leech-and-Lore-Reworked-1.0.0.zip", ("krs_leech_lore",)),
    "KRS-Items/Realistic Potions": ("Realistic-Potions-Aesop-1.0.0.zip", ("krs_realistic_potions",)),
    "KRS-Perks/Perks Reworked": ("Perks-Reworked-1.0.0.zip", ("krs_perks",)),
    "KRS-QoL/Everyday Tweaks": ("Everyday-Tweaks-1.0.0.zip", ("krs_qol",)),
    "KRS-Exploration/Exploration Reworked": ("Exploration-Reworked-1.0.0.zip", ("krs_exploration",)),
}


def split_xml(source: Path, table: str, keys: set[str] | None) -> bytes:
    tree = ET.parse(source)
    root = copy.deepcopy(tree.getroot())
    table_node = root.find("table")
    assert table_node is not None and table_node.get("name") == table
    rows = table_node.find("rows")
    assert rows is not None
    key_attr = "rpg_param_key" if table == "rpg_param" else None
    if keys is not None:
        assert key_attr is not None
        for row in list(rows):
            if row.get(key_attr) not in keys:
                rows.remove(row)
        assert {row.get(key_attr) for row in rows} == keys
    else:
        assert len(rows) > 0
    ET.indent(root, space="  ")
    return ET.tostring(root, encoding="utf-8", xml_declaration=True) + b"\n"


def manifest(modid: str, spec: dict) -> bytes:
    root = ET.parse(ITEMS / "mod.manifest").getroot()
    info = root.find("info")
    assert info is not None
    for tag, value in (("modid", modid), ("name", spec["name"]),
                       ("version", spec["version"]), ("description", spec["description"])):
        node = info.find(tag)
        assert node is not None
        node.text = value
    ET.indent(root, space="  ")
    return ET.tostring(root, encoding="utf-8", xml_declaration=True) + b"\n"


def build_split(modid: str, spec: dict, out: Path) -> None:
    folder = out / modid
    folder.mkdir(parents=True)
    (folder / "mod.manifest").write_bytes(manifest(modid, spec))
    data = {}
    for relative, keys in spec["files"].items():
        category, table = relative.split("/")
        source = ITEMS / "Data" / "Libs" / "Tables" / category / f"{table}__krs_items.xml"
        target = f"Libs/Tables/{category}/{table}__{modid}.xml"
        data[target] = split_xml(source, table, keys)
    bm.make_pak(str(folder / "Data" / f"{modid}.pak"), data)
    if not bm.check(str(folder)):
        raise RuntimeError(f"Invalid packed module: {modid}")


def make_upload(target: Path, modids: tuple[str, ...], built: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(target, "w") as archive:
        for modid in modids:
            folder = built / modid
            assert (folder / "mod.manifest").is_file()
            for path in sorted(folder.rglob("*")):
                if path.is_file():
                    relative = f"{modid}/{path.relative_to(folder).as_posix()}"
                    archive.writestr(bm.entry(relative, False), path.read_bytes())
    with zipfile.ZipFile(target) as archive:
        bad = archive.testzip()
        if bad:
            raise RuntimeError(f"Bad ZIP entry: {bad}")
        manifests = {name for name in archive.namelist() if name.endswith("/mod.manifest")}
        assert manifests == {f"{modid}/mod.manifest" for modid in modids}


def main() -> None:
    scratch = ROOT / "dist"
    scratch.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="krs_nexus_", dir=scratch) as temp:
        built = Path(temp)
        for modid, spec in SPLITS.items():
            build_split(modid, spec, built)
        for modid in ("krs_skipcost", "krs_perks", "krs_qol", "krs_exploration"):
            if not bm.build(modid, str(built)):
                raise RuntimeError(f"Module build failed: {modid}")
        for relative, (filename, modids) in UPLOADS.items():
            folder = NEXUS / relative
            assert (folder / "NEXUS_DESCRIPTION.txt").is_file(), relative
            target = folder / filename
            make_upload(target, modids, built)
            print(f"{target.relative_to(ROOT)}: {', '.join(modids)}")


if __name__ == "__main__":
    main()
