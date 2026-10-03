# Tests: how to run the game checks and read the results

> **Status date:** 2026-10-03 | **Kind:** evidence | **Trust:** measured | **Game version:** 1.9.6 and 1.9.8

The checks start the replica game with only the mods under test, read tables and constants back through the Lua API, and stop the game. Nothing is saved. Raw logs are in `logs/`, one short summary per run in `results/`.

## Running the first harness (rules and API tests)

```bash
python tools/harness/build_harness.py --game "<KCD folder>" --params-ref "Params Reference.md" --mode tables
```
```powershell
tools\harness\run_game_test.ps1 -GameDir "<KCD folder>" -OutFile result.log -Mods 'krs_harness','krs_harness_b'
```
The runner backs up `Mods\mod_order.txt`, loads only the listed mods, starts the game, waits for the harness line
`KRS_HARNESS end`, stops the game if needed and restores `mod_order.txt`. Remove the test mods from `Mods` afterwards.
Side effects: each run creates a new `kcd.log` and moves the previous one into `logbackups/`; the game does not save.


## Running the module gate

```bash
python tools/gate.py krs_items krs_perks krs_qol            # menu stage, no input needed
python tools/gate.py krs_items krs_perks krs_qol --mode full # also needs Continue pressed (level tables)
```

Limits: the test instance must run with Steam open; use at most a few runs per session, each takes 3 to 6 minutes. On 1.9.8 the main menu does not send `mm_main/OnStart`, so the menu-stage checks start from `sys_startup/OnEnd`.
