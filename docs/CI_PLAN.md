# CI/CD plan for the Kingdom Refinement Suite

Status date: 3 Oct 2026. This is a plan: no workflow file has been added yet. It builds on tools that already exist
(`tools/build_module.py`, `check_patch_names.py`, `check_ownership.py`, `audit_tables.py`, `gate.py`, `build_mods_index.py`).

## 1. Constraints that shape the design

| Fact | Consequence |
|---|---|
| The repo is **public**; Actions is enabled; no runner is registered | Hosted runners are free to use. A self-hosted runner on a public repo is a risk if it runs code from fork PRs (see 4) |
| The game (and its `Tables.pak`) cannot be on GitHub | Anything that needs vanilla values runs locally, or on a small committed snapshot (A2) |
| The in-game gate needs Steam, a desktop session and the game installed; it takes about 3 minutes at the main menu | It can only run on a self-hosted Windows runner (your PC), never on GitHub's runners |
| Perk, buff and sleeping-spot tables only load inside a level | Menu-stage gate covers 65 of the 74 row checks today; the rest needs the player stage (T1) |
| Tracked repo size is 3.3 MB | Checkouts are fast; keep `.pak`, `dist/` and game files out of git |
| The tools use only the Python standard library | No dependency install step is needed on the runner |

## 2. Branches and release flow

```
feature branch (claude/..., krs-<module>)  -->  PR to develop  -->  develop  -->  PR to main (release)  -->  tag
```

- `develop` is the integration branch (renamed from `dev` on 3 Oct 2026; PR #2 already targets it). `main` only receives release merges.
- Tags per module: `krs_items-v2.0.0`, `krs_perks-v1.0.0`, `krs_qol-v1.0.0` (the version in `modules/<id>/mod.manifest`).
- Protect `develop` and `main` once Tier A exists: required status checks (A1-A5), no force push, PRs required for `main`. Today neither is protected.
- Enable "Require approval for all outside collaborators" for workflows.

## 3. Tier A - hosted checks on every PR (GitHub-hosted `ubuntu-latest`, about 1 minute)

| # | Check | Command | What it catches | Why it matters (measured) |
|---|---|---|---|---|
| A1 | Build and engine rules | `python tools/build_module.py --all` | suffix != mod id, id with digits/hyphens, 7z-as-pak, partial rows, whole-table replacement | Before phase 0 none of the KRS patches loaded for exactly these reasons |
| A2 | Schema against vanilla | new: `tools/vanilla_snapshot.py` + `build_module.py --snapshot` | a patch header or row that does not match the vanilla table (missing `autolearnable` column in the perk rows, wrong column order or types, no-op rows) | Upstream Riposte rows omitted two columns; a no-op row can undo another mod's change |
| A3 | Localization files | new: `tools/check_localization.py` | not 3 cells per row, unescaped markup, language missing in `Localization/`, duplicate keys, languages without a pak (raw keys show in game) | The game only logs `Can't open file`; the failure is silent |
| A4 | Ownership | `python tools/check_ownership.py` (with the snapshot) | a changed row nobody owns, two modules setting the same row, a target value that differs from the file, a shipped row without an owner | Late mod wins the whole row, so duplicates are real conflicts |
| A5 | Docs do not drift | `python tools/build_mods_index.py && git diff --exit-code docs/mods/mods_index.csv` | lists updated without rebuilding the index | The lists change often |
| A6 | Lint | `ruff check tools` (or `python -m py_compile`), `luac5.1 -p` or `luacheck` on `tools/harness/*.lua` and future `modules/*/Data/Scripts` | syntax errors in the harness and in the bow script before they reach the game | A Lua error inside the game only shows in `kcd.log` |
| A7 | Repo hygiene | new: `tools/check_repo.py` | files over 5 MB, `.pak`/`.7z`/`.dds` outside `modules/`, third-party content (the Knox's Labelled Items folder is tracked today), `dist/` committed, CRLF/LF mix | Keeps game and third-party files out of the public repo |
| A8 | Markdown | `markdownlint` / link check on `docs/` | broken links | |

Output: a job summary with the pass/fail table and, for builds, the Vortex archives as workflow artifacts (`krs_items-2.0.0.zip` ...), so each PR has downloadable test builds.

**A2 detail.** The snapshot is a JSON file generated locally from `Tables.pak`: for every table a module patches, the header (column names and types), the key columns, and the vanilla rows the modules touch (about 70 rows). It contains no other game data. Decision needed: you may prefer to keep values out and store only headers and keys; then the no-op row check moves to Tier B.

Add also: `.gitattributes` (`* text=auto eol=lf`, `*.pak binary`, `*.dds binary`) because Git currently warns about LF/CRLF on every file; a PR template with the checklist in 6; `CODEOWNERS` for `modules/` and `docs/ownership.csv`; Dependabot for the actions used.

## 4. Tier B - in-game gate on a self-hosted Windows runner (your PC)

Runner labels: `self-hosted, windows, kcd`. It needs the game, Steam logged in and an interactive desktop session (run the runner as a program in your session, not as a service).

**Security (public repo).** Never run Tier B on pull requests from forks. Use `workflow_dispatch`, a `run-gate` label that only you can add, or `pull_request` with an explicit `if: github.event.pull_request.head.repo.full_name == github.repository`. Set the runner to ephemeral if you can.

| # | Job | Trigger | Command | Result |
|---|---|---|---|---|
| B1 | Gate, menu stage | label `run-gate` or manual | `python tools/gate.py krs_items krs_perks krs_qol --mode tables` | pass/fail, `docs/tests/gate_*.log` as artifact, summary table of rows and constants |
| B2 | Compatibility matrix | nightly or manual | the same with `--with` for each set in `ci/compat_sets.json` (your Vortex list, Perkaholic variants, Food Spoil Faster, Riposte upstream ...) | per set: which `Table ... is patched by` lines appeared, whether KRS rows still read back, which rows lose to a later mod |
| B3 | Engine contract tests | manual after each game update | new `tools/contract_tests.py`: re-runs the 10 rules of `docs/tests/PTF_FINDINGS.md` (suffix == id, partial rows blank columns, later mod wins, ZIP pak, hidden constant write) | tells you in minutes if a patch changes the rules; records the build string from `kcd.log` |
| B4 | Player stage | manual until T1 | `gate.py --mode full` | perk, sleeping-spot, override and `skill2item_category` rows, live bow test |

Operating rules for the runner: one job at a time (`concurrency: kcd-runner`), timeout 15 minutes, never while you are playing (schedule at night, and a repository variable `KCD_RUNNER_ENABLED` that you turn off to skip), and always restore `Mods/mod_order.txt` (the PowerShell runner already does this in a `finally` block and removes the test mods).

## 5. Tier C - release automation (on tag)

1. Build the module from the tag and verify the tag matches `<version>` in `mod.manifest`.
2. Refuse to release when `ownership.csv` still has a shipped row with permission pending (new column `permission`: `own`, `granted`, `pending`); today this blocks `StrengthToInventoryCapacity` in `krs_qol`.
3. Refuse to release without a B1 pass for the same commit (the gate log artifact, or a committed `docs/tests/gate_<id>_<sha>.log`).
4. Create the GitHub release with `krs_<id>-<version>.zip`, SHA256 sums, and the text of `modules/<id>/CHANGES.md` for that version.
5. Nexus upload and the Vortex install smoke test stay manual (checklist in the PR template); there is no stable public upload API to depend on.

## 6. Test backlog that improves the mods themselves

| # | Test | Why | Needs |
|---|---|---|---|
| T1 | Automate "Continue" in the test instance | Unlocks perk, buff, sleeping-spot and live tests | Screen-control approval (denied once while you were away), or a dedicated test save plus a start argument if one exists |
| T2 | Behaviour tests in game | Rows reading back is not the same as the mod working: reading time per book, hunger drop over one in-game day with `DigestionSpeed`, carry capacity (`GetDerivedStat('cap')` before and after), herb radius, repair price in a shop | T1 plus small Lua probes in `krs_gate.lua` (`extra_player` hook exists) |
| T3 | Bow live-read | Decides whether `AimSpreadMax` and `BowCharge*` are read when drawing (phase 4) | T1 plus a drawn arrow in the test save |
| T4 | No-op and overlap guard as a failing test | Prevents rows equal to vanilla and rows that two modules set | A2, A4 |
| T5 | Potion rules (phase 5) | `tools/potion_model_check.py` as an A-tier check: no designed potion changed, deltas bounded, complete rows | potions module |
| T6 | Save compatibility | The README promises "safe to remove": load a save made with the mods, remove them, load again | manual checklist first, automation after T1 |
| T7 | Version matrix | Run B1 and B3 on 1.9.6, 1.9.7, 1.9.8 and record which `<supports>` entries are true | the game versions installed side by side (PR #2 documents a separate 1.9.8 test install) |

## 7. Rollout order

| Step | Content | Effort |
|---|---|---|
| 1 | `.gitattributes`, PR template, CODEOWNERS, A1, A5, A6 as `ci.yml` (no new tools needed) | S |
| 2 | A2 snapshot tool, A3, A4, A7; protect `develop` with A1-A5 as required checks | M |
| 3 | Register the self-hosted runner, B1 on label/manual; log summary and artifact upload | M |
| 4 | Tier C release workflow and the `permission` column | S |
| 5 | B3 contract tests, B2 compatibility matrix | M |
| 6 | T1 and T2 (player stage, behaviour tests), then T3 and the bow | L |

## 8. Decisions needed from you

1. Is a self-hosted runner on your PC acceptable (labels, never for fork PRs, nightly schedule)? If not, Tier B stays a local command (`python tools/gate.py ...`) and Tier A is the only CI.
2. May the vanilla snapshot contain the values of the rows we touch, or only headers and keys?
3. Protect `develop` and `main` with required checks once Tier A exists? And should PR #1 (still targeting `main`) be retargeted to `develop`?
4. Tag format `krs_items-v2.0.0` and one release per module, or one suite release?
5. Remove the tracked third-party folder (Knox's Labelled Items) from the public repo, and keep the legacy `KingdomRefinementSuite/` folder until the modules are published?

## Appendix: skeletons (not committed as workflows)

`ci.yml` (Tier A, steps 1 of the rollout):

```yaml
name: ci
on:
  pull_request:
    branches: [develop, main]
  push:
    branches: [develop]
jobs:
  checks:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: "3.12" }
      - run: python tools/build_module.py --all
      - run: python tools/build_mods_index.py && git diff --exit-code docs/mods/mods_index.csv
      - run: python -m py_compile tools/*.py tools/harness/*.py
      - uses: actions/upload-artifact@v4
        with: { name: krs-modules, path: dist/*.zip }
```

`gate.yml` (Tier B1):

```yaml
name: gate
on:
  workflow_dispatch:
  pull_request:
    types: [labeled]
concurrency: kcd-runner
jobs:
  gate:
    if: github.event_name == 'workflow_dispatch' || (github.event.label.name == 'run-gate' && github.event.pull_request.head.repo.full_name == github.repository)
    runs-on: [self-hosted, windows, kcd]
    timeout-minutes: 15
    steps:
      - uses: actions/checkout@v4
      - run: python tools/gate.py krs_items krs_perks krs_qol --mode tables
      - uses: actions/upload-artifact@v4
        if: always()
        with: { name: gate-logs, path: docs/tests/gate_*.log }
```
