# Dynamic bow mechanics - what the tools can and cannot do

Question: can the hidden parameters and the Lua "hack tools" be used to change how the bow works
(e.g. aim spread and aiming stamina depending on Agility, Strength and bow weight)?

**Short answer:** yes for the parameters, and by design; the earlier attempts failed on the Lua *plumbing*
(wrong player handle, wrong stat API, a function that does not exist), not on the idea. The one thing that is
still unproven is whether the bow code re-reads a parameter every time it aims. A 10-minute in-game test
decides that (section 6).

Evidence comes from the game replica in `Mods WIP folder/KingdomComeDeliverance` (game build `ver_01_09_598307_726_master`,
i.e. 1.9.6): the 47 saved logs in `logbackups/`, the engine DLL strings, the Lua dump shipped with the Cheat mod
(`Mods/Cheat/Data/Docs/table_dump.txt`) and the game's own `Scripts*.pak`. Nothing was run in the game for this
document.

## 1. Verdict

| Capability | Verdict | Evidence |
|---|---|---|
| Change a hidden parameter statically (PTF `rpg_param` row) | **Works** | Immersive Archery ships `BowChargeDurationMin/Max`, `BowPowerToChargeDuration`, `AimSpreadSkillDecrease`, `AimPainlessDelay` as new rows; Parameters Plus carries 425 hidden keys in a full `rpg_param` file. See `docs/table-audit/TABLE_AUDIT.md` |
| Change a parameter while the game runs (Lua) | **Supported by the engine, never executed in your runs** | `rpgmodule.dll` / `WHGame.dll` contain `setmetatable(RPG, {__index=RPG._GetConstant, __newindex=RPG._SetConstant})` and the native message `Setting RPG constant/param key=%s to val=%f` (error: `no such rpg constant '%s'`). So `RPG.AimSpreadMax = 10` is the intended call |
| Read a parameter from Lua | **Works** | Vanilla Lua does it: `RPG.MoraleForCombat` in `sb_combat.xml`. Your logs show the same path rejecting unknown names: `no such rpg constant 'GetStat'` |
| Read Agility / Strength | **Works, with the right API** | Vanilla and the Cheat mod use `player.soul:GetStatLevel('agi')`, `'str'`, `'vit'`, `'cou'`, and `player.soul:GetDerivedStat('cha')` |
| Load your Lua **without the Cheat mod** | **Works** | The engine itself runs `scripts/main.lua` of every enabled mod (log: `Loading and executing script file 'scripts/main.lua'` followed by `mods/dynamic_bow_stats/data/scripts/main.lua: 2` in the stack) and every `Scripts/Startup/*.lua` (`fpsfix_mod_startup.lua`). See section 8 |
| Run code repeatedly | **Works, but not with the function you used** | `Script.SetUpdateFunction` does not exist. Existing options: `Script.SetTimer(ms, fn)` (one shot, re-arm it), `Script.SetTimerForFunction`, or a spawned entity with `Client:OnUpdate` (the 30FPSCutsceneFix mod does this in 1.9.6) |
| Bow *weight* from Lua | **Partly verified** | The held item can be reached with `player.human:GetItemInHand(0)` (used in `Crime.lua`). `GetRPGParam("ItemWeight")`, `inventory:GetEquippedItem` and `player:GetCurrentWeapon` appear nowhere (guesses). Weight is stored in `pickable_item`; the Lua accessor for it has not been found |
| Make the change per actor (player only) | **Probably not** | Constants are global (`S_Constants`). NPC archers would read the same value unless the parameter is player-only. Untested |
| Invent new mechanics that need engine code | **No** | Only what the existing parameters, buffs and perks can express |

## 2. Why the attempts failed (from the logs)

| Attempt (log, 2025) | What happened | Cause |
|---|---|---|
| 01 Jun 22:08 | `dynamic_bow_stats.lua:19: attempt to call field 'GetPlayer' (a nil value)` | `GetPlayer` is not a member of the table it was called on (probably `System`: the `System` dump has no such member) |
| 01 Jun 23:14 - 23:40 | Mod loads, `bow_debug` prints `Calculated AimSpreadMax: 10` with `Player Agility: 10` | 10/10 is exactly the script's **fallback**; from 02 Jun 01:35 the log says `All methods failed, using fallback values`. Treat the earlier numbers as fallback output, not real stats |
| 02 Jun 01:35 onwards | `DEBUG: Player 'dude' not found` in every later run | The player is not reachable by that name. The game exposes a global `player` (`player.soul`, `player.actor`, `player.inventory`) |
| 02 Jun 01:51 | Structure dump: `actor.__this = [userdata]`, only `RPG._SetConstant`, `RPG._GetConstant`, `RPG.AddStatXP`... listed | Properties like `soul.agility` do not exist; stats are methods |
| 03 Jun (several) | `no such rpg constant 'GetStat'`, `'GetPlayerStat'`, `'GetAttribute'`, `'GetStatValue'` | `RPG.<name>` is a *constant lookup*, not a method table. This also confirms the metatable is active |
| 03 Jun | `Failed to load script file Scripts/player_stats_reader.lua`, `attempt to call global 'player_stats_debug' (a nil value)` | MinimalModTools script path and global names did not match what was loaded |
| all | `Script.SetUpdateFunction` | Not a member of the `Script` table |
| all | **`Setting RPG constant/param key=AimSpreadMax` never appears in any log** | `ApplyDynamicBowStats()` returns early when the player is nil, so the key step (writing the constant) was **never executed** |

So the open question is exactly one line: does `RPG.AimSpreadMax = x` take effect on the next aim?

## 3. What a working script has to look like (sketch, untested)

```lua
-- 1. start after the level is loaded (pattern used by the 30FPSCutsceneFix mod)
BowMod = {}
function BowMod:onScene(actionName, eventName, argTable)
  if actionName == "sys_loadingimagescreen" and eventName == "OnEnd" then BowMod:tick() end
end
UIAction.RegisterActionListener(BowMod, "", "", "onScene")

-- 2. re-arm a timer; Script.SetTimer(ms, fn) is used this way in AIBase.lua
function BowMod:tick()
  if player and player.soul then
    local agi = player.soul:GetStatLevel('agi')
    local str = player.soul:GetStatLevel('str')
    RPG.AimSpreadMax = 15 - 10 * math.min(agi, 20) / 20      -- natives log "Setting RPG constant/param ..."
    RPG.AimStamCost  = 20 - 10 * math.min(str, 20) / 20
  end
  Script.SetTimer(1000, function() BowMod:tick() end)
end
```

Constants reset when the game restarts, so the script has to re-apply them on every load.

## 4. Data-only alternative (no Lua)

`perk_rpg_param_override (perk_id, rpg_param_key, rpg_param_value)` overrides parameters while a perk is active.
In vanilla it is used by exactly one pseudo-perk, **"Hardcore Mode - Constants"** (perk `01c3b32a-...`, 25 keys
including the ranged one `RangedWpnSelfHarmCoef`), so the mechanism accepts ranged parameters. A set of hidden
perks that auto-learn at Agility/Strength thresholds and override `AimSpreadMax`/`AimStamCost` would give a stepwise
version of the same idea. Whether the engine honours an override for every key is **unverified**.
Side effect to know: the repair values in `perk_rpg_param_override` (0.5 / 0.7 / 0.9) are *Hardcore-mode* values;
in normal mode the global `rpg_param` values (`RepairPriceModif` 0.65) apply.

Buffs are the third route: the `buff.params` column is an expression language (`weapon_bow+5`, `wat*1.1`,
`health+100/t`) that the potions already use, e.g. Bowman's Brew gives `weapon_bow+5`.

## 5. Parameter reference for the bow

Sources: `Params Reference.md` (hidden parameters exported from the engine), strings in `rpgmodule.dll`, and the
values listed by Parameters Plus (a 2019 dump of all constants) and Immersive Archery. `hidden` = not in the vanilla
`rpg_param` table, so it only exists in the engine and in these dumps. Descriptions come from the DLL where they
could be matched.

| Key | Meaning | Default (hidden = from Parameters Plus) | Immersive Archery |
|---|---|---|---|
| `AimSpreadMax` | [deg] aim spread due to low stamina and skill; the maximum angle, used just before all stamina is lost | 15 (in vanilla table) | - |
| `AimStamCost` | stamina lost per second after the painless delay | 20 (in vanilla table) | 15 |
| `AimPainlessDelay` | seconds of aiming without stamina loss | 2 hidden | 5 |
| `AimSpreadMinRatio` | spread right after entering the painless zone, relative to the max | 0.3 hidden | - |
| `AimSpreadSkillDecrease` | relative decrease of the maximum spread per skill level | 0.05 hidden | 0.058 |
| `ForcedFireAimSpreadMalus` | spread added when firing is forced on low stamina | 7 hidden | - |
| `AimZoomBase` / `AimZoomBaseSkill` | zoom (FOV decrease) at some skill level / minimum skill for the zoom | 10 / 10 hidden | - |
| `AimZoomMax` / `AimSkillToZoom` | maximum zoom / zoom gained per skill level above the base | 25 / 1.5 hidden | - |
| `AimCiriticalLimitTime` | time after which the AI is told the shooter is low on stamina | 0.75 hidden | - |
| `BowChargeDurationMin` | minimum bow-charge animation time | 1.35 hidden | 1.0 |
| `BowChargeDurationMax` | maximum bow-charge animation time | 3 hidden | 1.42 |
| `BowPowerToChargeDuration` | nominal charge time for power = 1 | 0.1 hidden | 0.062 |
| `RangedWpnPwrToSpeed` | total power to launch speed | 1 hidden | - |
| `RangedWpnMinPowerCoef` / `RangedWpnMinStrCoef` / `RangedWpnPowerConstA` | power for a very weak shooter / strength-ratio floor / strength-to-power constant | 0.1 / 0.5 / 1.85 hidden | - |
| `RangedWpnSelfHarmCoef` | self-harm equation constant (overridden by Hardcore mode: 20.5) | 15 hidden | - |
| `ProjectileMaxBreakProb` | arrow break chance on a rock-solid hit | 0.7 hidden | - |
| `MaxStatToAttackStaminaCostMult`, `StamDamage`, `BaseAttackStaminaCost` | generic combat stamina | 2 / 8 / 12 (in vanilla table) | - |

Known problem in `Params Reference.md`: some descriptions are shifted by one row (for example `AimSpreadMax` carries
"[s/m] attack mod deduced from impact speed", which belongs to a neighbouring key; the DLL says "[deg] ... max angle
... before all the stamina is lost"). Treat the file as a key list and check the meaning in the DLL or in game.

The nine rows under "Possible variables for my bow mod" in `rpg_param__KRS.xml` are all vanilla values, so they change
nothing; they are the table-backed subset of the list above.

## 6. Test that settles it (in game, Cheat mod loaded)

1. Open the console and run `cheat_eval RPG.AimSpreadMax = 40`.
2. Check the log for `Setting RPG constant/param key=AimSpreadMax to val=40.000000`. An `[Error] no such rpg constant`
   means the name is not registered.
3. Draw a bow and watch the reticle. A visibly wider spread means the bow code reads the value live. No change means
   it is cached; then only the PTF/perk route is left.
4. `cheat_eval cheat:logInfo(tostring(player.soul:GetStatLevel('agi')))` confirms the stat API.
5. Repeat with an NPC archer nearby to see whether the change is global.

## 7. Open points

- Result of the test in section 6 (live read, persistence across save/load, NPC impact).
- A Lua accessor for the equipped bow's weight.
- Whether `perk_rpg_param_override` accepts the aim keys.
- Parameters Plus is from 2019; its hidden defaults should be re-checked against the 1.9.6 DLL (the DLL registers the
  keys, the numeric defaults are not in readable strings).

## 8. Do you need the Cheat mod?

No. The Cheat mod was only a convenience here.

| What | Needs the Cheat mod? | Evidence |
|---|---|---|
| Running your script at startup | **No** | `Scripts/main.lua` and `Scripts/Startup/*.lua` of any mod are executed by the engine. In `logbackups/KCD Build(1) 01 Jun 25 (22 08 03).log` the bow script was loaded by the mod's own `main.lua`, not by the Cheat mod |
| `RPG.Key = value` | **No** | It is the engine's `RPG` metatable (`_SetConstant`), not a Cheat function |
| Reading stats (`player.soul:GetStatLevel`) | **No** | Used by the game's own scripts (29 times) |
| Typing test commands in the console | **No, but the syntax matters** | The game's own test scripts run Lua from the console with a leading `#` (`#a = player.soul:GetDerivedStat("cha")`). Your log shows `Unknown command: bow_debug`: a Lua function typed without `#` is treated as a console command. The Cheat mod adds `cheat_eval <lua>` as a wrapper |
| `cheat:` helper functions, `cheat.player` namespace (what MinimalModTools v1.1 used) | **Yes** | Provided by the Cheat mod; avoid them in the final mod |
| Seeing the result (log lines) | **No** | `System.LogAlways(...)` and the native `Setting RPG constant/param ...` line go to `kcd.log` |

The console itself must be enabled (the game was run with the dev console available in your logs). A shipped mod
should have no dependency on the Cheat mod.

## 9. The names that did not exist

`tools/lua_api_check.py` compares every call in the three bow/stats scripts with the game's own Lua, the live table dump
and the parameter lists; the result is in `API_CHECK.md`. Summary (the scripts were written for an earlier game build or
guessed):

| Call used | Result | Use instead |
|---|---|---|
| `System.GetEntityByName("dude")` | the function exists (2991 uses), but **"dude" is not a vanilla entity name** (0 uses) | the global `player` (also `g_localActor`) |
| `System.GetEntityByClass`, `System.IsDevMode`, `Game.GetPlayer`, `Game.SetRPGParam`, `Script.SetUpdateFunction` | not found anywhere | `System.GetEntitiesByClass`, `System.IsDevModeEnable`, `player`, `RPG.<Key> = v`, `Script.SetTimer` |
| `soul:GetStat`, `soul:GetAttribute`, `player.rpgStats:GetValue`, `soul.agility` | not found | `player.soul:GetStatLevel('agi')` (exists, 29 uses) |
| `GetRPGParam("ItemWeight")`, `inventory:GetEquippedItem`, `player:GetCurrentWeapon` | not found | `player.human:GetItemInHand(0)`, then find the weight accessor |
| `RPG.AimSpreadMax`, `RPG.AimStamCost` | valid parameter names | - |

So the parameters you picked exist; the functions around them did not. Run the tool on any new script before testing
in game:

```bash
python tools/lua_api_check.py --game "<KCD folder>" --params-ref "Params Reference.md" --out docs/bow/API_CHECK.md my_script.lua
```
