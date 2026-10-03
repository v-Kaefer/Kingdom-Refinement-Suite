-- Kingdom Come: Deliverance v1.9.6 - Dynamic Bow Stats Mod
-- Modifica AimSpreadMax e AimStamCost baseado em Agilidade e Força

-- Valores base de referência (do seu exemplo)
local BASE_AIM_SPREAD_MAX = 15
local BASE_AIM_STAM_COST = 20

-- Valores mínimos
local MIN_AIM_SPREAD_MAX = 5
local MIN_AIM_STAM_COST = 10

-- Cache para evitar cálculos desnecessários
local lastPlayerStats = {}
local lastBowWeight = 0
local lastCalculatedValues = {spread = BASE_AIM_SPREAD_MAX, stamCost = BASE_AIM_STAM_COST}

-- Função para obter os atributos do jogador (KCD 1.9.6 específico)
function GetPlayerStats()
    -- Verificar se System existe
    if not System then
        return {agility = 10, strength = 10, inMenu = true}
    end
    
    -- Tentar obter o player usando os métodos corretos do KCD 1.9.6
    local player = nil
    
    -- Método 1: System.GetEntityByName("dude")
    if System.GetEntityByName then
        player = System.GetEntityByName("dude")
    end
    
    -- Método 2: System.GetEntityByClass("Player") como fallback
    if not player and System.GetEntityByClass then
        player = System.GetEntityByClass("Player")
    end
    
    if not player then
        -- Jogador não carregado (ainda no menu)
        return {agility = 10, strength = 10, inMenu = true}
    end
    
    local stats = {inMenu = false}
    
    -- Verificar se o player tem o componente soul
    if not player.soul then
        -- Player existe mas soul não está disponível (menu/carregamento)
        return {agility = 10, strength = 10, inMenu = true}
    end
    
    -- Obter os níveis dos atributos usando métodos alternativos
    local success = false
    
    -- Método 1: Acesso direto aos stats através de propriedades
    if not success and player.soul then
        local agility = nil
        local strength = nil
        
        -- Tentar acessar diretamente como propriedades
        if player.soul.agility then
            agility = player.soul.agility
        elseif player.soul.Agility then
            agility = player.soul.Agility
        end
        
        if player.soul.strength then
            strength = player.soul.strength
        elseif player.soul.Strength then
            strength = player.soul.Strength
        end
        
        if agility and strength and agility > 0 and strength > 0 then
            stats.agility = agility
            stats.strength = strength
            success = true
        end
    end
    
    -- Método 2: Através de GetStat (sem Level)
    if not success and player.soul and player.soul.GetStat then
        local agility = player.soul:GetStat("agility")
        local strength = player.soul:GetStat("strength")
        
        if agility and strength and agility > 0 and strength > 0 then
            stats.agility = agility
            stats.strength = strength
            success = true
        end
    end
    
    -- Método 3: Através do sistema de RPG stats
    if not success and player.rpgStats then
        local agility = player.rpgStats:GetValue("agility")
        local strength = player.rpgStats:GetValue("strength")
        
        if agility and strength and agility > 0 and strength > 0 then
            stats.agility = agility
            stats.strength = strength
            success = true
        end
    end
    
    -- Método 4: Através de GetAttribute
    if not success and player.soul and player.soul.GetAttribute then
        local agility = player.soul:GetAttribute("agility")
        local strength = player.soul:GetAttribute("strength")
        
        if agility and strength and agility > 0 and strength > 0 then
            stats.agility = agility
            stats.strength = strength
            success = true
        end
    end
    
    -- Fallback com valores padrão se não conseguir obter os stats
    if not success then
        stats.agility = 10
        stats.strength = 10
    end
    
    return stats
end

-- Função para obter o peso do arco atual
function GetCurrentBowWeight()
    -- Verificar se System existe
    if not System then
        return 1.0
    end
    
    -- Obter o player
    local player = nil
    if System.GetEntityByName then
        player = System.GetEntityByName("dude")
    end
    
    if not player and System.GetEntityByClass then
        player = System.GetEntityByClass("Player")
    end
    
    if not player then
        return 1.0
    end
    
    -- Verificar se o jogador tem inventário
    if not player.inventory then
        return 1.0
    end
    
    -- Tentar obter item equipado na mão (arco)
    local success = false
    local weight = 1.0
    
    -- Método 1: slot_weapon_bow
    if not success and player.inventory.GetEquippedItem then
        local weapon = player.inventory:GetEquippedItem("slot_weapon_bow")
        if weapon and weapon.item then
            local itemWeight = weapon.item:GetRPGParam("ItemWeight")
            if itemWeight and itemWeight > 0 then
                weight = itemWeight
                success = true
            end
        end
    end
    
    -- Método 2: GetCurrentWeapon
    if not success and player.GetCurrentWeapon then
        local currentWeapon = player:GetCurrentWeapon()
        if currentWeapon then
            local weaponWeight = currentWeapon:GetRPGParam("ItemWeight")
            if weaponWeight and weaponWeight > 0 then
                weight = weaponWeight
                success = true
            end
        end
    end
    
    return weight
end

-- Função principal para calcular os novos valores
function CalculateDynamicBowStats()
    local stats = GetPlayerStats()
    if not stats then
        return BASE_AIM_SPREAD_MAX, BASE_AIM_STAM_COST
    end
    
    -- Se estiver no menu, retornar valores padrão
    if stats.inMenu then
        return BASE_AIM_SPREAD_MAX, BASE_AIM_STAM_COST
    end
    
    local bowWeight = GetCurrentBowWeight()
    
    -- Verificar se precisa recalcular (otimização)
    if stats.agility == lastPlayerStats.agility and 
       stats.strength == lastPlayerStats.strength and 
       bowWeight == lastBowWeight then
        return lastCalculatedValues.spread, lastCalculatedValues.stamCost
    end
    
    -- Calcular AimSpreadMax baseado na Agilidade (0-20)
    -- Fórmula: Spread diminui linearmente com agilidade
    local agilityFactor = math.min(stats.agility, 20) / 20.0
    local newAimSpreadMax = BASE_AIM_SPREAD_MAX - (BASE_AIM_SPREAD_MAX - MIN_AIM_SPREAD_MAX) * agilityFactor
    newAimSpreadMax = math.max(newAimSpreadMax, MIN_AIM_SPREAD_MAX)
    
    -- Calcular AimStamCost baseado na Força (0-20)
    -- Peso do arco reduz o efeito da força em 40%
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

-- Função para aplicar os novos valores (KCD 1.9.6 específico)
function ApplyDynamicBowStats()
    local newSpread, newStamCost = CalculateDynamicBowStats()
    
    -- Verificar se conseguimos obter o player antes de aplicar modificações
    local player = nil
    if System and System.GetEntityByName then
        player = System.GetEntityByName("dude")
    end
    
    if not player and System and System.GetEntityByClass then
        player = System.GetEntityByClass("Player")
    end
    
    -- Se não temos player válido, não aplicar modificações
    if not player or not player.soul then
        return
    end
    
    -- Método principal para KCD 1.9.6: modificar parâmetros RPG globais
    if RPG then
        RPG.AimSpreadMax = newSpread
        RPG.AimStamCost = newStamCost
    end
    
    -- Método alternativo através de Game.SetRPGParam (se disponível)
    if Game and Game.SetRPGParam then
        Game.SetRPGParam("AimSpreadMax", newSpread)
        Game.SetRPGParam("AimStamCost", newStamCost)
    end
    
    -- Log para debug (apenas se estiver em modo debug)
    if System and (System.IsEditor() or System.IsDevMode()) then
        System.Log("Dynamic Bow Stats Applied - Spread: " .. tostring(newSpread) .. ", StamCost: " .. tostring(newStamCost))
    end
end

-- Sistema de eventos para KCD 1.9.6
local DynamicBowMod = {
    updateTimer = 0,
    updateInterval = 1.0, -- atualizar a cada 1 segundo
}

-- Função de update principal
function DynamicBowMod:OnUpdate(frameTime)
    self.updateTimer = self.updateTimer + frameTime
    
    if self.updateTimer >= self.updateInterval then
        ApplyDynamicBowStats()
        self.updateTimer = 0
    end
end

-- Callbacks de eventos
function DynamicBowMod:OnPlayerStatsChanged()
    ApplyDynamicBowStats()
end

function DynamicBowMod:OnWeaponChanged()
    -- Resetar cache quando trocar de arma
    lastBowWeight = 0
    ApplyDynamicBowStats()
end

-- Inicialização do mod
function InitializeDynamicBowMod()
    -- Log de inicialização
    if System and System.Log then
        System.Log("Dynamic Bow Stats Mod v1.9.6 - Iniciando...")
    end
    
    -- Registrar sistema de update
    if Script and Script.SetUpdateFunction then
        Script.SetUpdateFunction(function(frameTime)
            DynamicBowMod:OnUpdate(frameTime)
        end)
    end
    
    -- Aplicar valores iniciais
    ApplyDynamicBowStats()
    
    -- Verificar se conseguiu inicializar
    if System and System.Log then
        System.Log("Dynamic Bow Stats Mod v1.9.6 - Inicializado com sucesso!")
    end
end

-- Função de debug avançada para descobrir a estrutura dos stats
function DebugPlayerStructure()
    local player = nil
    if System and System.GetEntityByName then
        player = System.GetEntityByName("dude")
    end
    
    if not player then
        if System and System.Log then
            System.Log("DEBUG: Player not found")
        end
        return "Player not found"
    end
    
    local debugInfo = "= P. Debug =\n"
    
    -- Verificar componente soul
    if player.soul then
        debugInfo = debugInfo .. "Soul comp.: Found\n"
        
        -- Listar propriedades do soul
        debugInfo = debugInfo .. "Soul prop.:\n"
        for key, value in pairs(player.soul) do
            if type(value) == "number" then
                debugInfo = debugInfo .. "  " .. key .. " = " .. tostring(value) .. "\n"
            elseif type(value) == "function" then
                debugInfo = debugInfo .. "  " .. key .. " = [function]\n"
            else
                debugInfo = debugInfo .. "  " .. key .. " = [" .. type(value) .. "]\n"
            end
        end
    else
        debugInfo = debugInfo .. "Soul component: NOT FOUND\n"
    end
    
    -- Verificar outros componentes relacionados a stats
    if player.rpgStats then
        debugInfo = debugInfo .. "RPG Stats component: Found\n"
    end
    
    if player.playerStats then
        debugInfo = debugInfo .. "Player Stats component: Found\n"
    end
    
    debugInfo = debugInfo .. "============================="
    
    if System and System.Log then
        System.Log(debugInfo)
    else
        print(debugInfo)
    end
    
    return debugInfo
end
function DebugBowStats()
    local stats = GetPlayerStats()
    local bowWeight = GetCurrentBowWeight()
    local newSpread, newStamCost = CalculateDynamicBowStats()
    
    local gameState = "In Menu"
    if stats and not stats.inMenu then
        gameState = "In Game"
    end
    
    -- Obter player para debug adicional
    local player = nil
    if System and System.GetEntityByName then
        player = System.GetEntityByName("dude")
    end
    
    local playerStatus = "Player: Not Found"
    local soulStatus = "Soul: Not Found"
    
    if player then
        playerStatus = "Player: Found"
        if player.soul then
            soulStatus = "Soul: Found"
        end
    end
    
    local debugText = "=Debug D.B.S. v1.9.6 =\n" ..
                     "GameState: " .. gameState .. "\n" ..
                     playerStatus .. "\n" ..
                     soulStatus .. "\n" ..
                     "P. Agi: " .. tostring(stats and stats.agility or "N/A") .. "\n" ..
                     "P. Str: " .. tostring(stats and stats.strength or "N/A") .. "\n" ..
                     "Bow Weight: " .. tostring(bowWeight) .. "\n" ..
                     "Base AimSpreadMax: " .. tostring(BASE_AIM_SPREAD_MAX) .. "\n" ..
                     "Calculated AimSpreadMax: " .. tostring(newSpread) .. "\n" ..
                     "Base AimStamCost: " .. tostring(BASE_AIM_STAM_COST) .. "\n" ..
                     "Calculated AimStamCost: " .. tostring(newStamCost) .. "\n" ..
                     "======================================="
    
    if System and System.Log then
        System.Log(debugText)
    else
        print(debugText)
    end
    
    return debugText
end

-- Função global para debug via console (com verificação de sintaxe)
if bow_debug == nil then
    bow_debug = DebugBowStats
end

-- Função global para debug da estrutura do player
if player_debug == nil then
    player_debug = DebugPlayerStructure
end

-- Auto-inicializar quando o script for carregado
InitializeDynamicBowMod()

-- Exportar para uso em outros scripts
DynamicBowStatsAPI = {
    GetCurrentValues = function()
        return CalculateDynamicBowStats()
    end,
    
    ForceUpdate = function()
        ApplyDynamicBowStats()
    end,
    
    Debug = function()
        DebugBowStats()
    end,
    
    GetPlayerStats = GetPlayerStats,
    GetBowWeight = GetCurrentBowWeight
}