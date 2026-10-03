-- Kingdom Come: Deliverance v1.9.6 - Dynamic Bow Stats Mod v1.9.8
-- Modifica AimSpreadMax e AimStamCost baseado em Agilidade e Força
-- Fixed with proper stat access methods based on KCD modding research

-- Valores base de referência
local BASE_AIM_SPREAD_MAX = 15
local BASE_AIM_STAM_COST = 20

-- Valores mínimos
local MIN_AIM_SPREAD_MAX = 5
local MIN_AIM_STAM_COST = 10

-- Cache para evitar cálculos desnecessários
local lastPlayerStats = {}
local lastBowWeight = 0
local lastCalculatedValues = {spread = BASE_AIM_SPREAD_MAX, stamCost = BASE_AIM_STAM_COST}

-- Função para obter os atributos do jogador (versão corrigida)
function GetPlayerStats()
    if not System then
        return {agility = 10, strength = 10, inMenu = true}
    end
    
    local player = System.GetEntityByName("dude")
    if not player then
        if System.Log then
            System.Log("DEBUG: Player 'dude' not found")
        end
        return {agility = 10, strength = 10, inMenu = true}
    end
    
    local stats = {inMenu = false}
    local success = false
    
    -- MÉTODO 1: Através do soul com GetRPGStats (mais provável de funcionar)
    if player.soul and not success then
        if System.Log then
            System.Log("DEBUG: Trying player.soul.GetRPGStats...")
        end
        
        -- Tentar GetRPGStats que é o método padrão para stats no KCD
        if player.soul.GetRPGStats then
            local ok, rpgStats = pcall(player.soul.GetRPGStats, player.soul)
            if ok and rpgStats then
                local agility = rpgStats.agility or rpgStats.Agility
                local strength = rpgStats.strength or rpgStats.Strength
                
                if System.Log then
                    System.Log("DEBUG: GetRPGStats - agility: " .. tostring(agility) .. ", strength: " .. tostring(strength))
                end
                
                if agility and strength and tonumber(agility) and tonumber(strength) then
                    stats.agility = tonumber(agility)
                    stats.strength = tonumber(strength)
                    success = true
                    if System.Log then
                        System.Log("DEBUG: GetRPGStats SUCCESS")
                    end
                end
            end
        end
        
        -- MÉTODO 2: Através do GetStat individual (backup)
        if not success and player.soul.GetStat then
            local agility = nil
            local strength = nil
            
            -- Tentar diferentes nomes/IDs de stats baseados na documentação do KCD
            local statVariants = {
                agility = {"agility", "Agility", "AGILITY", "stat_agility", 2}, -- 2 pode ser o ID da agility
                strength = {"strength", "Strength", "STRENGTH", "stat_strength", 1} -- 1 pode ser o ID da strength
            }
            
            for _, variant in ipairs(statVariants.agility) do
                if not agility then
                    local ok, result = pcall(player.soul.GetStat, player.soul, variant)
                    if ok and result and tonumber(result) then
                        agility = tonumber(result)
                        break
                    end
                end
            end
            
            for _, variant in ipairs(statVariants.strength) do
                if not strength then
                    local ok, result = pcall(player.soul.GetStat, player.soul, variant)
                    if ok and result and tonumber(result) then
                        strength = tonumber(result)
                        break
                    end
                end
            end
            
            if System.Log then
                System.Log("DEBUG: Soul GetStat method - agility: " .. tostring(agility) .. ", strength: " .. tostring(strength))
            end
            
            if agility and strength then
                stats.agility = agility
                stats.strength = strength
                success = true
                if System.Log then
                    System.Log("DEBUG: Soul GetStat method SUCCESS")
                end
            end
        end
        
        -- MÉTODO 3: Acesso direto às propriedades numéricas (se existirem)
        if not success then
            -- Tentar acessar como propriedades diretas usando diferentes casos
            local possibleProps = {
                {player.soul.agility, player.soul.strength},
                {player.soul.Agility, player.soul.Strength},
                {player.soul.AGILITY, player.soul.STRENGTH}
            }
            
            for _, props in ipairs(possibleProps) do
                local agility, strength = props[1], props[2]
                if agility and strength and tonumber(agility) and tonumber(strength) then
                    stats.agility = tonumber(agility)
                    stats.strength = tonumber(strength)
                    success = true
                    if System.Log then
                        System.Log("DEBUG: Soul direct property access SUCCESS - agility: " .. stats.agility .. ", strength: " .. stats.strength)
                    end
                    break
                end
            end
        end
    end
    
    -- MÉTODO 4: Através do RPG global (baseado na sua exploração anterior)
    if not success and RPG then
        if System.Log then
            System.Log("DEBUG: Trying RPG global methods...")
        end
        
        -- Como você viu RPG.AddStatXP, pode haver um método para obter stats também
        local rpgMethods = {"GetPlayerStat", "GetStat", "GetPlayerAttribute", "GetStatValue"}
        
        for _, method in ipairs(rpgMethods) do
            if RPG[method] and not success then
                local agilityResult = nil
                local strengthResult = nil
                
                -- Tentar com diferentes formatos de nome
                local statNames = {"agility", "Agility", "AGILITY", 2} -- 2 pode ser ID
                for _, statName in ipairs(statNames) do
                    if not agilityResult then
                        local ok, result = pcall(RPG[method], RPG, statName)
                        if ok and result and tonumber(result) then
                            agilityResult = tonumber(result)
                            break
                        end
                    end
                end
                
                statNames = {"strength", "Strength", "STRENGTH", 1} -- 1 pode ser ID
                for _, statName in ipairs(statNames) do
                    if not strengthResult then
                        local ok, result = pcall(RPG[method], RPG, statName)
                        if ok and result and tonumber(result) then
                            strengthResult = tonumber(result)
                            break
                        end
                    end
                end
                
                if System.Log then
                    System.Log("DEBUG: RPG." .. method .. " - agility: " .. tostring(agilityResult) .. ", strength: " .. tostring(strengthResult))
                end
                
                if agilityResult and strengthResult then
                    stats.agility = agilityResult
                    stats.strength = strengthResult
                    success = true
                    if System.Log then
                        System.Log("DEBUG: RPG." .. method .. " SUCCESS")
                    end
                    break
                end
            end
        end
    end
    
    -- MÉTODO 5: Usando console commands como backup (funciona mas é menos elegante)
    if not success then
        if System.Log then
            System.Log("DEBUG: Trying console command method as last resort...")
        end
        
        -- Este método usa comandos de console para obter stats
        -- Nota: Isso só funciona se devmode estiver ativo
        if System.ExecuteCommand then
            -- Tentar capturar output do comando stat
            local agilityCmd = "stat agility"
            local strengthCmd = "stat strength"
            
            local agilityResult = System.ExecuteCommand(agilityCmd)
            local strengthResult = System.ExecuteCommand(strengthCmd)
            
            if agilityResult and strengthResult then
                -- Parsing simples do resultado (pode precisar ajustar)
                local agility = tonumber(string.match(tostring(agilityResult), "%d+"))
                local strength = tonumber(string.match(tostring(strengthResult), "%d+"))
                
                if agility and strength then
                    stats.agility = agility
                    stats.strength = strength
                    success = true
                    if System.Log then
                        System.Log("DEBUG: Console command method SUCCESS")
                    end
                end
            end
        end
    end
    
    if not success then
        if System.Log then
            System.Log("DEBUG: All methods failed, using fallback values")
        end
        stats.agility = 10
        stats.strength = 10
    else
        if System.Log then
            System.Log("DEBUG: Successfully obtained stats - Agility: " .. stats.agility .. ", Strength: " .. stats.strength)
        end
    end
    
    return stats
end

-- Função para obter o peso do arco atual (mantida igual)
function GetCurrentBowWeight()
    if not System then
        return 1.0
    end
    
    local player = System.GetEntityByName("dude")
    if not player then
        return 1.0
    end
    
    -- Método 1: Através do inventory (original)
    if player.inventory and player.inventory.GetEquippedItem then
        local weapon = player.inventory:GetEquippedItem("slot_weapon_bow")
        if weapon and weapon.item then
            local itemWeight = weapon.item:GetRPGParam("ItemWeight")
            if itemWeight and tonumber(itemWeight) and tonumber(itemWeight) > 0 then
                return tonumber(itemWeight)
            end
        end
    end
    
    -- Método 2: Através do actor se disponível
    if player.actor and player.actor.GetEquippedItem then
        local weapon = player.actor:GetEquippedItem("slot_weapon_bow")
        if weapon and weapon.item then
            local itemWeight = weapon.item:GetRPGParam("ItemWeight")
            if itemWeight and tonumber(itemWeight) and tonumber(itemWeight) > 0 then
                return tonumber(itemWeight)
            end
        end
    end
    
    return 1.0
end

-- Função principal para calcular os novos valores (sem alterações)
function CalculateDynamicBowStats()
    local stats = GetPlayerStats()
    if stats.inMenu then
        return BASE_AIM_SPREAD_MAX, BASE_AIM_STAM_COST
    end
    
    local bowWeight = GetCurrentBowWeight()
    
    -- Verificar cache (otimização)
    if stats.agility == lastPlayerStats.agility and 
       stats.strength == lastPlayerStats.strength and 
       bowWeight == lastBowWeight then
        return lastCalculatedValues.spread, lastCalculatedValues.stamCost
    end
    
    -- Calcular AimSpreadMax baseado na Agilidade (0-20)
    local agilityFactor = math.min(stats.agility, 20) / 20.0
    local newAimSpreadMax = BASE_AIM_SPREAD_MAX - (BASE_AIM_SPREAD_MAX - MIN_AIM_SPREAD_MAX) * agilityFactor
    newAimSpreadMax = math.max(newAimSpreadMax, MIN_AIM_SPREAD_MAX)
    
    -- Calcular AimStamCost baseado na Força (0-20)
    local strengthFactor = math.min(stats.strength, 20) / 20.0
    local weightPenalty = math.min(bowWeight * 0.4, 0.4) -- máximo 40% de penalidade
    local effectiveStrengthFactor = strengthFactor * (1.0 - weightPenalty)
    local newAimStamCost = BASE_AIM_STAM_COST - (BASE_AIM_STAM_COST - MIN_AIM_STAM_COST) * effectiveStrengthFactor
    newAimStamCost = math.max(newAimStamCost, MIN_AIM_STAM_COST)
    
    -- Arredondar valores
    newAimSpreadMax = math.floor(newAimSpreadMax * 10 + 0.5) / 10
    newAimStamCost = math.floor(newAimStamCost * 10 + 0.5) / 10
    
    -- Atualizar cache
    lastPlayerStats = {agility = stats.agility, strength = stats.strength}
    lastBowWeight = bowWeight
    lastCalculatedValues = {spread = newAimSpreadMax, stamCost = newAimStamCost}
    
    return newAimSpreadMax, newAimStamCost
end

-- Função para aplicar os novos valores (melhorada)
function ApplyDynamicBowStats()
    local newSpread, newStamCost = CalculateDynamicBowStats()
    
    -- Verificar se temos player válido antes de aplicar
    local player = System and System.GetEntityByName("dude")
    if not player or not player.soul then
        return
    end
    
    -- MÉTODO 1: Aplicar através do RPG global
    if RPG then
        -- Tentar diferentes formas de aplicar
        if RPG.SetParam then
            RPG.SetParam("AimSpreadMax", newSpread)
            RPG.SetParam("AimStamCost", newStamCost)
        elseif RPG.SetRPGParam then
            RPG.SetRPGParam("AimSpreadMax", newSpread)
            RPG.SetRPGParam("AimStamCost", newStamCost)
        else
            -- Aplicação direta (pode não funcionar mas vale tentar)
            RPG.AimSpreadMax = newSpread
            RPG.AimStamCost = newStamCost
        end
    end
    
    -- MÉTODO 2: Através do Game global
    if Game then
        if Game.SetRPGParam then
            Game.SetRPGParam("AimSpreadMax", newSpread)
            Game.SetRPGParam("AimStamCost", newStamCost)
        elseif Game.SetParam then
            Game.SetParam("AimSpreadMax", newSpread)
            Game.SetParam("AimStamCost", newStamCost)
        end
    end
    
    -- MÉTODO 3: Através do sistema de configuração global (se existir)
    if CVar then
        CVar.Set("AimSpreadMax", newSpread)
        CVar.Set("AimStamCost", newStamCost)
    end
    
    -- MÉTODO 4: Através de comandos console (último recurso)
    if System and System.ExecuteCommand then
        System.ExecuteCommand("set AimSpreadMax " .. tostring(newSpread))
        System.ExecuteCommand("set AimStamCost " .. tostring(newStamCost))
    end
    
    if System and System.Log then
        System.Log("DEBUG: Applied bow stats - Spread: " .. newSpread .. ", StamCost: " .. newStamCost)
    end
end

-- Sistema de update otimizado (sem alterações)
local DynamicBowMod = {
    updateTimer = 0,
    updateInterval = 1.0, -- atualizar a cada 1 segundo
}

function DynamicBowMod:OnUpdate(frameTime)
    self.updateTimer = self.updateTimer + frameTime
    
    if self.updateTimer >= self.updateInterval then
        ApplyDynamicBowStats()
        self.updateTimer = 0
    end
end

-- Inicialização do mod (sem alterações)
function InitializeDynamicBowMod()
    -- Registrar sistema de update
    if Script and Script.SetUpdateFunction then
        Script.SetUpdateFunction(function(frameTime)
            DynamicBowMod:OnUpdate(frameTime)
        end)
    end
    
    -- Aplicar valores iniciais
    ApplyDynamicBowStats()
end

-- Função de debug melhorada
function DebugBowStats()
    local stats = GetPlayerStats()
    local bowWeight = GetCurrentBowWeight()
    local newSpread, newStamCost = CalculateDynamicBowStats()
    
    local gameState = "In Menu"
    if stats and not stats.inMenu then
        gameState = "In Game"
    end
    
    if System and System.Log then
        System.Log("=== Debug Dynamic Bow Stats v1.9.8 ===")
        System.Log("Game State: " .. gameState)
        System.Log("Player Agility: " .. tostring(stats and stats.agility or "N/A"))
        System.Log("Player Strength: " .. tostring(stats and stats.strength or "N/A"))
        System.Log("Bow Weight: " .. tostring(bowWeight))
        System.Log("Base AimSpreadMax: " .. tostring(BASE_AIM_SPREAD_MAX))
        System.Log("Calculated AimSpreadMax: " .. tostring(newSpread))
        System.Log("Base AimStamCost: " .. tostring(BASE_AIM_STAM_COST))
        System.Log("Calculated AimStamCost: " .. tostring(newStamCost))
        System.Log("=======================================")
    end
    
    return "Debug completed - check console log"
end

-- NOVA FUNÇÃO: Teste focado na soul
function TestSoulMethods()
    if not System then
        return "System not available"
    end
    
    local player = System.GetEntityByName("dude")
    if not player or not player.soul then
        return "Player or soul not found"
    end
    
    if System.Log then
        System.Log("=== TESTING SOUL METHODS ===")
        
        -- Listar todos os métodos disponíveis na soul
        for key, value in pairs(player.soul) do
            if type(value) == "function" then
                System.Log("  Available method: " .. key)
            end
        end
        
        -- Testar especificamente métodos relacionados a stats
        local methodsToTest = {"GetRPGStats", "GetStat", "GetStats", "GetAttribute", "GetAttributes"}
        
        for _, method in ipairs(methodsToTest) do
            if player.soul[method] then
                System.Log("  Testing " .. method .. "...")
                local success, result = pcall(player.soul[method], player.soul)
                if success then
                    System.Log("    " .. method .. " result: " .. tostring(result) .. " [" .. type(result) .. "]")
                    
                    -- Se for uma tabela, explorar
                    if type(result) == "table" then
                        for k, v in pairs(result) do
                            System.Log("      " .. k .. " = " .. tostring(v))
                        end
                    end
                else
                    System.Log("    " .. method .. " failed: " .. tostring(result))
                end
            end
        end
        
        System.Log("=============================")
    end
    
    return "Soul test completed"
end

-- Atualizar as funções globais
player_debug = DebugBowStats
bow_debug = DebugBowStats
soul_test = TestSoulMethods

-- Auto-inicializar quando o script for carregado
InitializeDynamicBowMod()