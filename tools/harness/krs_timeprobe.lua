-- KRS time probe starter: spawns the sampling entity and respawns it when it stops updating (a level change destroys it).
-- It also logs a sample on every UI action event (HUD and menu events keep firing in a loaded game), which is a fallback that does
-- not depend on the entity. Results go to kcd.log with the prefix KRS_TP.

KRS_TP_Starter = {}
KRS_TP_Events = 0
KRS_TP_Beat = 0          -- the entity increments it on every frame it updates
KRS_TP_LastBeat = -1
KRS_TP_Spawns = 0

local function cal(name)
    local f = Calendar and Calendar[name]
    if not f then return "nofunc" end
    local ok, v = pcall(f)
    if ok then return v end
    return "ERR"
end

local function hunger()
    if not (player and player.soul) then return "noplayer" end
    local ok, v = pcall(function() return player.soul:GetState("hunger") end)
    return ok and v or "ERR"
end

function KRS_TP_Starter:onAction(actionName, eventName, argTable)
    KRS_TP_Events = KRS_TP_Events + 1
    -- respawn the entity when its frame counter stopped moving since the previous event
    if KRS_TP_Beat == KRS_TP_LastBeat then
        KRS_TP_Spawns = KRS_TP_Spawns + 1
        local ok, ent = pcall(System.SpawnEntity, { class = "KRSTimeProbe", name = "KRSTimeProbe_Instance" .. KRS_TP_Spawns })
        if ok and ent then
            System.LogAlways("KRS_TP spawn " .. KRS_TP_Spawns .. " ok on action " .. tostring(actionName) .. "/" .. tostring(eventName))
        elseif KRS_TP_Spawns < 40 then
            System.LogAlways("KRS_TP spawn " .. KRS_TP_Spawns .. " failed: " .. tostring(ent))
        end
    end
    KRS_TP_LastBeat = KRS_TP_Beat
    if KRS_TP_Events <= 1500 then
        System.LogAlways(string.format("KRS_TP A %s/%s n=%d beat=%d player=%s wt=%s hr=%s ratio=%s paused=%s hunger=%s",
            tostring(actionName), tostring(eventName), KRS_TP_Events, KRS_TP_Beat, tostring(player and player.soul and 1 or 0),
            tostring(cal("GetWorldTime")), tostring(cal("GetWorldHourOfDay")), tostring(cal("GetWorldTimeRatio")), tostring(cal("IsWorldTimePaused")), tostring(hunger())))
    end
end

UIAction.RegisterActionListener(KRS_TP_Starter, "", "", "onAction")
System.LogAlways("KRS_TP startup script loaded")
