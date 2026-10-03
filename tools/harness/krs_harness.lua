-- KRS test harness: runs inside the game, writes everything to kcd.log with the prefix "KRS_HARNESS", then quits.
-- Nothing here changes saves or settings. It is loaded by the engine from Scripts/Startup/ (the way the
-- 30FPSCutsceneFix mod starts), so no Cheat mod is needed.
-- Script.SetTimer from a startup script never fired in the test instance, so it uses patterns that are proven to work:
-- a UIAction listener (menu / loading screen events) and a spawned entity with Client:OnUpdate.

KRS = KRS or {}
KRS.quit_after = true
KRS.stage2_after_s = 12       -- seconds after the player exists (world is settled by then)

local function log(msg) System.LogAlways("KRS_HARNESS " .. tostring(msg)) end

local function try(label, f, ...)
    local ok, a, b = pcall(f, ...)
    log(label .. " ok=" .. tostring(ok) .. " -> " .. tostring(a) .. (b ~= nil and (" | " .. tostring(b)) or ""))
    return ok, a, b
end

-- 1. which functions exist at run time (confirms docs/engine/lua-api-check.md) ---------------------------------------
function KRS.api()
    local names = {
        "System.GetEntitiesByClass", "System.GetEntityByName", "System.GetEntityByClass", "System.IsDevModeEnable",
        "System.IsDevMode", "System.Quit", "System.QuitInNSeconds", "System.ExecuteCommand", "System.GetCVar",
        "System.SetCVar", "Script.SetTimer", "Script.SetTimerForFunction", "Script.SetUpdateFunction",
        "Game.SetRPGParam", "Game.GetPlayer", "Database.GetTableInfo", "Database.GetTableLine",
        "Database.GetColumnInfo", "Database.GetTableColumnData", "RPG._GetConstant", "RPG._SetConstant",
        "UIAction.RegisterActionListener", "DatabaseUtils.LoadTableColumns",
    }
    for _, n in ipairs(names) do
        local obj, key = n:match("^([%w_]+)%.([%w_]+)$")
        local o = _G[obj]
        log("API " .. n .. " = " .. type(o and o[key]))
    end
    log("GLOBAL player=" .. type(player) .. " g_localActor=" .. type(g_localActor) .. " cheat=" .. type(cheat))
end

-- 2. read every known rpg constant (real 1.9.6 defaults, including the hidden ones) -------------------------------
function KRS.constants()
    for _, k in ipairs(KRS.keys or {}) do
        local ok, v = pcall(function() return RPG[k] end)
        log("CONST " .. k .. " = " .. (ok and tostring(v) or ("ERR " .. tostring(v))))
    end
end

-- 3. write test on two parameters ------------------------------------------------------------------------------------
function KRS.write_test()
    for _, k in ipairs({ "AimSpreadMax", "BowChargeDurationMax" }) do
        local before = RPG[k]
        local ok, err = pcall(function() RPG[k] = 40 end)
        local after = RPG[k]
        pcall(function() RPG[k] = before end)
        log("WRITE " .. k .. " before=" .. tostring(before) .. " set=40 ok=" .. tostring(ok) .. " err=" .. tostring(err)
            .. " after=" .. tostring(after) .. " restored=" .. tostring(RPG[k]))
    end
    local ok, err = pcall(function() RPG.ThisKeyDoesNotExist = 1 end)
    log("WRITE unknown key ok=" .. tostring(ok) .. " err=" .. tostring(err))
end

-- 4. read table rows through the Database API ----------------------------------------------------------------------
function KRS.row(tbl, key_column, key_value, wanted)
    local info = Database.GetTableInfo(tbl)
    local cols = {}
    for c = 0, info.ColumnCount - 1 do cols[Database.GetColumnInfo(tbl, c).Name] = c end
    local keys = Database.GetTableColumnData(tbl, cols[key_column])
    for i = 1, #keys do
        if tostring(keys[i]):lower() == key_value:lower() then
            local out = {}
            for _, w in ipairs(wanted) do
                local data = Database.GetTableColumnData(tbl, cols[w])
                out[#out + 1] = w .. "=" .. tostring(data[i])
            end
            return table.concat(out, " ")
        end
    end
    return "row not found"
end

function KRS.tables()
    for _, tbl in ipairs({ "potion", "item", "food", "rpg_param", "perk", "buff", "sleeping_spot_type", "document" }) do
        local ok, info = pcall(Database.GetTableInfo, tbl)
        log("COUNT " .. tbl .. " lines=" .. tostring(ok and info and info.LineCount) .. " cols=" .. tostring(ok and info and info.ColumnCount))
    end
    local seen = {}
    for _, t in ipairs(KRS.food_checks or {}) do
        local tbl = t.table or "food"
        if not seen[tbl] then
            seen[tbl] = true
            local info = Database.GetTableInfo(tbl)
            log("TABLE " .. tbl .. " LineCount=" .. tostring(info.LineCount) .. " ColumnCount=" .. tostring(info.ColumnCount))
        end
        log("ROW " .. t.label .. " :: " .. KRS.row(tbl, t.key or "item_id", t.id, t.cols))
    end
end

-- 5. player tests (need a loaded level) ------------------------------------------------------------------------------
function KRS.player()
    log("PLAYER global=" .. type(player) .. " soul=" .. type(player and player.soul) .. " human=" .. type(player and player.human))
    if player and player.soul then
        for _, st in ipairs({ "agi", "str", "vit", "spc", "cou" }) do
            try("GetStatLevel " .. st, function() return player.soul:GetStatLevel(st) end)
        end
        for _, st in ipairs({ "cha", "bad", "mor", "cap", "ble" }) do
            try("GetDerivedStat " .. st, function() return player.soul:GetDerivedStat(st) end)
        end
        try("GetState health", function() return player.soul:GetState("health") end)
    end
    if player and player.human then
        try("GetItemInHand(0)", function() return player.human:GetItemInHand(0) end)
        try("GetItemInHand(1)", function() return player.human:GetItemInHand(1) end)
    end
end

-- does a written constant change a value the engine computes later? (capacity = f(strength, StrengthToInventoryCapacity))
function KRS.live_test()
    if not (player and player.soul) then log("LIVE no player") return end
    local k = "StrengthToInventoryCapacity"
    local original = RPG[k]
    local cap0 = player.soul:GetDerivedStat("cap")
    RPG[k] = (tonumber(original) or 5) * 2
    local cap1 = player.soul:GetDerivedStat("cap")
    RPG[k] = original
    local cap2 = player.soul:GetDerivedStat("cap")
    log("LIVE " .. k .. " original=" .. tostring(original) .. " cap(before)=" .. tostring(cap0) .. " cap(x2)=" .. tostring(cap1)
        .. " cap(restored)=" .. tostring(cap2))
    for _, kk in ipairs({ "AimSpreadMax", "AimStamCost", "AimPainlessDelay", "BowChargeDurationMin", "BowChargeDurationMax", "BowPowerToChargeDuration" }) do
        log("LIVE bow constant " .. kk .. " = " .. tostring(RPG[kk]))
    end
end

function KRS.stage1()
    if KRS.stage1_done then return end
    KRS.stage1_done = true
    log("stage1 begin")
    try("api", KRS.api)
    try("constants", KRS.constants)
    try("write_test", KRS.write_test)
    try("tables", KRS.tables)
    if KRS.gate then try("gate menu", KRS.gate, "menu") end
    log("stage1 end")
end

function KRS.stage2()
    if KRS.stage2_done then return end
    KRS.stage2_done = true
    try("stage1", KRS.stage1)
    log("stage2 begin")
    try("player", KRS.player)
    try("live_test", KRS.live_test)
    if KRS.gate then try("gate player", KRS.gate, "player") end
    if KRS.extra_player then try("extra player", KRS.extra_player) end
    log("end")
    if KRS.quit_after then
        if System.Quit then System.Quit() else System.ExecuteCommand("quit") end
    end
end

-- start --------------------------------------------------------------------------------------------------------------
KRS_Starter = {}
KRS_Seen = {}
function KRS_Starter:onAction(actionName, eventName, argTable)
    local key = tostring(actionName) .. "/" .. tostring(eventName)
    if not KRS_Seen[key] and #KRS_Seen < 80 then
        KRS_Seen[key] = true
        log("ACTION " .. key)
    end
    -- tables and constants are loaded by the time the main menu starts. On 1.9.6 that is mm_main/OnStart; on 1.9.8 the
    -- main menu waits behind new start screens and never sends it, so sys_startup/OnEnd (level running) is accepted too.
    if KRS.mode == "tables" and not KRS.tables_done
        and ((actionName == "mm_main" and eventName == "OnStart") or (actionName == "sys_startup" and eventName == "OnEnd")) then
        KRS.tables_done = true
        log("tables stage triggered by " .. key)
        try("stage1", KRS.stage1)
        log("end")
        System.Quit()
    end
    -- full mode: spawn the update entity as soon as the entity system accepts it (retry on every action event)
    if KRS.mode ~= "tables" and not KRS.spawned then
        local ok, ent = pcall(System.SpawnEntity, { class = "KRSHarness", name = "KRSHarness_Instance" })
        if ok and ent then
            KRS.spawned = true
            log("spawn entity ok -> " .. tostring(ent) .. " on action " .. key)
        end
    end
end
UIAction.RegisterActionListener(KRS_Starter, "", "", "onAction")
log("startup script loaded")
