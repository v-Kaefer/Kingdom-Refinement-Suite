#!/usr/bin/env python3
"""
test_skipcost.py - syntax check and simulation of the krs_skipcost scripts outside the game, with Lua 5.1 (the game's Lua) from `lupa`.

    python -m venv <dir>; <dir>/Scripts/python -m pip install lupa        (a venv is enough: nothing else needs it)
    <dir>/Scripts/python tools/harness/skipcost/test_skipcost.py

What it does: loads the startup script and the entity script of modules/krs_skipcost into a Lua state that has fake versions of the
parts of the game they use (System, Calendar, os.time, player with a soul and a posture, RPG, UIAction), then feeds the entity frames
the way the engine did in the game logs (normal frames of 0.017 s; a Wait or sleep as a run of frames of 0.25 s with the clock moving
ratio x frame time) and checks what it charges. It proves the logic and the syntax; it does not prove that the engine behaves like the fake.
Exit code 1 when a check fails.
"""
import os
import sys

from lupa.lua51 import LuaRuntime

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
DATA = os.path.join(ROOT, "modules", "krs_skipcost", "Data", "Scripts")
START = os.path.join(DATA, "Startup", "krs_skipcost.lua")
ENT = os.path.join(DATA, "Entities", "KRSSkipCost.lua")

PRELUDE = r"""
LOG = {}
SPAWNED = {}
NOW = 1000          -- os.time()
WT = 4000000.0      -- world seconds
HUNGER = 60.0
EXHAUST = 99.0
POSTURE = "stand"
OSTIME_OK = true
RPG = { DigestionSpeed = 0.001302084, StarvationThreshold = 50 }
NOTES = {}
INFOS = {}
HAS_NOTIFY = true
HAS_INFO = true
Game = {
    ShowNotification = function(t) if not HAS_NOTIFY then error("no") end NOTES[#NOTES + 1] = t end,
    SendInfoText = function(t) if not HAS_INFO then error("no") end INFOS[#INFOS + 1] = t end,
}
System = {
    LogAlways = function(m) LOG[#LOG + 1] = m end,
    SpawnEntity = function(t) SPAWNED[#SPAWNED + 1] = t.name; return { name = t.name } end,
}
Calendar = { GetWorldTime = function() return WT end }
local real_os = os
os = { time = function() if OSTIME_OK then return NOW end return nil end, clock = real_os.clock }
player = {
    soul = {
        GetState = function(self, n) if n == "hunger" then return HUNGER elseif n == "exhaust" then return EXHAUST end end,
        SetState = function(self, n, v) if n == "hunger" then HUNGER = v end end,
    },
    player = {
        IsLaying = function() return POSTURE == "lay" end,
        IsSitting = function() return POSTURE == "sit" end,
    },
}
LISTENERS = {}
UIAction = { RegisterActionListener = function(obj, a, b, fn) LISTENERS[#LISTENERS + 1] = { obj = obj, fn = fn } end }
"""

DRIVER = r"""
ENTS = {}
function new_entity()
    local e = setmetatable({}, { __index = KRSSkipCost })
    ENTS[#ENTS + 1] = e
    e.Activate = function() end
    e.Client = KRSSkipCost.Client
    return e
end
function frame(e, ft, ratio)
    -- the clock moves by ratio x frame time, like the engine's
    WT = WT + ratio * ft
    KRSSkipCost.Client.OnUpdate(e, ft)
end
-- normal play: seconds of real time at 60 fps; hunger falls with the awake rate (per world second) in steps of 30 world seconds
STEP_ACC = 0
function play(e, real_secs, fps, rate_per_s)
    local ft = 1 / fps
    local n = math.floor(real_secs * fps)
    for i = 1, n do
        NOW = NOW + ft
        frame(e, ft, 15)
        STEP_ACC = STEP_ACC + 15 * ft
        if STEP_ACC >= 30 then STEP_ACC = STEP_ACC - 30; HUNGER = HUNGER - rate_per_s * 30 end
    end
end
-- a skip of `hours` world hours: long frames of 0.25 s with ratio x frame time; `real_secs` of real time
function fire_ui()
    local l = LISTENERS[1]
    l.obj[l.fn](l.obj, "hud", "OnStart", nil)
end
function skip(e, hours, ratio, real_secs)
    local secs = hours * 3600
    local ft = 0.25
    local d = ratio * ft
    local n = math.ceil(secs / d)
    for i = 1, n do
        NOW = NOW + real_secs / n
        frame(e, ft, ratio)
    end
end
"""


class Sim:
    def __init__(self):
        self.L = LuaRuntime(unpack_returned_tuples=True)
        self.L.execute(PRELUDE)
        for path in (START, ENT):
            src = open(path, encoding="utf-8").read()
            fn = self.L.eval("function(s, n) local f, e = loadstring(s, n) if not f then error(e) end return f end")(src, "@" + os.path.basename(path))
            fn()
        self.L.execute(DRIVER)
        self.g = self.L.globals()
        self.e = self.L.eval("new_entity")()

    def log(self):
        return [str(x) for x in self.g.LOG.values()]

    def skips(self):
        return [x for x in self.log() if "SKIP" in x]


fails = []


def check(name, cond, info=""):
    print(("ok   " if cond else "FAIL ") + name + (("  " + str(info)) if info else ""))
    if not cond:
        fails.append(name)


def num(line, key):
    import re
    m = re.search(key + r"=([-0-9.]+)", line)
    return float(m.group(1)) if m else None


def run():
    # 0. syntax of both files (loadstring succeeded in Sim()) and a clean start
    s = Sim()
    check("both scripts load (Lua 5.1 syntax)", True)
    check("startup script logged", any("startup script loaded" in x for x in s.log()))
    # 1. awake play: the rate is measured and nothing is charged
    awake_per_s = 0.0009130   # 3.287 per world hour
    s.L.execute("play(...)", s.e, 90, 60, awake_per_s) if False else s.g.play(s.e, 90, 60, awake_per_s)
    rates = [x for x in s.log() if "awake rate" in x or "prior rate" in x]
    check("prior rate from DigestionSpeed x 0.70", any("prior rate_per_h=3.2813" in x for x in rates), rates[:2])
    check("awake rate measured near 3.29 per hour", any("awake rate_per_h=3.2" in x or "awake rate_per_h=3.3" in x for x in rates), rates[-1:] )
    check("no skip charged while awake", not s.skips())

    # 2. Wait standing, 2 h, the engine's ratio and about 5.5 real seconds
    h0 = s.g.HUNGER
    s.g.skip(s.e, 2.0, 36.5625, 5.5)
    s.g.play(s.e, 3, 60, 0)    # normal frames close the skip
    sk = s.skips()
    check("Wait standing logged once", len(sk) == 1, sk)
    if sk:
        hours, cost, factor = num(sk[0], "hours"), num(sk[0], "cost"), num(sk[0], "factor")
        check("Wait hours near 2", abs(hours - 2.0) < 0.02, hours)
        check("Wait kind stand, factor 0.75", "kind=stand" in sk[0] and factor == 0.75, sk[0][:80])
        check("Wait cost = rate x hours x 0.75", abs(cost - 3.287 * hours * 0.75) < 0.1, cost)
        check("hunger lowered by the cost", abs((h0 - s.g.HUNGER) - cost) < 0.01, h0 - s.g.HUNGER)

    # 3. sleep lying, 6 h, ratio 58.125
    s.g.POSTURE = "lay"
    s.g.EXHAUST = 99.5
    s.g.play(s.e, 20, 60, awake_per_s)
    n0 = len(s.skips())
    s.g.skip(s.e, 6.0, 58.125, 14)
    s.g.EXHAUST = 100.0
    s.g.play(s.e, 3, 60, 0)
    sk = s.skips()
    check("sleep logged", len(sk) == n0 + 1)
    if len(sk) > n0:
        l = sk[-1]
        check("sleep kind lay, factor 0.5, hours near 6", "kind=lay" in l and num(l, "factor") == 0.5 and abs(num(l, "hours") - 6.0) < 0.05, l[:100])
        check("sleep cost = rate x hours x 0.5", abs(num(l, "cost") - num(l, "rate_per_h") * num(l, "hours") * 0.5) < 0.01, num(l, "cost"))

    # 4. sitting
    s.g.POSTURE = "sit"
    s.g.EXHAUST = 99.5
    s.g.play(s.e, 20, 60, awake_per_s)
    n0 = len(s.skips())
    s.g.skip(s.e, 3.0, 36.5625, 7)
    s.g.play(s.e, 3, 60, 0)
    sk = s.skips()
    check("sitting skip is charged 0.5", len(sk) == n0 + 1 and "kind=sit" in sk[-1] and num(sk[-1], "factor") == 0.5, sk[-1][:100] if sk else "")

    # 5. standing, vigour rising during the skip -> counted as lying
    s.g.POSTURE = "stand"
    s.g.EXHAUST = 90.0
    s.g.play(s.e, 20, 60, awake_per_s)
    n0 = len(s.skips())
    s.g.skip(s.e, 4.0, 36.5625, 6)
    s.g.EXHAUST = 95.0
    s.g.play(s.e, 3, 60, 0)
    sk = s.skips()
    check("vigour rise counts as lying", len(sk) == n0 + 1 and "kind=lay" in sk[-1], sk[-1][:100] if sk else "")

    # 6. R1: low frame rate play (5 fps, long frames, clock at ratio 15 in real time) is not a skip
    s.g.POSTURE = "stand"
    s.g.EXHAUST = 99.0
    n0 = len(s.skips())
    h0 = s.g.HUNGER
    s.g.play(s.e, 90, 5, awake_per_s)
    s.g.play(s.e, 3, 60, 0)
    check("R1: 90 s at 5 fps charges nothing", len(s.skips()) == n0 and abs(s.g.HUNGER - (h0 - awake_per_s * 15 * 90)) < 0.05, (len(s.skips()) - n0, h0 - s.g.HUNGER))

    # 7. R1: a real Wait right after slow play is still charged
    s.g.play(s.e, 20, 5, awake_per_s)
    n0 = len(s.skips())
    s.g.skip(s.e, 2.0, 36.5625, 5.5)
    s.g.play(s.e, 3, 60, 0)
    sk = s.skips()
    check("R1: a Wait after slow play is charged", len(sk) == n0 + 1 and abs(num(sk[-1], "hours") - 2.0) < 0.1, sk[-1][:100] if sk else "")

    # 8. a save loading moves the clock by days: not a skip
    n0 = len(s.skips())
    s.g.WT = s.g.WT + 4300000
    s.g.play(s.e, 3, 60, 0)
    check("a clock jump of days is not a skip", len(s.skips()) == n0)

    # 9. a short hitch is not a skip
    n0 = len(s.skips())
    s.L.execute("frame(...)", s.e, 0.4, 15) if False else s.g.frame(s.e, 0.4, 15)
    s.g.play(s.e, 3, 60, 0)
    check("one 0.4 s hitch is not a skip", len(s.skips()) == n0)

    # 10. without os.time the skip is still charged (no rate check possible) and nothing errors
    s2 = Sim()
    s2.g.OSTIME_OK = False
    s2.g.play(s2.e, 40, 60, awake_per_s)
    s2.g.skip(s2.e, 2.0, 36.5625, 5.5)
    s2.g.play(s2.e, 3, 60, 0)
    check("no os.time: still charged, no ERR", len(s2.skips()) == 1 and not any("ERR" in x for x in s2.log()), s2.log()[-2:])

    # 10b. the player is told what the skip cost
    s6 = Sim()
    s6.g.HUNGER = 80.0
    s6.g.play(s6.e, 40, 60, awake_per_s)
    s6.g.skip(s6.e, 2.0, 36.5625, 5.5)
    s6.g.play(s6.e, 3, 60, 0)
    notes = [str(x) for x in s6.g.NOTES.values()]
    check("notification after a Wait", len(notes) == 1 and notes[0].startswith("Waited 2.0 h: hunger -5") and "hungry" not in notes[0], notes)
    s6.g.HUNGER = 52.0
    s6.g.POSTURE = "lay"
    s6.g.play(s6.e, 20, 60, 0)
    s6.g.skip(s6.e, 6.0, 58.125, 14)
    s6.g.play(s6.e, 3, 60, 0)
    notes = [str(x) for x in s6.g.NOTES.values()]
    check("notification says Slept and hungry when it ends under the threshold", len(notes) == 2 and notes[1].startswith("Slept 6.0 h") and "(you are hungry)" in notes[1], notes[1:])
    s6.g.HUNGER = 3.0
    s6.g.POSTURE = "sit"
    s6.g.play(s6.e, 20, 60, 0)
    s6.g.skip(s6.e, 3.0, 36.5625, 7)
    s6.g.play(s6.e, 3, 60, 0)
    notes = [str(x) for x in s6.g.NOTES.values()]
    check("notification says starving when the skip empties the bar", len(notes) == 3 and notes[2].startswith("Rested 3.0 h") and "(starving)" in notes[2] and s6.g.HUNGER == 0, notes[2:])
    s7 = Sim()
    s7.g.HAS_NOTIFY = False
    s7.g.play(s7.e, 40, 60, awake_per_s)
    s7.g.skip(s7.e, 2.0, 36.5625, 5.5)
    s7.g.play(s7.e, 3, 60, 0)
    check("if ShowNotification fails the info line is used", len(s7.g.NOTES) == 0 and len(s7.g.INFOS) == 1 and len(s7.skips()) == 1)
    s8 = Sim()
    s8.L.execute("Game = nil")
    s8.g.play(s8.e, 40, 60, awake_per_s)
    s8.g.skip(s8.e, 2.0, 36.5625, 5.5)
    s8.g.play(s8.e, 3, 60, 0)
    check("with no Game table the skip is still charged and nothing errors", len(s8.skips()) == 1 and not any("ERR" in x for x in s8.log()))
    s9 = Sim()
    s9.L.execute("KRS_SC_CFG.notify = 0")
    s9.g.play(s9.e, 40, 60, awake_per_s)
    s9.g.skip(s9.e, 2.0, 36.5625, 5.5)
    s9.g.play(s9.e, 3, 60, 0)
    check("notify = 0 stays silent", len(s9.g.NOTES) == 0 and len(s9.g.INFOS) == 0 and len(s9.skips()) == 1)

    # 11. R2: the starter respawns the entity at most once every 10 real seconds
    s3 = Sim()
    fire = s3.g.fire_ui
    s3.g.NOW = 5000
    for i in range(50):          # 50 UI events in the same second, the entity never updates
        fire()
    check("R2: 50 events in one second spawn one entity", len(s3.g.SPAWNED) == 1, len(s3.g.SPAWNED))
    s3.g.NOW = 5011
    fire(); fire()
    check("R2: after 10 s one more spawn", len(s3.g.SPAWNED) == 2, len(s3.g.SPAWNED))
    for t in range(5020, 5020 + 600, 10):     # 10 minutes of paused game with events every 10 s
        s3.g.NOW = t
        fire()
    check("R2: no cap that ends respawning (spawns keep happening)", len(s3.g.SPAWNED) > 40, len(s3.g.SPAWNED))
    # when the entity is alive (beat moves) nothing is spawned
    n = len(s3.g.SPAWNED)
    s3.g.KRS_SC_Beat = s3.g.KRS_SC_Beat + 1
    s3.g.NOW = 9000
    fire()
    check("R2: a living entity is not respawned", len(s3.g.SPAWNED) == n)
    s4 = Sim()
    s4.g.OSTIME_OK = False
    for i in range(100):
        s4.g.fire_ui()
    check("R2: without os.time the respawns are capped at 40", len(s4.g.SPAWNED) == 40, len(s4.g.SPAWNED))

    # 12. the entity copy that is not the owner does nothing, and takes over when the owner stops
    s5 = Sim()
    e2 = s5.L.eval("new_entity")()
    s5.g.play(s5.e, 5, 60, 0)
    for i in range(3):
        s5.g.frame(e2, 0.017, 15)
    check("a second copy waits while the owner works", s5.L.eval("KRS_SC_Owner == ENTS[1]"))
    for i in range(6):
        s5.g.frame(e2, 0.017, 15)
    check("a second copy takes over when the owner stops", s5.L.eval("KRS_SC_Owner == ENTS[2]"))

    print()
    if fails:
        print("FAILED:", ", ".join(fails))
        return 1
    print("all checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(run())
