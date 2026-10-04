# Mod profiles (generated)

> **GENERATED** by `tools/audit_mods_deep.py`: do not edit | **Kind:** review | **Trust:** archives read statically (listed, extracted to a scratch folder, read, deleted); nothing was installed or run | **Game version:** 1.9.8

One section per archive of the P1/P2 mods, best first by grade. What it changes, how it is installed, where the data lives, how much it changes (against the vanilla tables), what it needs, and the risk result. See [`MOD_ANALYSIS.md`](MOD_ANALYSIS.md) for the grading rules.

## 2124 Half-looted Rebalance (P2, Progression / XP / perks)

- **What the author says (Nexus summary):** This is a collection of mods, focused on increasing the gameplay depth, realism and removing some frustrations without changing the game too much. It rebalances most items, tweaks combat and game difficulty, fixes few things and adds some
- **File:** `Complete EHLR mod collection with documentation 2124 2.5.0 2026-07-22T00-51Z 37afHBvHt.zip` (archive, 1.26 MB, `c_progression-xp-perks`), full (scratch, deleted after reading)
- **Grade:** A changes the most | **perceptibility:** high | **layers:** D0 content/text; D1 data tables (PTF); D2 engine config; D3 Lua scripts
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `1.9.6 1.9.7`, loads on 1.9.8: NO (disabled: lists 1.9.6, 1.9.7)
- **Where it changes things:** tables (PTF): 58; localization: 56; manifest: 14; pak (container): 14; other: 4; textures: 2; other xml (data): 2; docs: 1; config (.cfg): 1; ui: 1; scripts (Lua): 1; lua identical to vanilla: 0
- **Tables:** ammo, armor, armor_type, body_part, buff, combat_action_attack, combat_action_perfect_block, combat_action_sync_attack, combat_attack_type, divisible_item, equippable_item, food, inventory2item, inventory_preset2item, item, melee_weapon, missile_weapon, perk, perk_buff, perk_rpg_param_override, pick (17704 new rows, 4915 changed, 47199 identical to vanilla, 173044 vanilla rows dropped by a whole-table replace); median relative change 0.8
- **Largest changes:** shop_type2item:7899825d-ed6f-4f00-b698-649ba652cf6d amount 5->58; shop_type2item:907a2cd5-2730-424e-bf11-ef1f2db8f7e1 amount 2->25; shop_type2item:907a2cd5-2730-424e-bf11-ef1f2db8f7e1 amount 2->24; shop_type2item:81c21fdc-3d62-4d1f-854f-eb364db1bcff amount 3->35; shop_type2item:5ef63059-322e-4e1b-abe8-926e100c770e amount 200->8000; shop_type2item:5ef63059-322e-4e1b-abe8-926e100c770e amount 200->8000; pickable_item:ecae9bde-4b59-4ce2-8d3b-e718eb0f4c45 price 45->925; armor:4a2e6701-7c43-b97a-0823-6e22ea1d8fb3 smash_def 0.428->6.3
- **Lua:** 1 files, 38 lines; API used: System.AddCCommandx2, System.GetCVarx2, System.ExecuteCommandx1
- **Config:** 2 keys, e.g. wh_pl_showfirecursor=1, wh_ui_ShowCursor=1
- **Text:** 279 strings changed, 336 new
- **Same rows as KRS:** krs_items:food:73ff1fde-ec8b-41e9-95e3-b5938c715bf1; krs_items:rpg_param:DigestionSpeed
- **Problems:** EHLR_AbolishUnfairPerks/Data/EHLR_AbolishUnfairPerks.pak!Libs/Tables/rpg/soul2perk.xml: no suffix: replaces the whole vanilla table / EHLR_AdjustShops/Data/EHLR_AdjustShops.pak!Libs/Tables/shop/shop.xml: no suffix: replaces the whole vanilla table / EHLR_AdjustShops/Data/EHLR_AdjustShops.pak!Libs/Tables/shop/shop_type2item.xml: no suffix: replaces the whole vanilla table / EHLR_Archery/Data/EHLR_Archery.pak!Libs/Tables/item/ammo__EHLR_Archery.xml: suffix 'EHLR_Archery' != id 'ehlr_abolishunfairperks' (the game ignores it) / EHLR_Archery/Data/EHLR_Archery.pak!Libs/Tables/rpg/rpg_param__EHLR_Arc
- **Risk:** none

## 883 KingdomCome Rebalancing (P2, Progression / XP / perks)

- **What the author says (Nexus summary):** This Mod changes:- Weapons (mostly Swords)- Armor (Weight, Denfenserating, Prices, ...)- Skills/Perks (Lvl up slower, other Levels required to learn perks, changed some Perks)- Changed RPG Params (for harder combat or less player and horse
- **File:** `Rebalancing 1.3-883-1-3-1593332571.7z` (archive, 39.07 MB, `c_progression-xp-perks`), full (scratch, deleted after reading)
- **Grade:** A changes the most | **perceptibility:** high | **layers:** D0 content/text; D1 data tables (PTF)
- **How it installs:** loose .pak (legacy: copy into Data); manifest id `-`, supports `-`, loads on 1.9.8: no manifest (legacy install)
- **Where it changes things:** tables (PTF): 409; other: 384; localization: 22; ui: 10; other xml (data): 2; pak (container): 1; lua identical to vanilla: 0
- **Tables:** ?, achievement, armor, buff, equippable_item, gold_dayone_stash_diff, inventory_preset2item, melee_weapon, perk, perk_rpg_param_override, pickable_item, quest_objective, rpg_param, shop, soul_archetype, topic2sequence, weapon (21 new rows, 16848 changed, 782156 identical to vanilla, 121 vanilla rows dropped by a whole-table replace); median relative change 0.4
- **Largest changes:** equippable_item:41382adf-569c-4f33-90a0-36b6e874eca7 rpg_buff_weight 0.05->0.525; weapon:d459cb3a-04b5-4de7-b115-35ec17d293ba max_status 10->82; pickable_item:4d887670-13cb-746d-5e27-5d234e146cb3 price 660->4790; pickable_item:4e92a77b-f989-fa76-4147-4ed3cf5c0faf weight 5->29; pickable_item:4ab8c97d-6977-4b6c-4d66-86b471549483 weight 5->28; equippable_item:475642da-17e6-c06e-b035-2b1ab31cbb8f rpg_buff_weight 0.1->0.55; pickable_item:4c71ff43-0696-66e4-71d9-45f30cf05392 weight 6->32; pickable_item:49cbb237-9280-ba16-cfe4-3d05bacb85a3 weight 5->26
- **Text:** 2982 strings changed, 0 new
- **Same rows as KRS:** krs_qol:rpg_param:RepairPriceModif; krs_qol:rpg_param:StrengthToInventoryCapacity
- **Problems:** Tables.pak!Libs/Tables/action/actor_action_fragment_id_mapping.xml: no suffix: replaces the whole vanilla table / Tables.pak!Libs/Tables/action/actor_action_standup.xml: no suffix: replaces the whole vanilla table / Tables.pak!Libs/Tables/action/actor_action_transition_to_combat.xml: no suffix: replaces the whole vanilla table / Tables.pak!Libs/Tables/action/actor_action_type.xml: no suffix: replaces the whole vanilla table / Tables.pak!Libs/Tables/action/actor_action_type_group.xml: no suffix: replaces the whole vanilla table / Tables.pak!Libs/Tables/action/actor_activity.xml: no suffix: repl
- **Risk:** none

## 2299 1403 - Historical Rebalance (P2, Progression / XP / perks)

- **What the author says (Nexus summary):** A historically grounded overhaul of equipment, economy, combat, AI, progression, and survival.
- **File:** `1403 2299 1.5 2026-08-21T17-11Z ZWdhR2re2.zip` (archive, 1.0 MB, `c_progression-xp-perks`), full (scratch, deleted after reading)
- **Grade:** A changes the most | **perceptibility:** high | **layers:** D0 content/text; D1 data tables (PTF); D3 Lua scripts
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `(none)`, loads on 1.9.8: yes (no version restriction)
- **Where it changes things:** other: 42; tables (PTF): 33; docs: 15; other xml (data): 8; localization: 3; scripts (Lua): 3; manifest: 1; pak (container): 1; lua identical to vanilla: 0
- **Tables:** ammo, armor, armor2clothing_preset, buff, clothing_preset, combat_action_attack, combat_action_sync_attack, dialogue_functions, food, inventory2item, inventory_preset2item, melee_weapon, missile_weapon, money_change, ointment_item, perk, perk_rpg_param_override, pickable_area_desc, pickable_item, pl (1195 new rows, 7323 changed, 2254 identical to vanilla, 71650 vanilla rows dropped by a whole-table replace); median relative change 1.0
- **Largest changes:** armor:00000000-0000-0000-0000-000000000020 slash_def 0.1->3; armor:0082de35-b635-4b85-a9ec-95024713f3ab slash_def 2->36; armor:40024d27-b1c4-6ef7-3ca0-98025de43f9e smash_def 0.168->2; armor:40031fce-5752-3279-92f6-b564d55aeb8f smash_def 0.46->6; armor:400b4bb0-a1d0-9bec-1b90-5b2bfcb9e9af slash_def 0.1->3; armor:401179d4-8a48-cc9a-ceac-eeaf7eb7b099 slash_def 0.72->9; armor:40129e7b-b9e0-a193-1145-d53292caf7a1 slash_def 1.56->41; armor:4015718d-f526-1bb1-da6f-6e390b15e2b8 slash_def 0.1->2
- **Lua:** 3 files, 448 lines; API used: Script.SetTimerForFunctionx3, System.GetEntityByNamex2, XGenAIModule.SendMessageToEntityx1, player.inventoryx1
- **Text:** 0 strings changed, 1487 new
- **Mentions:** states requirements
- **Same rows as KRS:** krs_items:food:73ff1fde-ec8b-41e9-95e3-b5938c715bf1; krs_qol:rpg_param:HerbGatherSkillToRadius
- **Problems:** Mods/1403/Data/1403.pak!Libs/Tables/quest/quest_reward_item.xml: no suffix: replaces the whole vanilla table
- **Risk:** none

## 2294 Faster Combat - Directional Master Strikes - Better Group Fights (P2, Combat / AI)

- **What the author says (Nexus summary):** Modular installer: attack speed profiles, directional master strikes, optional tackle and slow-motion removal, group-fight limits, optional bow reticle Faster combat with directional Master Strikes, optional no tackles, reduced enemy swarming and no slow motion.
- **File:** `FasterCombat FOMOD 2294 1.2.1 2026-07-30T00-33Z U5RChtbhP.zip` (archive, 2.3 MB, `c_combat-ai`), full (scratch, deleted after reading)
- **Grade:** A changes the most | **perceptibility:** high | **layers:** D0 content/text; D1 data tables (PTF); D2 engine config
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `(none)`, loads on 1.9.8: yes (no version restriction)
- **Where it changes things:** tables (PTF): 55; pak (container): 32; config (.cfg): 32; models/animations/materials: 12; docs: 3; other xml (data): 3; manifest: 1; lua identical to vanilla: 0
- **Tables:** buff, combat_action_attack, combat_action_perfect_block, combat_action_sync_attack, combat_action_sync_pb_hit, combat_combo, combat_combo_step, perk_rpg_param_override, rpg_param, weapon_class (787 new rows, 2198 changed, 6 identical to vanilla, 9478 vanilla rows dropped by a whole-table replace); median relative change 0.091
- **Largest changes:** weapon_class:/1//3/0/5/0/24/12/0 hunt_attack_distance 1.9->-1; weapon_class:/1//3/0/5/0/24/12/0 hunt_attack_distance 1.9->-1; weapon_class:/1//3/0/5/0/24/12/0 hunt_attack_distance 1.9->-1; weapon_class:/1//3/8/1/0/16/1/0 hunt_attack_distance 2.4->-1; weapon_class:/1//3/0/1/0/16/2/0 hunt_attack_distance 2.4->-1; weapon_class:/2//3/0/1/0/17/3/0 hunt_attack_distance 2.4->-1; weapon_class:bf861d60-b892-42a3-9c3b-d3787362f88b/1//3/8/1/0/16/4/0 hunt_attack_distance 2.4->-1; weapon_class:/2//3/0/2/0/21/5/0 hunt_attack_distance 2.4->-1
- **Config:** 14 keys, e.g. WH_AI_CombatMove_CatchDistanceTolerance=0.70, WH_AI_CombatMove_InAreaHysteresisTolerance=0.55, WH_AI_CombatMove_TacticalRangeGain=2, WH_AI_CombatMove_TacticalRangeGain=3, WH_AI_CombatMove_TacticalRangeGain=5, WH_AI_CombatMove_TacticalSurround=1, WH_AI_CombatMove_TacticalSurround=2, wh_cs_AutomationAction_HuntAttackTimeLimit=-1
- **Mentions:** Vortex, mentions Tables.pak, states requirements
- **Risk:** none

## 1629 Exclusive Master Strikes - Make Them Reasonable (P2, Combat / AI)

- **What the author says (Nexus summary):** Only heavily armored NPCs keep the master strike; removes NPC tackles; affects only newly spawned NPCs on old saves. Same author as Restore Riposte Classify NPCs,only those wearing heavy armor can use master strike.给敌人分级，重甲单位才能使用大师反，同时移除所有npc的阻截能力,让你对抗多个无甲、轻甲敌人更加容易。
- **File:** `MakeThemReasonable-1629-1-2-0-1736432412.zip` (archive, 0.15 MB, `c_combat-ai`), full (scratch, deleted after reading)
- **Grade:** A changes the most | **perceptibility:** high | **layers:** D0 content/text; D1 data tables (PTF)
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `1.9.6`, loads on 1.9.8: NO (disabled: lists 1.9.6)
- **Where it changes things:** localization: 28; tables (PTF): 2; manifest: 1; pak (container): 1; other: 1; lua identical to vanilla: 0
- **Tables:** perk, soul2perk (2423 new rows, 1 changed, 44027 identical to vanilla, 5242 vanilla rows dropped by a whole-table replace); median relative change 1.0
- **Largest changes:** perk:61e91997-9b32-123b-ad05-8691afdb81be NEW row; perk:1627a1b6-64c5-422f-ac2d-3a6abc071690 visibility 0->1; soul2perk:61e91997-9b32-123b-ad05-8691afdb81be/00d2d228-b63c-4aa7-8f18-dc9cf74ec97e NEW row; soul2perk:61e91997-9b32-123b-ad05-8691afdb81be/010cde8e-c14f-49fa-a3b5-f1e7138d740e NEW row; soul2perk:61e91997-9b32-123b-ad05-8691afdb81be/01dfda33-2b1a-4cb7-8b98-5c0a940f4e3e NEW row; soul2perk:61e91997-9b32-123b-ad05-8691afdb81be/01e546ad-6b23-4976-85d2-4d1aa84d3be5 NEW row; soul2perk:61e91997-9b32-123b-ad05-8691afdb81be/01ecf00a-c8b6-4a0b-99e7-df9ad38a1824 NEW row; soul2perk:61e91997-9b32-123b-ad05-8691afdb81be/022467ed-66b0-4fb4-bde6-6c6600c98583 NEW row
- **Text:** 0 strings changed, 28 new
- **Problems:** MakeThemReasonable/Data/MakeThemReasonable.pak!Libs/Tables/rpg/soul2perk.xml: no suffix: replaces the whole vanilla table
- **Risk:** none

## 2049 Simple Ragdoll Physics (P2, Combat / AI)

- **What the author says (Nexus summary):** More Ragdolls, less Kinematics
- **File:** `Semi Functional Ragdoll Physics-2049-3-1772969471.7z` (archive, 35.88 MB, `c_combat-ai`), full (scratch, deleted after reading)
- **Grade:** A changes the most | **perceptibility:** high | **layers:** D0 content/text; D1 data tables (PTF); D2 engine config; D3 Lua scripts
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `zzzxdddbrdp`, supports `*`, loads on 1.9.8: NO (disabled: lists *)
- **Where it changes things:** textures: 274; models/animations/materials: 162; config (.cfg): 56; other xml (data): 54; other: 34; scripts (Lua): 27; docs: 13; tables (PTF): 11; pak (container): 4; localization: 3; manifest: 1; audio: 1; lua identical to vanilla: 0
- **Tables:** ammo, anim_fragment, combat_action_attack, combat_action_fragment_id_mapping, combat_action_sync_attack, hit_reaction, hit_reaction_type, missile_weapon, pickable_item, weapon, weapon_class (2 new rows, 1657 changed, 164 identical to vanilla, 3144 vanilla rows dropped by a whole-table replace); median relative change 0.62
- **Largest changes:** pickable_item:7db6b854-e307-4a47-ba39-943190b2469e price 1->38; pickable_item:c49aa63a-07a6-4417-9f9b-97f2712a4cd0 weight 0.1->0.7; weapon:deb5276d-4926-4545-bdda-f457cac8bc01 agi_req 1->4; pickable_item:802507e9-d620-47b5-ae66-08fcc314e26a price 10->39; weapon_class:/4/f8558fe2-f4cd-4899-932b-82e0e15fa964/3/3/-1/-1/18/9/2 max_attack_distance 45->150; pickable_item:4fd563e5-a44a-4a6e-958d-95bcb196814a price 30->63; ammo:278d26d1-e9a7-4354-84f9-37d20cb72b45 slash_att 0->3; ammo:ad6f0f01-aec4-44d1-982c-1210eb01b74a slash_att 0->0.5
- **Lua:** 27 files, 9122 lines; API used: Script.ReloadScriptx71, entity.Propertiesx55, entity.AIx16, System.GetEntityx11, entity.idx10, XGenAIModule.LootBeginx10
- **Config:** 1032 keys, e.g. WH_AI_LOD_DistanceMax=110, WH_AI_LOD_DistanceMax=130, WH_AI_LOD_DistanceMax=90, WH_AI_LOD_DistanceMin=100, WH_AI_LOD_DistanceMin=60, WH_AI_LOD_DistanceMin=80, a_poseAlignerAnimDrivenBlend=-1, a_poseAlignerEnable=1
- **Text:** 16 strings changed, 3 new
- **Mentions:** states requirements
- **Risk:** MEDIUM: MEDIUM: nested archive (not readable by the game): zzzxdddbrdp/install/DIY Engine/DDDB Do it Yourself Engine Install.7z / MEDIUM: nested archive (not readable by the game): zzzxdddbrdp/install/DIY Engine/sys_spec_Physics.7z / MEDIUM: Lua loadstring/loadfile/dofile in zzzxdddbrdp/Data/zzzxdddbrdp.pak!scripts/PickableItem__zzzxdddbrdp.lua / MEDIUM: nested archive: zzzxdddbrdp/install/DIY Engine/DDDB Do it Yourself Engine Install.7z / MEDIUM: nested archive: zzzxdddbrdp/install/DIY Engine/sys_spec_

## 2340 MatthusTweaks - Equipment and Progression Overhaul (PTF) (P2, Progression / XP / perks)

- **What the author says (Nexus summary):** This mod fixes and rebalances: + Misused items + Layered damage.
- **File:** `MatthusTweaksKCD All In One V1.5 2340 1.5 2026-09-01T23-59Z mDuHaewyB.zip` (archive, 0.08 MB, `c_progression-xp-perks`), full (scratch, deleted after reading)
- **Grade:** A changes the most | **perceptibility:** high | **layers:** D1 data tables (PTF)
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `1.*`, loads on 1.9.8: yes (wildcard)
- **Where it changes things:** tables (PTF): 12; other: 2; manifest: 1; pak (container): 1; lua identical to vanilla: 0
- **Tables:** armor, inventory_preset2item, melee_weapon, ointment_item, perk_rpg_param_override, pickable_item, rpg_param, shop, shop_type2item, skill2item_category, weapon, weapon2weapon_preset (11 new rows, 1621 changed, 54 identical to vanilla, 3672 vanilla rows dropped by a whole-table replace); median relative change 0.559
- **Largest changes:** armor:4fec3673-04fe-45ae-b200-600704ecea70 slash_def 0.1->1.25; pickable_item:413806e7-f3b7-c6cf-2309-e47ce3c97fa2 price 220->5220; pickable_item:4fec3673-04fe-45ae-b200-600704ecea70 price 220->8520; pickable_item:4bef1aa8-1d05-6ecc-7797-083fa321cf80 price 10->28010; pickable_item:41a9ea6a-eed1-471c-754a-196d368245a6 price 10->18010; pickable_item:44f5058a-a445-887b-d443-32fe726b528c price 10->15010; pickable_item:42c04555-15cb-ac3a-aef4-e377a125aca5 price 10->12310; pickable_item:481cfd5b-b646-1c6b-ff58-af749941cf9e price 10->15910
- **Same rows as KRS:** krs_qol:perk_rpg_param_override:01c3b32a-5751-4c98-b6ab-258d02370382/RepairPriceModif; krs_qol:rpg_param:RepairPriceModif; krs_qol:skill2item_category:armor.horse_bridle.*/8; krs_qol:skill2item_category:armor.horse_saddle.*/8
- **Risk:** none

## 1560 Karnages_Durability_Redux (P2, Weapons / armor / items)

- **What the author says (Nexus summary):** Massively increases armor and weapon durability
- **File:** `Karnages_Durability_Redux-1560-1-0-0-1700591696.7z` (archive, 0.06 MB, `c_weapons-armor-items`), full (scratch, deleted after reading)
- **Grade:** A changes the most | **perceptibility:** high | **layers:** D1 data tables (PTF)
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `(none)`, loads on 1.9.8: yes (no version restriction)
- **Where it changes things:** tables (PTF): 2; manifest: 1; pak (container): 1; lua identical to vanilla: 0
- **Tables:** armor, weapon (0 new rows, 964 changed, 22 identical to vanilla); median relative change 9.0
- **Largest changes:** weapon:00000000-0000-0000-0000-000000000005 max_status 1->10; weapon:01b86c1e-1614-4310-8bed-10b7682e5815 max_status 25->250; weapon:033fc7b6-17b6-486d-95cb-a22afb131be2 max_status 50->500; weapon:03589a69-d3f4-403a-a389-ca021e7c8f40 max_status 25->250; weapon:04c2c966-f55b-4afe-b0c2-bfdf4ba0deeb max_status 38->380; weapon:0ad36c8c-cfc7-44ab-8e8f-fe85e7646b71 max_status 81->810; weapon:0d03afe4-9785-44d2-88d2-2c870de8dbfa max_status 25->250; weapon:0eb0ac15-f0d9-49ce-9dd8-b37381a7a508 max_status 73->730
- **Risk:** none

## 1148 Combo and Weapon rebalance (P2, Combat / AI)

- **What the author says (Nexus summary):** Makes weapons weaker (sans polearms, will have to be done with polearms unleashed) and combos stronger.
- **File:** `deadlycombo-1148-1-1605253363.7z` (archive, 0.01 MB, `c_combat-ai`), full (scratch, deleted after reading)
- **Grade:** A changes the most | **perceptibility:** high | **layers:** D1 data tables (PTF)
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `(none)`, loads on 1.9.8: yes (no version restriction)
- **Where it changes things:** tables (PTF): 2; manifest: 1; pak (container): 1; lua identical to vanilla: 0
- **Tables:** combat_sync_action_hit, melee_weapon (0 new rows, 674 changed, 0 identical to vanilla, 90 vanilla rows dropped by a whole-table replace); median relative change 4.377
- **Largest changes:** combat_sync_action_hit:1/39 attack_value_coef 0.1->2.605583991837097; combat_sync_action_hit:27/44 attack_value_coef 0.2->2.706255285624903; combat_sync_action_hit:1/50 attack_value_coef 0.1->2.605583991837097; combat_sync_action_hit:1/51 attack_value_coef 0.1->2.605583991837097; combat_sync_action_hit:1/52 attack_value_coef 0.1->2.605583991837097; combat_sync_action_hit:1/53 attack_value_coef 0.1->2.605583991837097; combat_sync_action_hit:1/54 attack_value_coef 0.1->2.605583991837097; combat_sync_action_hit:1/55 attack_value_coef 0.1->2.605583991837097
- **Risk:** none

## 2219 True Hardcore Crime (PTF) (P2, Crime / stealth / loot)

- **What the author says (Nexus summary):** Fragile lockpicks, tougher pickpocketing, increased noise, harsher punishments, unforgiving reputation, a perk overhaul, and more. More details below.
- **File:** `True Hardcore Crime-2219-1-1-1779142069.zip` (archive, 0.04 MB, `c_crime-stealth-loot`), full (scratch, deleted after reading)
- **Grade:** A changes the most | **perceptibility:** high | **layers:** D0 content/text; D1 data tables (PTF); D3 Lua scripts
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `truehardcorecrime`, supports `(none)`, loads on 1.9.8: yes (no version restriction)
- **Where it changes things:** other: 8; tables (PTF): 8; pak (container): 2; localization: 2; manifest: 1; scripts (Lua): 1; lua identical to vanilla: 0
- **Tables:** buff, food, perk, perk2perk_exclusivity, perk_buff, pickable_item, reputation_change, rpg_param (29 new rows, 515 changed, 0 identical to vanilla, 3297 vanilla rows dropped by a whole-table replace); median relative change 10.0
- **Largest changes:** pickable_item:009e075b-16e2-4666-8f46-e05670783fb9 owner_fading_coef 0.02->1; pickable_item:00d32ef9-77b8-4eb0-b767-388c18e60343 owner_fading_coef 0.02->1; pickable_item:011a4b14-11d8-410d-94b4-c04bf1acf318 owner_fading_coef 0.02->1; pickable_item:049477dc-4b00-4eac-ac45-e5ffdda2f01d owner_fading_coef 0.02->1; pickable_item:052ff90f-e414-4fad-b637-665eddc7de71 owner_fading_coef 0.02->1; pickable_item:05a2745d-c99a-49ea-993a-9bc76897d0b7 owner_fading_coef 0.02->1; pickable_item:06231dba-37ff-45f9-8a9c-609272e4961d owner_fading_coef 0.02->1; pickable_item:070db71a-99f7-4b05-a247-28b964390a7f owner_fading_coef 0.02->1
- **Lua:** 1 files, 536 lines; API used: player.soulx3, player.actorx2, XGenAIModule.SendMessageToEntityDatax2, entity.soulx2, player.thisx2, player.humanx1
- **Text:** 32 strings changed, 4 new
- **Risk:** none

## 2188 True Hardcore Economy (PTF) (P2, Combat / AI)

- **What the author says (Nexus summary):** Shops sell to you at inflated prices and buy from you at drastically lower ones, haggling is more difficult, service costs are through the roof, and poverty is widespread throughout the region. More details below.
- **File:** `True Hardcore Economy-2188-1-3-1779017497.zip` (archive, 0.04 MB, `c_combat-ai`), full (scratch, deleted after reading)
- **Grade:** A changes the most | **perceptibility:** high | **layers:** D0 content/text; D1 data tables (PTF); D3 Lua scripts
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `truehardcoreeconomy`, supports `(none)`, loads on 1.9.8: yes (no version restriction)
- **Where it changes things:** other: 12; tables (PTF): 12; scripts (Lua): 6; pak (container): 2; localization: 2; manifest: 1; lua identical to vanilla: 0
- **Tables:** buff, food, inventory2item, inventory_preset2item, perk_rpg_param_override, pickable_item, reputation_change, rpg_param, sequence, shop, shop_type2item, topic2sequence (62 new rows, 394 changed, 0 identical to vanilla, 107406 vanilla rows dropped by a whole-table replace); median relative change 0.688
- **Largest changes:** inventory2item:5ef63059-322e-4e1b-abe8-926e100c770e amount 340->1800; inventory2item:5ef63059-322e-4e1b-abe8-926e100c770e amount_random_add 30->150; inventory2item:5ef63059-322e-4e1b-abe8-926e100c770e amount 50->250; inventory2item:5ef63059-322e-4e1b-abe8-926e100c770e amount_random_add 1->5; food:d837e829-d706-4db8-8e3d-e70a16882c96 refresh_benefit 4->-10; inventory2item:5ef63059-322e-4e1b-abe8-926e100c770e amount_random_add 1->4; pickable_item:983a6813-20b6-4fc8-bc2d-105939ff6000 price 20->80; inventory2item:5ef63059-322e-4e1b-abe8-926e100c770e amount 340->1200
- **Lua:** 6 files, 2827 lines; API used: player.soulx9, System.Logx8, player.inventoryx7, System.GetEntityByNamex6, XGenAIModule.SendMessageToEntityx5, player.thisx4
- **Text:** 30 strings changed, 0 new
- **Same rows as KRS:** krs_qol:perk_rpg_param_override:01c3b32a-5751-4c98-b6ab-258d02370382/RepairPriceModif; krs_qol:rpg_param:RepairPriceModif
- **Risk:** none

## 651 Better Combat and Immersion Compilation (P2, Combat / AI)

- **What the author says (Nexus summary):** A compilation of mods that aim to improve combat and immersion in KC:D
- **File:** `Better Combat and Immersion Compilation-651-1-6-2-1641836099.zip` (archive, 1.88 MB, `c_combat-ai`), full (scratch, deleted after reading)
- **Grade:** A changes the most | **perceptibility:** high | **layers:** D0 content/text; D1 data tables (PTF); D2 engine config; D3 Lua scripts
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `1.*`, loads on 1.9.8: yes (wildcard)
- **Where it changes things:** textures: 41; other xml (data): 31; localization: 24; pak (container): 16; tables (PTF): 15; other: 7; docs: 2; ui: 2; config (.cfg): 1; manifest: 1; models/animations/materials: 1; scripts (Lua): 1; lua identical to vanilla: 0
- **Tables:** armor, buff, clothing_preset, combat_action_perfect_block, equippable_item, food, inventory_preset2item, perk_rpg_param_override, pickable_item, rpg_param, shop_type2item, skill, social_class, soul_archetype (136 new rows, 308 changed, 29 identical to vanilla, 8207 vanilla rows dropped by a whole-table replace); median relative change 0.571
- **Largest changes:** buff:6741cdd0-837a-4b5c-bad8-fb32f389509d duration 60->1800; buff:7690a860-a843-4609-8a67-9868b87b32b5 duration 300->9000; buff:8503216a-a34c-49f0-aefa-54d4502046f9 duration 60->1800; buff:8f65895d-cbfe-4448-b605-4bb7c36da513 duration 300->9000; buff:976647ae-39b9-45ab-8581-eb61dfb2633b duration 300->9000; buff:a89a0f9e-464d-4d05-a350-732d257d4a3b duration 300->9000; buff:f6720007-689b-4f7c-9c7a-f9abbebcf28c duration 60->1800; buff:f67c12dd-b5f5-4f95-8409-8a5dfe5fb1a1 duration 60->1800
- **Lua:** 1 files, 238 lines; API used: Database.GetTableColumnDatax2, player.soulx2, Database.GetTableInfox1, Database.GetColumnInfox1, player.humanx1, XGenAIModule.SendMessageToEntityx1
- **Config:** 4 keys, e.g. e_viewdistratiolights=400, r_DepthOfFieldMode=0, sys_spec_twtoggle=2, wh_horse_CameraCentering=0
- **Text:** 124 strings changed, 0 new
- **Mentions:** states requirements
- **Same rows as KRS:** krs_items:food:73ff1fde-ec8b-41e9-95e3-b5938c715bf1; krs_items:rpg_param:DigestionSpeed; krs_qol:rpg_param:StrengthToInventoryCapacity
- **Risk:** none

## 2210 True Hardcore Alchemy (PTF) (P2, Combat / AI)

- **What the author says (Nexus summary):** Reduces the error tolerance of alchemy, rebalances potions and alchemy perks, and removes the exploit that allows a single potion to be applied to multiple food items. More details below.
- **File:** `True Hardcore Alchemy-2210-1-2-1778440238.zip` (archive, 0.03 MB, `c_combat-ai`), full (scratch, deleted after reading)
- **Grade:** A changes the most | **perceptibility:** high | **layers:** D0 content/text; D1 data tables (PTF); D3 Lua scripts
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `truehardcorealchemy`, supports `(none)`, loads on 1.9.8: yes (no version restriction)
- **Where it changes things:** other: 5; tables (PTF): 5; pak (container): 2; localization: 2; manifest: 1; scripts (Lua): 1; lua identical to vanilla: 0
- **Tables:** buff, divisible_item, food, pickable_item, rpg_param (8 new rows, 214 changed, 0 identical to vanilla, 3093 vanilla rows dropped by a whole-table replace); median relative change 0.8
- **Largest changes:** pickable_item:eec58bfb-063e-4838-b78d-3c2b354f1346 price 1->100; buff:25bdbc39-c19a-4a11-8c0f-6e16c432846f duration 600->14400; buff:db397470-27c5-4a3a-9717-1b3b5f42377a duration 600->43200; food:8b713d0c-9a04-4354-a53f-ffd384057fa6 refresh_benefit 4->-10; food:d837e829-d706-4db8-8e3d-e70a16882c96 refresh_benefit 4->-10; food:eca88106-4bab-4419-8772-4450739c193c refresh_benefit 4->-10; food:2668d311-8667-4f27-b94b-7f6175678f17 refresh_benefit 4->-5; food:6b955a9b-d8de-492c-a53e-a052fab4ff0a refresh_benefit 4->-5
- **Lua:** 1 files, 3127 lines; API used: player.soulx1
- **Text:** 38 strings changed, 3 new
- **Same rows as KRS:** krs_items:food:73ff1fde-ec8b-41e9-95e3-b5938c715bf1; krs_qol:rpg_param:HerbGatherSkillToRadius
- **Risk:** none

## 1563 Karnages_Polearm_Restoration 2.0 (P2, Weapons / armor / items)

- **What the author says (Nexus summary):** Restores Polearm Skill and adds Polearms to Blacksmiths
- **File:** `Karnages_Polearm_Restoration 2.0-1563-1-0-0-1700618380.7z` (archive, 0.21 MB, `c_weapons-armor-items`), full (scratch, deleted after reading)
- **Grade:** A changes the most | **perceptibility:** high | **layers:** D0 content/text; D1 data tables (PTF); D3 Lua scripts
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `(none)`, loads on 1.9.8: yes (no version restriction)
- **Where it changes things:** tables (PTF): 28; models/animations/materials: 5; scripts (Lua): 4; other: 4; localization: 2; manifest: 1; pak (container): 1; other xml (data): 1; lua identical to vanilla: 0
- **Tables:** combat_action_attack, combat_action_guard_movement, combat_action_perfect_block, combat_action_pose_modifier, combat_action_sync_attack, combat_action_sync_hit, combat_action_sync_pb_hit, combat_combo, combat_sync_action_hit, combat_weapon_group_to_class, melee_weapon, mn_fragment, perk, shop_type2i (164 new rows, 47 changed, 175 identical to vanilla, 6636 vanilla rows dropped by a whole-table replace); median relative change 0.206
- **Largest changes:** weapon:405c1865-413d-43b8-8db9-c44a0eefd350 max_status 15->500; weapon:49fa5ec9-92a9-4bfb-b56e-a33d04b69ee1 max_status 25->500; weapon:4bd249c6-0fea-4296-b60a-8d8a56ce76e6 max_status 1->500; weapon:7377215a-a0ca-44a2-b11a-113a024191ca max_status 26->500; weapon:033fc7b6-17b6-486d-95cb-a22afb131be2 max_status 50->500; weapon:8ef902ea-0c32-44c9-b101-71f35b9cbe3d max_status 50->500; weapon:0f5be0ac-ff11-4a01-a7f4-bf8e84c2e31b max_status 55->500; weapon:d289be6f-a7cb-44b2-b2d0-a0a45105ef98 max_status 65->500
- **Lua:** 4 files, 40 lines; API used: entity.humanx2, entity.actorx2, System.AddCCommandx2, Script.ReloadScriptx2, System.ExecuteCommandx2
- **Text:** 0 strings changed, 7 new
- **Risk:** none

## 1736 Rogue Life (P2, Progression / XP / perks)

- **What the author says (Nexus summary):** Adds perks to the Stealth, Alchemy, Speech, Drinking and Bow trees and adjusts vanilla perks; recommends Perkaholic A collection of modules to balance and enhance stealth play.
- **File:** `RogueLife-1736-V1-1-1739826542.7z` (archive, 0.02 MB, `c_progression-xp-perks`), full (scratch, deleted after reading)
- **Grade:** A changes the most | **perceptibility:** high | **layers:** D0 content/text; D1 data tables (PTF); D3 Lua scripts
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `1.9.6`, loads on 1.9.8: NO (disabled: lists 1.9.6)
- **Where it changes things:** tables (PTF): 23; localization: 16; manifest: 10; pak (container): 10; other xml (data): 2; docs: 1; scripts (Lua): 1; lua identical to vanilla: 0
- **Tables:** buff, buff_class, perk, perk2perk_exclusivity, perk_buff, reputation_change, sequence (53 new rows, 16 changed, 1 identical to vanilla, 60014 vanilla rows dropped by a whole-table replace); median relative change 2.0
- **Largest changes:** buff:f699eef9-c4fd-48b5-8793-3a3c16374729 NEW row; buff:c145ad4e-24c0-48de-b15e-123bab6838c4 NEW row; buff:be55fa8b-f094-4111-862d-9afef130c9a1 NEW row; buff:f789e376-f621-4fcf-815f-73bfcbba08fb NEW row; perk_buff:d2014e01-391d-4264-9ddb-c7fb1b22074a/f699eef9-c4fd-48b5-8793-3a3c16374729 NEW row; perk_buff:a2c0167b-80b6-464a-b354-accea6947384/c145ad4e-24c0-48de-b15e-123bab6838c4 NEW row; perk_buff:a8886461-c5ec-40c1-9bbb-2e3bb91b9cfe/be55fa8b-f094-4111-862d-9afef130c9a1 NEW row; perk_buff:ba09e059-7fbb-4841-b7c3-eb77dc1323b9/f789e376-f621-4fcf-815f-73bfcbba08fb NEW row
- **Lua:** 1 files, 19 lines; API used: player.soulx2, Game.SendInfoTextx1
- **Text:** 9 strings changed, 30 new
- **Mentions:** user.cfg
- **Problems:** RogueLife/TyburnBiancaSchnapps/Data/TyburnBiancaSchnapps.pak!Libs/Tables/text/sequence__TyburnBiancaSchnapps.xml: suffix 'TyburnBiancaSchnapps' != id 'tyburnalchemyperks' (the game ignores it) / RogueLife/TyburnBowPerks/Data/TyburnBowPerks.pak!Libs/Tables/rpg/buff__TyburnBowPerks.xml: suffix 'TyburnBowPerks' != id 'tyburnalchemyperks' (the game ignores it) / RogueLife/TyburnBowPerks/Data/TyburnBowPerks.pak!Libs/Tables/rpg/perk_buff__TyburnBowPerks.xml: suffix 'TyburnBowPerks' != id 'tyburnalchemyperks' (the game ignores it) / RogueLife/TyburnBowPerks/Data/TyburnBowPerks.pak!Libs/Tables/rpg/per
- **Risk:** none

## 2208 Medieval Poisons - True Hardcore Compatibility Patch (PTF) (P2, Combat / AI)

- **What the author says (Nexus summary):** A compatibility patch for 'Medieval Poisons', designed to work seamlessly with the 'True Hardcore' mod series. More details below.
- **File:** `patch True Hardcore Medieval Poisons-2208-1-1-1778440401.zip` (archive, 0.02 MB, `c_combat-ai`), full (scratch, deleted after reading)
- **Grade:** A changes the most | **perceptibility:** high | **layers:** D0 content/text; D1 data tables (PTF); D3 Lua scripts
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `patchtruehardcoremedievalpoisons`, supports `(none)`, loads on 1.9.8: yes (no version restriction)
- **Where it changes things:** other: 6; tables (PTF): 6; pak (container): 2; localization: 2; manifest: 1; scripts (Lua): 1; lua identical to vanilla: 0
- **Tables:** buff, document, document_required_skill, food, inventory2item, rpg_param (28 new rows, 13 changed, 0 identical to vanilla, 2151 vanilla rows dropped by a whole-table replace); median relative change 0.7
- **Largest changes:** buff:25bdbc39-c19a-4a11-8c0f-6e16c432846f duration 600->14400; buff:db397470-27c5-4a3a-9717-1b3b5f42377a duration 600->43200; food:8b713d0c-9a04-4354-a53f-ffd384057fa6 refresh_benefit 4->-10; buff:15387b1a-7f7e-4462-8ce6-ea652f0e182e duration 3600->10800; inventory2item:bce052d2-74b4-467c-af73-cf14b1f6fed8 NEW row; document:bce052d2-74b4-467c-af73-cf14b1f6fed8 NEW row; food:eec58bfb-063e-4838-b78d-3c2b354f1346 health_benefit 0->-20; food:1e482524-0e66-49e1-a3cc-e09e0c029afa NEW row
- **Lua:** 1 files, 3127 lines; API used: player.soulx1
- **Text:** 28 strings changed, 73 new
- **Risk:** none

## 1839 Realistic Horses (P2, Horses)

- **What the author says (Nexus summary):** Reduce horse carrying capacity to add realism and inventory management
- **File:** `Realistic Horses-1839-1-0-1739145195.rar` (archive, 0.08 MB, `_quarantine`), full (scratch, deleted after reading)
- **Grade:** A changes the most | **perceptibility:** high | **layers:** D1 data tables (PTF); D3 Lua scripts
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `1.*`, loads on 1.9.8: yes (wildcard)
- **Where it changes things:** scripts (Lua): 24; tables (PTF): 4; manifest: 1; pak (container): 1; lua identical to vanilla: 0
- **Tables:** buff, equippable_item, rpg_param, soul (1 new rows, 26 changed, 0 identical to vanilla, 6620 vanilla rows dropped by a whole-table replace); median relative change 0.7
- **Largest changes:** equippable_item:41382adf-569c-4f33-90a0-36b6e874eca7 rpg_buff_weight 0.05->0.4; equippable_item:475642da-17e6-c06e-b035-2b1ab31cbb8f rpg_buff_weight 0.1->0.45; equippable_item:45e2b460-dbd4-4bf4-3643-33c2648d60bc rpg_buff_weight 0.15->0.5; equippable_item:4692f1e5-e4bc-c8af-1b0b-1da823ec1db9 rpg_buff_weight 0.2->0.55; equippable_item:42b152d3-d3f4-b390-088e-3127534281aa rpg_buff_weight 0.25->0.6; equippable_item:43c85848-0181-06b6-a870-2b3c951e8aa8 rpg_buff_weight 0.3->0.65; rpg_param:StrengthToInventoryCapacity NEW row; equippable_item:4838fa1c-da32-9c55-b20b-d4b17b70ecac rpg_buff_weight 0.35->0.7
- **Lua:** 24 files, 6807 lines; API used: player.soulx48, System.ExecuteCommandx24, player.inventoryx22, entity.soulx11, Script.SetTimerx10, Database.LoadTablex9
- **Same rows as KRS:** krs_qol:rpg_param:StrengthToInventoryCapacity
- **Risk:** HIGH: HIGH: mod Lua loads code dynamically (loadstring/loadfile) and opens files (io.open): a script framework, not a data tweak / MEDIUM: Lua io.open in Realistic_Horse/Data/Realistic_Horse.pak!Scripts/cheat_console.lua / MEDIUM: Lua loadstring/loadfile/dofile in Realistic_Horse/Data/Realistic_Horse.pak!Scripts/cheat_console.lua / MEDIUM: Lua io.open in Realistic_Horse/Data/Realistic_Horse.pak!Scripts/cheat_core_exec.lua / MEDIUM: Lua loadstring/loadfile/dofile in Realistic_Horse/Data/Realistic_Horse (quarantined)

## 2338 Horse Collision Mod (P2, Horses)

- **What the author says (Nexus summary):** Horse collision reactions by speed; no vanilla file replaced This mod adds animations and physical reactions with immersive detail when Henry collides with NPCs while on horseback as well as new horsemanship perks .
- **File:** `HorseCollisionMod 2338 6.0.0 2026-09-30T04-12Z vicgJRjyv.zip` (archive, 0.19 MB, `c_horses`), full (scratch, deleted after reading)
- **Grade:** A changes the most | **perceptibility:** high | **layers:** D0 content/text; D1 data tables (PTF); D3 Lua scripts
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `1.9.*`, loads on 1.9.8: yes (wildcard)
- **Where it changes things:** scripts (Lua): 22; other xml (data): 4; tables (PTF): 4; models/animations/materials: 3; localization: 2; manifest: 1; docs: 1; pak (container): 1; lua identical to vanilla: 0
- **Tables:** buff, perk, perk_soul_ability, soul_ability (11 new rows, 0 changed, 0 identical to vanilla, 1097 vanilla rows dropped by a whole-table replace); median relative change 0.0
- **Largest changes:** buff:a8d30cd4-d7ae-4b58-a726-d94a875c50e8 NEW row; buff:488afdee-b2bb-4d94-8357-d923f40d65ef NEW row; perk:13ed04b3-297d-43ca-9fb8-d3a3a1192f9c NEW row; perk:da38020a-eecf-45b5-8203-34b0b678600a NEW row; perk:6a0ca946-cce5-4c2b-831a-585db059027d NEW row; perk_soul_ability:13ed04b3-297d-43ca-9fb8-d3a3a1192f9c/8 NEW row; perk_soul_ability:da38020a-eecf-45b5-8203-34b0b678600a/9 NEW row; perk_soul_ability:6a0ca946-cce5-4c2b-831a-585db059027d/11 NEW row
- **Lua:** 22 files, 13211 lines; API used: Script.SetTimerx50, Script.ReloadScriptx40, player.soulx18, XGenAIModule.SendMessageToEntityDatax7, System.GetEntitiesInSpherex7, player.humanx7
- **Text:** 0 strings changed, 10 new
- **Mentions:** Vortex
- **Risk:** none

## 2246 Console Editable RpgParams (P2, Progression / XP / perks)

- **What the author says (Nexus summary):** Makes rpg parameters editable from the console at any time; the search returned the KCD2 page, so the KCD1 page is unconfirmed Expose rpgparams to console, you can set them and see them come into effect in real time
- **File:** `Console Editable RpgParams 2246 3 2026-06-29T13-59Z gZWc5POkF.zip` (archive, 3.04 MB, `_quarantine`), full (scratch, deleted after reading)
- **Grade:** A changes the most | **perceptibility:** none | **layers:** D4 native/external
- **How it installs:** unclear: read the archive's own instructions; manifest id `-`, supports `-`, loads on 1.9.8: no manifest (legacy install)
- **Where it changes things:** executables/scripts: 1; other: 1; lua identical to vanilla: 0
- **Native file, read statically (never run):** KCSE/Plugins/ConsoleRpgParam.dll=f84e6224b289f9e1 | KCSE/Plugins/ConsoleRpgParam.dll: suspicious strings: none; game-related strings: kcse_rpgparam_ / [ConsoleRpgParam] Registered %d float + %d int RPG params as CVars / kcd_re REL::IDDatabase / kcd_addresslib_ / This plugin is incompatible with the current game build. / D:\a\libKCD1\libKCD1\.buildenv\build\ConsoleRpgParam\ConsoleRpgParam.pdb / ConsoleRpgParam.dll / KCSEPlugin_Load / KCSEPlugin_Version / Console RPG Params / _configure_narrow_argv
- **Risk:** HIGH: HIGH: native binary by magic bytes: KCSE/Plugins/ConsoleRpgParam.dll / HIGH: native code file: KCSE/Plugins/ConsoleRpgParam.dll (quarantined)

## 2326 Permanent Death (P2, Progression / XP / perks)

- **What the author says (Nexus summary):** Pick how many lives a playthrough gets. Spend them all - and that run is over.
- **File:** `Permadeath 0.91 2326 0.91 2026-08-09T14-26Z aSoQ0kcTE.zip` (archive, 0.19 MB, `_quarantine`), full (scratch, deleted after reading)
- **Grade:** A changes the most | **perceptibility:** high | **layers:** D0 content/text; D3 Lua scripts; D4 native/external
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `(none)`, loads on 1.9.8: yes (no version restriction)
- **Where it changes things:** localization: 4; executables/scripts: 3; other xml (data): 2; docs: 1; manifest: 1; pak (container): 1; scripts (Lua): 1; lua identical to vanilla: 0
- **Lua:** 1 files, 334 lines; API used: System.LogAlwaysx15, Script.SetTimerx9, System.AddCCommandx7, System.ExecuteCommandx6, player.soulx4, Game.SendInfoTextx2
- **Text:** 0 strings changed, 18 new
- **Native file, read statically (never run):** _dll/LightFX64.dll=efe39ec64a14d00d | _dll/LightFX64.dll: suspicious strings: none; game-related strings: playline hooks installed on  / no playline observed -- file hooks may not be installed /  matches in .text -- refusing to patch this build of WHGame.dll / game-over hook installed / WHGame.dll never appeared -- no game-over hook
- **Risk:** HIGH: HIGH: native binary by magic bytes: _dll/LightFX64.dll / HIGH: script or shortcut file: Install-Permadeath.cmd / HIGH: script or shortcut file: Uninstall-Permadeath.cmd / HIGH: native code file: _dll/LightFX64.dll (quarantined)

## 2348 KCD Zero Durability Repair (P2, Weapons / armor / items)

- **What the author says (Nexus summary):** Allows repair craftsmen to repair items with zero durability through the standard repair menu.
- **File:** `KcdZeroDurabilityRepair Release 2348 1 2026-09-03T11-13Z 8HMDLo1kO.zip` (archive, 0.01 MB, `_quarantine`), full (scratch, deleted after reading)
- **Grade:** A changes the most | **perceptibility:** none | **layers:** D4 native/external
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `(none)`, loads on 1.9.8: yes (no version restriction)
- **Where it changes things:** executables/scripts: 1; manifest: 1; other: 1; lua identical to vanilla: 0
- **Native file, read statically (never run):** KcdZeroDurabilityRepair.asi=52929cf9bb98c8d5 | KcdZeroDurabilityRepair.asi: suspicious strings: none; game-related strings: repair transaction validation / zero-health override path / [init] MinHook initialization failed: %s / [hook] repair check active at %p (object=%p vtable=%p) / [hook] repair check hook failed at %p: %s / [hook] repair check unresolved: object=%p vtable=%p / [init] active at %p; global zero-health repair override enabled / _configure_narrow_argv
- **Risk:** HIGH: HIGH: native binary by magic bytes: KcdZeroDurabilityRepair.asi / HIGH: native code file: KcdZeroDurabilityRepair.asi (quarantined)

## 2359 KCD Kombat Tune (P2, Combat / AI)

- **What the author says (Nexus summary):** Scales enemy block/riposte/dodge by comparing Warfare and agility of both sides; needs Ultimate ASI Loader (native plugin). The build string czj4 is the one of the 1.9.8 install Enemies scale to the matchup. Higher Warfare and agility than your opponent means fewer of their perfect blocks, master st
- **File:** `KcdCombatTune 2359 3 2026-09-12T07-45Z FksyYJVBR.zip` (archive, 0.24 MB, `_quarantine`), full (scratch, deleted after reading)
- **Grade:** A changes the most | **perceptibility:** none | **layers:** D4 native/external
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `(none)`, loads on 1.9.8: yes (no version restriction)
- **Where it changes things:** executables/scripts: 2; other: 2; manifest: 1; lua identical to vanilla: 0
- **Native file, read statically (never run):** KcdCombatTune.asi=171e86758a911177 KCDT.asi=26e01ad1e9913a43 | KcdCombatTune.asi: suspicious strings: none; game-related strings: KCDT.asi / KCDT_GetVersion / KCDT_IsReady / KCDT_GetGameBase / KCDT_InstallHook / KCDT_ReadMemory / KCDT_ReadCString / KCDT_Log / KCDT_BrainActor / KCDT_ActorSoul / KCDT_SoulSkill / KCDT_SoulStat / KCDT_DefenseWeights / KCDT_SetDefenseOverride // KCDT.asi: suspicious strings: none; game-related strings: masterStrike / inventory.hook.failed / init.inventory.hook.installed / inventory.hook.ready / item.transfer.hook.ready / item.transfer.hook.failed / input.action.hook.ready / input.action.hook.failed / input.registration.hook.ready / input.registration.hook.failed / input.map.creation.hook.ready / input.map.creation.hook.faile
- **Risk:** HIGH: HIGH: native binary by magic bytes: KcdCombatTune.asi / HIGH: native binary by magic bytes: KCDT.asi / HIGH: native code file: KcdCombatTune.asi / HIGH: native code file: KCDT.asi (quarantined)

## 1483 TSM Slower Food Spoil (P2, Alchemy / food / survival)

- **What the author says (Nexus summary):** Food durability x2 (recommended), x3 or x5; needs the From the Ashes DLC. (The same summary also named another title for the id; treat as unreliable) Extends the expiration date on all foodstuffs, either by 2X (recommended), 3X, or 5X.
- **File:** `TSM Splower Food Spoil-1483-1-0-1677271171.7z` (archive, 0.02 MB, `c_alchemy-food-survival`), full (scratch, deleted after reading)
- **Grade:** B large | **perceptibility:** high | **layers:** D1 data tables (PTF)
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `(none)`, loads on 1.9.8: yes (no version restriction)
- **Where it changes things:** manifest: 3; pak (container): 3; tables (PTF): 3; docs: 1; lua identical to vanilla: 0
- **Tables:** food (0 new rows, 333 changed, 0 identical to vanilla, 273 vanilla rows dropped by a whole-table replace); median relative change 2.0
- **Largest changes:** food:025f546b-7465-4070-a57d-e84852adc184 decay_time_hours 120->600; food:0368a199-117e-4079-b182-b042360c7d61 decay_time_hours 120->600; food:0686c001-d42b-467c-b3de-f87beb915c68 decay_time_hours 120->600; food:06be2a3d-4e05-4a78-85cd-33879cd669c9 decay_time_hours 24->120; food:0712d873-29bd-4fdd-8966-79aefb82c829 decay_time_hours 120->600; food:0a78fe34-737c-4346-9762-6b3036fbc9c6 decay_time_hours 24->120; food:0b4e244a-e3de-4502-afd0-fb7fe309629a decay_time_hours 48->240; food:0fc6cac7-29e6-4753-8873-0bcbbeba5548 decay_time_hours 24->120
- **Risk:** none

## 2011 Chefs Kiss (P2, Alchemy / food / survival)

- **What the author says (Nexus summary):** UI supported - New rules for foods, drinks, potions, poisons, health regen, stamina regen, weapon and stat buffs, nutrition, energy, starvation and more
- **File:** `Chefs Kiss 2011 3.7 2026-06-21T22-06Z HM0uQNJkR.7z` (archive, 0.03 MB, `c_alchemy-food-survival`), full (scratch, deleted after reading)
- **Grade:** B large | **perceptibility:** high | **layers:** D0 content/text; D1 data tables (PTF)
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `dddb_chefs_kiss`, supports `*`, loads on 1.9.8: NO (disabled: lists *)
- **Where it changes things:** tables (PTF): 7; localization: 3; manifest: 1; docs: 1; pak (container): 1; lua identical to vanilla: 0
- **Tables:** buff, buff_class, consumable_item, food, item, pickable_item, potion (56 new rows, 267 changed, 106 identical to vanilla, 4976 vanilla rows dropped by a whole-table replace); median relative change 1.0
- **Largest changes:** food:22eb16a0-1175-4e2e-a951-33d362e288fb max_status 2->200; food:28a7c5cd-d80d-4167-ba1b-fcfc520c40b7 max_status 1->44; food:006ec8d6-1ce1-4e90-8267-7c349812ddcd nutrition_benefit 1->-20; food:7c5126cd-b010-4484-8465-22a3d69fa0df refresh_benefit -2->24; food:390c0dc8-23fd-42a0-91f2-a4d42f96a387 refresh_benefit -2->18; food:0a78fe34-737c-4346-9762-6b3036fbc9c6 max_status 1->70; food:bd6a9ffc-68b6-4222-b7fd-7bd72634b712 refresh_benefit -2->19; food:fdd2036c-15a6-462e-9a0e-acbe20288bcc refresh_benefit -2->20
- **Text:** 94 strings changed, 44 new
- **Same rows as KRS:** krs_items:food:73ff1fde-ec8b-41e9-95e3-b5938c715bf1
- **Risk:** none

## 85 Perkaholic (P2, Progression / XP / perks)

- **What the author says (Nexus summary):** Adds additional perks to existing perk lists as well as adding perks to the Bow, Polearm and Unarmed skills.
- **File:** `Perkaholic 1.05-85-1-05.zip` (archive, 2.48 MB, `c_progression-xp-perks`), full (scratch, deleted after reading)
- **Grade:** B large | **perceptibility:** high | **layers:** D0 content/text; D1 data tables (PTF)
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `1.3 1.3.1`, loads on 1.9.8: NO (disabled: lists 1.3, 1.3.1)
- **Where it changes things:** localization: 12; other: 6; tables (PTF): 6; docs: 2; config (.cfg): 1; manifest: 1; pak (container): 1; other xml (data): 1; lua identical to vanilla: 0
- **Tables:** buff, perk, perk2perk_exclusivity, perk_buff, perk_buff_override, skill (188 new rows, 86 changed, 949 identical to vanilla, 156 vanilla rows dropped by a whole-table replace); median relative change 0.4
- **Largest changes:** buff:8190c0af-e298-4a4c-b0d4-5c1572ca53c2 NEW row; buff:44d83d20-9709-4e54-9b7d-9b6bcfb630be NEW row; buff:44d83d21-9709-4e54-9b7d-9b6bcfb630be NEW row; buff:44d83d22-9709-4e54-9b7d-9b6bcfb630be NEW row; buff:44d83d23-9709-4e54-9b7d-9b6bcfb630be NEW row; buff:44d83d24-9709-4e54-9b7d-9b6bcfb630be NEW row; buff:44d83d25-9709-4e54-9b7d-9b6bcfb630be NEW row; buff:44d83d26-9709-4e54-9b7d-9b6bcfb630be NEW row
- **Text:** 182 strings changed, 159 new
- **Problems:** Mods/perkaholic/Data/zzz_perkaholic.pak!Libs/Tables/rpg/buff.xml: no suffix: replaces the whole vanilla table / Mods/perkaholic/Data/zzz_perkaholic.pak!Libs/Tables/rpg/perk.xml: no suffix: replaces the whole vanilla table / Mods/perkaholic/Data/zzz_perkaholic.pak!Libs/Tables/rpg/perk2perk_exclusivity.xml: no suffix: replaces the whole vanilla table / Mods/perkaholic/Data/zzz_perkaholic.pak!Libs/Tables/rpg/perk_buff.xml: no suffix: replaces the whole vanilla table / Mods/perkaholic/Data/zzz_perkaholic.pak!Libs/Tables/rpg/perk_buff_override.xml: no suffix: replaces the whole vanilla table / Mods
- **Risk:** none

## 1112 Combat Overhaul (P2, Combat / AI)

- **What the author says (Nexus summary):** Makes directional combat matter.
- **File:** `combatoverhaul-1112-1-6-4-1603868865.7z` (archive, 0.02 MB, `c_combat-ai`), full (scratch, deleted after reading)
- **Grade:** B large | **perceptibility:** high | **layers:** D1 data tables (PTF)
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `(none)`, loads on 1.9.8: yes (no version restriction)
- **Where it changes things:** tables (PTF): 5; manifest: 1; pak (container): 1; lua identical to vanilla: 0
- **Tables:** combat_action_perfect_block, combat_attack_type, perk_rpg_param_override, rpg_param, soul (226 new rows, 17 changed, 14 identical to vanilla, 5568 vanilla rows dropped by a whole-table replace); median relative change 0.54
- **Largest changes:** combat_action_perfect_block:14/1/1/CombatBlockPerfect/4/1/0/3/-1/0/4/7/4/-1/1/-1/-1/-1/-1/-1/4/-1/1 NEW row; combat_action_perfect_block:14/1/0/CombatBlockPerfect/2/1/0/3/-1/0/2/7/4/-1/1/-1/-1/-1/-1/-1/4/-1/0 NEW row; combat_action_perfect_block:14/1/0/CombatBlockPerfect/3/1/0/4/-1/0/3/7/4/-1/1/-1/-1/-1/-1/-1/4/-1/0 NEW row; combat_action_perfect_block:14/1/2/CombatBlockPerfect/3/1/0/4/-1/0/1/7/4/-1/1/-1/-1/-1/-1/-1/4/-1/1 NEW row; combat_action_perfect_block:14/1/1/CombatBlockPerfect/0/1/0/3/-1/0/0/7/4/-1/1/-1/-1/-1/-1/-1/4/-1/2 NEW row; combat_action_perfect_block:14/1/1/CombatBlockPerfect/2/1/0/3/-1/0/0/7/4/-1/1/-1/-1/-1/-1/-1/4/-1/1 NEW row; combat_action_perfect_block:14/1/0/CombatBlock
- **Risk:** none

## 2179 True Hardcore Combat (PTF) (P2, Combat / AI)

- **What the author says (Nexus summary):** Makes combat more realistic, aggressive and combo-centered. Improves archery with faster bows and arrows, but makes it more punishing when you're weak. More details below.
- **File:** `True Hardcore Combat-2179-1-3-1778946895.zip` (archive, 0.02 MB, `c_combat-ai`), full (scratch, deleted after reading)
- **Grade:** B large | **perceptibility:** high | **layers:** D0 content/text; D1 data tables (PTF)
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `truehardcorecombat`, supports `(none)`, loads on 1.9.8: yes (no version restriction)
- **Where it changes things:** other: 11; tables (PTF): 11; localization: 2; manifest: 1; pak (container): 1; lua identical to vanilla: 0
- **Tables:** ammo, buff, food, morale_change, perk2perk_exclusivity, perk_rpg_param_override, pickable_item, rpg_movement_type, rpg_param, social_class, soul_archetype (72 new rows, 148 changed, 0 identical to vanilla, 3046 vanilla rows dropped by a whole-table replace); median relative change 0.4
- **Largest changes:** rpg_param:SkillToDefense rpg_param_value 0.02857->0.2857; food:3157d51d-7461-4fdc-9601-93bd5ed42156 refresh_benefit 4->-3; food:567fc1b1-1424-4784-9da8-5104e2e7354d refresh_benefit 4->-3; food:850d28d9-9d0a-4b2e-9feb-e6c48c5f1aad refresh_benefit 4->-3; ammo:13ba7468-11a2-483d-8cb9-25ce36a2d228 stab_att 0->1; ammo:a5b31bbc-1e11-4831-835b-c06d5b13a7da slash_att 0->1; ammo:c49aa63a-07a6-4417-9f9b-97f2712a4cd0 stab_att 0->1; ammo:c70cbea8-64fc-4309-b559-6b1ed76ea9d4 stab_att 0->10
- **Text:** 36 strings changed, 0 new
- **Risk:** none

## 1009 Perkaholic - PTF updated (1.9.4-1.9.8) (P2, Progression / XP / perks)

- **What the author says (Nexus summary):** Adds additional perks to existing perk lists as well as adding perks to the Bow, Polearm and Unarmed skills. 56 in total.
- **File:** `Perkaholic PTF-1009-1-2-3-1714642782` (folder (already extracted), 0 MB, `c_progression-xp-perks`), read in place (already extracted by the author)
- **Grade:** B large | **perceptibility:** high | **layers:** D0 content/text; D1 data tables (PTF)
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `1.9.4 1.9.5 1.9.6 1.9.7`, loads on 1.9.8: NO (disabled: lists 1.9.4, 1.9.5, 1.9.6, 1.9.7)
- **Where it changes things:** localization: 26; tables (PTF): 6; manifest: 1; other: 1; lua identical to vanilla: 0
- **Tables:** buff, perk, perk2perk_exclusivity, perk_buff, perk_buff_override, skill (187 new rows, 7 changed, 1 identical to vanilla, 1183 vanilla rows dropped by a whole-table replace); median relative change 0.25
- **Largest changes:** buff:44d83d20-9709-4e54-9b7d-9b6bcfb630be NEW row; buff:44d83d21-9709-4e54-9b7d-9b6bcfb630be NEW row; buff:44d83d22-9709-4e54-9b7d-9b6bcfb630be NEW row; buff:44d83d23-9709-4e54-9b7d-9b6bcfb630be NEW row; buff:44d83d24-9709-4e54-9b7d-9b6bcfb630be NEW row; buff:44d83d25-9709-4e54-9b7d-9b6bcfb630be NEW row; buff:44d83d26-9709-4e54-9b7d-9b6bcfb630be NEW row; buff:44d83d27-9709-4e54-9b7d-9b6bcfb630be NEW row
- **Text:** 130 strings changed, 1482 new
- **Problems:** Data/Tables/rpg/buff__perkaholic.xml: table patch outside Libs/Tables (the game looks for Libs/Tables only) / Data/Tables/rpg/perk2perk_exclusivity__perkaholic.xml: table patch outside Libs/Tables (the game looks for Libs/Tables only) / Data/Tables/rpg/perk_buff_override__perkaholic.xml: table patch outside Libs/Tables (the game looks for Libs/Tables only) / Data/Tables/rpg/perk_buff__perkaholic.xml: table patch outside Libs/Tables (the game looks for Libs/Tables only) / Data/Tables/rpg/perk__perkaholic.xml: table patch outside Libs/Tables (the game looks for Libs/Tables only) / Data/Tables/rp
- **Risk:** MEDIUM: MEDIUM: nested archive (not readable by the game): Data/perkaholic.7zip

## 1009 Perkaholic - PTF updated (1.9.4-1.9.8) (P2, Progression / XP / perks)

- **What the author says (Nexus summary):** Adds additional perks to existing perk lists as well as adding perks to the Bow, Polearm and Unarmed skills. 56 in total.
- **File:** `Perkaholic PTF-1009-1-2-3-1780997771.rar` (archive, 0.08 MB, `c_progression-xp-perks`), full (scratch, deleted after reading)
- **Grade:** B large | **perceptibility:** high | **layers:** D0 content/text; D1 data tables (PTF)
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `1.9.4 1.9.5 1.9.6 1.9.7 1.9.8 1.9.9`, loads on 1.9.8: yes (explicit)
- **Where it changes things:** localization: 26; tables (PTF): 6; manifest: 1; pak (container): 1; lua identical to vanilla: 0
- **Tables:** buff, perk, perk2perk_exclusivity, perk_buff, perk_buff_override, skill (187 new rows, 7 changed, 1 identical to vanilla, 1183 vanilla rows dropped by a whole-table replace); median relative change 0.25
- **Largest changes:** buff:44d83d20-9709-4e54-9b7d-9b6bcfb630be NEW row; buff:44d83d21-9709-4e54-9b7d-9b6bcfb630be NEW row; buff:44d83d22-9709-4e54-9b7d-9b6bcfb630be NEW row; buff:44d83d23-9709-4e54-9b7d-9b6bcfb630be NEW row; buff:44d83d24-9709-4e54-9b7d-9b6bcfb630be NEW row; buff:44d83d25-9709-4e54-9b7d-9b6bcfb630be NEW row; buff:44d83d26-9709-4e54-9b7d-9b6bcfb630be NEW row; buff:44d83d27-9709-4e54-9b7d-9b6bcfb630be NEW row
- **Text:** 130 strings changed, 1482 new
- **Risk:** none

## 770 Perkaholic updated (P2, Progression / XP / perks)

- **What the author says (Nexus summary):** Adds additional perks to existing perk lists as well as adding perks to the Bow, Polearm and Unarmed skills. Updated for 1.9.* (All credits for the mod creation to Xylosi, I just updated the mod to work with 1.9)
- **File:** `Perkaholic 1.07-770-1-07-1561341650.zip` (archive, 0.11 MB, `_quarantine`), full (scratch, deleted after reading)
- **Grade:** B large | **perceptibility:** high | **layers:** D0 content/text; D1 data tables (PTF)
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `(none)`, loads on 1.9.8: yes (no version restriction)
- **Where it changes things:** other: 10; tables (PTF): 5; localization: 2; manifest: 1; pak (container): 1; lua identical to vanilla: 0
- **Tables:** buff, perk, perk_buff, perk_buff_override (184 new rows, 2 changed, 1156 identical to vanilla); median relative change 0.25
- **Largest changes:** perk_buff_override:010b08d9-5346-402c-a7cb-a084d624b62e/44d83d28-9709-4e54-9b7d-9b6bcfb630be/44d83d29-9709-4e54-9b7d-9b6bcfb630be NEW row; perk_buff_override:010b08e0-5346-402c-a7cb-a084d624b62e/44d83d29-9709-4e54-9b7d-9b6bcfb630be/44d83d30-9709-4e54-9b7d-9b6bcfb630be NEW row; perk_buff_override:010b08e8-5346-402c-a7cb-a084d624b62e/44d83d37-9709-4e54-9b7d-9b6bcfb630be/44d83d38-9709-4e54-9b7d-9b6bcfb630be NEW row; perk_buff_override:010b08e9-5346-402c-a7cb-a084d624b62e/44d83d38-9709-4e54-9b7d-9b6bcfb630be/44d83d39-9709-4e54-9b7d-9b6bcfb630be NEW row; perk_buff_override:010b08c8-5346-402c-a7cb-a084d624b62e/44d83d12-9709-4e54-9b7d-9b6bcfb630be/44d83d13-9709-4e54-9b7d-9b6bcfb630be NEW row; perk_
- **Text:** 78 strings changed, 134 new
- **Problems:** Perkaholic/Data/Perkaholic.pak!Libs/Tables/rpg/perk_buff_override.xml: no suffix: replaces the whole vanilla table / Perkaholic/Data/Perkaholic.pak!Libs/Tables/rpg/perk2perk_exclusivity.xml: no suffix: replaces the whole vanilla table / Perkaholic/Data/Perkaholic.pak!Libs/Tables/rpg/perk_buff.xml: no suffix: replaces the whole vanilla table / Perkaholic/Data/Perkaholic.pak!Libs/Tables/rpg/buff.xml: no suffix: replaces the whole vanilla table / Perkaholic/Data/Perkaholic.pak!Libs/Tables/rpg/perk.xml: no suffix: replaces the whole vanilla table
- **Risk:** HIGH: HIGH: path traversal inside pak: Perkaholic/Data/Perkaholic.pak!../../../Data/Libs/Tables/rpg/perk2perk_exclusivity.tbl / HIGH: path traversal inside pak: Perkaholic/Data/Perkaholic.pak!../../../Data/Libs/Tables/rpg/buff.tbl / HIGH: path traversal inside pak: Perkaholic/Data/Perkaholic.pak!../../../Data/Libs/Tables/rpg/perk.tbl / HIGH: path traversal inside pak: Perkaholic/Data/Perkaholic.pak!../../../Data/Libs/Tables/rpg/perk_buff.tbl / HIGH: path traversal inside pak: Perkaholic/Data/Perkaholi (quarantined)

## 1384 Modified Combat Overhaul - Directional Combat and smarter AI (P2, Combat / AI)

- **What the author says (Nexus summary):** Directional master strikes and perfect blocks for player and AI; built on the Better Combat and Immersion Compilation Lite by replacing its .pak Master Strikes now require precise direction matching, Perfect Blocks require side matching, for both the player and the AI. This means you won't ever get 
- **File:** `zzz_BCAIC_BetterCombatLite.pak-1384-2-1654111935.zip` (archive, 0.02 MB, `c_combat-ai`), full (scratch, deleted after reading)
- **Grade:** B large | **perceptibility:** high | **layers:** D1 data tables (PTF)
- **How it installs:** loose .pak (legacy: copy into Data); manifest id `-`, supports `-`, loads on 1.9.8: no manifest (legacy install)
- **Where it changes things:** tables (PTF): 4; pak (container): 1; lua identical to vanilla: 0
- **Tables:** buff, combat_action_perfect_block, perk_rpg_param_override, rpg_param (160 new rows, 21 changed, 5 identical to vanilla, 976 vanilla rows dropped by a whole-table replace); median relative change 0.455
- **Largest changes:** rpg_param:CombatAutoDodgeWeight rpg_param_value 1.1->4; rpg_param:SkillToDmgConstA rpg_param_value 250->700; combat_action_perfect_block:14/1/1/CombatBlockPerfect/4/1/0/3/-1/0/4/7/4/-1/1/-1/-1/-1/-1/-1/4/-1/1 NEW row; combat_action_perfect_block:14/1/0/CombatBlockPerfect/2/1/0/3/-1/0/2/7/4/-1/1/-1/-1/-1/-1/-1/4/-1/0 NEW row; combat_action_perfect_block:14/1/0/CombatBlockPerfect/3/1/0/4/-1/0/3/7/4/-1/1/-1/-1/-1/-1/-1/4/-1/0 NEW row; combat_action_perfect_block:14/1/2/CombatBlockPerfect/3/1/0/4/-1/0/1/7/4/-1/1/-1/-1/-1/-1/-1/4/-1/1 NEW row; combat_action_perfect_block:14/1/1/CombatBlockPerfect/0/1/0/3/-1/0/0/7/4/-1/1/-1/-1/-1/-1/-1/4/-1/2 NEW row; combat_action_perfect_block:14/1/1/CombatBlock
- **Risk:** none

## 1558 Karnages_KCD_Essential_Fixes 2.0 (P2, Fix bundle)

- **What the author says (Nexus summary):** Total overhaul of the games RPG_Param File
- **File:** `Karnages_KCD_Essential_Fixes 2.0-1558-1-0-0-1700590734.7z` (archive, 0.0 MB, `c_fix-bundle`), full (scratch, deleted after reading)
- **Grade:** B large | **perceptibility:** high | **layers:** D1 data tables (PTF)
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `(none)`, loads on 1.9.8: yes (no version restriction)
- **Where it changes things:** tables (PTF): 3; manifest: 1; docs: 1; pak (container): 1; lua identical to vanilla: 0
- **Tables:** document_required_skill, perk_rpg_param_override, rpg_param (26 new rows, 129 changed, 2 identical to vanilla, 117 vanilla rows dropped by a whole-table replace); median relative change 1.0
- **Largest changes:** perk_rpg_param_override:01c3b32a-5751-4c98-b6ab-258d02370382/RepairKitCapacity rpg_param_value 450->8000; rpg_param:HorseRidingXPPerDistance rpg_param_value 12.5->150; rpg_param:RepairKitCapacity rpg_param_value 200->8000; rpg_param:SkillXPBlock rpg_param_value 2->30; rpg_param:StatXPVitalityPerVault rpg_param_value 0.7->8; rpg_param:ShoeHealthDecrease rpg_param_value 0.001->0.01; rpg_param:StatXPVitalityPerJump rpg_param_value 0.5->4; rpg_param:StatXPSpeechPerSequence rpg_param_value 1->7.5
- **Same rows as KRS:** krs_items:rpg_param:ReadingXpPerHour; krs_qol:rpg_param:HerbGatherSkillToRadius
- **Risk:** none

## 2345 Food and Drinks rebalance (P2, Alchemy / food / survival)

- **What the author says (Nexus summary):** A small mod to rebalance the nutrition, health and refresh benefits of all food and/or drinks in the game.
- **File:** `Food And Drinks Rebalance 2345 1 2026-08-30T23-35Z RVnPpl7KV.rar` (archive, 0.01 MB, `c_alchemy-food-survival`), full (scratch, deleted after reading)
- **Grade:** B large | **perceptibility:** high | **layers:** D1 data tables (PTF)
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `(none)`, loads on 1.9.8: yes (no version restriction)
- **Where it changes things:** manifest: 1; pak (container): 1; other: 1; tables (PTF): 1; lua identical to vanilla: 0
- **Tables:** food (0 new rows, 155 changed, 47 identical to vanilla); median relative change 0.5
- **Largest changes:** food:7beb4bdc-6478-455c-8746-afb92c604be8 refresh_benefit 1->-3; food:1d8ffd19-af12-4bd7-8afd-43b9b0348ade nutrition_benefit 4->18; food:154a8471-b753-4f84-ac5f-d989c8532d02 refresh_benefit -0.5->-2; food:b3e363cf-8dde-4733-89a9-c468d5580d2e refresh_benefit 0.5->-1; food:3d3f5935-c2e3-4e52-8a16-a6a04ee4a79f refresh_benefit 8->-10; food:45be379b-df05-4e13-9aa1-aaae649e8366 refresh_benefit 0.5->-0.5; food:6a324aa9-a566-406c-a3f8-6c416a00b399 refresh_benefit -0.5->-1.5; food:1c2da556-488b-4a86-b22a-c42acb299938 nutrition_benefit 3->8
- **Same rows as KRS:** krs_items:food:73ff1fde-ec8b-41e9-95e3-b5938c715bf1
- **Problems:** Jesoo333's Food and Drinks Rebalance/Data/Jesoo333's Food and Drinks Rebalance.pak!Libs/Tables/item/food.xml: no suffix: replaces the whole vanilla table
- **Risk:** none

## 1639 Alternate Food Spoil (2X) (P1, Alchemy / food / survival)

- **What the author says (Nexus summary):** Doubles the time it takes for food to spoil.
- **File:** `AlternateFoodSpoil2X-1639-1-0-1715595738.zip` (archive, 0.01 MB, `c_alchemy-food-survival`), full (scratch, deleted after reading)
- **Grade:** B large | **perceptibility:** high | **layers:** D1 data tables (PTF)
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `(none)`, loads on 1.9.8: yes (no version restriction)
- **Where it changes things:** manifest: 1; pak (container): 1; other: 1; tables (PTF): 1; lua identical to vanilla: 0
- **Tables:** food (0 new rows, 111 changed, 91 identical to vanilla); median relative change 1.0
- **Largest changes:** food:18ff9093-2cc4-4ab3-9f34-7cb0dd7cd30a decay_time_hours 24->2400; food:025f546b-7465-4070-a57d-e84852adc184 decay_time_hours 120->240; food:0368a199-117e-4079-b182-b042360c7d61 decay_time_hours 120->240; food:0686c001-d42b-467c-b3de-f87beb915c68 decay_time_hours 120->240; food:06be2a3d-4e05-4a78-85cd-33879cd669c9 decay_time_hours 24->48; food:0712d873-29bd-4fdd-8966-79aefb82c829 decay_time_hours 120->240; food:0a78fe34-737c-4346-9762-6b3036fbc9c6 decay_time_hours 24->48; food:0b4e244a-e3de-4502-afd0-fb7fe309629a decay_time_hours 48->96
- **Risk:** none

## 2045 Polearms Unleashed Rebalanced Lite Edition PTF (P2, Weapons / armor / items)

- **What the author says (Nexus summary):** A streamlined and rebalanced version of the great Polearms Unleashed mod, focused on realism and core gameplay. The polearm skill is now visible and functional, and every polearm has fully reworked stats. Experience playable, storable, and
- **File:** `Polearms Unleashed Rebalanced Lite Edition-2045-1-1-1779784172.7z` (archive, 0.2 MB, `c_weapons-armor-items`), full (scratch, deleted after reading)
- **Grade:** B large | **perceptibility:** high | **layers:** D0 content/text; D1 data tables (PTF); D3 Lua scripts
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `1.9.4 1.9.5 1.9.6 1.9.7 1.9.8`, loads on 1.9.8: yes (explicit)
- **Where it changes things:** tables (PTF): 12; pak (container): 5; models/animations/materials: 5; scripts (Lua): 2; manifest: 1; other xml (data): 1; lua identical to vanilla: 0
- **Tables:** combat_action_attack, combat_action_guard_movement, combat_action_perfect_block, combat_action_pose_modifier, combat_action_sync_pb_hit, equippable_item, melee_weapon, pickable_item, shop_type2item, skill, weapon, weapon_class (64 new rows, 42 changed, 8 identical to vanilla, 5225 vanilla rows dropped by a whole-table replace); median relative change 0.25
- **Largest changes:** pickable_item:8ef902ea-0c32-44c9-b101-71f35b9cbe3d price 1570->13800; pickable_item:44940b6c-f1f9-4ad1-9419-b5705a88e5b0 price 810->6000; melee_weapon:033fc7b6-17b6-486d-95cb-a22afb131be2 smash_att_mod 0.05->0.28; pickable_item:033fc7b6-17b6-486d-95cb-a22afb131be2 price 1500->6000; pickable_item:7377215a-a0ca-44a2-b11a-113a024191ca price 577->2280; pickable_item:3ef71c79-57c2-4f28-8f31-a091d9b78798 price 5325->16320; melee_weapon:7377215a-a0ca-44a2-b11a-113a024191ca smash_att_mod 0.05->0.15; melee_weapon:405c1865-413d-43b8-8db9-c44a0eefd350 smash_att_mod 0.05->0.15
- **Lua:** 2 files, 20 lines; API used: entity.humanx1, entity.actorx1, System.AddCCommandx1, Script.ReloadScriptx1, System.ExecuteCommandx1
- **Risk:** none

## 1380 Black Items Fix (P2, Weapons / armor / items)

- **What the author says (Nexus summary):** fixes items that should be black but are e.g. burgundy,grey etc.renaming items into proper colors + adding standalone versions of their black variant
- **File:** `BlackItems - PTF-1380-1-1-1780999063.rar` (archive, 0.32 MB, `c_weapons-armor-items`), full (scratch, deleted after reading)
- **Grade:** B large | **perceptibility:** high | **layers:** D0 content/text; D1 data tables (PTF)
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `1.9.4 1.9.5 1.9.6 1.9.7 1.9.8 1.9.9`, loads on 1.9.8: yes (explicit)
- **Where it changes things:** tables (PTF): 8; localization: 6; textures: 2; manifest: 1; pak (container): 1; models/animations/materials: 1; lua identical to vanilla: 0
- **Tables:** armor, clothing, clothing_raycast, equippable_item, item, pickable_item, player_item, shop_type2item (54 new rows, 5 changed, 0 identical to vanilla, 9851 vanilla rows dropped by a whole-table replace); median relative change 0.0
- **Largest changes:** armor:d640f7ba-a47a-46b9-b70d-e4abdfff2119 NEW row; armor:d640f7ba-a47a-46b9-b70d-e4abdfff2125 NEW row; armor:d640f7ba-a47a-46b9-b70d-e4abdfff2126 NEW row; armor:d640f7ba-a47a-46b9-b70d-e4abdfff2127 NEW row; armor:d640f7ba-a47a-46b9-b70d-e4abdfff2128 NEW row; armor:d640f7ba-a47a-46b9-b70d-e4abdfff2129 NEW row; equippable_item:d640f7ba-a47a-46b9-b70d-e4abdfff2119 NEW row; equippable_item:d640f7ba-a47a-46b9-b70d-e4abdfff2125 NEW row
- **Text:** 27 strings changed, 33 new
- **Risk:** none

## 2035 Ordinance an Archery Overhaul (P2, Archery / arrows)

- **What the author says (Nexus summary):** Complete++ overhaul of the entire Archery system, for both Henry and NPC's.
- **File:** `Ordinance Archery Overhaul DDDB-2035-6-1774914958.7z` (archive, 0.01 MB, `c_archery-arrows`), full (scratch, deleted after reading)
- **Grade:** B large | **perceptibility:** high | **layers:** D1 data tables (PTF)
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `zzdddbordinance`, supports `*`, loads on 1.9.8: NO (disabled: lists *)
- **Where it changes things:** tables (PTF): 8; docs: 2; pak (container): 2; manifest: 1; other xml (data): 1; lua identical to vanilla: 0
- **Tables:** ammo, equippable_item, item, missile_weapon, pickable_item, player_item, weapon, weapon_class (10 new rows, 48 changed, 27 identical to vanilla, 7704 vanilla rows dropped by a whole-table replace); median relative change 0.317
- **Largest changes:** pickable_item:7db6b854-e307-4a47-ba39-943190b2469e price 1->38; pickable_item:c49aa63a-07a6-4417-9f9b-97f2712a4cd0 weight 0.1->0.7; weapon:deb5276d-4926-4545-bdda-f457cac8bc01 agi_req 1->4; pickable_item:802507e9-d620-47b5-ae66-08fcc314e26a price 10->39; weapon_class:/4/f8558fe2-f4cd-4899-932b-82e0e15fa964/3/3/-1/-1/18/9/2 max_attack_distance 45->150; pickable_item:4fd563e5-a44a-4a6e-958d-95bcb196814a price 30->63; ammo:fc9ecc63-edc6-4bc9-8ba0-0a7620d5a4df NEW row; ammo:6f5b8900-c0f9-44a5-b1b8-ecef1a5a7b1c NEW row
- **Risk:** none

## 1062 SIM Camping Mini ML 1.5.1.1 (P2, Alchemy / food / survival)

- **What the author says (Nexus summary):** SIM Camping Mini Multilingual - Ru+En+Fr+De, corrections and ideas are accepted.
- **File:** `SIM_Camping.zip-1062-1-5-1-1-1598039154.zip` (archive, 0.04 MB, `c_alchemy-food-survival`), full (scratch, deleted after reading)
- **Grade:** B large | **perceptibility:** high | **layers:** D0 content/text; D1 data tables (PTF); D3 Lua scripts
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `(none)`, loads on 1.9.8: yes (no version restriction)
- **Where it changes things:** tables (PTF): 11; localization: 8; ui: 7; scripts (Lua): 3; manifest: 1; pak (container): 1; other: 1; lua identical to vanilla: 0
- **Tables:** buff, food, item, ointment_item, perk, perk_buff, pickable_item, player_item, questible_item, shop_type2item, sleeping_spot_type (39 new rows, 12 changed, 5 identical to vanilla, 9435 vanilla rows dropped by a whole-table replace); median relative change 0.667
- **Largest changes:** food:007ec8d6-1ce1-4e90-8267-7c349812ddcd NEW row; item:ef8970f9-2cc6-47c6-81a9-1939fc48e265 NEW row; item:007ec8d6-1ce1-4e90-8267-7c349812ddcd NEW row; item:008ec8d6-1ce1-4e90-8267-7c349812ddcd NEW row; item:009ec8d6-1ce1-4e90-8267-7c349812ddcd NEW row; item:010ec8d6-1ce1-4e90-8267-7c349812ddcd NEW row; ointment_item:ef8970f9-2cc6-47c6-81a9-1939fc48e265 NEW row; ointment_item:008ec8d6-1ce1-4e90-8267-7c349812ddcd NEW row
- **Lua:** 3 files, 1532 lines; API used: player.inventoryx57, Game.SendInfoTextx22, System.SpawnEntityx13, Game.ShowItemsTransferx10, System.GetEntitiesInSpherex10, System.LogAlwaysx9
- **Text:** 0 strings changed, 140 new
- **Problems:** SIM_Camping/Data/SIMCampingMinML.pak!Libs/Tables/rpg/sleeping_spot_type.xml: no suffix: replaces the whole vanilla table
- **Risk:** none

## 2173 True Hardcore Maintenance (PTF) (P2, Repair / durability)

- **What the author says (Nexus summary):** Rebalances repair kits, makes you pay full repair costs at shops, and removes repair kits from enemy inventories and camps. More details below.
- **File:** `True Hardcore Maintenance-2173-2-0-1776308890.zip` (archive, 0.01 MB, `c_repair-durability`), full (scratch, deleted after reading)
- **Grade:** B large | **perceptibility:** high | **layers:** D0 content/text; D1 data tables (PTF)
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `truehardcoremaintenance`, supports `(none)`, loads on 1.9.8: yes (no version restriction)
- **Where it changes things:** other: 8; tables (PTF): 8; localization: 2; manifest: 1; pak (container): 1; lua identical to vanilla: 0
- **Tables:** armor, buff, inventory_preset2item, ointment_item, perk_rpg_param_override, pickable_item, rpg_param, skill2item_category (7 new rows, 41 changed, 0 identical to vanilla, 4337 vanilla rows dropped by a whole-table replace); median relative change 1.0
- **Largest changes:** pickable_item:85310d06-2845-46ee-be8f-295503b35035 weight 0.1->0.5; pickable_item:9f7a0c0a-6458-4622-9cc5-2f4dd4898b50 weight 0.1->0.5; rpg_param:RepairKitCapacity rpg_param_value 200->600; inventory_preset2item:167eb312-0e9d-4c2f-8ce3-56c32f5a84cb amount_random_add 1->0; inventory_preset2item:c707733a-c0a7-4f02-b684-9392b0b15b83 amount_random_add 1->0; inventory_preset2item:167eb312-0e9d-4c2f-8ce3-56c32f5a84cb amount_random_add 1->0; inventory_preset2item:c707733a-c0a7-4f02-b684-9392b0b15b83 amount_random_add 1->0; armor:406c92ad-4c17-25d7-84d7-28500800f59e max_status 0->50
- **Text:** 2 strings changed, 0 new
- **Same rows as KRS:** krs_qol:perk_rpg_param_override:01c3b32a-5751-4c98-b6ab-258d02370382/RepairPriceModif; krs_qol:rpg_param:RepairPriceModif; krs_qol:skill2item_category:armor.horse_bridle.*/8; krs_qol:skill2item_category:armor.horse_saddle.*/8
- **Risk:** none

## 2209 Poisonous Enemies - True Hardcore Compatibility Patch (PTF) (P2, Combat / AI)

- **What the author says (Nexus summary):** Offers a selection of two compatibility patches for 'Poisonous Enemies', designed to work seamlessly with the 'True Hardcore' mod series. More details below.
- **File:** `patch True Hardcore Poisonous Enemies-2209-1-0-1776249027.zip` (archive, 0.01 MB, `c_combat-ai`), full (scratch, deleted after reading)
- **Grade:** B large | **perceptibility:** high | **layers:** D0 content/text; D1 data tables (PTF); D3 Lua scripts
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `patchtruehardcorepoisonousenemies`, supports `(none)`, loads on 1.9.8: yes (no version restriction)
- **Where it changes things:** other: 6; tables (PTF): 6; pak (container): 2; localization: 2; manifest: 1; scripts (Lua): 1; lua identical to vanilla: 0
- **Tables:** armor, armor_type, buff, pickable_item, player_item, shop_type2item (36 new rows, 0 changed, 0 identical to vanilla, 6290 vanilla rows dropped by a whole-table replace); median relative change 0.0
- **Largest changes:** armor:a36ebe4e-14e0-4110-b903-5c225a831410 NEW row; armor:b58d737a-0b33-410d-bcf1-c16f1e5fb682 NEW row; armor_type:67/ NEW row; armor_type:68/ NEW row; pickable_item:a36ebe4e-14e0-4110-b903-5c225a831410 NEW row; pickable_item:b58d737a-0b33-410d-bcf1-c16f1e5fb682 NEW row; player_item:a36ebe4e-14e0-4110-b903-5c225a831410 NEW row; player_item:b58d737a-0b33-410d-bcf1-c16f1e5fb682 NEW row
- **Lua:** 1 files, 464 lines; API used: player.soulx12, Game.SendInfoTextx11, player.lastHealthx2, System.GetViewCameraDirx2, player.idx2, player.actorx1
- **Text:** 0 strings changed, 3 new
- **Risk:** none

## 1105 Service Prices (P2, Economy / merchants)

- **What the author says (Nexus summary):** Increases the prices for basic services(Bathhouse, Trainers, Beds, Horses)
- **File:** `Service Prices-1105-1-0-1600469221.zip` (archive, 0.01 MB, `c_economy-merchants`), full (scratch, deleted after reading)
- **Grade:** B large | **perceptibility:** high | **layers:** D1 data tables (PTF); D3 Lua scripts
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `(none)`, loads on 1.9.8: yes (no version restriction)
- **Where it changes things:** scripts (Lua): 3; manifest: 1; pak (container): 1; tables (PTF): 1; lua identical to vanilla: 0
- **Tables:** sequence (0 new rows, 6 changed, 0 identical to vanilla, 52409 vanilla rows dropped by a whole-table replace); median relative change 0.0
- **Largest changes:** sequence:55336/ script Utils.SetLocalVar('s->Utils.SetLocalVar('s; sequence:55338/ script Utils.SetLocalVar('s->Utils.SetLocalVar('s; sequence:59202/ script Utils.SetLocalVar('s->Utils.SetLocalVar('s; sequence:55367/ script Utils.SetLocalVar('s->Utils.SetLocalVar('s; sequence:59155/ script Utils.SetLocalVar('s->Utils.SetLocalVar('s; sequence:55332/ script Utils.SetLocalVar('s->Utils.SetLocalVar('s
- **Lua:** 3 files, 1022 lines; API used: System.GetEntityByNamex6, player.soulx6, player.inventoryx4, player.thisx3, player.playerx2, XGenAIModule.SendMessageToEntityx2
- **Risk:** none

## 2343 Ultimate Horse Caparison Fix (P2, Horses)

- **What the author says (Nexus summary):** Short Description Fixes horse mane clipping through caparisons while preserving the tail. Full-cover caparisons hide the mane, while open-neck caparisons keep it visible.
- **File:** `Ultimate Horse Caparison Fix V1.0 2343 1.0 2026-08-24T20-12Z yvis1527X.zip` (archive, 0.6 MB, `c_horses`), full (scratch, deleted after reading)
- **Grade:** B large | **perceptibility:** high | **layers:** D0 content/text; D1 data tables (PTF); D3 Lua scripts
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `1.9.*`, loads on 1.9.8: yes (wildcard)
- **Where it changes things:** models/animations/materials: 3; docs: 2; tables (PTF): 2; manifest: 1; pak (container): 1; other xml (data): 1; ui: 1; scripts (Lua): 1; lua identical to vanilla: 0
- **Tables:** character_hair, soul (6 new rows, 0 changed, 0 identical to vanilla, 5060 vanilla rows dropped by a whole-table replace); median relative change 0.0
- **Largest changes:** character_hair:/d1317f64-c1c7-4c2d-b013-8f67c0201313/0/1/0 NEW row; character_hair:/d1317f64-c1c7-4c2d-b013-8f67c0201314/0/1/0 NEW row; soul:00000000-0000-0000-0000-000000035000/494dad1a-adec-4fc8-983e-19d81e60eb9c//4f14fe8f-5380-84b2-aeb3-6e51163f2a84/d1317f64-c1c7-4c2d-b013-8f67c0201313//483f3ddf-0894-164d-cb07-2a4135777497///488/9/3/7/40f7b115-7b9e-f1bb-d9b9-2d4a7bacd4bc/0 NEW row; soul:00000000-0000-0000-0000-000000035000/494dad1a-adec-4fc8-983e-19d81e60eb9c//4b58d97c-a4b0-f52f-7506-4b74504db390/d1317f64-c1c7-4c2d-b013-8f67c0201314//452d30e2-410f-7cb5-e0f5-4cbe282c759f///699//3/7/438809fe-1531-2ad9-0f5b-30cadaa83ca7/31 NEW row; soul:00000000-0000-0000-0000-000000035000/494dad1a-adec-4fc8
- **Lua:** 1 files, 1215 lines; API used: Script.SetTimerForFunctionx10, player.playerx7, player.humanx3, System.LogAlwaysx2, System.Logx2, XGenAIModule.GetEntityByWUIDx2
- **Risk:** none

## 2318 Visual Combo Helper (P2, Combat / AI)

- **What the author says (Nexus summary):** Displays your learned melee combos on the HUD whenever a supported weapon is drawn.
- **File:** `Visual Combo Helper 1.0.0 2318 1.0.0 2026-07-31T14-42Z uBF0oq5om.zip` (archive, 0.22 MB, `c_combat-ai`), full (scratch, deleted after reading)
- **Grade:** B large | **perceptibility:** high | **layers:** D0 content/text; D3 Lua scripts
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `(none)`, loads on 1.9.8: yes (no version restriction)
- **Where it changes things:** ui: 3; docs: 2; manifest: 1; pak (container): 1; scripts (Lua): 1; lua identical to vanilla: 0
- **Lua:** 1 files, 2388 lines; API used: System.GetCurrTimex12, Script.SetTimerx12, System.AddCCommandx11, System.LogAlwaysx4, entity.soulx3, entity.actorx2
- **Risk:** none

## 2323 Alchemy Stash Link (P2, Alchemy / food / survival)

- **What the author says (Nexus summary):** Alchemy Workbench Stash Link automatically links all of Henry's Master Stashes (Inn rooms, Ratay bed, home chests, mobile camping stashes) as well as your Horse's inventory directly to any Alchemy Bench you interact with!
- **File:** `Zz Alchemy Stash Link 2323 1.0 2026-08-03T20-39Z eXqNkidke.7z` (archive, 0.01 MB, `c_alchemy-food-survival`), full (scratch, deleted after reading)
- **Grade:** B large | **perceptibility:** high | **layers:** D3 Lua scripts
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `(none)`, loads on 1.9.8: yes (no version restriction)
- **Where it changes things:** scripts (Lua): 3; manifest: 1; pak (container): 1; lua identical to vanilla: 0
- **Lua:** 3 files, 1052 lines; API used: Script.SetTimerx16, Game.ShowTutorialx12, player.inventoryx8, System.AddCCommandx8, System.LogAlwaysx4, System.ExecuteCommandx4
- **Risk:** none

## 1334 Fast Learning Henry (P2, Progression / XP / perks)

- **What the author says (Nexus summary):** XP tables about 5x faster; version 1 raises every skill cap to 25; was not compatible with other mods that modify RPG_PARAMS I decided to make a quick mod for my save game that changes the xp tables to be around a 5x faster gain and increased the level cap for all skills to 25. Randomly thought of a
- **File:** `FastLearningHenry1.0-1334-0-5-1644641439.7z` (archive, 0.01 MB, `c_progression-xp-perks`), full (scratch, deleted after reading)
- **Grade:** C effective (few rows, strong effect) | **perceptibility:** high | **layers:** D1 data tables (PTF)
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `(none)`, loads on 1.9.8: yes (no version restriction)
- **Where it changes things:** manifest: 2; pak (container): 2; other: 2; tables (PTF): 2; lua identical to vanilla: 0
- **Tables:** rpg_param (4 new rows, 92 changed, 272 identical to vanilla); median relative change 4.0
- **Largest changes:** rpg_param:PickpocketingFailXPMod rpg_param_value 0.3->2; rpg_param:PickpocketingFailXPMod rpg_param_value 0.3->2; rpg_param:StatXPVitalityPerVault rpg_param_value 0.7->4; rpg_param:StatXPVitalityPerVault rpg_param_value 0.7->4; rpg_param:AlchemyXPPerSuccessfullBrewing rpg_param_value 40->200; rpg_param:HoundmasterXPContextCommand rpg_param_value 2->10; rpg_param:HoundmasterXPFeed rpg_param_value 25->125; rpg_param:HoundmasterXPFetch rpg_param_value 5->25
- **Same rows as KRS:** krs_items:rpg_param:ReadingXpPerHour
- **Problems:** FastLerningHenry1.0/LevelCap25/Mods/FastLearningHenry/Data/FastLearningHenry.pak!Libs/Tables/rpg/rpg_param.xml: no suffix: replaces the whole vanilla table / FastLerningHenry1.0/LevelCapDefault/Mods/FastLearningHenry/Data/FastLearningHenry.pak!Libs/Tables/rpg/rpg_param.xml: no suffix: replaces the whole vanilla table
- **Risk:** none

## 1260 RPG Tweaks (P2, Progression / XP / perks)

- **What the author says (Nexus summary):** Clean tweak of the rpg_param XML: stay clean longer; slightly bigger herb radius; lower stamina costs; easier sharpening; carry weight +60%; less bow aim shake; tougher lockpicks; more lockpicking and alchemy XP. Overlaps krs_qol and any bow work Various tweaks to make the game more enjoyable
- **File:** `Rpg Tweaks 0.9.1-1260-0-9-1-1627282645.rar` (archive, 0.0 MB, `c_progression-xp-perks`), full (scratch, deleted after reading)
- **Grade:** C effective (few rows, strong effect) | **perceptibility:** high | **layers:** D1 data tables (PTF)
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `(none)`, loads on 1.9.8: yes (no version restriction)
- **Where it changes things:** other: 3; tables (PTF): 3; manifest: 1; pak (container): 1; lua identical to vanilla: 0
- **Tables:** perk_rpg_param_override, rpg_param (9 new rows, 86 changed, 55 identical to vanilla, 249 vanilla rows dropped by a whole-table replace); median relative change 0.5
- **Largest changes:** perk_rpg_param_override:01c3b32a-5751-4c98-b6ab-258d02370382/RepairKitCapacity rpg_param_value 450->5200; rpg_param:HerbGatherSkillToRadius rpg_param_value 0.25->3; perk_rpg_param_override:01c3b32a-5751-4c98-b6ab-258d02370382/FullClothDirtyingOnFullSpeed rpg_param_value 5000->30000; rpg_param:StatXPVitalityPerJump rpg_param_value 0.5->3; rpg_param:BaseInventoryCapacity rpg_param_value 66->320; perk_rpg_param_override:01c3b32a-5751-4c98-b6ab-258d02370382/MaxSpecialPerfectBlockSlotModifier rpg_param_value 0.55->2.25; rpg_param:StatXPSpeechPerSequence rpg_param_value 1->4; rpg_param:MaxSpecialPerfectBlockSlotModifier rpg_param_value 0.6->1.99
- **Same rows as KRS:** krs_items:rpg_param:ReadingXpPerHour; krs_qol:rpg_param:HerbGatherSkillToRadius
- **Problems:** Rpg Tweaks 0.9.1/Data/Rpg_Tweaks.pak!Libs/Tables/rpg/perk_rpg_param_override.xml: no suffix: replaces the whole vanilla table / Rpg Tweaks 0.9.1/Data/Rpg_Tweaks.pak!Libs/Tables/rpg/rpg_param.xml: no suffix: replaces the whole vanilla table / Rpg Tweaks 0.9.1/Data/Libs/Tables/rpg/rpg_param.xml: no suffix: replaces the whole vanilla table
- **Risk:** none

## 1864 Cheap Savior Schnapps - PTF (P2, Economy / merchants)

- **What the author says (Nexus summary):** Savior schnapps cheap and sold by every merchant; PTF Save without going broke. With this mod, you can buy savior schnapps really cheap, find them sold everywhere and with abundance - PTF compatible
- **File:** `Cheap Savior Schnapps (No Alcohol Version)-1864-1-1-1739629893.zip` (archive, 0.0 MB, `c_economy-merchants`), full (scratch, deleted after reading)
- **Grade:** C effective (few rows, strong effect) | **perceptibility:** high | **layers:** D1 data tables (PTF)
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `cheapsaviorschnapps`, supports `(none)`, loads on 1.9.8: yes (no version restriction)
- **Where it changes things:** tables (PTF): 3; manifest: 1; pak (container): 1; lua identical to vanilla: 0
- **Tables:** food, pickable_item, shop_type2item (0 new rows, 89 changed, 0 identical to vanilla, 3128 vanilla rows dropped by a whole-table replace); median relative change 10.0
- **Largest changes:** shop_type2item:928463d9-e21a-4f7c-b5d3-8378ed375cd1 amount 2->100; shop_type2item:928463d9-e21a-4f7c-b5d3-8378ed375cd1 amount 4->100; shop_type2item:928463d9-e21a-4f7c-b5d3-8378ed375cd1 amount 5->100; shop_type2item:928463d9-e21a-4f7c-b5d3-8378ed375cd1 amount 2->100; shop_type2item:928463d9-e21a-4f7c-b5d3-8378ed375cd1 amount 3->100; shop_type2item:928463d9-e21a-4f7c-b5d3-8378ed375cd1 amount 3->100; shop_type2item:928463d9-e21a-4f7c-b5d3-8378ed375cd1 amount 2->100; shop_type2item:928463d9-e21a-4f7c-b5d3-8378ed375cd1 amount 3->100
- **Risk:** none

## 2165 Merchants Richer (P2, Economy / merchants)

- **What the author says (Nexus summary):** Merchants have 3x the money.A standalone PTF mod for the most recent game version.Sets in shop_type2item.xml: amount=3x for item_id="5ef63059-322e-4e1b-abe8-926e100c770e" (Groschen)
- **File:** `MerchantsRicher_3x-2165-1-0-2-1774198117.zip` (archive, 0.01 MB, `c_economy-merchants`), full (scratch, deleted after reading)
- **Grade:** C effective (few rows, strong effect) | **perceptibility:** high | **layers:** D1 data tables (PTF)
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `1.9.*`, loads on 1.9.8: yes (wildcard)
- **Where it changes things:** manifest: 1; pak (container): 1; tables (PTF): 1; lua identical to vanilla: 0
- **Tables:** shop_type2item (0 new rows, 79 changed, 0 identical to vanilla, 718 vanilla rows dropped by a whole-table replace); median relative change 2.0
- **Largest changes:** shop_type2item:5ef63059-322e-4e1b-abe8-926e100c770e amount 2800->8400; shop_type2item:5ef63059-322e-4e1b-abe8-926e100c770e amount 200->600; shop_type2item:5ef63059-322e-4e1b-abe8-926e100c770e amount 100->300; shop_type2item:5ef63059-322e-4e1b-abe8-926e100c770e amount 20000->60000; shop_type2item:5ef63059-322e-4e1b-abe8-926e100c770e amount 2000->6000; shop_type2item:5ef63059-322e-4e1b-abe8-926e100c770e amount 4000->12000; shop_type2item:5ef63059-322e-4e1b-abe8-926e100c770e amount 200->600; shop_type2item:5ef63059-322e-4e1b-abe8-926e100c770e amount 1500->4500
- **Risk:** none

## 1853 Richer Merchants (PTF) (P2, Economy / merchants)

- **What the author says (Nexus summary):** Every Merchant in the game have 10.000 Groschens
- **File:** `RicherMerchantsPRF-1853-1-0-1739403404.rar` (archive, 0.0 MB, `c_economy-merchants`), full (scratch, deleted after reading)
- **Grade:** C effective (few rows, strong effect) | **perceptibility:** high | **layers:** D1 data tables (PTF)
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `(none)`, loads on 1.9.8: yes (no version restriction)
- **Where it changes things:** manifest: 1; pak (container): 1; tables (PTF): 1; lua identical to vanilla: 0
- **Tables:** shop_type2item (0 new rows, 78 changed, 0 identical to vanilla, 718 vanilla rows dropped by a whole-table replace); median relative change 10.0
- **Largest changes:** shop_type2item:5ef63059-322e-4e1b-abe8-926e100c770e amount 2800->100000; shop_type2item:5ef63059-322e-4e1b-abe8-926e100c770e amount 200->100000; shop_type2item:5ef63059-322e-4e1b-abe8-926e100c770e amount 100->100000; shop_type2item:5ef63059-322e-4e1b-abe8-926e100c770e amount 2000->100000; shop_type2item:5ef63059-322e-4e1b-abe8-926e100c770e amount 4000->100000; shop_type2item:5ef63059-322e-4e1b-abe8-926e100c770e amount 200->100000; shop_type2item:5ef63059-322e-4e1b-abe8-926e100c770e amount 1500->100000; shop_type2item:5ef63059-322e-4e1b-abe8-926e100c770e amount 1500->100000
- **Risk:** none

## 1559 Karnages_Weapons_Damage_Balance 2.0 (P2, Weapons / armor / items)

- **What the author says (Nexus summary):** Full overhaul of weapons damages, does not include polearms or bows
- **File:** `Karnages_Weapons_Damage_Balance 2.0-1559-1-0-0-1700591190.7z` (archive, 0.0 MB, `c_weapons-armor-items`), full (scratch, deleted after reading)
- **Grade:** C effective (few rows, strong effect) | **perceptibility:** high | **layers:** D1 data tables (PTF)
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `(none)`, loads on 1.9.8: yes (no version restriction)
- **Where it changes things:** manifest: 1; pak (container): 1; tables (PTF): 1; lua identical to vanilla: 0
- **Tables:** melee_weapon (0 new rows, 77 changed, 0 identical to vanilla, 90 vanilla rows dropped by a whole-table replace); median relative change 1.727
- **Largest changes:** melee_weapon:aca90050-0b70-4ca0-9d29-b94326203c75 smash_att_mod 0.05->0.7; melee_weapon:ec470e0c-5bbd-43bb-803e-0e7867253c25 smash_att_mod 0.05->0.6; melee_weapon:24a7c868-f23f-4799-8e64-331435a77404 stab_att_mod 0.05->0.8; melee_weapon:c2d79308-ce89-41e4-b07c-8c00f4496370 stab_att_mod 0.05->1.6; melee_weapon:8e2ccaa1-17c2-4cef-b378-e71dc83bddb7 stab_att_mod 0.05->0.6; melee_weapon:db0725ac-c0e0-41db-b7a6-2887c57df612 smash_att_mod 0.05->0.5; melee_weapon:965cc83a-1d34-416f-aabd-c4a461a6e583 smash_att_mod 0.05->0.5; melee_weapon:d41af9ba-400f-49ae-91fa-38c7da4b815b smash_att_mod 0.05->0.5
- **Risk:** none

## 1950 Skill Books Take Time (P2, Progression / XP / perks)

- **What the author says (Nexus summary):** Reading books take time.
- **File:** `Skill Books Take Time 2x-1950-1-0-1742313588.zip` (archive, 0.0 MB, `c_progression-xp-perks`), full (scratch, deleted after reading)
- **Grade:** C effective (few rows, strong effect) | **perceptibility:** high | **layers:** D1 data tables (PTF)
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `1.*`, loads on 1.9.8: yes (wildcard)
- **Where it changes things:** tables (PTF): 2; manifest: 1; pak (container): 1; lua identical to vanilla: 0
- **Tables:** document, rpg_param (0 new rows, 57 changed, 0 identical to vanilla, 317 vanilla rows dropped by a whole-table replace); median relative change 1.0
- **Largest changes:** document:0a9b5b2a-2614-4f11-a987-aab64133bea0 length_in_game_hours 6->12; document:0defd37d-cfec-446f-b307-e9ef65fea3f3 length_in_game_hours 6->12; document:15a92bc2-d1f3-438f-a104-c1fc7bd71996 length_in_game_hours 6->12; document:17fee956-5ec2-4c95-abb4-e9f3a0aca530 length_in_game_hours 4->8; document:196ffe33-bec0-410d-abb5-138f69ececd7 length_in_game_hours 8->16; document:1dc7d3ef-08b0-4d4f-aca1-78ddf60a5c10 length_in_game_hours 4->8; document:20856f2c-1f0c-42dd-805a-87eb7902ddeb length_in_game_hours 6->12; document:218418c0-f211-40b3-afa9-f1bff300d0b5 length_in_game_hours 6->12
- **Same rows as KRS:** krs_items:document:0a9b5b2a-2614-4f11-a987-aab64133bea0; krs_items:document:0defd37d-cfec-446f-b307-e9ef65fea3f3; krs_items:document:15a92bc2-d1f3-438f-a104-c1fc7bd71996; krs_items:document:17fee956-5ec2-4c95-abb4-e9f3a0aca530; krs_items:document:196ffe33-bec0-410d-abb5-138f69ececd7; krs_items:docum
- **Risk:** none

## 1572 Increased Experience Gains (P2, Progression / XP / perks)

- **What the author says (Nexus summary):** Changes rpg_param to raise XP gain 1.5x / 2x / 5x; optional herb picking and auto brewing Increases experience gain by 1.5, 2x or 5x
- **File:** `Increased Experience Minor - 1.5x-1572-0-1-1701102679.zip` (archive, 0.0 MB, `c_progression-xp-perks`), full (scratch, deleted after reading)
- **Grade:** C effective (few rows, strong effect) | **perceptibility:** high | **layers:** D1 data tables (PTF)
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `(none)`, loads on 1.9.8: yes (no version restriction)
- **Where it changes things:** manifest: 1; pak (container): 1; tables (PTF): 1; lua identical to vanilla: 0
- **Tables:** rpg_param (2 new rows, 37 changed, 0 identical to vanilla, 145 vanilla rows dropped by a whole-table replace); median relative change 0.5
- **Largest changes:** rpg_param:AlchemyXPPerAutocookBrewingRelative NEW row; rpg_param:HerbGatherXP NEW row; rpg_param:SecondaryStatXPRatio rpg_param_value 0.5->0.8; rpg_param:StatXPVitalityPerJump rpg_param_value 0.5->0.8; rpg_param:HorseRidingXPPerDistance rpg_param_value 12.5->18.8; rpg_param:AlchemyXPPerSuccessfullBrewing rpg_param_value 40->60; rpg_param:HoundmasterXPContextCommand rpg_param_value 2->3; rpg_param:HoundmasterXPFeed rpg_param_value 25->37.5
- **Same rows as KRS:** krs_items:rpg_param:ReadingXpPerHour
- **Risk:** none

## 1660 Double Brew Yield (P2, Alchemy / food / survival)

- **What the author says (Nexus summary):** Doubling the brewing yield in Alchemy
- **File:** `Double Brew Yield-1660-1-0-1717587176.zip` (archive, 0.0 MB, `c_alchemy-food-survival`), full (scratch, deleted after reading)
- **Grade:** C effective (few rows, strong effect) | **perceptibility:** high | **layers:** D1 data tables (PTF)
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `(none)`, loads on 1.9.8: yes (no version restriction)
- **Where it changes things:** manifest: 1; pak (container): 1; tables (PTF): 1; lua identical to vanilla: 0
- **Tables:** recipe (0 new rows, 35 changed, 0 identical to vanilla); median relative change 1.0
- **Largest changes:** recipe:310e921d-da62-48e4-88ef-de9f295e0045/f1309a89-045f-44ae-a4d9-c997b892a162/2 max_yield 3->6; recipe:e96d768e-04e5-4480-9197-1c256d642ddc/8b713d0c-9a04-4354-a53f-ffd384057fa6/3 max_yield 3->6; recipe:310e921d-da62-48e4-88ef-de9f295e0045/3157d51d-7461-4fdc-9601-93bd5ed42156/4 max_yield 3->6; recipe:d5efb270-948b-4a38-b391-38b2edd31c8d/42e54d97-6e63-4e50-a09d-325ef4dd2286/5 max_yield 3->6; recipe:34bd1d0b-1203-42a0-b9b4-d3585a4d9b48/34d9f446-e5a7-4af4-858a-e96473de814f/6 max_yield 3->6; recipe:d5efb270-948b-4a38-b391-38b2edd31c8d/2b24a290-ec3c-454c-901e-fea76aa76d74/7 max_yield 3->6; recipe:d5efb270-948b-4a38-b391-38b2edd31c8d/1322a0ca-1be1-449a-b1fa-cd7079a9ba90/8 max_yield 1->2; recipe:
- **Risk:** none

## 1668 Relaxed RPG Params (P2, Progression / XP / perks)

- **What the author says (Nexus summary):** Pack of rpg_param values: inventory x3 (horse x4); riding XP +25%; bow aim spread -33%; stamina regen delay -33%; sprint/jump cost -15%; less alchemy grinding; slower dirt. Overlaps krs_qol and bow constants just a pack of some more "relaxed/forgiving" RPG parameters
- **File:** `Relaxed RPG Params-1668-1-0-1-1718992231.7z` (archive, 0.0 MB, `c_progression-xp-perks`), full (scratch, deleted after reading)
- **Grade:** C effective (few rows, strong effect) | **perceptibility:** high | **layers:** D1 data tables (PTF)
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `(none)`, loads on 1.9.8: yes (no version restriction)
- **Where it changes things:** manifest: 1; pak (container): 1; tables (PTF): 1; lua identical to vanilla: 0
- **Tables:** rpg_param (7 new rows, 26 changed, 0 identical to vanilla, 156 vanilla rows dropped by a whole-table replace); median relative change 0.5
- **Largest changes:** rpg_param:RepairKitCapacity rpg_param_value 200->4500; rpg_param:DogMoraleBuffFeed rpg_param_value 0.08->0.75; rpg_param:DogMoraleBuffPlay rpg_param_value 0.05->0.25; rpg_param:DogMoraleBuffPraise rpg_param_value 0.05->0.25; rpg_param:HorseMountMaxRelativeEncumberance rpg_param_value 1.5->6; rpg_param:BaseInventoryCapacity rpg_param_value 66->198; rpg_param:DogMoraleDecreaseWithoutInteraction rpg_param_value 5.5e-05->0; rpg_param:RepairKitItemHealthDefaultLimit NEW row
- **Risk:** none

## 1070 Better Combat (P2, Combat / AI)

- **What the author says (Nexus summary):** The horrendous combat we've all grown to hate where all you had to do was press Q when prompted to Master Strike your way to victory is no more.MANUAL INSTALLATION:Extract the folder 'Zeeb - Better Combat' into "...\Steam\steamapps\common\
- **File:** `Better Combat-1070-1-2-1594609210.rar` (archive, 0.0 MB, `c_combat-ai`), full (scratch, deleted after reading)
- **Grade:** C effective (few rows, strong effect) | **perceptibility:** high | **layers:** D1 data tables (PTF); D2 engine config
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `1.9.6`, loads on 1.9.8: NO (disabled: lists 1.9.6)
- **Where it changes things:** docs: 2; tables (PTF): 2; config (.cfg): 1; manifest: 1; pak (container): 1; lua identical to vanilla: 0
- **Tables:** perk_rpg_param_override, rpg_param (19 new rows, 13 changed, 0 identical to vanilla, 194 vanilla rows dropped by a whole-table replace); median relative change 0.375
- **Largest changes:** rpg_param:CombatAutoAttackDelayIncreasePerAttackerHorse NEW row; rpg_param:CombatAutoAttackDelayIncreasePerAttackerMissile NEW row; rpg_param:CombatAutoClinchReactionDelayMaxMax NEW row; rpg_param:CombatAutoClinchReactionDelayMaxMin NEW row; rpg_param:CombatAutoClinchReactionDelayMinMax NEW row; rpg_param:CombatAutoClinchReactionDelayMinMin NEW row; rpg_param:CombatAutoMaxAimDuration NEW row; perk_rpg_param_override:01c3b32a-5751-4c98-b6ab-258d02370382/CombatAutoAttackDelayIncreasePerAttackerHorse NEW row
- **Config:** 4 keys, e.g. wh_cs_TimeWarpDodgeFadeSpeedForOpp=1, wh_cs_TimeWarpDodgeFadeSpeedForPlayer=1, wh_cs_TimeWarpPBFadeSpeedForOpp=1, wh_cs_TimeWarpPBFadeSpeedForPlayer=1
- **Risk:** none

## 1564 Karnages_Rebalanced_Bows 2.0 (P2, Archery / arrows)

- **What the author says (Nexus summary):** a total overhaul of bow power and behavior
- **File:** `Karnages_Rebalanced_Bows 2.0-1564-1-0-0-1700618747.7z` (archive, 0.0 MB, `c_archery-arrows`), full (scratch, deleted after reading)
- **Grade:** C effective (few rows, strong effect) | **perceptibility:** high | **layers:** D1 data tables (PTF)
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `(none)`, loads on 1.9.8: yes (no version restriction)
- **Where it changes things:** tables (PTF): 2; manifest: 1; pak (container): 1; lua identical to vanilla: 0
- **Tables:** missile_weapon, rpg_param (9 new rows, 21 changed, 2 identical to vanilla, 182 vanilla rows dropped by a whole-table replace); median relative change 0.234
- **Largest changes:** rpg_param:BowPowerToChargeDuration NEW row; rpg_param:BowChargeDurationMin NEW row; rpg_param:BowChargeDurationMax NEW row; rpg_param:AimSpreadSkillDecrease NEW row; rpg_param:AimZoomBase NEW row; rpg_param:AimZoomBaseSkill NEW row; rpg_param:AimZoomMax NEW row; rpg_param:AimSkillToZoom NEW row
- **Risk:** none

## 1926 Potion no Satiety and ADD Heal plus Energy (P2, Alchemy / food / survival)

- **What the author says (Nexus summary):** Changes almost all potions in the game.
- **File:** `PotionNoSatietyAndHealEnergy-1926-1-0-1741597951.7z` (archive, 0.0 MB, `c_alchemy-food-survival`), full (scratch, deleted after reading)
- **Grade:** C effective (few rows, strong effect) | **perceptibility:** high | **layers:** D1 data tables (PTF)
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `1.9.6`, loads on 1.9.8: NO (disabled: lists 1.9.6)
- **Where it changes things:** manifest: 1; pak (container): 1; tables (PTF): 1; lua identical to vanilla: 0
- **Tables:** food (0 new rows, 22 changed, 0 identical to vanilla, 180 vanilla rows dropped by a whole-table replace); median relative change 1.0
- **Largest changes:** food:73ff1fde-ec8b-41e9-95e3-b5938c715bf1 refresh_benefit 4->100; food:2509115d-59c9-44f8-9802-f600eba63fa9 refresh_benefit 4->100; food:8b713d0c-9a04-4354-a53f-ffd384057fa6 refresh_benefit 4->100; food:850d28d9-9d0a-4b2e-9feb-e6c48c5f1aad refresh_benefit 4->100; food:f1309a89-045f-44ae-a4d9-c997b892a162 health_benefit 4->100; food:34d9f446-e5a7-4af4-858a-e96473de814f refresh_benefit 4->100; food:3157d51d-7461-4fdc-9601-93bd5ed42156 refresh_benefit 4->100; food:92c829ca-41f6-40a7-b8d9-aac5159c7a89 refresh_benefit 6->100
- **Same rows as KRS:** krs_items:food:73ff1fde-ec8b-41e9-95e3-b5938c715bf1
- **Risk:** none

## 1678 Better Archery (P2, Archery / arrows)

- **What the author says (Nexus summary):** Faster arrows, shorter draw, lower stamina drain, less aim spread, rebalanced damage; three variants (a no-OP variant added 2025-01-07) PTF.  Improved yet balanced Speed and DMG of arrows and draw
- **File:** `Better_Archery-1678-1-0-1720015220.7z` (archive, 0.0 MB, `c_archery-arrows`), full (scratch, deleted after reading)
- **Grade:** C effective (few rows, strong effect) | **perceptibility:** high | **layers:** D1 data tables (PTF)
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `1.9.*`, loads on 1.9.8: yes (wildcard)
- **Where it changes things:** tables (PTF): 2; manifest: 1; pak (container): 1; lua identical to vanilla: 0
- **Tables:** ammo, rpg_param (5 new rows, 16 changed, 0 identical to vanilla, 180 vanilla rows dropped by a whole-table replace); median relative change 0.482
- **Largest changes:** rpg_param:BowChargeDurationMin NEW row; rpg_param:BowChargeDurationMax NEW row; rpg_param:BowPowerToChargeDuration NEW row; rpg_param:AimPainlessDelay NEW row; rpg_param:AimSpreadSkillDecrease NEW row; ammo:d5e6764d-18ba-44cb-8dd0-6640a17785a8 power_mod 1.1->2.1; ammo:a5b31bbc-1e11-4831-835b-c06d5b13a7da power_mod 0.9->1.7; ammo:710e3706-8974-404b-b23a-6f51670ef1ed power_mod 1.1->2
- **Risk:** none

## 1419 Immersive Archery (P2, Archery / arrows)

- **What the author says (Nexus summary):** Draw speed to about 16 arrows per minute; arrow speed x1.7; lower stamina drain; arrow damage x1.2. The suite alters this mod (permission granted) The draw speed and arrow speed in the game feel way too low so in order to make archery more realistic -ish the draw is faster along with the flight spee
- **File:** `Immersive Archery-1419-1-2-1665671489.zip` (archive, 0.0 MB, `c_archery-arrows`), full (scratch, deleted after reading)
- **Grade:** C effective (few rows, strong effect) | **perceptibility:** high | **layers:** D1 data tables (PTF)
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `(none)`, loads on 1.9.8: yes (no version restriction)
- **Where it changes things:** tables (PTF): 2; manifest: 1; pak (container): 1; lua identical to vanilla: 0
- **Tables:** ammo, rpg_param (5 new rows, 15 changed, 0 identical to vanilla, 181 vanilla rows dropped by a whole-table replace); median relative change 0.541
- **Largest changes:** rpg_param:BowChargeDurationMin NEW row; rpg_param:BowChargeDurationMax NEW row; rpg_param:BowPowerToChargeDuration NEW row; rpg_param:AimPainlessDelay NEW row; rpg_param:AimSpreadSkillDecrease NEW row; ammo:dfea5d01-b25c-414a-9ab4-6911a5f82118 power_mod 0.85->1.45; ammo:13ba7468-11a2-483d-8cb9-25ce36a2d228 power_mod 1->1.7; ammo:19df1c5c-3dbf-45c0-ac01-336facf5f741 power_mod 1->1.7
- **Risk:** none

## 1545 Saddles Have Durability (P2, Weapons / armor / items)

- **What the author says (Nexus summary):** Saddles have actual durability so that they aren't completely destroyed in one hit to the horse.
- **File:** `Saddles Have Durability-1545-1-0-1694353149.7z` (archive, 0.0 MB, `c_weapons-armor-items`), full (scratch, deleted after reading)
- **Grade:** C effective (few rows, strong effect) | **perceptibility:** high | **layers:** D1 data tables (PTF)
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `1.*`, loads on 1.9.8: yes (wildcard)
- **Where it changes things:** manifest: 1; pak (container): 1; tables (PTF): 1; lua identical to vanilla: 0
- **Tables:** armor (0 new rows, 20 changed, 0 identical to vanilla, 776 vanilla rows dropped by a whole-table replace); median relative change 1.0
- **Largest changes:** armor:406c92ad-4c17-25d7-84d7-28500800f59e max_status 0->50; armor:40c16f73-5b83-c139-96eb-c39ff5e9e7a6 max_status 0->50; armor:41382adf-569c-4f33-90a0-36b6e874eca7 max_status 0->50; armor:41b3cfda-0a6c-c009-9482-4c78ea2f1980 max_status 0->50; armor:41f6e46c-bca6-16da-169a-f0c8f1a6e2ab max_status 0->50; armor:42a14b38-295a-a659-3e43-c1684a5dfa88 max_status 0->50; armor:42b152d3-d3f4-b390-088e-3127534281aa max_status 0->50; armor:43062de7-afe1-5743-5aec-d4dcff83c1b8 max_status 0->50
- **Risk:** none

## 1730 Drink Sound Effects (P2, Alchemy / food / survival)

- **What the author says (Nexus summary):** This mod will replace the "eating" sound effect certain drinks use with the potion "drinking" sound effect.
- **File:** `DrinkSoundEffects.pak` (loose file, 0.0 MB, `c_alchemy-food-survival`), read in place
- **Grade:** C effective (few rows, strong effect) | **perceptibility:** high | **layers:** D1 data tables (PTF)
- **How it installs:** loose .pak (legacy: copy into Data); manifest id `-`, supports `-`, loads on 1.9.8: no manifest (legacy install)
- **Where it changes things:** tables (PTF): 2; pak (container): 1; lua identical to vanilla: 0
- **Tables:** item, potion (9 new rows, 9 changed, 0 identical to vanilla, 2251 vanilla rows dropped by a whole-table replace); median relative change 0.0
- **Largest changes:** potion:0cb47176-06c5-42a9-8d70-969e917eb999 NEW row; potion:38df365c-a4bb-462b-80cc-eb92f16930fa NEW row; potion:390c0dc8-23fd-42a0-91f2-a4d42f96a387 NEW row; potion:51555071-7c55-4da1-9b61-ee3c14fde18b NEW row; potion:52afd6fa-9377-457c-83a2-b5b39321a4dc NEW row; potion:7c5126cd-b010-4484-8465-22a3d69fa0df NEW row; potion:ca5a0aa3-e373-48ec-96e4-1c3b9907bac3 NEW row; potion:c64b7286-07b8-4bdf-afd0-359171d35249 NEW row
- **Risk:** none

## 1883 Better Pickpocket - FIXED (P2, Crime / stealth / loot)

- **What the author says (Nexus summary):** This mod makes it easier to pickpocket drunk and sleeping NPCs by reducing the chance of waking them up, as it should be.
- **File:** `BetterPickpocket-1883-1-1-1773177388.zip` (archive, 0.0 MB, `c_crime-stealth-loot`), full (scratch, deleted after reading)
- **Grade:** C effective (few rows, strong effect) | **perceptibility:** high | **layers:** D1 data tables (PTF)
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `BetterPickpocket`, supports `1.9.*`, loads on 1.9.8: yes (wildcard)
- **Where it changes things:** manifest: 1; pak (container): 1; other: 1; tables (PTF): 1; lua identical to vanilla: 0
- **Tables:** rpg_param (15 new rows, 2 changed, 5 identical to vanilla, 175 vanilla rows dropped by a whole-table replace); median relative change 1.25
- **Largest changes:** rpg_param:PickpocketingXP rpg_param_value 15->45; rpg_param:PicklockFatalRelativeDist NEW row; rpg_param:PickpocketingAngleChancePenalty NEW row; rpg_param:PickpocketingComradePerkBonus NEW row; rpg_param:PickpocketingItemUncoverTimePerWeight NEW row; rpg_param:PickpocketingMaxSkillChargeSpeedRatio NEW row; rpg_param:PickpocketingMaxSkillChargeTime NEW row; rpg_param:PickpocketingMinChargeTime NEW row
- **Problems:** BetterPickpocket/Data/better_pickpocket.pak!Libs/Tables/rpg/rpg_param__better_pickpocket.xml: suffix 'better_pickpocket' != id 'BetterPickpocket' (the game ignores it)
- **Risk:** none

## 1914 Weightless Herbs (P2, Alchemy / food / survival)

- **What the author says (Nexus summary):** Makes alchemy herbs weightless
- **File:** `Weightless_Herbs-1914-1-1741286285.zip` (archive, 0.0 MB, `c_alchemy-food-survival`), full (scratch, deleted after reading)
- **Grade:** C effective (few rows, strong effect) | **perceptibility:** high | **layers:** D1 data tables (PTF)
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `(none)`, loads on 1.9.8: yes (no version restriction)
- **Where it changes things:** manifest: 1; pak (container): 1; tables (PTF): 1; lua identical to vanilla: 0
- **Tables:** pickable_item (0 new rows, 17 changed, 0 identical to vanilla, 2193 vanilla rows dropped by a whole-table replace); median relative change 1.0
- **Largest changes:** pickable_item:0290b689-c01c-480f-b121-bed71ad1f5e0 weight 0.1->0; pickable_item:05bef17b-ddeb-426d-aa53-52ff6d4f521e weight 0.1->0; pickable_item:27b8a61f-36e4-4101-9be5-1b814d43bd8f weight 0.1->0; pickable_item:2ddf6256-0662-44c4-99fe-f713b6d900ea weight 0.1->0; pickable_item:4d9e61aa-3f90-4e5d-b836-f9e158196438 weight 0.1->0; pickable_item:5e9b4fa1-aafa-4352-b5d6-58df2c263caa weight 0.1->0; pickable_item:7259b9bc-dfae-487e-a8bb-c1f500894e0c weight 0.1->0; pickable_item:7da04bba-0564-42da-bcf1-9a2fc5faf025 weight 0.1->0
- **Risk:** none

## 765 Poison Overhaul (P2, Alchemy / food / survival)

- **What the author says (Nexus summary):** Buffs or fixes some potions and adds a perk so poisons are useful (formerly Alchemical Warfare); users report it works on 1.9.6 and later Previously called "Alchemical Warfare". A simple mod that buff/fix some potions and adds a new perk, making poisons more useful, and in some cases, actually work.
- **File:** `Poison Overhaul v1.2-765-1-2-1657391917.zip` (archive, 0.01 MB, `c_alchemy-food-survival`), full (scratch, deleted after reading)
- **Grade:** C effective (few rows, strong effect) | **perceptibility:** high | **layers:** D0 content/text; D1 data tables (PTF)
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `1.9.4 1.9.5 1.9.6`, loads on 1.9.8: NO (disabled: lists 1.9.4, 1.9.5, 1.9.6)
- **Where it changes things:** tables (PTF): 4; localization: 2; manifest: 1; pak (container): 1; lua identical to vanilla: 0
- **Tables:** buff, food, perk, perk_buff (3 new rows, 12 changed, 1 identical to vanilla, 1317 vanilla rows dropped by a whole-table replace); median relative change 2.0
- **Largest changes:** buff:f405cbea-2a3f-4363-9e6a-23417e4e2a14 duration 25->300; food:5c17d1d9-70ec-49d9-9b05-ae23247c045f alcohol_content 20->150; buff:15387b1a-7f7e-4462-8ce6-ea652f0e182e duration 3600->21600; food:fd6cceee-06d0-4a0b-a0f6-c52d0afd5481 health_benefit -50->-300; food:42e54d97-6e63-4e50-a09d-325ef4dd2286 health_benefit -110->-480; buff:56f66d97-43c6-45d1-a463-05ec76fac01c duration 25->90; buff:f13d37c1-5524-4822-9515-48e1ccb0dde4 duration 3600->7400; buff:58138b68-0c86-4d5e-8823-417106d08d3c duration 55->-1
- **Text:** 8 strings changed, 2 new
- **Risk:** none

## 1376 Archery mod - Faster arrows (for real) (P2, Archery / arrows)

- **What the author says (Nexus summary):** Makes arrows leave the bow much faster (possibly making them more realistic since the default arrows seem too slow), enabling you to hit moving targets easier etc.
- **File:** `Archery mod - Faster arrows-1376-1-1-1775621786.zip` (archive, 0.0 MB, `c_archery-arrows`), full (scratch, deleted after reading)
- **Grade:** C effective (few rows, strong effect) | **perceptibility:** high | **layers:** D1 data tables (PTF)
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `1.9.4 1.9.5 1.9.6 1.9.7`, loads on 1.9.8: NO (disabled: lists 1.9.4, 1.9.5, 1.9.6, 1.9.7)
- **Where it changes things:** tables (PTF): 2; manifest: 1; pak (container): 1; other xml (data): 1; lua identical to vanilla: 0
- **Tables:** ammo (0 new rows, 14 changed, 23 identical to vanilla); median relative change 0.818
- **Largest changes:** ammo:13ba7468-11a2-483d-8cb9-25ce36a2d228 power_mod 1->2; ammo:19df1c5c-3dbf-45c0-ac01-336facf5f741 power_mod 1->2; ammo:278d26d1-e9a7-4354-84f9-37d20cb72b45 power_mod 1->2; ammo:4fd563e5-a44a-4a6e-958d-95bcb196814a power_mod 1->2; ammo:7db6b854-e307-4a47-ba39-943190b2469e power_mod 1->2; ammo:802507e9-d620-47b5-ae66-08fcc314e26a power_mod 1->2; ammo:a5b31bbc-1e11-4831-835b-c06d5b13a7da power_mod 0.9->1.8; ammo:ad6f0f01-aec4-44d1-982c-1210eb01b74a power_mod 1.1->2.2
- **Risk:** none

## 1565 Karnages_Arrow_Balance 2.0 (P2, Archery / arrows)

- **What the author says (Nexus summary):** Total Overhaul of Arrow Damage and Flight
- **File:** `Karnages_Arrow_Balance 2.0-1565-1-0-0-1700618949.7z` (archive, 0.0 MB, `c_archery-arrows`), full (scratch, deleted after reading)
- **Grade:** C effective (few rows, strong effect) | **perceptibility:** high | **layers:** D1 data tables (PTF)
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `(none)`, loads on 1.9.8: yes (no version restriction)
- **Where it changes things:** manifest: 1; pak (container): 1; tables (PTF): 1; other xml (data): 1; lua identical to vanilla: 0
- **Tables:** ammo (0 new rows, 12 changed, 0 identical to vanilla, 2 vanilla rows dropped by a whole-table replace); median relative change 1.0
- **Largest changes:** ammo:13ba7468-11a2-483d-8cb9-25ce36a2d228 smash_att 0->0.1; ammo:c49aa63a-07a6-4417-9f9b-97f2712a4cd0 smash_att 0->0.1; ammo:19df1c5c-3dbf-45c0-ac01-336facf5f741 slash_att 0->2; ammo:4fd563e5-a44a-4a6e-958d-95bcb196814a slash_att 0->2; ammo:710e3706-8974-404b-b23a-6f51670ef1ed slash_att 0->2; ammo:802507e9-d620-47b5-ae66-08fcc314e26a slash_att 0->2; ammo:a5b31bbc-1e11-4831-835b-c06d5b13a7da slash_att 0->2; ammo:ad6f0f01-aec4-44d1-982c-1210eb01b74a slash_att 0->2
- **Risk:** none

## 804 Loose (An Archery Mod) (P2, Archery / arrows)

- **What the author says (Nexus summary):** A rebalance of KCD’s archery gameplay.
- **File:** `Loose (An Archery Mod) V1.1-804-1-1-1565191248.7z` (archive, 0.0 MB, `c_archery-arrows`), full (scratch, deleted after reading)
- **Grade:** C effective (few rows, strong effect) | **perceptibility:** high | **layers:** D1 data tables (PTF)
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `(none)`, loads on 1.9.8: yes (no version restriction)
- **Where it changes things:** manifest: 1; pak (container): 1; other: 1; tables (PTF): 1; other xml (data): 1; lua identical to vanilla: 0
- **Tables:** rpg_param (9 new rows, 2 changed, 180 identical to vanilla); median relative change 0.225
- **Largest changes:** rpg_param:AimSpreadSkillDecrease NEW row; rpg_param:AimZoomBase NEW row; rpg_param:AimZoomBaseSkill NEW row; rpg_param:AimZoomMax NEW row; rpg_param:AimSkillToZoom NEW row; rpg_param:AimPainlessDelay NEW row; rpg_param:BowPowerToChargeDuration NEW row; rpg_param:BowChargeDurationMin NEW row
- **Problems:** Loose_An_Archery_Mod_v1.1/Data/Loose_An_Archery_Mod.pak!Libs/Tables/rpg/rpg_param.xml: no suffix: replaces the whole vanilla table
- **Risk:** none

## 1990 Veteran Hunting (P2, Alchemy / food / survival)

- **What the author says (Nexus summary):** Hunting overhaul: gives the player a perk with a custom buff that makes animals skittish; changes animal soul hearing parameters Started as experiment.. turned to Hunting overhaul, kind of..
- **File:** `Veteran Hunting 1.0-1990-1-0-1745597572.zip` (archive, 0.01 MB, `c_alchemy-food-survival`), full (scratch, deleted after reading)
- **Grade:** C effective (few rows, strong effect) | **perceptibility:** high | **layers:** D0 content/text; D1 data tables (PTF); D3 Lua scripts
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `1.9.6`, loads on 1.9.8: NO (disabled: lists 1.9.6)
- **Where it changes things:** tables (PTF): 4; scripts (Lua): 2; localization: 2; manifest: 1; pak (container): 1; lua identical to vanilla: 0
- **Tables:** buff, perk, perk_buff, soul (3 new rows, 8 changed, 0 identical to vanilla, 6145 vanilla rows dropped by a whole-table replace); median relative change 1.0
- **Largest changes:** buff:7e42e183-222b-42a6-addb-e1e1cb4ae4d3 NEW row; perk_buff:c92e5f13-4b57-4b02-b9cf-74e88e3b2517/7e42e183-222b-42a6-addb-e1e1cb4ae4d3 NEW row; perk:c92e5f13-4b57-4b02-b9cf-74e88e3b2517 NEW row; buff:8b546698-15a0-42bf-bf7f-634a932d2b8c params btw*0.4->btw*2; soul:00000000-0000-0000-0000-000000035000/959cb495-2b5b-42fe-bd47-9bcb3f1faeef////////8/5/14/4d9275e7-744b-2390-1e8d-943e0f2501a4/0 hearing 0->100; soul:00000000-0000-0000-0000-000000035000/48ad69c2-db1c-bd02-64a2-43d82129c981////////8/11/24/41f5c883-299d-645f-5a42-92db0d6c6c91/0 hearing 0->70; soul:00000000-0000-0000-0000-000000035000/434b2093-4f51-838c-aa4e-bdd16f27a4b5////////8/10/22/4eca3014-efa1-e85e-414d-c454aaed1baf/0 hearing 0->
- **Lua:** 2 files, 31 lines; API used: System.LogAlwaysx5, player.soulx2, Script.ReloadScriptx1
- **Text:** 0 strings changed, 4 new
- **Risk:** none

## 802 Archery for 1.9 (P2, Archery / arrows)

- **What the author says (Nexus summary):** An update of archery variables 'rpg_param,xml' for 1.9
- **File:** `Archer for 1.9-802-1-1563644280.7z` (archive, 0.0 MB, `c_archery-arrows`), full (scratch, deleted after reading)
- **Grade:** C effective (few rows, strong effect) | **perceptibility:** high | **layers:** D1 data tables (PTF)
- **How it installs:** loose .pak (legacy: copy into Data); manifest id `-`, supports `-`, loads on 1.9.8: no manifest (legacy install)
- **Where it changes things:** pak (container): 1; other: 1; tables (PTF): 1; lua identical to vanilla: 0
- **Tables:** rpg_param (9 new rows, 1 changed, 181 identical to vanilla); median relative change 0.5
- **Largest changes:** rpg_param:BowPowerToChargeDuration NEW row; rpg_param:BowChargeDurationMin NEW row; rpg_param:BowChargeDurationMax NEW row; rpg_param:AimSpreadSkillDecrease NEW row; rpg_param:AimZoomBase NEW row; rpg_param:AimZoomBaseSkill NEW row; rpg_param:AimZoomMax NEW row; rpg_param:AimSkillToZoom NEW row
- **Problems:** Archery 1.9/Data/Archery1.9.pak!Libs/Tables/rpg/rpg_param.xml: no suffix: replaces the whole vanilla table
- **Risk:** none

## 1266 Stronger drinks - PTF Edition (P2, Alchemy / food / survival)

- **What the author says (Nexus summary):** Raises the alcohol percentage of drinks (beer 8, moonshine 53, wine 18, mead 25 ...) in the food table; incompatible with mods that override the whole food.xml This mod increases the alcohol percentage in all drinks by about 50%
- **File:** `stronger_drinks-1266-1-0-1627071776.rar` (archive, 0.0 MB, `c_alchemy-food-survival`), full (scratch, deleted after reading)
- **Grade:** C effective (few rows, strong effect) | **perceptibility:** high | **layers:** D1 data tables (PTF)
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `(none)`, loads on 1.9.8: yes (no version restriction)
- **Where it changes things:** manifest: 1; pak (container): 1; tables (PTF): 1; lua identical to vanilla: 0
- **Tables:** food (0 new rows, 9 changed, 0 identical to vanilla, 193 vanilla rows dropped by a whole-table replace); median relative change 0.5
- **Largest changes:** food:9e782670-3291-4382-a6d3-a843d13e67d9 alcohol_content 5->30; food:2529e246-6f1b-4529-8d6b-64245207bae8 alcohol_content 90->160; food:52afd6fa-9377-457c-83a2-b5b39321a4dc alcohol_content 15->24; food:390c0dc8-23fd-42a0-91f2-a4d42f96a387 alcohol_content 50->75; food:c64b7286-07b8-4bdf-afd0-359171d35249 alcohol_content 80->120; food:ca5a0aa3-e373-48ec-96e4-1c3b9907bac3 alcohol_content 30->45; food:38df365c-a4bb-462b-80cc-eb92f16930fa alcohol_content 40->55; food:7c5126cd-b010-4484-8465-22a3d69fa0df alcohol_content 40->55
- **Risk:** none

## 1243 Easier Enemies PTF (Dumber Enemies) (P2, Combat / AI)

- **What the author says (Nexus summary):** This mod makes enemies less aggressive by reducing how often they dodge, parry, attack, and how often they attack in groups.Comes in 4 versions, 0%, 25%, 50%, and 75% easier than vanilla. All of these versions stop npcs from using master
- **File:** `02- 50 percent dumber enemies-1243-1-1-1618286957.rar` (archive, 0.0 MB, `c_combat-ai`), full (scratch, deleted after reading)
- **Grade:** C effective (few rows, strong effect) | **perceptibility:** high | **layers:** D1 data tables (PTF)
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `(none)`, loads on 1.9.8: yes (no version restriction)
- **Where it changes things:** manifest: 1; pak (container): 1; tables (PTF): 1; lua identical to vanilla: 0
- **Tables:** rpg_param (0 new rows, 8 changed, 0 identical to vanilla, 174 vanilla rows dropped by a whole-table replace); median relative change 0.629
- **Largest changes:** rpg_param:CombatAutoAttackDelayIncreasePerAttacker rpg_param_value 0.8->3.2; rpg_param:CombatAutoNoDefenseWeight rpg_param_value 0.4->1.2025; rpg_param:CombatAutoSPBWeight rpg_param_value 1.5->0; rpg_param:CombatAutoNormalBWeight rpg_param_value 2.8->4.9225; rpg_param:CombatAutoMaxAttackDelay rpg_param_value 6->9; rpg_param:CombatAutoUnarmedBlockProb rpg_param_value 1.6->0.8; rpg_param:CombatAutoPBWeight rpg_param_value 2.5->1.4375; rpg_param:CombatAutoDodgeWeight rpg_param_value 1.1->0.7375
- **Risk:** none

## 1842 Realistic Repairs (P2, Weapons / armor / items)

- **What the author says (Nexus summary):** Allows you to use your repair tools on gears that have above 10 durability left.
- **File:** `Realistic Repairs 1.1-1842-1-1-1739569897.rar` (archive, 0.0 MB, `c_weapons-armor-items`), full (scratch, deleted after reading)
- **Grade:** C effective (few rows, strong effect) | **perceptibility:** high | **layers:** D1 data tables (PTF)
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `1.*`, loads on 1.9.8: yes (wildcard)
- **Where it changes things:** tables (PTF): 3; manifest: 1; pak (container): 1; lua identical to vanilla: 0
- **Tables:** perk_rpg_param_override, rpg_param, skill2item_category (4 new rows, 4 changed, 0 identical to vanilla, 250 vanilla rows dropped by a whole-table replace); median relative change 0.567
- **Largest changes:** skill2item_category:armor.horse_bridle.*/8 NEW row; skill2item_category:armor.horse_saddle.*/8 NEW row; rpg_param:RepairKitItemHealthBestLimit NEW row; rpg_param:RepairKitItemHealthDefaultLimit NEW row; rpg_param:RepairPriceModif rpg_param_value 0.65->1.2; perk_rpg_param_override:01c3b32a-5751-4c98-b6ab-258d02370382/RepairKitItemHealthBestLimit rpg_param_value 0.5->0.1; perk_rpg_param_override:01c3b32a-5751-4c98-b6ab-258d02370382/RepairPriceModif rpg_param_value 0.9->1.2; perk_rpg_param_override:01c3b32a-5751-4c98-b6ab-258d02370382/RepairKitItemHealthDefaultLimit rpg_param_value 0.7->0.6
- **Same rows as KRS:** krs_qol:perk_rpg_param_override:01c3b32a-5751-4c98-b6ab-258d02370382/RepairPriceModif; krs_qol:rpg_param:RepairPriceModif; krs_qol:skill2item_category:armor.horse_bridle.*/8; krs_qol:skill2item_category:armor.horse_saddle.*/8
- **Risk:** none

## 2021 Repair Kits - Balanced and Scaled PTF (P2, Weapons / armor / items)

- **What the author says (Nexus summary):** Rescales armourer, blacksmith, tailor and cobbler kit efficiency (small and large); normal and Hardcore modes. Same area as krs_qol repairs Fixes the imbalance between small and large armourer’s kits by adjusting their efficiency. All repair kits received a small balanced boost, making them more use
- **File:** `Repair Kits - Balanced and Scaled PTF-2021-1-2-1779784418.7z` (archive, 0.0 MB, `c_weapons-armor-items`), full (scratch, deleted after reading)
- **Grade:** C effective (few rows, strong effect) | **perceptibility:** high | **layers:** D1 data tables (PTF)
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `1.9.4 1.9.5 1.9.6 1.9.7 1.9.8`, loads on 1.9.8: yes (explicit)
- **Where it changes things:** manifest: 1; pak (container): 1; tables (PTF): 1; lua identical to vanilla: 0
- **Tables:** ointment_item (0 new rows, 8 changed, 0 identical to vanilla, 2 vanilla rows dropped by a whole-table replace); median relative change 1.0
- **Largest changes:** ointment_item:238538b5-cd3e-460e-8e85-52c820edb716 efficiency 0.5->1; ointment_item:6aeb1531-369e-47cc-ad6c-f78df1c37d13 efficiency 1->2; ointment_item:85310d06-2845-46ee-be8f-295503b35035 efficiency 0.1->0.2; ointment_item:9f7a0c0a-6458-4622-9cc5-2f4dd4898b50 efficiency 0.1->0.2; ointment_item:c707733a-c0a7-4f02-b684-9392b0b15b83 efficiency 0.2->0.4; ointment_item:cda856d8-9ee4-4f61-b2c7-eace8e082d62 efficiency 0.5->1; ointment_item:f961d38d-12e6-430c-92d5-d7e7e45a87e9 efficiency 1->2; ointment_item:167eb312-0e9d-4c2f-8ce3-56c32f5a84cb efficiency 0.5->0.4
- **Risk:** none

## 2340 MatthusTweaks - Equipment and Progression Overhaul (PTF) (P2, Progression / XP / perks)

- **What the author says (Nexus summary):** This mod fixes and rebalances: + Misused items + Layered damage.
- **File:** `MatthusTweaksKCD Layered Damage Fix V1.0 2340 1 2026-09-02T00-01Z M04BeYCgC.zip` (archive, 0.0 MB, `c_progression-xp-perks`), full (scratch, deleted after reading)
- **Grade:** C effective (few rows, strong effect) | **perceptibility:** high | **layers:** D1 data tables (PTF)
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `1.*`, loads on 1.9.8: yes (wildcard)
- **Where it changes things:** tables (PTF): 2; other: 1; manifest: 1; pak (container): 1; lua identical to vanilla: 0
- **Tables:** perk_rpg_param_override, rpg_param (6 new rows, 0 changed, 0 identical to vanilla, 207 vanilla rows dropped by a whole-table replace); median relative change 0.0
- **Largest changes:** perk_rpg_param_override:01c3b32a-5751-4c98-b6ab-258d02370382/DamageToArmorStatus NEW row; perk_rpg_param_override:01c3b32a-5751-4c98-b6ab-258d02370382/DamageToArmorStatusHigherLayers NEW row; perk_rpg_param_override:01c3b32a-5751-4c98-b6ab-258d02370382/DamageToArmorStatusLowerLayers NEW row; rpg_param:DamageToArmorStatus NEW row; rpg_param:DamageToArmorStatusHigherLayers NEW row; rpg_param:DamageToArmorStatusLowerLayers NEW row
- **Risk:** none

## 480 Bed Comfort Restored (P2, Alchemy / food / survival)

- **What the author says (Nexus summary):** Brings back the Comfort value of beds that have been nerfed by Patch 1.3Compatible with Patch 1.4.1
- **File:** `Bed Comfort Restored-480-1-0.zip` (archive, 0.0 MB, `c_alchemy-food-survival`), full (scratch, deleted after reading)
- **Grade:** C effective (few rows, strong effect) | **perceptibility:** high | **layers:** D1 data tables (PTF)
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `(none)`, loads on 1.9.8: yes (no version restriction)
- **Where it changes things:** manifest: 1; pak (container): 1; other: 1; tables (PTF): 1; lua identical to vanilla: 0
- **Tables:** sleeping_spot_type (0 new rows, 5 changed, 0 identical to vanilla); median relative change 0.6
- **Largest changes:** sleeping_spot_type:4 sleeping_quality 0.1->0.3; sleeping_spot_type:2 sleeping_quality 0.3->0.5; sleeping_spot_type:3 sleeping_quality 0.5->0.8; sleeping_spot_type:1 sleeping_quality 0.7->1; sleeping_spot_type:0 sleeping_quality 1->1.2
- **Same rows as KRS:** krs_items:sleeping_spot_type:0; krs_items:sleeping_spot_type:1; krs_items:sleeping_spot_type:2; krs_items:sleeping_spot_type:3
- **Problems:** Data/Bed_Comfort.pak!Libs/Tables/rpg/sleeping_spot_type.xml: no suffix: replaces the whole vanilla table
- **Risk:** none

## 1243 Easier Enemies PTF (Dumber Enemies) (P2, Combat / AI)

- **What the author says (Nexus summary):** This mod makes enemies less aggressive by reducing how often they dodge, parry, attack, and how often they attack in groups.Comes in 4 versions, 0%, 25%, 50%, and 75% easier than vanilla. All of these versions stop npcs from using master
- **File:** `04- no npc master strike-1243-1-0-1618262566.rar` (archive, 0.0 MB, `c_combat-ai`), full (scratch, deleted after reading)
- **Grade:** C effective (few rows, strong effect) | **perceptibility:** high | **layers:** D1 data tables (PTF)
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `(none)`, loads on 1.9.8: yes (no version restriction)
- **Where it changes things:** other xml (data): 2; manifest: 1; pak (container): 1; tables (PTF): 1; lua identical to vanilla: 0
- **Tables:** rpg_param (0 new rows, 5 changed, 0 identical to vanilla, 177 vanilla rows dropped by a whole-table replace); median relative change 0.341
- **Largest changes:** rpg_param:CombatAutoSPBWeight rpg_param_value 1.5->0; rpg_param:CombatAutoNoDefenseWeight rpg_param_value 0.4->0.775; rpg_param:CombatAutoDodgeWeight rpg_param_value 1.1->1.475; rpg_param:CombatAutoPBWeight rpg_param_value 2.5->2.875; rpg_param:CombatAutoNormalBWeight rpg_param_value 2.8->3.175
- **Risk:** none

## 1375 No Aim Spread (Bow sway disabler) (P2, Archery / arrows)

- **What the author says (Nexus summary):** Adds a perk (True Shot) that removes bow sway for the player only; variant 2.1b has two stat-gated perks (Forceful Grip: Strength min 10; Ranger's Precision: Agility min 8). A perk-based way to change a bow constant per player Disables horizontal bow swaying when aiming. New version doesn't affect N
- **File:** `No Aim Spread - Normal version-1375-2-2-1775620893.zip` (archive, 0.0 MB, `c_archery-arrows`), full (scratch, deleted after reading)
- **Grade:** C effective (few rows, strong effect) | **perceptibility:** high | **layers:** D0 content/text; D1 data tables (PTF)
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `1.9.4 1.9.5 1.9.6 1.9.7`, loads on 1.9.8: NO (disabled: lists 1.9.4, 1.9.5, 1.9.6, 1.9.7)
- **Where it changes things:** tables (PTF): 6; localization: 2; manifest: 1; pak (container): 1; lua identical to vanilla: 0
- **Tables:** buff, game_mode, perk, perk_buff, soul2perk (5 new rows, 0 changed, 1 identical to vanilla, 50029 vanilla rows dropped by a whole-table replace); median relative change 0.0
- **Largest changes:** perk:ae32e325-fe7e-48d6-90bc-d04707e9fe5b NEW row; buff:dfa3d59d-5da0-41bc-8ce5-a2c1d7b4ed0c NEW row; perk_buff:ae32e325-fe7e-48d6-90bc-d04707e9fe5b/dfa3d59d-5da0-41bc-8ce5-a2c1d7b4ed0c NEW row; soul2perk:ae32e325-fe7e-48d6-90bc-d04707e9fe5b/43430cfa-9d81-0432-ab95-43f66f3c04a3 NEW row; game_mode:1/ae32e325-fe7e-48d6-90bc-d04707e9fe5b NEW row
- **Text:** 0 strings changed, 2 new
- **Risk:** none

## 1424 Better Sleep Fixed (P2, Alchemy / food / survival)

- **What the author says (Nexus summary):** This is a fixed version of BlickMang's Better Sleep mod. As luck would have it they gave us permission to modify, fix and upgrade so long as credit to the original author is provided.
- **File:** `Better Sleep Fixed-1424-1-1-1666227085.zip` (archive, 0.0 MB, `c_alchemy-food-survival`), full (scratch, deleted after reading)
- **Grade:** C effective (few rows, strong effect) | **perceptibility:** high | **layers:** D1 data tables (PTF)
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `1.9.4 1.9.5 1.9.6 1.9.7`, loads on 1.9.8: NO (disabled: lists 1.9.4, 1.9.5, 1.9.6, 1.9.7)
- **Where it changes things:** manifest: 1; pak (container): 1; other: 1; tables (PTF): 1; lua identical to vanilla: 0
- **Tables:** sleeping_spot_type (0 new rows, 5 changed, 0 identical to vanilla); median relative change 1.4
- **Largest changes:** sleeping_spot_type:4 sleeping_quality 0.1->1.2; sleeping_spot_type:2 sleeping_quality 0.3->1.2; sleeping_spot_type:3 sleeping_quality 0.5->1.2; sleeping_spot_type:1 sleeping_quality 0.7->1.2; sleeping_spot_type:0 sleeping_quality 1->1.2
- **Same rows as KRS:** krs_items:sleeping_spot_type:0; krs_items:sleeping_spot_type:1; krs_items:sleeping_spot_type:2; krs_items:sleeping_spot_type:3
- **Problems:** BetterSleep/Data/zzz_better_sleep.pak!Libs/Tables/rpg/sleeping_spot_type.xml: no suffix: replaces the whole vanilla table
- **Risk:** none

## 1782 No more clipping elbows for Andrew (P2, World / weather / visuals)

- **What the author says (Nexus summary):** Replaces Andrew the inn-keeper's body clothing to stop his elbows clipping through the sleeves.
- **File:** `Andrew Clothing Fix-1782-1-0-1736793391.rar` (archive, 0.0 MB, `c_world-weather-visuals`), full (scratch, deleted after reading)
- **Grade:** C effective (few rows, strong effect) | **perceptibility:** high | **layers:** D1 data tables (PTF)
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `1.9.*`, loads on 1.9.8: yes (wildcard)
- **Where it changes things:** tables (PTF): 2; manifest: 1; pak (container): 1; lua identical to vanilla: 0
- **Tables:** armor2clothing_preset, soul (5 new rows, 0 changed, 0 identical to vanilla, 13709 vanilla rows dropped by a whole-table replace); median relative change 0.0
- **Largest changes:** armor2clothing_preset:40692480-f24c-54fa-c938-50ccf45918b9/954dbf59-076e-094b-5d0a-4e44bec85cbb NEW row; armor2clothing_preset:4517b07b-ca19-07bf-6011-e2cec8868185/954dbf59-076e-094b-5d0a-4e44bec85cbb NEW row; armor2clothing_preset:473110cf-b888-a84b-7c65-e5b1beab47ac/954dbf59-076e-094b-5d0a-4e44bec85cbb NEW row; armor2clothing_preset:4b92491f-060f-d00d-642c-c7b5f9807aaf/954dbf59-076e-094b-5d0a-4e44bec85cbb NEW row; soul:00000000-0000-0000-0000-000000035000/2a7b75cd-8344-43f6-8483-0191a079e503//9fe6dae0-e195-42e0-a3fb-66cfc6382407//4d033237-bfba-f43a-beb2-172f2d8287bf/954dbf59-076e-094b-5d0a-4e44bec85cbb//d2db67fd-70cb-4791-8513-ac047f4e8616/226/6/0/29/469a778e-29f9-96ae-2132-5156c40d4281/0 
- **Risk:** none

## 1195 Get Water (P2, Alchemy / food / survival)

- **What the author says (Nexus summary):** Adds a water canteen that players can use to get water ingame. Is meant as a complementary Mod for "Fishing in Bohemia" by Chrisaton6799 and "SIM Camping Mini" by VVL99.
- **File:** `Get Water-1195-1-0-1612638603.7z` (archive, 0.01 MB, `c_alchemy-food-survival`), full (scratch, deleted after reading)
- **Grade:** C effective (few rows, strong effect) | **perceptibility:** high | **layers:** D0 content/text; D1 data tables (PTF); D3 Lua scripts
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `1.9.6`, loads on 1.9.8: NO (disabled: lists 1.9.6)
- **Where it changes things:** tables (PTF): 4; ui: 2; scripts (Lua): 2; localization: 2; manifest: 1; pak (container): 1; lua identical to vanilla: 0
- **Tables:** item, pickable_item, player_item, questible_item (4 new rows, 0 changed, 0 identical to vanilla, 7378 vanilla rows dropped by a whole-table replace); median relative change 0.0
- **Largest changes:** item:2aef9b0a-f485-4935-be7d-7ceee381b547 NEW row; pickable_item:2aef9b0a-f485-4935-be7d-7ceee381b547 NEW row; player_item:2aef9b0a-f485-4935-be7d-7ceee381b547 NEW row; questible_item:2aef9b0a-f485-4935-be7d-7ceee381b547 NEW row
- **Lua:** 2 files, 152 lines; API used: player.inventoryx9, System.LogAlwaysx4, System.GetEntitiesInSpherex3, Game.SendInfoTextx3, Database.LoadTablex1, Database.GetTableInfox1
- **Text:** 0 strings changed, 8 new
- **Risk:** none

## 1292 Ultimate Repair Kit 2.0 (P2, Weapons / armor / items)

- **What the author says (Nexus summary):** This mod aims to recreate the experience of Ultimate Repair Kit that will actually work with the new version of the game, be compatible with most other mods and hopefully won't break with time. It allows you to use repair kits to repair
- **File:** `Ultimate Repair Kit 2.0-1292-1-2-1642365001.7z` (archive, 0.0 MB, `c_weapons-armor-items`), full (scratch, deleted after reading)
- **Grade:** C effective (few rows, strong effect) | **perceptibility:** high | **layers:** D1 data tables (PTF)
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `1.9.*`, loads on 1.9.8: yes (wildcard)
- **Where it changes things:** tables (PTF): 3; manifest: 1; pak (container): 1; lua identical to vanilla: 0
- **Tables:** perk_rpg_param_override, rpg_param, skill2item_category (3 new rows, 1 changed, 0 identical to vanilla, 253 vanilla rows dropped by a whole-table replace); median relative change 0.0
- **Largest changes:** rpg_param:RepairKitItemHealthBestLimit NEW row; skill2item_category:armor.horse_bridle.*/8 NEW row; skill2item_category:armor.horse_saddle.*/8 NEW row; perk_rpg_param_override:01c3b32a-5751-4c98-b6ab-258d02370382/RepairKitItemHealthBestLimit rpg_param_value 0.5->
- **Same rows as KRS:** krs_qol:skill2item_category:armor.horse_bridle.*/8; krs_qol:skill2item_category:armor.horse_saddle.*/8
- **Risk:** none

## 284 No Mo' Slow Mo - Configurable Perfect Block Slow Motion and AI Master Strike frequency (P2, Crime / stealth / loot)

- **What the author says (Nexus summary):** Adds a console command for the perfect-block slow-motion length (can disable it) and sets how often the AI uses master strikes; optional sound files This mod adds a console command to configure the length of the Perfect Block slow-motion effect, including disabling it completely. Also includes optio
- **File:** `NoMoSlowMo - Options-284-2-0b-1672359814.7z` (archive, 1.11 MB, `c_crime-stealth-loot`), full (scratch, deleted after reading)
- **Grade:** C effective (few rows, strong effect) | **perceptibility:** high | **layers:** D0 content/text; D1 data tables (PTF)
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `1.9.*`, loads on 1.9.8: yes (wildcard)
- **Where it changes things:** other xml (data): 3; manifest: 3; pak (container): 3; tables (PTF): 3; textures: 1; docs: 1; lua identical to vanilla: 0
- **Tables:** rpg_param (0 new rows, 3 changed, 0 identical to vanilla, 543 vanilla rows dropped by a whole-table replace); median relative change 1.667
- **Largest changes:** rpg_param:CombatAutoSPBWeight rpg_param_value 1.5->-1; rpg_param:CombatAutoSPBWeight rpg_param_value 1.5->-1; rpg_param:CombatAutoSPBWeight rpg_param_value 1.5->0.75
- **Problems:** NoMoSloMo - Options/NoAIMasterStrikes/Data/noaimasterstrikes.pak!Libs/Tables/rpg/rpg_param__noaimasterstrikes.xml: suffix 'noaimasterstrikes' != id 'lessaimasterstrikes' (the game ignores it) / NoMoSloMo - Options/NoAIMasterStrikes/Data/Libs/Tables/rpg/rpg_param__noaimasterstrikes.xml: suffix 'noaimasterstrikes' != id 'lessaimasterstrikes' (the game ignores it)
- **Risk:** none

## 1100 Faster archery - PTF Edition (P2, Archery / arrows)

- **What the author says (Nexus summary):** Sets BowChargeDurationMax (1.00 hard / 1.25 normal / 1.50 easy) through rpg_param; aim spread unchanged. Shows that a published mod already sets this hidden constant by a table patch This mod decrease the charge duration (how fast you can charge a bow). There are three editions.
- **File:** `Faster archery easy-1100-1-0-1600006459.rar` (archive, 0.0 MB, `c_archery-arrows`), full (scratch, deleted after reading)
- **Grade:** C effective (few rows, strong effect) | **perceptibility:** high | **layers:** D1 data tables (PTF)
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `(none)`, loads on 1.9.8: yes (no version restriction)
- **Where it changes things:** manifest: 1; pak (container): 1; tables (PTF): 1; lua identical to vanilla: 0
- **Tables:** rpg_param (3 new rows, 0 changed, 0 identical to vanilla, 182 vanilla rows dropped by a whole-table replace); median relative change 0.0
- **Largest changes:** rpg_param:BowChargeDurationMin NEW row; rpg_param:BowChargeDurationMax NEW row; rpg_param:BowPowerToChargeDuration NEW row
- **Risk:** none

## 1863 Dirty And Charismatic - PTF (P2, Progression / XP / perks)

- **What the author says (Nexus summary):** With this mod, dirt and armor state will no longer affect Henry's charisma - PTF (should be compatible with PTF mods).
- **File:** `Dirty And Charismatic-1863-1-0-1739534931.zip` (archive, 0.0 MB, `c_progression-xp-perks`), full (scratch, deleted after reading)
- **Grade:** C effective (few rows, strong effect) | **perceptibility:** high | **layers:** D1 data tables (PTF)
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `dirtyandcharismatic`, supports `(none)`, loads on 1.9.8: yes (no version restriction)
- **Where it changes things:** tables (PTF): 2; manifest: 1; pak (container): 1; lua identical to vanilla: 0
- **Tables:** perk_rpg_param_override (2 new rows, 1 changed, 0 identical to vanilla, 49 vanilla rows dropped by a whole-table replace); median relative change 1.0
- **Largest changes:** perk_rpg_param_override:/ArmorDirtToCharismaCoef NEW row; perk_rpg_param_override:/ArmorStatusToCharismaCoef NEW row; perk_rpg_param_override:01c3b32a-5751-4c98-b6ab-258d02370382/ArmorStatusToCharismaCoef rpg_param_value 0.6->0
- **Risk:** none

## 2340 MatthusTweaks - Equipment and Progression Overhaul (PTF) (P2, Progression / XP / perks)

- **What the author says (Nexus summary):** This mod fixes and rebalances: + Misused items + Layered damage.
- **File:** `MatthusTweaksKCD Sabres V1.0 2340 1 2026-08-31T00-37Z 5RVx9I3GV.zip` (archive, 0.0 MB, `c_progression-xp-perks`), full (scratch, deleted after reading)
- **Grade:** C effective (few rows, strong effect) | **perceptibility:** high | **layers:** D1 data tables (PTF)
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `1.*`, loads on 1.9.8: yes (wildcard)
- **Where it changes things:** tables (PTF): 2; other: 1; manifest: 1; pak (container): 1; lua identical to vanilla: 0
- **Tables:** shop_type2item, weapon2weapon_preset (1 new rows, 2 changed, 1 identical to vanilla, 885 vanilla rows dropped by a whole-table replace); median relative change 0.0
- **Largest changes:** shop_type2item:aca90050-0b70-4ca0-9d29-b94326203c75 NEW row; weapon2weapon_preset:ec470e0c-5bbd-43bb-803e-0e7867253c25 weapon_preset_id 463dc53f-86c2-5b8c-a->42b3ad6f-cc12-bcb2-e; weapon2weapon_preset:ec470e0c-5bbd-43bb-803e-0e7867253c25 weapon_preset_id 463dc53f-86c2-5b8c-a->48271a75-6e1e-269a-f
- **Risk:** none

## 390 Stay Clean Longer - Get Dirty Gradually (P2, Alchemy / food / survival)

- **What the author says (Nexus summary):** This is a simple mod to keep your clothes clean for a longer distance.They will get dirty gradually and you need to wash them, but not as often as in the base game.
- **File:** `MGs Stay Clean Longer - Get Dirty Gradually 1.6-390-1-6-1707663382` (folder (already extracted), 0 MB, `c_alchemy-food-survival`), read in place (already extracted by the author)
- **Grade:** C effective (few rows, strong effect) | **perceptibility:** high | **layers:** D1 data tables (PTF)
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `(none)`, loads on 1.9.8: yes (no version restriction)
- **Where it changes things:** tables (PTF): 2; manifest: 1; other: 1; lua identical to vanilla: 0
- **Tables:** perk_rpg_param_override, rpg_param (1 new rows, 1 changed, 0 identical to vanilla, 206 vanilla rows dropped by a whole-table replace); median relative change 1.0
- **Largest changes:** perk_rpg_param_override:01c3b32a-5751-4c98-b6ab-258d02370382/FullClothDirtyingOnFullSpeed rpg_param_value 5000->10000; rpg_param:FullClothDirtyingOnFullSpeed NEW row
- **Risk:** MEDIUM: MEDIUM: nested archive (not readable by the game): Data/StayCleanLongerGetDirtyGradually.7zip

## 1084 Overpowered Bows - PTF Edition (P2, Archery / arrows)

- **What the author says (Nexus summary):** Raises the power of the Sinew and Hans Capon bows (100/200/500/1000 power editions); conflicts with mods that change those bows or override the whole missile_weapon table Increase the power on the Sinew and Hans Capon's bow.
- **File:** `op_bows_power_100-1084-1-1-1598736006.rar` (archive, 0.0 MB, `c_archery-arrows`), full (scratch, deleted after reading)
- **Grade:** C effective (few rows, strong effect) | **perceptibility:** high | **layers:** D1 data tables (PTF)
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `(none)`, loads on 1.9.8: yes (no version restriction)
- **Where it changes things:** manifest: 1; pak (container): 1; tables (PTF): 1; lua identical to vanilla: 0
- **Tables:** missile_weapon (0 new rows, 2 changed, 0 identical to vanilla, 21 vanilla rows dropped by a whole-table replace); median relative change 0.536
- **Largest changes:** missile_weapon:f2c83abc-2252-49f6-bbb7-dc8bc02979b2 power 54->100; missile_weapon:9bafcc7f-3931-4cc4-89ce-8f6ab205dfa8 power 82->100
- **Risk:** none

## 1236 Easy Combat PTF (easy parry and master strike) (P2, Combat / AI)

- **What the author says (Nexus summary):** Combat made easy :1-Easier Parries and Master Strikes from the player character.
- **File:** `easycombat-1236-1-1-1618287536.rar` (archive, 0.0 MB, `c_combat-ai`), full (scratch, deleted after reading)
- **Grade:** C effective (few rows, strong effect) | **perceptibility:** high | **layers:** D1 data tables (PTF)
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `(none)`, loads on 1.9.8: yes (no version restriction)
- **Where it changes things:** manifest: 1; pak (container): 1; tables (PTF): 1; other xml (data): 1; lua identical to vanilla: 0
- **Tables:** rpg_param (0 new rows, 2 changed, 0 identical to vanilla, 180 vanilla rows dropped by a whole-table replace); median relative change 3.265
- **Largest changes:** rpg_param:MaxSpecialPerfectBlockSlotModifier rpg_param_value 0.6->3; rpg_param:MaxPerfectBlockSlotModifier rpg_param_value 0.85->3
- **Risk:** none

## 1426 Energy and Hunger Patch for Timescale Mods (PTF) (P2, Alchemy / food / survival)

- **What the author says (Nexus summary):** Keeps energy and hunger depletion proportional to in-game time when a timescale mod is used; safe if loaded after non-PTF mods (PTF) Patch for use with eg SknTheLisper's Timescale mod to make Energy and Nourishment deplete at the correct rates (proportional to an unmodded game's rate)
- **File:** `1to10 Timescale Patch-1426-1-0-1666809096.rar` (archive, 0.0 MB, `c_alchemy-food-survival`), full (scratch, deleted after reading)
- **Grade:** C effective (few rows, strong effect) | **perceptibility:** high | **layers:** D1 data tables (PTF)
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `(none)`, loads on 1.9.8: yes (no version restriction)
- **Where it changes things:** manifest: 1; pak (container): 1; tables (PTF): 1; lua identical to vanilla: 0
- **Tables:** rpg_param (2 new rows, 0 changed, 0 identical to vanilla, 182 vanilla rows dropped by a whole-table replace); median relative change 0.0
- **Largest changes:** rpg_param:DigestionSpeed NEW row; rpg_param:ExhaustionSpeed NEW row
- **Same rows as KRS:** krs_items:rpg_param:DigestionSpeed
- **Risk:** none

## 1765 Restore Riposte (P1, Combat / AI)

- **What the author says (Nexus summary):** Restore Riposte for player use.Pick up your weapons and get a head start on adapting to the new combat system before KCD2 comes!
- **File:** `Riposte-1765-1-0-2-1735871267` (folder (already extracted), 0 MB, `c_combat-ai`), read in place (already extracted by the author)
- **Grade:** C effective (few rows, strong effect) | **perceptibility:** high | **layers:** D0 content/text; D1 data tables (PTF)
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `1.9.6`, loads on 1.9.8: NO (disabled: lists 1.9.6)
- **Where it changes things:** localization: 8; other: 2; manifest: 1; other xml (data): 1; tables (PTF): 1; lua identical to vanilla: 0
- **Tables:** perk (0 new rows, 2 changed, 0 identical to vanilla, 549 vanilla rows dropped by a whole-table replace); median relative change 0.8
- **Largest changes:** perk:ec4c5274-50e3-4bbf-9220-823b080647c4 visibility 0->2; perk:61e98757-9b32-493b-ad09-0087afdb81be visibility 0->1
- **Text:** 3 strings changed, 16 new
- **Same rows as KRS:** krs_perks:perk:61e98757-9b32-493b-ad09-0087afdb81be; krs_perks:perk:ec4c5274-50e3-4bbf-9220-823b080647c4
- **Risk:** MEDIUM: MEDIUM: nested archive (not readable by the game): Riposte.7zip / MEDIUM: nested archive (not readable by the game): Data/Riposte.7zip

## 1862 Faster Inury Regeneration - PTF (P2, Alchemy / food / survival)

- **What the author says (Nexus summary):** Injuries heal faster; PTF This mod makes injuries heal faster - PTF (should be compatible with PTF mods).
- **File:** `Faster Injury Regeneration x2-1862-1-0-1739533911.zip` (archive, 0.0 MB, `c_alchemy-food-survival`), full (scratch, deleted after reading)
- **Grade:** C effective (few rows, strong effect) | **perceptibility:** high | **layers:** D1 data tables (PTF)
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `fasterinjuryregeneration`, supports `(none)`, loads on 1.9.8: yes (no version restriction)
- **Where it changes things:** tables (PTF): 2; manifest: 1; pak (container): 1; lua identical to vanilla: 0
- **Tables:** perk_rpg_param_override (1 new rows, 1 changed, 0 identical to vanilla, 49 vanilla rows dropped by a whole-table replace); median relative change 0.5
- **Largest changes:** perk_rpg_param_override:/InjuryRegenInterval NEW row; perk_rpg_param_override:01c3b32a-5751-4c98-b6ab-258d02370382/InjuryRegenInterval rpg_param_value 15->7.5
- **Risk:** none

## 1893 Bianca's Ring PTF (P2, Weapons / armor / items)

- **What the author says (Nexus summary):** This is a work in progress mod aiming to bring the Bianca's Ring mods to a PTF version, but to make it less OP
- **File:** `Bianca's Ring PTF-1893-0-1-1740174007.zip` (archive, 0.0 MB, `c_weapons-armor-items`), full (scratch, deleted after reading)
- **Grade:** C effective (few rows, strong effect) | **perceptibility:** high | **layers:** D1 data tables (PTF)
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `(none)`, loads on 1.9.8: yes (no version restriction)
- **Where it changes things:** tables (PTF): 3; manifest: 1; pak (container): 1; lua identical to vanilla: 0
- **Tables:** armor, equippable_item (0 new rows, 2 changed, 1 identical to vanilla, 4003 vanilla rows dropped by a whole-table replace); median relative change 1.0
- **Largest changes:** equippable_item:aac0794c-8fb7-41f5-ba6a-90c313c286b2 conspicuousness 0.1->-1; armor:aac0794c-8fb7-41f5-ba6a-90c313c286b2 noise 0->-1
- **Problems:** BiancaRing/Data/bianca_ring.pak!Libs/Tables/item/armor__bianca.xml: suffix 'bianca' != id 'bianca's_ring_ptf' (the game ignores it) / BiancaRing/Data/bianca_ring.pak!Libs/Tables/item/equippable_item__bianca.xml: suffix 'bianca' != id 'bianca's_ring_ptf' (the game ignores it) / BiancaRing/Data/bianca_ring.pak!Libs/Tables/item/pickable_item__bianca.xml: suffix 'bianca' != id 'bianca's_ring_ptf' (the game ignores it)
- **Risk:** none

## 1425 Saving Soles (PTF) (P2, Weapons / armor / items)

- **What the author says (Nexus summary):** (PTF) I found myself running around bare foot just to protect the durability of my boots, well with this you wont need to anymore
- **File:** `SavingSoles-1425-1-0-1666738645.rar` (archive, 0.0 MB, `c_weapons-armor-items`), full (scratch, deleted after reading)
- **Grade:** C effective (few rows, strong effect) | **perceptibility:** high | **layers:** D1 data tables (PTF)
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `(none)`, loads on 1.9.8: yes (no version restriction)
- **Where it changes things:** manifest: 1; pak (container): 1; tables (PTF): 1; lua identical to vanilla: 0
- **Tables:** rpg_param (0 new rows, 1 changed, 0 identical to vanilla, 181 vanilla rows dropped by a whole-table replace); median relative change 1.0
- **Largest changes:** rpg_param:ShoeHealthDecrease rpg_param_value 0.001->0
- **Risk:** none

## 1578 Weighed Groschen - PTF Version (P2, Economy / merchants)

- **What the author says (Nexus summary):** Add a weight to the in game currency. - PTF Version!
- **File:** `Weiged Groschen - PTF Version-1578-1-9-5-1702120734.zip` (archive, 0.0 MB, `c_economy-merchants`), full (scratch, deleted after reading)
- **Grade:** C effective (few rows, strong effect) | **perceptibility:** high | **layers:** D1 data tables (PTF)
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `(none)`, loads on 1.9.8: yes (no version restriction)
- **Where it changes things:** manifest: 1; pak (container): 1; tables (PTF): 1; lua identical to vanilla: 0
- **Tables:** pickable_item (0 new rows, 1 changed, 0 identical to vanilla, 2209 vanilla rows dropped by a whole-table replace); median relative change 1.0
- **Largest changes:** pickable_item:5ef63059-322e-4e1b-abe8-926e100c770e weight 0->0.0005
- **Problems:** Data/WeighedGroschen.pak!Libs/Tables/item/pickable_item__weighedgroschen.xml: suffix 'weighedgroschen' != id 'weighed_groschen_ptf' (the game ignores it)
- **Risk:** none

## 1860 Train More Carry More - PTF (P2, Progression / XP / perks)

- **What the author says (Nexus summary):** Carry capacity scales with strength (x1.25 or x1.5) without changing the base carry weight; PTF. The suite's krs_qol carry value derives from it (permission requested) Increase the amount you can carry the more strength you have, this mod doesn't change the basic carry weight value so it should be c
- **File:** `Train More Carry More x10-1860-1-0-1739697344.zip` (archive, 0.0 MB, `c_progression-xp-perks`), full (scratch, deleted after reading)
- **Grade:** C effective (few rows, strong effect) | **perceptibility:** high | **layers:** D1 data tables (PTF)
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `(none)`, loads on 1.9.8: yes (no version restriction)
- **Where it changes things:** manifest: 1; pak (container): 1; tables (PTF): 1; lua identical to vanilla: 0
- **Tables:** rpg_param (1 new rows, 0 changed, 0 identical to vanilla, 182 vanilla rows dropped by a whole-table replace); median relative change 0.0
- **Largest changes:** rpg_param:StrengthToInventoryCapacity NEW row
- **Same rows as KRS:** krs_qol:rpg_param:StrengthToInventoryCapacity
- **Risk:** none

## 1938 My Herb Picking Radius (P2, Alchemy / food / survival)

- **What the author says (Nexus summary):** Double the herb picking radius.
- **File:** `Herb Picking Radius 2x-1938-1-0-1742117458.zip` (archive, 0.0 MB, `c_alchemy-food-survival`), full (scratch, deleted after reading)
- **Grade:** C effective (few rows, strong effect) | **perceptibility:** high | **layers:** D1 data tables (PTF)
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `1.*`, loads on 1.9.8: yes (wildcard)
- **Where it changes things:** manifest: 1; pak (container): 1; tables (PTF): 1; lua identical to vanilla: 0
- **Tables:** rpg_param (0 new rows, 1 changed, 0 identical to vanilla, 181 vanilla rows dropped by a whole-table replace); median relative change 1.0
- **Largest changes:** rpg_param:HerbGatherSkillToRadius rpg_param_value 0.25->0.5
- **Same rows as KRS:** krs_qol:rpg_param:HerbGatherSkillToRadius
- **Risk:** none

## 1671 Angriness Begone (P2, Combat / AI)

- **What the author says (Nexus summary):** Disables the angriness system, which informs NPCs that Henry is responsible for all unsolved crimes in the game world.
- **File:** `MagusAngrinessBegone-1671-Unknown-1718907026.7z` (archive, 0.0 MB, `c_combat-ai`), full (scratch, deleted after reading)
- **Grade:** D small tweak | **perceptibility:** medium | **layers:** D1 data tables (PTF)
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `(none)`, loads on 1.9.8: yes (no version restriction)
- **Where it changes things:** manifest: 1; pak (container): 1; tables (PTF): 1; lua identical to vanilla: 0
- **Tables:** angriness_enum (0 new rows, 7 changed, 0 identical to vanilla, 2 vanilla rows dropped by a whole-table replace); median relative change 1.0
- **Largest changes:** angriness_enum:2 value 0.55->0; angriness_enum:4 value 0.01->0; angriness_enum:5 value 0.15->0; angriness_enum:6 value 0.2->0; angriness_enum:7 value 0.025->0; angriness_enum:8 value 0.125->0; angriness_enum:9 value 0.1->0
- **Risk:** none

## 1693 Ravens beak and Spiked warhammer icon swap (P2, Weapons / armor / items)

- **What the author says (Nexus summary):** It only took 6 years for someone to make this mod
- **File:** `Ravens beak icon swap-1693-1-2-1733597371.7z` (archive, 0.0 MB, `c_weapons-armor-items`), full (scratch, deleted after reading)
- **Grade:** D small tweak | **perceptibility:** medium | **layers:** D1 data tables (PTF)
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `1.9.6`, loads on 1.9.8: NO (disabled: lists 1.9.6)
- **Where it changes things:** manifest: 1; pak (container): 1; tables (PTF): 1; lua identical to vanilla: 0
- **Tables:** player_item (0 new rows, 2 changed, 0 identical to vanilla, 2112 vanilla rows dropped by a whole-table replace); median relative change 0.0
- **Largest changes:** player_item:e16b0af6-fb6a-43e2-9a9c-1b8c227e64b8 icon_id 152->150; player_item:488d9792-0dbf-41dc-a320-753d94d1f1b6 icon_id 150->152
- **Risk:** none

## 1569 Karnages_Shield_Restoration (P2, Weapons / armor / items)

- **What the author says (Nexus summary):** Restores Shield Skill
- **File:** `Karnages_Shield_Restoration-1569-1-0-0-1700623905.7z` (archive, 0.0 MB, `c_weapons-armor-items`), full (scratch, deleted after reading)
- **Grade:** D small tweak | **perceptibility:** medium | **layers:** D1 data tables (PTF)
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `(none)`, loads on 1.9.8: yes (no version restriction)
- **Where it changes things:** manifest: 1; pak (container): 1; tables (PTF): 1; lua identical to vanilla: 0
- **Tables:** skill (0 new rows, 1 changed, 0 identical to vanilla, 32 vanilla rows dropped by a whole-table replace); median relative change 0.0
- **Largest changes:** skill:20 hidden True->False
- **Risk:** none

## 83 More Responsive Targeting (P2, Combat / AI)

- **What the author says (Nexus summary):** Loosens up the targeting system and makes it easier to move around in a fight and engage multiple opponents at once.
- **File:** `More Responsive Targeting-83-1-04-1.zip` (archive, 0.0 MB, `c_combat-ai`), full (scratch, deleted after reading)
- **Grade:** D small tweak | **perceptibility:** medium | **layers:** D2 engine config
- **How it installs:** unclear: read the archive's own instructions; manifest id `-`, supports `-`, loads on 1.9.8: no manifest (legacy install)
- **Where it changes things:** config (.cfg): 1; lua identical to vanilla: 0
- **Config:** 16 keys, e.g. wh_cs_playerhorizontalunlockdelay=0, wh_cs_playerinputcombatunlockdelay=0, wh_cs_playerinputcursorunlockdistance=0.05, wh_cs_playerinputlockareawidth=0.6, wh_cs_playerinputlockingtolerance=20, wh_cs_playerinputmouseunlockminoppangle=20, wh_cs_playerinputmouseunlockmintime=0, wh_cs_playerinputmouseunlockreturntime=1.5
- **Risk:** none

## 1040 Disable Combat Slowmotion (P2, Combat / AI)

- **What the author says (Nexus summary):** Disables the annoying Slowmotion that occurs during combat
- **File:** `DisableCombatSlowmotion.zip-1040-1-9-5-1592222070.zip` (archive, 0.0 MB, `c_combat-ai`), full (scratch, deleted after reading)
- **Grade:** D small tweak | **perceptibility:** none | **layers:** D3 Lua scripts
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `1.9.5`, loads on 1.9.8: NO (disabled: lists 1.9.5)
- **Where it changes things:** manifest: 1; pak (container): 1; scripts (Lua): 1; lua identical to vanilla: 0
- **Lua:** 1 files, 3 lines; API used: System.ExecuteCommandx2
- **Risk:** none

## 1518 Waystones Give XP (P2, Progression / XP / perks)

- **What the author says (Nexus summary):** Activating wayside shrines, conciliatory crosses, and images of saints in churches add 1 xp to reading if the object hasn't been discovered and/ or activated yet...
- **File:** `Wayshrine gives XP-1518-0-1-1689422764.7z` (archive, 0.0 MB, `c_progression-xp-perks`), full (scratch, deleted after reading)
- **Grade:** D small tweak | **perceptibility:** medium | **layers:** D3 Lua scripts
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `(none)`, loads on 1.9.8: yes (no version restriction)
- **Where it changes things:** manifest: 1; pak (container): 1; scripts (Lua): 1; lua identical to vanilla: 0
- **Lua:** 1 files, 67 lines; API used: Game.ShowCaptionObjectMessagex1, RPG.CaptionObjectUsedx1, RPG.NotifyLevelXpGainx1
- **Risk:** none

## 1519 Shooting Nests Gives XP (P2, Progression / XP / perks)

- **What the author says (Nexus summary):** Shooting nests will give XP on Archery(weapon_bow) if the nest hasn't dropped down yet...
- **File:** `Shooting Nests Gives XP-1519-0-1-1689446256.7z` (archive, 0.0 MB, `c_progression-xp-perks`), full (scratch, deleted after reading)
- **Grade:** D small tweak | **perceptibility:** high | **layers:** D3 Lua scripts
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `(none)`, loads on 1.9.8: yes (no version restriction)
- **Where it changes things:** manifest: 1; pak (container): 1; scripts (Lua): 1; lua identical to vanilla: 0
- **Lua:** 1 files, 179 lines; API used: Database.guidInventoryDBIdx3, Game.GetActionControlx1, player.soulx1, RPG.NotifyLevelXpGainx1
- **Risk:** none

## 1520 Shooting Archery Targets Gives XP (P2, Progression / XP / perks)

- **What the author says (Nexus summary):** Another one in my additional XP series of mods...
- **File:** `Targets give XP-1520-0-1-1689866187.7z` (archive, 0.0 MB, `c_progression-xp-perks`), full (scratch, deleted after reading)
- **Grade:** D small tweak | **perceptibility:** high | **layers:** D3 Lua scripts
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `(none)`, loads on 1.9.8: yes (no version restriction)
- **Where it changes things:** manifest: 1; pak (container): 1; scripts (Lua): 1; lua identical to vanilla: 0
- **Lua:** 1 files, 232 lines; API used: player.soulx1, RPG.NotifyLevelXpGainx1
- **Risk:** none

## 1612 Remove Auto Camera Lock In Combat (P2, Combat / AI)

- **What the author says (Nexus summary):** Are you tired of trying to play this game over and over, only to drop it because the combat is too frustrating? Look no further. This mod completely disables automatic camera locking in combat, but keeps manual locking, and even improves
- **File:** `RemoveAutoCameraLockInCombat-1612-1-0-0-1713519576.7z` (archive, 0.0 MB, `c_combat-ai`), full (scratch, deleted after reading)
- **Grade:** D small tweak | **perceptibility:** medium | **layers:** D2 engine config
- **How it installs:** unclear: read the archive's own instructions; manifest id `-`, supports `-`, loads on 1.9.8: no manifest (legacy install)
- **Where it changes things:** config (.cfg): 1; lua identical to vanilla: 0
- **Config:** 4 keys, e.g. wh_cs_playerinputcombatunlockdelay=0, wh_cs_playerinputcursorunlockdistance=300, wh_cs_playerinputlockareawidth=0, wh_cs_playerinputlockingtolerance=0
- **Risk:** none

## 1647 Slo Mo Begone (P2, Combat / AI)

- **What the author says (Nexus summary):** Disables slow motion for perfect blocks and dodges in combat completely.Experience the enhanced "combat flow" !
- **File:** `SloMoBegone-1647-1-0-0-1716234169.zip` (archive, 0.0 MB, `c_combat-ai`), full (scratch, deleted after reading)
- **Grade:** D small tweak | **perceptibility:** none | **layers:** D3 Lua scripts
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `(none)`, loads on 1.9.8: yes (no version restriction)
- **Where it changes things:** manifest: 1; pak (container): 1; scripts (Lua): 1; lua identical to vanilla: 0
- **Lua:** 1 files, 21 lines; API used: System.SetCVarx4, Game.ShowTutorialx1
- **Risk:** none

## 1655 Save Me Henry (P2, Progression / XP / perks)

- **What the author says (Nexus summary):** Adds new quality of life keybindings. Also changes the key layout from the controller setup to a user-friendly PC mouse and keyboard.
- **File:** `MagusSaveMeHenry-1655-Unknown-1720541841.7z` (archive, 0.01 MB, `c_progression-xp-perks`), full (scratch, deleted after reading)
- **Grade:** D small tweak | **perceptibility:** medium | **layers:** D3 Lua scripts
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `(none)`, loads on 1.9.8: yes (no version restriction)
- **Where it changes things:** other xml (data): 2; manifest: 1; pak (container): 1; scripts (Lua): 1; lua identical to vanilla: 0
- **Lua:** 1 files, 137 lines; API used: System.AddCCommandx24, System.ExecuteCommandx22, Game.SendInfoTextx6, Game.RemoveSaveLockx3, Game.IsLoadingEngineSaveGamex3, Game.SetWantedLevelx1
- **Risk:** none

## 2192 ENHANCED Toggle Aim Overhaul v2.0 KCD I (P2, Combat / AI)

- **What the author says (Nexus summary):** Tired of not being able to hit anyone with long-range weapons?Hans Capon laughing at you? I have a wonderful solution.
- **File:** `ENHANCED Toggle Aim Overhaul v2.0 KCD1 2192 2.0.1 2026-09-14T17-58Z sgZiUxTkd.zip` (archive, 0.0 MB, `c_combat-ai`), full (scratch, deleted after reading)
- **Grade:** D small tweak | **perceptibility:** medium | **layers:** D3 Lua scripts
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `aim`, supports `(none)`, loads on 1.9.8: yes (no version restriction)
- **Where it changes things:** config (.cfg): 1; manifest: 1; pak (container): 1; other xml (data): 1; scripts (Lua): 1; lua identical to vanilla: 0
- **Lua:** 1 files, 63 lines; API used: System.AddCCommandx5, System.SetCVarx3, System.ExecuteCommandx3
- **Risk:** none

## 2194 ENHANCED Easy FREE Combat Target Overhaul v3.0 KCD I (P2, Combat / AI)

- **What the author says (Nexus summary):** Now there is a free target in the game that doesn't stick to enemies, making it better flexible to control the battle. Full gamepad support is available.
- **File:** `ENHANCED Easy FREE Combat Target Overhaul KCD1-2194-1-1-1774268047.rar` (archive, 0.0 MB, `c_combat-ai`), full (scratch, deleted after reading)
- **Grade:** D small tweak | **perceptibility:** high | **layers:** D3 Lua scripts
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `eefct`, supports `(none)`, loads on 1.9.8: yes (no version restriction)
- **Where it changes things:** scripts (Lua): 2; config (.cfg): 1; manifest: 1; pak (container): 1; other xml (data): 1; lua identical to vanilla: 0
- **Lua:** 2 files, 158 lines; API used: System.ExecuteCommandx4, System.AddCCommandx3, System.LogAlwaysx2
- **Risk:** none

## 2372 Trough Washing Animation (P2, Alchemy / food / survival)

- **What the author says (Nexus summary):** Adds a Trough Washing animation just like in KCD2!
- **File:** `Trough Washing Animation 2372 1.0 2026-09-26T11-00Z U5RChtbw2.zip` (archive, 5.44 MB, `c_alchemy-food-survival`), full (scratch, deleted after reading)
- **Grade:** D small tweak | **perceptibility:** medium | **layers:** D0 content/text; D3 Lua scripts
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `(none)`, loads on 1.9.8: yes (no version restriction)
- **Where it changes things:** other: 16; models/animations/materials: 6; other xml (data): 3; textures: 3; manifest: 1; pak (container): 1; scripts (Lua): 1; lua identical to vanilla: 0
- **Lua:** 1 files, 30 lines; API used: Script.SetTimerx4, System.SetScreenFxx2
- **Risk:** none

## 366 First-person Herb Picking (P2, Alchemy / food / survival)

- **What the author says (Nexus summary):** Forces the game to stay in first-person-view when picking herbs.
- **File:** `First-person Herb Picking-366-1-9-5-1583164522.zip` (archive, 0.0 MB, `c_alchemy-food-survival`), full (scratch, deleted after reading)
- **Grade:** E non-perceptive to gameplay (content or text only) | **perceptibility:** low | **layers:** D0 content/text
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `(none)`, loads on 1.9.8: yes (no version restriction)
- **Where it changes things:** models/animations/materials: 2; manifest: 1; pak (container): 1; lua identical to vanilla: 0
- **Risk:** none

## 591 Bushes- Collision Remover (P2, World / weather / visuals)

- **What the author says (Nexus summary):** Removes collision from bushes (26 models); see check_1.9.8 in annotations Removes those annoying collision boxes on all bushes
- **File:** `Bushes.Only_Collision.Remover.pak` (loose file, 1.7 MB, `c_world-weather-visuals`), read in place
- **Grade:** E non-perceptive to gameplay (content or text only) | **perceptibility:** low | **layers:** D0 content/text
- **How it installs:** loose .pak (legacy: copy into Data); manifest id `-`, supports `-`, loads on 1.9.8: no manifest (legacy install)
- **Where it changes things:** models/animations/materials: 26; pak (container): 1; lua identical to vanilla: 0
- **Risk:** none

## 1090 Colored Arrows (P2, Archery / arrows)

- **What the author says (Nexus summary):** Adds colored stripes to the arrows and colors the feathers to make them easier to see in grass/ground. Optionally with plain feathers.
- **File:** `Colored Arrows and Feathers - White-1090-1-0-3-1599011013.zip` (archive, 1.1 MB, `c_archery-arrows`), full (scratch, deleted after reading)
- **Grade:** E non-perceptive to gameplay (content or text only) | **perceptibility:** low | **layers:** D0 content/text
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `1.9.*`, loads on 1.9.8: yes (wildcard)
- **Where it changes things:** textures: 11; manifest: 1; pak (container): 1; lua identical to vanilla: 0
- **Risk:** none

## 1205 ETSGF - Easy to see glowing Arrow feathers  - 1.9.6 - Multi-Colored arrow support (P2, Archery / arrows)

- **What the author says (Nexus summary):** An update of the old but loved ETSGF mod to work with the latest PTF update for KCD (1.9.6). Now has multi-colored arrow versions, thanks to Bluefirevortex!
- **File:** `ETSGF Multi-Color HiViz (Made by Bluefirevortex)-1205-1-0-1740342886.7z` (archive, 0.01 MB, `c_archery-arrows`), full (scratch, deleted after reading)
- **Grade:** E non-perceptive to gameplay (content or text only) | **perceptibility:** low | **layers:** D0 content/text
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `1.9.5 1.9.6 1.9.7`, loads on 1.9.8: NO (disabled: lists 1.9.5, 1.9.6, 1.9.7)
- **Where it changes things:** models/animations/materials: 10; manifest: 1; pak (container): 1; lua identical to vanilla: 0
- **Risk:** none

## 1205 ETSGF - Easy to see glowing Arrow feathers  - 1.9.6 - Multi-Colored arrow support (P2, Archery / arrows)

- **What the author says (Nexus summary):** An update of the old but loved ETSGF mod to work with the latest PTF update for KCD (1.9.6). Now has multi-colored arrow versions, thanks to Bluefirevortex!
- **File:** `ETSGF Multi-Color LowViz (Made by Bluefirevortex)-1205-1-0-1740343056.7z` (archive, 0.01 MB, `c_archery-arrows`), full (scratch, deleted after reading)
- **Grade:** E non-perceptive to gameplay (content or text only) | **perceptibility:** low | **layers:** D0 content/text
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `1.9.5 1.9.6 1.9.7`, loads on 1.9.8: NO (disabled: lists 1.9.5, 1.9.6, 1.9.7)
- **Where it changes things:** models/animations/materials: 10; manifest: 1; pak (container): 1; textures: 1; lua identical to vanilla: 0
- **Risk:** none

## 1323 Skalitz Shield Fix AWL (P2, Weapons / armor / items)

- **What the author says (Nexus summary):** Fixed a issue with the Skalitz Shield you get from Theresa after finishing her part in A Woman's Lot.
- **File:** `Skalitz Shield Fix-1323-1-0-1642601960.7z` (archive, 6.16 MB, `c_weapons-armor-items`), full (scratch, deleted after reading)
- **Grade:** E non-perceptive to gameplay (content or text only) | **perceptibility:** low | **layers:** D0 content/text
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `1.9.*`, loads on 1.9.8: yes (wildcard)
- **Where it changes things:** textures: 6; manifest: 1; docs: 1; pak (container): 1; models/animations/materials: 1; lua identical to vanilla: 0
- **Risk:** none

## 1922 No Prefixes in Alchemy Book (P2, Alchemy / food / survival)

- **What the author says (Nexus summary):** Removes sorting mod prefixes from the alchemy book.
- **File:** `No Prefixes in Alchemy Book-1922-1-0-1-1741961065.zip` (archive, 0.03 MB, `c_alchemy-food-survival`), full (scratch, deleted after reading)
- **Grade:** E non-perceptive to gameplay (content or text only) | **perceptibility:** low | **layers:** D0 content/text
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `(none)`, loads on 1.9.8: yes (no version restriction)
- **Where it changes things:** localization: 28; manifest: 1; pak (container): 1; ui: 1; lua identical to vanilla: 0
- **Text:** 0 strings changed, 378 new
- **Risk:** none

## 1991 BCAIC - Restore Hunting Spots - Patch (P2, Alchemy / food / survival)

- **What the author says (Nexus summary):** BCAIC is must have mod for every run. This tiny patch restores hunting spot markers for the map.
- **File:** `BCAIC - Restore Hunting Spot Icons - Patch-1991-1-0-1745002325.zip` (archive, 0.02 MB, `c_alchemy-food-survival`), full (scratch, deleted after reading)
- **Grade:** E non-perceptive to gameplay (content or text only) | **perceptibility:** low | **layers:** D0 content/text
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `1.9.6`, loads on 1.9.8: NO (disabled: lists 1.9.6)
- **Where it changes things:** ui: 4; textures: 2; manifest: 1; pak (container): 1; lua identical to vanilla: 0
- **Risk:** none

## 2040 Polymorphic Projectiles Arrow Overhaul (P2, Archery / arrows)

- **What the author says (Nexus summary):** Complete++ arrow overhaul. Killing Cumans with a watermelon is now on your bucket list
- **File:** `Polymorphic Fire Arrow-2040-2-1774384773.7z` (archive, 0.0 MB, `c_archery-arrows`), full (scratch, deleted after reading)
- **Grade:** E non-perceptive to gameplay (content or text only) | **perceptibility:** low | **layers:** D0 content/text
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `dddb_polymorph`, supports `*`, loads on 1.9.8: NO (disabled: lists *)
- **Where it changes things:** localization: 3; manifest: 1; docs: 1; pak (container): 1; other xml (data): 1; lua identical to vanilla: 0
- **Text:** 11 strings changed, 0 new
- **Risk:** none

## 2098 Medieval Poisons - spolszczenie (P2, Alchemy / food / survival)

- **What the author says (Nexus summary):** Polish translation of Medieval Poisons (TyburnKetch) Pełne spolszczenie do moda Tyburn's Medieval Poisons. Tłumaczenie obejmuje wszystkie nowe trucizny (m.in. arszenik, mandragora, szczwół), receptury, składniki oraz księgę "Liber de Venenis". Zachowano zgodność z polskim nazewnictwem w grze.
- **File:** `spolszczenie do moda Tyburn's Medieval Poisons-2098-1-0-1763383230.rar` (archive, 0.01 MB, `c_alchemy-food-survival`), full (scratch, deleted after reading)
- **Grade:** E non-perceptive to gameplay (content or text only) | **perceptibility:** low | **layers:** D0 content/text
- **How it installs:** loose .pak (legacy: copy into Data); manifest id `-`, supports `-`, loads on 1.9.8: no manifest (legacy install)
- **Where it changes things:** localization: 2; lua identical to vanilla: 0
- **Text:** 40 strings changed, 135 new
- **Risk:** none

## 2207 Findable Herbs HD (P2, Alchemy / food / survival)

- **What the author says (Nexus summary):** Makes hard to find herbs less hard to find by changing their visuals.
- **File:** `Findable Herbs HD-2207-1-0-1776182143.7z` (archive, 10.03 MB, `c_alchemy-food-survival`), full (scratch, deleted after reading)
- **Grade:** E non-perceptive to gameplay (content or text only) | **perceptibility:** low | **layers:** D0 content/text
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `(none)`, loads on 1.9.8: yes (no version restriction)
- **Where it changes things:** manifest: 1; pak (container): 1; textures: 1; lua identical to vanilla: 0
- **Risk:** none

## 2276 Instant Herb and faster Alchemy Merger (P2, Alchemy / food / survival)

- **What the author says (Nexus summary):** Mods that change animations usually conflict in KCD. This is T0rvadaL's instant herb picking with faster alchemy animations thrown in by me.
- **File:** `Instant Herb Picking Merged 4x version 2276 1 2026-07-01T21-38Z 9pAt2OHcY.zip` (archive, 0.2 MB, `c_alchemy-food-survival`), full (scratch, deleted after reading)
- **Grade:** E non-perceptive to gameplay (content or text only) | **perceptibility:** low | **layers:** D0 content/text
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `(none)`, loads on 1.9.8: yes (no version restriction)
- **Where it changes things:** models/animations/materials: 4; manifest: 1; pak (container): 1; lua identical to vanilla: 0
- **Risk:** none

## 2331 Bushes Collision Remover Redux (P2, World / weather / visuals)

- **What the author says (Nexus summary):** A clean, modern rebuild of JovianStone's original Bushes - Collision Remover for Kingdom Come: Deliverance.
- **File:** `Bushes Collision Remover Redux 2331 1 2026-08-12T06-14Z 4yvkqUP3B.zip` (archive, 1.67 MB, `c_world-weather-visuals`), full (scratch, deleted after reading)
- **Grade:** E non-perceptive to gameplay (content or text only) | **perceptibility:** low | **layers:** D0 content/text
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `bushes_collision_remover_redux`, supports `(none)`, loads on 1.9.8: yes (no version restriction)
- **Where it changes things:** models/animations/materials: 26; manifest: 1; docs: 1; pak (container): 1; lua identical to vanilla: 0
- **Mentions:** states requirements
- **Risk:** none

## 2362 Better Perk Descriptions (P2, Progression / XP / perks)

- **What the author says (Nexus summary):** Changes the perk descriptions to include precise information about the perk. Finally you can make informed choices!
- **File:** `Better Perk Descriptions 2362 1.0 2026-09-13T23-47Z pA6IjrM9q.zip` (archive, 0.04 MB, `c_progression-xp-perks`), full (scratch, deleted after reading)
- **Grade:** E non-perceptive to gameplay (content or text only) | **perceptibility:** low | **layers:** D0 content/text
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `1.*`, loads on 1.9.8: yes (wildcard)
- **Where it changes things:** localization: 2; manifest: 1; lua identical to vanilla: 0
- **Text:** 26 strings changed, 0 new
- **Risk:** none

## 84 Archery - Realistic Arrow Flight (P2, Archery / arrows)

- **What the author says (Nexus summary):** This is a revision of PcFreaky99's Faster Arrows.  I'd like to thank him for his work and saving me the time to find the files myself.I have used his mod and re-calibrated the numbers so that the arrow flight is a bit more realistic.   It's
- **File:** `Near Perfect Arrows.-84-69-69.zip` (archive, 0.0 MB, `c_archery-arrows`), full (scratch, deleted after reading)
- **Grade:** E non-perceptive to gameplay (no effective change found) | **perceptibility:** none | **layers:** none found
- **How it installs:** loose .pak (legacy: copy into Data); manifest id `-`, supports `-`, loads on 1.9.8: no manifest (legacy install)
- **Where it changes things:** pak (container): 1; other xml (data): 1; lua identical to vanilla: 0
- **Risk:** none

## 1652 Catches the Worm (P2, Alchemy / food / survival)

- **What the author says (Nexus summary):** All NPCs have a revised daily routine. They no longer sleep half the day. All immortal NPCs are now also mortal. (There are a handful of scripted NPCs that cannot have their immortality removed.)
- **File:** `catche the worm-1652-1-0-1716593673.zip` (archive, 0.78 MB, `c_alchemy-food-survival`), full (scratch, deleted after reading)
- **Grade:** E non-perceptive to gameplay (no effective change found) | **perceptibility:** none | **layers:** none found
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `(none)`, loads on 1.9.8: yes (no version restriction)
- **Where it changes things:** manifest: 1; pak (container): 1; tables (PTF): 1; lua identical to vanilla: 0
- **Problems:** catches_the_worm/Data/catchestheworm.pak!Libs/Tables/rpg/soul__catchestheworm.xml: not a readable table
- **Risk:** none

## 1673 Combat musics tweak (P2, Combat / AI)

- **What the author says (Nexus summary):** A mod that tweak the combat musics as best as possibleNot compatible with other musics mod that use the layer !
- **File:** `Combat music A Stressfull version-1673-1-0-1718966803.zip` (archive, 0.1 MB, `c_combat-ai`), full (scratch, deleted after reading)
- **Grade:** E non-perceptive to gameplay (no effective change found) | **perceptibility:** none | **layers:** none found
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `(none)`, loads on 1.9.8: yes (no version restriction)
- **Where it changes things:** other: 2; manifest: 1; pak (container): 1; lua identical to vanilla: 0
- **Risk:** none

## 1673 Combat musics tweak (P2, Combat / AI)

- **What the author says (Nexus summary):** A mod that tweak the combat musics as best as possibleNot compatible with other musics mod that use the layer !
- **File:** `Combat music A and Unreleased one-1673-1-0-1718968202.zip` (archive, 0.1 MB, `c_combat-ai`), full (scratch, deleted after reading)
- **Grade:** E non-perceptive to gameplay (no effective change found) | **perceptibility:** none | **layers:** none found
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `(none)`, loads on 1.9.8: yes (no version restriction)
- **Where it changes things:** other: 2; manifest: 1; pak (container): 1; lua identical to vanilla: 0
- **Risk:** none

## 1743 Persistent Arrows (P2, Archery / arrows)

- **What the author says (Nexus summary):** your arrows will stay firmly fixed on the exact location where you hit the npc bodies.
- **File:** `Persistentarrows-1743-1-2-1729568337.rar` (archive, 0.0 MB, `c_archery-arrows`), full (scratch, deleted after reading)
- **Grade:** E non-perceptive to gameplay (no effective change found) | **perceptibility:** none | **layers:** none found
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `1.9.*`, loads on 1.9.8: yes (wildcard)
- **Where it changes things:** manifest: 1; pak (container): 1; other xml (data): 1; lua identical to vanilla: 0
- **Risk:** none

## 1951 Baths dont affect energy and nourishment (P2, Alchemy / food / survival)

- **What the author says (Nexus summary):** Bathmaids don't feed and caffeinate you! Optional: slower energy increase
- **File:** `energy increased as if rested-1951-1-0-0-1742338696.7z` (archive, 0.02 MB, `c_alchemy-food-survival`), full (scratch, deleted after reading)
- **Grade:** E non-perceptive to gameplay (no effective change found) | **perceptibility:** none | **layers:** none found
- **How it installs:** loose .pak (legacy: copy into Data); manifest id `-`, supports `-`, loads on 1.9.8: no manifest (legacy install)
- **Where it changes things:** pak (container): 1; other xml (data): 1; lua identical to vanilla: 0
- **Risk:** none

## 1996 Alcohol Is Not Food Anymore (P2, Alchemy / food / survival)

- **What the author says (Nexus summary):** Exactly as the title says Alcohol Is Not Food Anymore.
- **File:** `Alcohol Is Not Food Anymore-1996-1-0-1745154676.zip` (archive, 0.0 MB, `c_alchemy-food-survival`), full (scratch, deleted after reading)
- **Grade:** E non-perceptive to gameplay (no effective change found) | **perceptibility:** none | **layers:** D1 data tables (PTF)
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `(none)`, loads on 1.9.8: yes (no version restriction)
- **Where it changes things:** manifest: 1; pak (container): 1; tables (PTF): 1; lua identical to vanilla: 0
- **Risk:** none

## 2066 Distant Smoke and Fire (P2, World / weather / visuals)

- **What the author says (Nexus summary):** Increases smoke and fire draw distance for chimneys, campfires, and torches.
- **File:** `DistantFireAndSmoke-2066-0-2-1755855018.zip` (archive, 0.02 MB, `c_world-weather-visuals`), full (scratch, deleted after reading)
- **Grade:** E non-perceptive to gameplay (no effective change found) | **perceptibility:** none | **layers:** none found
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `(none)`, loads on 1.9.8: yes (no version restriction)
- **Where it changes things:** manifest: 1; pak (container): 1; other xml (data): 1; lua identical to vanilla: 0
- **Risk:** none

## 2280 Remove Artemisia (Wormwood) Potion Visual Effect Overlay (P2, Alchemy / food / survival)

- **What the author says (Nexus summary):** The mod completely removes the blueish greenish visual effect from your screen when you drink Artemisia (Wormwood) potion.
- **File:** `No Wormwood Artemisia Potion Effect 2280 1 2026-07-05T17-40Z GK8rEaX2G.zip` (archive, 0.0 MB, `c_alchemy-food-survival`), full (scratch, deleted after reading)
- **Grade:** E non-perceptive to gameplay (no effective change found) | **perceptibility:** none | **layers:** none found
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `(none)`, loads on 1.9.8: yes (no version restriction)
- **Where it changes things:** manifest: 1; pak (container): 1; other xml (data): 1; lua identical to vanilla: 0
- **Risk:** none

## 2332 Baptism of Fire Fix Redux (P2, Quests / lore / content)

- **What the author says (Nexus summary):** A targeted Redux fix for the long-standing false "Too many of your men have died" failure during Baptism of Fire.
- **File:** `Baptism Of Fire Fix Redux 2332 1.0.0 2026-08-12T09-22Z q1JwghIHz.zip` (archive, 0.04 MB, `c_quests-lore-content`), full (scratch, deleted after reading)
- **Grade:** E non-perceptive to gameplay (no effective change found) | **perceptibility:** none | **layers:** none found
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `baptism_of_fire_fix_redux`, supports `(none)`, loads on 1.9.8: yes (no version restriction)
- **Where it changes things:** manifest: 1; docs: 1; pak (container): 1; other xml (data): 1; lua identical to vanilla: 0
- **Risk:** none

## 2381 Nest of Vipers Stealth (P2, Crime / stealth / loot)

- **What the author says (Nexus summary):** No more omniscient guards in Nest of Vipers! You can actually sabotage the food pots and arrow barrels without getting automatically caught- if you have the stealth skills to do so!
- **File:** `NestOfVipersStealth 2381 1 2026-10-01T03-43Z 2jGTl3QNE.zip` (archive, 0.05 MB, `c_crime-stealth-loot`), full (scratch, deleted after reading)
- **Grade:** E non-perceptive to gameplay (no effective change found) | **perceptibility:** none | **layers:** none found
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `(none)`, loads on 1.9.8: yes (no version restriction)
- **Where it changes things:** other xml (data): 2; manifest: 1; docs: 1; pak (container): 1; lua identical to vanilla: 0
- **Mentions:** Vortex
- **Risk:** none

## 311 O' Hungry Henry (P2, Alchemy / food / survival)

- **What the author says (Nexus summary):** More realistic needs pertaining to eating and sleeping. Increased Hunger and Fatigue requiring you to very carefully chose what to eat and you will have to keep an eye on your tiredness. Also changes energy gained from sleeping per hour,
- **File:** `5.5-6 Nourishment and 4 Energy lost per hour-311-1-0.7z` (archive, 0.0 MB, `c_alchemy-food-survival`), full (scratch, deleted after reading)
- **Grade:** X not analysed | **perceptibility:** unknown | **layers:** none found
- **How it installs:** loose .pak (legacy: copy into Data); manifest id `-`, supports `-`, loads on 1.9.8: no manifest (legacy install)
- **Where it changes things:** docs: 1; pak (container): 1; lua identical to vanilla: 0
- **Problems:** zzz_OHungryHenry.pak: not a ZIP (the game cannot read it either)
- **Risk:** none

## 2017 Realistic Items (P1, Weapons / armor / items)

- **What the author says (Nexus summary):** All items modifications made for the Kingdom Refinement Suite Collection.
- **File:** `KRS-Items-2017-1-0-0-1749069665.7z` (archive, 0.0 MB, `c_weapons-armor-items`), full (scratch, deleted after reading)
- **Grade:** X not analysed | **perceptibility:** unknown | **layers:** none found
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `krs_items`, supports `1.9.x`, loads on 1.9.8: NO (disabled: lists 1.9.x)
- **Where it changes things:** manifest: 1; pak (container): 1; lua identical to vanilla: 0
- **Problems:** KRS-Items/Data/krs-items.pak: not a ZIP (the game cannot read it either)
- **Risk:** none

## 2017 Realistic Items (P1, Weapons / armor / items)

- **What the author says (Nexus summary):** All items modifications made for the Kingdom Refinement Suite Collection.
- **File:** `KRS-Items-2017-1-1-1-1749401836.7z` (archive, 0.0 MB, `c_weapons-armor-items`), full (scratch, deleted after reading)
- **Grade:** X not analysed | **perceptibility:** unknown | **layers:** none found
- **How it installs:** loose .pak (legacy: copy into Data); manifest id `-`, supports `-`, loads on 1.9.8: no manifest (legacy install)
- **Where it changes things:** pak (container): 1; lua identical to vanilla: 0
- **Problems:** KRS-Items/Data/KRS-Items.pak: not a ZIP (the game cannot read it either)
- **Risk:** none
