TroughWash = TroughWash or {}
TroughWash.fx = 'WaterDroplets_Amount'
TroughWash.level = 0
TroughWash.fading = false
TroughWash.step = 0.05          -- per 100 ms -> 2.0 s from full to dry

function TroughWash.Tick()
  TroughWash.level = math.max(0, TroughWash.level - TroughWash.step)
  System.SetScreenFx(TroughWash.fx, TroughWash.level)
  if TroughWash.level > 0 then
    Script.SetTimer(100, TroughWash.Tick)
  else
    TroughWash.fading = false
  end
end

function TroughWash.Splash()
  TroughWash.level = 1
  System.SetScreenFx(TroughWash.fx, TroughWash.level)
  if not TroughWash.fading then
    TroughWash.fading = true
    Script.SetTimer(100, TroughWash.Tick)
  end
end

function TroughWash.Schedule()
  Script.SetTimer(1100, TroughWash.Splash)
  Script.SetTimer(2850, TroughWash.Splash)
end

-- Reshield (Nexus 2313, optional, shipped with krs_qol) puts the shield back when it stops seeing a torch. The wash takes the torch off
-- by itself and gives it back afterwards, so Reshield is paused for the length of the wash and put back as it was.
TroughWash.reshieldWas = nil

function TroughWash.Begin()
  if Reshield and TroughWash.reshieldWas == nil then
    TroughWash.reshieldWas = Reshield.enabled
    Reshield.enabled = false
  end
end

function TroughWash.End()
  -- a moment after the behaviour ends, so the torch is back in hand before Reshield looks again
  Script.SetTimer(1500, function()
    if Reshield and TroughWash.reshieldWas ~= nil then
      Reshield.enabled = TroughWash.reshieldWas
    end
    TroughWash.reshieldWas = nil
  end)
end
