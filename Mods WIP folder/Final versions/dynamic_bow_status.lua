-- Kingdom Come: Deliverance v1.9.6 - Dynamic Bow Stats Mod Veersion 1.0.0
-- Modifica AimSpreadMax e AimStamCost baseado em Agilidade e Força

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

-- Função para obter os atributos do jogador
function GetPlayerStats()
    if not System then
        return {agility = 1, strength = 1, inMenu = true}
    end
    
    local player = System.GetEntityByName("dude")
    if not player or not player.soul then
        return {agility = 1, strength = 1, inMenu = true}
    end
    
    -- Método que funcionou: acesso direto às propriedades
    local agility = player.soul.agility or player.soul.Agility
    local strength = player.soul.strength or player.soul.Strength
    
    if agility and strength and agility > 0 and strength > 0 then
        return {agility = agility, strength = strength, inMenu = false}
    end
    
    -- Fallback se não conseguir ler os stats
    return {agility = 1, strength = 1, inMenu = false}
end

-- Função para obter o peso do arco atual
function GetCurrentBowWeight()
    if not System then
        return 1.0
    end
    
    local player = System.GetEntityByName("dude")
    if not player or not player.inventory then
        return 1.0
    end
    
    -- Tentar obter arco equipado
    if player.inventory.GetEquippedItem then
        local weapon = player.inventory:GetEquippedItem("slot_weapon_bow")
        if weapon and weapon.item then
            local itemWeight = weapon.item:GetRPGParam("ItemWeight")
            if itemWeight and itemWeight > 0 then
                return itemWeight
            end
        end
    end
    
    return 1.0
end

-- Função principal para calcular os novos valores
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

-- Função para aplicar os novos valores
function ApplyDynamicBowStats()
    local newSpread, newStamCost = CalculateDynamicBowStats()
    
    -- Verificar se temos player válido antes de aplicar
    local player = System and System.GetEntityByName("dude")
    if not player or not player.soul then
        return
    end
    
    -- Aplicar modificações nos parâmetros RPG globais
    if RPG then
        RPG.AimSpreadMax = newSpread
        RPG.AimStamCost = newStamCost
    end
    
    -- Método alternativo se disponível
    if Game and Game.SetRPGParam then
        Game.SetRPGParam("AimSpreadMax", newSpread)
        Game.SetRPGParam("AimStamCost", newStamCost)
    end
end

-- Sistema de update otimizado
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

-- Inicialização do mod
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

-- Auto-inicializar quando o script for carregado
InitializeDynamicBowMod()