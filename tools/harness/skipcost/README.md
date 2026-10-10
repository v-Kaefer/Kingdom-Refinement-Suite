# krs_skipcost (prototype)

Takes hunger off after a Wait or a sleep. The engine charges no hunger during a time skip (measured in game 1.9.8), so a mod that
raises the digestion speed (KRS Items) makes the night free. This script charges, after each skip,

    hunger -= awake rate x skipped world seconds x factor

and leaves vigour and health to the engine.

| posture of the player during the skip | factor | default |
|---|---|---|
| standing (Wait from the inventory) | `--wait` | 0.75 |
| sitting (reading on a bench, a Wait on a chair) | `--sit` | 0.5 |
| lying (sleeping, fainting, reading in a bed), or vigour rising by more than 0.05 | `--sleep` | 0.5 |

Author's rule (10 Oct 2026): sleeping costs 50% and waiting 75% of the awake cost; reading and fainting count as 50% because a book
can only be read on a bed or better.

## How it works

- `krs_skipcost.lua` (startup script) keeps the settings and makes sure one entity is alive; a startup script has no frame hook, an
  entity has (`Client:OnUpdate`).
- `krs_skipcost_entity.lua` finds a skip from the frame time: during a Wait or a sleep the engine feeds the frame hook frames of
  about 0.25 s (normal ones are 0.02 to 0.05 s) and the clock moves by ratio x frame time, so the world seconds of those frames are the
  skipped time. The clock ratio is not used: it changes with the hours chosen and the last hour of a skip runs at the normal ratio.
- The kind comes from `player.player:IsLaying()` / `IsSitting()` while the skip runs. An earlier version flagged "sleep" when a bed was
  used (a wrapper on `Bed.OnUsedHold`); opening a bed and cancelling it then made a Wait right after cost 50%. Posture closes that.
- The awake rate is measured on the hunger bar over windows of 300 world seconds (it follows `DigestionSpeed` and perks); a window
  with a flat bar (the bar stops after a skip), a rise (eating) or a rate far from the current one is thrown away. The first value is
  `DigestionSpeed x 0.70`.
- One line per skip in `kcd.log`: `KRS_SC SKIP kind=stand|sit|lay hours=... rate_per_h=... factor=... cost=... hunger a -> b`.

## Build and test

    python tools/harness/skipcost/build_skipcost.py --game "<KCD folder>" [--wait 0.75] [--sit 0.5] [--sleep 0.5] [--apply 0|1] [--remove]
    powershell tools/harness/run_time_probe.ps1 -GameDir "<KCD folder>" -ProbeMod krs_skipcost -ExtraMods krs_items

The runner starts the game with only those mods, stamps the log lines and restores `mod_order.txt`. A person has to load a save.
Copy `Saved Games\kingdomcome\saves` before a test and compare it after: sleeping in a bed writes an autosave and the game deletes
the oldest autosave.

## Measured (replica 1.9.8, with krs_items)

- awake rate 3.19 to 3.29 per world hour (0.70 of the constant, 4.69 per hour);
- Wait of 3.991 h cost 9.534, Wait of 1.993 h cost 4.761 (rate x hours x 0.75), and the bar read back equal to the target;
- posture: stand awake, lay in the sleep dialog, then sit and stand after cancelling; a Wait after cancelling was charged 0.75.

Not tested: a real sleep with the mod, a Wait while sitting, reading a book, fainting. Not a module of the package yet.
