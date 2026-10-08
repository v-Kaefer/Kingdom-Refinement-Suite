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

On 1.9.8 the first screen is the EULA; the author reports that pressing `Q` passes it (not yet tried by a session).

Limits: the test instance must run with Steam open; use at most a few runs per session, each takes 3 to 6 minutes. On 1.9.8 the main menu does not send `mm_main/OnStart`, so the menu-stage checks start from `sys_startup/OnEnd`.


## Checking an animation database file (6 Oct 2026)

```bash
python tools/harness/build_adbtest.py --game "<KCD folder>" --adb merged.adb      # installs Mods/krs_adbtest (without --adb: baseline)
powershell -File tools/harness/run_game_test.ps1 -GameDir "<KCD folder>" -Mods krs_adbtest -Harness krs_adbtest -OutFile out.log
python tools/harness/build_adbtest.py --game "<KCD folder>" --remove
```
The game parses `Animations/Mannequin/ADB/kcd_male_database.adb` from a mod at startup (actors such as `DummyTarget`) and logs `XML reader: ...` and `Invalid animation DB for actor ...` for a malformed file; a valid one gives the same log as the baseline. The script also runs `mn_reload` and `mn_listAssets` at `sys_startup/OnEnd` (they print nothing to the log). The runner reports `harness done=False` even when the end marker is in `kcd.log` (it only looks at a log written after launch): read `kcd.log` itself, and copy it before the next run. Logs: `logs/adbtest_*_1.9.8.log`; results in `modules/krs_exploration/src/merge_tests/README.md`.

## Reshield (2313) with the trough wash
`reshield` polls every 400 ms, remembers the shield seen in hand, and calls `player.actor:EquipInventoryItem` when it stops seeing a torch. It does not bring a torch back. The wash unequips the torch inside the behaviour, so `reshield` may equip the shield during the wash animation, and then the wash's own torch return swaps it again. This is the thing to look at in a play test. Menu-level run on 1.9.8 with krs_exploration, krs_exploration_wash and reshield: all three loaded, `[Reshield] v2.0 loaded`, no Lua error from them (the `luatestctrlentity.lua` getenv error is vanilla, it is also in the editor logs).
