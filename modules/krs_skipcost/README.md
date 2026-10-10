# KRS Skip Cost

Part of the Kingdom Refinement Suite, in the **Gluttony Rebalanced** package. Waiting and sleeping cost hunger again.

The game charges **no hunger during a time skip** (Wait from the inventory, sleeping, reading, fainting; measured in game 1.9.8). So any
mod that makes hunger faster, KRS Items for one, makes the night free. This mod takes hunger off after each skip:

    hunger -= awake hunger rate x skipped world seconds x share

The share depends on the posture of the player while the skip runs:

| Posture | Share | Typical case |
|---|---|---|
| standing | 75% | Wait from the inventory |
| sitting | 50% | reading on a bench, a Wait on a chair |
| lying | 50% | sleeping, fainting, reading in a bed |

A skip during which vigour rises by more than 0.05 also counts as lying. Vigour and health are left to the game. The awake rate is read
from the hunger bar itself, so it follows `DigestionSpeed` (KRS Items sets it) and perks; it needs about 20 real seconds of play after a
load before the first measurement (until then it uses `DigestionSpeed x 0.70`).

## What it does not do
- It does not touch tables, saves or the sleep recovery. The hunger value it sets lives only in the game's memory and in your next save.
- The shares are in `Data/Scripts/Startup/krs_skipcost.lua` (`KRS_SC_CFG`: `wait`, `sit`, `sleep`, `apply`); `apply = 0` only logs.
- Not tested in game with this module: a real sleep, a Wait while sitting, reading a book, fainting (a Wait standing and the posture
  change lay, sit, stand were). One line per skip goes to `kcd.log`: `KRS_SC SKIP kind=stand|sit|lay hours=... cost=...`.

## Install
Vortex: install `krs_skipcost-<version>.zip` and enable it. Manually: copy the folder `krs_skipcost` into
`KingdomComeDeliverance/Mods/` and add `krs_skipcost` to `Mods/mod_order.txt`. Safe to remove at any time; hunger already taken stays.

## Compatibility
Scripts only: an entity (`KRSSkipCost`) with a frame hook and a startup script. It does not conflict with table patches. Another mod
that moves hunger after a skip would add to it. How it was measured and tested: `docs/modules/gluttony/ANALISE_BASE.html` (section 6)
and `tools/harness/skipcost/README.md`.
