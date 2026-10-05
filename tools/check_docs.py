#!/usr/bin/env python3
"""
check_docs.py - keeps the documentation consistent (docs/project/DOCS_PLAN.md).

    python tools/check_docs.py

Checks, for every Markdown file under docs/ (not archive/, mods-review/raw/, mods-review/sources/, tests/logs/):
  1. relative links `[text](path)` point to an existing file or folder
  2. backticked repo paths that start with `docs/`, `tools/` or `modules/` exist (glob characters and `<...>` placeholders are skipped)
  3. the file starts with the status block (`> **Status date:** ... | **Kind:** ... | **Trust:** ...`) or a GENERATED marker
  4. the file is mentioned in docs/README.md (the index), except README files of sub folders
  5. docs/project/STATUS.md has a Status date no older than 30 days
Exit code 1 when anything is reported.
"""
import datetime
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paths  # noqa: E402

SKIP = ("archive", os.path.join("mods-review", "raw"), os.path.join("mods-review", "sources"), os.path.join("tests", "logs"))
LINK = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")
TICK = re.compile(r"`((?:docs|tools|modules)/[^`\s*<>{}$]+)`")


def md_files():
    for dp, dn, fn in os.walk(paths.DOCS):
        rel = os.path.relpath(dp, paths.DOCS)
        if any(rel == s or rel.startswith(s + os.sep) for s in SKIP):
            dn[:] = []
            continue
        for f in fn:
            if f.endswith(".md"):
                yield os.path.join(dp, f)


def main():
    problems = []
    index = open(os.path.join(paths.DOCS, "README.md"), encoding="utf-8").read()
    for p in md_files():
        rel = os.path.relpath(p, paths.ROOT).replace("\\", "/")
        text = open(p, encoding="utf-8").read()
        head = "\n".join(text.splitlines()[:6])
        if "**Status date:**" not in head and "**GENERATED**" not in head:
            problems.append(f"{rel}: no status block in the first lines")
        for m in LINK.finditer(text):
            target = m.group(1).split("#")[0]
            if not target or re.match(r"[a-z]+:", target):
                continue
            if not os.path.exists(os.path.normpath(os.path.join(os.path.dirname(p), target))):
                problems.append(f"{rel}: broken link {m.group(1)}")
        for m in TICK.finditer(text):
            q = m.group(1).rstrip(".,:;)")
            if rel.endswith("DOCS_PLAN.md") or q.endswith(("/", ".md.", "...")):
                continue
            if not os.path.exists(os.path.join(paths.ROOT, q)):
                problems.append(f"{rel}: path in backticks does not exist: {q}")
        base = os.path.basename(p)
        sub = os.path.relpath(p, paths.DOCS).replace("\\", "/")
        if base != "README.md" and sub not in index and base not in index:
            problems.append(f"{rel}: not mentioned in docs/README.md")
    status = os.path.join(paths.PROJECT, "STATUS.md")
    if os.path.exists(status):
        m = re.search(r"\*\*Status date:\*\* (\d{4}-\d{2}-\d{2})", open(status, encoding="utf-8").read())
        if m and (datetime.date.today() - datetime.date.fromisoformat(m.group(1))).days > 30:
            problems.append(f"docs/project/STATUS.md: Status date {m.group(1)} is older than 30 days")
    print("\n".join(problems) or "docs OK")
    print(f"{len(problems)} problem(s)")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
