"""
grade_b_data.py - merges the curated parts of the Grade B review (grade_b_data_core / _mods1..4 / _balance) into one namespace for
tools/build_grade_b_page.py: SUBCATS, MODS, RANK, FEATURES, BALANCE, INTERS, QUESTIONS, GLOSSARY, STATUS.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from grade_b_data_core import FEATURES, GLOSSARY, INTERS, QUESTIONS, RANK, STATUS, SUBCATS  # noqa: E402,F401
from grade_b_data_balance import BALANCE  # noqa: E402,F401

MODS = {}
for _n in ("mods1", "mods2", "mods3", "mods4"):
    _m = __import__("grade_b_data_" + _n)
    MODS.update(_m.MODS)

FIELDS = ["name", "author", "version", "subcat", "status", "purpose", "observed", "loads", "systems", "newcontent", "stats", "text", "assets", "params", "balance",
          "snippets", "deps", "file_overlap", "func_overlap", "conflicts", "errors", "unique", "keep", "reject", "questions", "rank_note", "action", "verdict", "verdict_text"]
for _id, _m in MODS.items():
    _miss = [f for f in FIELDS if f not in _m]
    assert not _miss, (_id, _miss)
    _m.setdefault("family", "")

assert sorted(MODS) == sorted(i for _, _, _, ids in SUBCATS for i in ids), "every Grade B mod must be in exactly one sub-category"
