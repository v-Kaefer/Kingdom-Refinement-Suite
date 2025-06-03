-- Kingdom Come: Deliverance v1.9.6 - Player Stats Reader
-- File: player_stats_reader.lua
-- Version: 1.1.0 (Enhanced Debug)

-- Initialize in mmt namespace
if not mmt then mmt = {} end
if not mmt.player then mmt.player = {} end

local PlayerStatsReader = mmt.player

-- Debug configuration
local DEBUG_MODE = true -- Set to true to enable verbose logging
local DEBUG_STATS = false -- Set to true to log stat retrievals

-- Cache for performance
local statsCache = {
    lastUpdate = 0,
    updateInterval = 0.5,
    cachedStats = {}
}

-- Debug logging function
local function DebugLog(message, level)
    if not DEBUG_MODE then return end
    level = level or "INFO"
    if System and System.LogAlways then
        System.LogAlways("[PLAYER_STATS][" .. level .. "] " .. tostring(message))
    end
end

-- Get player entity with fallback methods
function PlayerStatsReader.GetPlayerEntity()
    local player = nil
    
    -- Method 1: Global player
    if _G.player and type(_G.player) == "table" and _G.player.soul then
        DebugLog("Found player via global _G.player")
        return _G.player
    end
    
    -- Method 2: Standard KCD method
    if System and System.GetEntityByName then
        player = System.GetEntityByName("dude")
        if player and player.soul then 
            DebugLog("Found player via System.GetEntityByName('dude')")
            return player 
        end
    end
    
    -- Method 3: GetEntityByClass
    if System and System.GetEntityByClass then
        player = System.GetEntityByClass("Player")
        if player and player.soul then 
            DebugLog("Found player via System.GetEntityByClass('Player')")
            return player 
        end
    end
    
    -- Method 4: Game.GetPlayer
    if Game and Game.GetPlayer then
        player = Game.GetPlayer()
        if player and player.soul then 
            DebugLog("Found player via Game.GetPlayer()")
            return player 
        end
    end
    
    DebugLog("No player entity found!", "WARN")
    return nil
end

-- Get player soul component
function PlayerStatsReader.GetPlayerSoul()
    local player = PlayerStatsReader.GetPlayerEntity()
    if player and player.soul then
        DebugLog("Soul component found")
        return player.soul
    end
    DebugLog("No soul component found!", "WARN")
    return nil
end

-- Get specific stat value
function PlayerStatsReader.GetStatValue(statName)
    if not statName or type(statName) ~= "string" then 
        DebugLog("Invalid stat name: " .. tostring(statName), "ERROR")
        return nil 
    end
    
    local soul = PlayerStatsReader.GetPlayerSoul()
    if not soul then return nil end
    
    local value = nil
    
    -- Try direct property access (lowercase)
    if soul[statName] and type(soul[statName]) == "number" then
        value = soul[statName]
        if DEBUG_STATS then DebugLog("Got " .. statName .. " = " .. value .. " (direct lowercase)") end
        return value
    end
    
    -- Try capitalized
    local capitalizedName = statName:gsub("^%l", string.upper)
    if soul[capitalizedName] and type(soul[capitalizedName]) == "number" then
        value = soul[capitalizedName]
        if DEBUG_STATS then DebugLog("Got " .. statName .. " = " .. value .. " (capitalized)") end
        return value
    end
    
    -- Try GetStatLevel (most reliable for main stats)
    if soul.GetStatLevel then
        local success, result = pcall(function() return soul:GetStatLevel(statName) end)
        if success and result and type(result) == "number" then
            if DEBUG_STATS then DebugLog("Got " .. statName .. " = " .. result .. " (GetStatLevel)") end
            return result
        end
    end
    
    -- Try GetStat
    if soul.GetStat then
        local success, result = pcall(function() return soul:GetStat(statName) end)
        if success and result and type(result) == "number" then
            if DEBUG_STATS then DebugLog("Got " .. statName .. " = " .. result .. " (GetStat)") end
            return result
        end
    end
    
    if DEBUG_STATS then DebugLog("Could not find stat: " .. statName, "WARN") end
    return nil
end

-- Get all player stats
function PlayerStatsReader.GetAllPlayerStats()
    local currentTime = System and System.GetCurrTime and System.GetCurrTime() or 0
    
    -- Use cache if recent
    if currentTime - statsCache.lastUpdate < statsCache.updateInterval and next(statsCache.cachedStats) ~= nil then
        DebugLog("Using cached stats")
        return statsCache.cachedStats
    end
    
    DebugLog("Refreshing player stats")
    
    local stats = {
        inGame = false,
        hasValidSoul = false
    }
    
    local player = PlayerStatsReader.GetPlayerEntity()
    if not player then return stats end
    
    local soul = PlayerStatsReader.GetPlayerSoul()
    if not soul then return stats end
    
    stats.inGame = true
    stats.hasValidSoul = true
    
    -- Primary stats (mmt mod naming)
    stats.str = PlayerStatsReader.GetStatValue("str") or 10
    stats.agi = PlayerStatsReader.GetStatValue("agi") or 10
    stats.vit = PlayerStatsReader.GetStatValue("vit") or 10
    stats.spc = PlayerStatsReader.GetStatValue("spc") or 10
    
    -- Alternative names for compatibility
    stats.strength = stats.str
    stats.agility = stats.agi
    stats.vitality = stats.vit
    stats.speech = stats.spc
    
    -- Combat skills
    local combatSkills = {"bow", "sword", "mace", "axe", "unarmed", "block", "dodge", "archery", "warfare", "defense"}
    for _, skill in ipairs(combatSkills) do
        stats[skill] = PlayerStatsReader.GetStatValue(skill) or 0
    end
    
    -- Other skills
    local otherSkills = {"horsemanship", "hunting", "herbalism", "alchemy", "reading", 
                        "pickpocketing", "lockpicking", "stealth", "drinking", 
                        "alpha_male", "burgher", "savage"}
    for _, skill in ipairs(otherSkills) do
        stats[skill] = PlayerStatsReader.GetStatValue(skill) or 0
    end
    
    -- Derived stats
    stats.level = PlayerStatsReader.GetStatValue("level") or 1
    stats.health = PlayerStatsReader.GetStatValue("health") or 100
    stats.stamina = PlayerStatsReader.GetStatValue("stamina") or 100
    stats.energy = PlayerStatsReader.GetStatValue("energy") or 100
    
    -- Update cache
    statsCache.lastUpdate = currentTime
    statsCache.cachedStats = stats
    
    DebugLog("Stats refreshed - Level: " .. stats.level .. ", STR: " .. stats.str)
    
    return stats
end

-- Simple debug info
function PlayerStatsReader.GetDebugInfo()
    local player = PlayerStatsReader.GetPlayerEntity()
    if not player then
        return "No player entity found"
    end
    
    local soul = PlayerStatsReader.GetPlayerSoul()
    local info = {
        "Player Entity: " .. tostring(player),
        "Soul Component: " .. tostring(soul),
        "In Game: " .. tostring(soul ~= nil)
    }
    
    if soul then
        -- Test a few key stats
        local testStats = {"str", "agi", "vit", "spc", "bow", "level"}
        info[#info + 1] = "Sample Stats:"
        for _, stat in ipairs(testStats) do
            local value = PlayerStatsReader.GetStatValue(stat)
            info[#info + 1] = "  " .. stat .. " = " .. tostring(value)
        end
    end
    
    return table.concat(info, "\n")
end

-- NEW: Performance debug info
function PlayerStatsReader.GetPerformanceInfo()
    local info = {
        "=== Performance Debug Info ===",
        "Cache Update Interval: " .. statsCache.updateInterval .. "s",
        "Last Cache Update: " .. statsCache.lastUpdate,
        "Cache Has Data: " .. tostring(next(statsCache.cachedStats) ~= nil)
    }
    
    if System and System.GetCurrTime then
        local currentTime = System.GetCurrTime()
        local timeSinceUpdate = currentTime - statsCache.lastUpdate
        info[#info + 1] = "Time Since Update: " .. string.format("%.2f", timeSinceUpdate) .. "s"
        info[#info + 1] = "Cache Valid: " .. tostring(timeSinceUpdate < statsCache.updateInterval)
    end
    
    return table.concat(info, "\n")
end

-- NEW: Enable/disable debug modes
function PlayerStatsReader.SetDebugMode(enabled, statsDebug)
    DEBUG_MODE = enabled or false
    DEBUG_STATS = statsDebug or false
    DebugLog("Debug mode: " .. tostring(DEBUG_MODE) .. ", Stats debug: " .. tostring(DEBUG_STATS))
end

-- Global functions for easy access (following mmt mod pattern)
mmt.GetPlayerStats = PlayerStatsReader.GetAllPlayerStats
mmt.GetPlayerStat = PlayerStatsReader.GetStatValue
mmt.GetPlayerDebugInfo = PlayerStatsReader.GetDebugInfo
mmt.GetPlayerPerformanceInfo = PlayerStatsReader.GetPerformanceInfo
mmt.SetStatsDebugMode = PlayerStatsReader.SetDebugMode

-- Also make them global for compatibility
GetPlayerStats = mmt.GetPlayerStats
GetPlayerStat = mmt.GetPlayerStat
GetPlayerDebugInfo = mmt.GetPlayerDebugInfo
GetPlayerPerformanceInfo = mmt.GetPlayerPerformanceInfo
SetStatsDebugMode = mmt.SetStatsDebugMode

-- Export the reader (following mmt mod pattern)
mmt.PlayerStatsAPI = PlayerStatsReader

-- Simple initialization message (following mmt mod pattern)
if System and System.LogAlways then
    System.LogAlways("Player Stats Reader v1.1.0 loaded - Functions available in mmt.player namespace")
    System.LogAlways("Global functions: GetPlayerStats(), GetPlayerStat(name), GetPlayerDebugInfo()")
    System.LogAlways("Debug functions: GetPlayerPerformanceInfo(), SetStatsDebugMode(debug, stats)")
end