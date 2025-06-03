-- Kingdom Come: Deliverance v1.9.6 - Player Stats Reader
-- Minimal API for reading player stats only
-- File: player_stats_reader.lua
-- Version: 1.0.0

local PlayerStatsReader = {}

-- Cache for performance
local statsCache = {
    lastUpdate = 0,
    updateInterval = 0.5,
    cachedStats = {}
}

-- Get player entity with fallback methods
function PlayerStatsReader.GetPlayerEntity()
    local player = nil
    
    -- Method 1: Global player (from cheat mod)
    if _G.player and type(_G.player) == "table" and _G.player.soul then
        return _G.player
    end
    
    -- Method 2: Standard KCD method
    if System and System.GetEntityByName then
        player = System.GetEntityByName("dude")
        if player and player.soul then return player end
    end
    
    -- Method 3: GetEntityByClass
    if System and System.GetEntityByClass then
        player = System.GetEntityByClass("Player")
        if player and player.soul then return player end
    end
    
    -- Method 4: Game.GetPlayer
    if Game and Game.GetPlayer then
        player = Game.GetPlayer()
        if player and player.soul then return player end
    end
    
    return nil
end

-- Get player soul component
function PlayerStatsReader.GetPlayerSoul()
    local player = PlayerStatsReader.GetPlayerEntity()
    return player and player.soul or nil
end

-- Get specific stat value
function PlayerStatsReader.GetStatValue(statName)
    if not statName or type(statName) ~= "string" then return nil end
    
    local soul = PlayerStatsReader.GetPlayerSoul()
    if not soul then return nil end
    
    -- Try direct property access (lowercase)
    if soul[statName] and type(soul[statName]) == "number" then
        return soul[statName]
    end
    
    -- Try capitalized
    local capitalizedName = statName:gsub("^%l", string.upper)
    if soul[capitalizedName] and type(soul[capitalizedName]) == "number" then
        return soul[capitalizedName]
    end
    
    -- Try GetStatLevel (most reliable for main stats)
    if soul.GetStatLevel then
        local success, result = pcall(function() return soul:GetStatLevel(statName) end)
        if success and result and type(result) == "number" then
            return result
        end
    end
    
    -- Try GetStat
    if soul.GetStat then
        local success, result = pcall(function() return soul:GetStat(statName) end)
        if success and result and type(result) == "number" then
            return result
        end
    end
    
    return nil
end

-- Get all player stats
function PlayerStatsReader.GetAllPlayerStats()
    local currentTime = System and System.GetCurrTime and System.GetCurrTime() or 0
    
    -- Use cache if recent
    if currentTime - statsCache.lastUpdate < statsCache.updateInterval and next(statsCache.cachedStats) ~= nil then
        return statsCache.cachedStats
    end
    
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
    
    -- Primary stats (cheat mod naming)
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

-- Global functions for easy access
GetPlayerStats = PlayerStatsReader.GetAllPlayerStats
GetPlayerStat = PlayerStatsReader.GetStatValue
GetPlayerDebugInfo = PlayerStatsReader.GetDebugInfo

-- Export the reader
PlayerStatsAPI = PlayerStatsReader

-- Simple initialization message
if System and System.LogAlways then
    System.LogAlways("Player Stats Reader loaded - Functions: GetPlayerStats(), GetPlayerStat(name)")
end