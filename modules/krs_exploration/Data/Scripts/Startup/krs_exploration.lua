-- KRS Exploration: small skill XP for exploring.
--   * reading a wayside shrine or cross for the first time gives 1 XP of the "reading" skill
--   * shooting down a nest gives 1 XP of the "weapon_bow" skill
-- Ideas from "Waystones Give XP" (1518) and "Shooting Nests Gives XP" (1519), both by CrEaToXx. The code is written for this module: it wraps the
-- game's own entity functions instead of replacing the game's script files, so a game update to those scripts is not undone.
-- Status: written, not yet run in the test game (see docs/engine/lua-and-constants.md for the patterns that are known to work at startup).

KRS_Exploration = KRS_Exploration or {}
local K = KRS_Exploration

K.READING_XP = 1      -- XP of "reading" for a shrine or cross read for the first time (provisional, depends on the suite's XP curve)
K.BOW_XP = 1          -- XP of "weapon_bow" for a nest shot down (provisional)

local function log(msg)
	if System and System.LogAlways then
		System.LogAlways("[KRS_Exploration] " .. tostring(msg))
	end
end

function K.GrantXP(skill, amount)
	local ok, err = pcall(function()
		player.soul:AddSkillXP(skill, amount)
		RPG.NotifyLevelXpGain(skill)
	end)
	if not ok then
		log("could not give " .. tostring(skill) .. " XP: " .. tostring(err))
	end
end

-- Shrines and crosses: CaptionObject:OnUsed sets bDiscovered to true after the first reading, so the flag is read BEFORE the original runs.
local function wrapCaptionObject()
	if type(CaptionObject) ~= "table" or type(CaptionObject.OnUsed) ~= "function" then
		return false
	end
	if CaptionObject.KRS_wrapped then
		return true
	end
	local original = CaptionObject.OnUsed
	CaptionObject.OnUsed = function(self, ...)
		local first = (self.bDiscovered == false)
		local result = original(self, ...)
		if first then
			K.GrantXP("reading", K.READING_XP)
		end
		return result
	end
	CaptionObject.KRS_wrapped = true
	return true
end

-- Nests: Nest.Client:OnHit sets shotDown from 0 to 1 the first time the nest is hit; the XP is given on that change only.
local function wrapNest()
	if type(Nest) ~= "table" or type(Nest.Client) ~= "table" or type(Nest.Client.OnHit) ~= "function" then
		return false
	end
	if Nest.Client.KRS_wrapped then
		return true
	end
	local original = Nest.Client.OnHit
	Nest.Client.OnHit = function(self, hit)
		local before = self.shotDown
		local result = original(self, hit)
		if before == 0 and self.shotDown == 1 then
			K.GrantXP("weapon_bow", K.BOW_XP)
		end
		return result
	end
	Nest.Client.KRS_wrapped = true
	return true
end

function K.Install()
	local shrine = wrapCaptionObject()
	local nest = wrapNest()
	if shrine and not K.shrineLogged then
		K.shrineLogged = true
		log("shrine and cross XP installed")
	end
	if nest and not K.nestLogged then
		K.nestLogged = true
		log("nest XP installed")
	end
	return shrine and nest
end

-- The entity tables may not exist yet when this script runs: try now and again when the loading screen ends
-- (the listener pattern that is known to work, see the harness in tools/harness/krs_harness.lua).
KRS_Exploration_init = KRS_Exploration_init or {}
function KRS_Exploration_init:sceneInitListener(actionName, eventName, argTable)
	if actionName == "sys_loadingimagescreen" and eventName == "OnEnd" then
		local ok, err = pcall(K.Install)
		if not ok then
			log("install failed: " .. tostring(err))
		end
	end
end

pcall(K.Install)
if UIAction and UIAction.RegisterActionListener then
	UIAction.RegisterActionListener(KRS_Exploration_init, "", "", "sceneInitListener")
end
