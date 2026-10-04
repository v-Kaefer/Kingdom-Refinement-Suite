# Mod analysis: what the P3/P4 and unlisted mods change (generated)

> **GENERATED** by `tools/audit_mods_deep.py`: do not edit | **Kind:** review | **Trust:** archives read statically (listed, extracted to a scratch folder, read, deleted); nothing was installed or run | **Game version:** 1.9.8

Read on 2026-10-04: **227 archives, folders and loose files of 208 mods** (all P3/P4 and unlisted mods that are in the downloads folder). Method: each archive is listed with 7-Zip (nothing extracted yet) and judged for risk; the safe ones are extracted to a scratch folder, read with Python (file names, magic bytes, XML tables compared with the vanilla `Tables.pak`, Lua and config text), and the scratch folder is deleted. No file was executed, installed or loaded by the game; no game run was made. Per-mod detail: [`MOD_PROFILES_P3_P4.md`](MOD_PROFILES_P3_P4.md); tables: `mod_analysis_p3_p4.csv`, `mod_tables_p3_p4.csv`, `mod_overlap_p3_p4.csv`, `risk_scan_p3_p4.csv`.

## Risk result

| Level | Archives |
|---|---|
| HIGH | 19 |
| MEDIUM | 7 |
| LOW | 0 |
| none | 201 |

HIGH means native code, scripts or shortcuts, dangerous Lua calls, path traversal or encrypted entries: those archives were moved to `_quarantine/` (19 moved). Details and how to restore them: [`QUARANTINE.md`](QUARANTINE.md).

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
| A changes the most | 46 | 41 |
| B large | 17 | 17 |
| C effective (few rows, strong effect) | 24 | 24 |
| D small tweak | 54 | 46 |
| E visual, audio or UI only (no gameplay change) | 65 | 61 |
| E text only (no gameplay change) | 5 | 5 |
| E non-perceptive to gameplay (no effective change found) | 14 | 13 |
| X not analysed | 2 | 2 |

Loads on 1.9.8 by the manifest rule (docs/engine/game-versions.md): yes 119, NO 20, no manifest (legacy install) 88.

How the mods install: 139 x Mods/<mod folder> with mod.manifest (Vortex or manual); 71 x unclear: read the archive's own instructions; 11 x loose .pak (legacy: copy into Data); 4 x legacy: files go into the game's Bin folder; 2 x legacy: files go into the game's Data folder.

Layout problems found (each makes the mod do nothing or something other than intended): table files without a suffix, in total: 72; archives with table files without a suffix (they replace whole vanilla tables): 20; archives whose pak is not a ZIP (not readable by the game): 2.

## A changes the most (46)

| Id | Mod | Domain | Rows (new / changed) | Tables | Median rel. | Gameplay / visual | Highlights | Risk |
|---|---|---|---|---|---|---|---|---|
| 2061 | Meticulously Edited Shops and Services | gameplay data | 1449 / 6013 | 3 | 0.943 | high / none | shop_type2item:00000000-0000-0000-0000-00000000001b amount 3->100; shop_type2item:22eb16a0-1175-4e2e-a951-33d362e288fb amount 1->100 | none |
| 840 | Blood and Iron Encounter System | gameplay data | 0 / 5081 | 2 | 0.647 | high / none | random_event:0/5/5 base_run_chance 0.07->0.5; random_event:0/68/7 base_run_chance 0.15->0.4 | none |
| 808 | Named NPCs | gameplay data, text | 3263 / 0 | 1 | 0.0 | high / low | v_soul_character_data:soul_ui_name_armorer_001/4203d715-43a1-0049-e26b-8579c81ce0b0/0 NEW row; v_soul_character_data:soul_ui_name_armorer_002/4618f1c3 | none |
| 808 | Named NPCs | gameplay data, text | 3263 / 0 | 1 | 0.0 | high / low | v_soul_character_data:soul_ui_name_armorer_001/4203d715-43a1-0049-e26b-8579c81ce0b0/0 NEW row; v_soul_character_data:soul_ui_name_armorer_002/4618f1c3 | none |
| 726 | Early Bird NPC Schedules | gameplay data | 0 / 2390 | 1 | 0.0 | high / none | soul:00000000-0000-0000-0000-000000035000/2a7b75cd-8344-43f6-8483-0191a079e503//9fe6dae0-e195-42e0-a3fb-66cfc6382407/498bc146-f7d1-1c55-7a6b-b549cbdfb | none |
| 726 | Early Bird NPC Schedules | gameplay data | 0 / 2390 | 1 | 0.0 | high / none | soul:00000000-0000-0000-0000-000000035000/2a7b75cd-8344-43f6-8483-0191a079e503//9fe6dae0-e195-42e0-a3fb-66cfc6382407/498bc146-f7d1-1c55-7a6b-b549cbdfb | none |
| 2158 | Finders Keepers | gameplay data | 0 / 2109 | 1 | 1.0 | high / none | pickable_item:00000000-0000-0000-0000-000000000005 owner_fading_coef 0.02->0; pickable_item:00000000-0000-0000-0000-00000000001b owner_fading_coef 0.0 | none |
| 1356 | Fan Side Quest - Heritage | gameplay data, scripts, other game data (xml), | 2022 / 27 | 48 | 1.08 | high / high | brain2subbrain:41564e9f-2a60-8716-22ee-d87fc4f11ca5/405923ef-0846-68eb-0983-f014f5b20bb9 NEW row; brain2subbrain:4db77d1f-f7a9-fcbd-57ed-b824e6ad1c85/ | MEDIUM |
| 829 | Shop Proper | gameplay data | 282 / 577 | 2 | 6.866 | high / none | shop_type2item:cda856d8-9ee4-4f61-b2c7-eace8e082d62 amount 2->8; shop_type2item:9fa3000e-3807-48a8-bed8-81427f0bda55 amount 3->12 | none |
| 1636 | More Sensible Weapons and Armor | gameplay data | 0 / 822 | 7 | 0.333 | high / none | equippable_item:00000000-0000-0000-0000-00000000001b conspicuousness -0.02->-0.26; equippable_item:4a22fe68-b9c5-7b04-ee81-23613de682b6 conspicuousnes | none |
| 2358 | MatthusTweaksKCDarmwea | gameplay data | 0 / 537 | 3 | 0.316 | high / none | armor:4fec3673-04fe-45ae-b200-600704ecea70 slash_def 0.1->1.25; melee_weapon:033fc7b6-17b6-486d-95cb-a22afb131be2 smash_att_mod 0.05->0.5978261129 | none |
| 2046 | Arsenal - A Weapons Overhaul - DDDB | gameplay data, text | 153 / 344 | 8 | 0.333 | high / low | melee_weapon:547dbb33-e2a7-414c-a2ea-379c96b776ee stab_att_mod 0.05->0.55; melee_weapon:662a3ac5-5883-4b7d-bd84-173eaa136a73 slash_att_mod 0.05->0.85 | none |
| 1777 | TyburnDiseases | gameplay data, scripts, other game data (xml), | 411 / 29 | 24 | 0.7 | high / high | inventory2item:ba85cb8a-80c3-420e-b073-1d50807334f6 NEW row; armor2clothing_attachment:e4f950e5-4b46-48e4-8b27-a910e87da97b NEW row | none |
| 1777 | TyburnDiseases | gameplay data, scripts, other game data (xml), | 411 / 29 | 24 | 0.7 | high / high | inventory2item:ba85cb8a-80c3-420e-b073-1d50807334f6 NEW row; armor2clothing_attachment:e4f950e5-4b46-48e4-8b27-a910e87da97b NEW row | none |
| 554 | Parameters Plus | gameplay data, other game data (xml) | 425 / 0 | 1 | 0.0 | high / none | rpg_param:AdditionalAttackerCountForMaxFadingBuff NEW row; rpg_param:AgiDiffToAttackSpeed NEW row | none |
| 2203 | Categorized Sorted Inventory | gameplay data, text | 0 / 425 | 1 | 0.0 | high / low | player_item:4d49d1bd-5a73-3659-5209-5a38acd4c0b6 ui_name ui_nm_jacket_001_rac->ui_nm_jacket_002_rac; player_item:4119b64e-f072-0cf2-4b8c-13e5ee901994  | none |
| 2204 | A Real Sorted Inventory (ARSI) | gameplay data, scripts, textures/models/animat | 0 / 425 | 1 | 0.0 | high / medium | player_item:4d49d1bd-5a73-3659-5209-5a38acd4c0b6 ui_name ui_nm_jacket_001_rac->ui_nm_jacket_002_rac; player_item:4119b64e-f072-0cf2-4b8c-13e5ee901994  | MEDIUM |
| 950 | Henry's Castle at Pribyslavits | gameplay data, scripts, other game data (xml), | 401 / 0 | 9 | 0.0 | high / high | equippable_item:c049e569-f0bf-4425-b0df-2e0a7f769af7 NEW row; item:c049e569-f0bf-4425-b0df-2e0a7f769af7 NEW row | MEDIUM |
| 1733 | TyburnMedievalPoisons | gameplay data, other game data (xml), textures | 268 / 71 | 20 | 1.0 | high / high | pickable_item:9186b747-2591-43c0-91c6-54146543a8d8 price 30->450; pickable_item:b5587dd4-f7d8-4378-9903-7626a227ca0f price 10->250 | none |
| 771 | Hoods Over Helmats Removed Clipping Helmets On N | gameplay data, scripts, engine config, graphic | 182 / 108 | 15 | 10.0 | high / high | rpg_param:BaseInventoryCapacity rpg_param_value 66->840; shop_type2item:5ef63059-322e-4e1b-abe8-926e100c770e amount 2800->2000000 | HIGH |
| 771 | Hoods Over Helmats Removed Clipping Helmets On N | gameplay data, scripts, engine config, graphic | 182 / 108 | 15 | 10.0 | high / high | rpg_param:BaseInventoryCapacity rpg_param_value 66->840; shop_type2item:5ef63059-322e-4e1b-abe8-926e100c770e amount 2800->2000000 | HIGH |
| 1088 | Polearms Unleashed | gameplay data, scripts, other game data (xml), | 107 / 49 | 18 | 0.171 | high / high | melee_weapon:44940b6c-f1f9-4ad1-9419-b5705a88e5b0 smash_att_mod 0.05->0.5; melee_weapon:033fc7b6-17b6-486d-95cb-a22afb131be2 smash_att_mod 0.05->0.5 | none |
| 1807 | TyburnPoisonousEnemies | gameplay data, scripts, other game data (xml), | 95 / 0 | 13 | 0.0 | high / low | armor2clothing_attachment:a36ebe4e-14e0-4110-b903-5c225a831410 NEW row; armor2clothing_preset:a36ebe4e-14e0-4110-b903-5c225a831410/41648381-53a9-5c97- | none |
| 1956 | Auto Hide HUD REBORN | gameplay data, scripts, textures/models/animat | 4 / 0 | 4 | 0.0 | high / medium | buff:2c19a972-cfcf-453b-9d27-82124899c579 NEW row; perk_buff:40f2a9e4-564b-48ff-89bb-937684416542/2c19a972-cfcf-453b-9d27-82124899c579 NEW row | MEDIUM |
| 106 | Cheat | gameplay data, scripts, other game data (xml), | 2 / 0 | 1 | 0.0 | high / low | buff:a218af80-b2a5-11ed-afa1-0242ac120002 NEW row; buff:a218b534-b2a5-11ed-afa1-0242ac120002 NEW row | HIGH |
| 491 | Loot Info - Container is empty or I already open | scripts, text | 0 / 0 | 0 | 0.0 | high / low | localization: 19; scripts (Lua): 17; docs: 2; config (.cfg): 1; manifest: 1; pak (container): 1; lua identical to vanilla: 0 | none |
| 972 | Let Me Loot | native/external | 0 / 0 | 0 | 0.0 | none / none | executables/scripts: 2; docs: 1; lua identical to vanilla: 0 | HIGH |
| 1046 | Rudy ENB for KCD | graphics config, post-processing (ReShade/ENB) | 0 / 0 | 0 | 0.0 | medium / high | reshade/ENB (shaders, presets): 27; textures: 9; docs: 1; config (.cfg): 1; lua identical to vanilla: 0 | none |
| 1074 | Realism Enlighted ReShade - lore-friendly realis | post-processing (ReShade/ENB), native/external | 0 / 0 | 0 | 0.0 | none / high | reshade/ENB (shaders, presets): 311; executables/scripts: 1; lua identical to vanilla: 0 | HIGH |
| 1193 | Weather Mod | scripts | 0 / 0 | 0 | 0.0 | high / none | scripts (Lua): 24; docs: 2; manifest: 1; pak (container): 1; lua identical to vanilla: 0 | HIGH |
| 1314 | Ultimate Ray Tracing KCD Reshade Preset | post-processing (ReShade/ENB), native/external | 0 / 0 | 0 | 0.0 | none / high | reshade/ENB (shaders, presets): 2; docs: 1; lua identical to vanilla: 0 | none |
| 1394 | KDC ReShader | post-processing (ReShade/ENB), native/external | 0 / 0 | 0 | 0.0 | none / high | reshade/ENB (shaders, presets): 58; lua identical to vanilla: 0 | HIGH |
| 1403 | Ultra Reshade for Low Settings | post-processing (ReShade/ENB), native/external | 0 / 0 | 0 | 0.0 | none / high | reshade/ENB (shaders, presets): 341; executables/scripts: 1; lua identical to vanilla: 0 | HIGH |
| 1428 | Reshade DOF With UI Mask | post-processing (ReShade/ENB), native/external | 0 / 0 | 0 | 0.0 | none / high | reshade/ENB (shaders, presets): 3; docs: 2; lua identical to vanilla: 0 | none |
| 1527 | Infinite Draw Distance | native/external | 0 / 0 | 0 | 0.0 | none / none | config (.cfg): 3; docs: 1; lua identical to vanilla: 0 | none |
| 1603 | Sharper graphic reshade for Kingdom Come Deliver | post-processing (ReShade/ENB), native/external | 0 / 0 | 0 | 0.0 | none / high | docs: 1; reshade/ENB (shaders, presets): 1; lua identical to vanilla: 0 | none |
| 1702 | SLEE realistic reshade preset and performance fi | engine config, graphics config, post-processin | 0 / 0 | 0 | 0.0 | medium / high | reshade/ENB (shaders, presets): 594; config (.cfg): 1; executables/scripts: 1; docs: 1; lua identical to vanilla: 0 | HIGH |
| 1829 | Mod Order Tool 1.2 | native/external | 0 / 0 | 0 | 0.0 | none / none | executables/scripts: 1; lua identical to vanilla: 0 | HIGH |
| 2244 | Kingdom Come Script Extender | native/external | 0 / 0 | 0 | 0.0 | none / none | executables/scripts: 1; other: 1; lua identical to vanilla: 0 | HIGH |
| 2255 | Fast Travel Tweaks | native/external | 0 / 0 | 0 | 0.0 | none / none | executables/scripts: 1; other: 1; lua identical to vanilla: 0 | HIGH |
| 2261 | Proper Third Person View (TPV Camera) | native/external | 0 / 0 | 0 | 0.0 | none / none | docs: 2; executables/scripts: 1; ini (text settings): 1; lua identical to vanilla: 0 | HIGH |
| 2270 | Horse Control Tweaks | native/external | 0 / 0 | 0 | 0.0 | none / none | executables/scripts: 1; other: 1; lua identical to vanilla: 0 | HIGH |
| 2277 | Toggle Hud - KCSE | native/external | 0 / 0 | 0 | 0.0 | none / none | executables/scripts: 1; ini (text settings): 1; other: 1; lua identical to vanilla: 0 | HIGH |
| 2365 | KCDT | native/external | 0 / 0 | 0 | 0.0 | none / none | executables/scripts: 1; manifest: 1; other: 1; lua identical to vanilla: 0 | HIGH |
| 2365 | KCDT | native/external | 0 / 0 | 0 | 0.0 | none / none | executables/scripts: 1; manifest: 1; other: 1; lua identical to vanilla: 0 | HIGH |
| 2366 | Faster Book Flipping | native/external | 0 / 0 | 0 | 0.0 | none / none | executables/scripts: 1; ini (text settings): 1; manifest: 1; other: 1; lua identical to vanilla: 0 | HIGH |

## B large (17)

| Id | Mod | Domain | Rows (new / changed) | Tables | Median rel. | Gameplay / visual | Highlights | Risk |
|---|---|---|---|---|---|---|---|---|
| 1153 | More historically accurate item stats | gameplay data | 0 / 370 | 6 | 1.09 | high / none | melee_weapon:24a7c868-f23f-4799-8e64-331435a77404 slash_att_mod 0.05->0.95; melee_weapon:3ef71c79-57c2-4f28-8f31-a091d9b78798 slash_att_mod 0.05->1 | none |
| 796 | Miller Guild Items | gameplay data, text | 123 / 107 | 13 | 1.0 | high / low | armor:4962e864-5964-aecf-7a62-6e117b96ec99 zone3_brightness 1->41; armor:ff5ab403-62fa-41d2-9afd-7d6857f999c4 noise 0.1->1 | none |
| 1535 | Dandelion Baron | gameplay data | 0 / 220 | 2 | 1.0 | high / none | pickable_item:3373a604-a2fd-4af0-a5e8-760e1a9893f9 price 2->0; pickable_item:5e9b4fa1-aafa-4352-b5d6-58df2c263caa price 1->0 | none |
| 977 | Alms for Beggars | gameplay data, text | 207 / 4 | 10 | 0.0 | high / low | clothing_mesh_data:Objects/characters/humans/body/s1_body_npc.skin/0/// NEW row; clothing_mesh_data:Objects/characters/humans/head/s1_head_v002.skin/0 | none |
| 2279 | Immersive Economy FIXED | gameplay data | 0 / 164 | 2 | 0.875 | high / none | rpg_param:ItemHealthPriceStatusWeight rpg_param_value 0.8->1; shop:25/17/14 price_sell_multiplier 1->0.1 | none |
| 1870 | Fair Trade - PTF | gameplay data | 0 / 133 | 1 | 0.375 | high / none | shop:25/15/13 price_sell_multiplier 0.5->1.5; shop:25/102/52 price_sell_multiplier 0.4->1.2 | none |
| 1873 | Daily Restock And Rich Merchants - PTF | gameplay data | 0 / 125 | 2 | 10.0 | high / none | shop_type2item:5ef63059-322e-4e1b-abe8-926e100c770e amount 2800->280000; shop_type2item:5ef63059-322e-4e1b-abe8-926e100c770e amount 200->20000 | none |
| 1110 | AI Standalone Library | gameplay data, other game data (xml) | 116 / 0 | 7 | 0.0 | high / none | brain2mailbox:47b6c85f-8264-085c-f9b4-aba01c3b6aa5/14e5d62e-91fd-436b-84b5-ae570a5391a5 NEW row; brain2mailbox:47b6c85f-8264-085c-f9b4-aba01c3b6aa5/3f | none |
| 1689 | Playable Daggers | gameplay data, scripts, textures/models/animat | 101 / 10 | 14 | 0.4 | high / high | weapon_class:/5/8a5dd3a2-04e1-4ce7-8833-9252b410662b/1/0/-1/-1/20/8/1 NEW row; inventory2item:e794cabc-9629-45c2-9f76-83231a80f7c5 NEW row | none |
| 2068 | SPOA Silver Knight Armor for Kingdom Come Delive | gameplay data, textures/models/animations, tex | 82 / 0 | 13 | 0.0 | high / high | armor2clothing_attachment:03bde0d1-1499-4cf1-8599-c9f865c6f787 NEW row; armor2clothing_preset:03bde0d1-1499-4cf1-8599-c9f865c6f787/440e9c0e-c8c9-c691- | none |
| 1566 | Karnages_Lost_Weapons_Pack_Redux 2.0 | gameplay data | 23 / 50 | 7 | 1.0 | high / none | melee_weapon:e5fc1a89-9bb1-44a9-a524-c6834a5e2e76 smash_att_mod 0.05->1; melee_weapon:a7d5c50c-de7d-4982-969e-33fcbccb749a smash_att_mod 0.05->2 | none |
| 2174 | Horse Body Armor (Barding) | gameplay data, textures/models/animations, tex | 65 / 0 | 12 | 0.0 | high / high | player_item:100c0a43-d863-4c8e-b49e-375c3fc825fb NEW row; player_item:cd23e264-eabb-49fe-973c-3d86c7910931 NEW row | none |
| 1605 | Formidable Runt | gameplay data | 25 / 8 | 7 | 0.667 | high / none | soul2skill:20/47e2f514-fa2e-826f-3565-c97a749265bc value 2->20; soul2skill:16/47e2f514-fa2e-826f-3565-c97a749265bc value 8->20 | none |
| 892 | Baselard Dagger | gameplay data, scripts, textures/models/animat | 17 / 0 | 7 | 0.0 | high / high | equippable_item:0e7b2f6b-8ff1-4154-a2de-77f3defb7a7c NEW row; item:0e7b2f6b-8ff1-4154-a2de-77f3defb7a7c NEW row | none |
| 966 | 15th to 16th Century style Ottoman sword | gameplay data, scripts, textures/models/animat | 16 / 0 | 14 | 0.0 | high / high | equippable_item:ad9b8664-4d94-423e-9189-ff4ba8f22282 NEW row; item:ad9b8664-4d94-423e-9189-ff4ba8f22282 NEW row | none |
| 2383 | Wooden Training Mace | gameplay data, other game data (xml), text | 6 / 0 | 6 | 0.0 | high / low | equippable_item:e53e6098-b10a-4efe-95fc-cd02bb489c69 NEW row; item:e53e6098-b10a-4efe-95fc-cd02bb489c69 NEW row | none |
| 1909 | Helmet-Off Dialog (Beta) | scripts | 0 / 0 | 0 | 0.0 | high / none | scripts (Lua): 19; manifest: 1; docs: 1; pak (container): 1; lua identical to vanilla: 0 | none |

## C effective (few rows, strong effect) (24)

| Id | Mod | Domain | Rows (new / changed) | Tables | Median rel. | Gameplay / visual | Highlights | Risk |
|---|---|---|---|---|---|---|---|---|
| 1309 | Less Encounters | gameplay data | 0 / 85 | 1 | 0.667 | high / none | random_event:2/0/3 map_disappear_time 11->0; random_event:1/4/6 map_disappear_time 11->0 | none |
| 1423 | Hoods and Scarfs UP (PTF - Dynamic - with Correc | gameplay data | 2 / 79 | 3 | 0.0 | high / none | armor:420f7feb-dc22-a2ec-b2a6-e1178f8c8386 clothing2_id ->4c33164c-a49d-54a8-7; armor:42e146c8-f2d1-1db1-c44c-7482b0f307b2 clothing2_id ->42a330c3-e60 | none |
| 1460 | Merchants Have x3 Money | gameplay data | 0 / 78 | 1 | 2.0 | high / none | shop_type2item:5ef63059-322e-4e1b-abe8-926e100c770e amount 2800->8400; shop_type2item:5ef63059-322e-4e1b-abe8-926e100c770e amount 200->600 | none |
| 1308 | Less Income Pribyslavitz | gameplay data | 0 / 77 | 3 | 0.9 | high / none | new_homes_structure_tier:11 people 13->38; new_homes_modifier_effect_structure:57/10 income 70->-7 | none |
| 483 | Hoods and Scarfs UP (dynamic) | gameplay data | 0 / 54 | 2 | 0.0 | high / none | armor:420f7feb-dc22-a2ec-b2a6-e1178f8c8386 clothing2_id ->4e7dfef5-2237-7fb4-0; armor:42e146c8-f2d1-1db1-c44c-7482b0f307b2 clothing2_id ->42a330c3-e60 | none |
| 1311 | Knightly Robard and Bernard | gameplay data | 41 / 12 | 4 | 0.0 | high / none | inventory_preset2item:45ff9e32-ee90-4051-f963-1058dd4360a4 NEW row; inventory_preset2item:19d5def6-e491-43c7-ab1d-5978ac197485 NEW row | none |
| 2079 | Thin The Herd - Immersive Hunting and Realistic  | gameplay data, other game data (xml) | 2 / 47 | 3 | 0.96 | high / none | inventory_preset2item:87a65e52-dfa1-4b45-9306-0b7083f93c90 priority 0.05->1; inventory2item:a0a6a756-e204-4943-b215-543471b5cc39 amount_random_add 1-> | none |
| 129 | Equal Horse Caparisons | gameplay data | 0 / 44 | 2 | 0.524 | high / none | armor:46ee8c8f-2c9a-3002-a31e-8623e2da529d slash_def 0.26->0.9; armor:402c55d2-ae62-bf47-823f-8a5760eab7bd slash_def 0.32->0.9 | none |
| 2271 | No Horse Manes | gameplay data | 44 / 0 | 1 | 0.0 | high / none | soul:00000000-0000-0000-0000-000000035000/00000000-0000-0000-0000-000000045002//445d16d9-5798-b136-1d02-9859932ce5a4///4e33cb49-0ff2-a50b-8fac-be63bab | none |
| 837 | Easy Edit | gameplay data | 0 / 29 | 1 | 0.5 | high / none | food:5dceabb5-aef0-4bf5-b401-acbc30a44e21 nutrition_benefit -0.5->2; food:b3e363cf-8dde-4733-89a9-c468d5580d2e refresh_benefit 0.5->-2 | none |
| 1944 | Lore Of Die | gameplay data | 0 / 20 | 1 | 1.65 | high / none | pickable_item:c56c54b5-b113-41ce-a250-b4eb137909bc price 100->2300; pickable_item:045b5264-5840-43bf-90fb-d8635cd799cf price 500->3500 | none |
| 1562 | Karnages_Polearm_Rebalance 2.0 | gameplay data | 0 / 10 | 1 | 0.4 | high / none | melee_weapon:44940b6c-f1f9-4ad1-9419-b5705a88e5b0 smash_att_mod 0.05->0.5; melee_weapon:033fc7b6-17b6-486d-95cb-a22afb131be2 smash_att_mod 0.05->0.5 | none |
| 1452 | Storable Halberds | gameplay data | 2 / 7 | 1 | 0.6 | high / none | weapon_class:/9//0/0/-1/22/0/1 NEW row; weapon_class:/0/8938ac5f-35d3-44dc-8251-97df7570b672/0/0/1/23/7/0 NEW row | none |
| 2171 | No Stolen Items (PTF) | gameplay data | 8 / 0 | 1 | 0.0 | high / none | rpg_param:ItemOwnerFactionDistanceCoef1 NEW row; rpg_param:ItemOwnerFactionDistanceCoef2 NEW row | none |
| 2202 | Animals Looted Statistic Tracker - Separate from | gameplay data, scripts, engine config, UI, tex | 1 / 7 | 1 | 0.0 | high / medium | statistic:/3/184// NEW row; statistic:/3/83// ui_order 73->74 | none |
| 2022 | Restored Sabres PTF | gameplay data, textures/models/animations | 1 / 5 | 5 | 1.577 | high / medium | melee_weapon:50ef44b2-73f9-412f-bb4b-29047887a11b slash_att_mod 0.75->3.8; pickable_item:50ef44b2-73f9-412f-bb4b-29047887a11b price 302->900 | none |
| 1391 | Better Equipped Runt | gameplay data | 5 / 0 | 1 | 0.0 | high / none | armor2clothing_preset:4eee90c8-2406-357f-6d9f-8e8e4274b387/448c4755-e462-0058-b108-d5f7b2af9eb8 NEW row; armor2clothing_preset:4a946556-ee8b-ed84-ecf1 | none |
| 1093 | Fishing in Bohemia | gameplay data, scripts, UI, text | 4 / 0 | 4 | 0.0 | high / medium | item:2aef9b0a-f485-4935-be7d-7ceee381b546 NEW row; pickable_item:2aef9b0a-f485-4935-be7d-7ceee381b546 NEW row | none |
| 1984 | Sharpening Overhaul | gameplay data, scripts, textures/models/animat | 4 / 0 | 1 | 0.0 | high / low | buff:f7985d3c-dfc5-4d65-a6a9-238cefc1fa39 NEW row; buff:38e2c0a5-90b4-4e99-8d95-19e2a137ff6d NEW row | none |
| 1330 | Noble Sir Hans | gameplay data | 3 / 0 | 1 | 0.0 | high / none | armor2clothing_preset:46a124e4-481c-5880-d187-573c1d8a57b9/4a15d408-3c02-7dbe-6615-e2fbe6dca0a1 NEW row; armor2clothing_preset:4d253305-bc59-a0b0-1d6f | none |
| 1861 | Sell Damaged Items At Full Price - PTF | gameplay data | 1 / 1 | 2 | 1.0 | high / none | perk_rpg_param_override:01c3b32a-5751-4c98-b6ab-258d02370382/ItemHealthPriceStatusWeight rpg_param_value 0.85->0; perk_rpg_param_override:/ItemHealthP | none |
| 1259 | Easy Assassination | gameplay data, other game data (xml) | 0 / 1 | 1 | 4.0 | high / none | rpg_param:StealthKillProbCoefA rpg_param_value 4->20 | none |
| 1510 | Mount while encumbered | gameplay data | 0 / 1 | 1 | 5.667 | high / none | rpg_param:HorseMountMaxRelativeEncumberance rpg_param_value 1.5->10 | none |
| 1548 | Immersive Economy | gameplay data | 0 / 1 | 1 | 0.25 | high / none | rpg_param:ItemHealthPriceStatusWeight rpg_param_value 0.8->1 | none |

## D small tweak (54)

| Id | Mod | Domain | Rows (new / changed) | Tables | Median rel. | Gameplay / visual | Highlights | Risk |
|---|---|---|---|---|---|---|---|---|
| 667 | Naked Armor Fix | gameplay data | 15 / 0 | 1 | 0.0 | medium / none | soul_archetype:0/0/0 NEW row; soul_archetype:1/0/1 NEW row | none |
| 1981 | Lesser Income Pribyslavitz - Supplies Cost Patch | gameplay data | 0 / 8 | 1 | 9.5 | medium / none | new_homes_modifier_effect_structure:8/8 income -120->-2184; new_homes_modifier_effect_structure:9/8 income -80->-1740 | none |
| 1092 | Pollax replacer (Axe and Hammer head interchanga | gameplay data, textures/models/animations, tex | 0 / 2 | 2 | 0.0 | medium / high | pickable_item:3ef71c79-57c2-4f28-8f31-a091d9b78798 model weapons/long_weapons->weapons/war_hammers/; player_item:3ef71c79-57c2-4f28-8f31-a091d9b78798  | none |
| 1981 | Lesser Income Pribyslavitz - Supplies Cost Patch | gameplay data | 0 / 2 | 1 | 1.727 | low / none | new_homes_modifier_effect_structure:10/8 income -220->-650; new_homes_modifier_effect_structure:11/8 income -180->-450 | none |
| 1654 | Boots with Common Plate Chausses | gameplay data | 1 / 0 | 1 | 0.0 | low / none | clothing:55/4ec05c66-af3e-7f25-c995-3a432314c789/1/0 NEW row | none |
| 2288 | Light Armour Vambraces | gameplay data | 0 / 1 | 1 | 0.0 | medium / none | armor:4573af03-8382-d87c-93aa-5dbb6fc79698 armor_type_id 5->2 | none |
| 2369 | Fewer Tournaments | gameplay data | 0 / 1 | 1 | 0.0 | low / none | quest_objective:4/123694193 autocomplete_timeout_str 5d #WT->13d #WT | none |
| 326 | Knox's Labelled Items (XML) | other game data (xml) | 0 / 0 | 0 | 0.0 | medium / none | other game data (xml, not table rows): 9; docs: 1; lua identical to vanilla: 0 | none |
| 657 | Binoculars Zoom | scripts | 0 / 0 | 0 | 0.0 | medium / none | docs: 1; config (.cfg): 1; manifest: 1; pak (container): 1; scripts (Lua): 1; lua identical to vanilla: 0 | none |
| 800 | Volumetric Fog Shadows | other game data (xml), graphics config | 0 / 0 | 0 | 0.0 | medium / medium | config (.cfg): 2; pak (container): 2; other game data (xml, not table rows): 2; manifest: 1; lua identical to vanilla: 0 | none |
| 867 | APEX Realistic Modding Guide tweaks and fixes | engine config, graphics config | 0 / 0 | 0 | 0.0 | medium / high | config (.cfg): 3; lua identical to vanilla: 0 | none |
| 930 | Photorealistic Beauty | engine config, graphics config, post-processin | 0 / 0 | 0 | 0.0 | medium / high | reshade/ENB (shaders, presets): 174; config (.cfg): 2; lua identical to vanilla: 0 | none |
| 1045 | MORE BLOOD | other game data (xml) | 0 / 0 | 0 | 0.0 | medium / none | other game data (xml, not table rows): 2; manifest: 1; pak (container): 1; lua identical to vanilla: 0 | none |
| 1063 | Paper UI | other game data (xml), textures/models/animati | 0 / 0 | 0 | 0.0 | medium / high | textures: 83; manifest: 1; pak (container): 1; other game data (xml, not table rows): 1; lua identical to vanilla: 0 | none |
| 1227 | 30 FPS Cutscene Fix V3 | scripts | 0 / 0 | 0 | 0.0 | medium / none | scripts (Lua): 2; manifest: 1; pak (container): 1; other: 1; lua identical to vanilla: 0 | none |
| 1322 | Mutt Be Quiet | other game data (xml) | 0 / 0 | 0 | 0.0 | medium / none | manifest: 1; docs: 1; pak (container): 1; other game data (xml, not table rows): 1; lua identical to vanilla: 0 | none |
| 1327 | Weather Overhaul | other game data (xml) | 0 / 0 | 0 | 0.0 | medium / none | pak (container): 2; other game data (xml, not table rows): 2; manifest: 1; docs: 1; lua identical to vanilla: 0 | none |
| 1327 | Weather Overhaul | other game data (xml) | 0 / 0 | 0 | 0.0 | medium / none | manifest: 1; docs: 1; pak (container): 1; other game data (xml, not table rows): 1; lua identical to vanilla: 0 | none |
| 1332 | Less Headbob | scripts | 0 / 0 | 0 | 0.0 | medium / none | scripts (Lua): 1; lua identical to vanilla: 0 | none |
| 1342 | Adjusted Ultra Graphics Config | engine config, graphics config | 0 / 0 | 0 | 0.0 | medium / high | config (.cfg): 1; docs: 1; lua identical to vanilla: 0 | none |
| 1342 | Adjusted Ultra Graphics Config | engine config, graphics config | 0 / 0 | 0 | 0.0 | medium / high | config (.cfg): 1; docs: 1; lua identical to vanilla: 0 | none |
| 1355 | Better Crime Stealth Plus No Dogs | scripts | 0 / 0 | 0 | 0.0 | high / none | manifest: 1; pak (container): 1; scripts (Lua): 1; lua identical to vanilla: 0 | none |
| 1410 | Better Rain | other game data (xml), textures/models/animati | 0 / 0 | 0 | 0.0 | medium / medium | other: 967; pak (container): 5; textures: 3; config (.cfg): 1; other game data (xml, not table rows): 1; lua identical to vanilla: 0 | none |
| 1552 | See NPCs and Animals Farther (Increased NPC rend | engine config, graphics config | 0 / 0 | 0 | 0.0 | medium / high | config (.cfg): 2; docs: 1; pak (container): 1; lua identical to vanilla: 0 | none |
| 1552 | See NPCs and Animals Farther (Increased NPC rend | engine config, graphics config | 0 / 0 | 0 | 0.0 | medium / high | config (.cfg): 2; docs: 1; pak (container): 1; lua identical to vanilla: 0 | none |
| 1552 | See NPCs and Animals Farther (Increased NPC rend | engine config, graphics config | 0 / 0 | 0 | 0.0 | medium / high | config (.cfg): 2; docs: 1; pak (container): 1; lua identical to vanilla: 0 | none |
| 1561 | Karnages_KCD_user.cfg 2.0 | engine config, graphics config | 0 / 0 | 0 | 0.0 | medium / high | docs: 1; config (.cfg): 1; lua identical to vanilla: 0 | none |
| 1625 | MadHUDAutoHideHUDRebornEdition | other game data (xml), text | 0 / 0 | 0 | 0.0 | medium / low | localization: 9; other game data (xml, not table rows): 2; manifest: 1; pak (container): 1; lua identical to vanilla: 0 | none |
| 1646 | AutoLimitFPS | scripts | 0 / 0 | 0 | 0.0 | high / none | scripts (Lua): 6; other: 2; manifest: 1; pak (container): 1; lua identical to vanilla: 0 | none |
| 1667 | Surface Type Rework | other game data (xml) | 0 / 0 | 0 | 0.0 | medium / none | manifest: 1; pak (container): 1; other game data (xml, not table rows): 1; lua identical to vanilla: 0 | none |
| 1691 | zzz_Clean_Items_In_Trough.pak | other game data (xml) | 0 / 0 | 0 | 0.0 | medium / none | pak (container): 1; other game data (xml, not table rows): 1; lua identical to vanilla: 0 | none |
| 1720 | Performance Configuration (Mid-High End) | engine config, graphics config | 0 / 0 | 0 | 0.0 | medium / high | config (.cfg): 1; lua identical to vanilla: 0 | none |
| 1732 | Torch Radius | other game data (xml) | 0 / 0 | 0 | 0.0 | medium / none | manifest: 1; pak (container): 1; other game data (xml, not table rows): 1; lua identical to vanilla: 0 | none |
| 1779 | Semi Sorted soul XML | other game data (xml) | 0 / 0 | 0 | 0.0 | medium / none | other game data (xml, not table rows): 1; lua identical to vanilla: 0 | none |
| 1823 | RTX 3050 PACK | other game data (xml), engine config, graphics | 0 / 0 | 0 | 0.0 | medium / high | other game data (xml, not table rows): 1; config (.cfg): 1; docs: 1; lua identical to vanilla: 0 | none |
| 1823 | RTX 3050 PACK | other game data (xml), engine config, graphics | 0 / 0 | 0 | 0.0 | medium / high | other game data (xml, not table rows): 1; config (.cfg): 1; docs: 1; lua identical to vanilla: 0 | none |
| 1958 | Selected Immersion Breaking Music Mute | other game data (xml) | 0 / 0 | 0 | 0.0 | medium / none | manifest: 1; pak (container): 1; other game data (xml, not table rows): 1; lua identical to vanilla: 0 | none |
| 1972 | FINAL Beyond SUPER Ultra Graphics and Visuals Co | engine config, graphics config | 0 / 0 | 0 | 0.0 | medium / high | config (.cfg): 2; lua identical to vanilla: 0 | none |
| 1982 | Stormy Skies | other game data (xml), textures/models/animati | 0 / 0 | 0 | 0.0 | medium / medium | textures: 4; other game data (xml, not table rows): 2; docs: 1; lua identical to vanilla: 0 | none |
| 2084 | Mount  Horse - Torch Toggle Keys | other game data (xml), text | 0 / 0 | 0 | 0.0 | medium / low | localization: 7; pak (container): 1; other game data (xml, not table rows): 1; lua identical to vanilla: 0 | none |
| 2106 | High FPS FX (KCD1) | other game data (xml) | 0 / 0 | 0 | 0.0 | medium / none | other game data (xml, not table rows): 8; manifest: 1; pak (container): 1; lua identical to vanilla: 0 | none |
| 2106 | High FPS FX (KCD1) | other game data (xml) | 0 / 0 | 0 | 0.0 | medium / none | other game data (xml, not table rows): 8; manifest: 1; pak (container): 1; lua identical to vanilla: 0 | none |
| 2153 | Engine Tweaks KCD 2.0 - user.cfg details | engine config, graphics config | 0 / 0 | 0 | 0.0 | medium / high | config (.cfg): 1; lua identical to vanilla: 0 | none |
| 2175 | Enhanced Color Grading | scripts, textures/models/animations, UI | 0 / 0 | 0 | 0.0 | medium / medium | manifest: 1; pak (container): 1; textures: 1; ui: 1; scripts (Lua): 1; lua identical to vanilla: 0 | none |
| 2190 | ENHANCED Bohemian Redux  and FX Overhaul | scripts, other game data (xml), graphics confi | 0 / 0 | 0 | 0.0 | medium / high | textures: 25; models/animations/materials: 5; other game data (xml, not table rows): 4; config (.cfg): 1; manifest: 1; pak (container): 1; scripts (Lu | none |
| 2191 | Realistic Footprints v2.0 KCD I | other game data (xml), textures/models/animati | 0 / 0 | 0 | 0.0 | medium / high | textures: 12; models/animations/materials: 7; other game data (xml, not table rows): 5; manifest: 1; pak (container): 1; lua identical to vanilla: 0 | none |
| 2206 | Rivers of Blood KCD I HD v2.0 | other game data (xml), textures/models/animati | 0 / 0 | 0 | 0.0 | medium / high | textures: 8; models/animations/materials: 4; other game data (xml, not table rows): 3; manifest: 1; pak (container): 1; lua identical to vanilla: 0 | none |
| 2223 | Stop Looking Up On Horseback | engine config | 0 / 0 | 0 | 0.0 | none / none | config (.cfg): 1; lua identical to vanilla: 0 | none |
| 2224 | More Realistic Horse Handling | engine config | 0 / 0 | 0 | 0.0 | none / none | config (.cfg): 1; lua identical to vanilla: 0 | none |
| 2243 | Performance Tweaks and best visuals | engine config, graphics config | 0 / 0 | 0 | 0.0 | medium / high | config (.cfg): 1; lua identical to vanilla: 0 | none |
| 2243 | Performance Tweaks and best visuals | engine config, graphics config | 0 / 0 | 0 | 0.0 | medium / high | config (.cfg): 1; lua identical to vanilla: 0 | none |
| 2313 | Reshield From Torch | scripts | 0 / 0 | 0 | 0.0 | high / none | manifest: 1; pak (container): 1; scripts (Lua): 1; lua identical to vanilla: 0 | none |
| 2333 | Homecoming - Runt Fight Redux | other game data (xml) | 0 / 0 | 0 | 0.0 | medium / none | manifest: 1; docs: 1; pak (container): 1; other game data (xml, not table rows): 1; lua identical to vanilla: 0 | none |
| 2353 | Ultimate Graphics Adjustment | engine config, graphics config | 0 / 0 | 0 | 0.0 | medium / high | config (.cfg): 1; lua identical to vanilla: 0 | none |

## E visual, audio or UI only (no gameplay change) (65)

| Id | Mod | Domain | Rows (new / changed) | Tables | Median rel. | Gameplay / visual | Highlights | Risk |
|---|---|---|---|---|---|---|---|---|
| 28 | No Helmet Vision | textures/models/animations, UI | 0 / 0 | 0 | 0.0 | low / medium | textures: 9; manifest: 1; pak (container): 1; ui: 1; lua identical to vanilla: 0 | none |
| 387 | Ambient_Occlusion_Fix_user_v1.07-387-1-07.7z | graphics config | 0 / 0 | 0 | 0.0 | medium / high | config (.cfg): 1; lua identical to vanilla: 0 | none |
| 392 | Sky Fix 1.2-392-1-2.rar | textures/models/animations | 0 / 0 | 0 | 0.0 | low / low | textures: 1; lua identical to vanilla: 0 | none |
| 392 | Sky and Grass Fix 1.2-392-1-2.rar | textures/models/animations | 0 / 0 | 0 | 0.0 | low / low | textures: 1; lua identical to vanilla: 0 | none |
| 611 | Dice.pak | textures/models/animations | 0 / 0 | 0 | 0.0 | low / high | textures: 28; models/animations/materials: 7; pak (container): 1; lua identical to vanilla: 0 | none |
| 660 | Apex ENB-660-2-2-1590351047.7z | post-processing (ReShade/ENB) | 0 / 0 | 0 | 0.0 | none / high | reshade/ENB (shaders, presets): 19; lua identical to vanilla: 0 | none |
| 660 | Apex ENB-660-2-2-1590351047.7z | post-processing (ReShade/ENB) | 0 / 0 | 0 | 0.0 | none / high | reshade/ENB (shaders, presets): 19; lua identical to vanilla: 0 | none |
| 754 | Painted Lords of Leipa Hounskull | textures/models/animations | 0 / 0 | 0 | 0.0 | low / low | textures: 2; pak (container): 1; lua identical to vanilla: 0 | none |
| 844 | Yet Another (Realistic) Reshade | post-processing (ReShade/ENB) | 0 / 0 | 0 | 0.0 | none / high | reshade/ENB (shaders, presets): 48; other: 1; lua identical to vanilla: 0 | none |
| 879 | Original clouds KCD no mipmap | textures/models/animations | 0 / 0 | 0 | 0.0 | low / high | textures: 39; other: 10; docs: 1; pak (container): 1; lua identical to vanilla: 0 | none |
| 922 | Enhanced Hair Textures | textures/models/animations | 0 / 0 | 0 | 0.0 | low / high | textures: 25; models/animations/materials: 5; docs: 1; manifest: 1; pak (container): 1; lua identical to vanilla: 0 | none |
| 955 | Treasure Maps Of Bohemia | textures/models/animations | 0 / 0 | 0 | 0.0 | low / high | textures: 66; manifest: 1; pak (container): 1; lua identical to vanilla: 0 | none |
| 957 | Dark Souls Death Screen | UI | 0 / 0 | 0 | 0.0 | none / medium | docs: 1; manifest: 1; pak (container): 1; ui: 1; lua identical to vanilla: 0 | none |
| 969 | Enhanced Eyes | textures/models/animations | 0 / 0 | 0 | 0.0 | low / high | models/animations/materials: 28; textures: 2; manifest: 1; pak (container): 1; lua identical to vanilla: 0 | none |
| 975 | Super Natural Reshade | post-processing (ReShade/ENB) | 0 / 0 | 0 | 0.0 | none / high | reshade/ENB (shaders, presets): 1; lua identical to vanilla: 0 | none |
| 978 | minimalistic HUD | textures/models/animations | 0 / 0 | 0 | 0.0 | low / medium | textures: 4; manifest: 1; pak (container): 1; lua identical to vanilla: 0 | none |
| 994 | Depth ReShade | post-processing (ReShade/ENB) | 0 / 0 | 0 | 0.0 | none / high | reshade/ENB (shaders, presets): 1; lua identical to vanilla: 0 | none |
| 1059 | Icon ID Resource | textures/models/animations | 0 / 0 | 0 | 0.0 | low / medium | textures: 3; lua identical to vanilla: 0 | none |
| 1080 | ReformationFX Reshade | post-processing (ReShade/ENB) | 0 / 0 | 0 | 0.0 | none / high | reshade/ENB (shaders, presets): 1; lua identical to vanilla: 0 | none |
| 1107 | Blood and Steel with NO FPS LOSS | post-processing (ReShade/ENB) | 0 / 0 | 0 | 0.0 | none / high | reshade/ENB (shaders, presets): 10; lua identical to vanilla: 0 | none |
| 1114 | Snow Mod | textures/models/animations | 0 / 0 | 0 | 0.0 | low / high | textures: 257; pak (container): 4; manifest: 1; ini (text settings): 1; other: 1; lua identical to vanilla: 0 | none |
| 1196 | Better graphics reshade | post-processing (ReShade/ENB) | 0 / 0 | 0 | 0.0 | none / high | reshade/ENB (shaders, presets): 1; lua identical to vanilla: 0 | none |
| 1197 | Proper Cyrillic Fonts | UI | 0 / 0 | 0 | 0.0 | none / medium | ui: 2; manifest: 1; pak (container): 1; lua identical to vanilla: 0 | none |
| 1218 | Lartigue's Upscale Project 2.0 - Upscaled UI and | textures/models/animations | 0 / 0 | 0 | 0.0 | low / high | textures: 945; manifest: 1; other: 1; lua identical to vanilla: 0 | MEDIUM |
| 1218 | Lartigue's Upscale Project 2.0 - Upscaled UI and | textures/models/animations | 0 / 0 | 0 | 0.0 | low / high | textures: 945; manifest: 1; other: 1; pak (container): 1; lua identical to vanilla: 0 | none |
| 1256 | Horus 2.0 KCD Reshade Preset | post-processing (ReShade/ENB) | 0 / 0 | 0 | 0.0 | none / high | reshade/ENB (shaders, presets): 1; lua identical to vanilla: 0 | none |
| 1258 | vShade for GShade Realistic Graphic Preset | post-processing (ReShade/ENB) | 0 / 0 | 0 | 0.0 | none / high | reshade/ENB (shaders, presets): 1; lua identical to vanilla: 0 | none |
| 1283 | KINGDOM CINEMATIC ReShade | post-processing (ReShade/ENB) | 0 / 0 | 0 | 0.0 | none / high | reshade/ENB (shaders, presets): 1; lua identical to vanilla: 0 | none |
| 1291 | Eye Candy Reshade | post-processing (ReShade/ENB) | 0 / 0 | 0 | 0.0 | none / high | reshade/ENB (shaders, presets): 1; lua identical to vanilla: 0 | none |
| 1337 | Helmet Vision | textures/models/animations, UI | 0 / 0 | 0 | 0.0 | low / medium | textures: 9; manifest: 1; pak (container): 1; ui: 1; lua identical to vanilla: 0 | none |
| 1349 | Natural Reshade | post-processing (ReShade/ENB) | 0 / 0 | 0 | 0.0 | none / high | reshade/ENB (shaders, presets): 48; lua identical to vanilla: 0 | none |
| 1373 | Custom UI Loading progress | textures/models/animations | 0 / 0 | 0 | 0.0 | low / medium | textures: 5; manifest: 1; pak (container): 1; lua identical to vanilla: 0 | none |
| 1414 | Real Life Kingdom Come Experience Reshade | post-processing (ReShade/ENB) | 0 / 0 | 0 | 0.0 | none / high | reshade/ENB (shaders, presets): 1; lua identical to vanilla: 0 | none |
| 1485 | SOLID HELMET VISORS | textures/models/animations | 0 / 0 | 0 | 0.0 | low / high | textures: 52; manifest: 3; pak (container): 3; docs: 1; lua identical to vanilla: 0 | none |
| 1511 | JSCR - Just simple custom Reshade | post-processing (ReShade/ENB) | 0 / 0 | 0 | 0.0 | none / high | reshade/ENB (shaders, presets): 133; lua identical to vanilla: 0 | none |
| 1544 | Summertime Reshade for Kindom Come | post-processing (ReShade/ENB) | 0 / 0 | 0 | 0.0 | none / high | reshade/ENB (shaders, presets): 1; lua identical to vanilla: 0 | none |
| 1570 | Karnages_Inventory_Recolour | textures/models/animations | 0 / 0 | 0 | 0.0 | low / medium | textures: 13; manifest: 1; pak (container): 1; lua identical to vanilla: 0 | none |
| 1577 | Invisible hands FIX (UPDATE) | textures/models/animations | 0 / 0 | 0 | 0.0 | low / low | manifest: 1; pak (container): 1; textures: 1; lua identical to vanilla: 0 | none |
| 1589 | Realistic Colour Correction Kingdom Come Deliver | post-processing (ReShade/ENB) | 0 / 0 | 0 | 0.0 | none / high | other: 1; reshade/ENB (shaders, presets): 1; lua identical to vanilla: 0 | none |
| 1618 | HD Clock Retexture - Inventory Clock Updated | textures/models/animations | 0 / 0 | 0 | 0.0 | low / low | textures: 2; manifest: 1; pak (container): 1; lua identical to vanilla: 0 | none |
| 1723 | Intimidation Stat In Inventory | UI | 0 / 0 | 0 | 0.0 | none / medium | manifest: 1; other: 1; ui: 1; lua identical to vanilla: 0 | MEDIUM |
| 1800 | KCD 2 Reshade | post-processing (ReShade/ENB) | 0 / 0 | 0 | 0.0 | none / high | reshade/ENB (shaders, presets): 1; lua identical to vanilla: 0 | none |
| 1875 | KCD1 Enhanced Visuals - UBER Graphics ReShade | post-processing (ReShade/ENB) | 0 / 0 | 0 | 0.0 | none / high | reshade/ENB (shaders, presets): 2; lua identical to vanilla: 0 | none |
| 1900 | Jiggle Physics | textures/models/animations | 0 / 0 | 0 | 0.0 | low / high | models/animations/materials: 12; pak (container): 2; manifest: 1; lua identical to vanilla: 0 | none |
| 1907 | Visorless Helmets | textures/models/animations | 0 / 0 | 0 | 0.0 | low / medium | pak (container): 5; textures: 5; manifest: 1; lua identical to vanilla: 0 | none |
| 1918 | KCD1 Reborn - Verdant Vegetation | textures/models/animations | 0 / 0 | 0 | 0.0 | low / high | textures: 66; manifest: 1; pak (container): 1; lua identical to vanilla: 0 | none |
| 1927 | KCD1 Reborn-Terrain and Structures | textures/models/animations | 0 / 0 | 0 | 0.0 | low / high | textures: 196; manifest: 1; pak (container): 1; lua identical to vanilla: 0 | none |
| 1961 | Unconscious Crime UI | textures/models/animations | 0 / 0 | 0 | 0.0 | low / low | textures: 2; manifest: 1; pak (container): 1; lua identical to vanilla: 0 | none |
| 1964 | KCD1 Reborn - Enhanced Faces and Skin | textures/models/animations | 0 / 0 | 0 | 0.0 | low / high | textures: 155; manifest: 1; pak (container): 1; lua identical to vanilla: 0 | none |
| 1980 | Medieval Loading Screens | textures/models/animations, UI | 0 / 0 | 0 | 0.0 | low / high | textures: 23; manifest: 1; pak (container): 1; ui: 1; lua identical to vanilla: 0 | none |
| 2008 | Perfection | post-processing (ReShade/ENB) | 0 / 0 | 0 | 0.0 | none / high | reshade/ENB (shaders, presets): 69; lua identical to vanilla: 0 | MEDIUM |
| 2030 | Clean and Minimal HUD and Map | textures/models/animations | 0 / 0 | 0 | 0.0 | low / high | textures: 97; manifest: 1; pak (container): 1; lua identical to vanilla: 0 | none |
| 2031 | Mud and Iron Kingdom Come Deliverance Reshade | post-processing (ReShade/ENB) | 0 / 0 | 0 | 0.0 | none / high | reshade/ENB (shaders, presets): 1; lua identical to vanilla: 0 | none |
| 2031 | Mud and Iron Kingdom Come Deliverance Reshade | post-processing (ReShade/ENB) | 0 / 0 | 0 | 0.0 | none / high | reshade/ENB (shaders, presets): 1; lua identical to vanilla: 0 | none |
| 2103 | Pickpocket menu  from KCD2 | textures/models/animations, UI | 0 / 0 | 0 | 0.0 | low / medium | textures: 11; manifest: 1; pak (container): 1; ui: 1; lua identical to vanilla: 0 | none |
| 2108 | New KCD HUD 2.0 | textures/models/animations, UI | 0 / 0 | 0 | 0.0 | low / medium | textures: 15; manifest: 1; pak (container): 1; ui: 1; lua identical to vanilla: 0 | none |
| 2152 | Lighting and Shadow 2.0 - ENB for KCD | post-processing (ReShade/ENB) | 0 / 0 | 0 | 0.0 | none / high | reshade/ENB (shaders, presets): 16; lua identical to vanilla: 0 | none |
| 2196 | ENHANCED Adult Bounce KCD I | textures/models/animations | 0 / 0 | 0 | 0.0 | low / high | models/animations/materials: 12; manifest: 1; pak (container): 1; lua identical to vanilla: 0 | none |
| 2199 | DualSense Buttons | textures/models/animations | 0 / 0 | 0 | 0.0 | low / high | textures: 23; manifest: 1; pak (container): 1; lua identical to vanilla: 0 | none |
| 2293 | Bigger Hud (KCD1) | UI | 0 / 0 | 0 | 0.0 | none / medium | ui: 2; manifest: 1; pak (container): 1; lua identical to vanilla: 0 | none |
| 2297 | Ultimate Loadingscreen Artwork Overhaul | textures/models/animations, UI | 0 / 0 | 0 | 0.0 | low / high | textures: 44; manifest: 1; pak (container): 1; ui: 1; lua identical to vanilla: 0 | none |
| 2317 | Enemy Health Bar | UI | 0 / 0 | 0 | 0.0 | none / medium | manifest: 1; pak (container): 1; ui: 1; lua identical to vanilla: 0 | none |
| 2330 | Compass and Map Upgrades - Wayfinder | UI | 0 / 0 | 0 | 0.0 | none / medium | ui: 9; manifest: 1; docs: 1; pak (container): 1; lua identical to vanilla: 0 | none |
| 2349 | KCD1 Map Cursor Contrast - Visible Ring and X | textures/models/animations | 0 / 0 | 0 | 0.0 | low / low | manifest: 1; docs: 1; pak (container): 1; textures: 1; lua identical to vanilla: 0 | none |
| 2384 | KCD HI-Res Maps | textures/models/animations | 0 / 0 | 0 | 0.0 | low / medium | textures: 18; lua identical to vanilla: 0 | none |

## E text only (no gameplay change) (5)

| Id | Mod | Domain | Rows (new / changed) | Tables | Median rel. | Gameplay / visual | Highlights | Risk |
|---|---|---|---|---|---|---|---|---|
| 797 | Inventoried | text | 0 / 0 | 0 | 0.0 | low / low | localization: 2; manifest: 1; lua identical to vanilla: 0 | none |
| 1780 | Timed Quest Indicator | text | 0 / 0 | 0 | 0.0 | low / low | localization: 4; manifest: 2; docs: 1; lua identical to vanilla: 0 | none |
| 1944 | Lore Of Die | text | 0 / 0 | 0 | 0.0 | low / low | localization: 2; manifest: 1; lua identical to vanilla: 0 | none |
| 2005 | Snarky Loading Screens PTF Edition | text | 0 / 0 | 0 | 0.0 | low / low | localization: 2; manifest: 1; lua identical to vanilla: 0 | none |
| 2100 | Diseases - spolszczenie | text | 0 / 0 | 0 | 0.0 | low / low | localization: 2; lua identical to vanilla: 0 | none |

## E non-perceptive to gameplay (no effective change found) (14)

| Id | Mod | Domain | Rows (new / changed) | Tables | Median rel. | Gameplay / visual | Highlights | Risk |
|---|---|---|---|---|---|---|---|---|
| 266 | All Referenced Strings In Kingdom Come Deliveran | none | 0 / 0 | 0 | 0.0 | none / none | docs: 1; lua identical to vanilla: 0 | none |
| 502 | zzzz_JCD_CLAM | none | 0 / 0 | 0 | 0.0 | none / none | docs: 2; config (.cfg): 1; manifest: 1; pak (container): 1; localization: 1; lua identical to vanilla: 0 | none |
| 1367 | Apostalus User Configs | none | 0 / 0 | 0 | 0.0 | none / none | manifest: 1; other: 1; lua identical to vanilla: 0 | none |
| 1479 | Batch files for all items sorted and easy to rea | none | 0 / 0 | 0 | 0.0 | none / none | docs: 18; lua identical to vanilla: 0 | none |
| 1526 | Force High Quality Trees in the distance | none | 0 / 0 | 0 | 0.0 | none / none | config (.cfg): 3; docs: 1; lua identical to vanilla: 0 | none |
| 1528 | Enchanced Shadows and Shadow Cascades | none | 0 / 0 | 0 | 0.0 | none / none | config (.cfg): 2; docs: 1; lua identical to vanilla: 0 | none |
| 1538 | Batch's Ultra Graphics Settings | none | 0 / 0 | 0 | 0.0 | none / none | config (.cfg): 2; docs: 1; lua identical to vanilla: 0 | none |
| 1538 | Batch's Ultra Graphics Settings | none | 0 / 0 | 0 | 0.0 | none / none | config (.cfg): 2; docs: 1; lua identical to vanilla: 0 | none |
| 2132 | MOD file override conflicts and PTF patch detect | none | 0 / 0 | 0 | 0.0 | none / none | docs: 1; lua identical to vanilla: 0 | none |
| 2180 | Optimized CryEngine simple tweaks | none | 0 / 0 | 0 | 0.0 | none / none | docs: 1; lua identical to vanilla: 0 | none |
| 2216 | KCD Mod Organizer Plugin (Steam - GOG - Epic) | none | 0 / 0 | 0 | 0.0 | none / none | other: 1; lua identical to vanilla: 0 | HIGH |
| 2273 | Address Library For KCSE | none | 0 / 0 | 0 | 0.0 | none / none | other: 3; lua identical to vanilla: 0 | none |
| 2351 | Keyboard Controls | none | 0 / 0 | 0 | 0.0 | none / none | other: 1; lua identical to vanilla: 0 | none |
| 2367 | Pray Animation KCD1 | none | 0 / 0 | 0 | 0.0 | none / none | docs: 1; lua identical to vanilla: 0 | none |

## X not analysed (2)

| Id | Mod | Domain | Rows (new / changed) | Tables | Median rel. | Gameplay / visual | Highlights | Risk |
|---|---|---|---|---|---|---|---|---|
| 1568 | Karnages_Shop_Prices | none | 0 / 0 | 0 | 0.0 | unknown / none | manifest: 1; pak (container): 1; lua identical to vanilla: 0 | none |
| 1683 | Roads Are Dangerous - Redux | none | 0 / 0 | 0 | 0.0 | unknown / none | manifest: 1; pak (container): 1; lua identical to vanilla: 0 | none |

## Overlap between the analysed mods

4751 table rows are changed by two or more of the 208 mods (`mod_overlap.csv`). Most contested: shop_type2item:5ef63059-322e-4e1b-abe8-926e100c770e (6 mods); melee_weapon:3ef71c79-57c2-4f28-8f31-a091d9b78798 (6 mods); melee_weapon:cf58c28c-f2bd-41a0-9c6d-764767d144cf (6 mods); melee_weapon:8ef902ea-0c32-44c9-b101-71f35b9cbe3d (6 mods); melee_weapon:1f389792-6ddb-4060-8cc4-13bcc9117db8 (6 mods); melee_weapon:f2817f34-9e28-4b97-8f6c-d2b2a7aaa61b (6 mods); melee_weapon:0f5be0ac-ff11-4a01-a7f4-bf8e84c2e31b (6 mods); melee_weapon:033fc7b6-17b6-486d-95cb-a22afb131be2 (6 mods).

Pairs of mods that change the most rows in common (rows shared by 2 to 8 mods; the later one in load order wins each row):

| Mod A | Mod B | Shared rows |
|---|---|---|
| 726 Early Bird NPC Schedules | 840 Blood and Iron Encounter System | 2390 |
| 726 Early Bird NPC Schedules | 2061 Meticulously Edited Shops and Services | 2390 |
| 840 Blood and Iron Encounter System | 2061 Meticulously Edited Shops and Services | 2390 |
| 829 Shop Proper | 2061 Meticulously Edited Shops and Services | 532 |
| 2203 Categorized Sorted Inventory | 2204 A Real Sorted Inventory (ARSI) | 425 |
| 1636 More Sensible Weapons and Armor | 2358 MatthusTweaksKCDarmwea | 333 |
| 1153 More historically accurate item stats | 2358 MatthusTweaksKCDarmwea | 322 |
| 1636 More Sensible Weapons and Armor | 2158 Finders Keepers | 247 |
| 1153 More historically accurate item stats | 1636 More Sensible Weapons and Armor | 234 |
| 2046 Arsenal - A Weapons Overhaul - DDDB | 2358 MatthusTweaksKCDarmwea | 213 |
| 950 Henry's Castle at Pribyslavits | 1356 Fan Side Quest - Heritage | 163 |
| 829 Shop Proper | 2279 Immersive Economy FIXED | 154 |
| 1870 Fair Trade - PTF | 2279 Immersive Economy FIXED | 133 |
| 829 Shop Proper | 1870 Fair Trade - PTF | 124 |
| 977 Alms for Beggars | 1356 Fan Side Quest - Heritage | 112 |

3 archives change rows that a KRS module also sets (the later mod in load order wins the whole row): 554, 796, 837.

## Needs something outside the game files

106 (autoexec.cfg, states requirements); 491 (unpack); 502 (unpack); 657 (user.cfg); 771 (states requirements, user.cfg); 771 (states requirements, user.cfg); 829 (states requirements); 892 (states requirements); 1046 (ReShade, user.cfg); 1314 (ReShade, user.cfg); 1342 (autoexec.cfg); 1342 (autoexec.cfg); 1356 (states requirements, unpack); 1428 (ReShade); 1526 (autoexec.cfg); 1527 (ReShade, autoexec.cfg); 1528 (autoexec.cfg); 1538 (autoexec.cfg); 1538 (autoexec.cfg); 1561 (user.cfg); 1603 (ReShade); 1702 (ReShade, states requirements); 1777 (mentions Tables.pak, states requirements, user.cfg); 1777 (mentions Tables.pak, states requirements, user.cfg); 1807 (mentions Tables.pak); 1823 (autoexec.cfg); 1823 (autoexec.cfg); 1982 (unpack); 2079 (states requirements); 2202 (mentions Tables.pak); 2261 (ASI loader); 2333 (states requirements); 2349 (Vortex); 2383 (Vortex)
