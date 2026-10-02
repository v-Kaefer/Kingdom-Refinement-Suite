-- Entity used by the KRS test harness: Client:OnUpdate gives a per-frame hook (same pattern as the 30FPSCutsceneFix mod).
KRSHarness = {
    Client = {},
    Server = {},
    Properties = { bSaved_by_game = 0, Saved_by_game = 0, bSerialize = 0 },
    States = {},
}

function KRSHarness:OnReset()
    self:Activate(1)
    self.elapsed = 0
end

function KRSHarness.Server:OnInit()
    if not self.bInitialized then self:OnReset() self.bInitialized = 1 end
end

function KRSHarness.Client:OnInit()
    if not self.bInitialized then self:OnReset() self.bInitialized = 1 end
    System.LogAlways("KRS_HARNESS entity client init")
end

function KRSHarness.Client:OnUpdate(frameTime)
    -- wait until the level has loaded and the player exists, then give the world a few seconds
    if player and player.soul then
        self.elapsed = (self.elapsed or 0) + frameTime
        if self.elapsed >= (KRS and KRS.stage2_after_s or 12) then
            if KRS and KRS.stage2 then KRS.stage2() end
        end
    end
end

function KRSHarness:OnPropertyChange() self:OnReset() end
