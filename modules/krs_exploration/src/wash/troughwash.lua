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
