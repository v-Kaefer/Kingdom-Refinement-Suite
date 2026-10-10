-- KRS time probe entity: samples the world clock, the hunger state and the clock ratio, and writes KRS_TP lines to kcd.log.
-- It reads values and, once, sets the world time ratio to 2/3 of its value and puts it back (to see whether a script can change the
-- length of the day and whether the engine keeps it). It never saves, never changes the world time itself and quits at the end.
-- Same pattern as krs_harness_entity.lua: Client:OnUpdate gives a frame hook; Script.SetTimer from a startup script never fired.

KRSTimeProbe = {
    Client = {},
    Server = {},
    Properties = { bSaved_by_game = 0, Saved_by_game = 0, bSerialize = 0 },
    States = {},
}

local function log(m) System.LogAlways("KRS_TP " .. tostring(m)) end

local function cal(name, ...)
    local f = Calendar and Calendar[name]
    if not f then return "nofunc" end
    local ok, v = pcall(f, ...)
    if ok then return v end
    return "ERR:" .. tostring(v)
end

local function st(name)
    if not (player and player.soul) then return "noplayer" end
    local ok, v = pcall(function() return player.soul:GetState(name) end)
    if ok then return v end
    return "ERR"
end

local function clocks()
    local c, t = "nil", "nil"
    if os and os.clock then local ok, v = pcall(os.clock); c = ok and v or "ERR" end
    if os and os.time then local ok, v = pcall(os.time); t = ok and v or "ERR" end
    return c, t
end

function KRSTimeProbe:Sample(tag)
    local c, t = clocks()
    log(string.format("S %s ft=%.2f oc=%s ot=%s player=%s wt=%s hr=%s ratio=%s paused=%s hunger=%s exhaust=%s health=%s",
        tag, self.ft, tostring(c), tostring(t), tostring(player and player.soul and 1 or 0),
        tostring(cal("GetWorldTime")), tostring(cal("GetWorldHourOfDay")), tostring(cal("GetWorldTimeRatio")), tostring(cal("IsWorldTimePaused")),
        tostring(st("hunger")), tostring(st("exhaust")), tostring(st("health"))))
end

function KRSTimeProbe:Constants()
    for _, k in ipairs({ "DigestionSpeed", "ExhaustionSpeed", "FoodFull", "FoodOverEat", "StarvationThreshold", "StarvationHugeThreshold",
        "StarvationExtremeThreshold", "ShortTermNutritionDigestionSpeedMultiplier", "MetabolismDigestSpeed", "MetabolismAbsorbSpeed",
        "SleepHealthRegenBaseSpeed", "DefaultWorldTimeRatio", "StarvationHealthLossSpeed", "FoodHealSpeed", "StarvationPlayerEffectMinMin",
        "StarvationPlayerEffectMaxMin", "StarvationPlayerEffectMinMax", "StarvationPlayerEffectMaxMax", "BaseItemDisappearingTime" }) do
        local ok, v = pcall(function() return RPG[k] end)
        log("CONST " .. k .. " = " .. (ok and tostring(v) or ("ERR " .. tostring(v))))
    end
    for _, n in ipairs({ "hunger", "exhaust", "health", "stamina", "energy", "food", "nutrition", "fatigue" }) do
        log("STATE " .. n .. " = " .. tostring(st(n)))
    end
    for _, n in ipairs({ "GetWorldTime", "GetWorldHourOfDay", "GetGameTime", "GetWorldTimeRatio", "SetWorldTimeRatio", "IsWorldTimePaused" }) do
        log("CALFUNC " .. n .. " = " .. type(Calendar and Calendar[n]))
    end
    log("OS os=" .. type(os) .. " clock=" .. type(os and os.clock) .. " time=" .. type(os and os.time) .. " date=" .. type(os and os.date))
    for _, cv in ipairs({ "e_TimeOfDay", "e_TimeOfDaySpeed", "t_scale", "wh_game_time_ratio" }) do
        local ok, v = pcall(function() return System.GetCVar(cv) end)
        log("CVAR " .. cv .. " = " .. (ok and tostring(v) or "ERR"))
    end
end

function KRSTimeProbe:OnReset()
    self:Activate(1)
    self.ft = 0
    self.phase = "menu"
    self.phase_t = 0
    self.next_sample = 0
    self.last_hour = nil
    self.orig_ratio = nil
end

function KRSTimeProbe.Server:OnInit()
    if not self.bInitialized then self:OnReset() self.bInitialized = 1 end
end

function KRSTimeProbe.Client:OnInit()
    if not self.bInitialized then self:OnReset() self.bInitialized = 1 end
    log("entity client init")
end

function KRSTimeProbe:Go(phase)
    self.phase = phase
    self.phase_t = 0
    log("PHASE " .. phase .. " at ft=" .. string.format("%.2f", self.ft))
end

function KRSTimeProbe.Client:OnUpdate(frameTime)
    if not self.phase then self:OnReset() end
    KRS_TP_Beat = (KRS_TP_Beat or 0) + 1
    self.ft = self.ft + frameTime
    self.phase_t = self.phase_t + frameTime
    local hr = cal("GetWorldHourOfDay")
    if type(hr) == "number" then
        local h = math.floor(hr)
        if self.last_hour ~= nil and h ~= self.last_hour then
            local c, t = clocks()
            log(string.format("HOUR %d wt=%s ft=%.2f oc=%s ot=%s phase=%s", h, tostring(cal("GetWorldTime")), self.ft, tostring(c), tostring(t), self.phase))
        end
        self.last_hour = h
    end
    local havePlayer = player and player.soul
    if self.phase == "menu" then
        if self.ft >= self.next_sample and self.ft < 600 then self:Sample("menu") self.next_sample = self.ft + 3 end
        if havePlayer then self:Constants() self:Go("settle") end
    elseif self.phase == "settle" then
        if self.ft >= self.next_sample then self:Sample("settle") self.next_sample = self.ft + 3 end
        if self.phase_t >= 15 then self:Go("base") self.next_sample = 0 end
    elseif self.phase == "base" then
        if self.ft >= self.next_sample then self:Sample("base") self.next_sample = self.ft + 2 end
        if self.phase_t >= 150 then
            self.orig_ratio = cal("GetWorldTimeRatio")
            log("ORIG ratio=" .. tostring(self.orig_ratio))
            -- several copies of this entity can be alive (the starter respawns it after a level change): only the first one
            -- changes the ratio, and it remembers the value to put back
            if type(self.orig_ratio) == "number" and not KRS_TP_RatioDone then
                KRS_TP_RatioDone = true
                self.did_set = true
                local ok, err = pcall(Calendar.SetWorldTimeRatio, self.orig_ratio * 2 / 3)
                log("SET ratio=" .. tostring(self.orig_ratio * 2 / 3) .. " ok=" .. tostring(ok) .. " err=" .. tostring(err) .. " readback=" .. tostring(cal("GetWorldTimeRatio")))
            end
            self:Go("slow") self.next_sample = 0
        end
    elseif self.phase == "slow" then
        if self.ft >= self.next_sample then self:Sample("slow") self.next_sample = self.ft + 2 end
        if self.phase_t >= 60 then
            if self.did_set and type(self.orig_ratio) == "number" then
                local ok, err = pcall(Calendar.SetWorldTimeRatio, self.orig_ratio)
                log("RESTORE ratio=" .. tostring(self.orig_ratio) .. " ok=" .. tostring(ok) .. " err=" .. tostring(err) .. " readback=" .. tostring(cal("GetWorldTimeRatio")))
            end
            self:Go("restore") self.next_sample = 0
        end
    elseif self.phase == "restore" then
        if self.ft >= self.next_sample then self:Sample("restore") self.next_sample = self.ft + 2 end
        if self.phase_t >= 30 then
            self:Go("done")
            log("end")
            if System.Quit then System.Quit() else System.ExecuteCommand("quit") end
        end
    end
end

function KRSTimeProbe:OnPropertyChange() self:OnReset() end
