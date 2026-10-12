-- KRS ADB test: at the main menu, reload the animation databases and list the referenced animation assets, then quit.
-- Used to check that a merged kcd_male_database.adb is accepted by the game (mn_reload parses the databases again; a malformed or
-- inconsistent file shows up as an engine error in kcd.log, a crash as a game that never reaches the end marker).
-- Nothing is saved; the game quits by itself. The marker "KRS_HARNESS end" is what tools/harness/run_game_test.ps1 waits for.

KRS_AdbTest = {}
KRS_AdbTest.done = false

local function log(msg)
	System.LogAlways("KRS_ADBTEST " .. tostring(msg))
end

local function run(cmd)
	log(cmd .. " begin")
	local ok, err = pcall(System.ExecuteCommand, cmd)
	log(cmd .. " end ok=" .. tostring(ok) .. (ok and "" or (" " .. tostring(err))))
end

function KRS_AdbTest:onAction(actionName, eventName, argTable)
	if self.done then
		return
	end
	-- on 1.9.8 the main menu waits behind new start screens; sys_startup/OnEnd is the first event after the level runs
	if (actionName == "sys_startup" and eventName == "OnEnd") or (actionName == "mm_main" and eventName == "OnStart") then
		self.done = true
		log("triggered by " .. actionName .. "/" .. eventName)
		run("mn_listAssets")
		run("mn_reload")
		run("mn_listAssets")
		System.LogAlways("KRS_HARNESS end")
		if System.Quit then
			System.Quit()
		else
			System.ExecuteCommand("quit")
		end
	end
end

UIAction.RegisterActionListener(KRS_AdbTest, "", "", "onAction")
log("startup script loaded")
