# Mod analysis: what the P1/P2 mods change (generated)

> **GENERATED** by `tools/audit_mods_deep.py`: do not edit | **Kind:** review | **Trust:** archives read statically (listed, extracted to a scratch folder, read, deleted); nothing was installed or run | **Game version:** 1.9.8

Read on 2026-10-04: **138 archives, folders and loose files of 131 mods** (all P1/P2 mods that are in the downloads folder). Method: each archive is listed with 7-Zip (nothing extracted yet) and judged for risk; the safe ones are extracted to a scratch folder, read with Python (file names, magic bytes, XML tables compared with the vanilla `Tables.pak`, Lua and config text), and the scratch folder is deleted. No file was executed, installed or loaded by the game; no game run was made. Per-mod detail: [`MOD_PROFILES.md`](MOD_PROFILES.md); tables: `mod_analysis.csv`, `mod_tables.csv`, `mod_overlap.csv`, `risk_scan.csv`.

## Risk result

| Level | Archives |
|---|---|
| HIGH | 6 |
| MEDIUM | 4 |
| LOW | 0 |
| none | 128 |

HIGH means native code, scripts or shortcuts, dangerous Lua calls, path traversal or encrypted entries: those archives were moved to `_quarantine/` (6 moved). Details and how to restore them: [`QUARANTINE.md`](QUARANTINE.md).

## How the mods are graded

Each mod gets a **grade** (how much it changes the game), a **perceptibility** (would a player notice) and the **depth** of the change.

| Grade | Rule |
|---|---|
| A changes the most | native code or an external tool, or 400+ rows, or 15+ tables, or 3000+ lines of Lua |
| B large | 100+ rows, or 6+ tables, or 600+ lines of Lua |
| C effective (few rows, strong effect) | 1 to 39 rows, but at least one core-gameplay row changes by 20 % or more (or 30+ rows / 150+ lines of Lua reach 'high' perceptibility) |
| D small tweak | some rows, config keys or script lines, none of them a large change in a core table |
| E visual, audio or UI only (no gameplay change) | textures, models, ReShade/ENB presets, audio, UI or graphics config (r_, e_, sys_ cvars) only; no data row or script changes. Not imperceptible: see the visual impact column |
| E text only (no gameplay change) | only changed or new text strings |
| E non-perceptive to gameplay (no effective change found) | nothing found that changes the game (empty, no-op rows, or unreadable pak) |
| X not analysed | nothing readable (damaged, encrypted, not a ZIP, or refused by the safety judgement) |

Perceptibility: **high** = a core gameplay row (rpg_param, perk, skill, buff, weapon, item, food, ...) changes by 20 % or more, or 30+ rows, or 150+ Lua lines; **medium** = 5+ rows, 3+ config keys, 30+ Lua lines or any core row; **low** = few rows, or only assets or text; **none** = nothing.

Depth layers: D0 content or text, D1 data tables (PTF), D2 engine config (.cfg), D3 Lua scripts, D4 native code or an external tool. "Relative change" is |new - old| / |old| of a changed numeric cell against the vanilla value (a new row counts as 1.0, capped at 10).

## Result

| Grade | Archives | Mods |
|---|---|---|
| A changes the most | 23 | 23 |
| B large | 22 | 21 |
| C effective (few rows, strong effect) | 53 | 51 |
| D small tweak | 22 | 22 |
| E visual, audio or UI only (no gameplay change) | 11 | 10 |
| E text only (no gameplay change) | 2 | 2 |
| E non-perceptive to gameplay (no effective change found) | 2 | 1 |
| X not analysed | 3 | 2 |

Loads on 1.9.8 by the manifest rule (docs/engine/game-versions.md): yes 101, NO 24, no manifest (legacy install) 13.

How the mods install: 125 x Mods/<mod folder> with mod.manifest (Vortex or manual); 10 x loose .pak (legacy: copy into Data); 3 x unclear: read the archive's own instructions.

Layout problems found (each makes the mod do nothing or something other than intended): table files without a suffix, in total: 434; archives with table files without a suffix (they replace whole vanilla tables): 14; patch files outside Libs/Tables, in total: 6; archives whose pak is not a ZIP (not readable by the game): 3; archives with patch files outside Libs/Tables (never loaded): 1.

## A changes the most (23)

| Id | Mod | Domain | Rows (new / changed) | Tables | Median rel. | Gameplay / visual | Highlights | Risk |
|---|---|---|---|---|---|---|---|---|
| 2124 | Half-looted Rebalance | gameplay data, scripts, other game data (xml), | 17704 / 4915 | 57 | 0.8 | high / medium | shop_type2item:7899825d-ed6f-4f00-b698-649ba652cf6d amount 5->58; shop_type2item:907a2cd5-2730-424e-bf11-ef1f2db8f7e1 amount 2->25 | none |
| 883 | KingdomCome Rebalancing | gameplay data, other game data (xml), UI, text | 22 / 16851 | 20 | 0.4 | high / medium | equippable_item:41382adf-569c-4f33-90a0-36b6e874eca7 rpg_buff_weight 0.05->0.525; weapon:d459cb3a-04b5-4de7-b115-35ec17d293ba max_status 10->82 | none |
| 2299 | 1403 - Historical Rebalance | gameplay data, scripts, other game data (xml), | 1195 / 7323 | 33 | 1.0 | high / low | armor:00000000-0000-0000-0000-000000000020 slash_def 0.1->3; armor:0082de35-b635-4b85-a9ec-95024713f3ab slash_def 2->36 | none |
| 2294 | Faster Combat - Directional Master Strikes - Bet | gameplay data, other game data (xml), engine c | 787 / 2198 | 55 | 0.091 | high / high | weapon_class:/1//3/0/5/0/24/12/0 hunt_attack_distance 1.9->-1; weapon_class:/1//3/0/5/0/24/12/0 hunt_attack_distance 1.9->-1 | none |
| 1652 | Catches the Worm | gameplay data | 147 / 2329 | 1 | 0.0 | high / none | soul:00000000-0000-0000-0000-000000035000/2a7b75cd-8344-43f6-8483-0191a079e503//9fe6dae0-e195-42e0-a3fb-66cfc6382407/4b61cecf-a191-72ce-01bf-36ce711ea | none |
| 1629 | Exclusive Master Strikes - Make Them Reasonable | gameplay data, text | 2423 / 1 | 2 | 1.0 | high / low | perk:61e91997-9b32-123b-ad05-8691afdb81be NEW row; perk:1627a1b6-64c5-422f-ac2d-3a6abc071690 visibility 0->1 | none |
| 2049 | Simple Ragdoll Physics | gameplay data, scripts, other game data (xml), | 2 / 1657 | 11 | 0.62 | high / high | pickable_item:7db6b854-e307-4a47-ba39-943190b2469e price 1->38; pickable_item:c49aa63a-07a6-4417-9f9b-97f2712a4cd0 weight 0.1->0.7 | MEDIUM |
| 2340 | MatthusTweaks - Equipment and Progression Overha | gameplay data | 11 / 1621 | 12 | 0.559 | high / none | armor:4fec3673-04fe-45ae-b200-600704ecea70 slash_def 0.1->1.25; pickable_item:413806e7-f3b7-c6cf-2309-e47ce3c97fa2 price 220->5220 | none |
| 1560 | Karnages_Durability_Redux | gameplay data | 0 / 964 | 2 | 9.0 | high / none | weapon:00000000-0000-0000-0000-000000000005 max_status 1->10; weapon:01b86c1e-1614-4310-8bed-10b7682e5815 max_status 25->250 | none |
| 1148 | Combo and Weapon rebalance | gameplay data | 0 / 674 | 2 | 4.377 | high / none | combat_sync_action_hit:1/39 attack_value_coef 0.1->2.605583991837097; combat_sync_action_hit:27/44 attack_value_coef 0.2->2.706255285624903 | none |
| 2219 | True Hardcore Crime (PTF) | gameplay data, scripts, text | 29 / 515 | 8 | 10.0 | high / low | pickable_item:009e075b-16e2-4666-8f46-e05670783fb9 owner_fading_coef 0.02->1; pickable_item:00d32ef9-77b8-4eb0-b767-388c18e60343 owner_fading_coef 0.0 | none |
| 2188 | True Hardcore Economy (PTF) | gameplay data, scripts, text | 62 / 394 | 12 | 0.688 | high / low | inventory2item:5ef63059-322e-4e1b-abe8-926e100c770e amount 340->1800; inventory2item:5ef63059-322e-4e1b-abe8-926e100c770e amount_random_add 30->150 | none |
| 651 | Better Combat and Immersion Compilation | gameplay data, scripts, other game data (xml), | 136 / 308 | 15 | 0.571 | high / high | buff:6741cdd0-837a-4b5c-bad8-fb32f389509d duration 60->1800; buff:7690a860-a843-4609-8a67-9868b87b32b5 duration 300->9000 | none |
| 2210 | True Hardcore Alchemy (PTF) | gameplay data, scripts, text | 8 / 214 | 5 | 0.8 | high / low | pickable_item:eec58bfb-063e-4838-b78d-3c2b354f1346 price 1->100; buff:25bdbc39-c19a-4a11-8c0f-6e16c432846f duration 600->14400 | none |
| 1563 | Karnages_Polearm_Restoration 2.0 | gameplay data, scripts, other game data (xml), | 164 / 47 | 28 | 0.206 | high / high | weapon:405c1865-413d-43b8-8db9-c44a0eefd350 max_status 15->500; weapon:49fa5ec9-92a9-4bfb-b56e-a33d04b69ee1 max_status 25->500 | none |
| 1736 | Rogue Life | gameplay data, scripts, other game data (xml), | 53 / 16 | 22 | 2.0 | high / low | buff:f699eef9-c4fd-48b5-8793-3a3c16374729 NEW row; buff:c145ad4e-24c0-48de-b15e-123bab6838c4 NEW row | none |
| 2208 | Medieval Poisons - True Hardcore Compatibility P | gameplay data, scripts, text | 28 / 13 | 6 | 0.7 | high / low | buff:25bdbc39-c19a-4a11-8c0f-6e16c432846f duration 600->14400; buff:db397470-27c5-4a3a-9717-1b3b5f42377a duration 600->43200 | none |
| 1839 | Realistic Horses | gameplay data, scripts | 1 / 26 | 4 | 0.7 | high / none | equippable_item:41382adf-569c-4f33-90a0-36b6e874eca7 rpg_buff_weight 0.05->0.4; equippable_item:475642da-17e6-c06e-b035-2b1ab31cbb8f rpg_buff_weight 0 | HIGH |
| 2338 | Horse Collision Mod | gameplay data, scripts, other game data (xml), | 11 / 0 | 4 | 0.0 | high / high | buff:a8d30cd4-d7ae-4b58-a726-d94a875c50e8 NEW row; buff:488afdee-b2bb-4d94-8357-d923f40d65ef NEW row | none |
| 2246 | Console Editable RpgParams | native/external | 0 / 0 | 0 | 0.0 | none / none | executables/scripts: 1; other: 1; lua identical to vanilla: 0 | HIGH |
| 2326 | Permanent Death | scripts, other game data (xml), text, native/e | 0 / 0 | 0 | 0.0 | high / low | localization: 4; executables/scripts: 3; other game data (xml, not table rows): 2; docs: 1; manifest: 1; pak (container): 1; scripts (Lua): 1; lua ide | HIGH |
| 2348 | KCD Zero Durability Repair | native/external | 0 / 0 | 0 | 0.0 | none / none | executables/scripts: 1; manifest: 1; other: 1; lua identical to vanilla: 0 | HIGH |
| 2359 | KCD Kombat Tune | native/external | 0 / 0 | 0 | 0.0 | none / none | executables/scripts: 2; other: 2; manifest: 1; lua identical to vanilla: 0 | HIGH |

## B large (22)

| Id | Mod | Domain | Rows (new / changed) | Tables | Median rel. | Gameplay / visual | Highlights | Risk |
|---|---|---|---|---|---|---|---|---|
| 1483 | TSM Slower Food Spoil | gameplay data | 0 / 333 | 3 | 2.0 | high / none | food:025f546b-7465-4070-a57d-e84852adc184 decay_time_hours 120->600; food:0368a199-117e-4079-b182-b042360c7d61 decay_time_hours 120->600 | none |
| 2011 | Chefs Kiss | gameplay data, text | 56 / 267 | 7 | 1.0 | high / low | food:22eb16a0-1175-4e2e-a951-33d362e288fb max_status 2->200; food:28a7c5cd-d80d-4167-ba1b-fcfc520c40b7 max_status 1->44 | none |
| 85 | Perkaholic | gameplay data, other game data (xml), text | 188 / 86 | 6 | 0.4 | high / low | buff:8190c0af-e298-4a4c-b0d4-5c1572ca53c2 NEW row; buff:44d83d20-9709-4e54-9b7d-9b6bcfb630be NEW row | none |
| 1112 | Combat Overhaul | gameplay data | 226 / 17 | 5 | 0.54 | high / none | combat_action_perfect_block:14/1/1/CombatBlockPerfect/4/1/0/3/-1/0/4/7/4/-1/1/-1/-1/-1/-1/-1/4/-1/1 NEW row; combat_action_perfect_block:14/1/0/Combat | none |
| 2179 | True Hardcore Combat (PTF) | gameplay data, text | 72 / 148 | 11 | 0.4 | high / low | rpg_param:SkillToDefense rpg_param_value 0.02857->0.2857; food:3157d51d-7461-4fdc-9601-93bd5ed42156 refresh_benefit 4->-3 | none |
| 1009 | Perkaholic - PTF updated (1.9.4-1.9.8) | gameplay data, text | 187 / 7 | 6 | 0.25 | high / low | buff:44d83d20-9709-4e54-9b7d-9b6bcfb630be NEW row; buff:44d83d21-9709-4e54-9b7d-9b6bcfb630be NEW row | MEDIUM |
| 1009 | Perkaholic - PTF updated (1.9.4-1.9.8) | gameplay data, text | 187 / 7 | 6 | 0.25 | high / low | buff:44d83d20-9709-4e54-9b7d-9b6bcfb630be NEW row; buff:44d83d21-9709-4e54-9b7d-9b6bcfb630be NEW row | none |
| 770 | Perkaholic updated | gameplay data, text | 184 / 2 | 4 | 0.25 | high / low | perk_buff_override:010b08d9-5346-402c-a7cb-a084d624b62e/44d83d28-9709-4e54-9b7d-9b6bcfb630be/44d83d29-9709-4e54-9b7d-9b6bcfb630be NEW row; perk_buff_o | HIGH |
| 1384 | Modified Combat Overhaul - Directional Combat an | gameplay data | 160 / 21 | 4 | 0.455 | high / none | rpg_param:CombatAutoDodgeWeight rpg_param_value 1.1->4; rpg_param:SkillToDmgConstA rpg_param_value 250->700 | none |
| 1558 | Karnages_KCD_Essential_Fixes 2.0 | gameplay data | 26 / 129 | 3 | 1.0 | high / none | perk_rpg_param_override:01c3b32a-5751-4c98-b6ab-258d02370382/RepairKitCapacity rpg_param_value 450->8000; rpg_param:HorseRidingXPPerDistance rpg_param | none |
| 2345 | Food and Drinks rebalance | gameplay data | 0 / 155 | 1 | 0.5 | high / none | food:7beb4bdc-6478-455c-8746-afb92c604be8 refresh_benefit 1->-3; food:1d8ffd19-af12-4bd7-8afd-43b9b0348ade nutrition_benefit 4->18 | none |
| 1639 | Alternate Food Spoil (2X) | gameplay data | 0 / 111 | 1 | 1.0 | high / none | food:18ff9093-2cc4-4ab3-9f34-7cb0dd7cd30a decay_time_hours 24->2400; food:025f546b-7465-4070-a57d-e84852adc184 decay_time_hours 120->240 | none |
| 2045 | Polearms Unleashed Rebalanced Lite Edition PTF | gameplay data, scripts, other game data (xml), | 64 / 42 | 12 | 0.25 | high / high | pickable_item:8ef902ea-0c32-44c9-b101-71f35b9cbe3d price 1570->13800; pickable_item:44940b6c-f1f9-4ad1-9419-b5705a88e5b0 price 810->6000 | none |
| 1380 | Black Items Fix | gameplay data, textures/models/animations, tex | 54 / 5 | 8 | 0.0 | high / high | armor:d640f7ba-a47a-46b9-b70d-e4abdfff2119 NEW row; armor:d640f7ba-a47a-46b9-b70d-e4abdfff2125 NEW row | none |
| 2035 | Ordinance an Archery Overhaul | gameplay data, other game data (xml) | 10 / 48 | 8 | 0.317 | high / none | pickable_item:7db6b854-e307-4a47-ba39-943190b2469e price 1->38; pickable_item:c49aa63a-07a6-4417-9f9b-97f2712a4cd0 weight 0.1->0.7 | none |
| 1062 | SIM Camping Mini ML 1.5.1.1 | gameplay data, scripts, UI, text | 39 / 12 | 11 | 0.667 | high / medium | food:007ec8d6-1ce1-4e90-8267-7c349812ddcd NEW row; item:ef8970f9-2cc6-47c6-81a9-1939fc48e265 NEW row | none |
| 2173 | True Hardcore Maintenance (PTF) | gameplay data, text | 7 / 41 | 8 | 1.0 | high / low | pickable_item:85310d06-2845-46ee-be8f-295503b35035 weight 0.1->0.5; pickable_item:9f7a0c0a-6458-4622-9cc5-2f4dd4898b50 weight 0.1->0.5 | none |
| 2209 | Poisonous Enemies - True Hardcore Compatibility  | gameplay data, scripts, text | 36 / 0 | 6 | 0.0 | high / low | armor:a36ebe4e-14e0-4110-b903-5c225a831410 NEW row; armor:b58d737a-0b33-410d-bcf1-c16f1e5fb682 NEW row | none |
| 1105 | Service Prices | gameplay data, scripts | 0 / 6 | 1 | 0.0 | high / none | sequence:55336/ script Utils.SetLocalVar('s->Utils.SetLocalVar('s; sequence:55338/ script Utils.SetLocalVar('s->Utils.SetLocalVar('s | none |
| 2343 | Ultimate Horse Caparison Fix | gameplay data, scripts, other game data (xml), | 6 / 0 | 2 | 0.0 | high / high | character_hair:/d1317f64-c1c7-4c2d-b013-8f67c0201313/0/1/0 NEW row; character_hair:/d1317f64-c1c7-4c2d-b013-8f67c0201314/0/1/0 NEW row | none |
| 2318 | Visual Combo Helper | scripts, UI | 0 / 0 | 0 | 0.0 | high / medium | ui: 3; docs: 2; manifest: 1; pak (container): 1; scripts (Lua): 1; lua identical to vanilla: 0 | none |
| 2323 | Alchemy Stash Link | scripts | 0 / 0 | 0 | 0.0 | high / none | scripts (Lua): 3; manifest: 1; pak (container): 1; lua identical to vanilla: 0 | none |

## C effective (few rows, strong effect) (53)

| Id | Mod | Domain | Rows (new / changed) | Tables | Median rel. | Gameplay / visual | Highlights | Risk |
|---|---|---|---|---|---|---|---|---|
| 1334 | Fast Learning Henry | gameplay data | 4 / 92 | 2 | 4.0 | high / none | rpg_param:PickpocketingFailXPMod rpg_param_value 0.3->2; rpg_param:PickpocketingFailXPMod rpg_param_value 0.3->2 | none |
| 1260 | RPG Tweaks | gameplay data | 9 / 86 | 3 | 0.5 | high / none | perk_rpg_param_override:01c3b32a-5751-4c98-b6ab-258d02370382/RepairKitCapacity rpg_param_value 450->5200; rpg_param:HerbGatherSkillToRadius rpg_param_ | none |
| 1864 | Cheap Savior Schnapps - PTF | gameplay data | 0 / 89 | 3 | 10.0 | high / none | shop_type2item:928463d9-e21a-4f7c-b5d3-8378ed375cd1 amount 2->100; shop_type2item:928463d9-e21a-4f7c-b5d3-8378ed375cd1 amount 4->100 | none |
| 2165 | Merchants Richer | gameplay data | 0 / 79 | 1 | 2.0 | high / none | shop_type2item:5ef63059-322e-4e1b-abe8-926e100c770e amount 2800->8400; shop_type2item:5ef63059-322e-4e1b-abe8-926e100c770e amount 200->600 | none |
| 1853 | Richer Merchants (PTF) | gameplay data | 0 / 78 | 1 | 10.0 | high / none | shop_type2item:5ef63059-322e-4e1b-abe8-926e100c770e amount 2800->100000; shop_type2item:5ef63059-322e-4e1b-abe8-926e100c770e amount 200->100000 | none |
| 1559 | Karnages_Weapons_Damage_Balance 2.0 | gameplay data | 0 / 77 | 1 | 1.727 | high / none | melee_weapon:aca90050-0b70-4ca0-9d29-b94326203c75 smash_att_mod 0.05->0.7; melee_weapon:ec470e0c-5bbd-43bb-803e-0e7867253c25 smash_att_mod 0.05->0.6 | none |
| 1950 | Skill Books Take Time | gameplay data | 0 / 57 | 2 | 1.0 | high / none | document:0a9b5b2a-2614-4f11-a987-aab64133bea0 length_in_game_hours 6->12; document:0defd37d-cfec-446f-b307-e9ef65fea3f3 length_in_game_hours 6->12 | none |
| 1572 | Increased Experience Gains | gameplay data | 2 / 37 | 1 | 0.5 | high / none | rpg_param:AlchemyXPPerAutocookBrewingRelative NEW row; rpg_param:HerbGatherXP NEW row | none |
| 1660 | Double Brew Yield | gameplay data | 0 / 35 | 1 | 1.0 | high / none | recipe:310e921d-da62-48e4-88ef-de9f295e0045/f1309a89-045f-44ae-a4d9-c997b892a162/2 max_yield 3->6; recipe:e96d768e-04e5-4480-9197-1c256d642ddc/8b713d0 | none |
| 1668 | Relaxed RPG Params | gameplay data | 7 / 26 | 1 | 0.5 | high / none | rpg_param:RepairKitCapacity rpg_param_value 200->4500; rpg_param:DogMoraleBuffFeed rpg_param_value 0.08->0.75 | none |
| 1070 | Better Combat | gameplay data, engine config | 19 / 13 | 2 | 0.375 | high / none | rpg_param:CombatAutoAttackDelayIncreasePerAttackerHorse NEW row; rpg_param:CombatAutoAttackDelayIncreasePerAttackerMissile NEW row | none |
| 1564 | Karnages_Rebalanced_Bows 2.0 | gameplay data | 9 / 21 | 2 | 0.234 | high / none | rpg_param:BowPowerToChargeDuration NEW row; rpg_param:BowChargeDurationMin NEW row | none |
| 1926 | Potion no Satiety and ADD Heal plus Energy | gameplay data | 0 / 22 | 1 | 1.0 | high / none | food:73ff1fde-ec8b-41e9-95e3-b5938c715bf1 refresh_benefit 4->100; food:2509115d-59c9-44f8-9802-f600eba63fa9 refresh_benefit 4->100 | none |
| 1678 | Better Archery | gameplay data | 5 / 16 | 2 | 0.482 | high / none | rpg_param:BowChargeDurationMin NEW row; rpg_param:BowChargeDurationMax NEW row | none |
| 1419 | Immersive Archery | gameplay data | 5 / 15 | 2 | 0.541 | high / none | rpg_param:BowChargeDurationMin NEW row; rpg_param:BowChargeDurationMax NEW row | none |
| 1545 | Saddles Have Durability | gameplay data | 0 / 20 | 1 | 1.0 | high / none | armor:406c92ad-4c17-25d7-84d7-28500800f59e max_status 0->50; armor:40c16f73-5b83-c139-96eb-c39ff5e9e7a6 max_status 0->50 | none |
| 1730 | Drink Sound Effects | gameplay data | 9 / 9 | 2 | 0.0 | high / none | potion:0cb47176-06c5-42a9-8d70-969e917eb999 NEW row; potion:38df365c-a4bb-462b-80cc-eb92f16930fa NEW row | none |
| 1883 | Better Pickpocket - FIXED | gameplay data | 15 / 2 | 1 | 1.25 | high / none | rpg_param:PickpocketingXP rpg_param_value 15->45; rpg_param:PicklockFatalRelativeDist NEW row | none |
| 1914 | Weightless Herbs | gameplay data | 0 / 17 | 1 | 1.0 | high / none | pickable_item:0290b689-c01c-480f-b121-bed71ad1f5e0 weight 0.1->0; pickable_item:05bef17b-ddeb-426d-aa53-52ff6d4f521e weight 0.1->0 | none |
| 765 | Poison Overhaul | gameplay data, text | 3 / 12 | 4 | 2.0 | high / low | buff:f405cbea-2a3f-4363-9e6a-23417e4e2a14 duration 25->300; food:5c17d1d9-70ec-49d9-9b05-ae23247c045f alcohol_content 20->150 | none |
| 1376 | Archery mod - Faster arrows (for real) | gameplay data, other game data (xml) | 0 / 14 | 1 | 0.818 | high / none | ammo:13ba7468-11a2-483d-8cb9-25ce36a2d228 power_mod 1->2; ammo:19df1c5c-3dbf-45c0-ac01-336facf5f741 power_mod 1->2 | none |
| 1565 | Karnages_Arrow_Balance 2.0 | gameplay data, other game data (xml) | 0 / 12 | 1 | 1.0 | high / none | ammo:13ba7468-11a2-483d-8cb9-25ce36a2d228 smash_att 0->0.1; ammo:c49aa63a-07a6-4417-9f9b-97f2712a4cd0 smash_att 0->0.1 | none |
| 804 | Loose (An Archery Mod) | gameplay data, other game data (xml) | 9 / 2 | 1 | 0.225 | high / none | rpg_param:AimSpreadSkillDecrease NEW row; rpg_param:AimZoomBase NEW row | none |
| 1990 | Veteran Hunting | gameplay data, scripts, text | 3 / 8 | 4 | 1.0 | high / low | buff:7e42e183-222b-42a6-addb-e1e1cb4ae4d3 NEW row; perk_buff:c92e5f13-4b57-4b02-b9cf-74e88e3b2517/7e42e183-222b-42a6-addb-e1e1cb4ae4d3 NEW row | none |
| 802 | Archery for 1.9 | gameplay data | 9 / 1 | 1 | 0.5 | high / none | rpg_param:BowPowerToChargeDuration NEW row; rpg_param:BowChargeDurationMin NEW row | none |
| 1266 | Stronger drinks - PTF Edition | gameplay data | 0 / 9 | 1 | 0.5 | high / none | food:9e782670-3291-4382-a6d3-a843d13e67d9 alcohol_content 5->30; food:2529e246-6f1b-4529-8d6b-64245207bae8 alcohol_content 90->160 | none |
| 1243 | Easier Enemies PTF (Dumber Enemies) | gameplay data | 0 / 8 | 1 | 0.629 | high / none | rpg_param:CombatAutoAttackDelayIncreasePerAttacker rpg_param_value 0.8->3.2; rpg_param:CombatAutoNoDefenseWeight rpg_param_value 0.4->1.2025 | none |
| 1842 | Realistic Repairs | gameplay data | 4 / 4 | 3 | 0.567 | high / none | skill2item_category:armor.horse_bridle.*/8 NEW row; skill2item_category:armor.horse_saddle.*/8 NEW row | none |
| 1996 | Alcohol Is Not Food Anymore | gameplay data | 0 / 8 | 1 | 0.694 | high / none | food:c64b7286-07b8-4bdf-afd0-359171d35249 nutrition_benefit 20->3; food:2529e246-6f1b-4529-8d6b-64245207bae8 nutrition_benefit 20->3 | none |
| 2021 | Repair Kits - Balanced and Scaled PTF | gameplay data | 0 / 8 | 1 | 1.0 | high / none | ointment_item:238538b5-cd3e-460e-8e85-52c820edb716 efficiency 0.5->1; ointment_item:6aeb1531-369e-47cc-ad6c-f78df1c37d13 efficiency 1->2 | none |
| 2340 | MatthusTweaks - Equipment and Progression Overha | gameplay data | 6 / 0 | 2 | 0.0 | high / none | perk_rpg_param_override:01c3b32a-5751-4c98-b6ab-258d02370382/DamageToArmorStatus NEW row; perk_rpg_param_override:01c3b32a-5751-4c98-b6ab-258d02370382 | none |
| 480 | Bed Comfort Restored | gameplay data | 0 / 5 | 1 | 0.6 | high / none | sleeping_spot_type:4 sleeping_quality 0.1->0.3; sleeping_spot_type:2 sleeping_quality 0.3->0.5 | none |
| 1243 | Easier Enemies PTF (Dumber Enemies) | gameplay data, other game data (xml) | 0 / 5 | 1 | 0.341 | high / none | rpg_param:CombatAutoSPBWeight rpg_param_value 1.5->0; rpg_param:CombatAutoNoDefenseWeight rpg_param_value 0.4->0.775 | none |
| 1375 | No Aim Spread (Bow sway disabler) | gameplay data, text | 5 / 0 | 5 | 0.0 | high / low | perk:ae32e325-fe7e-48d6-90bc-d04707e9fe5b NEW row; buff:dfa3d59d-5da0-41bc-8ce5-a2c1d7b4ed0c NEW row | none |
| 1424 | Better Sleep Fixed | gameplay data | 0 / 5 | 1 | 1.4 | high / none | sleeping_spot_type:4 sleeping_quality 0.1->1.2; sleeping_spot_type:2 sleeping_quality 0.3->1.2 | none |
| 1782 | No more clipping elbows for Andrew | gameplay data | 5 / 0 | 2 | 0.0 | high / none | armor2clothing_preset:40692480-f24c-54fa-c938-50ccf45918b9/954dbf59-076e-094b-5d0a-4e44bec85cbb NEW row; armor2clothing_preset:4517b07b-ca19-07bf-6011 | none |
| 1195 | Get Water | gameplay data, scripts, UI, text | 4 / 0 | 4 | 0.0 | high / medium | item:2aef9b0a-f485-4935-be7d-7ceee381b547 NEW row; pickable_item:2aef9b0a-f485-4935-be7d-7ceee381b547 NEW row | none |
| 1292 | Ultimate Repair Kit 2.0 | gameplay data | 3 / 1 | 3 | 0.0 | high / none | rpg_param:RepairKitItemHealthBestLimit NEW row; skill2item_category:armor.horse_bridle.*/8 NEW row | none |
| 284 | No Mo' Slow Mo - Configurable Perfect Block Slow | gameplay data, other game data (xml), textures | 0 / 3 | 3 | 1.667 | high / low | rpg_param:CombatAutoSPBWeight rpg_param_value 1.5->-1; rpg_param:CombatAutoSPBWeight rpg_param_value 1.5->-1 | none |
| 1100 | Faster archery - PTF Edition | gameplay data | 3 / 0 | 1 | 0.0 | high / none | rpg_param:BowChargeDurationMin NEW row; rpg_param:BowChargeDurationMax NEW row | none |
| 1863 | Dirty And Charismatic - PTF | gameplay data | 2 / 1 | 2 | 1.0 | high / none | perk_rpg_param_override:/ArmorDirtToCharismaCoef NEW row; perk_rpg_param_override:/ArmorStatusToCharismaCoef NEW row | none |
| 2340 | MatthusTweaks - Equipment and Progression Overha | gameplay data | 1 / 2 | 2 | 0.0 | high / none | shop_type2item:aca90050-0b70-4ca0-9d29-b94326203c75 NEW row; weapon2weapon_preset:ec470e0c-5bbd-43bb-803e-0e7867253c25 weapon_preset_id 463dc53f-86c2- | none |
| 390 | Stay Clean Longer - Get Dirty Gradually | gameplay data | 1 / 1 | 2 | 1.0 | high / none | perk_rpg_param_override:01c3b32a-5751-4c98-b6ab-258d02370382/FullClothDirtyingOnFullSpeed rpg_param_value 5000->10000; rpg_param:FullClothDirtyingOnFu | MEDIUM |
| 1084 | Overpowered Bows - PTF Edition | gameplay data | 0 / 2 | 1 | 0.536 | high / none | missile_weapon:f2c83abc-2252-49f6-bbb7-dc8bc02979b2 power 54->100; missile_weapon:9bafcc7f-3931-4cc4-89ce-8f6ab205dfa8 power 82->100 | none |
| 1236 | Easy Combat PTF (easy parry and master strike) | gameplay data, other game data (xml) | 0 / 2 | 1 | 3.265 | high / none | rpg_param:MaxSpecialPerfectBlockSlotModifier rpg_param_value 0.6->3; rpg_param:MaxPerfectBlockSlotModifier rpg_param_value 0.85->3 | none |
| 1426 | Energy and Hunger Patch for Timescale Mods (PTF) | gameplay data | 2 / 0 | 1 | 0.0 | high / none | rpg_param:DigestionSpeed NEW row; rpg_param:ExhaustionSpeed NEW row | none |
| 1765 | Restore Riposte | gameplay data, other game data (xml), text | 0 / 2 | 1 | 0.8 | high / low | perk:ec4c5274-50e3-4bbf-9220-823b080647c4 visibility 0->2; perk:61e98757-9b32-493b-ad09-0087afdb81be visibility 0->1 | MEDIUM |
| 1862 | Faster Inury Regeneration - PTF | gameplay data | 1 / 1 | 2 | 0.5 | high / none | perk_rpg_param_override:/InjuryRegenInterval NEW row; perk_rpg_param_override:01c3b32a-5751-4c98-b6ab-258d02370382/InjuryRegenInterval rpg_param_value | none |
| 1893 | Bianca's Ring PTF | gameplay data | 0 / 2 | 2 | 1.0 | high / none | equippable_item:aac0794c-8fb7-41f5-ba6a-90c313c286b2 conspicuousness 0.1->-1; armor:aac0794c-8fb7-41f5-ba6a-90c313c286b2 noise 0->-1 | none |
| 1425 | Saving Soles (PTF) | gameplay data | 0 / 1 | 1 | 1.0 | high / none | rpg_param:ShoeHealthDecrease rpg_param_value 0.001->0 | none |
| 1578 | Weighed Groschen - PTF Version | gameplay data | 0 / 1 | 1 | 1.0 | high / none | pickable_item:5ef63059-322e-4e1b-abe8-926e100c770e weight 0->0.0005 | none |
| 1860 | Train More Carry More - PTF | gameplay data | 1 / 0 | 1 | 0.0 | high / none | rpg_param:StrengthToInventoryCapacity NEW row | none |
| 1938 | My Herb Picking Radius | gameplay data | 0 / 1 | 1 | 1.0 | high / none | rpg_param:HerbGatherSkillToRadius rpg_param_value 0.25->0.5 | none |

## D small tweak (22)

| Id | Mod | Domain | Rows (new / changed) | Tables | Median rel. | Gameplay / visual | Highlights | Risk |
|---|---|---|---|---|---|---|---|---|
| 1671 | Angriness Begone | gameplay data | 0 / 7 | 1 | 1.0 | medium / none | angriness_enum:2 value 0.55->0; angriness_enum:4 value 0.01->0 | none |
| 1693 | Ravens beak and Spiked warhammer icon swap | gameplay data | 0 / 2 | 1 | 0.0 | medium / none | player_item:e16b0af6-fb6a-43e2-9a9c-1b8c227e64b8 icon_id 152->150; player_item:488d9792-0dbf-41dc-a320-753d94d1f1b6 icon_id 150->152 | none |
| 1569 | Karnages_Shield_Restoration | gameplay data | 0 / 1 | 1 | 0.0 | medium / none | skill:20 hidden True->False | none |
| 83 | More Responsive Targeting | engine config | 0 / 0 | 0 | 0.0 | medium / none | config (.cfg): 1; lua identical to vanilla: 0 | none |
| 84 | Archery - Realistic Arrow Flight | other game data (xml) | 0 / 0 | 0 | 0.0 | medium / none | pak (container): 1; other game data (xml, not table rows): 1; lua identical to vanilla: 0 | none |
| 1040 | Disable Combat Slowmotion | scripts | 0 / 0 | 0 | 0.0 | none / none | manifest: 1; pak (container): 1; scripts (Lua): 1; lua identical to vanilla: 0 | none |
| 1518 | Waystones Give XP | scripts | 0 / 0 | 0 | 0.0 | medium / none | manifest: 1; pak (container): 1; scripts (Lua): 1; lua identical to vanilla: 0 | none |
| 1519 | Shooting Nests Gives XP | scripts | 0 / 0 | 0 | 0.0 | high / none | manifest: 1; pak (container): 1; scripts (Lua): 1; lua identical to vanilla: 0 | none |
| 1520 | Shooting Archery Targets Gives XP | scripts | 0 / 0 | 0 | 0.0 | high / none | manifest: 1; pak (container): 1; scripts (Lua): 1; lua identical to vanilla: 0 | none |
| 1612 | Remove Auto Camera Lock In Combat | engine config | 0 / 0 | 0 | 0.0 | medium / none | config (.cfg): 1; lua identical to vanilla: 0 | none |
| 1647 | Slo Mo Begone | scripts | 0 / 0 | 0 | 0.0 | none / none | manifest: 1; pak (container): 1; scripts (Lua): 1; lua identical to vanilla: 0 | none |
| 1655 | Save Me Henry | scripts, other game data (xml) | 0 / 0 | 0 | 0.0 | medium / none | other game data (xml, not table rows): 2; manifest: 1; pak (container): 1; scripts (Lua): 1; lua identical to vanilla: 0 | none |
| 1743 | Persistent Arrows | other game data (xml) | 0 / 0 | 0 | 0.0 | medium / none | manifest: 1; pak (container): 1; other game data (xml, not table rows): 1; lua identical to vanilla: 0 | none |
| 1951 | Baths dont affect energy and nourishment | other game data (xml) | 0 / 0 | 0 | 0.0 | medium / none | pak (container): 1; other game data (xml, not table rows): 1; lua identical to vanilla: 0 | none |
| 2040 | Polymorphic Projectiles Arrow Overhaul | other game data (xml), text | 0 / 0 | 0 | 0.0 | medium / low | localization: 3; manifest: 1; docs: 1; pak (container): 1; other game data (xml, not table rows): 1; lua identical to vanilla: 0 | none |
| 2066 | Distant Smoke and Fire | other game data (xml) | 0 / 0 | 0 | 0.0 | medium / none | manifest: 1; pak (container): 1; other game data (xml, not table rows): 1; lua identical to vanilla: 0 | none |
| 2192 | ENHANCED Toggle Aim Overhaul v2.0 KCD I | scripts, other game data (xml) | 0 / 0 | 0 | 0.0 | medium / none | config (.cfg): 1; manifest: 1; pak (container): 1; other game data (xml, not table rows): 1; scripts (Lua): 1; lua identical to vanilla: 0 | none |
| 2194 | ENHANCED Easy FREE Combat Target Overhaul v3.0 K | scripts, other game data (xml) | 0 / 0 | 0 | 0.0 | high / none | scripts (Lua): 2; config (.cfg): 1; manifest: 1; pak (container): 1; other game data (xml, not table rows): 1; lua identical to vanilla: 0 | none |
| 2280 | Remove Artemisia (Wormwood) Potion Visual Effect | other game data (xml) | 0 / 0 | 0 | 0.0 | medium / none | manifest: 1; pak (container): 1; other game data (xml, not table rows): 1; lua identical to vanilla: 0 | none |
| 2332 | Baptism of Fire Fix Redux | other game data (xml) | 0 / 0 | 0 | 0.0 | medium / none | manifest: 1; docs: 1; pak (container): 1; other game data (xml, not table rows): 1; lua identical to vanilla: 0 | none |
| 2372 | Trough Washing Animation | scripts, other game data (xml), textures/model | 0 / 0 | 0 | 0.0 | medium / high | other: 16; models/animations/materials: 6; other game data (xml, not table rows): 3; textures: 3; manifest: 1; pak (container): 1; scripts (Lua): 1; l | none |
| 2381 | Nest of Vipers Stealth | other game data (xml) | 0 / 0 | 0 | 0.0 | medium / none | other game data (xml, not table rows): 2; manifest: 1; docs: 1; pak (container): 1; lua identical to vanilla: 0 | none |

## E visual, audio or UI only (no gameplay change) (11)

| Id | Mod | Domain | Rows (new / changed) | Tables | Median rel. | Gameplay / visual | Highlights | Risk |
|---|---|---|---|---|---|---|---|---|
| 366 | First-person Herb Picking | textures/models/animations | 0 / 0 | 0 | 0.0 | low / high | models/animations/materials: 2; manifest: 1; pak (container): 1; lua identical to vanilla: 0 | none |
| 591 | Bushes- Collision Remover | textures/models/animations | 0 / 0 | 0 | 0.0 | low / high | models/animations/materials: 26; pak (container): 1; lua identical to vanilla: 0 | none |
| 1090 | Colored Arrows | textures/models/animations | 0 / 0 | 0 | 0.0 | low / medium | textures: 11; manifest: 1; pak (container): 1; lua identical to vanilla: 0 | none |
| 1205 | ETSGF - Easy to see glowing Arrow feathers  - 1. | textures/models/animations | 0 / 0 | 0 | 0.0 | low / high | models/animations/materials: 10; manifest: 1; pak (container): 1; lua identical to vanilla: 0 | none |
| 1205 | ETSGF - Easy to see glowing Arrow feathers  - 1. | textures/models/animations | 0 / 0 | 0 | 0.0 | low / high | models/animations/materials: 10; manifest: 1; pak (container): 1; textures: 1; lua identical to vanilla: 0 | none |
| 1323 | Skalitz Shield Fix AWL | textures/models/animations | 0 / 0 | 0 | 0.0 | low / high | textures: 6; manifest: 1; docs: 1; pak (container): 1; models/animations/materials: 1; lua identical to vanilla: 0 | none |
| 1922 | No Prefixes in Alchemy Book | UI, text | 0 / 0 | 0 | 0.0 | low / medium | localization: 28; manifest: 1; pak (container): 1; ui: 1; lua identical to vanilla: 0 | none |
| 1991 | BCAIC - Restore Hunting Spots - Patch | textures/models/animations, UI | 0 / 0 | 0 | 0.0 | low / medium | ui: 4; textures: 2; manifest: 1; pak (container): 1; lua identical to vanilla: 0 | none |
| 2207 | Findable Herbs HD | textures/models/animations | 0 / 0 | 0 | 0.0 | low / low | manifest: 1; pak (container): 1; textures: 1; lua identical to vanilla: 0 | none |
| 2276 | Instant Herb and faster Alchemy Merger | textures/models/animations | 0 / 0 | 0 | 0.0 | low / high | models/animations/materials: 4; manifest: 1; pak (container): 1; lua identical to vanilla: 0 | none |
| 2331 | Bushes Collision Remover Redux | textures/models/animations | 0 / 0 | 0 | 0.0 | low / high | models/animations/materials: 26; manifest: 1; docs: 1; pak (container): 1; lua identical to vanilla: 0 | none |

## E text only (no gameplay change) (2)

| Id | Mod | Domain | Rows (new / changed) | Tables | Median rel. | Gameplay / visual | Highlights | Risk |
|---|---|---|---|---|---|---|---|---|
| 2098 | Medieval Poisons - spolszczenie | text | 0 / 0 | 0 | 0.0 | low / low | localization: 2; lua identical to vanilla: 0 | none |
| 2362 | Better Perk Descriptions | text | 0 / 0 | 0 | 0.0 | low / low | localization: 2; manifest: 1; lua identical to vanilla: 0 | none |

## E non-perceptive to gameplay (no effective change found) (2)

| Id | Mod | Domain | Rows (new / changed) | Tables | Median rel. | Gameplay / visual | Highlights | Risk |
|---|---|---|---|---|---|---|---|---|
| 1673 | Combat musics tweak | none | 0 / 0 | 0 | 0.0 | none / none | other: 2; manifest: 1; pak (container): 1; lua identical to vanilla: 0 | none |
| 1673 | Combat musics tweak | none | 0 / 0 | 0 | 0.0 | none / none | other: 2; manifest: 1; pak (container): 1; lua identical to vanilla: 0 | none |

## X not analysed (3)

| Id | Mod | Domain | Rows (new / changed) | Tables | Median rel. | Gameplay / visual | Highlights | Risk |
|---|---|---|---|---|---|---|---|---|
| 311 | O' Hungry Henry | none | 0 / 0 | 0 | 0.0 | unknown / none | docs: 1; pak (container): 1; lua identical to vanilla: 0 | none |
| 2017 | Realistic Items | none | 0 / 0 | 0 | 0.0 | unknown / none | manifest: 1; pak (container): 1; lua identical to vanilla: 0 | none |
| 2017 | Realistic Items | none | 0 / 0 | 0 | 0.0 | unknown / none | pak (container): 1; lua identical to vanilla: 0 | none |

## Overlap between the analysed mods

4643 table rows are changed by two or more of the 131 mods (`mod_overlap.csv`). Most contested: rpg_param:CombatAutoSPBWeight (12 mods); rpg_param:CombatAutoMaxAttackDelay (11 mods); rpg_param:CombatAutoNormalBWeight (10 mods); rpg_param:MaxPerfectBlockSlotModifier (10 mods); rpg_param:MaxSpecialPerfectBlockSlotModifier (10 mods); rpg_param:CombatAutoPBWeight (10 mods); rpg_param:CombatAutoAttackDelayIncreasePerAttacker (10 mods); food:2529e246-6f1b-4529-8d6b-64245207bae8 (9 mods).

Pairs of mods that change the most rows in common (rows shared by 2 to 8 mods; the later one in load order wins each row):

| Mod A | Mod B | Shared rows |
|---|---|---|
| 2124 Half-looted Rebalance | 2299 1403 - Historical Rebalance | 2745 |
| 2299 1403 - Historical Rebalance | 2340 MatthusTweaks - Equipment and Progressio | 1565 |
| 883 KingdomCome Rebalancing | 2299 1403 - Historical Rebalance | 1038 |
| 1560 Karnages_Durability_Redux | 2299 1403 - Historical Rebalance | 960 |
| 2124 Half-looted Rebalance | 2340 MatthusTweaks - Equipment and Progressio | 846 |
| 883 KingdomCome Rebalancing | 2340 MatthusTweaks - Equipment and Progressio | 841 |
| 1560 Karnages_Durability_Redux | 2124 Half-looted Rebalance | 838 |
| 883 KingdomCome Rebalancing | 2124 Half-looted Rebalance | 776 |
| 2049 Simple Ragdoll Physics | 2299 1403 - Historical Rebalance | 402 |
| 1560 Karnages_Durability_Redux | 2340 MatthusTweaks - Equipment and Progressio | 347 |
| 2049 Simple Ragdoll Physics | 2124 Half-looted Rebalance | 337 |
| 883 KingdomCome Rebalancing | 1560 Karnages_Durability_Redux | 284 |
| 85 Perkaholic | 1009 Perkaholic - PTF updated (1.9.4-1.9.8) | 192 |
| 651 Better Combat and Immersion Compilation | 2124 Half-looted Rebalance | 191 |
| 85 Perkaholic | 770 Perkaholic updated | 186 |

25 archives change rows that a KRS module also sets (the later mod in load order wins the whole row): 480, 651, 883, 1260, 1292, 1334, 1424, 1426, 1558, 1572, 1765, 1839, 1842, 1860, 1926, 1938, 1950, 2011, 2124, 2173, 2188, 2210, 2299, 2340, 2345.

## Needs something outside the game files

651 (states requirements); 1736 (user.cfg); 2049 (states requirements); 2294 (Vortex, mentions Tables.pak, states requirements); 2299 (states requirements); 2331 (states requirements); 2338 (Vortex); 2381 (Vortex)
