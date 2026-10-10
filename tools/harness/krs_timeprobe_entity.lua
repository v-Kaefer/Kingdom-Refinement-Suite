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

-- mode "eat": set the hunger state once, then log every change of hunger/exhaust/stamina/health (so the effect of eating, sleeping or
-- waiting done by hand shows up with its size) and a full sample every 5 s; quits KRS_TP_RUN_S seconds after the hunger was set (the time spent in the menu does not count). Several copies of the
-- entity can be alive: the globals make sure the hunger is set once and each change is logged once.
function KRSTimeProbe:EatMode()
    if not (player and player.soul) then return end
    local now = (os and os.time) and os.time() or 0
    if not KRS_TP_T0 then KRS_TP_T0 = now log("EAT armed at os.time=" .. tostring(now)) end
    local el = now - KRS_TP_T0
    if el >= 10 and not KRS_TP_HungerSet then
        KRS_TP_HungerSet = true
        local ok, err = pcall(function() player.soul:SetState("hunger", KRS_TP_HUNGER or 60) end)
        log("SETSTATE hunger=" .. tostring(KRS_TP_HUNGER or 60) .. " ok=" .. tostring(ok) .. " err=" .. tostring(err) .. " readback=" .. tostring(st("hunger")))
        KRS_TP_SetAt = now
    end
    local h, e, sta, hp = st("hunger"), st("exhaust"), st("stamina"), st("health")
    local key = tostring(h) .. "|" .. tostring(e) .. "|" .. tostring(hp)
    if key ~= KRS_TP_LastKey then
        KRS_TP_LastKey = key
        log(string.format("CH el=%d hunger=%s exhaust=%s health=%s stamina=%s hr=%s", el, tostring(h), tostring(e), tostring(hp), tostring(sta), tostring(cal("GetWorldHourOfDay"))))
    end
    if now - (KRS_TP_LastFull or 0) >= 5 then
        KRS_TP_LastFull = now
        self:Sample("eat")
    end
    if KRS_TP_SetAt and now - KRS_TP_SetAt >= (KRS_TP_RUN_S or 480) then
        log("end")
        if System.Quit then System.Quit() else System.ExecuteCommand("quit") end
    end
end

-- mode "skip": the engine charges no hunger while the clock runs fast for a Wait or a sleep (measured). While one of those runs the
-- engine raises the world time ratio (15 -> 36.56 for a Wait) and speeds the frames up, so the skip is found from the ratio, not from
-- a jump in the clock. The world seconds that passed between the ratio going up and coming back are the skipped time. With
-- KRS_TP_APPLY = 1 the script then takes off hunger = awake rate x skipped seconds x factor (KRS_TP_FWAIT for a Wait, KRS_TP_FSLEEP
-- for sleep or a faint; reading is not charged), where the awake rate is measured live from the hunger bar between skips, so it follows
-- whatever DigestionSpeed the loaded mods set.
-- The kind of skip comes from KRS_TP_CtxType (set by the dialog event GetStatsSimulation if the UI listener sees it, or by the bed
-- trigger below): 0 Wait, 1 sleep, 2 faint, 3 read.
-- Test helpers: KRS_TP_HUNGER is set once KRS_TP_SETDELAY s after a save has loaded, and KRS_TP_BEDAT s after that the nearest Bed is
-- asked to put the player to sleep (the same call a held "use" on a bed makes). Several copies of the entity can be alive: only the
-- first one to see a given world time does the work.
KRS_SK = KRS_SK or { rate = nil, w0 = nil, h0 = nil, open = false, last_wt = nil, last_h = nil, last_e = nil, key = nil, owner = nil, base = nil, loaded_at = nil, set_done = false, bed_done = false }

local function nearest_bed()
    local best, bd, list = nil, 1e9, {}
    local ok, ents = pcall(System.GetEntitiesByClass, "Bed")
    if not (ok and type(ents) == "table") then return nil, "noents:" .. tostring(ents) end
    local pp = player:GetWorldPos()
    for _, e in pairs(ents) do
        local okp, ep = pcall(function() return e:GetWorldPos() end)
        if okp and ep and pp then
            local dx, dy, dz = ep.x - pp.x, ep.y - pp.y, ep.z - pp.z
            local d = math.sqrt(dx * dx + dy * dy + dz * dz)
            list[#list + 1] = string.format("%s d=%.1f type=%s q=%s", tostring(e:GetName()), d, tostring(e.Properties and e.Properties.Script and e.Properties.Script.esBedTypes), tostring(e.Properties and e.Properties.Bed and e.Properties.Bed.esSleepQuality))
            if d < bd then bd, best = d, e end
        end
    end
    table.sort(list)
    return best, string.format("n=%d nearest d=%.1f | %s", #list, bd, table.concat(list, " ; "):sub(1, 700))
end

function KRSTimeProbe:SkipMode(frameTime)
    if not (player and player.soul) then return end
    local wt = cal("GetWorldTime")
    if type(wt) ~= "number" then return end
    local K = KRS_SK
    local key = tostring(wt)
    if K.key == key and K.owner ~= self then return end
    K.key = key
    K.owner = self
    local h, e = st("hunger"), st("exhaust")
    local ratio = cal("GetWorldTimeRatio")
    if type(ratio) ~= "number" then ratio = 0 end
    local now = (os and os.time) and os.time() or 0
    if not KRS_TP_T0 then KRS_TP_T0 = now end
    if not K.rate then
        local ds = RPG and RPG.DigestionSpeed
        if type(ds) == "number" then K.rate = ds * 0.68 end
    end
    -- a save loading moves the clock by days in one frame: not a skip; start over
    if K.last_wt and (wt - K.last_wt > 100000 or wt < K.last_wt) then
        log(string.format("LOAD wt %s -> %s ratio=%s", tostring(K.last_wt), tostring(wt), tostring(ratio)))
        K.open, K.w0, K.h0, K.base, K.loaded_at, K.set_done, K.bed_done = false, nil, nil, nil, now, false, false
    end
    if not K.loaded_at and ratio > 0 and wt > 100000 then K.loaded_at = now end
    -- the normal ratio is the one seen while awake with the clock running and no skip going on
    if not K.base and ratio > 0 and K.loaded_at and now - K.loaded_at >= 3 then K.base = ratio log("BASE ratio=" .. tostring(ratio)) end
    if K.loaded_at and K.base then
        if not K.set_done and now - K.loaded_at >= (KRS_TP_SETDELAY or 20) then
            K.set_done = true
            local ok, err = pcall(function() player.soul:SetState("hunger", KRS_TP_HUNGER or 60) end)
            log("SETHUNGER " .. tostring(KRS_TP_HUNGER or 60) .. " ok=" .. tostring(ok) .. " readback=" .. tostring(st("hunger")))
            K.w0, K.h0 = nil, nil
            K.set_at = now
        end
        if K.set_done and not K.bed_done and KRS_TP_BEDAT and KRS_TP_BEDAT > 0 and now - K.set_at >= KRS_TP_BEDAT then
            K.bed_done = true
            local okb, bed, info = pcall(nearest_bed)
            if not okb then info = tostring(bed) bed = nil end
            log("BED " .. tostring(info))
            if bed then
                KRS_TP_CtxType = 1
                local ok, err = pcall(function() bed:OnUsedHold(player) end)
                log("BED OnUsedHold ok=" .. tostring(ok) .. " err=" .. tostring(err))
            end
        end
    end
    if K.base then
        local fast = ratio > K.base * 1.3
        if fast and not K.open then
            K.open = true
            K.start_wt, K.h_before, K.e_before, K.ctx_at_start = K.last_wt or wt, K.last_h, K.last_e, KRS_TP_CtxType
            log(string.format("SKIP start wt=%s hunger=%s exhaust=%s ctx=%s ratio=%s base=%s", tostring(K.start_wt), tostring(K.last_h), tostring(K.last_e), tostring(KRS_TP_CtxType), tostring(ratio), tostring(K.base)))
        elseif K.open and not fast then
            K.open = false
            local secs = wt - K.start_wt
            local ctx = K.ctx_at_start or KRS_TP_CtxType
            local factor = 0.75
            if ctx == 1 or ctx == 2 then factor = 0.5 elseif ctx == 3 then factor = 0 end
            if KRS_TP_FSLEEP and (ctx == 1 or ctx == 2) then factor = KRS_TP_FSLEEP end
            if KRS_TP_FWAIT and (ctx == 0 or ctx == nil) then factor = KRS_TP_FWAIT end
            local rate = K.rate or 0
            local cost = rate * secs * factor
            local hnow = tonumber(h) or 0
            log(string.format("SKIP end hours=%.3f ctx=%s ratio=%s hunger_before=%s hunger_after_engine=%s exhaust_before=%s exhaust_after=%s rate_per_h=%.4f factor=%s cost=%.3f", secs / 3600, tostring(ctx), tostring(ratio), tostring(K.h_before), tostring(h), tostring(K.e_before), tostring(e), rate * 3600, tostring(factor), cost))
            if KRS_TP_APPLY == 1 and cost > 0 then
                local target = math.max(0, hnow - cost)
                local ok, err = pcall(function() player.soul:SetState("hunger", target) end)
                log(string.format("APPLY hunger %s -> %s ok=%s err=%s readback=%s", tostring(hnow), tostring(target), tostring(ok), tostring(err), tostring(st("hunger"))))
                h = st("hunger")
            end
            KRS_TP_CtxType = nil
            K.w0, K.h0 = nil, nil
        elseif K.open then
            if not K.logged_fast or K.logged_fast < 6 then
                K.logged_fast = (K.logged_fast or 0) + 1
                log(string.format("SKIP frame wt=%s ratio=%s ft=%.2f hunger=%s exhaust=%s", tostring(wt), tostring(ratio), self.ft, tostring(h), tostring(e)))
            end
        else
            K.logged_fast = 0
            -- awake: measure the hunger rate over windows of at least 150 world seconds (the bar moves in steps of ~30 world seconds)
            if not K.w0 then K.w0, K.h0 = wt, tonumber(h)
            elseif wt - K.w0 >= 150 then
                local dh = K.h0 - (tonumber(h) or K.h0)
                if dh > 0 and dh < 1.5 then
                    K.rate = dh / (wt - K.w0)
                    log(string.format("RATE awake per_h=%.4f per_s=%.7f", K.rate * 3600, K.rate))
                end
                K.w0, K.h0 = wt, tonumber(h)
            end
        end
    end
    K.last_wt, K.last_h, K.last_e = wt, h, e
    if self.ft >= self.next_sample then self:Sample("skip") self.next_sample = self.ft + 10 end
    if now - KRS_TP_T0 >= (KRS_TP_RUN_S or 480) then
        log("end")
        if System.Quit then System.Quit() else System.ExecuteCommand("quit") end
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
    if KRS_TP_MODE == "eat" then self:EatMode() return end
    if KRS_TP_MODE == "skip" then self:SkipMode(frameTime) return end
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
