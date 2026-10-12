"""
params_info.py - what an rpg_param constant means and what its value is in the unmodified game.

    from params_info import load; P = load(); P["CombatAutoPBWeight"] -> {"desc", "section", "default", "source"}

Sources (all read-only, all in the repository):
    Mods WIP folder/Params Reference.md          the game's own one-line comments of the constants, by section
    docs/engine/rpg_constants_runtime.csv        the value the running game returned for each constant (read on 1.9.6 with the harness;
                                                 for constants that are rows of the vanilla rpg_param table the table value is in the same file)
    Data/Tables.pak rpg_param                    the 1.9.8 table (through tools/audit_tables.py), when given
"""
import csv
import os
import re

import paths

REF = os.path.join(paths.ROOT, "Mods WIP folder", "Params Reference.md")
RUNTIME = os.path.join(paths.ENGINE, "rpg_constants_runtime.csv")


def load(vanilla_rpg_param_rows=None):
    desc = {}
    section = ""
    if os.path.exists(REF):
        for line in open(REF, encoding="utf-8", errors="replace"):
            line = line.rstrip("\n")
            m = re.match(r"^##\s+(.*)$", line)
            if m:
                section = m.group(1).strip()
                continue
            m = re.match(r"^([A-Za-z][A-Za-z0-9_]*)\s*(?:\*\s*(.*))?$", line)
            if m:
                desc[m.group(1)] = (section, (m.group(2) or "").strip())
    out = {}
    if os.path.exists(RUNTIME):
        for r in csv.DictReader(open(RUNTIME, encoding="utf-8", newline="")):
            k = r["key"]
            out[k] = {"desc": desc.get(k, ("", ""))[1], "section": desc.get(k, ("", ""))[0] or r.get("params_reference_section", ""),
                      "default": r["runtime_value"], "source": "valor lido no jogo (1.9.6, harness)", "table_value": r.get("vanilla_table_value", "")}
    for k, (sec, d) in desc.items():
        out.setdefault(k, {"desc": d, "section": sec, "default": "", "source": "", "table_value": ""})
    if vanilla_rpg_param_rows:
        for r in vanilla_rpg_param_rows:
            k = r.get("rpg_param_key")
            e = out.setdefault(k, {"desc": "", "section": "", "default": "", "source": "", "table_value": ""})
            e["default"] = r.get("rpg_param_value", "")
            e["source"] = "tabela rpg_param do jogo (1.9.8)"
    return out
