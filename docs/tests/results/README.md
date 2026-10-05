# Test results: one line per game run

> **Status date:** 2026-10-03 | **Kind:** evidence | **Trust:** measured | **Game version:** 1.9.6 and 1.9.8

Newest first. A run is one start of the test game. Raw logs are in `../logs/`; the rules they established are in `../../engine/`.

| Date | Game | What was run | Result | Log |
|---|---|---|---|---|
| 2026-10-03 | 1.9.8 | the three modules after the docs and tools reorganization (menu stage), to confirm the gate still works | **Gate passed, 73/73, 8/8 patch files** | `gate_krs_items_krs_perks_krs_qol_1.9.8_tables.log` |
| 2026-10-03 | 1.9.8 | `krs_items`, `krs_perks`, `krs_qol` + 5 manifest probe mods + a real Riposte copy with its version line edited (menu stage) | **Gate passed, 73/73 checks, 8/8 patch files applied.** Probes: `1.9.6`-only and `1.9.x` disabled; edited, range and no-block loaded and patched; edited Riposte loaded (`perk__riposte`, modified 2). See `../../engine/game-versions.md` | `gate_manifest_probe_1.9.8_tables.log` |
| 2026-10-03 | 1.9.8 | same modules + the author's Vortex mod list (second attempt, before the harness knew about the missing `mm_main` event) | modules enabled and all 8 patches applied; harness never ran its checks (no `mm_main`); also showed Riposte and Drink Sound Effects disabled by their manifests | `gate_compat_user_mods_1.9.8_tables.log` |
| 2026-10-03 | 1.9.8 | same modules, first attempt with manifests listing only 1.9.6 | **all four mods disabled by the engine**, including the test harness, so nothing ran; led to the manifest findings | (output only, summarized in `engine/game-versions.md`) |
| 2026-10-03 | 1.9.8 | modules again, interrupted when the session ended | no result | `gate_all_1.9.8_tables.log` (partial) |
| 2026-10-02 | 1.9.6 | modules with the author's Vortex mod list (menu stage) | passed, 73/73; `krs_perks` after the upstream Riposte: modified 1, equal 1 | `gate_compat_user_mods_tables.log` |
| 2026-10-02 | 1.9.6 | the three modules together (menu stage) | passed, 73/73 | `gate_krs_items_krs_perks_krs_qol_tables.log` |
| 2026-10-02 | 1.9.6 | `krs_items` alone, menu stage; then full mode (waited 6 min at the menu) | menu stage passed 67/67; full mode stopped: Continue not pressed | `gate_krs_items_tables.log`, `gate_krs_items_full.log` |
| 2026-10-02 | 1.9.6 | first harness runs: patch-rule probes, API and constants, KRS files as packaged vs fixed | the rules in `engine/ptf-rules.md` and `engine/lua-and-constants.md` | `run_*.log` |
