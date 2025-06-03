-- Kingdom Come: Deliverance - Minimal Mod Tools
-- Mod configuration
mmt = {}
mmt.versionMajor = 1
mmt.versionMinor = 1
mmt.devHome = ""
mmt.isCommandLineBuild = false
mmt.commands = {}

-- Log initialization
if not mmt.isCommandLineBuild then
    System.LogAlways("--- Minimal Mod Tools main.lua initialized ---")
end

-- Load file function
function mmt:loadFile(file, fromDisk)
    if not mmt.isCommandLineBuild and not fromDisk then
        Script.ReloadScript("Scripts/" .. file)
    else
        local chunk, err = loadfile(mmt.devHome .. "/Source/Scripts/" .. file)
        if not err then
            chunk()
            print("Loaded file [" .. file .. "].")
        else
            error("Failed to load file [" .. file .. "]. Error [" .. err .. "].")
        end
    end
end

-- Load files function
function mmt:loadFiles(fromDisk)
    if fromDisk then
        fromDisk = true
    else
        fromDisk = false
    end
    
    -- Load Order. Do not change.
    mmt:loadFile("minimal_mod_tools.lua", fromDisk)
end

-- Initialize following mmt mod pattern
mmt:loadFiles()