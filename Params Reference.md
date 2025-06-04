Contains some hidden Params from the original .dll file


## Player

SkillCap                        * max skill level, also effects of a general skill are maximal at this level
StatCap                         * max stat level

SkillXPLevelBase                * base value (additive) to calculate XPs needed for the next level
SkillXPLevelDiff                * multiplicative value to calculate XPs needed
AgilityXPLevelBase
AgilityXPLevelDiff
StrengthXPLevelBase
StrengthXPLevelDiff
VitalityXPLevelBase
VitalityXPLevelDiff
SpeechXPLevelBase
SpeechXPLevelDiff
StoryProgressXPLevelBase
StoryProgressXPLevelDiff
StatToMainLevelBase

StatXPHit
StatXPComboHit
StatXPKill
StatXPAgilityPerDodge           * xp gain after a dodge
StatXPSpeechPerSequence         * speech xp gain after selecting an unused sequence (multiplied by speech_coef of that sequence)
StatXPSpeechPersuadeSuccessMax  * maximal xp gain for persuade
StatXPVitalityPerDistance       * vitality xp gain after sprinting AthleticXPAwardDistance
StatXPVitalityPerJump           * vitality xp gain for each jump
StatXPVitalityPerVault          * vitality xp gain for each vault over a ledge
StatXPVitalityPerKill           * vitality xp gain after a kill

SkillXPPerfectBlock   
SkillXPRiposte
SkillXPDrinkAlcohol
SkillXPUseRepairKit

PickpocketingXP                 * XP for each successful pickpocketing
PickpocketingStealthXP          * XP to stealth for each successful pickpocketing
PickpocketingTreasurePriceXP    * [xp/value] additional XP gain calculated by stolen items total value
PickpocketingFailXPMod          * XP modified on fail
HorseRidingAwardDistance        * award xp for travelling some distance on horse
AthleticXPAwardDistance         * award xp for travelling some distance
HorseRidingXPPerDistance        * horse riding xp gain after riding HorseRidingAwardDistance
SecondaryStatXPRatio            * secondary weapon stat ratio

SpeechDiffToSkillCheckResult        * > 0; speech diff for result = -1/1
BadassnessDiffToSkillCheckResult
CharismaDiffToSkillCheckResult      * > 0; scaled charisma diff for result = -1/1

SkillToDmgConstA
SkillToDefense                  
SkillToFencingBase              * a1 of the geometric progression
SkillToPerfectBlockPowTo        * slot = relativeSkill ^ this, see GDD: *defense
MinPerfectBlockSlot01           * the smallest PB slot for the lowest level
StatsToDodgePowTo               * slot = relativeStats ^ this, see GDD: *defense
BigZoneDistanceSlotMod          * temporary solution, slot mod for distance > 1
MaxPerfectBlockSlotModifier     * % - modifier of PB slot window - determined as (t_hit - t_pbslot) from attack * this value
MaxSpecialPerfectBlockSlotModifier * modifier of SPB slot window - determined as (t_hit - t_pbslot) from attack x this value

MinStatToAttackMult             * minimal relative attack multiplier (for a low stat)
MaxStatToAttackMult             * maximal relative attack multiplier (for a high stat)
MaxStatToAttackStatDiff         * stat difference for max/min relative attack multiplier

BaseInventoryCapacity           * base inventory capacity
StrengthToInventoryCapacity     * [lb/str] derives the inventory capacity from the strength stat

HealthFull                      * maximum health
ImmortalHealthMin               * min health for immortal souls
LowHealthThreshold              * threshold for low health effects (for npcs)

InjuryLowThreshold                  * limb is considered healthy if below this treshold
InjuryHighThreshold                 * limb is bleeding if above this threshold
InjuryRegenInterval                 * injuries fade-out, the time required to regen 1% of injury
InjuryBleedingInterval              * bleeding interval, the time required to lose 1HP

AlchemyToleranceBase                * base brewing tolerance on level 1
AlchemyTolerancePerLevel            * Brewing tolerance gain per level
AlchemyRecipeStepsTolerance         * how many recipe steps might fail in order to successfully brew the recipe
AlchemyTrialEndErrorPerkTolerance   * Additional tolerance gained by having Train And Error perk
HourglassTimeout                    * Alchemy - the time until all the sand goes down
BundleAlchemistPerkAdd              * Addition of potions created with Bundle Alchemist perk
AlchemyXPPerSuccessfullBrewing      * how many XP you get when successfully brew a potion

HerbsInInventoryForFlowerPowerPerk      * number of herbs in inventory needed for FlowerPower perk to be active (#herb)
HerbsInHorseInventoryForHorsenipPerk    * number of herbs in horse inventory needed for Horsenip perk to be active (#herb)
HerbGatherSkillToCount                  * multiplied by sqrt(skill level) to modify the number of collected herbs (#herb)
HerbGatherSkillToRadius                 * [m/xp] multiplied by skill level to calculate radius (#herb)
HerbGatherXP                            * final XP reward for one herb gathering(#herb)

HunterLootAmountAddCoef         * add coef, the fixed portion (#hunter)
HunterXPKill                    * hunter skill XP gain after a kill, multiplied by the game db coef and level
HunterXPLoot                    * hunter skill XP gain after a loot, multiplied by the game db coef and level

ReadingXpPerHour                * Reading
ReadingRestEffectiveness        * If this value is 30, reading will regen player as sleeping on bed with comfort 30%
ReadingRestUpperLimit           * When sleeping, the rest can not exceed bed quality - When reading, the threshold is given by this value
AvidReaderReadingSpeed          * AvidReader soul ability advances reading progress on one book in inventory during sleep or skiptime - This constant determines speed of reading (reading spot is always None)
ImprovedSleepMultiplier         * How much better better (Rest regeneration speed) is SleepImproved than Sleep buff - This buff is used for reading when player has perk InTheFlow
DefaultReadingQuality           * Reading quality when doing nothing special (standing)
NonSkillBookXP                  * XP rewarded for reading non-skill books
OverreadnessFillTime            * how long (in game hours) does it take to fill the oversleepness stat (max time player can read)
OverreadnessEmptyTime           * how long (in game hours) does it take to empty the oversleepness stat (time player have to be not reading to be able to read max time again)

PicklockDmgSpeed                * dmg/s - how fast is picklock durability decreasing (will be multiplied by the relative distance)
PicklockFatalRelativeDist       * maximal relative distance, if futher the pick lock is destroyer
PickpocketingMinChargeTime      * min charge time needed
PickpocketingNPCDrunkTimeChanceMod  * Modifies TimeChancePenalty when drunk
PickpocketingNPCHurtTimeChanceMod   * Modifies TimeChancePenalty when hurt
PickpocketingTimeChancePenaltyBest  * penalty in pickpocketing chance in best case (s)
PickpocketingTimeChancePenaltyWorst * penalty in pickpocketing chance in worst case (s)
PickpocketingAngleChancePenalty     * penalty in (0-1) to chance pickpocketing for each angle from optimal possition exactly from behind victim (180 max)
PickpocketingRobbedAngrinessChancePenalty * penalty in (0-1) to pickpocketing chance for each time victim was robbed before
PickpocketingComradePerkBonus       * max bonus in (0-1) to pickpocketing for comrade perk
PickpocketingIndicatorSharpness     * 0 - precise slow change, 1 - sharp change
PickpocketingMaxSkillChargeTime
PickpocketingMaxSkillChargeSpeedRatio   * charge speed ratio boost with best skill
PickpocketingItemUncoverTimePerWeight   * time to uncover item per weight unit
PickpocketingNPCSleepingTimeChanceMod   * Modifies TimeChancePenalty when sleeping

LockPickingToleranceMCoef       * the kockpicking tolerance formula *lockpicking
LockPickingToleranceNCoef       * the lockpicking tolerance formula *lockpicking
LockPickingToleranceACoef
LockPickingToleranceKCoef
LockPickingTurnBackMulCoef      * multiplicative constant to derive the turnback speed of a lock *lockpicking
LockPickingTurnBackDivCoef      * constant used in the denominator to derive the turnback speed of a lock *lockpicking
LockpickingSoundIntensityMin    * minimal multiplier the lockpicking minigame will generate
LockpickingRelDistanceToSoundIntensity  * [inten/dist] how relative distance influences sound
LockpickingFailSoundIntensity           * [inten] one-shot intensity relative to the database
LockpickingLockpickBreakChance          * base lockpick break chance
LockPickingAppropriateTolerance         * the lock is considered too hard to pick, if the tolerance is smaller than this *lockpicking
LockPickingCursorShakeSpeed             * how fast does cursor shake during lock picking
LockPickingCursorShakeRange             * how much does cursor shake during lock picking (maximum/base value)
LockPickingSkillToShakeRel              * [xp^-1] how much does the skill decrease the cursor shake (skill * this is relative to maximum/base)
LockPickingFailRelativeXPMulCoef        * multiplicative constant to derive XP reward relative to the success *lockpicking
LockPickingSuccessXPMulCoef             * multiplicative constant to derive XP reward for a successfully opened lock *lockpicking
LockPickingSuccessXPDivCoef             * constant used in the denominator to derive XP reward for a successfully opened lock *lockpicking
LockPickingStealthXP                    * xp to stealth for each successful lock-pick

SharpeningMinEfficiencyHealth   * health you can achieve with the worst efficiency
SharpeningSuccessfulHealthDelta * change in weapon health at which the sharpening is considered successful
SharpeningMinIdealAngle         * [stam], [0,1]
SharpeningMaxIdealAngle
SharpeningMinDestructionAngle
SharpeningMaxDestructionAngle
SharpeningFullPositiveHealthXP
SharpeningFullNegativeHealthXP

RepairKitItemHealthBestLimit        * With high skill/quality repairkit can repauir items until this health limit
RepairKitMaxSkillCapacityCoef       * Max skill coef for repair kit total capacity
RepairKitCapacity                   * Repair kit capacity to repair
RepairKitItemPerkBuffHealthThreshold * Buffs added by repair kit perks wont be functional under this item health
RepairKitItemHealthDefaultLimit     * Default repairkit item helth limit 

* when player has Well Worn perk, weight of items is lowered when they are equipped; equippedWeight=standardWeight*(10 - EquippedWeightSubWithWellWornPerk)
EquippedWeightSubWithWellWornPerk

Modifies TimeChancePenalty when sleeping

## --- Barter ---
BasketSuspiciencyThreashold         * Haggle reaction 1 threshold (haggle more difficult)
BasketSuspiciencyNoDealThreashold   * Haggle reaction 2 threshold (transaction refused)
BarterCoefWeightA                   * shopkeeper shop barter calculation 'a' coef
BarterCoefWeightB                   * shopkeeper shop barter calculation 'b' coef
BarterAngrynessCoefWeightA
BarterAngrynessCoefWeightB
BarterPriceSellRepCoef              * sell reputation coef
BarterPriceSellRepMultip            * sell reputation multiplier
BarterPriceSellRepBuying            * price sell vs buy mod
RepairPriceModif                    * Default reparing shop price modif


## --- Perks ----
MaxPerkPoints                   * total number of perk points player will gain per stat/skill
MinPerkPoints                   * no leftovers if the number of perk points would be <= than this
MinLeftoverPerks                * preferred number of leftovers

MaxCloudAverageForShiningArmor          * used by perk Knight in a shining armor; this is maximal current cloud average that still allows this perk to be active
PerkBrutusCombatDmgRBonusFromBehind     * brutus perk multiplicative base Dmg (CombatDmgRBonusFromBehind)
StillBuffDuration                       * duration of standing still after which Still buff bonuses are activated (in worldtime seconds)
PerkWaterOfLifeHealthMultiplier         * potion health effect multiplier for Water of life perk
PerkWaterOfLifeAlcoholMultiplier        * potion alcohol effect multiplier for Water of life perk
PerkTauntAttackerMoraleMultiplier       * multiplier for 'combat_dodge_attacker' morale change when victim has Taunt perk
PerkProperDietActivationTime            * hours until ProperDiet perk bonuses are activated
ThunderstormBuffRainIntensity           * rain intensity threshold when Thunderstorm buff bonuses are activated
PerkBloodRushDistance                   * distance from dying enemy when BloodRush perk bonuses are activated
PerkBloodRushDuration                   * duration of BloodRush perk bonuses after an enemy dies nearby
PerkCarriedBodyGravediggerWeightMul     * carried body weight multiplier for gravedigger perk
LocalHeroInfamousReputationThreshold    * above this rep local hero, under infamous
PerkManlyOdourDirtinessThreshold        * above this dirtiness manly odour perk bonuses are activated
PerkDaringDebonairWantedLevel           * daring debonair wanted level threshold
AdditionalAttackerCountForMaxFadingBuff * for AdditionalAttackerCountFading buff
PerkLastGaspCooldown                    * how fast can the perk be activated again
PerkBerserkDuration                     * how long are buffs active after the perk is triggered
PerkBerserkHealthThreshold
PerkChainStrikeMaxChain                 * maximal successive strikes

StillAndHiddenHysteresis                * switch the state after this timeout
DuringFaderHysteresis                   * the in-fader state is kept for how longer


## --- Movement and Stamina ---
ArmorLoadToSprint               * how armor load coefficient affects sprint
ArmorLoadToRun                  * how armor load coefficient affects running speed
ArmorLoadToJumpCost             * how armor load coefficient affects the stamina jump cost (times base)
JumpCostBase                    * stamina cost of one jump
MaxAgilityToMovementSpeedAddition  * max positive addition (for maximal vit), the same amount is subtracted on level 0
SprintCost                      * stamina/s - stam cost of sprint
StamRegenCooldown               * cooldown timer expiry

StamRegenBase                   * base regeneration speed
StamRegenRelativeDiff           * maximal relative difference to the base speed on low/high stamina
StamRegenBlockMod               * relative stam regen speed during active block or raised weapon
StamRegenMoveMod                * relative stam regen speed during movement
StamRegenFromVit                * how our VIT stat affects stamina regeneration
MinRelativeStaminaMax           * short-term stamina maximum relative to long-term maximum

HarmlessFallHeight                  * falling height below which no health or stamina damage is taken at agility 0
InjuringFallHeight                  * falling height above which health damage is taken at agility 0
FatalFallHeight                     * [%/s] falling height above which fatal health damage is taken at agility 0
FallDamageMultiplierAtMaxAgility    * fall damage multiplier when agility is maxed out

VigourFull                                  * 
VigourTickInterval                          * vigour timer expiry
ExhaustionSpeed                             * amount of energy/vigour 'lost' per world-time second (global base value)
ExhaustedThreshold                          * player will have the 'exhausted' debuff when 'exhaust' stat is lower or equal to this value (in percents)
ExhaustedPlayerEffectMinMin                 * the shortest interval between effects for low exhaust stat
ExhaustedPlayerEffectMaxMin                 * the longest interval between effects for low exhaust stat
ExhaustedPlayerEffectMinMax                 * the shortest interval between effects for high exhaust stat
ExhaustedPlayerEffectMaxMax                 * the longest interval between effects for high exhaust stat
ExtremeExhaustionFaintAveragePeriod
SpeechMulOnExtremeExhaustion    * Player will have this speech multiplied by this value when he has exhaust equal to 0 - Speech will not be changed when exhaust is 50
                                * Linear interpolation on multiplier is applied when exhaust is between 0 and 50
CharismaMulOnExtremeExhaustion  * Player will have this charisma multiplied by this value when he has exhaust equal to 0 - Charisma will not be changed when exhaust is 50
                                * Linear interpolation on multiplier is applied when exhaust is between 0 and 50;
                                
SleepToSaveThreshold                        * sleeping at least this time triggers autosave
SleepHealthRegenBaseSpeed                   * full regen after 8 world-time hours
MinHealthToBeAbleToSleepOrSkiptime          * player will not be able to go sleep or skiptime if his health would go under this threshold during the sleep or skiptime
MinPossibleSleepTime                        * player will reject to lie into bed when he will not be able to sleep at least this long (due to bleeding/hunger/etc, in hours)
OversleepnessFillTime                       * how long (in game hours) does it take to fill the oversleepness stat (max time player can sleep)
OversleepnessEmptyTime                      * how long (in game hours) does it take to empty the oversleepness stat (time player have to be awake to be able to sleep max time again)
InactiveTimeToDestroyOversleep              * how long to let inactive oversleep buff survive (in game seconds) (we have this threshold so that the buff will not be destroyed right after being created in SkipTime class)

MinPedalCost                                * maximum vigour - pedaling STA cost (pressure 0)
MaxPedalCost                                * pedaling STA cost (pressure 1)

## --- Digestion ---
DigestionSpeed                                  * amount of food 'lost' per world-time second (global base value)
ShortTermNutritionDigestionSpeedMultiplier      * digestion multiplier for part of the food with low nutrition value
FoodTickInterval                                * food timer expiry
MetabolismDigestSpeed                           * food/alcohol digested(added) in world time
MetabolismDigestSpeedMultiplier                 * accelerate digest speed multiplier to_digest = max_poisoning
MetabolismAbsorbSpeed                           * food/alcohol metabolised(removed) in world time
FoodPoisoningMaxValue                           * Max amount of food poisoning
FoodFull                                        * you are full
FoodOverEat                                     * you cannot eat more
CaffeineFullThreshold                           * [caf] you cannot use more refreshing items if above this value
CaffeineFromFoodCoef                            * [caf/exh] how much caffeine is added from a unit refresh
FoodSaltOrSmokePerkDecayModif                   * food decay perk modif
FoodSaltOrSmokePerkDecayModif
FoodWitcherPerkNutritionModif
FoodHealthThreshold                             * Health threshold for possitive/negative food effect
FoodHealSpeed                           * hp regen speed
FoodPreserverHealthIncreaseAmount       * this amount is added to food's health when food preserver is applied

AlcoholismRemoveSpeed
AlcoholismTickInterval                  * alcoholism timer expiry
AlcoholismDuration                      * alcoholism duration in world time
AlcoholPerkDrunkMoodRangeMod            * mood range is expanded by this mod
AlcoholPerkDrunkHangoverDurationMod     * hangover duration mod
AlcoholPerkBacchusHangoverEffectMod     * hangover effects mod
AlcoholPerkTrueSlavMaxAlcoholMod        * max amount of alcohol is divided by this mod
AlcoholPerkTrueSlavHangoverDurationMod  
AlcoholPerkCorrectResistanceModif       * alcohol content modif for correct resistance
AlcoholHangoverOffsetModif
AlcoholMaxDrinkingSkillHangoverDurationModifier     * hangover duration modifier for max=best drinking skill
AlcoholDigestSpeedModfifOnEmptyStomache     * digest speed on empty stomache
AlcoholDigestSpeedModfifOnFullStomache      * digest speed on full stomache
AlcoholContentFPAntidoteThreshold           * food with alcohol content above this threashold have anti food poisoning effect
AlcoholismThreshold                         * amount of alcohol that will cause temporary alcoholism
AlcoholismMaxSkillLevelThreshold            * temporary alcoholism threashold with max drinikng skill
AlcoholMaxSTREffect                         * [alcoholism/s] alcoholism removed per world-time second (default 100 / 4days)
AlcoholMaxAGIEffect
AlcoholMaxVITEffect
AlcoholMaxSPCEffect
AlcoholMaxCHAEffect
AlcoholMaxCONEffect
AlcoholMoodMaxExhaustPossitiveEffect        * max positive exhaust effect while in mood
AlcoholDrunkMaxExhaustNegativeEffect        * max negative exhaust effect while drunk
AlcoholBlackoutDuration                     * blackout unconscious duration
AlcoholBaseHangoverDuration                 * base max duration for hangover (after blackout) in world time
AlcoholMoodThreshold                        * [coef] threshold for alcohol mood from max alcohol poisoning
AlcoholDrunkThreshold                       * [coef] threshold for drunkenness mood from max alcohol poisoning
AlcoholPerkWrongResistanceModif             * alcohol content modif for wrong resistance
AlcoholPerkLooseTongueSpcChaModif           * speech and charisma modif bonus/malus for loose tongue perk

FoodPoisoningThreshold                      * starting hangover negative effects are modified by this offset
FoodPoisoningMinHealthEffectSpeed           * minimum loose of health per sec for food poisoning
FoodPoisoningMaxHealthEffectSpeed           * Maximum loose of health per sec for food poisoning
FoodPoisoningMaxStatPenalty                 * maximum temporary penalty for affected stats while food poisoning

StarvationPlayerEffectMaxMin                * max negative/positive stat effect
StarvationPlayerEffectMinMax                * the shortest interval between effects for high hunger stat
StarvationPlayerEffectMaxMax                * the longest interval between effects for high hunger stat
StarvationPlayerEffectMinMin                * the shortest interval between effects for low hunger stat

StarvationHealthLossSpeed       * by design the same speed as the digestion
StarvationThreshold
StarvationHugeThreshold
StarvationExtremeThreshold

## --- Horse ---
HorseRidingToHorseCourage
RiderThreatToHorseMorale        * [morale] morale decrease per one rider threat
HorseMoraleToThrowOffRider      * if the horse mor is below this, it throws off the rider
RiderHorseStaminaCoef           * the ratio between stamina consumption of a horse and its rider
AttSkillToHorsePullDown         * relative attacker skill to horse pull down
AttStrengthToHorsePullDown      * relative attacker stat to horse pull down
RiderSkillToHorsePullDown       * relative riding skill skill to horse pull down
RiderAgilityToHorsePullDown     * relative rider agility to horse pull down
HorseMaxAttackCoef              * maximal multiplicative coef a rider will gain when attacking on HorseMaxAttackSpeed
HorseAttackMaxSpeed             * m/s speed of the attacking rider to gain maximal attack bonus

HorseRidingToHorseStamina       * how the rider's horse riding skill lowers sta consumption of his horse

## --- Ranged Weapon ----
RangedWpnSpeedToAttack 
RangedWpnCosThetaToAttackMin        * cos(theta) lieary lowers the attack in the range [this,1]
RangedWpnSelfHarmCoef               * Special constant used in self harm equation
RangedWpnOptimalDistanceToMinamal   * ratio between the database attack distance and the minimal range for the AI
RangedWpnMinPowerCoef               * the power coef for a really weak soul (the stats are far below requirements)
RangedWpnMinStrCoef                 * if the curr/req strength ratio goes below this, the power is minimal, GDD: 25/222
RangedWpnPowerConstA                * used to convert strength requirements to the resulting power, GDD: 25/222
RangedWpnPwrToSpeed                 * total power to launch speed

SkillToRangedWpnAIRange             * how the relative skill influences the weapon range for the AI
ProjectileMaxBreakProb              * probability of breaking an arrow if a rock-solid material is hit
MatPierceableMaxArmor               * armor of a rock-solid material
BowChargeDurationMin                * the minimal field of view a deaf NPC will have minimum duration of bow charge animation
BowChargeDurationMax                * maximum duration of bow charge animation
BowPowerToChargeDuration            * nominal charge duration for bow with power = 1

AimSpreadMax                        * [s/m] attack mod deduced from impact speed
AimSpreadSkillDecrease              * relative decrease of MAX aim spread for each skill level
ForcedFireAimSpreadMalus            * spread added when the rpg forces the firing on low stamina
AimZoomBase                         * aim zoom (=fov decrease) after reaching some skill level
AimZoomBaseSkill                    * minimal skill level required to benefit from the zoom effect
AimZoomMax                          * maximal aim zoom (=fov decrease)
AimSkillToZoom                      * [deg/skill] zoom increase by each skill level above the base
AimCiriticalLimitTime               * time limit after when AI is notified about low stamina when aiming
AimPainlessDelay                    * aiming without stam loss
AimStamCost                         * after painless delay, stam loss
AimSpreadMinRatio                   * aiming spread min relative to max - this value is used right after entering the painless zone

## --- Stealth ---
StealthAttackMinXp                  * xp gain for successful stealth kill or take-down, weakest enemy
StealthAttackMaxXp                  * xp gain for successful stealth kill or take-down, strongest enemy
StealthAttackFailXp                 * xp gain for failed stealth kill or take-down
StealthSneakBaseXp                  * base xp gain when sneaking, *perception
StealthSneakBaseDistance            * sneaked distance that triggers stealth leveling, *perception
StealthSneakXpSumCoefA              * combine xps from more npcs, *perception
StealthSneakXpSumCoefB
StealthKillProbCoefB
StealthKillProbCoefC

StealthKillDamage                   * damage given to the victim
StealthKillProbCoefA                * stealth kill/knock-out probability formula

StealthCooldown                     * after last detector npc stops seeing player
StealthSneakCheckRadius             * npc query radius when sneaking, *perception
StealthSkillToFootstepSoundMult     * how much how much are footsteps attenuated for the max skill *perception
StealthSkillToRecogTime
StealthSkillToViewRadiusDecr        * how much is the view radius decreased by the skill level (relative) *perception

RecognitionTimeKNegativeCoef        * how much is the required time extended by the skill level (relative) *perception
RecognitionTimeDistanceGain         * perlin gain for the distance influencing the recognition time
RecognitionSpeedNotVisible          * must be negative, how the recognition is decreased
RecognitionTimePCoef                * recognition time for a character with conspicuousness = 0
RecognitionTimeKPositiveCoef        * [s/vib] multiplicative coef for positive values of conspicuousness *perception

StealthKnockOutUnconsciousDepthBase * the base unconsciousness depth for stealth knockout
StealthToUnconsciousDepth           * modifies the time victim is unconscious
UnconsciousDepthFadeoutSpeedBase    * [depth/s] how fast is the depth consumed
VitalityToUnconsciousDepthFadeoutSpeed  * relative vitality
UnconsciousTimeWhenTimeIsNotRunning * if world time is not running, skiptime can not be started when player is unconscious; screen will only fade for this long instead; this is slightly modified by some rpg stats
CombatHitUnconsciousDepth           * depth after a combat hit
CombatHitImmortalUnconsciousDepth   * depth for immortal knock-out

TrueRelationDistThresholdRel    * distance, relative to observers maximum distance, required to see the true faction *perception
MinTrueRelationDistThreshold    * minimal distance required to see the true faction *perception
PerceivedSuperfactionImportanceThresholdRel * superfaction items must occupy more than this for the soul to look like the superfaction *perception

DefaultVisVolume                * [dm3] default item size-volume that have no visibility recognition penalty
BestVisVolume                   * [h/decigrosh]
NightCoefToVis                  * nightCoef = 1 - daytimeCoef; *perception

MinModConspicuousness           * final modified conspicuousness stat minimum (the least conspicuous actor)
MaxModConspicuousness           * final modified conspicuousness stat maximum (the most conspicuous actor)

MinLightProbeVisibility         * min value for the minimal probe result
MaxLightProbeValue              * value for the max visibility

PerceptionMinFov                
PerceptionMaxFov                * the maximal field of view a superman NPC will have
HearingToFov                    * [deg/hea] an increase of FOV caused by the hea stat
MinViewRadius                   * the minimal view radius an almost blind NPC will have, also threshold for instant detection
MaxViewRadius                   * the maximal view radius a superman NPC will have
VisionToViewRadius              * [m/vis]
MinModVisibility                * final modified visibility stat minimum (the most invisible actor)
MaxModVisibility                * final modified visibility stat maximum (the most visible actor)

PerceptionPriorGender
PerceptionPriorNotHumanRace
PerceptionPriorWeapon
PerceptionPriorDead                     * dead or unconscious, *perception
PerceptionPriorThreatened
PerceptionPriorTarget
PerceptionPriorBoostRangedWeapon        * boost for ranged weapons (multiplied by PriorWeapon!), *perception
PerceptionPriorCrimeLoot                * priority boost for crime *perception
PerceptionPriorCrimeLockpick
PerceptionPriorBoostPlayer              * boost for player *perception
PerceptionPriorVisPeople
PerceptionPriorVisItems
PerceptionPriorVisCrimes
PerceptionPriorDist
PerceptionMeanDist
PerceptionPriorConsp
PerceptionPriorFriendRelationship
PerceptionPriorEnemyRelationship
PerceptionPriorCha
PerceptionBaseCha

NightCoefToNoise
MaxHearingSoundAttenuationCoef          * minimal attenuation for non-zero hearing stat
MaxWeatherSoundAttenuationCoef          * 0 - allow weather conditions to mute the sounds, 1 - no influence
MinStealthHitSoundMultiplier            * intensity multiplier for max stealth level
MaxStealthHitSoundMultiplier            * intensity multiplier for min stealth level

ItemOwnerFactionDistanceCoef1
ItemOwnerFactionDistanceCoef2
ItemOwnerFactionDistanceToSuspiciencyMin
ItemOwnerFactionDistanceToSuspiciencyMax
ItemOwnerRelationshipToSuspiciencyMin
ItemOwnerIsShopkeeperToSuspiciency
ItemOwnerFadePriceToHours               * world time hours per decigrosh
ItemOwnerFadeConspicuousnessToHours     * [h/con] world time hours 
ItemOwnerNeverFadesToSuspiciency
ItemOwnerFadeCoefToSuspiciencyMul
ItemOwnerFadeCoefToSuspiciencyExp
ItemOwnerDescFadeToSuspiciencyExp

BarterDominanceSpcWeightA   * barter dominance calculation 'a' coef
BarterDominanceRelationshipWeightB
BarterDominanceChaWeightC
BarterDominanceSpcWeightD
BarterDominanceChaBaseE

## --- Combat ---
ArmorStatusToDefenseCoef
ArmorStatusToCharismaCoef
ArmorDirtToCharismaCoef
WeaponStatusToAttackCoef        * weapon health to status multiplicative coef
MaxFencingWeaponUsageMod        * relative weapon status damage for max fencing

StrAgiToEqwArmorLoad
ArmorLoadDiffToMax
MaxArmorLoad

AttackStamModMin                * attack strength/power stamina modifier minimum (0stam->Xattack)
AttackRequiredStamRatio         * actual/cost stamina ratio must be > than this value for attack to be allowed

AttackSpeedNormal               * normal attack speed, 0-min, 1-max
AttackSpeedNormalAgi            * agility required for the normal attack speed
MaxAttackSpeedMod               * maximal relative change in the attack speed
AgiDiffToAttackSpeed            * relative attak speed gain for one agi level difference 
SkillDiffToAttackSpeed          * relative attak speed gain for one skill level difference
AttackSpeedPlayerRelative       * 1 - attack speed is always calculated using the player, 0 - using opponents skill

MaxStatToAttackStaminaCostMult      * health to armor defense multiplicative coef
MinStatToAttackStaminaCostMult      * min stamina cost mult for a high stat
MaxStatToAttackStaminaCostStatDiff  * stat difference for max/min cost multiplier

StaminaDamageToInjury           * [%] - note: stamina is [0-100] but injury is [0-1]
HealthDamageToInjury            * note: health is [0-100] but injury is [0-1]
HealthDeltaAbsLimit             * [hp/s] - abs max of health delta

UnarmedAttackBase               * attack value for attack with relative stam cost = 1
UnarmedBlockDefense             * defense value for unarmed block
UnarmedAttackReqStrBase         * for attack with relative stam cost = 1

DmgRToHealthCoefA
DmgRToHealthCoefB

StaminaToHealthDamageMin        * [hp/sta] stamina-health damage transfer for dmgr=0
StaminaToHealthDamageMax        * [hp/sta] stamina-health damage transfer for dmgr=1

AverageArmorDefenseWeight               * 0 = only body part defense, 1 = only average defense
ArmorDefenseToAttackingWeaponStatus     * [status/defense] how opponet's defense value damages my weapon - hit to armor
WeaponDefenseToAttackingWeaponStatus    * how opponet's defense value damages my weapon - hit to weapon/block

GoodArmorDefense            * mainly for AI, used to judge armor
PoorWeaponDefense           * mainly for AI, used to judge weapon
GoodWeaponDefense           * mainly for AI, used to judge weapon
SuperWeaponDefense          * like the best shield mainly for AI, used to judge weapon
GoodWeaponAttack

AttackEnergyModifier
HeavyWeaponWeight           * used to deduce 'attack weight' (lbs)

MaxDamage               * all stam and health damages are clamped
MaxDmgR                 * ceil of DmgR ('damage raw')
LethalDmgR              * DmgR that is known to cause death
StamDamage

CombatDmgRBonusFromBehind   * multiplicative DmgR bohus for attacks from behind
FromBehindAngle             * [rad] minimal angle to classify the attack as 'from behind' - 0 face, PI back

HeadHitKnockOutBaseProbability  * for hits dealing a hp damage

WeakBlockStamCoef
HealthToKnockOut                    * [hp] threshold for unarmed combat, health cannot reach this level
EncumberedToSpeedSurfaceCoef        * Coef that controls terrain/surface influence in encumbered speed mod *encumbered
EncumberanceForSecondaryModifiers   * when the buff will activate the secondary group
SurfaceToArmorLoadTWCoef            * Coef tw from terrain/surface to armor load influence calculation
SurfaceToArmorLoadALWCoef           * Coef alw from terrain/surface to armor load influence calculation

MaxStabBuffApplyChance              * chance to apply buff on stab when giving max hp damage
MaxSlashBuffApplyChance             * chance to apply buff on slash when giving max hp damage
MaxSmashBuffApplyChance             * chance to apply buff on smash when giving max hp damage
MinWeaponBuffCharge                 
MaxWeaponBuffCharge

CombatAutoMaxAttackDelay
CombatAutoAttackDelayIncreasePerAttacker        * how many times is the period increased for each attacker
CombatAutoAttackDelayIncreasePerAttackerHorse   * CombatAutoAttackDelayIncreasePerAttacker if the victim is on horse
CombatAutoAttackDelayIncreasePerAttackerMissile * CombatAutoAttackDelayIncreasePerAttacker if the victim has a missile wpn
CombatAutoScaleDefensivenessDelayRel            * relative to attack delay, time to override defensiveness and go near
CombatAutoAttackDelaySigma                      * attack delay variation
CombatAutoTrickNoAttackProb                     * [0-1] no attack prob for the first step
CombatAutoTrickAttackProb                       * [0-1] max trick prob for the first step
CombatAutoReactivePreblockMinDelay
CombatAutoReactivePreblockMaxDelay
CombatAutoStaticPreblockMaxTime
CombatAutoStaticPreblockRandBias                * [0-1] higher nunber -> changes state less often
CombatAutoRiposteAggressionWeight               * [0-1] 0 - use just stamina; 1 - use just 1 - aggression
CombatAutoAggressionDiffScale                   * the bigger number the bigger difference in aggresion for skill differnce
CombatAutoMasterComboSteps                      * combo steps a skilled npc will typically perform
CombatAutoComboStepsSigma                       * standard deviation of performed combo steps
CombatAutoNaturalComboRatio                     * [0-1] ratio of natural combos
CombatAutoNormalBWeight
CombatAutoPBWeight
CombatAutoSPBWeight
CombatAutoDodgeWeight
CombatAutoNoDefenseWeight
CombatAutoUnarmedBlockProb
CombatAutoWpnHealthBlockMax
CombatAutoWpnHealthMinBlockProb
CombatAutoReactionDelayRangeSpread
CombatAutoTrickReactionStaWeight
CombatAutoTrickReactionSkillWeight
CombatAutoTrickReactionMinDelay
CombatAutoTrickReactionMaxDelay
CombatAutoMoveActivityDecreasePerAttacker       * how much must an NPC have to not flee from combat
CombatAutoMinHuntAttackDuration                 * minimal time the NPC is hunting/chasing
CombatAutoMaxHuntAttackDuration                 * maximal time the NPC is hunting/chasing
CombatAutoMinAtkDistOffset                      * offset from min attack distance defined in percentage from attack range
CombatAutoMaxAtkDistOffset                      * offset from max attack distance defined in percentage from attack range
CombatMoveApproachSprintMinStamina              * do not allow sprint during the approach
CombatMoveApproachHysteresis
CombatAutoClinchReactionDelayMaxMin     
CombatAutoClinchReactionDelayMaxMax             
CombatAutoClinchReactionDelayMinMin
CombatAutoClinchReactionDelayMinMax
CombatAutoMasterGuardOffset
CombatAutoLameGuardOffset
CombatAutoGuardHysteresis
CombatAutoForcedPeriodicalAttackStaminaLimit    * stamina threshold
CombatAutoForcedComboStaminaLimit
CombatAutoMaxAimDuration                        * the longest aim time for the lowest skill
CombatAutoMaxAimDurationRandomAdd               * max random time added to the aim duration
CombatAutoOppZoneAdaptDelayMaxMin               * my activity decrease per opponents aditinal attackers
CombatAutoOppZoneAdaptDelayMaxMax
CombatAutoZoneChangeDelayMinMin
CombatAutoZoneChangeDelayMinMax
CombatAutoZoneChangeDelayMaxMin
CombatAutoZoneChangeDelayMaxMax
CombatAutoTrickMaxProb
CombatAutoTrickInvalidBlockAttackMaxProb        * [0-1] max trick prob for a skilled AI if the block is invalid
CombatAutoTrickMinMaxDelay                      * lower bound of the max delay
CombatAutoTrickDelayVariability                 * added to the lower bound
CombatAutoEasyZoneWeight                        * [0-1] how much are easy zones favored by the lame AI (1 = favored)
CombatAutoMinDefenseModeWeight                  * [0-1] the lowest weight for the defense mode
CombatAutoOppZoneAdaptDelayMinMin
CombatAutoOppZoneAdaptDelayMinMax


MinMorale       * min deriv stat value
MaxMorale       * max deriv stat value
MoraleForCombat * mean delay between attacks for a defensive AI
SoulCourageMoraleWeight
ClassCourageMoraleWeight        * Weight of soul class courage affecting morale
HealthToMoraleMinCoef           * multiplicative coef for health = 0
OverallArmorDefenseMoraleWeight * Weight of normalized oad affecting morale
OverallWeaponAttackMoraleWeight * Weight of normalized attack affecting morale
MoraleContextFadingSpeed        * Speed of Morale context increasing/decreasing to 0
MoraleDecisionReliability       * Reliability of morale checks
MaxCourageMoraleContextFadingMod * how much can courage affect morale context fading


## --- General ---
DefaultRelationship                 * default value for the alied forces
ResetPublicFriendsRelationshipMin   * minimal relationship for the alied forces after reset
ResetNearbyRelationshipRange        * range for relationship reset
RelationshipToImpressCharisma       * [0,inf]: how much is the repuation used to raise charisma
RelationshipToPersuadeSpeech        * [0,inf]: how much is the repuation used to raise speech
RelationshipToThreatenBadassness    * [0,inf]: how much is the repuation used to raise badassness
ThreatenStrenghtWeight              * [0,1]: 0 - full weight to morale; 1- full weight to strength
HighbornWealthThreshold             * social class wealth threshold for perks
FactionAngrinessPropagationScale    * Faction angriness propagation distance scale
ReputationPropagationTime           * propagation time from npc to faction/superfaction (world time)
ReputationPropagationBiasTime       * random bias to propagation time (world time)
LocationReputationLovedThreshold    * reputation threshold above which a location will love the player
LocationReputationHatedThreshold    * reputation threshold below which a location will hate the player

ReputationPropagationCoef           * Propagation coef up (soul->faction->superfaction)
NPCRepWeight                        * Weight of player - npc reputation (reputation median)
FactionRepWeight                    * Weight of player - faction reputation (reputation median)
SuperFactionRepWeight               * Weight of superfaction reputation (reputation median)
FactionAngrinessDecayShift          * Faction angriness decay speed shift
FactionAngrinessDecayExp            * Faction angriness decay speed exponent
FactionAngrinessDecayMod            * Faction angriness decay speed mod, whatever it is
FactionAngrinessDecayBase           * Faction angriness decay speed base, whatever it is
FactionAngrinessPropagationCoef     * Faction angriness is propagated through space between factions

CollisionVelocityDeltaToDmgR        * [attack/ms-1]
DefaultWorldTimeRatio               * default world time ratio useed to calculate game time ration in superspeed skiptime
CombatDangerCooldown                * how long is the combat danger active after last enemy stops to be a threat
DefaultStateDeltaSpeed              * any soul state regen / loosing speed
DistanceCheckInterval               * check distance travelled for statistics
ShoeHealthDecrease                  * [status/m] status delta per traveled m
ShoeHealthUpdateDistance            * shoe health is update after traveling N m
QuestMoneyRewardScaleConstant       * scale constnat for quest reward item amount
ItemHealthPriceStatusWeight         * item health status weight price coef
TreasureItemPricee                  * starting price of treasure items

BaseItemDisappearingTime            * base game time for dropped items to auto disappear
ItemDisappearingMulti               * multiplier 1/x - x limit(up/down) for item disappearing speed in extremes (cheap vs expensive, small vs large)
MaxItemDisappearingTime             * max game time for dropped items to disapper

FatCollisionWeightMul               * multiplies the archetype body weight if the character is fat
SlimCollisionWeightMul              * multiplies the archetype body weight if the character is slim
CarriedBodyWeightCoef               * how much of the carried body weight is added to the carried weight of the carrier
CarriedCarriedWeightCoef            * how much of the carried weight of the carried NPC is added to the carried weight of the carrier
CarriedBodyMaxStamConsumption       * uses encumberence to interpolate from 0 to this

JailRecoveryDebuffMaxHours              * hours spent in jail after JailRecovery debuff reaches its maximal values
JailRecoveryDebuffDurationMultiplier    * duration of JailRecovery debuff is calculated as jail duration * this multiplier

HealthFadingFromLimitValue              * health percentage to activate health fading buff

FullClothDirtyingOnFullSpeed            * how far do we walk with full speed (10 walk speed) to get 100% dirty
FullClothDirtyingOnZeroSpeed            * how far do we walk with half speed to get 100% dirty (other speeds than FullSpeed and HalfSpeed are linearly interpolated)
ClothDirtyingUpdatePeriod               * how often (in meters walked) do we add dirt to clothing (both for player and NPCs)

RespawnTimeBase                         * [minutes GameTime] time before a hidden corpse respawns (base time)
RespawnTimeVariation                    * time before a hidden corpse respawns (random extra time)
CorpseDisappearanceTimeUndiscovered     * time before a NPC corpse is hidden when undiscovered
CorpseDisappearanceTimeDiscovered       * time before a NPC corpse is hidden when discovered
CorpseDisapperanceMinDistanceFromPlayer * distance from player below which a corpse will never disappear