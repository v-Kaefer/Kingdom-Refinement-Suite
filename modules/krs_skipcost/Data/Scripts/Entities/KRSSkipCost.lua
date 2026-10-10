-- KRS Skip Cost (prototype) - the entity that does the work. See krs_skipcost.lua for what the mod does.
--
-- How a skip is found (measured in game, docs/modules/gluttony/ANALISE_BASE.html): while a Wait or a sleep runs the engine feeds the
-- frame hook with frames of about 0.25 s (normal frames are 0.02 to 0.05 s) and the world clock moves by ratio x frame time, so the
-- skipped world seconds are the clock movement of those long frames. The clock ratio is not used: it differs with the hours chosen
-- and the last part of a skip runs at the normal ratio.
-- How the kind of skip is told: by the posture of the player while it runs (player.player:IsLaying() / IsSitting()). Sleeping, fainting
-- and reading all happen sitting or lying (a book can only be read on a bed or better), and a Wait is made standing. A skip during which
-- the vigour goes up by more than 0.05 also counts as lying down. No bed hook: a bed that was opened and cancelled leaves nothing behind.
-- The awake rate comes from the hunger bar itself (so it follows DigestionSpeed and perks), measured over windows of awake time.
-- Several copies of the entity can be alive: the one in KRS_SC_Owner does the work, the others wait and take over if it stops.

KRSSkipCost = {
    Client = {},
    Server = {},
    Properties = { bSaved_by_game = 0, Saved_by_game = 0, bSerialize = 0 },
    States = {},
}

local LONG_FRAME_MIN = 0.15   -- frame time (s) from which a frame counts as part of a skip
local LONG_FRAME_MAX = 2.0    -- above this it is a loading hitch, not a skip
local QUIET_FRAMES = 45       -- normal frames in a row that end a skip
local WINDOW_SECS = 300       -- world seconds of awake time per rate measurement
local MIN_SKIP_SECS = 120  -- world seconds below which a run of long frames is taken for a hitch
local PRIOR_SHARE = 0.70      -- hunger bar rate over the DigestionSpeed constant (measured 0.70)

local function log(m) System.LogAlways("KRS_SC " .. tostring(m)) end

local function state(name)
    if not (player and player.soul) then return nil end
    local ok, v = pcall(function() return player.soul:GetState(name) end)
    if ok and type(v) == "number" then return v end
    return nil
end

local function worldtime()
    local ok, v = pcall(Calendar.GetWorldTime)
    if ok and type(v) == "number" then return v end
    return nil
end

local function realtime()
    if os and os.time then
        local ok, v = pcall(os.time)
        if ok and type(v) == "number" then return v end
    end
    return 0
end

KRS_SC_K = KRS_SC_K or { open = false, secs = 0, frames = 0, quiet = 0, wt_prev = nil, w_secs = 0, w_h0 = nil, rate = nil, rest = nil }

local function truthy(v) return v == true or (type(v) == "number" and v ~= 0) end

-- "lay", "sit" or "stand"; nil when the player object does not answer
local function posture()
    if not (player and player.player) then return nil end
    local okl, lay = pcall(function() return player.player:IsLaying() end)
    if okl and truthy(lay) then return "lay" end
    local oks, sit = pcall(function() return player.player:IsSitting() end)
    if oks and truthy(sit) then return "sit" end
    if okl or oks then return "stand" end
    return nil
end

local function finish_skip(K, wt)
    local cfg = KRS_SC_CFG
    if K.secs < MIN_SKIP_SECS then
        -- a hitch in the frame time, not a skip
        K.open, K.secs, K.frames, K.quiet = false, 0, 0, 0
        return
    end
    local e_now = state("exhaust")
    local kind = K.pos or "stand"
    if kind == "stand" and K.e_start and e_now and e_now - K.e_start > 0.05 then kind = "lay" end
    local factor = cfg.wait
    if kind == "lay" then factor = cfg.sleep elseif kind == "sit" then factor = cfg.sit end
    local h_now = state("hunger")
    local rate = K.rate
    local cost = 0
    if rate and h_now then cost = rate * K.secs * factor end
    local target = h_now
    if cfg.apply == 1 and cost > 0 and h_now then
        target = math.max(0, h_now - cost)
        local ok, err = pcall(function() player.soul:SetState("hunger", target) end)
        if not ok then log("SetState failed: " .. tostring(err)) end
    end
    log(string.format("SKIP kind=%s hours=%.3f rate_per_h=%s factor=%s cost=%.3f hunger %s -> %s exhaust %s -> %s frames=%d",
        kind, K.secs / 3600, rate and string.format("%.4f", rate * 3600) or "unknown", tostring(factor), cost, tostring(h_now), tostring(target),
        tostring(K.e_start), tostring(e_now), K.frames))
    K.open, K.secs, K.frames, K.quiet = false, 0, 0, 0
    K.w_secs, K.w_h0 = 0, nil
end

function KRSSkipCost:Step(frameTime)
    local K = KRS_SC_K
    local wt = worldtime()
    local h = state("hunger")
    if not wt or not h then return end
    if K.rate == nil and not K.prior_done then
        K.prior_done = true
        local ok, ds = pcall(function() return RPG.DigestionSpeed end)
        if ok and type(ds) == "number" and ds > 0 then K.rate = ds * PRIOR_SHARE; log(string.format("prior rate_per_h=%.4f", K.rate * 3600)) end
    end
    local pnow = posture()
    if pnow ~= K.pos_seen then
        K.pos_seen = pnow
        log("posture " .. tostring(pnow))
    end
    local d = 0
    if K.wt_prev then d = wt - K.wt_prev end
    K.wt_prev = wt
    -- a save loading moves the clock by days (or back) in one frame: not a skip, start over
    if d < 0 or d > 100000 then
        K.open, K.secs, K.frames, K.quiet, K.w_secs, K.w_h0 = false, 0, 0, 0, 0, nil
        return
    end
    if d == 0 then return end
    if frameTime >= LONG_FRAME_MIN and frameTime <= LONG_FRAME_MAX then
        if not K.open then
            K.open = true
            K.secs, K.frames = 0, 0
            K.e_start = state("exhaust")
            K.pos = posture()
        end
        -- the posture is read again now and then: the player can lie down after the skip has begun
        if K.frames % 30 == 5 and K.pos ~= "lay" then
            local pp = posture()
            if pp == "lay" or (pp == "sit" and K.pos ~= "sit") then K.pos = pp end
        end
        K.secs = K.secs + d
        K.frames = K.frames + 1
        K.quiet = 0
        return
    end
    if K.open then
        K.quiet = K.quiet + 1
        if K.quiet >= QUIET_FRAMES then finish_skip(K, wt) end
        return
    end
    -- awake: measure the hunger rate over windows of WINDOW_SECS world seconds; a window with a flat bar (the bar stops for a while
    -- after a skip), a rise (eating) or a rate far from the current one is thrown away
    if not K.w_h0 then K.w_h0, K.w_secs = h, 0 end
    K.w_secs = K.w_secs + d
    if K.w_secs >= WINDOW_SECS then
        local dh = K.w_h0 - h
        if dh > 0 then
            local r = dh / K.w_secs
            if K.rate == nil or (r >= K.rate * 0.85 and r <= K.rate * 1.2) then
                K.rate = K.rate and (K.rate * 0.7 + r * 0.3) or r
                K.rate_n = (K.rate_n or 0) + 1
                K.cand, K.cand_n = nil, 0
                if K.rate_n <= 3 then log(string.format("awake rate_per_h=%.4f", K.rate * 3600)) end
            else
                -- far from the current rate: thrown away, unless 4 windows in a row agree with each other (a perk or another mod
                -- changed the real rate), then it becomes the rate
                if K.cand and math.abs(r - K.cand) <= 0.1 * K.cand then K.cand_n = (K.cand_n or 0) + 1 else K.cand, K.cand_n = r, 1 end
                if K.cand_n >= 4 then
                    K.rate, K.cand, K.cand_n = r, nil, 0
                    log(string.format("rate changed to rate_per_h=%.4f", r * 3600))
                end
            end
        end
        K.w_h0, K.w_secs = h, 0
    end
end

function KRSSkipCost:OnReset()
    self:Activate(1)
    self.stale = 0
    self.seen_stamp = nil
end

function KRSSkipCost.Server:OnInit()
    if not self.bInitialized then self:OnReset() self.bInitialized = 1 end
end

function KRSSkipCost.Client:OnInit()
    if not self.bInitialized then self:OnReset() self.bInitialized = 1 end
end

function KRSSkipCost.Client:OnUpdate(frameTime)
    if not self.stale then self:OnReset() end
    if KRS_SC_Owner ~= self then
        if KRS_SC_OwnerStamp == self.seen_stamp then self.stale = self.stale + 1 else self.stale = 0 end
        self.seen_stamp = KRS_SC_OwnerStamp
        if KRS_SC_Owner == nil or self.stale > 3 then
            KRS_SC_Owner = self
            self.stale = 0
            log("entity took over")
        else
            return
        end
    end
    KRS_SC_OwnerStamp = (KRS_SC_OwnerStamp or 0) + 1
    KRS_SC_Beat = KRS_SC_Beat + 1
    local ok, err = pcall(self.Step, self, frameTime)
    if not ok and not KRS_SC_ErrLogged then
        KRS_SC_ErrLogged = true
        log("ERR " .. tostring(err))
    end
end

function KRSSkipCost:OnPropertyChange() self:OnReset() end
