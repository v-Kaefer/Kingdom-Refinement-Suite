# Lua and hidden constants (measured)

> **Status date:** 2026-10-03 | **Kind:** engine | **Trust:** measured | **Game version:** 1.9.6

Measured on 1.9.6 (2 Oct 2026). The generated list of calls that exist is `lua-api-check.md`; every constant as the game reports it is `rpg_constants_runtime.csv`.

## 3. Lua and parameters (`run_full_api_stats_constants.log`)

| Observation | Result |
|---|---|
| The harness mod's `Scripts/Startup/*.lua`, a spawned entity and a UIAction listener run **without the Cheat mod** | works; `cheat` is `nil` |
| `Script.SetTimer` called from a startup script | **never fired** (use the listener / entity pattern) |
| `System.GetEntityByClass`, `System.IsDevMode`, `Script.SetUpdateFunction`, `Game.SetRPGParam`, `Game.GetPlayer` | `nil` (matches `docs/engine/lua-api-check.md`) |
| Global `player` (table with `soul`, `human`) and `g_localActor` | present once a save is loaded |
| `player.soul:GetStatLevel('agi'/'str'/'vit'/'spc'/'cou')`, `GetDerivedStat('cha'/'bad'/'mor'/'cap'/'ble')`, `GetState('health')` | work (test save: 15 / 13 / 9 / 14 / 16; capacity 153) |
| `player.human:GetItemInHand(0)` | callable; returns an empty handle when nothing is held |
| `RPG.AimSpreadMax = 40` and `RPG.BowChargeDurationMax = 40` | read back 40, restore worked |
| `RPG.ThisKeyDoesNotExist = 1` | no Lua error, but the engine logs `no such rpg constant` |
| 597 keys read from `Params Reference.md` + the vanilla table | **588 exist, 9 do not**: `AlcoholPerkLooseTongueSpcChaModif`, `AlcoholismTickInterval`, `DistanceCheckInterval`, `FoodTickInterval`, `ReadingRestEffectiveness`, `ReadingRestUpperLimit`, `TreasureItemPricee`, `UnarmedAttackBase`, `VigourTickInterval`. 406 of the 588 are hidden (not in the vanilla `rpg_param` table). Full list with real values: `docs/engine/rpg_constants_runtime.csv` |


## 3b. Not tested yet

- Whether the bow reads `AimSpreadMax`, `AimStamCost` and the `BowCharge*` constants **live** when aiming (needs a person
  or an automated input to load a save, equip a bow and draw). A first test of this kind (capacity changes when
  `StrengthToInventoryCapacity` is written) is in the harness but the instance stopped at the main menu in the last runs.
- Effects on NPC archers.
- Perk and buff tables (they are only loaded together with a level).

