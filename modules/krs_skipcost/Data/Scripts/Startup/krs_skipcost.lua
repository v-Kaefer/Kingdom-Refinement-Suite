-- KRS Skip Cost (prototype) - starter script.
--
-- The engine charges no hunger while the clock is skipped (Wait from the inventory, sleeping in a bed): measured in game. This mod takes
-- hunger off after a skip, as a share of what the same hours cost while awake. The share depends on the posture of the player during the
-- skip: standing (a Wait) KRS_SC_CFG.wait; sitting KRS_SC_CFG.sit; lying (sleeping, fainting, reading in a bed) KRS_SC_CFG.sleep.
-- Vigour and health are left to the engine.
-- The work is done by the entity KRSSkipCost (it gets a frame hook that startup scripts do not have); this script only makes sure one
-- of them is alive, and keeps the defaults that the builder overwrites (tools/harness/skipcost/build_skipcost.py).

KRS_SC_CFG = KRS_SC_CFG or {}
local cfg = KRS_SC_CFG
if cfg.wait == nil then cfg.wait = 0.75 end        -- share of the awake hunger cost charged for a Wait (standing)
if cfg.sit == nil then cfg.sit = 0.5 end           -- share charged for a skip made sitting (reading on a bench, a Wait on a chair)
if cfg.sleep == nil then cfg.sleep = 0.5 end       -- share charged for a skip made lying down (sleep, faint) or with vigour rising
if cfg.apply == nil then cfg.apply = 1 end         -- 0 only logs what would be charged

KRS_SC_Starter = {}
KRS_SC_Beat = 0          -- the entity that owns the work adds 1 on every frame it updates
KRS_SC_LastBeat = -1
KRS_SC_Spawns = 0

function KRS_SC_Starter:onAction(actionName, eventName, argTable)
    -- respawn the entity when its frame counter stopped moving since the previous UI event (a level change destroys it)
    if KRS_SC_Beat == KRS_SC_LastBeat and KRS_SC_Spawns < 40 then
        KRS_SC_Spawns = KRS_SC_Spawns + 1
        local ok, ent = pcall(System.SpawnEntity, { class = "KRSSkipCost", name = "KRSSkipCost_Instance" .. KRS_SC_Spawns })
        if not (ok and ent) then System.LogAlways("KRS_SC spawn " .. KRS_SC_Spawns .. " failed: " .. tostring(ent)) end
    end
    KRS_SC_LastBeat = KRS_SC_Beat
end

UIAction.RegisterActionListener(KRS_SC_Starter, "", "", "onAction")
System.LogAlways("KRS_SC startup script loaded")
