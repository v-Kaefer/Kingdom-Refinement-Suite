"""Where things live in the repository. Import from here instead of hard-coding folder names (docs/project/DOCS_PLAN.md)."""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(ROOT, "docs")
PROJECT = os.path.join(DOCS, "project")
ENGINE = os.path.join(DOCS, "engine")
MODULE_DOCS = os.path.join(DOCS, "modules")
MODS_REVIEW = os.path.join(DOCS, "mods-review")
DATA = os.path.join(DOCS, "data")
TESTS = os.path.join(DOCS, "tests")
TEST_LOGS = os.path.join(TESTS, "logs")
TEST_RESULTS = os.path.join(TESTS, "results")
ARCHIVE = os.path.join(DOCS, "archive")
OWNERSHIP = os.path.join(DATA, "ownership.csv")
AUDIT_DIR = os.path.join(DATA, "table-audit")
MODULES = os.path.join(ROOT, "modules")
