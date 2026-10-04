# Mod profiles: P3/P4 and unlisted (generated)

> **GENERATED** by `tools/audit_mods_deep.py`: do not edit | **Kind:** review | **Trust:** archives read statically (listed, extracted to a scratch folder, read, deleted); nothing was installed or run | **Game version:** 1.9.8

One section per archive of the P3/P4 and unlisted mods, best first by grade. What it changes, how it is installed, where the data lives, how much it changes (against the vanilla tables), what it needs, and the risk result. See [`MOD_ANALYSIS_P3_P4.md`](MOD_ANALYSIS_P3_P4.md) for the grading rules.

## 2061 Meticulously Edited Shops and Services (P3, Economy / merchants)

- **What the author says (Nexus summary):** Edits shop_type2item.xml and soul.xml (randomized vendor stock, hours, gold); requires all DLC; conflicts with mods that change soul.xml or shops (Early Bird patches soul) Overhauls vendors, mostly by expanding their inventories and then randomizing what's for sale. Later, I want to include separate
- **File:** `Meticulously Edited Shops (and Services)-2061-0-4-4-1771229823.zip` (archive, 0.89 MB, `c_economy-merchants`), full (scratch, deleted after reading)
- **Grade:** A changes the most | **gameplay perceptibility:** high | **visual/audio impact:** none | **layers:** D1 data tables (PTF) | **domain:** gameplay data
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `1.9.4 1.9.5 1.9.6 1.9.7`, loads on 1.9.8: NO (disabled: lists 1.9.4, 1.9.5, 1.9.6, 1.9.7)
- **Where it changes things:** tables (PTF): 3; other: 2; docs: 1; manifest: 1; pak (container): 1; lua identical to vanilla: 0
- **Tables:** shop, shop_type2item, soul (1449 new rows, 6013 changed, 2891 identical to vanilla, 49 vanilla rows dropped by a whole-table replace); median relative change 0.943
- **Largest changes:** shop_type2item:00000000-0000-0000-0000-00000000001b amount 3->100; shop_type2item:22eb16a0-1175-4e2e-a951-33d362e288fb amount 1->100; shop_type2item:ddb0fc96-be22-42d8-ba8c-ff00b68c0481 amount 2->100; shop_type2item:4cea28a0-0814-405a-bf24-4fd711f7eb63 amount 5->10.86; shop_type2item:44414acf-f175-7e9b-3af0-57f2b339aa90 NEW row; shop_type2item:453ea77f-9f5a-dfb5-1934-f18e44ab08a0 NEW row; shop_type2item:4472ab5e-def2-e154-34a3-15349c976283 NEW row; shop_type2item:44dd60cb-a67f-395f-a6a2-25feeceadd99 NEW row
- **Problems:** MESS/Data/MESS.pak!Libs/Tables/shop/shop.xml: no suffix: replaces the whole vanilla table / MESS/Data/MESS.pak!Libs/Tables/shop/shop_type2item.xml: no suffix: replaces the whole vanilla table
- **Risk:** none

## 840 Blood and Iron Encounter System (P3, Quests / lore / content)

- **What the author says (Nexus summary):** The encounter system from Blood and Iron Overhaul as a stand-alone mod.
- **File:** `Blood and Iron Encounter System-840-1-0-1567464422.7z` (archive, 0.77 MB, `c_quests-lore-content`), full (scratch, deleted after reading)
- **Grade:** A changes the most | **gameplay perceptibility:** high | **visual/audio impact:** none | **layers:** D1 data tables (PTF) | **domain:** gameplay data
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `(none)`, loads on 1.9.8: yes (no version restriction)
- **Where it changes things:** other: 2; tables (PTF): 2; manifest: 1; pak (container): 1; lua identical to vanilla: 0
- **Tables:** random_event, soul (0 new rows, 5081 changed, 29 identical to vanilla); median relative change 0.647
- **Largest changes:** random_event:0/5/5 base_run_chance 0.07->0.5; random_event:0/68/7 base_run_chance 0.15->0.4; random_event:0/9/8 base_run_chance 0.2->0.5; random_event:0/67/7 base_run_chance 0.1->0.25; random_event:0/111/7 base_run_chance 0.1->0.25; random_event:0/112/7 base_run_chance 0.1->0.25; random_event:0/113/7 base_run_chance 0.1->0.25; random_event:0/114/7 base_run_chance 0.1->0.25
- **Problems:** Blood and Iron Encounter System/Data/BIO Encounter System.pak!Libs/Tables/random_event.xml: no suffix: replaces the whole vanilla table / Blood and Iron Encounter System/Data/BIO Encounter System.pak!Libs/Tables/rpg/soul.xml: no suffix: replaces the whole vanilla table
- **Risk:** none

## 808 Named NPCs (P3, Quests / lore / content)

- **What the author says (Nexus summary):** Adds proper names to the NPCs of Kingdom Come Deliverance.
- **File:** `Named NPCs (BIO version) 1.4-808-1-4-1568060707.7z` (archive, 0.19 MB, `c_quests-lore-content`), full (scratch, deleted after reading)
- **Grade:** A changes the most | **gameplay perceptibility:** high | **visual/audio impact:** low | **layers:** D0 content/text; D1 data tables (PTF) | **domain:** gameplay data, text
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `(none)`, loads on 1.9.8: yes (no version restriction)
- **Where it changes things:** localization: 2; manifest: 1; pak (container): 1; other: 1; tables (PTF): 1; lua identical to vanilla: 0
- **Tables:** v_soul_character_data (3263 new rows, 0 changed, 1762 identical to vanilla, 3263 vanilla rows dropped by a whole-table replace); median relative change 0.0
- **Largest changes:** v_soul_character_data:soul_ui_name_armorer_001/4203d715-43a1-0049-e26b-8579c81ce0b0/0 NEW row; v_soul_character_data:soul_ui_name_armorer_002/4618f1c3-240c-52fb-eb00-97d3179c56af/105 NEW row; v_soul_character_data:soul_ui_name_armorer_003/47a70946-4377-2716-ba39-0ddcc7becc9c/0 NEW row; v_soul_character_data:soul_ui_name_armorer_004/47ecc7dc-f8aa-f615-7599-b079bcec6ea1/76 NEW row; v_soul_character_data:soul_ui_name_bailiff_001/413b78e1-9650-a4f7-979e-ff7afbb576a8/0 NEW row; v_soul_character_data:soul_ui_name_bailiff_002/4161c2ed-8426-3257-d2df-0380d9ee6886/81 NEW row; v_soul_character_data:soul_ui_name_bailiff_003/424f8832-7d19-26e8-c9cc-d6fbe9597bbf/98 NEW row; v_soul_character_data:soul_ui_
- **Text:** 185 strings changed, 2713 new
- **Problems:** zzzz_Named_NPCs_BIO_1.4/Data/More_Named_NPCs.pak!Libs/Tables/rpg/v_soul_character_data.xml: no suffix: replaces the whole vanilla table
- **Risk:** none

## 808 Named NPCs (P3, Quests / lore / content)

- **What the author says (Nexus summary):** Adds proper names to the NPCs of Kingdom Come Deliverance.
- **File:** `Named NPCs 1.4-808-1-4-1568060673.7z` (archive, 0.19 MB, `c_quests-lore-content`), full (scratch, deleted after reading)
- **Grade:** A changes the most | **gameplay perceptibility:** high | **visual/audio impact:** low | **layers:** D0 content/text; D1 data tables (PTF) | **domain:** gameplay data, text
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `(none)`, loads on 1.9.8: yes (no version restriction)
- **Where it changes things:** localization: 2; manifest: 1; pak (container): 1; other: 1; tables (PTF): 1; lua identical to vanilla: 0
- **Tables:** v_soul_character_data (3263 new rows, 0 changed, 1762 identical to vanilla, 3263 vanilla rows dropped by a whole-table replace); median relative change 0.0
- **Largest changes:** v_soul_character_data:soul_ui_name_armorer_001/4203d715-43a1-0049-e26b-8579c81ce0b0/0 NEW row; v_soul_character_data:soul_ui_name_armorer_002/4618f1c3-240c-52fb-eb00-97d3179c56af/105 NEW row; v_soul_character_data:soul_ui_name_armorer_003/47a70946-4377-2716-ba39-0ddcc7becc9c/0 NEW row; v_soul_character_data:soul_ui_name_armorer_004/47ecc7dc-f8aa-f615-7599-b079bcec6ea1/76 NEW row; v_soul_character_data:soul_ui_name_bailiff_001/413b78e1-9650-a4f7-979e-ff7afbb576a8/0 NEW row; v_soul_character_data:soul_ui_name_bailiff_002/4161c2ed-8426-3257-d2df-0380d9ee6886/81 NEW row; v_soul_character_data:soul_ui_name_bailiff_003/424f8832-7d19-26e8-c9cc-d6fbe9597bbf/98 NEW row; v_soul_character_data:soul_ui_
- **Text:** 173 strings changed, 2631 new
- **Problems:** Named_NPCs_1.4/Data/Named_NPCs_1.4.pak!Libs/Tables/rpg/v_soul_character_data.xml: no suffix: replaces the whole vanilla table
- **Risk:** none

## 726 Early Bird NPC Schedules (P3, Quests / lore / content)

- **What the author says (Nexus summary):** Changes NPC schedules so they start their days earlier and waste less daylight. NPC activities that start in the morning now start earlier, while afternoon and evening activities are only slightly altered. Monk schedules are not altered for
- **File:** `Early Bird NPC rescheduler-726-2-1-0-1640796373.7z` (archive, 0.39 MB, `c_quests-lore-content`), full (scratch, deleted after reading)
- **Grade:** A changes the most | **gameplay perceptibility:** high | **visual/audio impact:** none | **layers:** D1 data tables (PTF) | **domain:** gameplay data
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `(none)`, loads on 1.9.8: yes (no version restriction)
- **Where it changes things:** manifest: 1; pak (container): 1; tables (PTF): 1; lua identical to vanilla: 0
- **Tables:** soul (0 new rows, 2390 changed, 0 identical to vanilla, 2635 vanilla rows dropped by a whole-table replace); median relative change 0.0
- **Largest changes:** soul:00000000-0000-0000-0000-000000035000/2a7b75cd-8344-43f6-8483-0191a079e503//9fe6dae0-e195-42e0-a3fb-66cfc6382407/498bc146-f7d1-1c55-7a6b-b549cbdfb98f/4278ca1d-6a0e-4dca-0f72-e423458832bd/42265331-4b1e-4b03-98f8-ae3ecf9eb7bb/4c7f52b3-d389-602a-88a5-b32a404b20a0/4f9db3d6-9938-457f-a928-279f818b29a5/460/58/0//0249aa52-f5ac-48ea-b707-0f50c0c76c56/0 time_0 8:00->6:55; soul:00000000-0000-0000-0000-000000035000/2a7b75cd-8344-43f6-8483-0191a079e503//9fe6dae0-e195-42e0-a3fb-66cfc6382407/481bb23a-06af-86b7-934c-e87acf7f3a91/4e1a8fe6-b6ae-7130-c3f6-c113717e3b8f/45cf32d1-dfde-8035-25f4-8f19c77aee82/4d2978a2-6fef-5f59-dd06-0bb6ee2fd9b3//637/43/0//051b9554-3b3d-4b2b-a416-070fca05cc00/0 time_0 7:09->5:
- **Risk:** none

## 726 Early Bird NPC Schedules (P3, Quests / lore / content)

- **What the author says (Nexus summary):** Changes NPC schedules so they start their days earlier and waste less daylight. NPC activities that start in the morning now start earlier, while afternoon and evening activities are only slightly altered. Monk schedules are not altered for
- **File:** `earlybird.pak` (loose file, 0.4 MB, `c_quests-lore-content`), read in place
- **Grade:** A changes the most | **gameplay perceptibility:** high | **visual/audio impact:** none | **layers:** D1 data tables (PTF) | **domain:** gameplay data
- **How it installs:** loose .pak (legacy: copy into Data); manifest id `-`, supports `-`, loads on 1.9.8: no manifest (legacy install)
- **Where it changes things:** pak (container): 1; tables (PTF): 1; lua identical to vanilla: 0
- **Tables:** soul (0 new rows, 2390 changed, 0 identical to vanilla, 2635 vanilla rows dropped by a whole-table replace); median relative change 0.0
- **Largest changes:** soul:00000000-0000-0000-0000-000000035000/2a7b75cd-8344-43f6-8483-0191a079e503//9fe6dae0-e195-42e0-a3fb-66cfc6382407/498bc146-f7d1-1c55-7a6b-b549cbdfb98f/4278ca1d-6a0e-4dca-0f72-e423458832bd/42265331-4b1e-4b03-98f8-ae3ecf9eb7bb/4c7f52b3-d389-602a-88a5-b32a404b20a0/4f9db3d6-9938-457f-a928-279f818b29a5/460/58/0//0249aa52-f5ac-48ea-b707-0f50c0c76c56/0 time_0 8:00->6:55; soul:00000000-0000-0000-0000-000000035000/2a7b75cd-8344-43f6-8483-0191a079e503//9fe6dae0-e195-42e0-a3fb-66cfc6382407/481bb23a-06af-86b7-934c-e87acf7f3a91/4e1a8fe6-b6ae-7130-c3f6-c113717e3b8f/45cf32d1-dfde-8035-25f4-8f19c77aee82/4d2978a2-6fef-5f59-dd06-0bb6ee2fd9b3//637/43/0//051b9554-3b3d-4b2b-a416-070fca05cc00/0 time_0 7:09->5:
- **Risk:** none

## 2158 Finders Keepers (P3, Crime / stealth / loot)

- **What the author says (Nexus summary):** This PTF mod speeds up the time until items loose their stolen status.Versions: Wait_No or Wait_Less_2x.
- **File:** `FindersKeepers_Wait_No-2158-1-2-1773048312.zip` (archive, 0.06 MB, `c_crime-stealth-loot`), full (scratch, deleted after reading)
- **Grade:** A changes the most | **gameplay perceptibility:** high | **visual/audio impact:** none | **layers:** D1 data tables (PTF) | **domain:** gameplay data
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `1.9.*`, loads on 1.9.8: yes (wildcard)
- **Where it changes things:** manifest: 1; pak (container): 1; tables (PTF): 1; lua identical to vanilla: 0
- **Tables:** pickable_item (0 new rows, 2109 changed, 0 identical to vanilla, 101 vanilla rows dropped by a whole-table replace); median relative change 1.0
- **Largest changes:** pickable_item:00000000-0000-0000-0000-000000000005 owner_fading_coef 0.02->0; pickable_item:00000000-0000-0000-0000-00000000001b owner_fading_coef 0.02->0; pickable_item:00000000-0000-0000-0000-00000000001c owner_fading_coef 0.02->0; pickable_item:00000000-0000-0000-0000-00000000001d owner_fading_coef 0.02->0; pickable_item:00000000-0000-0000-0000-000000000020 owner_fading_coef 0.02->0; pickable_item:00000000-0000-0000-0000-000000000023 owner_fading_coef 0.02->0; pickable_item:00000000-0000-0000-0000-000000000024 owner_fading_coef 0.02->0; pickable_item:00000000-0000-0000-0000-000000000025 owner_fading_coef 0.02->0
- **Problems:** FindersKeepers_Wait_No/Data/FindersKeepers_Wait_No.pak!Libs/Tables/item/pickable_item__FindersKeepers_Wait_No.xml: suffix 'FindersKeepers_Wait_No' != id 'finders_keepers_wait_no' (the game ignores it)
- **Risk:** none

## 1356 Fan Side Quest - Heritage (P3, Maps / UI / HUD)

- **What the author says (Nexus summary):** This is a fan created Side Quest for Kingdom Come: Deliverance.Quest features English and Czech translations.(Any other localization uses English)
- **File:** `heritage_release-1356-1-2-1648922073.rar` (archive, 1.45 MB, `c_maps-ui-hud`), full (scratch, deleted after reading)
- **Grade:** A changes the most | **gameplay perceptibility:** high | **visual/audio impact:** high | **layers:** D0 content/text; D1 data tables (PTF); D1 game data xml (not table rows); D3 Lua scripts | **domain:** gameplay data, scripts, other game data (xml), textures/models/animations, text
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `heritage_release`, supports `(none)`, loads on 1.9.8: yes (no version restriction)
- **Where it changes things:** scripts (Lua): 581; lua identical to vanilla: 481; other game data (xml, not table rows): 203; other: 53; tables (PTF): 48; localization: 20; docs: 7; pak (container): 2; models/animations/materials: 2; manifest: 1
- **Tables:** ?, anim_fragment, brain, brain2subbrain, clothing_mesh_data, clothing_raycast, item, mailbox, mailbox_filter, misc, pickable_item, player_item, quest, quest2skald_subchapter, quest_asset, quest_item, quest_npc, quest_objective, quest_place, quest_reward_exp, quest_reward_money, quest_tracked_asset,  (2022 new rows, 27 changed, 0 identical to vanilla, 923492 vanilla rows dropped by a whole-table replace); median relative change 1.08
- **Largest changes:** brain2subbrain:41564e9f-2a60-8716-22ee-d87fc4f11ca5/405923ef-0846-68eb-0983-f014f5b20bb9 NEW row; brain2subbrain:4db77d1f-f7a9-fcbd-57ed-b824e6ad1c85/4141bf4f-2461-5ca1-9ec9-7bac6c4b4ea0 NEW row; brain:41564e9f-2a60-8716-22ee-d87fc4f11ca5 NEW row; brain:4db77d1f-f7a9-fcbd-57ed-b824e6ad1c85 NEW row; mailbox:4befb8bd-d42b-15b7-9999-3fc0dfe64590 NEW row; mailbox_filter:49a7118c-c7ce-eb56-02b1-04e198d387b1/4befb8bd-d42b-15b7-9999-3fc0dfe64590 NEW row; subbrain:405923ef-0846-68eb-0983-f014f5b20bb9 NEW row; subbrain:4141bf4f-2461-5ca1-9ec9-7bac6c4b4ea0 NEW row
- **Lua:** 581 files, 9643 lines; API used: player.soulx90, System.GetEntityByNamex78, player.actorx72, player.inventoryx59, entity.Propertiesx53, System.Logx36
- **Text:** 3 strings changed, 2922 new
- **Mentions:** states requirements, unpack
- **Problems:** heritage_release/data/tables_patch.pak!libs/tables/text/topictorole__heritage_release.xml: table 'TopicToRole__heritage_release' is not in the vanilla game
- **Risk:** MEDIUM: MEDIUM: Lua loadstring/loadfile/dofile in heritage_release/data/data.pak!scripts/entities/triggers/cinematictrigger.lua / MEDIUM: command or downloader string in heritage_release/data/data.pak!scripts/featuretests/found_checkpoints.csv: CScript

## 829 Shop Proper (P3, Economy / merchants)

- **What the author says (Nexus summary):** Shop proper with Shop Proper. A trader and shop overhaul mod.
- **File:** `Shop Proper-829-1-0-5-1575357704.7z` (archive, 0.06 MB, `c_economy-merchants`), full (scratch, deleted after reading)
- **Grade:** A changes the most | **gameplay perceptibility:** high | **visual/audio impact:** none | **layers:** D1 data tables (PTF) | **domain:** gameplay data
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `(none)`, loads on 1.9.8: yes (no version restriction)
- **Where it changes things:** other: 2; tables (PTF): 2; manifest: 1; docs: 1; pak (container): 1; lua identical to vanilla: 0
- **Tables:** shop, shop_type2item (282 new rows, 577 changed, 1843 identical to vanilla, 10 vanilla rows dropped by a whole-table replace); median relative change 6.866
- **Largest changes:** shop_type2item:cda856d8-9ee4-4f61-b2c7-eace8e082d62 amount 2->8; shop_type2item:9fa3000e-3807-48a8-bed8-81427f0bda55 amount 3->12; shop_type2item:9f7a0c0a-6458-4622-9cc5-2f4dd4898b50 amount 3->10; shop_type2item:4454e377-d0d8-5bbb-e968-3e41cd366899 amount 1->3; shop_type2item:4662e866-6a82-eb4b-ed98-26213ca118a8 amount 1->3; shop_type2item:486c1cda-e1ec-5d01-b1f1-1540d0863c9e amount 1->3; shop_type2item:432237ec-b13a-bd6c-4026-a3db68e4d89e amount 1->3; shop_type2item:4bdc6232-47e7-e675-3730-5d218359e3ac amount 1->3
- **Mentions:** states requirements
- **Problems:** ShopProper/data/ShopProper.pak!Libs/Tables/shop/shop.xml: no suffix: replaces the whole vanilla table / ShopProper/data/ShopProper.pak!Libs/Tables/shop/shop_type2item.xml: no suffix: replaces the whole vanilla table
- **Risk:** none

## 1636 More Sensible Weapons and Armor (P3, Weapons / armor / items)

- **What the author says (Nexus summary):** Improves armour & weapons to be more sensible, with clearer roles and more logical stats, giving many items a new lease on life while staying very close to vanilla. Ever wondered why the Cuman Harness is so bad, a "Heavy" shield is lighter
- **File:** `More Sensible Weapons and Armor-1636-1-11-1741394601.zip` (archive, 0.26 MB, `c_weapons-armor-items`), full (scratch, deleted after reading)
- **Grade:** A changes the most | **gameplay perceptibility:** high | **visual/audio impact:** none | **layers:** D1 data tables (PTF) | **domain:** gameplay data
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `1.9.*`, loads on 1.9.8: yes (wildcard)
- **Where it changes things:** tables (PTF): 7; other: 3; manifest: 1; pak (container): 1; lua identical to vanilla: 0
- **Tables:** armor, equippable_item, melee_weapon, missile_weapon, ointment_item, pickable_item, weapon (0 new rows, 822 changed, 3574 identical to vanilla); median relative change 0.333
- **Largest changes:** equippable_item:00000000-0000-0000-0000-00000000001b conspicuousness -0.02->-0.26; equippable_item:4a22fe68-b9c5-7b04-ee81-23613de682b6 conspicuousness -0.02->-0.22; equippable_item:4b82dda9-7cfe-4c26-01c7-c1322b7fc8b4 visibility -0.02->0.26; pickable_item:2b08dbc7-31bf-42fd-89ce-b840299930b5 price 10->400; pickable_item:40a2b1d3-f475-a8f3-667a-075486518b8f price 10->8500; pickable_item:41a9ea6a-eed1-471c-754a-196d368245a6 price 10->8900; pickable_item:42414d23-c8dc-7b1a-31e6-00644075feaa price 10->4700; pickable_item:42c04555-15cb-ac3a-aef4-e377a125aca5 price 10->4500
- **Risk:** none

## 2358 MatthusTweaksKCDarmwea (unlisted, (not in the 365 index))

- **What the author says (Nexus summary):** -
- **File:** `MT New Armor And Weapon System V1.0 2358 1 2026-09-11T18-39Z EfL7D0sNl.zip` (archive, 0.04 MB, `_unmatched`), full (scratch, deleted after reading)
- **Grade:** A changes the most | **gameplay perceptibility:** high | **visual/audio impact:** none | **layers:** D1 data tables (PTF) | **domain:** gameplay data
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `1.*`, loads on 1.9.8: yes (wildcard)
- **Where it changes things:** tables (PTF): 3; other: 2; manifest: 1; pak (container): 1; lua identical to vanilla: 0
- **Tables:** armor, melee_weapon, weapon (0 new rows, 537 changed, 8 identical to vanilla, 608 vanilla rows dropped by a whole-table replace); median relative change 0.316
- **Largest changes:** armor:4fec3673-04fe-45ae-b200-600704ecea70 slash_def 0.1->1.25; melee_weapon:033fc7b6-17b6-486d-95cb-a22afb131be2 smash_att_mod 0.05->0.5978261129; melee_weapon:44940b6c-f1f9-4ad1-9419-b5705a88e5b0 smash_att_mod 0.05->0.6321839008; weapon:3e1e9a1d-37b5-4564-be23-af1017296d6c max_status 1->50; melee_weapon:662a3ac5-5883-4b7d-bd84-173eaa136a73 slash_att_mod 0.05->0.538; melee_weapon:24a7c868-f23f-4799-8e64-331435a77404 stab_att_mod 0.05->0.534; armor:413806e7-f3b7-c6cf-2309-e47ce3c97fa2 slash_def 0.1->0.85; melee_weapon:9d9bdc38-9e6e-459f-8a75-700fdc1e604f stab_att_mod 0.05->0.418
- **Risk:** none

## 2046 Arsenal - A Weapons Overhaul - DDDB (P3, Weapons / armor / items)

- **What the author says (Nexus summary):** Complete++ Overhaul of all of the melee weapons within the lands of Bohemia
- **File:** `Arsenal Melee Weapons Overhaul-2046-6-1774914631.7z` (archive, 0.03 MB, `c_weapons-armor-items`), full (scratch, deleted after reading)
- **Grade:** A changes the most | **gameplay perceptibility:** high | **visual/audio impact:** low | **layers:** D0 content/text; D1 data tables (PTF) | **domain:** gameplay data, text
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `zzdddbarsenal`, supports `*`, loads on 1.9.8: NO (disabled: lists *)
- **Where it changes things:** tables (PTF): 9; docs: 2; localization: 2; manifest: 1; pak (container): 1; lua identical to vanilla: 0
- **Tables:** equippable_item, item_manipulation_type, melee_weapon, melee_weapon_type, pickable_item, player_item, weapon, weapon_class (153 new rows, 344 changed, 166 identical to vanilla, 5255 vanilla rows dropped by a whole-table replace); median relative change 0.333
- **Largest changes:** melee_weapon:547dbb33-e2a7-414c-a2ea-379c96b776ee stab_att_mod 0.05->0.55; melee_weapon:662a3ac5-5883-4b7d-bd84-173eaa136a73 slash_att_mod 0.05->0.85; melee_weapon:af7fd872-0830-4e33-843e-5c015bbe9e73 stab_att_mod 0.05->0.66; melee_weapon:e3ee5787-f4c5-42b7-a900-33dc97c60706 stab_att_mod 0.05->0.7; melee_weapon:2db35809-5a6b-4a5b-8782-eaf85c46f1d5 stab_att_mod 0.05->0.63; melee_weapon:49fa5ec9-92a9-4bfb-b56e-a33d04b69ee1 attack 0.2->5; melee_weapon:8468933a-7d6b-4cf9-92f0-af5874d40a9b attack 0.1->3.2; melee_weapon:e73cf113-a458-40fc-82a5-36c00f96da08 attack 0.1->2.5
- **Text:** 9 strings changed, 0 new
- **Risk:** none

## 1777 TyburnDiseases (unlisted, (not in the 365 index))

- **What the author says (Nexus summary):** -
- **File:** `Diseases-1777-V2-0-1739366414.7z` (archive, 120.66 MB, `_unmatched`), full (scratch, deleted after reading)
- **Grade:** A changes the most | **gameplay perceptibility:** high | **visual/audio impact:** high | **layers:** D0 content/text; D1 data tables (PTF); D1 game data xml (not table rows); D3 Lua scripts | **domain:** gameplay data, scripts, other game data (xml), textures/models/animations, text
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `1.9.6`, loads on 1.9.8: NO (disabled: lists 1.9.6)
- **Where it changes things:** textures: 33; other game data (xml, not table rows): 32; tables (PTF): 24; models/animations/materials: 22; scripts (Lua): 15; docs: 4; localization: 2; manifest: 1; pak (container): 1; lua identical to vanilla: 0
- **Tables:** armor, armor2clothing_attachment, armor2clothing_preset, armor_type, buff, buff_class, character_head, consumable_item, divisible_item, document, document_content, equippable_item, food, inventory, inventory2item, item, perk, perk_codex, pickable_item, player_item, questible_item, shop_type2item, st (411 new rows, 29 changed, 18 identical to vanilla, 23682 vanilla rows dropped by a whole-table replace); median relative change 0.7
- **Largest changes:** inventory2item:ba85cb8a-80c3-420e-b073-1d50807334f6 NEW row; armor2clothing_attachment:e4f950e5-4b46-48e4-8b27-a910e87da97b NEW row; armor2clothing_preset:e4f950e5-4b46-48e4-8b27-a910e87da97b/41648381-53a9-5c97-d96f-7fcb7a3e6ea5 NEW row; armor_type:66/5164435d-0ba4-40da-a17f-817e3738966f NEW row; armor:e4f950e5-4b46-48e4-8b27-a910e87da97b NEW row; consumable_item:aaae7109-660f-48c3-801a-05f74b4819a6 NEW row; consumable_item:ef8c5339-d1ce-4e58-97f2-08a0140129d2 NEW row; consumable_item:fafd8838-6f80-418e-988d-2652cb879023 NEW row
- **Lua:** 15 files, 2878 lines; API used: player.inventoryx79, Game.SendInfoTextx70, player.soulx42, Script.ReloadScriptx20, RPG.GetFactionByIdx9, XGenAIModule.LootBeginx6
- **Text:** 8 strings changed, 382 new
- **Mentions:** mentions Tables.pak, states requirements, user.cfg
- **Risk:** none

## 1777 TyburnDiseases (unlisted, (not in the 365 index))

- **What the author says (Nexus summary):** -
- **File:** `Diseases_NoAudio-1777-V2-0-1739366653.7z` (archive, 120.67 MB, `_unmatched`), full (scratch, deleted after reading)
- **Grade:** A changes the most | **gameplay perceptibility:** high | **visual/audio impact:** high | **layers:** D0 content/text; D1 data tables (PTF); D1 game data xml (not table rows); D3 Lua scripts | **domain:** gameplay data, scripts, other game data (xml), textures/models/animations, text
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `1.9.6`, loads on 1.9.8: NO (disabled: lists 1.9.6)
- **Where it changes things:** textures: 33; other game data (xml, not table rows): 32; tables (PTF): 24; models/animations/materials: 22; scripts (Lua): 15; docs: 4; localization: 2; manifest: 1; pak (container): 1; lua identical to vanilla: 0
- **Tables:** armor, armor2clothing_attachment, armor2clothing_preset, armor_type, buff, buff_class, character_head, consumable_item, divisible_item, document, document_content, equippable_item, food, inventory, inventory2item, item, perk, perk_codex, pickable_item, player_item, questible_item, shop_type2item, st (411 new rows, 29 changed, 18 identical to vanilla, 23682 vanilla rows dropped by a whole-table replace); median relative change 0.7
- **Largest changes:** inventory2item:ba85cb8a-80c3-420e-b073-1d50807334f6 NEW row; armor2clothing_attachment:e4f950e5-4b46-48e4-8b27-a910e87da97b NEW row; armor2clothing_preset:e4f950e5-4b46-48e4-8b27-a910e87da97b/41648381-53a9-5c97-d96f-7fcb7a3e6ea5 NEW row; armor_type:66/5164435d-0ba4-40da-a17f-817e3738966f NEW row; armor:e4f950e5-4b46-48e4-8b27-a910e87da97b NEW row; consumable_item:aaae7109-660f-48c3-801a-05f74b4819a6 NEW row; consumable_item:ef8c5339-d1ce-4e58-97f2-08a0140129d2 NEW row; consumable_item:fafd8838-6f80-418e-988d-2652cb879023 NEW row
- **Lua:** 15 files, 2878 lines; API used: player.inventoryx79, Game.SendInfoTextx70, player.soulx42, Script.ReloadScriptx20, RPG.GetFactionByIdx9, XGenAIModule.LootBeginx6
- **Text:** 8 strings changed, 382 new
- **Mentions:** mentions Tables.pak, states requirements, user.cfg
- **Risk:** none

## 554 Parameters Plus (P3, Tools / reference)

- **What the author says (Nexus summary):** Great resource for anyone interested in modding KCD. Featuring some 420+ gameplay parameters not readily available in the file provided by Warhorse to tweak, this resource will allow for additional fine tuning of many gameplay systems for
- **File:** `Parameters Plus-554-1-5-1562283931.zip` (archive, 0.01 MB, `c_tools-reference`), full (scratch, deleted after reading)
- **Grade:** A changes the most | **gameplay perceptibility:** high | **visual/audio impact:** none | **layers:** D1 data tables (PTF); D1 game data xml (not table rows) | **domain:** gameplay data, other game data (xml)
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `(none)`, loads on 1.9.8: yes (no version restriction)
- **Where it changes things:** manifest: 1; other game data (xml, not table rows): 1; pak (container): 1; other: 1; tables (PTF): 1; lua identical to vanilla: 0
- **Tables:** rpg_param (425 new rows, 0 changed, 182 identical to vanilla); median relative change 0.0
- **Largest changes:** rpg_param:AdditionalAttackerCountForMaxFadingBuff NEW row; rpg_param:AgiDiffToAttackSpeed NEW row; rpg_param:AgilityXPLevelBase NEW row; rpg_param:AgilityXPLevelDiff NEW row; rpg_param:AimCiriticalLimitTime NEW row; rpg_param:AimPainlessDelay NEW row; rpg_param:AimSkillToZoom NEW row; rpg_param:AimSpreadMinRatio NEW row
- **Same rows as KRS:** krs_items:rpg_param:DigestionSpeed; krs_qol:rpg_param:StrengthToInventoryCapacity
- **Problems:** ParametersPlus/data/ParametersPlus.pak!Libs/Tables/rpg/rpg_param.xml: no suffix: replaces the whole vanilla table
- **Risk:** none

## 2203 Categorized Sorted Inventory (P3, Maps / UI / HUD)

- **What the author says (Nexus summary):** Strongly based on "Sorted Inventory (2026)﻿"Re added stats for tacks and charm items, added alcohol %, changed the food system (sorting by raw, smoked, cooked, ...).Removed redundant descriptions for weapons and armor. Example: Sword - Long
- **File:** `CategorizedSortedInventory-2203-1-0-0-1775489193.zip` (archive, 0.04 MB, `c_maps-ui-hud`), full (scratch, deleted after reading)
- **Grade:** A changes the most | **gameplay perceptibility:** high | **visual/audio impact:** low | **layers:** D0 content/text; D1 data tables (PTF) | **domain:** gameplay data, text
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `(none)`, loads on 1.9.8: yes (no version restriction)
- **Where it changes things:** localization: 2; manifest: 1; pak (container): 1; tables (PTF): 1; lua identical to vanilla: 0
- **Tables:** player_item (0 new rows, 425 changed, 0 identical to vanilla, 1689 vanilla rows dropped by a whole-table replace); median relative change 0.0
- **Largest changes:** player_item:4d49d1bd-5a73-3659-5209-5a38acd4c0b6 ui_name ui_nm_jacket_001_rac->ui_nm_jacket_002_rac; player_item:4119b64e-f072-0cf2-4b8c-13e5ee901994 ui_name ui_nm_jacket_001_rac->ui_nm_jacket_003_rac; player_item:49f1d199-c8e4-5e9a-7aeb-09e3999a25a7 ui_name ui_nm_hood_black->ui_nm_hood_grey; player_item:46f60a88-47c9-9fa9-e55b-58553a841592 ui_name ui_nm_hood_black_yel->ui_nm_hood_blue_blue; player_item:42de552f-eaac-ee43-5e36-129615d2b4ab ui_name ui_nm_pros_kukla->ui_nm_pros_kukla_bla; player_item:4b0bdc51-a989-db25-bccb-9fe09655a8b0 ui_name bavorsky_kabatec_bar->bavorsky_kabatec_bar; player_item:4a60cbcc-9de1-055d-e37c-0856d8897482 ui_name kutnohorska_prosivan->kutnohorska_prosivan; player
- **Text:** 58 strings changed, 347 new
- **Risk:** none

## 2204 A Real Sorted Inventory (ARSI) (P3, Maps / UI / HUD)

- **What the author says (Nexus summary):** This mod approaches inventory sorting differently than standard sorting mods. Instead of simply adding tags as prefixes to the localized strings, this mod intervenes more deeply in the inventory sorting process. It takes into account the
- **File:** `A Real Sorted Inventory 2204 1.3.3.1 2026-06-26T10-36Z M04BeYC8a.zip` (archive, 0.25 MB, `c_maps-ui-hud`), full (scratch, deleted after reading)
- **Grade:** A changes the most | **gameplay perceptibility:** high | **visual/audio impact:** medium | **layers:** D0 content/text; D1 data tables (PTF); D3 Lua scripts | **domain:** gameplay data, scripts, textures/models/animations, UI, text
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `1.*`, loads on 1.9.8: yes (wildcard)
- **Where it changes things:** ui: 2; textures: 2; localization: 2; manifest: 1; pak (container): 1; tables (PTF): 1; scripts (Lua): 1; lua identical to vanilla: 0
- **Tables:** player_item (0 new rows, 425 changed, 0 identical to vanilla, 1689 vanilla rows dropped by a whole-table replace); median relative change 0.0
- **Largest changes:** player_item:4d49d1bd-5a73-3659-5209-5a38acd4c0b6 ui_name ui_nm_jacket_001_rac->ui_nm_jacket_002_rac; player_item:4119b64e-f072-0cf2-4b8c-13e5ee901994 ui_name ui_nm_jacket_001_rac->ui_nm_jacket_003_rac; player_item:49f1d199-c8e4-5e9a-7aeb-09e3999a25a7 ui_name ui_nm_hood_black->ui_nm_hood_grey; player_item:46f60a88-47c9-9fa9-e55b-58553a841592 ui_name ui_nm_hood_black_yel->ui_nm_hood_blue_blue; player_item:42de552f-eaac-ee43-5e36-129615d2b4ab ui_name ui_nm_pros_kukla->ui_nm_pros_kukla_bla; player_item:4b0bdc51-a989-db25-bccb-9fe09655a8b0 ui_name bavorsky_kabatec_bar->bavorsky_kabatec_bar; player_item:4a60cbcc-9de1-055d-e37c-0856d8897482 ui_name kutnohorska_prosivan->kutnohorska_prosivan; player
- **Lua:** 1 files, 298 lines; API used: System.LogAlwaysx2
- **Text:** 0 strings changed, 408 new
- **Risk:** MEDIUM: MEDIUM: Lua loadstring/loadfile/dofile in ARealSortedInventory/Data/ARealSortedInventory.pak!Scripts/mods/ARealSortedInventory.lua

## 950 Henry's Castle at Pribyslavits (P3, World / weather / visuals)

- **What the author says (Nexus summary):** Finally, Henry has a castle in Pribyslavits to call home
- **File:** `Castle Pribyslavits-950-1-2-1583519496.zip` (archive, 529.38 MB, `c_world-weather-visuals`), full (scratch, deleted after reading)
- **Grade:** A changes the most | **gameplay perceptibility:** high | **visual/audio impact:** high | **layers:** D0 content/text; D1 data tables (PTF); D1 game data xml (not table rows); D3 Lua scripts | **domain:** gameplay data, scripts, other game data (xml), textures/models/animations
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `castle_pribyslavits`, supports `(none)`, loads on 1.9.8: yes (no version restriction)
- **Where it changes things:** other: 142851; models/animations/materials: 4024; other game data (xml, not table rows): 1861; tables (PTF): 12; docs: 3; pak (container): 3; manifest: 1; scripts (Lua): 1; lua identical to vanilla: 0
- **Tables:** clothing_mesh_data, clothing_raycast, equippable_item, item, melee_weapon, pickable_item, player_item, shop_type2item, weapon (401 new rows, 0 changed, 37 identical to vanilla, 166456 vanilla rows dropped by a whole-table replace); median relative change 0.0
- **Largest changes:** equippable_item:c049e569-f0bf-4425-b0df-2e0a7f769af7 NEW row; item:c049e569-f0bf-4425-b0df-2e0a7f769af7 NEW row; melee_weapon:c049e569-f0bf-4425-b0df-2e0a7f769af7 NEW row; pickable_item:c049e569-f0bf-4425-b0df-2e0a7f769af7 NEW row; player_item:c049e569-f0bf-4425-b0df-2e0a7f769af7 NEW row; weapon:c049e569-f0bf-4425-b0df-2e0a7f769af7 NEW row; shop_type2item:c049e569-f0bf-4425-b0df-2e0a7f769af7 NEW row; shop_type2item:c049e569-f0bf-4425-b0df-2e0a7f769af7 NEW row
- **Lua:** 1 files, 112 lines; API used: Script.ReloadScriptx1
- **Risk:** MEDIUM: MEDIUM: long base64-like blob in castle_pribyslavits 1.2/data/data.pak!prefabs/smartobjects.xml / MEDIUM: long base64-like blob in castle_pribyslavits 1.2/data/data.pak!prefabs/staticlights.xml

## 1733 TyburnMedievalPoisons (unlisted, (not in the 365 index))

- **What the author says (Nexus summary):** -
- **File:** `MedievalPoisons-1733-V2-0-1729998376.7z` (archive, 6.37 MB, `_unmatched`), full (scratch, deleted after reading)
- **Grade:** A changes the most | **gameplay perceptibility:** high | **visual/audio impact:** high | **layers:** D0 content/text; D1 data tables (PTF); D1 game data xml (not table rows) | **domain:** gameplay data, other game data (xml), textures/models/animations, text
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `1.9.6`, loads on 1.9.8: NO (disabled: lists 1.9.6)
- **Where it changes things:** textures: 22; tables (PTF): 20; other game data (xml, not table rows): 13; docs: 3; localization: 2; manifest: 1; pak (container): 1; lua identical to vanilla: 0
- **Tables:** alchemy_material, buff, consumable_item, divisible_item, document, document_content_images, document_required_skill, food, herb, inventory, inventory2item, item, pickable_item, player_item, potion, recipe, recipe_ingredient, recipe_step, shop_type2item, soul (268 new rows, 71 changed, 5 identical to vanilla, 16273 vanilla rows dropped by a whole-table replace); median relative change 1.0
- **Largest changes:** pickable_item:9186b747-2591-43c0-91c6-54146543a8d8 price 30->450; pickable_item:b5587dd4-f7d8-4378-9903-7626a227ca0f price 10->250; pickable_item:38ea59b9-ead9-4fb5-a62a-2051abd844a2 price 70->350; pickable_item:b6de890f-068b-4a58-b927-0860becae508 price 120->250; inventory2item:e72ea05c-06d6-4292-8f02-c8ad222ff788 NEW row; inventory2item:b5587dd4-f7d8-4378-9903-7626a227ca0f NEW row; inventory2item:c6a00407-df94-4e52-bb07-9df1e55fa59e NEW row; inventory2item:d092f230-df9d-4050-b871-ba4d98c4bd87 NEW row
- **Text:** 25 strings changed, 135 new
- **Risk:** none

## 771 Hoods Over Helmats Removed Clipping Helmets On NPC'S (P3, Quests / lore / content)

- **What the author says (Nexus summary):** ALL Hood over helmets work that I listed and Scarfs I Added for Henry and Theresa.Of Course I Did Not Add The Hood/Scarf You Like But if I did not add it it did not work.Read the read me.
- **File:** `Hoods Over Helmets Remove Kettle Helmets NPC-771-1-1-1562422310` (folder (already extracted), 0 MB, `_quarantine`), read in place (already extracted by the author)
- **Grade:** A changes the most | **gameplay perceptibility:** high | **visual/audio impact:** high | **layers:** D0 content/text; D1 data tables (PTF); D2 engine config; D3 Lua scripts | **domain:** gameplay data, scripts, engine config, graphics config, textures/models/animations
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `(none)`, loads on 1.9.8: yes (no version restriction)
- **Where it changes things:** textures: 26; scripts (Lua): 24; other: 23; tables (PTF): 15; models/animations/materials: 11; docs: 6; manifest: 1; pak (container): 1; config (.cfg): 1; lua identical to vanilla: 0
- **Tables:** ammo, armor, armor2clothing_attachment, clothing, equippable_item, item, melee_weapon, pickable_item, player_item, rpg_param, shop_type2item, soul, weapon, weapon2weapon_preset, weapon_preset (182 new rows, 108 changed, 17608 identical to vanilla, 191 vanilla rows dropped by a whole-table replace); median relative change 10.0
- **Largest changes:** rpg_param:BaseInventoryCapacity rpg_param_value 66->840; shop_type2item:5ef63059-322e-4e1b-abe8-926e100c770e amount 2800->2000000; shop_type2item:5ef63059-322e-4e1b-abe8-926e100c770e amount 200->2000000; shop_type2item:5ef63059-322e-4e1b-abe8-926e100c770e amount 100->2000000; shop_type2item:5ef63059-322e-4e1b-abe8-926e100c770e amount 20000->2000000; shop_type2item:5ef63059-322e-4e1b-abe8-926e100c770e amount 2000->2000000; shop_type2item:5ef63059-322e-4e1b-abe8-926e100c770e amount 4000->2000000; shop_type2item:5ef63059-322e-4e1b-abe8-926e100c770e amount 200->2000000
- **Lua:** 24 files, 5848 lines; API used: player.soulx31, System.ExecuteCommandx25, player.inventoryx17, entity.soulx13, Script.SetTimerx10, Database.LoadTablex9
- **Config:** 16 keys, e.g. con_restricted=0, sys_spec_GameEffects=3, sys_spec_ObjectDetail=3, sys_spec_Particles=3, sys_spec_Physics=3, sys_spec_PostProcessing=3, sys_spec_Shading=3, sys_spec_Shadows=3
- **Mentions:** states requirements, user.cfg
- **Problems:** Data/Libs/Tables/item/ammo.xml: no suffix: replaces the whole vanilla table / Data/Libs/Tables/item/armor.xml: no suffix: replaces the whole vanilla table / Data/Libs/Tables/item/armor2clothing_attachment.xml: no suffix: replaces the whole vanilla table / Data/Libs/Tables/item/clothing.xml: no suffix: replaces the whole vanilla table / Data/Libs/Tables/item/equippable_item.xml: no suffix: replaces the whole vanilla table / Data/Libs/Tables/item/item.xml: no suffix: replaces the whole vanilla table / Data/Libs/Tables/item/melee_weapon.xml: no suffix: replaces the whole vanilla table / Data/Libs
- **Risk:** HIGH: HIGH: mod Lua loads code dynamically (loadstring/loadfile) and opens files (io.open): a script framework, not a data tweak / MEDIUM: nested archive (not readable by the game): Data/Hoods Over Helmets.7zip / MEDIUM: Lua io.open in Data/Scripts/cheat_console.lua / MEDIUM: Lua loadstring/loadfile/dofile in Data/Scripts/cheat_console.lua / MEDIUM: Lua io.open in Data/Scripts/cheat_core_exec.lua / MEDIUM: Lua loadstring/loadfile/dofile in Data/Scripts/cheat_debug.lua / MEDIUM: Lua debug.* in Data/Scr (quarantined)

## 771 Hoods Over Helmats Removed Clipping Helmets On NPC'S (P3, Quests / lore / content)

- **What the author says (Nexus summary):** ALL Hood over helmets work that I listed and Scarfs I Added for Henry and Theresa.Of Course I Did Not Add The Hood/Scarf You Like But if I did not add it it did not work.Read the read me.
- **File:** `Hoods Over Helmets Remove Kettle Helmets NPC-771-1-1-1562422310.7z` (archive, 6.95 MB, `_quarantine`), full (scratch, deleted after reading)
- **Grade:** A changes the most | **gameplay perceptibility:** high | **visual/audio impact:** high | **layers:** D0 content/text; D1 data tables (PTF); D2 engine config; D3 Lua scripts | **domain:** gameplay data, scripts, engine config, graphics config, textures/models/animations
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `(none)`, loads on 1.9.8: yes (no version restriction)
- **Where it changes things:** textures: 26; scripts (Lua): 24; other: 22; tables (PTF): 15; models/animations/materials: 11; docs: 6; pak (container): 2; manifest: 1; config (.cfg): 1; lua identical to vanilla: 0
- **Tables:** ammo, armor, armor2clothing_attachment, clothing, equippable_item, item, melee_weapon, pickable_item, player_item, rpg_param, shop_type2item, soul, weapon, weapon2weapon_preset, weapon_preset (182 new rows, 108 changed, 17608 identical to vanilla, 191 vanilla rows dropped by a whole-table replace); median relative change 10.0
- **Largest changes:** rpg_param:BaseInventoryCapacity rpg_param_value 66->840; shop_type2item:5ef63059-322e-4e1b-abe8-926e100c770e amount 2800->2000000; shop_type2item:5ef63059-322e-4e1b-abe8-926e100c770e amount 200->2000000; shop_type2item:5ef63059-322e-4e1b-abe8-926e100c770e amount 100->2000000; shop_type2item:5ef63059-322e-4e1b-abe8-926e100c770e amount 20000->2000000; shop_type2item:5ef63059-322e-4e1b-abe8-926e100c770e amount 2000->2000000; shop_type2item:5ef63059-322e-4e1b-abe8-926e100c770e amount 4000->2000000; shop_type2item:5ef63059-322e-4e1b-abe8-926e100c770e amount 200->2000000
- **Lua:** 24 files, 5848 lines; API used: player.soulx31, System.ExecuteCommandx25, player.inventoryx17, entity.soulx13, Script.SetTimerx10, Database.LoadTablex9
- **Config:** 16 keys, e.g. con_restricted=0, sys_spec_GameEffects=3, sys_spec_ObjectDetail=3, sys_spec_Particles=3, sys_spec_Physics=3, sys_spec_PostProcessing=3, sys_spec_Shading=3, sys_spec_Shadows=3
- **Mentions:** states requirements, user.cfg
- **Problems:** mods/Hoods Over Helmets/Data/Hoods Over Helmets.pak!Libs/Tables/item/ammo.xml: no suffix: replaces the whole vanilla table / mods/Hoods Over Helmets/Data/Hoods Over Helmets.pak!Libs/Tables/item/armor.xml: no suffix: replaces the whole vanilla table / mods/Hoods Over Helmets/Data/Hoods Over Helmets.pak!Libs/Tables/item/armor2clothing_attachment.xml: no suffix: replaces the whole vanilla table / mods/Hoods Over Helmets/Data/Hoods Over Helmets.pak!Libs/Tables/item/clothing.xml: no suffix: replaces the whole vanilla table / mods/Hoods Over Helmets/Data/Hoods Over Helmets.pak!Libs/Tables/item/equip
- **Risk:** HIGH: HIGH: mod Lua loads code dynamically (loadstring/loadfile) and opens files (io.open): a script framework, not a data tweak / MEDIUM: Lua io.open in mods/Hoods Over Helmets/Data/Hoods Over Helmets.pak!Scripts/cheat_console.lua / MEDIUM: Lua loadstring/loadfile/dofile in mods/Hoods Over Helmets/Data/Hoods Over Helmets.pak!Scripts/cheat_console.lua / MEDIUM: Lua io.open in mods/Hoods Over Helmets/Data/Hoods Over Helmets.pak!Scripts/cheat_core_exec.lua / MEDIUM: Lua loadstring/loadfile/dofile in mod (quarantined)

## 1088 Polearms Unleashed (P3, Weapons / armor / items)

- **What the author says (Nexus summary):** This is the most comprehensive polearm overhaul available right now for KCD. Enables perfect block and feint for polearms, as well as adds combos for polearms. You can also feint other polearm users now.
- **File:** `PolearmsUnleashed-1088-2-4-3-1603958640.7z` (archive, 0.21 MB, `c_weapons-armor-items`), full (scratch, deleted after reading)
- **Grade:** A changes the most | **gameplay perceptibility:** high | **visual/audio impact:** high | **layers:** D0 content/text; D1 data tables (PTF); D1 game data xml (not table rows); D3 Lua scripts | **domain:** gameplay data, scripts, other game data (xml), textures/models/animations, text
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `(none)`, loads on 1.9.8: yes (no version restriction)
- **Where it changes things:** tables (PTF): 18; pak (container): 6; models/animations/materials: 5; scripts (Lua): 2; localization: 2; manifest: 1; other game data (xml, not table rows): 1; lua identical to vanilla: 0
- **Tables:** combat_action_attack, combat_action_guard_movement, combat_action_perfect_block, combat_action_pose_modifier, combat_action_sync_attack, combat_action_sync_hit, combat_action_sync_pb_hit, combat_combo, combat_sync_action_hit, combat_weapon_group_to_class, melee_weapon, mn_fragment, perk, shop_type2i (107 new rows, 49 changed, 8 identical to vanilla, 4579 vanilla rows dropped by a whole-table replace); median relative change 0.171
- **Largest changes:** melee_weapon:44940b6c-f1f9-4ad1-9419-b5705a88e5b0 smash_att_mod 0.05->0.5; melee_weapon:033fc7b6-17b6-486d-95cb-a22afb131be2 smash_att_mod 0.05->0.5; melee_weapon:7377215a-a0ca-44a2-b11a-113a024191ca smash_att_mod 0.05->0.5; melee_weapon:405c1865-413d-43b8-8db9-c44a0eefd350 smash_att_mod 0.05->0.45; melee_weapon:0f5be0ac-ff11-4a01-a7f4-bf8e84c2e31b smash_att_mod 0.1->0.4; combat_action_sync_attack:18/-1/1/-1/0/0/1/-1/-1/4/-1/7/-1/CombatAttackCombo/-1/-1/-1/-1/-1/-1/7/-1/-1 NEW row; combat_action_sync_attack:18/-1/0/-1/0/0/2/-1/-1/-1/-1/7/-1/CombatAttackCombo/-1/-1/-1/-1/-1/-1/7/-1/-1 NEW row; combat_action_sync_attack:18/-1/1/-1/0/0/1/-1/-1/2/-1/7/-1/CombatAttackCombo/-1/-1/-1/-1/-1/-1/7/-1/
- **Lua:** 2 files, 20 lines; API used: entity.humanx1, entity.actorx1, System.AddCCommandx1, Script.ReloadScriptx1, System.ExecuteCommandx1
- **Text:** 0 strings changed, 7 new
- **Risk:** none

## 1807 TyburnPoisonousEnemies (unlisted, (not in the 365 index))

- **What the author says (Nexus summary):** -
- **File:** `PoisonousEnemies-1807-V1-1-1739657277.7z` (archive, 0.07 MB, `_unmatched`), full (scratch, deleted after reading)
- **Grade:** A changes the most | **gameplay perceptibility:** high | **visual/audio impact:** low | **layers:** D0 content/text; D1 data tables (PTF); D1 game data xml (not table rows); D3 Lua scripts | **domain:** gameplay data, scripts, other game data (xml), text
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `1.9.6`, loads on 1.9.8: NO (disabled: lists 1.9.6)
- **Where it changes things:** tables (PTF): 13; docs: 5; scripts (Lua): 4; localization: 2; manifest: 1; pak (container): 1; other game data (xml, not table rows): 1; lua identical to vanilla: 0
- **Tables:** armor, armor2clothing_attachment, armor2clothing_preset, armor_type, buff, divisible_item, equippable_item, food, item, pickable_item, player_item, shop_type2item, statistic (95 new rows, 0 changed, 0 identical to vanilla, 19144 vanilla rows dropped by a whole-table replace); median relative change 0.0
- **Largest changes:** armor2clothing_attachment:a36ebe4e-14e0-4110-b903-5c225a831410 NEW row; armor2clothing_preset:a36ebe4e-14e0-4110-b903-5c225a831410/41648381-53a9-5c97-d96f-7fcb7a3e6ea5 NEW row; armor2clothing_preset:b58d737a-0b33-410d-bcf1-c16f1e5fb682/40173a1a-33ae-8c7a-93bc-12dfc0b55ab8 NEW row; armor_type:67/6872d989-3628-415b-bce2-bd8487a3e41d NEW row; armor_type:68/78854441-f00f-49da-a3f5-4c2ffd6f020d NEW row; armor:a36ebe4e-14e0-4110-b903-5c225a831410 NEW row; armor:b58d737a-0b33-410d-bcf1-c16f1e5fb682 NEW row; divisible_item:15063d71-3c1b-4267-8ea1-edd9437fc63b NEW row
- **Lua:** 4 files, 3891 lines; API used: System.LogAlwaysx559, player.soulx165, Game.SendInfoTextx73, player.inventoryx64, player.idx5, player.actorx4
- **Text:** 0 strings changed, 32 new
- **Mentions:** mentions Tables.pak
- **Risk:** none

## 1956 Auto Hide HUD REBORN (P3, Maps / UI / HUD)

- **What the author says (Nexus summary):** Automatically hides and shows HUD elements at the right moments during gameplay. In addition, it adds the "Eagle Eye" perk from KCD2.
- **File:** `AutoHideHUDReborn-1956-1-4-0-1777734198.zip` (archive, 3.27 MB, `c_maps-ui-hud`), full (scratch, deleted after reading)
- **Grade:** A changes the most | **gameplay perceptibility:** high | **visual/audio impact:** medium | **layers:** D0 content/text; D1 data tables (PTF); D3 Lua scripts | **domain:** gameplay data, scripts, textures/models/animations, UI, text
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `1.*`, loads on 1.9.8: yes (wildcard)
- **Where it changes things:** localization: 26; config (.cfg): 8; tables (PTF): 4; ui: 4; docs: 3; scripts (Lua): 2; textures: 2; manifest: 1; pak (container): 1; lua identical to vanilla: 0
- **Tables:** buff, perk, perk_buff, soul2perk (4 new rows, 0 changed, 0 identical to vanilla, 49846 vanilla rows dropped by a whole-table replace); median relative change 0.0
- **Largest changes:** buff:2c19a972-cfcf-453b-9d27-82124899c579 NEW row; perk_buff:40f2a9e4-564b-48ff-89bb-937684416542/2c19a972-cfcf-453b-9d27-82124899c579 NEW row; perk:40f2a9e4-564b-48ff-89bb-937684416542 NEW row; soul2perk:40f2a9e4-564b-48ff-89bb-937684416542/43144483-f3bb-fab8-9ceb-f77e3020598a NEW row
- **Lua:** 2 files, 8052 lines; API used: System.LogAlwaysx443, System.AddCCommandx90, System.SetCVarx69, Script.SetTimerx48, System.GetCVarx29, player.soulx27
- **Text:** 0 strings changed, 39 new
- **Risk:** MEDIUM: MEDIUM: Lua debug.* in AutoHideHUDReborn/Data/AutoHideHUDReborn.pak!Scripts/RHUD.lua

## 106 Cheat (P3, Tools / reference)

- **What the author says (Nexus summary):** Adds console commands to spawn/teleport/kill NPCs, unlimited F5 quicksave, auto run console commands on game start, manipulate money, buffs, items, perks, skills, stats, stolen items, time, weather, wanted level, merchants, recipes, access
- **File:** `cheat-106-1-58-1732985419.zip` (archive, 0.14 MB, `_quarantine`), full (scratch, deleted after reading)
- **Grade:** A changes the most | **gameplay perceptibility:** high | **visual/audio impact:** low | **layers:** D0 content/text; D1 data tables (PTF); D1 game data xml (not table rows); D3 Lua scripts | **domain:** gameplay data, scripts, other game data (xml), text
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `(none)`, loads on 1.9.8: yes (no version restriction)
- **Where it changes things:** scripts (Lua): 24; docs: 6; localization: 4; other game data (xml, not table rows): 2; manifest: 1; pak (container): 1; tables (PTF): 1; lua identical to vanilla: 0
- **Tables:** buff (2 new rows, 0 changed, 0 identical to vanilla, 439 vanilla rows dropped by a whole-table replace); median relative change 0.0
- **Largest changes:** buff:a218af80-b2a5-11ed-afa1-0242ac120002 NEW row; buff:a218b534-b2a5-11ed-afa1-0242ac120002 NEW row
- **Lua:** 24 files, 6806 lines; API used: player.soulx48, System.ExecuteCommandx23, player.inventoryx22, entity.soulx11, Script.SetTimerx10, Database.LoadTablex9
- **Text:** 0 strings changed, 22 new
- **Mentions:** autoexec.cfg, states requirements
- **Risk:** HIGH: HIGH: mod Lua loads code dynamically (loadstring/loadfile) and opens files (io.open): a script framework, not a data tweak / MEDIUM: Lua io.open in Cheat/Data/data.pak!Scripts/Startup/main.lua / MEDIUM: Lua loadstring/loadfile/dofile in Cheat/Data/data.pak!Scripts/Startup/main.lua / MEDIUM: Lua io.open in Cheat/Data/data.pak!Scripts/cheat_console.lua / MEDIUM: Lua loadstring/loadfile/dofile in Cheat/Data/data.pak!Scripts/cheat_console.lua / MEDIUM: Lua io.open in Cheat/Data/data.pak!Scripts/chea (quarantined)

## 491 Loot Info - Container is empty or I already opened-looted it (P3, Crime / stealth / loot)

- **What the author says (Nexus summary):** Displays in the Loot/Open/Steal button whether the content is empty or has already been opened. / Zeigt beim Plündern/Öffnen/Stehlen-Button an, ob der Inhalt leer ist oder ob schon geöffnet wurde.Compatible with DLC "From The Ashes".
- **File:** `JCD_LootInfo-491-1-8-0-1582327030.zip` (archive, 0.04 MB, `c_crime-stealth-loot`), full (scratch, deleted after reading)
- **Grade:** A changes the most | **gameplay perceptibility:** high | **visual/audio impact:** low | **layers:** D0 content/text; D3 Lua scripts | **domain:** scripts, text
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `1.* 2.*`, loads on 1.9.8: yes (wildcard)
- **Where it changes things:** localization: 19; scripts (Lua): 17; docs: 2; config (.cfg): 1; manifest: 1; pak (container): 1; lua identical to vanilla: 0
- **Lua:** 17 files, 4554 lines; API used: Script.ReloadScriptx40, XGenAIModule.LootBeginx12, Database.guidInventoryDBIdx6, XGenAIModule.SendMessageToEntityx4, Game.GetActionControlx3, player.idx2
- **Text:** 0 strings changed, 72 new
- **Mentions:** unpack
- **Risk:** none

## 972 Let Me Loot (P3, Crime / stealth / loot)

- **What the author says (Nexus summary):** [OUT OF DATE] Game is on pause while looting. Pick those items with no fear of being stubbed or something.
- **File:** `Let Me Loot v1.3-972-1-3-1592335957.zip` (archive, 0.07 MB, `_quarantine`), full (scratch, deleted after reading)
- **Grade:** A changes the most | **gameplay perceptibility:** none | **visual/audio impact:** none | **layers:** D4 native/external | **domain:** native/external
- **How it installs:** legacy: files go into the game's Bin folder; manifest id `-`, supports `-`, loads on 1.9.8: no manifest (legacy install)
- **Where it changes things:** executables/scripts: 2; docs: 1; lua identical to vanilla: 0
- **Native file, read statically (never run):** bin/Win64/dinput8.dll=71c42e0d61e84ebc NativeMods/letmeloot.dll=cdfb3fdae385a502 | bin/Win64/dinput8.dll: suspicious strings: none; game-related strings:  // NativeMods/letmeloot.dll: suspicious strings: none; game-related strings: GetGameVersionNumber: Cannot parse system.cfg / system.cfg / Initialize: InjectHooks failed
- **Risk:** HIGH: HIGH: native binary by magic bytes: bin/Win64/dinput8.dll / HIGH: native binary by magic bytes: NativeMods/letmeloot.dll / HIGH: native code file: bin/Win64/dinput8.dll / HIGH: native code file: NativeMods/letmeloot.dll (quarantined)

## 1046 Rudy ENB for KCD (P4, Reshade / ENB / visual preset)

- **What the author says (Nexus summary):** My ENB preset for KCD. slightly improves the game's appearance.
- **File:** `Rudy ENB for KCD-1046-1-0a-1591826956.rar` (archive, 0.58 MB, `c_reshade-enb-visual-preset`), full (scratch, deleted after reading)
- **Grade:** A changes the most | **gameplay perceptibility:** medium | **visual/audio impact:** high | **layers:** D0 content/text; D2 engine config; D4 native/external | **domain:** graphics config, post-processing (ReShade/ENB), textures/models/animations, native/external
- **How it installs:** unclear: read the archive's own instructions; manifest id `-`, supports `-`, loads on 1.9.8: no manifest (legacy install)
- **Where it changes things:** reshade/ENB (shaders, presets): 27; textures: 9; docs: 1; config (.cfg): 1; lua identical to vanilla: 0
- **Config:** 26 keys, e.g. e_ShadowsMaxTexRes=1536, e_svoTI_ConeMaxLength=16, e_svoTI_DiffuseAmplifier=1.12, e_svoTI_DiffuseBias=-0.05, e_svoTI_DiffuseConeWidth=12, e_svoTI_InjectionMultiplier=1.5, e_svoTI_LowSpecMode=2, e_svoTI_MinReflectance=0.3
- **Mentions:** ReShade, user.cfg
- **Risk:** none

## 1074 Realism Enlighted ReShade - lore-friendly realistic Visual Enhancing and Sharpening - big quality boost on lower resolutions (P4, Reshade / ENB / visual preset)

- **What the author says (Nexus summary):** Reshade Preset aiming for overall grahpic enhancing the lil washed out look of the game, while trying to preserve it's tone and realistic colour palette. Adds a nuance of saturation.It really sharpens the game, making it suitable and
- **File:** `Realism Enlighted Reshade 1.0-1074-1-0-1594741584.rar` (archive, 37.55 MB, `_quarantine`), full (scratch, deleted after reading)
- **Grade:** A changes the most | **gameplay perceptibility:** none | **visual/audio impact:** high | **layers:** D0 content/text; D4 native/external | **domain:** post-processing (ReShade/ENB), native/external
- **How it installs:** unclear: read the archive's own instructions; manifest id `-`, supports `-`, loads on 1.9.8: no manifest (legacy install)
- **Where it changes things:** reshade/ENB (shaders, presets): 311; executables/scripts: 1; lua identical to vanilla: 0
- **Native file, read statically (never run):** dxgi.dll=28205140b368210f | dxgi.dll: suspicious strings: CreateRemoteThread, GetAsyncKeyState, InternetOpen, InternetReadFile, http://, https://; game-related strings: glDispatchCompute / glDispatchComputeIndirect / glFramebufferParameteri / glFramebufferParameteriMESA / glGetBufferParameteri64v / glGetBufferParameteriv / glGetFramebufferAttachmentParameteriv / glGetFramebufferParameteriv / glGetFramebufferParameterivMESA / glGetNamedBufferParameteri64v / glGetNamedBufferParameteriv / glGetNamedFramebufferAttachmentParameteriv / glGetNamedFramebufferParameteriv / glGetNamedRenderbufferParameteriv
- **Risk:** HIGH: HIGH: native binary by magic bytes: dxgi.dll / HIGH: native code file: dxgi.dll / LOW: URL in reshade-shaders/Shaders/Pirate/Pirate_Depth.cfg: https://raw.githubusercontent.com/crosire/reshade-shaders/master/Shaders/ReShade (quarantined)

## 1193 Weather Mod (P3, World / weather / visuals)

- **What the author says (Nexus summary):** Play in any weather as long as you want.Slow motion or even God Mode.
- **File:** `Weather Mod-1193-1-0-1610176393.7z` (archive, 0.07 MB, `_quarantine`), full (scratch, deleted after reading)
- **Grade:** A changes the most | **gameplay perceptibility:** high | **visual/audio impact:** none | **layers:** D3 Lua scripts | **domain:** scripts
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `(none)`, loads on 1.9.8: yes (no version restriction)
- **Where it changes things:** scripts (Lua): 24; docs: 2; manifest: 1; pak (container): 1; lua identical to vanilla: 0
- **Lua:** 24 files, 5840 lines; API used: player.soulx31, System.ExecuteCommandx23, player.inventoryx17, entity.soulx13, Script.SetTimerx10, Database.LoadTablex9
- **Risk:** HIGH: HIGH: mod Lua loads code dynamically (loadstring/loadfile) and opens files (io.open): a script framework, not a data tweak / MEDIUM: Lua io.open in mods/Weather/Data/Weather.pak!Scripts/cheat_console.lua / MEDIUM: Lua loadstring/loadfile/dofile in mods/Weather/Data/Weather.pak!Scripts/cheat_console.lua / MEDIUM: Lua io.open in mods/Weather/Data/Weather.pak!Scripts/cheat_core_exec.lua / MEDIUM: Lua loadstring/loadfile/dofile in mods/Weather/Data/Weather.pak!Scripts/cheat_debug.lua / MEDIUM: Lua d (quarantined)

## 1314 Ultimate Ray Tracing KCD Reshade Preset (P4, Reshade / ENB / visual preset)

- **What the author says (Nexus summary):** A reshade with Ray Tracing Global Illumination
- **File:** `Reshade Preset file-1314-1-1650805970.zip` (archive, 0.01 MB, `c_reshade-enb-visual-preset`), full (scratch, deleted after reading)
- **Grade:** A changes the most | **gameplay perceptibility:** none | **visual/audio impact:** high | **layers:** D0 content/text; D4 native/external | **domain:** post-processing (ReShade/ENB), native/external
- **How it installs:** unclear: read the archive's own instructions; manifest id `-`, supports `-`, loads on 1.9.8: no manifest (legacy install)
- **Where it changes things:** reshade/ENB (shaders, presets): 2; docs: 1; lua identical to vanilla: 0
- **Mentions:** ReShade, user.cfg
- **Risk:** none

## 1394 KDC ReShader (P4, Reshade / ENB / visual preset)

- **What the author says (Nexus summary):** ReShader
- **File:** `KDC ReShader-1394-1-0-1656189412.rar` (archive, 28.19 MB, `_quarantine`), full (scratch, deleted after reading)
- **Grade:** A changes the most | **gameplay perceptibility:** none | **visual/audio impact:** high | **layers:** D0 content/text; D4 native/external | **domain:** post-processing (ReShade/ENB), native/external
- **How it installs:** unclear: read the archive's own instructions; manifest id `-`, supports `-`, loads on 1.9.8: no manifest (legacy install)
- **Where it changes things:** reshade/ENB (shaders, presets): 58; lua identical to vanilla: 0
- **Native file, read statically (never run):** ReShader KDC/dxgi.dll=9e319e190d24fa29 | ReShader KDC/dxgi.dll: suspicious strings: CreateProcess, CreateRemoteThread, GetAsyncKeyState, InternetOpen, InternetReadFile, ShellExecute, http://, https://; game-related strings: glFramebufferParameteri / glFramebufferParameteriMESA / glGetBufferParameteri64v / glGetFramebufferParameteriv / glGetFramebufferParameterivMESA / glGetNamedBufferParameteri64v / glGetNamedBufferParameteriv / glGetNamedFramebufferAttachmentParameteriv / glGetNamedFramebufferParameteriv / glGetNamedRenderbufferParameteriv / glGetSamplerParameterIiv / glGetSamplerParameterIuiv / glGetSamplerParameterfv / glGetSamplerParameteriv
- **Risk:** HIGH: HIGH: native binary by magic bytes: ReShader KDC/dxgi.dll / HIGH: native code file: ReShader KDC/dxgi.dll (quarantined)

## 1403 Ultra Reshade for Low Settings (P4, Reshade / ENB / visual preset)

- **What the author says (Nexus summary):** Tested in low settings, 1080p, except textures and antialiasing (High). Performance Loss ~10-15%. (i7 3770, GTX 1070). Aims to improve looks without sacrificing too much fps at low settings.
- **File:** `Ultra ENB for Low Settings-1403-1-0-1659381780.rar` (archive, 12.44 MB, `_quarantine`), full (scratch, deleted after reading)
- **Grade:** A changes the most | **gameplay perceptibility:** none | **visual/audio impact:** high | **layers:** D0 content/text; D4 native/external | **domain:** post-processing (ReShade/ENB), native/external
- **How it installs:** legacy: files go into the game's Bin folder; manifest id `-`, supports `-`, loads on 1.9.8: no manifest (legacy install)
- **Where it changes things:** reshade/ENB (shaders, presets): 341; executables/scripts: 1; lua identical to vanilla: 0
- **Native file, read statically (never run):** bin/Win64/dxgi.dll=7520cb9170fca0f0 | bin/Win64/dxgi.dll: suspicious strings: CreateRemoteThread, GetAsyncKeyState, InternetOpen, InternetReadFile, ShellExecute, http://, https://; game-related strings: glDispatchCompute / glDispatchComputeIndirect / glFramebufferParameteri / glFramebufferParameteriMESA / glGetBufferParameteri64v / glGetBufferParameteriv / glGetFramebufferAttachmentParameteriv / glGetFramebufferParameteriv / glGetFramebufferParameterivMESA / glGetNamedBufferParameteri64v / glGetNamedBufferParameteriv / glGetNamedFramebufferAttachmentParameteriv / glGetNamedFramebufferParameteriv / glGetNamedRenderbufferParameteriv
- **Risk:** HIGH: HIGH: native binary by magic bytes: bin/Win64/dxgi.dll / HIGH: URL in script bin/Win64/reshade-shaders/Shaders/AstrayFX/TobiiEye_FreePie_AstrayFX.py: http://www.Depth3D.com / HIGH: URL in script bin/Win64/reshade-shaders/Shaders/Depth3D/TobiiEye_FreePie_Depth3D.py: http://www.Depth3D.com / HIGH: native code file: bin/Win64/dxgi.dll / HIGH: script or shortcut file: bin/Win64/reshade-shaders/Shaders/AstrayFX/TobiiEye_FreePie_AstrayFX.py / HIGH: script or shortcut file: bin/Win64/reshade-shaders/Sh (quarantined)

## 1428 Reshade DOF With UI Mask (P4, Reshade / ENB / visual preset)

- **What the author says (Nexus summary):** Reshade DOF settings using "MatsoDOF" complete with UI Mask for 1080p, 1440p and 2160p
- **File:** `MatsoDOFSettings-1428-1-0-1667951429.rar` (archive, 0.02 MB, `c_reshade-enb-visual-preset`), full (scratch, deleted after reading)
- **Grade:** A changes the most | **gameplay perceptibility:** none | **visual/audio impact:** high | **layers:** D0 content/text; D4 native/external | **domain:** post-processing (ReShade/ENB), native/external
- **How it installs:** unclear: read the archive's own instructions; manifest id `-`, supports `-`, loads on 1.9.8: no manifest (legacy install)
- **Where it changes things:** reshade/ENB (shaders, presets): 3; docs: 2; lua identical to vanilla: 0
- **Mentions:** ReShade
- **Risk:** none

## 1527 Infinite Draw Distance (P4, Graphics config (cfg))

- **What the author says (Nexus summary):** Infinite Draw Distance and other Tweaks with a press of a button (great for taking screenshots).
- **File:** `KCD PhotoMode-1527-1-1690992048.zip` (archive, 0.0 MB, `c_graphics-config-cfg`), full (scratch, deleted after reading)
- **Grade:** A changes the most | **gameplay perceptibility:** none | **visual/audio impact:** none | **layers:** D4 native/external | **domain:** native/external
- **How it installs:** unclear: read the archive's own instructions; manifest id `-`, supports `-`, loads on 1.9.8: no manifest (legacy install)
- **Where it changes things:** config (.cfg): 3; docs: 1; lua identical to vanilla: 0
- **Mentions:** ReShade, autoexec.cfg
- **Risk:** none

## 1603 Sharper graphic reshade for Kingdom Come Deliverance (P4, Reshade / ENB / visual preset)

- **What the author says (Nexus summary):** My Reshade present for Kingdom Come: Deliverance. Improved sharpening, so it has less blurry textures, more alive colors, brighter nights and more. Impact on FPS  is max 10 FPS. See pictures for difference.
- **File:** `Kingdom Come Deliverence Present v2.4-1603-2-4-1711991518.zip` (archive, 0.0 MB, `c_reshade-enb-visual-preset`), full (scratch, deleted after reading)
- **Grade:** A changes the most | **gameplay perceptibility:** none | **visual/audio impact:** high | **layers:** D0 content/text; D4 native/external | **domain:** post-processing (ReShade/ENB), native/external
- **How it installs:** unclear: read the archive's own instructions; manifest id `-`, supports `-`, loads on 1.9.8: no manifest (legacy install)
- **Where it changes things:** docs: 1; reshade/ENB (shaders, presets): 1; lua identical to vanilla: 0
- **Mentions:** ReShade
- **Risk:** none

## 1702 SLEE realistic reshade preset and performance file (P4, Reshade / ENB / visual preset)

- **What the author says (Nexus summary):** Optimization file and Realistic preset for Reshade! That looks very good, has eye adaptation and properly adjusted HDR along with Tonemaper.
- **File:** `GST-1702-1-0-0-1724428743.rar` (archive, 56.7 MB, `_quarantine`), full (scratch, deleted after reading)
- **Grade:** A changes the most | **gameplay perceptibility:** medium | **visual/audio impact:** high | **layers:** D0 content/text; D2 engine config; D4 native/external | **domain:** engine config, graphics config, post-processing (ReShade/ENB), native/external
- **How it installs:** unclear: read the archive's own instructions; manifest id `-`, supports `-`, loads on 1.9.8: no manifest (legacy install)
- **Where it changes things:** reshade/ENB (shaders, presets): 594; config (.cfg): 1; executables/scripts: 1; docs: 1; lua identical to vanilla: 0
- **Config:** 25 keys, e.g. cl_fov=110, e_PreloadMaterials=1, e_ShadowsPoolSize=2048, r_BatchType=0, r_TexMaxAnisotropy=16, r_TexMinAnisotropy=16, r_TexturesStreamPoolSize=4096, r_TexturesStreamingMaxRequestedMB=160
- **Mentions:** ReShade, states requirements
- **Native file, read statically (never run):** GST Preset + Bonus/Preset/dxgi.dll=d39d04d1931ede6e | GST Preset + Bonus/Preset/dxgi.dll: suspicious strings: CreateProcess, CreateRemoteThread, GetAsyncKeyState, InternetOpen, InternetReadFile, ShellExecute, http://, https://; game-related strings: glFramebufferParameteri / glFramebufferParameteriMESA / glGetBufferParameteri64v / glGetFramebufferParameteriv / glGetFramebufferParameterivMESA / glGetNamedBufferParameteri64v / glGetNamedBufferParameteriv / glGetNamedFramebufferAttachmentParameteriv / glGetNamedFramebufferParameteriv / glGetNamedRenderbufferParameteriv / glGetSamplerParameterIiv / glGetSamplerParameterIuiv / glGetSamplerParameterfv / glGetSamplerParameteriv
- **Risk:** HIGH: HIGH: native binary by magic bytes: GST Preset + Bonus/Preset/dxgi.dll / HIGH: URL in script GST Preset + Bonus/Preset/reshade-shaders/Shaders/AstrayFX/TobiiEye_FreePie_AstrayFX.py: http://www.Depth3D.com / HIGH: URL in script GST Preset + Bonus/Preset/reshade-shaders/Shaders/Depth3D/TobiiEye_FreePie_Depth3D.py: http://www.Depth3D.com / HIGH: native code file: GST Preset + Bonus/Preset/dxgi.dll / HIGH: script or shortcut file: GST Preset + Bonus/Preset/reshade-shaders/Shaders/AstrayFX/TobiiEye_F (quarantined)

## 1829 Mod Order Tool 1.2 (P3, Tools / reference)

- **What the author says (Nexus summary):** MOT (Mod Order Tool) is a lightweight and user-friendly tool for getting mod_order in Kingdom Come: Deliverance with ease. It scans your mod folder, and creates a mod_order.txt file to organize your mods. The tool also handles folder name
- **File:** `EN-1829-1-2-1741033054.zip` (archive, 0.02 MB, `_quarantine`), full (scratch, deleted after reading)
- **Grade:** A changes the most | **gameplay perceptibility:** none | **visual/audio impact:** none | **layers:** D4 native/external | **domain:** native/external
- **How it installs:** unclear: read the archive's own instructions; manifest id `-`, supports `-`, loads on 1.9.8: no manifest (legacy install)
- **Where it changes things:** executables/scripts: 1; lua identical to vanilla: 0
- **Native file, read statically (never run):** MOT 1.2 en_US/MOT 1.2 en_US.exe=bc439e469212ea53 | MOT 1.2 en_US/MOT 1.2 en_US.exe: suspicious strings: ShellExecute; game-related strings: DispatchMessageW / _invalid_parameter_noinfo_noreturn / _configure_wide_argv / _configthreadlocale
- **Risk:** HIGH: HIGH: native binary by magic bytes: MOT 1.2 en_US/MOT 1.2 en_US.exe / HIGH: native code file: MOT 1.2 en_US/MOT 1.2 en_US.exe (quarantined)

## 2244 Kingdom Come Script Extender (P3, Tools / reference)

- **What the author says (Nexus summary):** A tool to expand KCD modding capabilities
- **File:** `KCSE 2244 3 2026-06-29T13-46Z b37E8uyAU.zip` (archive, 7.8 MB, `_quarantine`), full (scratch, deleted after reading)
- **Grade:** A changes the most | **gameplay perceptibility:** none | **visual/audio impact:** none | **layers:** D4 native/external | **domain:** native/external
- **How it installs:** legacy: files go into the game's Bin folder; manifest id `-`, supports `-`, loads on 1.9.8: no manifest (legacy install)
- **Where it changes things:** executables/scripts: 1; other: 1; lua identical to vanilla: 0
- **Native file, read statically (never run):** Bin/Win64/dinput8.dll=37e49c57c25421b0 | Bin/Win64/dinput8.dll: suspicious strings: none; game-related strings: Hooks installed / KCSEPlugin_Version /   {} has no KCSEPlugin_Version export, skipping / Skipping duplicate plugin: {} from {} /   Registered plugin: {} v{} by {} / Plugins / Total plugins found: {} / KCSEPlugin_Load / {} has no KCSEPlugin_Load export / {} returned false from KCSEPlugin_Load / kcd_re REL::IDDatabase / kcd_addresslib_ / This plugin is incompatible with the current game build. / spdlog::thread_pool(): invalid threads_n param (valid range is 1-1000)
- **Risk:** HIGH: HIGH: native binary by magic bytes: Bin/Win64/dinput8.dll / HIGH: native code file: Bin/Win64/dinput8.dll (quarantined)

## 2255 Fast Travel Tweaks (P3, Maps / UI / HUD)

- **What the author says (Nexus summary):** 1. Added ESC to interrupt fast travel anytime 2.Added click E on checkpoint marker to fast travel to checkpoint marker
- **File:** `FastTravelTweaks 2255 3 2026-06-29T13-59Z EfL7D0slv.zip` (archive, 3.06 MB, `_quarantine`), full (scratch, deleted after reading)
- **Grade:** A changes the most | **gameplay perceptibility:** none | **visual/audio impact:** none | **layers:** D4 native/external | **domain:** native/external
- **How it installs:** unclear: read the archive's own instructions; manifest id `-`, supports `-`, loads on 1.9.8: no manifest (legacy install)
- **Where it changes things:** executables/scripts: 1; other: 1; lua identical to vanilla: 0
- **Native file, read statically (never run):** KCSE/Plugins/FastTravelTweaks.dll=1af900c3935d4466 | KCSE/Plugins/FastTravelTweaks.dll: suspicious strings: none; game-related strings: kcd_re REL::IDDatabase / kcd_addresslib_ / This plugin is incompatible with the current game build. / D:\a\libKCD1\libKCD1\.buildenv\build\FastTravelTweaks\FastTravelTweaks.pdb / KCSEPlugin_Load / KCSEPlugin_Version / _configure_narrow_argv
- **Risk:** HIGH: HIGH: native binary by magic bytes: KCSE/Plugins/FastTravelTweaks.dll / HIGH: native code file: KCSE/Plugins/FastTravelTweaks.dll (quarantined)

## 2261 Proper Third Person View (TPV Camera) (P3, Maps / UI / HUD)

- **What the author says (Nexus summary):** A third-person camera mod for Kingdom Come: Deliverance, with camera collision and frustum-culling correction, a partial raycast-based crosshair fix, and an experimental free-look orbit mode.
- **File:** `Proper Third Person View (TPV Camera) 2261 1.0.1 2026-06-30T19-31Z pA6IjrMhB.zip` (archive, 0.77 MB, `_quarantine`), full (scratch, deleted after reading)
- **Grade:** A changes the most | **gameplay perceptibility:** none | **visual/audio impact:** none | **layers:** D4 native/external | **domain:** native/external
- **How it installs:** unclear: read the archive's own instructions; manifest id `-`, supports `-`, loads on 1.9.8: no manifest (legacy install)
- **Where it changes things:** docs: 2; executables/scripts: 1; ini (text settings): 1; lua identical to vanilla: 0
- **Mentions:** ASI loader
- **Native file, read statically (never run):** KCD1_TPVCamera.asi=b0d21ba68e623c9a | KCD1_TPVCamera.asi: suspicious strings: GetAsyncKeyState, ShellExecute, https://; game-related strings: Input_P3_EventTypeDispatch / ActionDispatch_P1_Prologue / ActionDispatch_P2_DoubleDeref / ActionDispatch_P3_StructLea / InputDispatch / ActionDispatch / KCD1_TPVCamera / Menu,Overlay,Combat,Mount,Lockpicking,Dice,Reading,Alchemy,Pickpocketing,Sharpening / combat / UI Menu hooks initialization failed - menu suppression disabled / UI Overlay hooks initialization failed - overlay suppression disabled / Interaction hook initialization failed - camera-space interaction disabled / Player OnAction hook initialization failed - orbit move-detection uses body speed / Critical: third-person camera ho
- **Risk:** HIGH: HIGH: native binary by magic bytes: KCD1_TPVCamera.asi / HIGH: native code file: KCD1_TPVCamera.asi (quarantined)

## 2270 Horse Control Tweaks (P3, Horses)

- **What the author says (Nexus summary):** Tweaks the horse's canter/sprint controls to be shift toggle canter and hold shift sprint, from hold canter and double-tap before hold sprint.
- **File:** `HorseControlTweaks 2270 2 2026-06-29T14-02Z OrmK3LNnM.zip` (archive, 3.11 MB, `_quarantine`), full (scratch, deleted after reading)
- **Grade:** A changes the most | **gameplay perceptibility:** none | **visual/audio impact:** none | **layers:** D4 native/external | **domain:** native/external
- **How it installs:** unclear: read the archive's own instructions; manifest id `-`, supports `-`, loads on 1.9.8: no manifest (legacy install)
- **Where it changes things:** executables/scripts: 1; other: 1; lua identical to vanilla: 0
- **Native file, read statically (never run):** KCSE/Plugins/HorseControl.dll=da71c8d2ed85229e | KCSE/Plugins/HorseControl.dll: suspicious strings: none; game-related strings: kcd_re REL::IDDatabase / kcd_addresslib_ / This plugin is incompatible with the current game build. / D:\a\libKCD1\libKCD1\.buildenv\build\HorseControl\HorseControl.pdb / HorseControl.dll / KCSEPlugin_Load / KCSEPlugin_Version / HorseControls / _configure_narrow_argv
- **Risk:** HIGH: HIGH: native binary by magic bytes: KCSE/Plugins/HorseControl.dll / HIGH: native code file: KCSE/Plugins/HorseControl.dll (quarantined)

## 2277 Toggle Hud - KCSE (P3, Tools / reference)

- **What the author says (Nexus summary):** KCSE plugin that toggles configurable elements of HUD on key press at an engine level
- **File:** `ToggleHud 2277 1.1.1 2026-07-05T16-42Z sgZiUxTFA.zip` (archive, 4.69 MB, `_quarantine`), full (scratch, deleted after reading)
- **Grade:** A changes the most | **gameplay perceptibility:** none | **visual/audio impact:** none | **layers:** D4 native/external | **domain:** native/external
- **How it installs:** unclear: read the archive's own instructions; manifest id `-`, supports `-`, loads on 1.9.8: no manifest (legacy install)
- **Where it changes things:** executables/scripts: 1; ini (text settings): 1; other: 1; lua identical to vanilla: 0
- **Native file, read statically (never run):** KCSE/Plugins/ToggleHud.dll=8d7bfa24beb6788a | KCSE/Plugins/ToggleHud.dll: suspicious strings: none; game-related strings: ToggleHud.ini / Plugins / Failed to initialize ConfigHandler. Check if ToggleHud.ini exists and is valid. / kcd_re REL::IDDatabase / kcd_addresslib_ / This plugin is incompatible with the current game build. / D:\a\KCD1-ToggleHud\KCD1-ToggleHud\buildRel\ToggleHud.pdb / KCSEPlugin_Load / KCSEPlugin_Version / _configure_narrow_argv
- **Risk:** HIGH: HIGH: native binary by magic bytes: KCSE/Plugins/ToggleHud.dll / HIGH: native code file: KCSE/Plugins/ToggleHud.dll (quarantined)

## 2365 KCDT (P3, (unclassified))

- **What the author says (Nexus summary):** My personal modding library. Do not download it unless it’s required by some of my other mods.
- **File:** `Kcdt 2365 1 2026-09-16T13-46Z 8HMDLo1KJ (1).zip` (archive, 0.15 MB, `_quarantine`), full (scratch, deleted after reading)
- **Grade:** A changes the most | **gameplay perceptibility:** none | **visual/audio impact:** none | **layers:** D4 native/external | **domain:** native/external
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `(none)`, loads on 1.9.8: yes (no version restriction)
- **Where it changes things:** executables/scripts: 1; manifest: 1; other: 1; lua identical to vanilla: 0
- **Native file, read statically (never run):** KCDT.asi=26e01ad1e9913a43 | KCDT.asi: suspicious strings: none; game-related strings: masterStrike / inventory.hook.failed / init.inventory.hook.installed / inventory.hook.ready / item.transfer.hook.ready / item.transfer.hook.failed / input.action.hook.ready / input.action.hook.failed / input.registration.hook.ready / input.registration.hook.failed / input.map.creation.hook.ready / input.map.creation.hook.failed / KCDT-test.mode / KCDT-test-report.txt
- **Risk:** HIGH: HIGH: native binary by magic bytes: KCDT.asi / HIGH: native code file: KCDT.asi (quarantined)

## 2365 KCDT (P3, (unclassified))

- **What the author says (Nexus summary):** My personal modding library. Do not download it unless it’s required by some of my other mods.
- **File:** `Kcdt 2365 1 2026-09-16T13-46Z 8HMDLo1KJ.zip` (archive, 0.15 MB, `_quarantine`), full (scratch, deleted after reading)
- **Grade:** A changes the most | **gameplay perceptibility:** none | **visual/audio impact:** none | **layers:** D4 native/external | **domain:** native/external
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `(none)`, loads on 1.9.8: yes (no version restriction)
- **Where it changes things:** executables/scripts: 1; manifest: 1; other: 1; lua identical to vanilla: 0
- **Native file, read statically (never run):** KCDT.asi=26e01ad1e9913a43 | KCDT.asi: suspicious strings: none; game-related strings: masterStrike / inventory.hook.failed / init.inventory.hook.installed / inventory.hook.ready / item.transfer.hook.ready / item.transfer.hook.failed / input.action.hook.ready / input.action.hook.failed / input.registration.hook.ready / input.registration.hook.failed / input.map.creation.hook.ready / input.map.creation.hook.failed / KCDT-test.mode / KCDT-test-report.txt
- **Risk:** HIGH: HIGH: native binary by magic bytes: KCDT.asi / HIGH: native code file: KCDT.asi (quarantined)

## 2366 Faster Book Flipping (P3, Maps / UI / HUD)

- **What the author says (Nexus summary):** Alchemy bench book pages flip at 3x
- **File:** `FasterBookFlipping 2366 1 2026-09-17T08-10Z aSoQ0kc7B.zip` (archive, 0.08 MB, `_quarantine`), full (scratch, deleted after reading)
- **Grade:** A changes the most | **gameplay perceptibility:** none | **visual/audio impact:** none | **layers:** D4 native/external | **domain:** native/external
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `(none)`, loads on 1.9.8: yes (no version restriction)
- **Where it changes things:** executables/scripts: 1; ini (text settings): 1; manifest: 1; other: 1; lua identical to vanilla: 0
- **Native file, read statically (never run):** FasterBookFlipping.asi=1c25f60f1b6e16cf | FasterBookFlipping.asi: suspicious strings: none; game-related strings: %s.ini / KCDT.asi / KCDT_GetVersion / KCDT_IsReady / KCDT_GetGameBase / KCDT_InstallHook / KCDT_ReadMemory
- **Risk:** HIGH: HIGH: native binary by magic bytes: FasterBookFlipping.asi / HIGH: native code file: FasterBookFlipping.asi (quarantined)

## 1153 More historically accurate item stats (P3, Weapons / armor / items)

- **What the author says (Nexus summary):** The real transitional armour is way better in terms of defence, including brigandines, plates, chain mails and even gambesons.This mod will manage to enhance the defensive abilities of most types of armour and will have some alternations in
- **File:** `mod-1153-1-0-0-1605526312.zip` (archive, 0.1 MB, `c_weapons-armor-items`), full (scratch, deleted after reading)
- **Grade:** B large | **gameplay perceptibility:** high | **visual/audio impact:** none | **layers:** D1 data tables (PTF) | **domain:** gameplay data
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `1.9.4 1.9.5 1.9.6`, loads on 1.9.8: NO (disabled: lists 1.9.4, 1.9.5, 1.9.6)
- **Where it changes things:** other: 6; tables (PTF): 6; manifest: 1; pak (container): 1; lua identical to vanilla: 0
- **Tables:** ammo, armor, equippable_item, melee_weapon, missile_weapon, weapon (0 new rows, 370 changed, 1820 identical to vanilla); median relative change 1.09
- **Largest changes:** melee_weapon:24a7c868-f23f-4799-8e64-331435a77404 slash_att_mod 0.05->0.95; melee_weapon:3ef71c79-57c2-4f28-8f31-a091d9b78798 slash_att_mod 0.05->1; melee_weapon:488d9792-0dbf-41dc-a320-753d94d1f1b6 slash_att_mod 0.05->1.1; melee_weapon:662a3ac5-5883-4b7d-bd84-173eaa136a73 slash_att_mod 0.05->1.2; melee_weapon:6ec15d56-4f77-4751-af72-e6225f825ae8 slash_att_mod 0.05->1; melee_weapon:e16b0af6-fb6a-43e2-9a9c-1b8c227e64b8 slash_att_mod 0.05->1.2; melee_weapon:033fc7b6-17b6-486d-95cb-a22afb131be2 smash_att_mod 0.05->0.45; armor:4da15cb9-ab68-def0-f5c4-cb44e6c4a393 slash_def 0.39->2.6
- **Problems:** Data/mod.pak!Libs/Tables/item/ammo.xml: no suffix: replaces the whole vanilla table / Data/mod.pak!Libs/Tables/item/armor.xml: no suffix: replaces the whole vanilla table / Data/mod.pak!Libs/Tables/item/equippable_item.xml: no suffix: replaces the whole vanilla table / Data/mod.pak!Libs/Tables/item/melee_weapon.xml: no suffix: replaces the whole vanilla table / Data/mod.pak!Libs/Tables/item/missile_weapon.xml: no suffix: replaces the whole vanilla table / Data/mod.pak!Libs/Tables/item/weapon.xml: no suffix: replaces the whole vanilla table
- **Risk:** none

## 796 Miller Guild Items (P3, World / weather / visuals)

- **What the author says (Nexus summary):** Stealth armor set with a unique buff per piece (Thick as Thieves quests); includes a horse item fix Adds a new stealth armor set.  Each item has a unique buff.  The items are obtained by doing the Thick as Thieves quests from the Miller guild.1.9 compatible.  Now with bonus horse item fix
- **File:** `Miller Guild Items-796-1-3-1564712669.7z` (archive, 0.61 MB, `c_world-weather-visuals`), full (scratch, deleted after reading)
- **Grade:** B large | **gameplay perceptibility:** high | **visual/audio impact:** low | **layers:** D0 content/text; D1 data tables (PTF) | **domain:** gameplay data, text
- **How it installs:** loose .pak (legacy: copy into Data); manifest id `-`, supports `-`, loads on 1.9.8: no manifest (legacy install)
- **Where it changes things:** other: 13; tables (PTF): 13; localization: 3; pak (container): 1; lua identical to vanilla: 0
- **Tables:** armor, armor2clothing_attachment, armor_type, buff, clothing, clothing_preset, equippable_item, item, pickable_item, player_item, quest_reward_item, shop_type2item, skill2item_category (123 new rows, 107 changed, 12987 identical to vanilla); median relative change 1.0
- **Largest changes:** armor:4962e864-5964-aecf-7a62-6e117b96ec99 zone3_brightness 1->41; armor:ff5ab403-62fa-41d2-9afd-7d6857f999c4 noise 0.1->1; armor:4063f2eb-d6d6-a27e-c1d7-a0885269108c color_saturation 1->2; armor:42d6c8cd-d109-5bd2-0cbf-62f6dae942b9 max_status 40->0; armor:45345fd3-43ed-b961-fde6-af37d4993aa7 max_status 40->0; armor:45f0293a-b0b9-cd56-6864-ade54db775b8 color_hue 0->0.205556; armor:46cf7471-dccd-7e3a-18e8-e4a2e05d7ea5 max_status 40->0; armor:48f6cde5-a747-dbee-2af1-9fae418ef68b brightness 0.5->1
- **Text:** 4 strings changed, 41 new
- **Same rows as KRS:** krs_qol:skill2item_category:armor.horse_bridle.*/8; krs_qol:skill2item_category:armor.horse_saddle.*/8
- **Problems:** Miller Guild Items 1.3/Data/guilditems.pak!Libs/Tables/item/armor.xml: no suffix: replaces the whole vanilla table / Miller Guild Items 1.3/Data/guilditems.pak!Libs/Tables/item/armor2clothing_attachment.xml: no suffix: replaces the whole vanilla table / Miller Guild Items 1.3/Data/guilditems.pak!Libs/Tables/item/armor_type.xml: no suffix: replaces the whole vanilla table / Miller Guild Items 1.3/Data/guilditems.pak!Libs/Tables/item/clothing.xml: no suffix: replaces the whole vanilla table / Miller Guild Items 1.3/Data/guilditems.pak!Libs/Tables/item/clothing_preset.xml: no suffix: replaces the
- **Risk:** none

## 1535 Dandelion Baron (P3, Quests / lore / content)

- **What the author says (Nexus summary):** "Dandelion Baron" attempts to rein in the more egregious aspects of Herbalism's economic impact, and more generally, to moderate the pace of the player's accumulation of wealth.
- **File:** `DandelionBaron-1535-1-0-1691856480.7z` (archive, 0.0 MB, `c_quests-lore-content`), full (scratch, deleted after reading)
- **Grade:** B large | **gameplay perceptibility:** high | **visual/audio impact:** none | **layers:** D1 data tables (PTF) | **domain:** gameplay data
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `1.*`, loads on 1.9.8: yes (wildcard)
- **Where it changes things:** tables (PTF): 2; manifest: 1; pak (container): 1; lua identical to vanilla: 0
- **Tables:** pickable_item, shop_type2item (0 new rows, 220 changed, 18 identical to vanilla, 2896 vanilla rows dropped by a whole-table replace); median relative change 1.0
- **Largest changes:** pickable_item:3373a604-a2fd-4af0-a5e8-760e1a9893f9 price 2->0; pickable_item:5e9b4fa1-aafa-4352-b5d6-58df2c263caa price 1->0; pickable_item:a11cc7f6-b499-4003-aef1-938e87b30a2e price 4->0; pickable_item:a364b800-c1ca-4bd1-92cb-ae1689bfa7ea price 2->0; shop_type2item:0290b689-c01c-480f-b121-bed71ad1f5e0 amount 10->0; shop_type2item:7259b9bc-dfae-487e-a8bb-c1f500894e0c amount 10->0; shop_type2item:7da04bba-0564-42da-bcf1-9a2fc5faf025 amount 10->0; shop_type2item:9b771c16-c0b1-438c-aeda-8c4d3ce28465 amount 10->0
- **Risk:** none

## 977 Alms for Beggars (P3, Economy / merchants)

- **What the author says (Nexus summary):** EN:Henry now can give alms to refugees/beggars in Rattay.CZ:Jindra nyní může dávat almužnu žebrákům/uprchlíkům v Ratajích.Lokalizace / Localization:CZE,ENG,FRA,GER,RUS,CHN,PL
- **File:** `Beggars_alms_mod_v1.5.2-977-1-5-2-1590399761.zip` (archive, 0.05 MB, `c_economy-merchants`), full (scratch, deleted after reading)
- **Grade:** B large | **gameplay perceptibility:** high | **visual/audio impact:** low | **layers:** D0 content/text; D1 data tables (PTF) | **domain:** gameplay data, text
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `alms_for_beggars`, supports `(none)`, loads on 1.9.8: yes (no version restriction)
- **Where it changes things:** localization: 14; other: 10; tables (PTF): 10; manifest: 1; docs: 1; pak (container): 1; lua identical to vanilla: 0
- **Tables:** ?, clothing_mesh_data, clothing_raycast, response, sequence, sequence_line, topic, topic2sequence, v_branch, v_dialogue_commands (207 new rows, 4 changed, 0 identical to vanilla, 502463 vanilla rows dropped by a whole-table replace); median relative change 0.0
- **Largest changes:** clothing_mesh_data:Objects/characters/humans/body/s1_body_npc.skin/0/// NEW row; clothing_mesh_data:Objects/characters/humans/head/s1_head_v002.skin/0/// NEW row; clothing_mesh_data:Objects/characters/humans/head/s1_head_v001.skin/0/// NEW row; clothing_mesh_data:Objects/characters/humans/attachment/s2_att_belt_006.skin/0/// NEW row; clothing_mesh_data:Objects/characters/humans/attachment/s2_att_p2_l2_v003.skin/0/// NEW row; clothing_mesh_data:Objects/characters/humans/attachment/s2_att_p2_l1_v005.skin/0/// NEW row; clothing_mesh_data:Objects/characters/humans/body/s2_body.skin/0/// NEW row; clothing_mesh_data:Objects/characters/humans/head/s2_head_v001.skin/0/// NEW row
- **Text:** 0 strings changed, 126 new
- **Problems:** alms_for_beggars/data/tables_patch.pak!libs/tables/text/topictorole__alms_for_beggars.xml: table 'TopicToRole__alms_for_beggars' is not in the vanilla game
- **Risk:** none

## 2279 Immersive Economy FIXED (P3, Economy / merchants)

- **What the author says (Nexus summary):** I fixed the errors in: Immersive Economy - https://www.nexusmods.com/kingdomcomedeliverance/mods/1548?tab=files&file_id=6927&nmm=1
- **File:** `ImmersiveEconomyFIXED 2279 1.0.2 2026-07-17T19-29Z 6b3zKD4k2.zip` (archive, 0.05 MB, `c_economy-merchants`), full (scratch, deleted after reading)
- **Grade:** B large | **gameplay perceptibility:** high | **visual/audio impact:** none | **layers:** D1 data tables (PTF) | **domain:** gameplay data
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `1.9.4 1.9.5 1.9.6 1.9.7 1.9.8 1.9.*`, loads on 1.9.8: yes (explicit)
- **Where it changes things:** tables (PTF): 2; manifest: 1; pak (container): 1; lua identical to vanilla: 0
- **Tables:** rpg_param, shop (0 new rows, 164 changed, 0 identical to vanilla, 181 vanilla rows dropped by a whole-table replace); median relative change 0.875
- **Largest changes:** rpg_param:ItemHealthPriceStatusWeight rpg_param_value 0.8->1; shop:25/17/14 price_sell_multiplier 1->0.1; shop:25/28/30 price_sell_multiplier 1->0.1; shop:25/78/35 price_sell_multiplier 1->0.1; shop:25/106/54 price_sell_multiplier 1->0.1; shop:8/139/57 price_sell_multiplier 1->0.1; shop:8/140/55 price_sell_multiplier 1->0.1; shop:8/141/56 price_sell_multiplier 1->0.1
- **Problems:** ImmersiveEconomy/Data/immersive_economy.pak!immersive_economy/Libs/Tables/rpg/rpg_param.xml: no suffix: replaces the whole vanilla table / ImmersiveEconomy/Data/immersive_economy.pak!immersive_economy/Libs/Tables/shop/shop.xml: no suffix: replaces the whole vanilla table
- **Risk:** none

## 1870 Fair Trade - PTF (P3, Economy / merchants)

- **What the author says (Nexus summary):** Items sell at the price they are bought at (base selling price); PTF Sell items at the same price you buy at - PTF Compatible
- **File:** `Fair Trade-1870-1-0-1739553563.zip` (archive, 0.0 MB, `c_economy-merchants`), full (scratch, deleted after reading)
- **Grade:** B large | **gameplay perceptibility:** high | **visual/audio impact:** none | **layers:** D1 data tables (PTF) | **domain:** gameplay data
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `fairtrade`, supports `(none)`, loads on 1.9.8: yes (no version restriction)
- **Where it changes things:** manifest: 1; pak (container): 1; tables (PTF): 1; lua identical to vanilla: 0
- **Tables:** shop (0 new rows, 133 changed, 30 identical to vanilla); median relative change 0.375
- **Largest changes:** shop:25/15/13 price_sell_multiplier 0.5->1.5; shop:25/102/52 price_sell_multiplier 0.4->1.2; shop:25/118/41 price_sell_multiplier 0.4->1.2; shop:25/119/60 price_sell_multiplier 0.4->1.2; shop:25/137/53 price_sell_multiplier 0.4->1.2; shop:3/159/85 price_sell_multiplier 0.3->0.8; shop:3/166/94 price_sell_multiplier 0.3->0.8; shop:10/11/9 price_sell_multiplier 0.4->1
- **Risk:** none

## 1873 Daily Restock And Rich Merchants - PTF (P3, Economy / merchants)

- **What the author says (Nexus summary):** Merchants will restock daily (or the alternative frequency you've chosen), and will have 100 times more money.
- **File:** `Daily Restock And Rich Merchants-1873-1-0-1739611543.zip` (archive, 0.0 MB, `c_economy-merchants`), full (scratch, deleted after reading)
- **Grade:** B large | **gameplay perceptibility:** high | **visual/audio impact:** none | **layers:** D1 data tables (PTF) | **domain:** gameplay data
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `dailyrestockrichmerchant`, supports `(none)`, loads on 1.9.8: yes (no version restriction)
- **Where it changes things:** tables (PTF): 2; manifest: 1; pak (container): 1; lua identical to vanilla: 0
- **Tables:** shop, shop_type2item (0 new rows, 125 changed, 117 identical to vanilla, 718 vanilla rows dropped by a whole-table replace); median relative change 10.0
- **Largest changes:** shop_type2item:5ef63059-322e-4e1b-abe8-926e100c770e amount 2800->280000; shop_type2item:5ef63059-322e-4e1b-abe8-926e100c770e amount 200->20000; shop_type2item:5ef63059-322e-4e1b-abe8-926e100c770e amount 100->10000; shop_type2item:5ef63059-322e-4e1b-abe8-926e100c770e amount 20000->2000000; shop_type2item:5ef63059-322e-4e1b-abe8-926e100c770e amount 2000->200000; shop_type2item:5ef63059-322e-4e1b-abe8-926e100c770e amount 4000->400000; shop_type2item:5ef63059-322e-4e1b-abe8-926e100c770e amount 1500->150000; shop_type2item:5ef63059-322e-4e1b-abe8-926e100c770e amount 20000->2000000
- **Risk:** none

## 1110 AI Standalone Library (P3, Tools / reference)

- **What the author says (Nexus summary):** Mod library/resource to use in my mods and in other mods
- **File:** `resource-1110-1-5-1603783234.7z` (archive, 0.14 MB, `c_tools-reference`), full (scratch, deleted after reading)
- **Grade:** B large | **gameplay perceptibility:** high | **visual/audio impact:** none | **layers:** D1 data tables (PTF); D1 game data xml (not table rows) | **domain:** gameplay data, other game data (xml)
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `aistandalone`, supports `(none)`, loads on 1.9.8: yes (no version restriction)
- **Where it changes things:** tables (PTF): 7; other game data (xml, not table rows): 4; pak (container): 2; manifest: 1; docs: 1; lua identical to vanilla: 0
- **Tables:** brain, brain2mailbox, brain2subbrain, brain_variable, subbrain, subbrain_behaviour_tree, subbrain_combat (116 new rows, 0 changed, 0 identical to vanilla, 4438 vanilla rows dropped by a whole-table replace); median relative change 0.0
- **Largest changes:** brain2mailbox:47b6c85f-8264-085c-f9b4-aba01c3b6aa5/14e5d62e-91fd-436b-84b5-ae570a5391a5 NEW row; brain2mailbox:47b6c85f-8264-085c-f9b4-aba01c3b6aa5/3fc6fad4-31e6-4834-8943-4321435509d5 NEW row; brain2mailbox:47b6c85f-8264-085c-f9b4-aba01c3b6aa5/406877cd-58bb-a2db-343d-dc9d2d083e84 NEW row; brain2mailbox:47b6c85f-8264-085c-f9b4-aba01c3b6aa5/40f9ec95-374e-829c-82b8-9554078a5482 NEW row; brain2mailbox:47b6c85f-8264-085c-f9b4-aba01c3b6aa5/40fb6ff5-d1a8-6708-f5f6-c6717981cebd NEW row; brain2mailbox:47b6c85f-8264-085c-f9b4-aba01c3b6aa5/42e861d6-b5d9-deba-6b3c-f030a3f6a5a5 NEW row; brain2mailbox:47b6c85f-8264-085c-f9b4-aba01c3b6aa5/437ed51e-4c52-8997-210a-efb2040e6380 NEW row; brain2mailbox:47b6c85
- **Risk:** none

## 1689 Playable Daggers (P3, Weapons / armor / items)

- **What the author says (Nexus summary):** Fight with dual wielding daggers.
- **File:** `PlayableDaggers-1689-V3-0-1736559656.7z` (archive, 2.08 MB, `c_weapons-armor-items`), full (scratch, deleted after reading)
- **Grade:** B large | **gameplay perceptibility:** high | **visual/audio impact:** high | **layers:** D0 content/text; D1 data tables (PTF); D3 Lua scripts | **domain:** gameplay data, scripts, textures/models/animations, text
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `1.9.6`, loads on 1.9.8: NO (disabled: lists 1.9.6)
- **Where it changes things:** tables (PTF): 14; models/animations/materials: 4; textures: 4; docs: 3; scripts (Lua): 2; localization: 2; manifest: 1; pak (container): 1; lua identical to vanilla: 0
- **Tables:** buff, equippable_item, inventory2item, item, melee_weapon, perk, perk_buff, pickable_item, player_item, shop_type2item, skill, weapon, weapon2weapon_preset, weapon_class (101 new rows, 10 changed, 1 identical to vanilla, 11055 vanilla rows dropped by a whole-table replace); median relative change 0.4
- **Largest changes:** weapon_class:/5/8a5dd3a2-04e1-4ce7-8833-9252b410662b/1/0/-1/-1/20/8/1 NEW row; inventory2item:e794cabc-9629-45c2-9f76-83231a80f7c5 NEW row; equippable_item:a8f152f2-1693-4686-82c0-df620f073276 NEW row; equippable_item:bcccf2cf-dced-49ac-a291-4b76b20442e7 NEW row; equippable_item:ca446315-e266-4a0c-9674-9654ecd47702 NEW row; equippable_item:da56ed6d-4306-412b-bf34-cca2a24c720f NEW row; equippable_item:e794cabc-9629-45c2-9f76-83231a80f7c5 NEW row; item:a8f152f2-1693-4686-82c0-df620f073276 NEW row
- **Lua:** 2 files, 114 lines; API used: System.LogAlwaysx8, player.inventoryx8, Database.LoadTablex4, Database.GetTableInfox4, Database.GetTableLinex4, Game.SendInfoTextx4
- **Text:** 19 strings changed, 36 new
- **Risk:** none

## 2068 SPOA Silver Knight Armor for Kingdom Come Deliverance (P3, Weapons / armor / items)

- **What the author says (Nexus summary):** Silver Piece of Art - Silver Knight Armor for KCD. Stylish armor with high details. Max resolution 4K (4096x4096).
- **File:** `SPOA SKA for KCD (2K textures)-2068-1-03-1755982732.zip` (archive, 131.02 MB, `c_weapons-armor-items`), full (scratch, deleted after reading)
- **Grade:** B large | **gameplay perceptibility:** high | **visual/audio impact:** high | **layers:** D0 content/text; D1 data tables (PTF) | **domain:** gameplay data, textures/models/animations, text
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `1.9.*`, loads on 1.9.8: yes (wildcard)
- **Where it changes things:** textures: 36; models/animations/materials: 22; tables (PTF): 13; localization: 6; docs: 1; manifest: 1; pak (container): 1; lua identical to vanilla: 0
- **Tables:** armor, armor2clothing_attachment, armor2clothing_preset, clothing, clothing_attachment, clothing_mesh_data, clothing_raycast, equippable_item, helmet, item, pickable_item, player_item, shop_type2item (82 new rows, 0 changed, 0 identical to vanilla, 19228 vanilla rows dropped by a whole-table replace); median relative change 0.0
- **Largest changes:** armor2clothing_attachment:03bde0d1-1499-4cf1-8599-c9f865c6f787 NEW row; armor2clothing_preset:03bde0d1-1499-4cf1-8599-c9f865c6f787/440e9c0e-c8c9-c691-fdab-2411fa876bba NEW row; armor2clothing_preset:03bde0d1-1499-4cf1-8599-c9f865c6f787/4f604161-fd71-f76d-1c9d-08295e1119be NEW row; armor:3112d89d-1d6f-4791-9244-b901f043f917 NEW row; armor:0600d533-3421-4723-abdd-5317b5ed8184 NEW row; armor:e53bf9f0-1552-4a1e-b082-4c6e75eb3276 NEW row; armor:03bde0d1-1499-4cf1-8599-c9f865c6f787 NEW row; armor:1a09f922-13f2-4ba4-a94b-b1348c4ae22a NEW row
- **Text:** 0 strings changed, 42 new
- **Risk:** none

## 1566 Karnages_Lost_Weapons_Pack_Redux 2.0 (P3, Weapons / armor / items)

- **What the author says (Nexus summary):** re-implements  and balances the lost weapons that the devs decided to not include
- **File:** `Karnages_Lost_Weapons_Pack_Redux 2.0-1566-1-0-0-1700619203.7z` (archive, 0.01 MB, `c_weapons-armor-items`), full (scratch, deleted after reading)
- **Grade:** B large | **gameplay perceptibility:** high | **visual/audio impact:** none | **layers:** D1 data tables (PTF) | **domain:** gameplay data
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `(none)`, loads on 1.9.8: yes (no version restriction)
- **Where it changes things:** tables (PTF): 7; manifest: 1; pak (container): 1; lua identical to vanilla: 0
- **Tables:** equippable_item, melee_weapon, pickable_item, player_item, shop_type2item, weapon, weapon_class (23 new rows, 50 changed, 10 identical to vanilla, 6356 vanilla rows dropped by a whole-table replace); median relative change 1.0
- **Largest changes:** melee_weapon:e5fc1a89-9bb1-44a9-a524-c6834a5e2e76 smash_att_mod 0.05->1; melee_weapon:a7d5c50c-de7d-4982-969e-33fcbccb749a smash_att_mod 0.05->2; pickable_item:6dda19ab-a26d-4585-9600-15942e16caeb price 666->19244; pickable_item:2c9e4731-1858-423d-a898-a15484507cb7 price 666->7867; weapon:6dda19ab-a26d-4585-9600-15942e16caeb defense 1->17.5; weapon:2c9e4731-1858-423d-a898-a15484507cb7 defense 1->13; weapon:b741463f-fe65-430b-9082-13d1950a523d max_status 70->800; weapon:e73cf113-a458-40fc-82a5-36c00f96da08 max_status 25->800
- **Risk:** none

## 2174 Horse Body Armor (Barding) (P3, Horses)

- **What the author says (Nexus summary):** Improved version of "Barding (new items)" mod. Adds 3 armor items for the horse, which fit into the dedicated horse body armor slot. PTF mod, fully localized, compatible with latest game version and the body armor correctly overlaps with
- **File:** `Barding Improved-2174-1-0-1-1772742779 (1).zip` (archive, 20.59 MB, `c_horses`), full (scratch, deleted after reading)
- **Grade:** B large | **gameplay perceptibility:** high | **visual/audio impact:** high | **layers:** D0 content/text; D1 data tables (PTF) | **domain:** gameplay data, textures/models/animations, text
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `1.9.*`, loads on 1.9.8: yes (wildcard)
- **Where it changes things:** localization: 28; tables (PTF): 12; textures: 9; models/animations/materials: 3; manifest: 1; pak (container): 1; lua identical to vanilla: 0
- **Tables:** armor, armor2clothing_preset, armor_archetype, armor_archetype2body_subpart, clothing, clothing_raycast, equipment_slot, equippable_item, item, pickable_item, player_item, shop_type2item (65 new rows, 0 changed, 0 identical to vanilla, 19302 vanilla rows dropped by a whole-table replace); median relative change 0.0
- **Largest changes:** player_item:100c0a43-d863-4c8e-b49e-375c3fc825fb NEW row; player_item:cd23e264-eabb-49fe-973c-3d86c7910931 NEW row; player_item:df1b7bc5-770c-4f9a-857f-7ca77ae53799 NEW row; pickable_item:cd23e264-eabb-49fe-973c-3d86c7910931 NEW row; pickable_item:100c0a43-d863-4c8e-b49e-375c3fc825fb NEW row; pickable_item:df1b7bc5-770c-4f9a-857f-7ca77ae53799 NEW row; item:100c0a43-d863-4c8e-b49e-375c3fc825fb NEW row; item:cd23e264-eabb-49fe-973c-3d86c7910931 NEW row
- **Text:** 0 strings changed, 84 new
- **Risk:** none

## 1605 Formidable Runt (P3, Quests / lore / content)

- **What the author says (Nexus summary):** Runt will become a formidable opponent during his final encounter with Henry. The original game Runt was a let down in so many ways. The fight was over quickly and did not feel like a climactic moment at all. The 'Better Equipped Runt' mod
- **File:** `Formidable Runt-1605-1-4-1711201397.zip` (archive, 0.01 MB, `c_quests-lore-content`), full (scratch, deleted after reading)
- **Grade:** B large | **gameplay perceptibility:** high | **visual/audio impact:** none | **layers:** D1 data tables (PTF) | **domain:** gameplay data
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `(none)`, loads on 1.9.8: yes (no version restriction)
- **Where it changes things:** tables (PTF): 7; manifest: 1; pak (container): 1; lua identical to vanilla: 0
- **Tables:** armor2clothing_preset, buff, perk, perk_buff, soul, soul2perk, soul2skill (25 new rows, 8 changed, 0 identical to vanilla, 99989 vanilla rows dropped by a whole-table replace); median relative change 0.667
- **Largest changes:** soul2skill:20/47e2f514-fa2e-826f-3565-c97a749265bc value 2->20; soul2skill:16/47e2f514-fa2e-826f-3565-c97a749265bc value 8->20; soul2skill:21/47e2f514-fa2e-826f-3565-c97a749265bc value 8->20; armor2clothing_preset:4a8c97cb-9312-333e-2384-6a2a12aba398/448c4755-e462-0058-b108-d5f7b2af9eb8 NEW row; armor2clothing_preset:4af19514-66e8-1a2b-67d5-6528225681b4/448c4755-e462-0058-b108-d5f7b2af9eb8 NEW row; armor2clothing_preset:40129e7b-b9e0-a193-1145-d53292caf7a1/f6583131-1b13-4979-97f0-10f679cc3525 NEW row; armor2clothing_preset:4156d594-be4a-71c2-8ede-4d517ac668a5/f6583131-1b13-4979-97f0-10f679cc3525 NEW row; armor2clothing_preset:418864f6-f9c0-ead7-dd4e-6f3aacb0288c/f6583131-1b13-4979-97f0-10f67
- **Risk:** none

## 892 Baselard Dagger (P3, Weapons / armor / items)

- **What the author says (Nexus summary):** Adds a new custom 14th century baselard dagger.
- **File:** `Baselard Dagger Mod-892-1-0-2-1581856259.zip` (archive, 2.07 MB, `c_weapons-armor-items`), full (scratch, deleted after reading)
- **Grade:** B large | **gameplay perceptibility:** high | **visual/audio impact:** high | **layers:** D0 content/text; D1 data tables (PTF); D3 Lua scripts | **domain:** gameplay data, scripts, textures/models/animations, text
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `(none)`, loads on 1.9.8: yes (no version restriction)
- **Where it changes things:** tables (PTF): 7; textures: 4; models/animations/materials: 2; scripts (Lua): 2; localization: 2; manifest: 1; docs: 1; pak (container): 1; lua identical to vanilla: 0
- **Tables:** equippable_item, item, melee_weapon, pickable_item, player_item, shop_type2item, weapon (17 new rows, 0 changed, 0 identical to vanilla, 8614 vanilla rows dropped by a whole-table replace); median relative change 0.0
- **Largest changes:** equippable_item:0e7b2f6b-8ff1-4154-a2de-77f3defb7a7c NEW row; item:0e7b2f6b-8ff1-4154-a2de-77f3defb7a7c NEW row; melee_weapon:0e7b2f6b-8ff1-4154-a2de-77f3defb7a7c NEW row; pickable_item:0e7b2f6b-8ff1-4154-a2de-77f3defb7a7c NEW row; player_item:0e7b2f6b-8ff1-4154-a2de-77f3defb7a7c NEW row; weapon:0e7b2f6b-8ff1-4154-a2de-77f3defb7a7c NEW row; shop_type2item:0e7b2f6b-8ff1-4154-a2de-77f3defb7a7c NEW row; shop_type2item:0e7b2f6b-8ff1-4154-a2de-77f3defb7a7c NEW row
- **Lua:** 2 files, 30 lines; API used: System.LogAlwaysx2, player.inventoryx2, Database.LoadTablex1, Database.GetTableInfox1, Database.GetTableLinex1, Game.SendInfoTextx1
- **Text:** 0 strings changed, 2 new
- **Mentions:** states requirements
- **Risk:** none

## 966 15th to 16th Century style Ottoman sword (P3, Weapons / armor / items)

- **What the author says (Nexus summary):** A new model of 15th / 16th century  type Ottoman Turkish saber for people who want to act like Cumans in game :)
- **File:** `ottomansword-966-1-0-1584472459.rar` (archive, 3.13 MB, `c_weapons-armor-items`), full (scratch, deleted after reading)
- **Grade:** B large | **gameplay perceptibility:** high | **visual/audio impact:** high | **layers:** D0 content/text; D1 data tables (PTF); D3 Lua scripts | **domain:** gameplay data, scripts, textures/models/animations, text
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `ottomansword`, supports `(none)`, loads on 1.9.8: yes (no version restriction)
- **Where it changes things:** tables (PTF): 14; textures: 6; scripts (Lua): 4; models/animations/materials: 4; localization: 3; other: 2; manifest: 1; docs: 1; pak (container): 1; lua identical to vanilla: 0
- **Tables:** equippable_item, item, melee_weapon, pickable_item, player_item, shop_type2item, weapon (16 new rows, 0 changed, 0 identical to vanilla, 17228 vanilla rows dropped by a whole-table replace); median relative change 0.0
- **Largest changes:** equippable_item:ad9b8664-4d94-423e-9189-ff4ba8f22282 NEW row; item:ad9b8664-4d94-423e-9189-ff4ba8f22282 NEW row; melee_weapon:ad9b8664-4d94-423e-9189-ff4ba8f22282 NEW row; pickable_item:ad9b8664-4d94-423e-9189-ff4ba8f22282 NEW row; player_item:ad9b8664-4d94-423e-9189-ff4ba8f22282 NEW row; weapon:ad9b8664-4d94-423e-9189-ff4ba8f22282 NEW row; shop_type2item:ad9b8664-4d94-423e-9189-ff4ba8f22282 NEW row; shop_type2item:ad9b8664-4d94-423e-9189-ff4ba8f22282 NEW row
- **Lua:** 4 files, 60 lines; API used: System.LogAlwaysx4, player.inventoryx4, Database.LoadTablex2, Database.GetTableInfox2, Database.GetTableLinex2, Game.SendInfoTextx2
- **Text:** 0 strings changed, 4 new
- **Risk:** none

## 2383 Wooden Training Mace (unlisted, (not in the 365 index))

- **What the author says (Nexus summary):** -
- **File:** `TrainingMace 1.0.0 2383 1 2026-10-01T20-08Z GK8rEaXw5.zip` (archive, 0.09 MB, `_unmatched`), full (scratch, deleted after reading)
- **Grade:** B large | **gameplay perceptibility:** high | **visual/audio impact:** low | **layers:** D0 content/text; D1 data tables (PTF); D1 game data xml (not table rows) | **domain:** gameplay data, other game data (xml), text
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `(none)`, loads on 1.9.8: yes (no version restriction)
- **Where it changes things:** localization: 28; tables (PTF): 6; manifest: 1; docs: 1; pak (container): 1; other game data (xml, not table rows): 1; lua identical to vanilla: 0
- **Tables:** equippable_item, item, melee_weapon, pickable_item, player_item, weapon (6 new rows, 0 changed, 0 identical to vanilla, 7895 vanilla rows dropped by a whole-table replace); median relative change 0.0
- **Largest changes:** equippable_item:e53e6098-b10a-4efe-95fc-cd02bb489c69 NEW row; item:e53e6098-b10a-4efe-95fc-cd02bb489c69 NEW row; melee_weapon:e53e6098-b10a-4efe-95fc-cd02bb489c69 NEW row; pickable_item:e53e6098-b10a-4efe-95fc-cd02bb489c69 NEW row; player_item:e53e6098-b10a-4efe-95fc-cd02bb489c69 NEW row; weapon:e53e6098-b10a-4efe-95fc-cd02bb489c69 NEW row
- **Text:** 0 strings changed, 28 new
- **Mentions:** Vortex
- **Risk:** none

## 1909 Helmet-Off Dialog (Beta) (P3, Weapons / armor / items)

- **What the author says (Nexus summary):** This mod automatically unequips your helmet, head chainmail and coif when starting a conversation with an NPC, then re-equips them when the dialog ends.
- **File:** `Helmet-Off Dialog-1909-1-4-3-1743453648.zip` (archive, 0.02 MB, `c_weapons-armor-items`), full (scratch, deleted after reading)
- **Grade:** B large | **gameplay perceptibility:** high | **visual/audio impact:** none | **layers:** D3 Lua scripts | **domain:** scripts
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `helmet_off_dialog`, supports `(none)`, loads on 1.9.8: yes (no version restriction)
- **Where it changes things:** scripts (Lua): 19; manifest: 1; docs: 1; pak (container): 1; lua identical to vanilla: 0
- **Lua:** 19 files, 1654 lines; API used: System.LogAlwaysx86, player.soulx10, player.inventoryx6, player.actorx6, Script.LoadScriptx6, player.humanx2
- **Risk:** none

## 1309 Less Encounters (P3, Quests / lore / content)

- **What the author says (Nexus summary):** This makes changes to the chances of random encounters along roads (contact with various and often hostile NPCs).Useful for slow-paced players who wish to enjoy the atmosphere, habits and landscapes of the game.Vanilla meetings are too
- **File:** `less_encounters-1309-1-1640901979.zip` (archive, 0.0 MB, `c_quests-lore-content`), full (scratch, deleted after reading)
- **Grade:** C effective (few rows, strong effect) | **gameplay perceptibility:** high | **visual/audio impact:** none | **layers:** D1 data tables (PTF) | **domain:** gameplay data
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `(none)`, loads on 1.9.8: yes (no version restriction)
- **Where it changes things:** manifest: 1; pak (container): 1; other: 1; tables (PTF): 1; lua identical to vanilla: 0
- **Tables:** random_event (0 new rows, 85 changed, 0 identical to vanilla); median relative change 0.667
- **Largest changes:** random_event:2/0/3 map_disappear_time 11->0; random_event:1/4/6 map_disappear_time 11->0; random_event:2/7/4 map_disappear_time 11->0; random_event:0/8/7 map_game_speed 0->0.5; random_event:1/11/6 map_disappear_time 11->0; random_event:1/31/6 map_disappear_time 11->0; random_event:1/32/6 map_disappear_time 11->0; random_event:1/33/6 map_disappear_time 11->0
- **Problems:** less_encounters/Data/less_encounters.pak!Libs/Tables/random_event.xml: no suffix: replaces the whole vanilla table
- **Risk:** none

## 1423 Hoods and Scarfs UP (PTF - Dynamic - with Correct Meshes) (P3, Weapons / armor / items)

- **What the author says (Nexus summary):** Combines Ctobias and Hankyspanky69boi's previous mods and updates the files to EDIT things rather than overwrite them under the PTF framework.  This should improve functionality and compatibility
- **File:** `HoodsUp-1423-1-2-1673054605.rar` (archive, 0.01 MB, `c_weapons-armor-items`), full (scratch, deleted after reading)
- **Grade:** C effective (few rows, strong effect) | **gameplay perceptibility:** high | **visual/audio impact:** none | **layers:** D1 data tables (PTF) | **domain:** gameplay data
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `(none)`, loads on 1.9.8: yes (no version restriction)
- **Where it changes things:** tables (PTF): 3; manifest: 1; pak (container): 1; lua identical to vanilla: 0
- **Tables:** armor, clothing, clothing_preset (2 new rows, 79 changed, 0 identical to vanilla, 2536 vanilla rows dropped by a whole-table replace); median relative change 0.0
- **Largest changes:** armor:420f7feb-dc22-a2ec-b2a6-e1178f8c8386 clothing2_id ->4c33164c-a49d-54a8-7; armor:42e146c8-f2d1-1db1-c44c-7482b0f307b2 clothing2_id ->42a330c3-e603-86cb-b; armor:432237ec-b13a-bd6c-4026-a3db68e4d89e clothing2_id ->4c33164c-a49d-54a8-7; armor:45c1c6ff-b658-9ed5-5395-66d1ce58cf93 clothing2_id ->4c33164c-a49d-54a8-7; armor:4715c753-bafa-df3e-d3a6-c3fcd5d76f8c clothing2_id ->42a330c3-e603-86cb-b; armor:47aedf46-0047-053a-28f0-03e51a9f0baf clothing2_id ->4c33164c-a49d-54a8-7; armor:486c1cda-e1ec-5d01-b1f1-1540d0863c9e clothing2_id ->4c33164c-a49d-54a8-7; armor:48d624ae-0149-0854-2c41-82dba1f99088 clothing2_id ->42a330c3-e603-86cb-b
- **Risk:** none

## 1460 Merchants Have x3 Money (P3, Economy / merchants)

- **What the author says (Nexus summary):** Compatible with 1.9.6 as of 1/24/2023.It triples the amount of money every merchant has in the game.
- **File:** `For 1.9.6-1460-1-1674511920.rar` (archive, 0.03 MB, `c_economy-merchants`), full (scratch, deleted after reading)
- **Grade:** C effective (few rows, strong effect) | **gameplay perceptibility:** high | **visual/audio impact:** none | **layers:** D1 data tables (PTF) | **domain:** gameplay data
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `(none)`, loads on 1.9.8: yes (no version restriction)
- **Where it changes things:** manifest: 1; pak (container): 1; other: 1; tables (PTF): 1; lua identical to vanilla: 0
- **Tables:** shop_type2item (0 new rows, 78 changed, 1875 identical to vanilla); median relative change 2.0
- **Largest changes:** shop_type2item:5ef63059-322e-4e1b-abe8-926e100c770e amount 2800->8400; shop_type2item:5ef63059-322e-4e1b-abe8-926e100c770e amount 200->600; shop_type2item:5ef63059-322e-4e1b-abe8-926e100c770e amount 100->300; shop_type2item:5ef63059-322e-4e1b-abe8-926e100c770e amount 20000->60000; shop_type2item:5ef63059-322e-4e1b-abe8-926e100c770e amount 2000->6000; shop_type2item:5ef63059-322e-4e1b-abe8-926e100c770e amount 4000->12000; shop_type2item:5ef63059-322e-4e1b-abe8-926e100c770e amount 200->600; shop_type2item:5ef63059-322e-4e1b-abe8-926e100c770e amount 1500->4500
- **Problems:** MerchantsHavex3Money/Data/MerchantsHavex3Money.pak!Libs/Tables/shop/shop_type2item.xml: no suffix: replaces the whole vanilla table
- **Risk:** none

## 1308 Less Income Pribyslavitz (P3, Economy / merchants)

- **What the author says (Nexus summary):** This makes changes to periodic expenses and incomes generated by various buildings created in the new settlement, Pribyslavitz (or resulted after Judgements).Useful for slow-paced players who wish to enjoy the atmosphere, habits and
- **File:** `less_income_Pribyslavitz-1308-1-1640897693.zip` (archive, 0.0 MB, `c_economy-merchants`), full (scratch, deleted after reading)
- **Grade:** C effective (few rows, strong effect) | **gameplay perceptibility:** high | **visual/audio impact:** none | **layers:** D1 data tables (PTF) | **domain:** gameplay data
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `(none)`, loads on 1.9.8: yes (no version restriction)
- **Where it changes things:** other: 3; tables (PTF): 3; manifest: 1; pak (container): 1; lua identical to vanilla: 0
- **Tables:** new_homes_modifier_effect_structure, new_homes_objective, new_homes_structure_tier (0 new rows, 77 changed, 14 identical to vanilla); median relative change 0.9
- **Largest changes:** new_homes_structure_tier:11 people 13->38; new_homes_modifier_effect_structure:57/10 income 70->-7; new_homes_modifier_effect_structure:60/11 income 50->-5; new_homes_structure_tier:10 income 140->-14; new_homes_modifier_effect_structure:54/9 income 200->2; new_homes_objective:1 complete_limit 1200->12; new_homes_structure_tier:9 income 500->5; new_homes_modifier_effect_structure:49/4 income 250->5
- **Problems:** less_income_Pribyslavitz/Data/less_income_Pribyslavitz.pak!Libs/Tables/minigame/new_homes_modifier_effect_structure.xml: no suffix: replaces the whole vanilla table / less_income_Pribyslavitz/Data/less_income_Pribyslavitz.pak!Libs/Tables/minigame/new_homes_objective.xml: no suffix: replaces the whole vanilla table / less_income_Pribyslavitz/Data/less_income_Pribyslavitz.pak!Libs/Tables/minigame/new_homes_structure_tier.xml: no suffix: replaces the whole vanilla table
- **Risk:** none

## 483 Hoods and Scarfs UP (dynamic) (P3, Weapons / armor / items)

- **What the author says (Nexus summary):** This mod simply makes 37 hoods and 7 scarfs to be warn up and down (hoods and scarfs are dynamic)
- **File:** `Dynamic Hoods and Scarfs up and down-483-1-9-1590343806.zip` (archive, 0.11 MB, `c_weapons-armor-items`), full (scratch, deleted after reading)
- **Grade:** C effective (few rows, strong effect) | **gameplay perceptibility:** high | **visual/audio impact:** none | **layers:** D1 data tables (PTF) | **domain:** gameplay data
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `(none)`, loads on 1.9.8: yes (no version restriction)
- **Where it changes things:** other: 2; tables (PTF): 2; docs: 1; manifest: 1; pak (container): 1; lua identical to vanilla: 0
- **Tables:** armor, clothing_preset (0 new rows, 54 changed, 2142 identical to vanilla); median relative change 0.0
- **Largest changes:** armor:420f7feb-dc22-a2ec-b2a6-e1178f8c8386 clothing2_id ->4e7dfef5-2237-7fb4-0; armor:42e146c8-f2d1-1db1-c44c-7482b0f307b2 clothing2_id ->42a330c3-e603-86cb-b; armor:432237ec-b13a-bd6c-4026-a3db68e4d89e clothing2_id ->4c33164c-a49d-54a8-7; armor:45c1c6ff-b658-9ed5-5395-66d1ce58cf93 clothing2_id ->4e7dfef5-2237-7fb4-0; armor:4715c753-bafa-df3e-d3a6-c3fcd5d76f8c clothing2_id ->42a330c3-e603-86cb-b; armor:47aedf46-0047-053a-28f0-03e51a9f0baf clothing2_id ->4e7dfef5-2237-7fb4-0; armor:486c1cda-e1ec-5d01-b1f1-1540d0863c9e clothing2_id ->4e7dfef5-2237-7fb4-0; armor:48d624ae-0149-0854-2c41-82dba1f99088 clothing2_id ->42a330c3-e603-86cb-b
- **Problems:** zzz Hoods and Scarfs UP (dynamic)/Data/Hoods and Scarfs UP (dynamic).pak!Libs/Tables/item/armor.xml: no suffix: replaces the whole vanilla table / zzz Hoods and Scarfs UP (dynamic)/Data/Hoods and Scarfs UP (dynamic).pak!Libs/Tables/item/clothing_preset.xml: no suffix: replaces the whole vanilla table
- **Risk:** none

## 1311 Knightly Robard and Bernard (P3, Quests / lore / content)

- **What the author says (Nexus summary):** This mod equips the knights Sir Robard and Sir Bernard with appropriate armor.
- **File:** `Knightly Robard and Bernard-1311-1-1-1641324997.zip` (archive, 0.09 MB, `c_quests-lore-content`), full (scratch, deleted after reading)
- **Grade:** C effective (few rows, strong effect) | **gameplay perceptibility:** high | **visual/audio impact:** none | **layers:** D1 data tables (PTF) | **domain:** gameplay data
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `(none)`, loads on 1.9.8: yes (no version restriction)
- **Where it changes things:** other: 4; tables (PTF): 4; manifest: 1; pak (container): 1; lua identical to vanilla: 0
- **Tables:** armor2clothing_preset, clothing_preset, inventory_preset2item, soul (41 new rows, 12 changed, 3403 identical to vanilla, 13704 vanilla rows dropped by a whole-table replace); median relative change 0.0
- **Largest changes:** inventory_preset2item:45ff9e32-ee90-4051-f963-1058dd4360a4 NEW row; inventory_preset2item:19d5def6-e491-43c7-ab1d-5978ac197485 NEW row; inventory_preset2item:4af53552-ba45-84fc-7dea-aabc594a55a0 NEW row; inventory_preset2item:47d11f76-1007-00c0-1c63-cfb2b02b0c80 NEW row; armor2clothing_preset:19d5def6-e491-43c7-ab1d-5978ac197485/48a6f701-c6f4-b05a-6472-b8e8386d30a3 NEW row; armor2clothing_preset:4a8c97cb-9312-333e-2384-6a2a12aba398/48a6f701-c6f4-b05a-6472-b8e8386d30a3 NEW row; armor2clothing_preset:45edc80c-1b34-a0f5-001c-a08a1fe632a6/48a6f701-c6f4-b05a-6472-b8e8386d30a3 NEW row; armor2clothing_preset:44135951-cf1c-f2fd-15f0-0f0ea223a584/48a6f701-c6f4-b05a-6472-b8e8386d30a3 NEW row
- **Risk:** none

## 2079 Thin The Herd - Immersive Hunting and Realistic Animal Loot (P3, Crime / stealth / loot)

- **What the author says (Nexus summary):** Rebalances animal loot drops and quest requirements; PTF Realistic animal loot quantities with rebalanced hunting and meat-delivery quests.
- **File:** `Thin The Herd 2079 1.3.1 2026-07-16T19-00Z ksgvwCnjt.zip` (archive, 0.13 MB, `c_crime-stealth-loot`), full (scratch, deleted after reading)
- **Grade:** C effective (few rows, strong effect) | **gameplay perceptibility:** high | **visual/audio impact:** none | **layers:** D1 data tables (PTF); D1 game data xml (not table rows) | **domain:** gameplay data, other game data (xml)
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `(none)`, loads on 1.9.8: yes (no version restriction)
- **Where it changes things:** other game data (xml, not table rows): 3; tables (PTF): 3; docs: 2; manifest: 1; pak (container): 1; lua identical to vanilla: 0
- **Tables:** inventory2item, inventory_preset2item, quest_tracked_asset (2 new rows, 47 changed, 0 identical to vanilla, 3788 vanilla rows dropped by a whole-table replace); median relative change 0.96
- **Largest changes:** inventory_preset2item:87a65e52-dfa1-4b45-9306-0b7083f93c90 priority 0.05->1; inventory2item:a0a6a756-e204-4943-b215-543471b5cc39 amount_random_add 1->4; inventory2item:81c21fdc-3d62-4d1f-854f-eb364db1bcff amount 1->3; inventory2item:d1d1b932-4b23-4622-bd7e-b77ad40e29cd NEW row; inventory2item:4446bc26-efff-4117-b4f5-19ee9045847d amount 1->2; inventory2item:6f1d0e9e-d532-4476-af7a-e24ea01da040 amount 0->1; inventory2item:87a65e52-dfa1-4b45-9306-0b7083f93c90 NEW row; inventory2item:a1dda25f-3a35-4376-b198-4e5173c742a8 amount 0->1
- **Mentions:** states requirements
- **Risk:** none

## 129 Equal Horse Caparisons (P3, Horses)

- **What the author says (Nexus summary):** Players can change the colour/style of the padded quilt blanket armour (Caparison) on their horse without worry of stat changes, choice by colour/style not by stats!
- **File:** `Equal Caparisons Grouped-129--5-1758213686.zip` (archive, 0.0 MB, `c_horses`), full (scratch, deleted after reading)
- **Grade:** C effective (few rows, strong effect) | **gameplay perceptibility:** high | **visual/audio impact:** none | **layers:** D1 data tables (PTF) | **domain:** gameplay data
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `1.9.*`, loads on 1.9.8: yes (wildcard)
- **Where it changes things:** tables (PTF): 2; manifest: 1; pak (container): 1; lua identical to vanilla: 0
- **Tables:** armor, pickable_item (0 new rows, 44 changed, 2 identical to vanilla, 2960 vanilla rows dropped by a whole-table replace); median relative change 0.524
- **Largest changes:** armor:46ee8c8f-2c9a-3002-a31e-8623e2da529d slash_def 0.26->0.9; armor:402c55d2-ae62-bf47-823f-8a5760eab7bd slash_def 0.32->0.9; armor:4b609a17-9266-0e3e-75dc-d4d709533dba slash_def 0.32->0.9; pickable_item:46ee8c8f-2c9a-3002-a31e-8623e2da529d price 293->762; pickable_item:402c55d2-ae62-bf47-823f-8a5760eab7bd price 322->762; pickable_item:4b609a17-9266-0e3e-75dc-d4d709533dba price 322->762; armor:40a5de5a-d3a5-c4c3-f5f1-71ab661d55b4 slash_def 0.43->0.9; armor:411f568d-9e62-417c-38a1-ae108bb233ba smash_def 0.098->0.2
- **Risk:** none

## 2271 No Horse Manes (P3, Horses)

- **What the author says (Nexus summary):** Removes mane of horses that spawn with caparison, so it does not stick through the cloth. Optionally also removes mane of the player's horse.
- **File:** `NoHorseMane Basic 2271 1.0.1 2026-07-13T20-32Z NYwqvZpIg.zip` (archive, 0.02 MB, `c_horses`), full (scratch, deleted after reading)
- **Grade:** C effective (few rows, strong effect) | **gameplay perceptibility:** high | **visual/audio impact:** none | **layers:** D1 data tables (PTF) | **domain:** gameplay data
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `1.9.*`, loads on 1.9.8: yes (wildcard)
- **Where it changes things:** manifest: 1; pak (container): 1; tables (PTF): 1; lua identical to vanilla: 0
- **Tables:** soul (44 new rows, 0 changed, 0 identical to vanilla, 5025 vanilla rows dropped by a whole-table replace); median relative change 0.0
- **Largest changes:** soul:00000000-0000-0000-0000-000000035000/00000000-0000-0000-0000-000000045002//445d16d9-5798-b136-1d02-9859932ce5a4///4e33cb49-0ff2-a50b-8fac-be63bab45185/////3/7/4022aef9-9d0a-b0c3-1221-51c2bd7ebe85/0 NEW row; soul:00000000-0000-0000-0000-000000035000/00000000-0000-0000-0000-000000045002//445d16d9-5798-b136-1d02-9859932ce5a4///4e33cb49-0ff2-a50b-8fac-be63bab45185/////3/7/415108b4-41f8-2715-6d6d-de4686ada79d/0 NEW row; soul:00000000-0000-0000-0000-000000035000/494dad1a-adec-4fc8-983e-19d81e60eb9c//425451b6-ba9b-91d2-f3b5-9dc977ed0fb4////////3/7/41913183-e462-8ee0-779f-44404d093bb1/0 NEW row; soul:00000000-0000-0000-0000-000000035000/494dad1a-adec-4fc8-983e-19d81e60eb9c//42855b88-f189-7ee4-5
- **Risk:** none

## 837 Easy Edit (P3, (unclassified))

- **What the author says (Nexus summary):** Do you find it hard to read xml and edit what your looking for without having to jump back and forth between google and your xml to find item id's, names, buff id's ect ect. I set out to make modding easier for me but considering i'v spent
- **File:** `EasyEdit-837--1-1567314659.zip` (archive, 0.01 MB, `c_unclassified`), full (scratch, deleted after reading)
- **Grade:** C effective (few rows, strong effect) | **gameplay perceptibility:** high | **visual/audio impact:** none | **layers:** D1 data tables (PTF) | **domain:** gameplay data
- **How it installs:** loose .pak (legacy: copy into Data); manifest id `-`, supports `-`, loads on 1.9.8: no manifest (legacy install)
- **Where it changes things:** pak (container): 1; tables (PTF): 1; other: 1; lua identical to vanilla: 0
- **Tables:** food (0 new rows, 29 changed, 170 identical to vanilla, 3 vanilla rows dropped by a whole-table replace); median relative change 0.5
- **Largest changes:** food:5dceabb5-aef0-4bf5-b401-acbc30a44e21 nutrition_benefit -0.5->2; food:b3e363cf-8dde-4733-89a9-c468d5580d2e refresh_benefit 0.5->-2; food:6a324aa9-a566-406c-a3f8-6c416a00b399 refresh_benefit -0.5->-1.5; food:9e782670-3291-4382-a6d3-a843d13e67d9 refresh_benefit 10->-1; food:8d6964b1-b645-4aa1-adcc-db22646f3722 refresh_benefit 0->-3; food:55537a99-41ba-4497-925c-a543ced248e3 refresh_benefit 0->1; food:5f02ef0d-0551-44b1-902c-c96a8650d01d nutrition_benefit 0->2; food:86e4ff24-88db-4024-abe6-46545fa0fbd1 refresh_benefit 0->-3
- **Same rows as KRS:** krs_items:food:73ff1fde-ec8b-41e9-95e3-b5938c715bf1
- **Problems:** EasyEdit/Data/EasyEdit.pak!Libs/Tables/rpg/food.xml: no suffix: replaces the whole vanilla table
- **Risk:** none

## 1944 Lore Of Die (P3, Quests / lore / content)

- **What the author says (Nexus summary):** Expand how die's experienced in the game.
- **File:** `Lore Of Die Pricing Module-1944-1-0-1743087028.zip` (archive, 0.05 MB, `c_quests-lore-content`), full (scratch, deleted after reading)
- **Grade:** C effective (few rows, strong effect) | **gameplay perceptibility:** high | **visual/audio impact:** none | **layers:** D1 data tables (PTF) | **domain:** gameplay data
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `1.9.6`, loads on 1.9.8: NO (disabled: lists 1.9.6)
- **Where it changes things:** manifest: 1; pak (container): 1; other: 1; tables (PTF): 1; lua identical to vanilla: 0
- **Tables:** pickable_item (0 new rows, 20 changed, 1 identical to vanilla, 2189 vanilla rows dropped by a whole-table replace); median relative change 1.65
- **Largest changes:** pickable_item:c56c54b5-b113-41ce-a250-b4eb137909bc price 100->2300; pickable_item:045b5264-5840-43bf-90fb-d8635cd799cf price 500->3500; pickable_item:f3cf6a4e-4749-495e-91c7-3e935e2b301a price 500->3100; pickable_item:ff5efcee-a92f-406a-8c6f-518556c205da price 500->2100; pickable_item:29fb91de-5454-41b6-a591-c86c8d614db9 price 1000->4000; pickable_item:6d4602d4-790e-44f0-816b-96d514db0b7a price 500->2000; pickable_item:65ccc0cd-de18-4305-9d64-42bb3c6d8d30 price 500->2000; pickable_item:4ede7cfe-e698-4917-a092-a01d8ac3646f price 500->1800
- **Risk:** none

## 1562 Karnages_Polearm_Rebalance 2.0 (P3, Weapons / armor / items)

- **What the author says (Nexus summary):** a total overhaul of Polearms Damage
- **File:** `Karnage's_Polearm_Rebalance 2.0-1562-1-0-0-1700618129.7z` (archive, 0.0 MB, `c_weapons-armor-items`), full (scratch, deleted after reading)
- **Grade:** C effective (few rows, strong effect) | **gameplay perceptibility:** high | **visual/audio impact:** none | **layers:** D1 data tables (PTF) | **domain:** gameplay data
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `(none)`, loads on 1.9.8: yes (no version restriction)
- **Where it changes things:** manifest: 1; pak (container): 1; tables (PTF): 1; lua identical to vanilla: 0
- **Tables:** melee_weapon (0 new rows, 10 changed, 0 identical to vanilla, 157 vanilla rows dropped by a whole-table replace); median relative change 0.4
- **Largest changes:** melee_weapon:44940b6c-f1f9-4ad1-9419-b5705a88e5b0 smash_att_mod 0.05->0.5; melee_weapon:033fc7b6-17b6-486d-95cb-a22afb131be2 smash_att_mod 0.05->0.5; melee_weapon:7377215a-a0ca-44a2-b11a-113a024191ca smash_att_mod 0.05->0.5; melee_weapon:405c1865-413d-43b8-8db9-c44a0eefd350 smash_att_mod 0.05->0.5; melee_weapon:3ef71c79-57c2-4f28-8f31-a091d9b78798 slash_att_mod 0.05->0.25; melee_weapon:0f5be0ac-ff11-4a01-a7f4-bf8e84c2e31b smash_att_mod 0.1->0.4; melee_weapon:1f389792-6ddb-4060-8cc4-13bcc9117db8 smash_att_mod 0.25->0.57; melee_weapon:f2817f34-9e28-4b97-8f6c-d2b2a7aaa61b smash_att_mod 0.25->0.5
- **Risk:** none

## 1452 Storable Halberds (P3, Weapons / armor / items)

- **What the author says (Nexus summary):** Storable & useable Halberds like other melee weapon (sword, axe, mace).
- **File:** `Storable Halberds v1.0-1452-1-0-1673203304.rar` (archive, 0.0 MB, `c_weapons-armor-items`), full (scratch, deleted after reading)
- **Grade:** C effective (few rows, strong effect) | **gameplay perceptibility:** high | **visual/audio impact:** none | **layers:** D1 data tables (PTF) | **domain:** gameplay data
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `(none)`, loads on 1.9.8: yes (no version restriction)
- **Where it changes things:** manifest: 1; docs: 1; pak (container): 1; other: 1; tables (PTF): 1; lua identical to vanilla: 0
- **Tables:** weapon_class (2 new rows, 7 changed, 5 identical to vanilla, 2 vanilla rows dropped by a whole-table replace); median relative change 0.6
- **Largest changes:** weapon_class:/9//0/0/-1/22/0/1 NEW row; weapon_class:/0/8938ac5f-35d3-44dc-8251-97df7570b672/0/0/1/23/7/0 NEW row; weapon_class:/1//8/1/0/16/1/0 horse_pull_down_z_tolerance 0.5->0.2; weapon_class:/1//0/1/0/16/2/0 horse_pull_down_z_tolerance 0.5->0.2; weapon_class:/2//0/1/0/17/3/0 horse_pull_down_z_tolerance 0.5->0.2; weapon_class:bf861d60-b892-42a3-9c3b-d3787362f88b/1//8/1/0/16/4/0 horse_pull_down_z_tolerance 0.5->0.2; weapon_class:/2//0/2/0/21/5/0 horse_pull_down_z_tolerance 0.5->0.2; weapon_class:/1//0/5/0/24/12/0 horse_pull_down_z_tolerance 0.5->0.2
- **Problems:** Halberds/Data/StorableHalberds.pak!Libs/Tables/item/weapon_class.xml: no suffix: replaces the whole vanilla table
- **Risk:** none

## 2171 No Stolen Items (PTF) (P3, Crime / stealth / loot)

- **What the author says (Nexus summary):** Prevents stolen items from being identified as stolen. Items are immediately able to be sold. Immediately updates any stolen items in the player's inventory.
- **File:** `No Stolen Items-2171-1-2-1772686214.zip` (archive, 0.0 MB, `c_crime-stealth-loot`), full (scratch, deleted after reading)
- **Grade:** C effective (few rows, strong effect) | **gameplay perceptibility:** high | **visual/audio impact:** none | **layers:** D1 data tables (PTF) | **domain:** gameplay data
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `(none)`, loads on 1.9.8: yes (no version restriction)
- **Where it changes things:** manifest: 1; pak (container): 1; tables (PTF): 1; lua identical to vanilla: 0
- **Tables:** rpg_param (8 new rows, 0 changed, 0 identical to vanilla, 182 vanilla rows dropped by a whole-table replace); median relative change 0.0
- **Largest changes:** rpg_param:ItemOwnerFactionDistanceCoef1 NEW row; rpg_param:ItemOwnerFactionDistanceCoef2 NEW row; rpg_param:ItemOwnerFactionDistanceToSuspiciencyMax NEW row; rpg_param:ItemOwnerFactionDistanceToSuspiciencyMin NEW row; rpg_param:ItemOwnerFadeCoefToSuspiciencyExp NEW row; rpg_param:ItemOwnerFadeCoefToSuspiciencyMul NEW row; rpg_param:ItemOwnerFadeConspicuousnessToHours NEW row; rpg_param:ItemOwnerFadePriceToHours NEW row
- **Risk:** none

## 2202 Animals Looted Statistic Tracker - Separate from Corpses Looted (P3, Crime / stealth / loot)

- **What the author says (Nexus summary):** Splits the vanilla Corpses looted statistic into two separate tracked values: "Corpses looted" for human NPC corpses and "Animals looted" for animal corpses. The mod updates the in-game Player → Statistics → Crime screen automatically and
- **File:** `LootStatSplit-2202-1-1774557285.zip` (archive, 0.42 MB, `c_crime-stealth-loot`), full (scratch, deleted after reading)
- **Grade:** C effective (few rows, strong effect) | **gameplay perceptibility:** high | **visual/audio impact:** medium | **layers:** D0 content/text; D1 data tables (PTF); D2 engine config; D3 Lua scripts | **domain:** gameplay data, scripts, engine config, UI, text
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `1.*`, loads on 1.9.8: yes (wildcard)
- **Where it changes things:** ui: 4; docs: 3; pak (container): 3; scripts (Lua): 2; localization: 2; config (.cfg): 1; manifest: 1; tables (PTF): 1; lua identical to vanilla: 0
- **Tables:** statistic (1 new rows, 7 changed, 0 identical to vanilla, 176 vanilla rows dropped by a whole-table replace); median relative change 0.0
- **Largest changes:** statistic:/3/184// NEW row; statistic:/3/83// ui_order 73->74; statistic:/3/84/3/ ui_order 74->75; statistic:/3/10// ui_order 75->76; statistic:/3/23// ui_order 76->77; statistic:/3/90// ui_order 77->78; statistic:/3/93// ui_order 78->79; statistic:/3/94/1/ ui_order 79->80
- **Lua:** 2 files, 277 lines; API used: Script.ReloadScriptx52, System.LogAlwaysx8, XGenAIModule.LootBeginx2, Events.luax1
- **Config:** 1 keys, e.g. name=LootStatSplit
- **Text:** 0 strings changed, 1 new
- **Mentions:** mentions Tables.pak
- **Risk:** none

## 2022 Restored Sabres PTF (P3, Weapons / armor / items)

- **What the author says (Nexus summary):** Adds the previously unused Oriental Blade to the swordsmith’s shop with new textures. Allows enemies to use the Rider’s Sabre, which was not used by any enemies before. Buffs and balances the weak Nicopolis Sabre, making it usable while
- **File:** `Restored Sabres PTF-2022-1-1-1779784649.7z` (archive, 2.83 MB, `c_weapons-armor-items`), full (scratch, deleted after reading)
- **Grade:** C effective (few rows, strong effect) | **gameplay perceptibility:** high | **visual/audio impact:** medium | **layers:** D0 content/text; D1 data tables (PTF) | **domain:** gameplay data, textures/models/animations
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `1.9.4 1.9.5 1.9.6 1.9.7 1.9.8`, loads on 1.9.8: yes (explicit)
- **Where it changes things:** tables (PTF): 5; textures: 4; manifest: 1; pak (container): 1; lua identical to vanilla: 0
- **Tables:** melee_weapon, pickable_item, shop_type2item, weapon, weapon2weapon_preset (1 new rows, 5 changed, 1 identical to vanilla, 3449 vanilla rows dropped by a whole-table replace); median relative change 1.577
- **Largest changes:** melee_weapon:50ef44b2-73f9-412f-bb4b-29047887a11b slash_att_mod 0.75->3.8; pickable_item:50ef44b2-73f9-412f-bb4b-29047887a11b price 302->900; weapon:50ef44b2-73f9-412f-bb4b-29047887a11b max_status 23->50; shop_type2item:aca90050-0b70-4ca0-9d29-b94326203c75 NEW row; weapon2weapon_preset:ec470e0c-5bbd-43bb-803e-0e7867253c25 weapon_preset_id 463dc53f-86c2-5b8c-a->42b3ad6f-cc12-bcb2-e; weapon2weapon_preset:ec470e0c-5bbd-43bb-803e-0e7867253c25 weapon_preset_id 463dc53f-86c2-5b8c-a->48271a75-6e1e-269a-f
- **Risk:** none

## 1391 Better Equipped Runt (P3, Quests / lore / content)

- **What the author says (Nexus summary):** Runt with more pieces of armor for more realistic look and difficulty
- **File:** `Better Equipped Runt-1391-1-0-1655791454.zip` (archive, 0.0 MB, `c_quests-lore-content`), full (scratch, deleted after reading)
- **Grade:** C effective (few rows, strong effect) | **gameplay perceptibility:** high | **visual/audio impact:** none | **layers:** D1 data tables (PTF) | **domain:** gameplay data
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `(none)`, loads on 1.9.8: yes (no version restriction)
- **Where it changes things:** manifest: 1; pak (container): 1; other: 1; tables (PTF): 1; lua identical to vanilla: 0
- **Tables:** armor2clothing_preset (5 new rows, 0 changed, 8 identical to vanilla, 8676 vanilla rows dropped by a whole-table replace); median relative change 0.0
- **Largest changes:** armor2clothing_preset:4eee90c8-2406-357f-6d9f-8e8e4274b387/448c4755-e462-0058-b108-d5f7b2af9eb8 NEW row; armor2clothing_preset:4a946556-ee8b-ed84-ecf1-f848601cf486/448c4755-e462-0058-b108-d5f7b2af9eb8 NEW row; armor2clothing_preset:229d96aa-a435-4e89-85ce-8119a1df8228/448c4755-e462-0058-b108-d5f7b2af9eb8 NEW row; armor2clothing_preset:42de552f-eaac-ee43-5e36-129615d2b4ab/448c4755-e462-0058-b108-d5f7b2af9eb8 NEW row; armor2clothing_preset:4af19514-66e8-1a2b-67d5-6528225681b4/448c4755-e462-0058-b108-d5f7b2af9eb8 NEW row
- **Risk:** none

## 1093 Fishing in Bohemia (P3, Quests / lore / content)

- **What the author says (Nexus summary):** Only mentioned in a video of mods that still work; no page details seen Adds fishing to the lands of Bohemia!
- **File:** `Fishing in Bohemia 1.1-1093-1-1-1598974175.7z` (archive, 0.01 MB, `c_quests-lore-content`), full (scratch, deleted after reading)
- **Grade:** C effective (few rows, strong effect) | **gameplay perceptibility:** high | **visual/audio impact:** medium | **layers:** D0 content/text; D1 data tables (PTF); D3 Lua scripts | **domain:** gameplay data, scripts, UI, text
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `(none)`, loads on 1.9.8: yes (no version restriction)
- **Where it changes things:** tables (PTF): 4; ui: 2; scripts (Lua): 2; localization: 2; manifest: 1; pak (container): 1; lua identical to vanilla: 0
- **Tables:** item, pickable_item, player_item, questible_item (4 new rows, 0 changed, 0 identical to vanilla, 7378 vanilla rows dropped by a whole-table replace); median relative change 0.0
- **Largest changes:** item:2aef9b0a-f485-4935-be7d-7ceee381b546 NEW row; pickable_item:2aef9b0a-f485-4935-be7d-7ceee381b546 NEW row; player_item:2aef9b0a-f485-4935-be7d-7ceee381b546 NEW row; questible_item:2aef9b0a-f485-4935-be7d-7ceee381b546 NEW row
- **Lua:** 2 files, 158 lines; API used: player.inventoryx9, System.LogAlwaysx4, Game.SendInfoTextx4, System.GetEntitiesInSpherex3, Database.LoadTablex1, Database.GetTableInfox1
- **Text:** 0 strings changed, 8 new
- **Risk:** none

## 1984 Sharpening Overhaul (P3, Weapons / armor / items)

- **What the author says (Nexus summary):** Overhauls Grindstone and sharpening of weapons.
- **File:** `Sharpening Overhaul-1984-2-1-1749895972.zip` (archive, 0.01 MB, `c_weapons-armor-items`), full (scratch, deleted after reading)
- **Grade:** C effective (few rows, strong effect) | **gameplay perceptibility:** high | **visual/audio impact:** low | **layers:** D0 content/text; D1 data tables (PTF); D3 Lua scripts | **domain:** gameplay data, scripts, textures/models/animations, text
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `1.9.6`, loads on 1.9.8: NO (disabled: lists 1.9.6)
- **Where it changes things:** scripts (Lua): 7; localization: 2; manifest: 1; pak (container): 1; tables (PTF): 1; textures: 1; other: 1; lua identical to vanilla: 0
- **Tables:** buff (4 new rows, 0 changed, 0 identical to vanilla, 439 vanilla rows dropped by a whole-table replace); median relative change 0.0
- **Largest changes:** buff:f7985d3c-dfc5-4d65-a6a9-238cefc1fa39 NEW row; buff:38e2c0a5-90b4-4e99-8d95-19e2a137ff6d NEW row; buff:2180e3d9-0a1d-42c1-bf49-d2bdf8c89d88 NEW row; buff:4cd02867-5583-4b68-b5c0-0ad5b362f9d0 NEW row
- **Lua:** 7 files, 445 lines; API used: player.soulx5, Script.ReloadScriptx5, System.GetEntityx3, Script.SetTimerx3, System.GetCurrTimex3, player.thisx2
- **Text:** 0 strings changed, 23 new
- **Risk:** none

## 1330 Noble Sir Hans (P3, Quests / lore / content)

- **What the author says (Nexus summary):** Changes Sir Hans' outfit to look more noble
- **File:** `Noble Sir Hans-1330-1-1-1645324411.zip` (archive, 0.0 MB, `c_quests-lore-content`), full (scratch, deleted after reading)
- **Grade:** C effective (few rows, strong effect) | **gameplay perceptibility:** high | **visual/audio impact:** none | **layers:** D1 data tables (PTF) | **domain:** gameplay data
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `(none)`, loads on 1.9.8: yes (no version restriction)
- **Where it changes things:** manifest: 1; pak (container): 1; other: 1; tables (PTF): 1; lua identical to vanilla: 0
- **Tables:** armor2clothing_preset (3 new rows, 0 changed, 3 identical to vanilla, 8681 vanilla rows dropped by a whole-table replace); median relative change 0.0
- **Largest changes:** armor2clothing_preset:46a124e4-481c-5880-d187-573c1d8a57b9/4a15d408-3c02-7dbe-6615-e2fbe6dca0a1 NEW row; armor2clothing_preset:4d253305-bc59-a0b0-1d6f-ff202e1aaf89/4a15d408-3c02-7dbe-6615-e2fbe6dca0a1 NEW row; armor2clothing_preset:af6f2946-ce54-4e38-9b2b-5ab95d5c4777/4a15d408-3c02-7dbe-6615-e2fbe6dca0a1 NEW row
- **Risk:** none

## 1861 Sell Damaged Items At Full Price - PTF (P3, Economy / merchants)

- **What the author says (Nexus summary):** Damaged items sell at full price; PTF With this mod, you can sell damaged items at their full price (as if they were in perfect condition) - PFT (should be compatible with PTF mods).
- **File:** `Sell Damaged Items At Full Price-1861-1-0-1739532223.zip` (archive, 0.0 MB, `c_economy-merchants`), full (scratch, deleted after reading)
- **Grade:** C effective (few rows, strong effect) | **gameplay perceptibility:** high | **visual/audio impact:** none | **layers:** D1 data tables (PTF) | **domain:** gameplay data
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `selldamagedfullprice`, supports `(none)`, loads on 1.9.8: yes (no version restriction)
- **Where it changes things:** tables (PTF): 2; manifest: 1; pak (container): 1; lua identical to vanilla: 0
- **Tables:** perk_rpg_param_override (1 new rows, 1 changed, 0 identical to vanilla, 49 vanilla rows dropped by a whole-table replace); median relative change 1.0
- **Largest changes:** perk_rpg_param_override:01c3b32a-5751-4c98-b6ab-258d02370382/ItemHealthPriceStatusWeight rpg_param_value 0.85->0; perk_rpg_param_override:/ItemHealthPriceStatusWeight NEW row
- **Risk:** none

## 1259 Easy Assassination (P3, Crime / stealth / loot)

- **What the author says (Nexus summary):** Easier knock-out and sneak kills Improve Knock out & Sneak Kill. No more reloading to stealth kill/ knock out!
- **File:** `EasyAssassination 1.1-1259-1-1-1628879677.zip` (archive, 0.0 MB, `c_crime-stealth-loot`), full (scratch, deleted after reading)
- **Grade:** C effective (few rows, strong effect) | **gameplay perceptibility:** high | **visual/audio impact:** none | **layers:** D1 data tables (PTF); D1 game data xml (not table rows) | **domain:** gameplay data, other game data (xml)
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `(none)`, loads on 1.9.8: yes (no version restriction)
- **Where it changes things:** manifest: 1; pak (container): 1; tables (PTF): 1; other game data (xml, not table rows): 1; lua identical to vanilla: 0
- **Tables:** rpg_param (0 new rows, 1 changed, 0 identical to vanilla, 181 vanilla rows dropped by a whole-table replace); median relative change 4.0
- **Largest changes:** rpg_param:StealthKillProbCoefA rpg_param_value 4->20
- **Risk:** none

## 1510 Mount while encumbered (P3, Horses)

- **What the author says (Nexus summary):** Allows mounting of your horse even with encumbrance factor of 10.
- **File:** `mount_while_encumbered-1510-1-0-1684251631.zip` (archive, 0.0 MB, `c_horses`), full (scratch, deleted after reading)
- **Grade:** C effective (few rows, strong effect) | **gameplay perceptibility:** high | **visual/audio impact:** none | **layers:** D1 data tables (PTF) | **domain:** gameplay data
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `(none)`, loads on 1.9.8: yes (no version restriction)
- **Where it changes things:** manifest: 1; pak (container): 1; tables (PTF): 1; lua identical to vanilla: 0
- **Tables:** rpg_param (0 new rows, 1 changed, 0 identical to vanilla, 181 vanilla rows dropped by a whole-table replace); median relative change 5.667
- **Largest changes:** rpg_param:HorseMountMaxRelativeEncumberance rpg_param_value 1.5->10
- **Risk:** none

## 1548 Immersive Economy (P3, Economy / merchants)

- **What the author says (Nexus summary):** Base game Henry earns way too much money considering his position, this mod tries to remedy it a bit.
- **File:** `Immersive Economy-1548-1-1-1696198684.7z` (archive, 0.0 MB, `c_economy-merchants`), full (scratch, deleted after reading)
- **Grade:** C effective (few rows, strong effect) | **gameplay perceptibility:** high | **visual/audio impact:** none | **layers:** D1 data tables (PTF) | **domain:** gameplay data
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `1.9.4 1.9.5 1.9.6`, loads on 1.9.8: NO (disabled: lists 1.9.4, 1.9.5, 1.9.6)
- **Where it changes things:** tables (PTF): 2; manifest: 1; pak (container): 1; lua identical to vanilla: 0
- **Tables:** rpg_param (0 new rows, 1 changed, 0 identical to vanilla, 181 vanilla rows dropped by a whole-table replace); median relative change 0.25
- **Largest changes:** rpg_param:ItemHealthPriceStatusWeight rpg_param_value 0.8->1
- **Problems:** ImmersiveEconomy/Data/immersive_economy.pak!Libs/Tables/rpg/rpg_param.xml: no suffix: replaces the whole vanilla table / ImmersiveEconomy/Data/immersive_economy.pak!Libs/Tables/shop/shop.xml: not a readable table (malformed XML, or not a table): the game would reject or ignore it
- **Risk:** none

## 667 Naked Armor Fix (P3, Weapons / armor / items)

- **What the author says (Nexus summary):** Fix the player naked armor, so you are not overpowered anymore in Stealth missions.
- **File:** `Naked Armor Fix 1.1-667-1-1-1545056415.zip` (archive, 0.0 MB, `c_weapons-armor-items`), full (scratch, deleted after reading)
- **Grade:** D small tweak | **gameplay perceptibility:** medium | **visual/audio impact:** none | **layers:** D1 data tables (PTF) | **domain:** gameplay data
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `(none)`, loads on 1.9.8: yes (no version restriction)
- **Where it changes things:** docs: 1; manifest: 1; pak (container): 1; other: 1; tables (PTF): 1; lua identical to vanilla: 0
- **Tables:** soul_archetype (15 new rows, 0 changed, 0 identical to vanilla, 16 vanilla rows dropped by a whole-table replace); median relative change 0.0
- **Largest changes:** soul_archetype:0/0/0 NEW row; soul_archetype:1/0/1 NEW row; soul_archetype:2/0/2 NEW row; soul_archetype:3/1/3 NEW row; soul_archetype:3/2/4 NEW row; soul_archetype:3/3/5 NEW row; soul_archetype:3/4/6 NEW row; soul_archetype:3/5/7 NEW row
- **Problems:** zzz_NakedArmorFix_1.1/Data/zzz_NakedArmorFix_1.1.pak!Libs/Tables/rpg/soul_archetype.xml: no suffix: replaces the whole vanilla table
- **Risk:** none

## 1981 Lesser Income Pribyslavitz - Supplies Cost Patch (P3, Economy / merchants)

- **What the author says (Nexus summary):** Tiny mod to revert some supplies costs from Lesser Income Pribyslavitz.
- **File:** `LIP - Annual Contract Supplies Cost Patch-1981-1-0-1744439495.zip` (archive, 0.0 MB, `c_economy-merchants`), full (scratch, deleted after reading)
- **Grade:** D small tweak | **gameplay perceptibility:** medium | **visual/audio impact:** none | **layers:** D1 data tables (PTF) | **domain:** gameplay data
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `1.9.6`, loads on 1.9.8: NO (disabled: lists 1.9.6)
- **Where it changes things:** manifest: 1; pak (container): 1; tables (PTF): 1; lua identical to vanilla: 0
- **Tables:** new_homes_modifier_effect_structure (0 new rows, 8 changed, 0 identical to vanilla, 64 vanilla rows dropped by a whole-table replace); median relative change 9.5
- **Largest changes:** new_homes_modifier_effect_structure:8/8 income -120->-2184; new_homes_modifier_effect_structure:9/8 income -80->-1740; new_homes_modifier_effect_structure:12/8 income -30->-550; new_homes_modifier_effect_structure:14/8 income -50->-950; new_homes_modifier_effect_structure:13/8 income -70->-700; new_homes_modifier_effect_structure:7/8 income -160->-1540; new_homes_modifier_effect_structure:10/8 income -220->-650; new_homes_modifier_effect_structure:11/8 income -180->-450
- **Risk:** none

## 1092 Pollax replacer (Axe and Hammer head interchangable) (P3, Weapons / armor / items)

- **What the author says (Nexus summary):** Replaces lucerne hammer with a pollax model. Comes with an optional script that will allow you to swap between the axe and hammer head in game in real time.
- **File:** `pollax-1092-1-4-1601148804.7z` (archive, 0.09 MB, `c_weapons-armor-items`), full (scratch, deleted after reading)
- **Grade:** D small tweak | **gameplay perceptibility:** medium | **visual/audio impact:** high | **layers:** D0 content/text; D1 data tables (PTF) | **domain:** gameplay data, textures/models/animations, text
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `(none)`, loads on 1.9.8: yes (no version restriction)
- **Where it changes things:** tables (PTF): 2; models/animations/materials: 2; localization: 2; manifest: 1; pak (container): 1; lua identical to vanilla: 0
- **Tables:** pickable_item, player_item (0 new rows, 2 changed, 0 identical to vanilla, 4322 vanilla rows dropped by a whole-table replace); median relative change 0.0
- **Largest changes:** pickable_item:3ef71c79-57c2-4f28-8f31-a091d9b78798 model weapons/long_weapons->weapons/war_hammers/; player_item:3ef71c79-57c2-4f28-8f31-a091d9b78798 ui_info ui_in_lucerne_hammer->ui_in_pollax
- **Text:** 0 strings changed, 2 new
- **Risk:** none

## 1981 Lesser Income Pribyslavitz - Supplies Cost Patch (P3, Economy / merchants)

- **What the author says (Nexus summary):** Tiny mod to revert some supplies costs from Lesser Income Pribyslavitz.
- **File:** `LIP - Supplies Cost Patch-1981-1-1-1744439433.zip` (archive, 0.0 MB, `c_economy-merchants`), full (scratch, deleted after reading)
- **Grade:** D small tweak | **gameplay perceptibility:** low | **visual/audio impact:** none | **layers:** D1 data tables (PTF) | **domain:** gameplay data
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `1.9.6`, loads on 1.9.8: NO (disabled: lists 1.9.6)
- **Where it changes things:** manifest: 1; pak (container): 1; tables (PTF): 1; lua identical to vanilla: 0
- **Tables:** new_homes_modifier_effect_structure (0 new rows, 2 changed, 6 identical to vanilla, 64 vanilla rows dropped by a whole-table replace); median relative change 1.727
- **Largest changes:** new_homes_modifier_effect_structure:10/8 income -220->-650; new_homes_modifier_effect_structure:11/8 income -180->-450
- **Risk:** none

## 1654 Boots with Common Plate Chausses (P3, Weapons / armor / items)

- **What the author says (Nexus summary):** Allows the player to wear any boots with the shoe-less variant of the Common plate chausses
- **File:** `Plate Legs-1654-1-0-1716846598.7z` (archive, 0.0 MB, `c_weapons-armor-items`), full (scratch, deleted after reading)
- **Grade:** D small tweak | **gameplay perceptibility:** low | **visual/audio impact:** none | **layers:** D1 data tables (PTF) | **domain:** gameplay data
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `1.9.4 1.9.5 1.9.6`, loads on 1.9.8: NO (disabled: lists 1.9.4, 1.9.5, 1.9.6)
- **Where it changes things:** manifest: 1; pak (container): 1; tables (PTF): 1; lua identical to vanilla: 0
- **Tables:** clothing (1 new rows, 0 changed, 0 identical to vanilla, 419 vanilla rows dropped by a whole-table replace); median relative change 0.0
- **Largest changes:** clothing:55/4ec05c66-af3e-7f25-c995-3a432314c789/1/0 NEW row
- **Risk:** none

## 2288 Light Armour Vambraces (P3, Weapons / armor / items)

- **What the author says (Nexus summary):** Simple, lightweight and effective. The mod changes Vambraces to be classified as light armour, no other items or stats changed.
- **File:** `Lightarmvam 2288 1 2026-07-16T21-14Z ZWdhR2r8c.zip` (archive, 0.0 MB, `c_weapons-armor-items`), full (scratch, deleted after reading)
- **Grade:** D small tweak | **gameplay perceptibility:** medium | **visual/audio impact:** none | **layers:** D1 data tables (PTF) | **domain:** gameplay data
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `(none)`, loads on 1.9.8: yes (no version restriction)
- **Where it changes things:** manifest: 1; pak (container): 1; tables (PTF): 1; lua identical to vanilla: 0
- **Tables:** armor (0 new rows, 1 changed, 0 identical to vanilla, 795 vanilla rows dropped by a whole-table replace); median relative change 0.0
- **Largest changes:** armor:4573af03-8382-d87c-93aa-5dbb6fc79698 armor_type_id 5->2
- **Risk:** none

## 2369 Fewer Tournaments (P3, Crime / stealth / loot)

- **What the author says (Nexus summary):** This mod lets you choose how often the Rattay Tournament should occur, replacing the weekly cycle with longer intervals to stop constant notification spam.
- **File:** `Rattay Tournament 15 Days Cycle 2369 1.0 2026-09-19T12-07Z ZWdhR2rgE.zip` (archive, 0.22 MB, `c_crime-stealth-loot`), full (scratch, deleted after reading)
- **Grade:** D small tweak | **gameplay perceptibility:** low | **visual/audio impact:** none | **layers:** D1 data tables (PTF) | **domain:** gameplay data
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `(none)`, loads on 1.9.8: yes (no version restriction)
- **Where it changes things:** manifest: 1; pak (container): 1; other: 1; tables (PTF): 1; lua identical to vanilla: 0
- **Tables:** quest_objective (0 new rows, 1 changed, 9196 identical to vanilla); median relative change 0.0
- **Largest changes:** quest_objective:4/123694193 autocomplete_timeout_str 5d #WT->13d #WT
- **Problems:** RattayTournament15Days/Data/RattayTournament15Days.pak!Libs/Tables/quest/quest_objective.xml: no suffix: replaces the whole vanilla table
- **Risk:** none

## 326 Knox's Labelled Items (XML) (P3, Tools / reference)

- **What the author says (Nexus summary):** Knox's Labelled Items is a mod resource which aims to make adjusting equipment (all weapons and armour/clothing) variables much easier by including each item's in-game name in commented XML.
- **File:** `Knox's Labelled Items (XML)-326-1-0-2.zip` (archive, 0.25 MB, `c_tools-reference`), full (scratch, deleted after reading)
- **Grade:** D small tweak | **gameplay perceptibility:** medium | **visual/audio impact:** none | **layers:** D1 game data xml (not table rows) | **domain:** other game data (xml)
- **How it installs:** unclear: read the archive's own instructions; manifest id `-`, supports `-`, loads on 1.9.8: no manifest (legacy install)
- **Where it changes things:** other game data (xml, not table rows): 9; docs: 1; lua identical to vanilla: 0
- **Risk:** none

## 657 Binoculars Zoom (unlisted, (not in the 365 index))

- **What the author says (Nexus summary):** -
- **File:** `BinocularsZoom-657-1-1-1542038638.zip` (archive, 0.0 MB, `_unmatched`), full (scratch, deleted after reading)
- **Grade:** D small tweak | **gameplay perceptibility:** medium | **visual/audio impact:** none | **layers:** D3 Lua scripts | **domain:** scripts
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `(none)`, loads on 1.9.8: yes (no version restriction)
- **Where it changes things:** docs: 1; config (.cfg): 1; manifest: 1; pak (container): 1; scripts (Lua): 1; lua identical to vanilla: 0
- **Lua:** 1 files, 81 lines; API used: System.AddCCommandx2, System.GetCVarx2, System.ExecuteCommandx1
- **Mentions:** user.cfg
- **Risk:** none

## 800 Volumetric Fog Shadows (P4, Graphics config (cfg))

- **What the author says (Nexus summary):** This mod turns on volumetric shadows for fog, making it look better and more realistic.
- **File:** `VolumetricFogShadows-800-1-1-1563786542` (folder (already extracted), 0 MB, `c_graphics-config-cfg`), read in place (already extracted by the author)
- **Grade:** D small tweak | **gameplay perceptibility:** medium | **visual/audio impact:** medium | **layers:** D1 game data xml (not table rows); D2 engine config | **domain:** other game data (xml), graphics config
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `1.9.*`, loads on 1.9.8: yes (wildcard)
- **Where it changes things:** config (.cfg): 2; pak (container): 2; other game data (xml, not table rows): 2; manifest: 1; lua identical to vanilla: 0
- **Config:** 2 keys, e.g. r_FogShadows=1, r_FogShadows=2
- **Risk:** none

## 867 APEX Realistic Modding Guide tweaks and fixes (P3, Tools / reference)

- **What the author says (Nexus summary):** I try to explain here everything step by step to let your game look as realistic as possible :D
- **File:** `cfg files-867-1-4-1585770880.7z` (archive, 0.0 MB, `c_tools-reference`), full (scratch, deleted after reading)
- **Grade:** D small tweak | **gameplay perceptibility:** medium | **visual/audio impact:** high | **layers:** D2 engine config | **domain:** engine config, graphics config
- **How it installs:** unclear: read the archive's own instructions; manifest id `-`, supports `-`, loads on 1.9.8: no manifest (legacy install)
- **Where it changes things:** config (.cfg): 3; lua identical to vanilla: 0
- **Config:** 118 keys, e.g. ac_disableLivingVsLivingCollisions=1, ac_disableLivingVsRigidCollisions=1, ac_enableExtraSolidCollider=0, ac_enableProceduralLeaning=0, ai_ExtraActorAvoidanceRadius=0, ai_ExtraAvoidanceRadius=0, ai_useMNM=1, ca_CharEditModel="Objects/characters/humans/skeleton/male.cdf"
- **Risk:** none

## 930 Photorealistic Beauty (P3, World / weather / visuals)

- **What the author says (Nexus summary):** A photorealistic/realistic Reshade preset, made with the idea to recreate the perception of the real world by the eyes more than a camera even though pictures and videos are been used to make comparisions
- **File:** `Photorealistic Beauty 3.0-930-3-0-1584403800.zip` (archive, 9.64 MB, `c_world-weather-visuals`), full (scratch, deleted after reading)
- **Grade:** D small tweak | **gameplay perceptibility:** medium | **visual/audio impact:** high | **layers:** D0 content/text; D2 engine config | **domain:** engine config, graphics config, post-processing (ReShade/ENB)
- **How it installs:** legacy: files go into the game's Bin folder; manifest id `-`, supports `-`, loads on 1.9.8: no manifest (legacy install)
- **Where it changes things:** reshade/ENB (shaders, presets): 174; config (.cfg): 2; lua identical to vanilla: 0
- **Config:** 130 keys, e.g. ac_disableLivingVsLivingCollisions=1, ac_disableLivingVsRigidCollisions=1, ac_enableExtraSolidCollider=0, ac_enableProceduralLeaning=0, ai_ExtraActorAvoidanceRadius=0, ai_ExtraAvoidanceRadius=0, ai_useMNM=1, ca_CharEditModel="Objects/characters/humans/skeleton/male.cdf"
- **Risk:** none

## 1045 MORE BLOOD (P3, World / weather / visuals)

- **What the author says (Nexus summary):** More blood particles spawned on hit, making your enemies bleed longer and your hits more satisfying!
- **File:** `More blood-1045-0-2-2-1592095918.zip` (archive, 0.01 MB, `c_world-weather-visuals`), full (scratch, deleted after reading)
- **Grade:** D small tweak | **gameplay perceptibility:** medium | **visual/audio impact:** none | **layers:** D1 game data xml (not table rows) | **domain:** other game data (xml)
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `*`, loads on 1.9.8: NO (disabled: lists *)
- **Where it changes things:** other game data (xml, not table rows): 2; manifest: 1; pak (container): 1; lua identical to vanilla: 0
- **Risk:** none

## 1063 Paper UI (P3, Maps / UI / HUD)

- **What the author says (Nexus summary):** A paper retexture of the KCD user interface.
- **File:** `PaperUI-1063-1-0-1593630274.rar` (archive, 2.71 MB, `c_maps-ui-hud`), full (scratch, deleted after reading)
- **Grade:** D small tweak | **gameplay perceptibility:** medium | **visual/audio impact:** high | **layers:** D0 content/text; D1 game data xml (not table rows) | **domain:** other game data (xml), textures/models/animations
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `(none)`, loads on 1.9.8: yes (no version restriction)
- **Where it changes things:** textures: 83; manifest: 1; pak (container): 1; other game data (xml, not table rows): 1; lua identical to vanilla: 0
- **Risk:** none

## 1227 30 FPS Cutscene Fix V3 (P4, Graphics config (cfg))

- **What the author says (Nexus summary):** V3 Update: Thanks to webspam the mod should now work without spamming the console and automatically set your in game max FPS. V2 Update: Automatically increases FPS, no keybind required anymore!A very basic mod to increase the fps of the in
- **File:** `CutsceneFPSFixV3-1227-3-0-1766546982.zip` (archive, 0.0 MB, `c_graphics-config-cfg`), full (scratch, deleted after reading)
- **Grade:** D small tweak | **gameplay perceptibility:** medium | **visual/audio impact:** none | **layers:** D3 Lua scripts | **domain:** scripts
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `(none)`, loads on 1.9.8: yes (no version restriction)
- **Where it changes things:** scripts (Lua): 2; manifest: 1; pak (container): 1; other: 1; lua identical to vanilla: 0
- **Lua:** 2 files, 130 lines; API used: System.LogAlwaysx6, System.GetCVarx1, System.SetCVarx1, Game.ShowTutorialx1, System.SpawnEntityx1
- **Risk:** none

## 1322 Mutt Be Quiet (P3, Animations / audio)

- **What the author says (Nexus summary):** Removes the annoying howling from Mutt
- **File:** `Mutt Be Quiet-1322-1-0-1642520795.7z` (archive, 0.0 MB, `c_animations-audio`), full (scratch, deleted after reading)
- **Grade:** D small tweak | **gameplay perceptibility:** medium | **visual/audio impact:** none | **layers:** D1 game data xml (not table rows) | **domain:** other game data (xml)
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `1.9.*`, loads on 1.9.8: yes (wildcard)
- **Where it changes things:** manifest: 1; docs: 1; pak (container): 1; other game data (xml, not table rows): 1; lua identical to vanilla: 0
- **Risk:** none

## 1327 Weather Overhaul (P3, World / weather / visuals)

- **What the author says (Nexus summary):** Personally I wasn't a huge fan of one particular weather type, which made it rain a lot during sunny days, now that type of weather should look more like a rainy day.NOW WITH DLC SUPPORT!
- **File:** `Weather Overhaul DLC-1327-1-2-1669068726.7z` (archive, 0.04 MB, `c_world-weather-visuals`), full (scratch, deleted after reading)
- **Grade:** D small tweak | **gameplay perceptibility:** medium | **visual/audio impact:** none | **layers:** D1 game data xml (not table rows) | **domain:** other game data (xml)
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `1.9.*`, loads on 1.9.8: yes (wildcard)
- **Where it changes things:** pak (container): 2; other game data (xml, not table rows): 2; manifest: 1; docs: 1; lua identical to vanilla: 0
- **Risk:** none

## 1327 Weather Overhaul (P3, World / weather / visuals)

- **What the author says (Nexus summary):** Personally I wasn't a huge fan of one particular weather type, which made it rain a lot during sunny days, now that type of weather should look more like a rainy day.NOW WITH DLC SUPPORT!
- **File:** `Weather Overhaul-1327-1-2-1669068697.7z` (archive, 0.04 MB, `c_world-weather-visuals`), full (scratch, deleted after reading)
- **Grade:** D small tweak | **gameplay perceptibility:** medium | **visual/audio impact:** none | **layers:** D1 game data xml (not table rows) | **domain:** other game data (xml)
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `1.9.*`, loads on 1.9.8: yes (wildcard)
- **Where it changes things:** manifest: 1; docs: 1; pak (container): 1; other game data (xml, not table rows): 1; lua identical to vanilla: 0
- **Risk:** none

## 1332 Less Headbob (P3, Animations / audio)

- **What the author says (Nexus summary):** This mod makes headbob less annoying
- **File:** `KCB Less Headbob-1332-1-0-1644512525.7z` (archive, 0.0 MB, `c_animations-audio`), full (scratch, deleted after reading)
- **Grade:** D small tweak | **gameplay perceptibility:** medium | **visual/audio impact:** none | **layers:** D3 Lua scripts | **domain:** scripts
- **How it installs:** unclear: read the archive's own instructions; manifest id `-`, supports `-`, loads on 1.9.8: no manifest (legacy install)
- **Where it changes things:** scripts (Lua): 1; lua identical to vanilla: 0
- **Lua:** 1 files, 33 lines; API used: -
- **Risk:** none

## 1342 Adjusted Ultra Graphics Config (P4, Graphics config (cfg))

- **What the author says (Nexus summary):** A config for better performance using Ultra graphic settings. Improves texture streaming, LODs, lighting, and tweaked shadows for increased FPS.
- **File:** `Adjusted Config-1342-1-0-1666308185.zip` (archive, 0.0 MB, `c_graphics-config-cfg`), full (scratch, deleted after reading)
- **Grade:** D small tweak | **gameplay perceptibility:** medium | **visual/audio impact:** high | **layers:** D2 engine config | **domain:** engine config, graphics config
- **How it installs:** unclear: read the archive's own instructions; manifest id `-`, supports `-`, loads on 1.9.8: no manifest (legacy install)
- **Where it changes things:** config (.cfg): 1; docs: 1; lua identical to vanilla: 0
- **Config:** 46 keys, e.g. con_restricted=0, e_LodFaceAreaTargetSize=0.0008, e_MergedMeshesActiveDist=300, e_MergedMeshesLodRatio=16, e_MergedMeshesViewDistRatio=125, e_ShadowsCastViewDistRatio=0.8, e_ShadowsCastViewDistRatioLights=0.3, e_ShadowsCastViewDistRatioMulInvis=0.3
- **Mentions:** autoexec.cfg
- **Risk:** none

## 1342 Adjusted Ultra Graphics Config (P4, Graphics config (cfg))

- **What the author says (Nexus summary):** A config for better performance using Ultra graphic settings. Improves texture streaming, LODs, lighting, and tweaked shadows for increased FPS.
- **File:** `Custom Config-1342-1-0-1666308248.zip` (archive, 0.0 MB, `c_graphics-config-cfg`), full (scratch, deleted after reading)
- **Grade:** D small tweak | **gameplay perceptibility:** medium | **visual/audio impact:** high | **layers:** D2 engine config | **domain:** engine config, graphics config
- **How it installs:** unclear: read the archive's own instructions; manifest id `-`, supports `-`, loads on 1.9.8: no manifest (legacy install)
- **Where it changes things:** config (.cfg): 1; docs: 1; lua identical to vanilla: 0
- **Config:** 43 keys, e.g. con_restricted=0, e_LodFaceAreaTargetSize=0.0008, e_MergedMeshesActiveDist=300, e_MergedMeshesLodRatio=16, e_MergedMeshesViewDistRatio=125, e_ShadowsCastViewDistRatio=0.8, e_ShadowsCastViewDistRatioLights=0.3, e_ShadowsCastViewDistRatioMulInvis=0.3
- **Mentions:** autoexec.cfg
- **Risk:** none

## 1355 Better Crime Stealth Plus No Dogs (P3, Crime / stealth / loot)

- **What the author says (Nexus summary):** Makes Crime and Stealth a bit more enjoyable and less annoying by toning down the AI detection and Crime reporting in the game.
- **File:** `Better Stealth Plus Crime-1355-1-0-1648906747.zip` (archive, 0.0 MB, `c_crime-stealth-loot`), full (scratch, deleted after reading)
- **Grade:** D small tweak | **gameplay perceptibility:** high | **visual/audio impact:** none | **layers:** D3 Lua scripts | **domain:** scripts
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `(none)`, loads on 1.9.8: yes (no version restriction)
- **Where it changes things:** manifest: 1; pak (container): 1; scripts (Lua): 1; lua identical to vanilla: 0
- **Lua:** 1 files, 491 lines; API used: player.soulx3, player.actorx2, XGenAIModule.SendMessageToEntityDatax2, entity.soulx2, player.thisx2, player.humanx1
- **Risk:** none

## 1410 Better Rain (P3, World / weather / visuals)

- **What the author says (Nexus summary):** Improves the appearance of rain to be more realistic and in particular makes it less visible, less bright at night
- **File:** `Better Rain mod 2.1-1410-2-1-1676326729.zip` (archive, 102.33 MB, `c_world-weather-visuals`), full (scratch, deleted after reading)
- **Grade:** D small tweak | **gameplay perceptibility:** medium | **visual/audio impact:** medium | **layers:** D0 content/text; D1 game data xml (not table rows) | **domain:** other game data (xml), textures/models/animations
- **How it installs:** legacy: files go into the game's Data folder; manifest id `-`, supports `-`, loads on 1.9.8: no manifest (legacy install)
- **Where it changes things:** other: 967; pak (container): 5; textures: 3; config (.cfg): 1; other game data (xml, not table rows): 1; lua identical to vanilla: 0
- **Risk:** none

## 1552 See NPCs and Animals Farther (Increased NPC render distance) (P4, Graphics config (cfg))

- **What the author says (Nexus summary):** This mod allows you to see NPCs and animals live out their lives from very far away (by increasing their render distance only). No more enemy ambushes or NPCs on the road "popping-in" and killing immersion. See entire villages/towns/castles
- **File:** `NPC_RenderDist_Extreme-1552-1-0-1696674070.zip` (archive, 0.0 MB, `c_graphics-config-cfg`), full (scratch, deleted after reading)
- **Grade:** D small tweak | **gameplay perceptibility:** medium | **visual/audio impact:** high | **layers:** D2 engine config | **domain:** engine config, graphics config
- **How it installs:** loose .pak (legacy: copy into Data); manifest id `-`, supports `-`, loads on 1.9.8: no manifest (legacy install)
- **Where it changes things:** config (.cfg): 2; docs: 1; pak (container): 1; lua identical to vanilla: 0
- **Config:** 85 keys, e.g. WH_AI_LOD_DistanceMax=660, WH_AI_LOD_DistanceMin=600, ca_AttachmentCullingRation=145, ca_AttachmentCullingRation=300, ca_AttachmentCullingRation=360, ca_AttachmentCullingRation=370, ca_AttachmentCullingRation=450, e_CoverageBufferReproj=6
- **Risk:** none

## 1552 See NPCs and Animals Farther (Increased NPC render distance) (P4, Graphics config (cfg))

- **What the author says (Nexus summary):** This mod allows you to see NPCs and animals live out their lives from very far away (by increasing their render distance only). No more enemy ambushes or NPCs on the road "popping-in" and killing immersion. See entire villages/towns/castles
- **File:** `NPC_RenderDist_High-1552-1-0-1696674005.zip` (archive, 0.0 MB, `c_graphics-config-cfg`), full (scratch, deleted after reading)
- **Grade:** D small tweak | **gameplay perceptibility:** medium | **visual/audio impact:** high | **layers:** D2 engine config | **domain:** engine config, graphics config
- **How it installs:** loose .pak (legacy: copy into Data); manifest id `-`, supports `-`, loads on 1.9.8: no manifest (legacy install)
- **Where it changes things:** config (.cfg): 2; docs: 1; pak (container): 1; lua identical to vanilla: 0
- **Config:** 85 keys, e.g. WH_AI_LOD_DistanceMax=500, WH_AI_LOD_DistanceMin=440, ca_AttachmentCullingRation=145, ca_AttachmentCullingRation=300, ca_AttachmentCullingRation=360, ca_AttachmentCullingRation=370, ca_AttachmentCullingRation=450, e_CoverageBufferReproj=6
- **Risk:** none

## 1552 See NPCs and Animals Farther (Increased NPC render distance) (P4, Graphics config (cfg))

- **What the author says (Nexus summary):** This mod allows you to see NPCs and animals live out their lives from very far away (by increasing their render distance only). No more enemy ambushes or NPCs on the road "popping-in" and killing immersion. See entire villages/towns/castles
- **File:** `NPC_RenderDist_Medium-1552-1-0-1696673983.zip` (archive, 0.0 MB, `c_graphics-config-cfg`), full (scratch, deleted after reading)
- **Grade:** D small tweak | **gameplay perceptibility:** medium | **visual/audio impact:** high | **layers:** D2 engine config | **domain:** engine config, graphics config
- **How it installs:** loose .pak (legacy: copy into Data); manifest id `-`, supports `-`, loads on 1.9.8: no manifest (legacy install)
- **Where it changes things:** config (.cfg): 2; docs: 1; pak (container): 1; lua identical to vanilla: 0
- **Config:** 85 keys, e.g. WH_AI_LOD_DistanceMax=360, WH_AI_LOD_DistanceMin=300, ca_AttachmentCullingRation=145, ca_AttachmentCullingRation=300, ca_AttachmentCullingRation=360, ca_AttachmentCullingRation=370, ca_AttachmentCullingRation=450, e_CoverageBufferReproj=6
- **Risk:** none

## 1561 Karnages_KCD_user.cfg 2.0 (P4, Graphics config (cfg))

- **What the author says (Nexus summary):** My user.cfg File
- **File:** `Karnages_KCD_user.cfg 2.0-1561-1-0-0-1700592743.7z` (archive, 0.0 MB, `c_graphics-config-cfg`), full (scratch, deleted after reading)
- **Grade:** D small tweak | **gameplay perceptibility:** medium | **visual/audio impact:** high | **layers:** D2 engine config | **domain:** engine config, graphics config
- **How it installs:** unclear: read the archive's own instructions; manifest id `-`, supports `-`, loads on 1.9.8: no manifest (legacy install)
- **Where it changes things:** docs: 1; config (.cfg): 1; lua identical to vanilla: 0
- **Config:** 47 keys, e.g. e_PreloadMaterials=1, e_VolumetricFog=1, e_svoTI_ConeMaxLength=8, e_svoTI_DiffuseAmplifier=1.12, e_svoTI_DiffuseConeWidth=24, e_svoTI_LowSpecMode=3, e_svoTI_MinReflectance=0.19, e_svoTI_ResScaleBase=0
- **Mentions:** user.cfg
- **Risk:** none

## 1625 MadHUDAutoHideHUDRebornEdition (unlisted, (not in the 365 index))

- **What the author says (Nexus summary):** -
- **File:** `MadHUD-AutoHideHUDRebornEdition-MsRhtBttnComptblVr-1625-r1-1-0-1745126962.zip` (archive, 0.02 MB, `_unmatched`), full (scratch, deleted after reading)
- **Grade:** D small tweak | **gameplay perceptibility:** medium | **visual/audio impact:** low | **layers:** D0 content/text; D1 game data xml (not table rows) | **domain:** other game data (xml), text
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `1.9.*`, loads on 1.9.8: yes (wildcard)
- **Where it changes things:** localization: 9; other game data (xml, not table rows): 2; manifest: 1; pak (container): 1; lua identical to vanilla: 0
- **Text:** 0 strings changed, 144 new
- **Risk:** none

## 1646 AutoLimitFPS (P4, Graphics config (cfg))

- **What the author says (Nexus summary):** Automatically uncap framerate during fasttravel, sleep and wait, and recap it when done.
- **File:** `AutoLimitFps144-1646-0-1-0-1716157681.zip` (archive, 0.01 MB, `c_graphics-config-cfg`), full (scratch, deleted after reading)
- **Grade:** D small tweak | **gameplay perceptibility:** high | **visual/audio impact:** none | **layers:** D3 Lua scripts | **domain:** scripts
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `1.9.4 1.9.5 1.9.6`, loads on 1.9.8: NO (disabled: lists 1.9.4, 1.9.5, 1.9.6)
- **Where it changes things:** scripts (Lua): 6; other: 2; manifest: 1; pak (container): 1; lua identical to vanilla: 0
- **Lua:** 6 files, 242 lines; API used: System.ExecuteCommandx10, System.GetCurrTimex4, System.SpawnEntityx2
- **Risk:** none

## 1667 Surface Type Rework (P3, World / weather / visuals)

- **What the author says (Nexus summary):** Reworks the physical attributes (mainly the pierceability) of surfaces and materials.
- **File:** `Surface Type Rework-1667-1-0-0-1718540697.7z` (archive, 0.0 MB, `c_world-weather-visuals`), full (scratch, deleted after reading)
- **Grade:** D small tweak | **gameplay perceptibility:** medium | **visual/audio impact:** none | **layers:** D1 game data xml (not table rows) | **domain:** other game data (xml)
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `(none)`, loads on 1.9.8: yes (no version restriction)
- **Where it changes things:** manifest: 1; pak (container): 1; other game data (xml, not table rows): 1; lua identical to vanilla: 0
- **Risk:** none

## 1691 zzz_Clean_Items_In_Trough.pak (unlisted, (not in the 365 index))

- **What the author says (Nexus summary):** -
- **File:** `zzz_Clean_Items_In_Trough.pak` (loose file, 0.0 MB, `_unmatched`), read in place
- **Grade:** D small tweak | **gameplay perceptibility:** medium | **visual/audio impact:** none | **layers:** D1 game data xml (not table rows) | **domain:** other game data (xml)
- **How it installs:** loose .pak (legacy: copy into Data); manifest id `-`, supports `-`, loads on 1.9.8: no manifest (legacy install)
- **Where it changes things:** pak (container): 1; other game data (xml, not table rows): 1; lua identical to vanilla: 0
- **Risk:** none

## 1720 Performance Configuration (Mid-High End) (P4, Graphics config (cfg))

- **What the author says (Nexus summary):** I have had some luck improving my overall FPS outside of towns with this autoexec.cfg file. I wanted to upload mine in case it is useful to anyone else. Settings are based on my current hardware (Ryzen 7 3700x, RTX 4070, 16GB RAM, 1GB NVMe
- **File:** `autoexec.cfg-1720-1-1726007579.7z` (archive, 0.0 MB, `c_graphics-config-cfg`), full (scratch, deleted after reading)
- **Grade:** D small tweak | **gameplay perceptibility:** medium | **visual/audio impact:** high | **layers:** D2 engine config | **domain:** engine config, graphics config
- **How it installs:** unclear: read the archive's own instructions; manifest id `-`, supports `-`, loads on 1.9.8: no manifest (legacy install)
- **Where it changes things:** config (.cfg): 1; lua identical to vanilla: 0
- **Config:** 64 keys, e.g. cl_fov=90, con_restricted=0, e_AutoPrecacheCameraJumpDist=1, e_AutoPrecacheCgf=2, e_AutoPrecacheTerrainAndProcVeget=1, e_AutoPrecacheTexturesAndShaders=1, e_LodFaceAreaTargetSize=0.0008, e_LodRatio=200
- **Risk:** none

## 1732 Torch Radius (P3, World / weather / visuals)

- **What the author says (Nexus summary):** Increases the range of the torch.
- **File:** `Torch Light Radius-1732-1-0-1728140274.zip` (archive, 0.0 MB, `c_world-weather-visuals`), full (scratch, deleted after reading)
- **Grade:** D small tweak | **gameplay perceptibility:** medium | **visual/audio impact:** none | **layers:** D1 game data xml (not table rows) | **domain:** other game data (xml)
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `(none)`, loads on 1.9.8: yes (no version restriction)
- **Where it changes things:** manifest: 1; pak (container): 1; other game data (xml, not table rows): 1; lua identical to vanilla: 0
- **Risk:** none

## 1779 Semi Sorted soul XML (P3, Tools / reference)

- **What the author says (Nexus summary):** This file is a semi sorted XML for the original soul.xml file naming all souls present in the game
- **File:** `souls_sorted_v1.2-1779-1-2-1736773918.zip` (archive, 0.62 MB, `c_tools-reference`), full (scratch, deleted after reading)
- **Grade:** D small tweak | **gameplay perceptibility:** medium | **visual/audio impact:** none | **layers:** D1 game data xml (not table rows) | **domain:** other game data (xml)
- **How it installs:** unclear: read the archive's own instructions; manifest id `-`, supports `-`, loads on 1.9.8: no manifest (legacy install)
- **Where it changes things:** other game data (xml, not table rows): 1; lua identical to vanilla: 0
- **Risk:** none

## 1823 RTX 3050 PACK (P4, Graphics config (cfg))

- **What the author says (Nexus summary):** This pack enhances performance, ensuring stable 60+ FPS on RTX 3050 (Mobile), RTX 3050TI, RTX 3050 (Desktop).
- **File:** `3050 8GB VRAM - 16GB RAM-1823-1-1-1739410244.zip` (archive, 0.0 MB, `c_graphics-config-cfg`), full (scratch, deleted after reading)
- **Grade:** D small tweak | **gameplay perceptibility:** medium | **visual/audio impact:** high | **layers:** D1 game data xml (not table rows); D2 engine config | **domain:** other game data (xml), engine config, graphics config
- **How it installs:** unclear: read the archive's own instructions; manifest id `-`, supports `-`, loads on 1.9.8: no manifest (legacy install)
- **Where it changes things:** other game data (xml, not table rows): 1; config (.cfg): 1; docs: 1; lua identical to vanilla: 0
- **Config:** 59 keys, e.g. ai_NavigationSystemMT=1, anti_aliasing="SMAA, e_MaxViewDistSpecLerp=0.4, e_ShadowsCastViewDistRatioLights=-0.1, e_ShadowsMaxTexRes=1024, e_ShadowsPoolSize=1024, e_VegetationUseTerrainColor=1, e_VolumetricFog=1
- **Mentions:** autoexec.cfg
- **Risk:** none

## 1823 RTX 3050 PACK (P4, Graphics config (cfg))

- **What the author says (Nexus summary):** This pack enhances performance, ensuring stable 60+ FPS on RTX 3050 (Mobile), RTX 3050TI, RTX 3050 (Desktop).
- **File:** `3050 8GB VRAM - 32GB RAM-1823-1-1-1739410283.zip` (archive, 0.0 MB, `c_graphics-config-cfg`), full (scratch, deleted after reading)
- **Grade:** D small tweak | **gameplay perceptibility:** medium | **visual/audio impact:** high | **layers:** D1 game data xml (not table rows); D2 engine config | **domain:** other game data (xml), engine config, graphics config
- **How it installs:** unclear: read the archive's own instructions; manifest id `-`, supports `-`, loads on 1.9.8: no manifest (legacy install)
- **Where it changes things:** other game data (xml, not table rows): 1; config (.cfg): 1; docs: 1; lua identical to vanilla: 0
- **Config:** 59 keys, e.g. ai_NavigationSystemMT=1, anti_aliasing="SMAA, e_MaxViewDistSpecLerp=0.4, e_ShadowsCastViewDistRatioLights=-0.1, e_ShadowsMaxTexRes=1024, e_ShadowsPoolSize=1024, e_VegetationUseTerrainColor=1, e_VolumetricFog=1
- **Mentions:** autoexec.cfg
- **Risk:** none

## 1958 Selected Immersion Breaking Music Mute (P3, Animations / audio)

- **What the author says (Nexus summary):** This seems to be always problem to my ears and immersion. Reminds me of Oblivion and it's combat music, you heard combat music before you saw the enemy.
- **File:** `SIBMM All-1958-1-2-1743947561.zip` (archive, 0.0 MB, `c_animations-audio`), full (scratch, deleted after reading)
- **Grade:** D small tweak | **gameplay perceptibility:** medium | **visual/audio impact:** none | **layers:** D1 game data xml (not table rows) | **domain:** other game data (xml)
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `1.9.6`, loads on 1.9.8: NO (disabled: lists 1.9.6)
- **Where it changes things:** manifest: 1; pak (container): 1; other game data (xml, not table rows): 1; lua identical to vanilla: 0
- **Risk:** none

## 1972 FINAL Beyond SUPER Ultra Graphics and Visuals Configs (P4, Graphics config (cfg))

- **What the author says (Nexus summary):** My very first mod! i just love gaming and modding my games so much and as i went on, something in me always wanted to learn more or mod myself. so today i present you my very first own small mod.
- **File:** `FINAL Beyond SUPER Ultra Graphics and Visuals Conf-1972-1--1743452912.zip` (archive, 0.01 MB, `c_graphics-config-cfg`), full (scratch, deleted after reading)
- **Grade:** D small tweak | **gameplay perceptibility:** medium | **visual/audio impact:** high | **layers:** D2 engine config | **domain:** engine config, graphics config
- **How it installs:** unclear: read the archive's own instructions; manifest id `-`, supports `-`, loads on 1.9.8: no manifest (legacy install)
- **Where it changes things:** config (.cfg): 2; lua identical to vanilla: 0
- **Config:** 222 keys, e.g. ai_NavigationSystemMT=1, ca_FacialAnimationFramerate=120, ca_MemoryDefragEnabled=0, ca_ParametricPoolSize=1024, ca_UseIMG_CAF=1, ca_attachmentcullingration=4000, cl_fov=80, con_restricted=0
- **Risk:** none

## 1982 Stormy Skies (P3, World / weather / visuals)

- **What the author says (Nexus summary):** Stormy Skies is a simple weather mod that fixes the cloudless rainstorms in KCD. No more immersion-shattering "sun showers." It is lightweight, doesn't affect performance at all, and is a 100% game changer (literally) when it comes to
- **File:** `Stormy_Skies_v1.0.zip-1982-1-0-1744237965 (1).zip` (archive, 1.54 MB, `c_world-weather-visuals`), full (scratch, deleted after reading)
- **Grade:** D small tweak | **gameplay perceptibility:** medium | **visual/audio impact:** medium | **layers:** D0 content/text; D1 game data xml (not table rows) | **domain:** other game data (xml), textures/models/animations
- **How it installs:** unclear: read the archive's own instructions; manifest id `-`, supports `-`, loads on 1.9.8: no manifest (legacy install)
- **Where it changes things:** textures: 4; other game data (xml, not table rows): 2; docs: 1; lua identical to vanilla: 0
- **Mentions:** unpack
- **Risk:** none

## 2084 Mount  Horse - Torch Toggle Keys (P3, Horses)

- **What the author says (Nexus summary):** Key binding for torch and mounting This mod combines two features into one: with a single key you can equip your torch, and with another key you can easily mount or dismount your horse.
- **File:** `Mount Horse - Torch Toggle Keys-2084-1-0-1758809416.rar` (archive, 0.0 MB, `c_horses`), full (scratch, deleted after reading)
- **Grade:** D small tweak | **gameplay perceptibility:** medium | **visual/audio impact:** low | **layers:** D0 content/text; D1 game data xml (not table rows) | **domain:** other game data (xml), text
- **How it installs:** legacy: files go into the game's Data folder; manifest id `-`, supports `-`, loads on 1.9.8: no manifest (legacy install)
- **Where it changes things:** localization: 7; pak (container): 1; other game data (xml, not table rows): 1; lua identical to vanilla: 0
- **Text:** 0 strings changed, 3 new
- **Risk:** none

## 2106 High FPS FX (KCD1) (P4, Graphics config (cfg))

- **What the author says (Nexus summary):** Particle Framerates Increased
- **File:** `High FPS FX 2106 2.1 2026-07-11T22-23Z LQeSByZhK.zip` (archive, 0.07 MB, `c_graphics-config-cfg`), full (scratch, deleted after reading)
- **Grade:** D small tweak | **gameplay perceptibility:** medium | **visual/audio impact:** none | **layers:** D1 game data xml (not table rows) | **domain:** other game data (xml)
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `1.9.4 1.9.5 1.9.6 1.9.7 1.9.8`, loads on 1.9.8: yes (explicit)
- **Where it changes things:** other game data (xml, not table rows): 8; manifest: 1; pak (container): 1; lua identical to vanilla: 0
- **Risk:** none

## 2106 High FPS FX (KCD1) (P4, Graphics config (cfg))

- **What the author says (Nexus summary):** Particle Framerates Increased
- **File:** `High FPS FX-2106-1-3-1777265116.zip` (archive, 0.07 MB, `c_graphics-config-cfg`), full (scratch, deleted after reading)
- **Grade:** D small tweak | **gameplay perceptibility:** medium | **visual/audio impact:** none | **layers:** D1 game data xml (not table rows) | **domain:** other game data (xml)
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `1.9.4 1.9.5 1.9.6 1.9.7 1.9.8`, loads on 1.9.8: yes (explicit)
- **Where it changes things:** other game data (xml, not table rows): 8; manifest: 1; pak (container): 1; lua identical to vanilla: 0
- **Risk:** none

## 2153 Engine Tweaks KCD 2.0 - user.cfg details (P4, Graphics config (cfg))

- **What the author says (Nexus summary):** Engine Tweaks KCD 2.0 - user.cfg details
- **File:** `user.cfg-2153-1-0-1770914009.zip` (archive, 0.0 MB, `c_graphics-config-cfg`), full (scratch, deleted after reading)
- **Grade:** D small tweak | **gameplay perceptibility:** medium | **visual/audio impact:** high | **layers:** D2 engine config | **domain:** engine config, graphics config
- **How it installs:** unclear: read the archive's own instructions; manifest id `-`, supports `-`, loads on 1.9.8: no manifest (legacy install)
- **Where it changes things:** config (.cfg): 1; lua identical to vanilla: 0
- **Config:** 43 keys, e.g. ca_AttachmentCullingRation=400, con_restricted=0, e_LodFaceAreaTargetSize=0.0008, e_MergedMeshesActiveDist=300, e_MergedMeshesLodRatio=16, e_MergedMeshesViewDistRatio=125, e_ShadowsCastViewDistRatio=0.8, e_ShadowsCastViewDistRatioLights=0.3
- **Risk:** none

## 2175 Enhanced Color Grading (P4, Reshade / ENB / visual preset)

- **What the author says (Nexus summary):** This mod makes some adjusts in the lights, shadows and color grading, to bring visuals similar to those of Kingdom Come: Deliverance 2.
- **File:** `Enhanced Color Grading-2175-1-3-1775786024.zip` (archive, 0.02 MB, `c_reshade-enb-visual-preset`), full (scratch, deleted after reading)
- **Grade:** D small tweak | **gameplay perceptibility:** medium | **visual/audio impact:** medium | **layers:** D0 content/text; D3 Lua scripts | **domain:** scripts, textures/models/animations, UI
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `1.*`, loads on 1.9.8: yes (wildcard)
- **Where it changes things:** manifest: 1; pak (container): 1; textures: 1; ui: 1; scripts (Lua): 1; lua identical to vanilla: 0
- **Lua:** 1 files, 77 lines; API used: System.SetCVarx42, System.LogAlwaysx1
- **Risk:** none

## 2190 ENHANCED Bohemian Redux  and FX Overhaul (P3, World / weather / visuals)

- **What the author says (Nexus summary):** ENHANCED Bohemian Redux is a compact graphics mod that makes the game’s visuals richer and more expressive,  with enhanced FX particles and new smoke effects, while keeping the style clean and performance-friendly.
- **File:** `ENHANCED Bohemian Redux FX Overhaul-2190-2-0-1774439071 (1).rar` (archive, 18.68 MB, `c_world-weather-visuals`), full (scratch, deleted after reading)
- **Grade:** D small tweak | **gameplay perceptibility:** medium | **visual/audio impact:** high | **layers:** D0 content/text; D1 game data xml (not table rows); D2 engine config; D3 Lua scripts | **domain:** scripts, other game data (xml), graphics config, textures/models/animations
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `lut`, supports `(none)`, loads on 1.9.8: yes (no version restriction)
- **Where it changes things:** textures: 25; models/animations/materials: 5; other game data (xml, not table rows): 4; config (.cfg): 1; manifest: 1; pak (container): 1; scripts (Lua): 1; lua identical to vanilla: 0
- **Lua:** 1 files, 32 lines; API used: System.LogAlwaysx2, System.GetCVarx1, System.ExecuteCommandx1
- **Config:** 18 keys, e.g. e_Clouds=1, e_ShadowsClouds=1, e_svoTI_DiffuseAmplifier=1.12, e_svoTI_MinReflectance=0.19, e_svoTI_SSAOAmount=1.545, e_svoTI_SpecularAmplifier=0.82, e_svoTI_TemporalFilteringBase=1, r_CloudsUpdateAlways=1
- **Risk:** none

## 2191 Realistic Footprints v2.0 KCD I (P3, World / weather / visuals)

- **What the author says (Nexus summary):** Realistic Footprints v2.0 represents a major leap in environmental immersion. This version expands ground interaction, deepensatmosphere, elevates realism without compromising stability.
- **File:** `Realistic Footprints v2.0 KCD1-2191-3-0-1780731196.rar` (archive, 0.91 MB, `c_world-weather-visuals`), full (scratch, deleted after reading)
- **Grade:** D small tweak | **gameplay perceptibility:** medium | **visual/audio impact:** high | **layers:** D0 content/text; D1 game data xml (not table rows) | **domain:** other game data (xml), textures/models/animations
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `realisticfootprints`, supports `(none)`, loads on 1.9.8: yes (no version restriction)
- **Where it changes things:** textures: 12; models/animations/materials: 7; other game data (xml, not table rows): 5; manifest: 1; pak (container): 1; lua identical to vanilla: 0
- **Risk:** none

## 2206 Rivers of Blood KCD I HD v2.0 (P3, World / weather / visuals)

- **What the author says (Nexus summary):** Realistic, dynamic, and brutal - the port of the best definitive blood mod for KCD II.
- **File:** `Rivers of Blood KCD I HD v2.0-2206-1-0-1775912726.rar` (archive, 6.15 MB, `c_world-weather-visuals`), full (scratch, deleted after reading)
- **Grade:** D small tweak | **gameplay perceptibility:** medium | **visual/audio impact:** high | **layers:** D0 content/text; D1 game data xml (not table rows) | **domain:** other game data (xml), textures/models/animations
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `rivers_of_blood_kcdi_hd`, supports `(none)`, loads on 1.9.8: yes (no version restriction)
- **Where it changes things:** textures: 8; models/animations/materials: 4; other game data (xml, not table rows): 3; manifest: 1; pak (container): 1; lua identical to vanilla: 0
- **Risk:** none

## 2223 Stop Looking Up On Horseback (P3, Horses)

- **What the author says (Nexus summary):** Stop looking up (seeing so much sky) while riding a horse.
- **File:** `StopLookingUpOnHorseback-2223-2-1778010739.7z` (archive, 0.0 MB, `c_horses`), full (scratch, deleted after reading)
- **Grade:** D small tweak | **gameplay perceptibility:** none | **visual/audio impact:** none | **layers:** D2 engine config | **domain:** engine config
- **How it installs:** unclear: read the archive's own instructions; manifest id `-`, supports `-`, loads on 1.9.8: no manifest (legacy install)
- **Where it changes things:** config (.cfg): 1; lua identical to vanilla: 0
- **Config:** 1 keys, e.g. wh_horse_CameraCenteringPitchOffset=-16
- **Risk:** none

## 2224 More Realistic Horse Handling (P3, Horses)

- **What the author says (Nexus summary):** My personal preference of horse handling in KCD.
- **File:** `HorseHandlingKCD-2224-1-1778012631.7z` (archive, 0.0 MB, `c_horses`), full (scratch, deleted after reading)
- **Grade:** D small tweak | **gameplay perceptibility:** none | **visual/audio impact:** none | **layers:** D2 engine config | **domain:** engine config
- **How it installs:** unclear: read the archive's own instructions; manifest id `-`, supports `-`, loads on 1.9.8: no manifest (legacy install)
- **Where it changes things:** config (.cfg): 1; lua identical to vanilla: 0
- **Config:** 2 keys, e.g. wh_horse_RotationSmoothInSpeed=0.20, wh_horse_RotationSmoothOutSpeed=0.10
- **Risk:** none

## 2243 Performance Tweaks and best visuals (P4, Graphics config (cfg))

- **What the author says (Nexus summary):** A cfg that combines most of the cfg tweaks made by other respective modders, plus some CryEngine tweaks
- **File:** `Autoexec-2243-1-1779736741.rar` (archive, 0.0 MB, `c_graphics-config-cfg`), full (scratch, deleted after reading)
- **Grade:** D small tweak | **gameplay perceptibility:** medium | **visual/audio impact:** high | **layers:** D2 engine config | **domain:** engine config, graphics config
- **How it installs:** unclear: read the archive's own instructions; manifest id `-`, supports `-`, loads on 1.9.8: no manifest (legacy install)
- **Where it changes things:** config (.cfg): 1; lua identical to vanilla: 0
- **Config:** 106 keys, e.g. ai_NavigationSystemMT=1, ca_thread0Affinity=9, ca_thread1Affinity=10, cl_fov=90, con_restricted=0, e_AutoPrecacheCameraJumpDist=1, e_AutoPrecacheCgf=2, e_AutoPrecacheTerrainAndProcVeget=1
- **Risk:** none

## 2243 Performance Tweaks and best visuals (P4, Graphics config (cfg))

- **What the author says (Nexus summary):** A cfg that combines most of the cfg tweaks made by other respective modders, plus some CryEngine tweaks
- **File:** `AutoexecCPUTWEAKS 2243 1 2026-06-28T16-43Z zEf3mMkId.rar` (archive, 0.0 MB, `c_graphics-config-cfg`), full (scratch, deleted after reading)
- **Grade:** D small tweak | **gameplay perceptibility:** medium | **visual/audio impact:** high | **layers:** D2 engine config | **domain:** engine config, graphics config
- **How it installs:** unclear: read the archive's own instructions; manifest id `-`, supports `-`, loads on 1.9.8: no manifest (legacy install)
- **Where it changes things:** config (.cfg): 1; lua identical to vanilla: 0
- **Config:** 29 keys, e.g. ai_NavigationSystemMT=1, ca_thread0Affinity=9, ca_thread1Affinity=10, cl_fov=90, con_restricted=0, e_ParticlesThread=11, e_StatObjMergeUseThread=1, pl_movement.power_sprint_targetFov=85
- **Risk:** none

## 2313 Reshield From Torch (P3, Weapons / armor / items)

- **What the author says (Nexus summary):** Equipping a torch removes your shield. This mod puts it back.
- **File:** `Reshield 2313 3 2026-08-01T01-48Z OrmK3LN3q.zip` (archive, 0.01 MB, `c_weapons-armor-items`), full (scratch, deleted after reading)
- **Grade:** D small tweak | **gameplay perceptibility:** high | **visual/audio impact:** none | **layers:** D3 Lua scripts | **domain:** scripts
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `reshield`, supports `(none)`, loads on 1.9.8: yes (no version restriction)
- **Where it changes things:** manifest: 1; pak (container): 1; scripts (Lua): 1; lua identical to vanilla: 0
- **Lua:** 1 files, 544 lines; API used: System.AddCCommandx8, player.inventoryx5, player.humanx5, player.actorx3, XGenAIModule.GetEntityByWUIDx2, System.LogAlwaysx2
- **Risk:** none

## 2333 Homecoming - Runt Fight Redux (P3, Quests / lore / content)

- **What the author says (Nexus summary):** A more believable and immersive rebuild of the first fight with Runt during Homecoming.
- **File:** `Homecoming Runt Fight Redux 2333 1.0.0 2026-08-12T10-25Z JCx5Wpz09.zip` (archive, 0.03 MB, `c_quests-lore-content`), full (scratch, deleted after reading)
- **Grade:** D small tweak | **gameplay perceptibility:** medium | **visual/audio impact:** none | **layers:** D1 game data xml (not table rows) | **domain:** other game data (xml)
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `(none)`, loads on 1.9.8: yes (no version restriction)
- **Where it changes things:** manifest: 1; docs: 1; pak (container): 1; other game data (xml, not table rows): 1; lua identical to vanilla: 0
- **Mentions:** states requirements
- **Risk:** none

## 2353 Ultimate Graphics Adjustment (P4, Graphics config (cfg))

- **What the author says (Nexus summary):** Use User.cfg to improve game graphics and optimize performance.
- **File:** `KCD Ultimate Adjustment 2353 1 2026-09-09T14-55Z q1JwghIVc.rar` (archive, 0.0 MB, `c_graphics-config-cfg`), full (scratch, deleted after reading)
- **Grade:** D small tweak | **gameplay perceptibility:** medium | **visual/audio impact:** high | **layers:** D2 engine config | **domain:** engine config, graphics config
- **How it installs:** unclear: read the archive's own instructions; manifest id `-`, supports `-`, loads on 1.9.8: no manifest (legacy install)
- **Where it changes things:** config (.cfg): 1; lua identical to vanilla: 0
- **Config:** 113 keys, e.g. ai_NavigationSystemMT=1, ca_thread0Affinity=9, ca_thread1Affinity=10, e_AutoPrecacheCameraJumpDist=1, e_AutoPrecacheCgf=2, e_AutoPrecacheTerrainAndProcVeget=1, e_AutoPrecacheTexturesAndShaders=1, e_Clouds=1
- **Risk:** none

## 28 No Helmet Vision (unlisted, (not in the 365 index))

- **What the author says (Nexus summary):** -
- **File:** `No Helmet Vision-28-1-9-1559069013.zip` (archive, 0.0 MB, `_unmatched`), full (scratch, deleted after reading)
- **Grade:** E visual, audio or UI only (no gameplay change) | **gameplay perceptibility:** low | **visual/audio impact:** medium | **layers:** D0 content/text | **domain:** textures/models/animations, UI
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `(none)`, loads on 1.9.8: yes (no version restriction)
- **Where it changes things:** textures: 9; manifest: 1; pak (container): 1; ui: 1; lua identical to vanilla: 0
- **Risk:** none

## 387 Ambient_Occlusion_Fix_user_v1.07-387-1-07.7z (unlisted, (not in the 365 index))

- **What the author says (Nexus summary):** -
- **File:** `Ambient_Occlusion_Fix_user_v1.07-387-1-07.7z` (archive, 0.0 MB, `_unmatched`), full (scratch, deleted after reading)
- **Grade:** E visual, audio or UI only (no gameplay change) | **gameplay perceptibility:** medium | **visual/audio impact:** high | **layers:** D2 engine config | **domain:** graphics config
- **How it installs:** unclear: read the archive's own instructions; manifest id `-`, supports `-`, loads on 1.9.8: no manifest (legacy install)
- **Where it changes things:** config (.cfg): 1; lua identical to vanilla: 0
- **Config:** 13 keys, e.g. e_svoTI_DiffuseAmplifier=1.12, e_svoTI_MinReflectance=0.19, e_svoTI_SSAOAmount=1.545, e_svoTI_SpecularAmplifier=0.82, e_svoTI_TemporalFilteringBase=1, r_ssdo=1, r_ssdoAmountAmbient=1.4, r_ssdoAmountDirect=2
- **Risk:** none

## 392 Sky Fix 1.2-392-1-2.rar (unlisted, (not in the 365 index))

- **What the author says (Nexus summary):** -
- **File:** `Sky Fix 1.2-392-1-2.rar` (archive, 0.02 MB, `_unmatched`), full (scratch, deleted after reading)
- **Grade:** E visual, audio or UI only (no gameplay change) | **gameplay perceptibility:** low | **visual/audio impact:** low | **layers:** D0 content/text | **domain:** textures/models/animations
- **How it installs:** unclear: read the archive's own instructions; manifest id `-`, supports `-`, loads on 1.9.8: no manifest (legacy install)
- **Where it changes things:** textures: 1; lua identical to vanilla: 0
- **Risk:** none

## 392 Sky and Grass Fix 1.2-392-1-2.rar (unlisted, (not in the 365 index))

- **What the author says (Nexus summary):** -
- **File:** `Sky and Grass Fix 1.2-392-1-2.rar` (archive, 0.03 MB, `_unmatched`), full (scratch, deleted after reading)
- **Grade:** E visual, audio or UI only (no gameplay change) | **gameplay perceptibility:** low | **visual/audio impact:** low | **layers:** D0 content/text | **domain:** textures/models/animations
- **How it installs:** unclear: read the archive's own instructions; manifest id `-`, supports `-`, loads on 1.9.8: no manifest (legacy install)
- **Where it changes things:** textures: 1; lua identical to vanilla: 0
- **Risk:** none

## 611 Dice.pak (unlisted, (not in the 365 index))

- **What the author says (Nexus summary):** -
- **File:** `Dice.pak` (loose file, 1.9 MB, `_unmatched`), read in place
- **Grade:** E visual, audio or UI only (no gameplay change) | **gameplay perceptibility:** low | **visual/audio impact:** high | **layers:** D0 content/text | **domain:** textures/models/animations
- **How it installs:** loose .pak (legacy: copy into Data); manifest id `-`, supports `-`, loads on 1.9.8: no manifest (legacy install)
- **Where it changes things:** textures: 28; models/animations/materials: 7; pak (container): 1; lua identical to vanilla: 0
- **Risk:** none

## 660 Apex ENB-660-2-2-1590351047.7z (unlisted, (not in the 365 index))

- **What the author says (Nexus summary):** -
- **File:** `Apex ENB-660-2-2-1590351047.7z` (archive, 0.02 MB, ``), full (scratch, deleted after reading)
- **Grade:** E visual, audio or UI only (no gameplay change) | **gameplay perceptibility:** none | **visual/audio impact:** high | **layers:** D0 content/text | **domain:** post-processing (ReShade/ENB)
- **How it installs:** unclear: read the archive's own instructions; manifest id `-`, supports `-`, loads on 1.9.8: no manifest (legacy install)
- **Where it changes things:** reshade/ENB (shaders, presets): 19; lua identical to vanilla: 0
- **Risk:** none

## 660 Apex ENB-660-2-2-1590351047.7z (unlisted, (not in the 365 index))

- **What the author says (Nexus summary):** -
- **File:** `Apex ENB-660-2-2-1590351047.7z` (archive, 0.02 MB, `_unmatched`), full (scratch, deleted after reading)
- **Grade:** E visual, audio or UI only (no gameplay change) | **gameplay perceptibility:** none | **visual/audio impact:** high | **layers:** D0 content/text | **domain:** post-processing (ReShade/ENB)
- **How it installs:** unclear: read the archive's own instructions; manifest id `-`, supports `-`, loads on 1.9.8: no manifest (legacy install)
- **Where it changes things:** reshade/ENB (shaders, presets): 19; lua identical to vanilla: 0
- **Risk:** none

## 754 Painted Lords of Leipa Hounskull (P3, Weapons / armor / items)

- **What the author says (Nexus summary):** Armor texture mod; legacy install: the .pak goes into Data and Data\_fastload This mod turns this otherwise standard looking hounskull into a medieval state of the art!
- **File:** `Painted Leipa Hounskull-754-1-0-1559896602.zip` (archive, 6.47 MB, `c_weapons-armor-items`), full (scratch, deleted after reading)
- **Grade:** E visual, audio or UI only (no gameplay change) | **gameplay perceptibility:** low | **visual/audio impact:** low | **layers:** D0 content/text | **domain:** textures/models/animations
- **How it installs:** loose .pak (legacy: copy into Data); manifest id `-`, supports `-`, loads on 1.9.8: no manifest (legacy install)
- **Where it changes things:** textures: 2; pak (container): 1; lua identical to vanilla: 0
- **Risk:** none

## 844 Yet Another (Realistic) Reshade (P4, Reshade / ENB / visual preset)

- **What the author says (Nexus summary):** Yet Another Reshade, This is just my preset for Reshade, based on realism, with couple of mods and ingame tweaks for finetuning.No FPS loss!EDIT: I've forgotten to mention, in the readme included in this mod is some more ,(possibly),
- **File:** `Yet Another Reshade-844-1-0-1567756118.7z` (archive, 8.38 MB, `c_reshade-enb-visual-preset`), full (scratch, deleted after reading)
- **Grade:** E visual, audio or UI only (no gameplay change) | **gameplay perceptibility:** none | **visual/audio impact:** high | **layers:** D0 content/text | **domain:** post-processing (ReShade/ENB)
- **How it installs:** unclear: read the archive's own instructions; manifest id `-`, supports `-`, loads on 1.9.8: no manifest (legacy install)
- **Where it changes things:** reshade/ENB (shaders, presets): 48; other: 1; lua identical to vanilla: 0
- **Risk:** none

## 879 Original clouds KCD no mipmap (P3, World / weather / visuals)

- **What the author says (Nexus summary):** Improves the quality of clouds in the sky.A drop in performance is not noticed.Clouds with mipmap removed.
- **File:** `zima101-879-1-0-1575121825.zip` (archive, 33.24 MB, `c_world-weather-visuals`), full (scratch, deleted after reading)
- **Grade:** E visual, audio or UI only (no gameplay change) | **gameplay perceptibility:** low | **visual/audio impact:** high | **layers:** D0 content/text | **domain:** textures/models/animations
- **How it installs:** loose .pak (legacy: copy into Data); manifest id `-`, supports `-`, loads on 1.9.8: no manifest (legacy install)
- **Where it changes things:** textures: 39; other: 10; docs: 1; pak (container): 1; lua identical to vanilla: 0
- **Risk:** none

## 922 Enhanced Hair Textures (P3, World / weather / visuals)

- **What the author says (Nexus summary):** No more glowing hair and increase of clarity and contrast to all NPCs hair/beards, also fixes some weird hair colors for now.
- **File:** `Enhanced Hair Textures by Grimsy 1.1-922-1-1-1583842369.rar` (archive, 42.12 MB, `c_world-weather-visuals`), full (scratch, deleted after reading)
- **Grade:** E visual, audio or UI only (no gameplay change) | **gameplay perceptibility:** low | **visual/audio impact:** high | **layers:** D0 content/text | **domain:** textures/models/animations
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `(none)`, loads on 1.9.8: yes (no version restriction)
- **Where it changes things:** textures: 25; models/animations/materials: 5; docs: 1; manifest: 1; pak (container): 1; lua identical to vanilla: 0
- **Risk:** none

## 955 Treasure Maps Of Bohemia (P3, Quests / lore / content)

- **What the author says (Nexus summary):** Treasure Maps Of Bohemia is a hand-drawn retexture of all Treasure Maps and Ancient Maps found in Kingdom Come: Deliverance and all its DLC.
- **File:** `Treasure Maps Of Bohemia-955-1-9-5-1-1585332038.7z` (archive, 98.46 MB, `c_quests-lore-content`), full (scratch, deleted after reading)
- **Grade:** E visual, audio or UI only (no gameplay change) | **gameplay perceptibility:** low | **visual/audio impact:** high | **layers:** D0 content/text | **domain:** textures/models/animations
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `(none)`, loads on 1.9.8: yes (no version restriction)
- **Where it changes things:** textures: 66; manifest: 1; pak (container): 1; lua identical to vanilla: 0
- **Risk:** none

## 957 Dark Souls Death Screen (P3, Maps / UI / HUD)

- **What the author says (Nexus summary):** Changes KCD death screen (2 possible options) to enhance your experience while you DIE
- **File:** `DSDeathScreen (Option 1)-957-1-0-1584101845.rar` (archive, 0.26 MB, `c_maps-ui-hud`), full (scratch, deleted after reading)
- **Grade:** E visual, audio or UI only (no gameplay change) | **gameplay perceptibility:** none | **visual/audio impact:** medium | **layers:** D0 content/text | **domain:** UI
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `(none)`, loads on 1.9.8: yes (no version restriction)
- **Where it changes things:** docs: 1; manifest: 1; pak (container): 1; ui: 1; lua identical to vanilla: 0
- **Risk:** none

## 969 Enhanced Eyes (P3, World / weather / visuals)

- **What the author says (Nexus summary):** Makes eyes more vivid, sharper and natural, together with eyelashes fix to all characters including Henry.
- **File:** `Enhanced Eyes 1.1-969-1-1-1585051202.zip` (archive, 0.19 MB, `c_world-weather-visuals`), full (scratch, deleted after reading)
- **Grade:** E visual, audio or UI only (no gameplay change) | **gameplay perceptibility:** low | **visual/audio impact:** high | **layers:** D0 content/text | **domain:** textures/models/animations
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `(none)`, loads on 1.9.8: yes (no version restriction)
- **Where it changes things:** models/animations/materials: 28; textures: 2; manifest: 1; pak (container): 1; lua identical to vanilla: 0
- **Risk:** none

## 975 Super Natural Reshade (P4, Reshade / ENB / visual preset)

- **What the author says (Nexus summary):** A subtle, lightweight, non over-the-top natural color correction for KCD.
- **File:** `Super Natural Reshade v1.5-975-v1-5-1587646699.zip` (archive, 0.0 MB, `c_reshade-enb-visual-preset`), full (scratch, deleted after reading)
- **Grade:** E visual, audio or UI only (no gameplay change) | **gameplay perceptibility:** none | **visual/audio impact:** high | **layers:** D0 content/text | **domain:** post-processing (ReShade/ENB)
- **How it installs:** unclear: read the archive's own instructions; manifest id `-`, supports `-`, loads on 1.9.8: no manifest (legacy install)
- **Where it changes things:** reshade/ENB (shaders, presets): 1; lua identical to vanilla: 0
- **Risk:** none

## 978 minimalistic HUD (P3, Maps / UI / HUD)

- **What the author says (Nexus summary):** Are you annoyed by the huge Vanilla HUD? This mod gives you a "minimalistic HUD" that is not as intrusive as the Vanilla one with full control over the HUD elements via keybinds.
- **File:** `minimalisticHUD-978-1-0-1585828036.zip` (archive, 0.35 MB, `c_maps-ui-hud`), full (scratch, deleted after reading)
- **Grade:** E visual, audio or UI only (no gameplay change) | **gameplay perceptibility:** low | **visual/audio impact:** medium | **layers:** D0 content/text | **domain:** textures/models/animations
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `1.*`, loads on 1.9.8: yes (wildcard)
- **Where it changes things:** textures: 4; manifest: 1; pak (container): 1; lua identical to vanilla: 0
- **Risk:** none

## 994 Depth ReShade (P4, Reshade / ENB / visual preset)

- **What the author says (Nexus summary):** Get rid of the flat default look of KCD! Simple, minimal ReShade using two effects for brighter sunlight, deeper shadows, and widened contrast. Low/no performance hit
- **File:** `Depth Reshade by Ahaut-994-2-0-1586561627.zip` (archive, 0.0 MB, `c_reshade-enb-visual-preset`), full (scratch, deleted after reading)
- **Grade:** E visual, audio or UI only (no gameplay change) | **gameplay perceptibility:** none | **visual/audio impact:** high | **layers:** D0 content/text | **domain:** post-processing (ReShade/ENB)
- **How it installs:** unclear: read the archive's own instructions; manifest id `-`, supports `-`, loads on 1.9.8: no manifest (legacy install)
- **Where it changes things:** reshade/ENB (shaders, presets): 1; lua identical to vanilla: 0
- **Risk:** none

## 1059 Icon ID Resource (P3, Tools / reference)

- **What the author says (Nexus summary):** A mod resource containing a useful set of images showing all available buff, perk and object icons with corresponding IDs.
- **File:** `Icon ID Resource-1059-1-0-1592792055.rar` (archive, 14.14 MB, `c_tools-reference`), full (scratch, deleted after reading)
- **Grade:** E visual, audio or UI only (no gameplay change) | **gameplay perceptibility:** low | **visual/audio impact:** medium | **layers:** D0 content/text | **domain:** textures/models/animations
- **How it installs:** unclear: read the archive's own instructions; manifest id `-`, supports `-`, loads on 1.9.8: no manifest (legacy install)
- **Where it changes things:** textures: 3; lua identical to vanilla: 0
- **Risk:** none

## 1080 ReformationFX Reshade (P4, Reshade / ENB / visual preset)

- **What the author says (Nexus summary):** Brighter and realistic color correction for KCD
- **File:** `ReformationFX v1.1-1080-v1-1-1597071272.rar` (archive, 0.0 MB, `c_reshade-enb-visual-preset`), full (scratch, deleted after reading)
- **Grade:** E visual, audio or UI only (no gameplay change) | **gameplay perceptibility:** none | **visual/audio impact:** high | **layers:** D0 content/text | **domain:** post-processing (ReShade/ENB)
- **How it installs:** unclear: read the archive's own instructions; manifest id `-`, supports `-`, loads on 1.9.8: no manifest (legacy install)
- **Where it changes things:** reshade/ENB (shaders, presets): 1; lua identical to vanilla: 0
- **Risk:** none

## 1107 Blood and Steel with NO FPS LOSS (P3, World / weather / visuals)

- **What the author says (Nexus summary):** Gives a better and more realistic look, with nearly NO fps loss
- **File:** `Blood and Steel-1107-1-0-1600512585.zip` (archive, 0.06 MB, `c_world-weather-visuals`), full (scratch, deleted after reading)
- **Grade:** E visual, audio or UI only (no gameplay change) | **gameplay perceptibility:** none | **visual/audio impact:** high | **layers:** D0 content/text | **domain:** post-processing (ReShade/ENB)
- **How it installs:** unclear: read the archive's own instructions; manifest id `-`, supports `-`, loads on 1.9.8: no manifest (legacy install)
- **Where it changes things:** reshade/ENB (shaders, presets): 10; lua identical to vanilla: 0
- **Risk:** none

## 1114 Snow Mod (P3, World / weather / visuals)

- **What the author says (Nexus summary):** This mod replaces several texture files to make the world of Kingdom Come: Deliverance look snowy.
- **File:** `Snow-Mod-1114-0-5-1600873143.zip` (archive, 341.04 MB, `c_world-weather-visuals`), full (scratch, deleted after reading)
- **Grade:** E visual, audio or UI only (no gameplay change) | **gameplay perceptibility:** low | **visual/audio impact:** high | **layers:** D0 content/text | **domain:** textures/models/animations
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `1.*`, loads on 1.9.8: yes (wildcard)
- **Where it changes things:** textures: 257; pak (container): 4; manifest: 1; ini (text settings): 1; other: 1; lua identical to vanilla: 0
- **Risk:** none

## 1196 Better graphics reshade (P4, Reshade / ENB / visual preset)

- **What the author says (Nexus summary):** Better graphics reshade is a mod that aims to improve the graphics in the game.
- **File:** `Better_graphics Reshade-1196-V-1-0-1610810923.zip` (archive, 0.01 MB, `c_reshade-enb-visual-preset`), full (scratch, deleted after reading)
- **Grade:** E visual, audio or UI only (no gameplay change) | **gameplay perceptibility:** none | **visual/audio impact:** high | **layers:** D0 content/text | **domain:** post-processing (ReShade/ENB)
- **How it installs:** unclear: read the archive's own instructions; manifest id `-`, supports `-`, loads on 1.9.8: no manifest (legacy install)
- **Where it changes things:** reshade/ENB (shaders, presets): 1; lua identical to vanilla: 0
- **Risk:** none

## 1197 Proper Cyrillic Fonts (P3, Maps / UI / HUD)

- **What the author says (Nexus summary):** This mod introduce proper (closer to original) glyphs to cyrillic subset of game fonts.Enjoy the beauty of medieval calligraphy.
- **File:** `ProperCyrillicFonts.zip-1197-1-2-1612480063.zip` (archive, 12.68 MB, `c_maps-ui-hud`), full (scratch, deleted after reading)
- **Grade:** E visual, audio or UI only (no gameplay change) | **gameplay perceptibility:** none | **visual/audio impact:** medium | **layers:** D0 content/text | **domain:** UI
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `(none)`, loads on 1.9.8: yes (no version restriction)
- **Where it changes things:** ui: 2; manifest: 1; pak (container): 1; lua identical to vanilla: 0
- **Risk:** none

## 1218 Lartigue's Upscale Project 2.0 - Upscaled UI and icons (P3, Maps / UI / HUD)

- **What the author says (Nexus summary):** Full AI upscale of the game's UI.
- **File:** `LartiguesUpscaleProject2.1-1218-2-1-1734099038` (folder (already extracted), 0 MB, `c_maps-ui-hud`), read in place (already extracted by the author)
- **Grade:** E visual, audio or UI only (no gameplay change) | **gameplay perceptibility:** low | **visual/audio impact:** high | **layers:** D0 content/text | **domain:** textures/models/animations
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `(none)`, loads on 1.9.8: yes (no version restriction)
- **Where it changes things:** textures: 945; manifest: 1; other: 1; lua identical to vanilla: 0
- **Risk:** MEDIUM: MEDIUM: nested archive (not readable by the game): Data/GameData.7zip

## 1218 Lartigue's Upscale Project 2.0 - Upscaled UI and icons (P3, Maps / UI / HUD)

- **What the author says (Nexus summary):** Full AI upscale of the game's UI.
- **File:** `LartiguesUpscaleProject2.1.1-1218-2-1-1-1750232674.zip` (archive, 311.86 MB, `c_maps-ui-hud`), full (scratch, deleted after reading)
- **Grade:** E visual, audio or UI only (no gameplay change) | **gameplay perceptibility:** low | **visual/audio impact:** high | **layers:** D0 content/text | **domain:** textures/models/animations
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `(none)`, loads on 1.9.8: yes (no version restriction)
- **Where it changes things:** textures: 945; manifest: 1; other: 1; pak (container): 1; lua identical to vanilla: 0
- **Risk:** none

## 1256 Horus 2.0 KCD Reshade Preset (P4, Reshade / ENB / visual preset)

- **What the author says (Nexus summary):** Reshade Preset for "Kingdom Come: Deliverance" to greatly improve your visual experience.
- **File:** `Horus 2.0 KCD-1256-2-0-1662311636.zip` (archive, 0.0 MB, `c_reshade-enb-visual-preset`), full (scratch, deleted after reading)
- **Grade:** E visual, audio or UI only (no gameplay change) | **gameplay perceptibility:** none | **visual/audio impact:** high | **layers:** D0 content/text | **domain:** post-processing (ReShade/ENB)
- **How it installs:** unclear: read the archive's own instructions; manifest id `-`, supports `-`, loads on 1.9.8: no manifest (legacy install)
- **Where it changes things:** reshade/ENB (shaders, presets): 1; lua identical to vanilla: 0
- **Risk:** none

## 1258 vShade for GShade Realistic Graphic Preset (P4, Reshade / ENB / visual preset)

- **What the author says (Nexus summary):** You will see KCD like never before.
- **File:** `vShade-1258-1-0-1625557844.zip` (archive, 0.0 MB, `c_reshade-enb-visual-preset`), full (scratch, deleted after reading)
- **Grade:** E visual, audio or UI only (no gameplay change) | **gameplay perceptibility:** none | **visual/audio impact:** high | **layers:** D0 content/text | **domain:** post-processing (ReShade/ENB)
- **How it installs:** unclear: read the archive's own instructions; manifest id `-`, supports `-`, loads on 1.9.8: no manifest (legacy install)
- **Where it changes things:** reshade/ENB (shaders, presets): 1; lua identical to vanilla: 0
- **Risk:** none

## 1283 KINGDOM CINEMATIC ReShade (P4, Reshade / ENB / visual preset)

- **What the author says (Nexus summary):** A Lightweight ReShade preset that gives the game a much brighter and warmer environment as well as sharpness and visual clarity.
- **File:** `Kingdom Cinematic ReShade-1283-2-0-1728918057.rar` (archive, 0.02 MB, `c_reshade-enb-visual-preset`), full (scratch, deleted after reading)
- **Grade:** E visual, audio or UI only (no gameplay change) | **gameplay perceptibility:** none | **visual/audio impact:** high | **layers:** D0 content/text | **domain:** post-processing (ReShade/ENB)
- **How it installs:** unclear: read the archive's own instructions; manifest id `-`, supports `-`, loads on 1.9.8: no manifest (legacy install)
- **Where it changes things:** reshade/ENB (shaders, presets): 1; lua identical to vanilla: 0
- **Risk:** none

## 1291 Eye Candy Reshade (P4, Reshade / ENB / visual preset)

- **What the author says (Nexus summary):** IntroductionHello and welcome to my first ever Reshade Preset for KCD!I tried to make this as realistic and beautiful as possible without any oversharpening etc.This preset is for Reshade 4.9.1WARNING: I am not responsible for your game
- **File:** `Eye Candy Reshade Preset-1291-1-0-1636232494.rar` (archive, 0.0 MB, `c_reshade-enb-visual-preset`), full (scratch, deleted after reading)
- **Grade:** E visual, audio or UI only (no gameplay change) | **gameplay perceptibility:** none | **visual/audio impact:** high | **layers:** D0 content/text | **domain:** post-processing (ReShade/ENB)
- **How it installs:** unclear: read the archive's own instructions; manifest id `-`, supports `-`, loads on 1.9.8: no manifest (legacy install)
- **Where it changes things:** reshade/ENB (shaders, presets): 1; lua identical to vanilla: 0
- **Risk:** none

## 1337 Helmet Vision (P3, Weapons / armor / items)

- **What the author says (Nexus summary):** Improves/Widens your Helmet vision by 20%
- **File:** `WhisHelmetVision-1337-1-2-1644818002.rar` (archive, 1.45 MB, `c_weapons-armor-items`), full (scratch, deleted after reading)
- **Grade:** E visual, audio or UI only (no gameplay change) | **gameplay perceptibility:** low | **visual/audio impact:** medium | **layers:** D0 content/text | **domain:** textures/models/animations, UI
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `(none)`, loads on 1.9.8: yes (no version restriction)
- **Where it changes things:** textures: 9; manifest: 1; pak (container): 1; ui: 1; lua identical to vanilla: 0
- **Risk:** none

## 1349 Natural Reshade (P4, Reshade / ENB / visual preset)

- **What the author says (Nexus summary):** Uses qUINT_mxao, needs access to depth buffer.
- **File:** `Reshade preset-1349-1-0-1646765704.zip` (archive, 18.84 MB, `c_reshade-enb-visual-preset`), full (scratch, deleted after reading)
- **Grade:** E visual, audio or UI only (no gameplay change) | **gameplay perceptibility:** none | **visual/audio impact:** high | **layers:** D0 content/text | **domain:** post-processing (ReShade/ENB)
- **How it installs:** unclear: read the archive's own instructions; manifest id `-`, supports `-`, loads on 1.9.8: no manifest (legacy install)
- **Where it changes things:** reshade/ENB (shaders, presets): 48; lua identical to vanilla: 0
- **Risk:** none

## 1373 Custom UI Loading progress (P3, Maps / UI / HUD)

- **What the author says (Nexus summary):** First mod upload for KCD.More to come.Contains 5 dds graphics to overwrite 5 original dds graphics to alter the loading progress UI element of the game.
- **File:** `UI Loading Progress Retexture-1373-1-0-1652104461.zip` (archive, 0.14 MB, `c_maps-ui-hud`), full (scratch, deleted after reading)
- **Grade:** E visual, audio or UI only (no gameplay change) | **gameplay perceptibility:** low | **visual/audio impact:** medium | **layers:** D0 content/text | **domain:** textures/models/animations
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `(none)`, loads on 1.9.8: yes (no version restriction)
- **Where it changes things:** textures: 5; manifest: 1; pak (container): 1; lua identical to vanilla: 0
- **Risk:** none

## 1414 Real Life Kingdom Come Experience Reshade (P4, Reshade / ENB / visual preset)

- **What the author says (Nexus summary):** I've made a Reshade that adds more detail to the world making them wood effects stand out more as well as the ground, lighting, walls, vehicle textures and dirt marks, and skin. It also adds a bit more darkness to shadowed areas making it
- **File:** `Real Life Kingdom Come Experience Reshade-1414-1-0-1-1663774303.rar` (archive, 0.0 MB, `c_reshade-enb-visual-preset`), full (scratch, deleted after reading)
- **Grade:** E visual, audio or UI only (no gameplay change) | **gameplay perceptibility:** none | **visual/audio impact:** high | **layers:** D0 content/text | **domain:** post-processing (ReShade/ENB)
- **How it installs:** unclear: read the archive's own instructions; manifest id `-`, supports `-`, loads on 1.9.8: no manifest (legacy install)
- **Where it changes things:** reshade/ENB (shaders, presets): 1; lua identical to vanilla: 0
- **Risk:** none

## 1485 SOLID HELMET VISORS (P3, Weapons / armor / items)

- **What the author says (Nexus summary):** SOLID HELMET VISORS - Redrawn helmet visors to remove blurrines, makes them slightly wider and sharper.
- **File:** `SOLID HELMET VISORS-1485-1-2-1737430681.rar` (archive, 68.96 MB, `c_weapons-armor-items`), full (scratch, deleted after reading)
- **Grade:** E visual, audio or UI only (no gameplay change) | **gameplay perceptibility:** low | **visual/audio impact:** high | **layers:** D0 content/text | **domain:** textures/models/animations
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `(none)`, loads on 1.9.8: yes (no version restriction)
- **Where it changes things:** textures: 52; manifest: 3; pak (container): 3; docs: 1; lua identical to vanilla: 0
- **Risk:** none

## 1511 JSCR - Just simple custom Reshade (P4, Reshade / ENB / visual preset)

- **What the author says (Nexus summary):** Base on Sovereign reshade and apex enb, i tweak some setting to make it lightning look most natural and real like in Bohemia 1403. It contains Tonemap, technicolor2, fimicpass, level, curve,dpx, level plus,clarity...
- **File:** `JSCR RESHADE V3-1511-V3-0-1687154831.rar` (archive, 20.22 MB, `c_reshade-enb-visual-preset`), full (scratch, deleted after reading)
- **Grade:** E visual, audio or UI only (no gameplay change) | **gameplay perceptibility:** none | **visual/audio impact:** high | **layers:** D0 content/text | **domain:** post-processing (ReShade/ENB)
- **How it installs:** unclear: read the archive's own instructions; manifest id `-`, supports `-`, loads on 1.9.8: no manifest (legacy install)
- **Where it changes things:** reshade/ENB (shaders, presets): 133; lua identical to vanilla: 0
- **Risk:** none

## 1544 Summertime Reshade for Kindom Come (P4, Reshade / ENB / visual preset)

- **What the author says (Nexus summary):** Better colors and Ambient Occlusion
- **File:** `Flunkiii Reshade for Kingdom Come-1544-1-0-1694268222.zip` (archive, 0.01 MB, `c_reshade-enb-visual-preset`), full (scratch, deleted after reading)
- **Grade:** E visual, audio or UI only (no gameplay change) | **gameplay perceptibility:** none | **visual/audio impact:** high | **layers:** D0 content/text | **domain:** post-processing (ReShade/ENB)
- **How it installs:** unclear: read the archive's own instructions; manifest id `-`, supports `-`, loads on 1.9.8: no manifest (legacy install)
- **Where it changes things:** reshade/ENB (shaders, presets): 1; lua identical to vanilla: 0
- **Risk:** none

## 1570 Karnages_Inventory_Recolour (P3, Maps / UI / HUD)

- **What the author says (Nexus summary):** Changes the colour of the inventory
- **File:** `Karnages_Inventory_Recolour-1570-1-0-0-1700624167.7z` (archive, 3.59 MB, `c_maps-ui-hud`), full (scratch, deleted after reading)
- **Grade:** E visual, audio or UI only (no gameplay change) | **gameplay perceptibility:** low | **visual/audio impact:** medium | **layers:** D0 content/text | **domain:** textures/models/animations
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `(none)`, loads on 1.9.8: yes (no version restriction)
- **Where it changes things:** textures: 13; manifest: 1; pak (container): 1; lua identical to vanilla: 0
- **Risk:** none

## 1577 Invisible hands FIX (UPDATE) (P3, Fix bundle)

- **What the author says (Nexus summary):** This will fix the invisible forearms when wearing sleeveless clothes
- **File:** `Vest Fix 3.0-1577-3-0-1702474761.zip` (archive, 1.26 MB, `c_fix-bundle`), full (scratch, deleted after reading)
- **Grade:** E visual, audio or UI only (no gameplay change) | **gameplay perceptibility:** low | **visual/audio impact:** low | **layers:** D0 content/text | **domain:** textures/models/animations
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `(none)`, loads on 1.9.8: yes (no version restriction)
- **Where it changes things:** manifest: 1; pak (container): 1; textures: 1; lua identical to vanilla: 0
- **Risk:** none

## 1589 Realistic Colour Correction Kingdom Come Deliverance (P4, Reshade / ENB / visual preset)

- **What the author says (Nexus summary):** This Reshade presset improves the color scheme in the game,       balances the contrast, color brightness.
- **File:** `Realistic Colour Correction Kingdom Come Deliveran-1589-1-0-1705385136.rar` (archive, 0.01 MB, `c_reshade-enb-visual-preset`), full (scratch, deleted after reading)
- **Grade:** E visual, audio or UI only (no gameplay change) | **gameplay perceptibility:** none | **visual/audio impact:** high | **layers:** D0 content/text | **domain:** post-processing (ReShade/ENB)
- **How it installs:** unclear: read the archive's own instructions; manifest id `-`, supports `-`, loads on 1.9.8: no manifest (legacy install)
- **Where it changes things:** other: 1; reshade/ENB (shaders, presets): 1; lua identical to vanilla: 0
- **Risk:** none

## 1618 HD Clock Retexture - Inventory Clock Updated (P3, Maps / UI / HUD)

- **What the author says (Nexus summary):** Now the clock at inventory page and fast travel page are also retextured. Retexture of the time spinner in wait interface, inventory and fast travel.
- **File:** `Time-HD-updated v1.2.zip-1618-1-2-1714429516.zip` (archive, 0.43 MB, `c_maps-ui-hud`), full (scratch, deleted after reading)
- **Grade:** E visual, audio or UI only (no gameplay change) | **gameplay perceptibility:** low | **visual/audio impact:** low | **layers:** D0 content/text | **domain:** textures/models/animations
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `(none)`, loads on 1.9.8: yes (no version restriction)
- **Where it changes things:** textures: 2; manifest: 1; pak (container): 1; lua identical to vanilla: 0
- **Risk:** none

## 1723 Intimidation Stat In Inventory (P3, Maps / UI / HUD)

- **What the author says (Nexus summary):** Displaying current intimidation stat in inventory.
- **File:** `IntimidationStat-1723-1-1-1728217688` (folder (already extracted), 0 MB, `c_maps-ui-hud`), read in place (already extracted by the author)
- **Grade:** E visual, audio or UI only (no gameplay change) | **gameplay perceptibility:** none | **visual/audio impact:** medium | **layers:** D0 content/text | **domain:** UI
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `(none)`, loads on 1.9.8: yes (no version restriction)
- **Where it changes things:** manifest: 1; other: 1; ui: 1; lua identical to vanilla: 0
- **Risk:** MEDIUM: MEDIUM: nested archive (not readable by the game): Data/IntimidationStat.7zip

## 1800 KCD 2 Reshade (P4, Reshade / ENB / visual preset)

- **What the author says (Nexus summary):** Adds clarity, color correction, depth, better overall lightning, deeper shadows,
- **File:** `KCD2 Reshade-1800-1-0-1737510963.rar` (archive, 0.01 MB, `c_reshade-enb-visual-preset`), full (scratch, deleted after reading)
- **Grade:** E visual, audio or UI only (no gameplay change) | **gameplay perceptibility:** none | **visual/audio impact:** high | **layers:** D0 content/text | **domain:** post-processing (ReShade/ENB)
- **How it installs:** unclear: read the archive's own instructions; manifest id `-`, supports `-`, loads on 1.9.8: no manifest (legacy install)
- **Where it changes things:** reshade/ENB (shaders, presets): 1; lua identical to vanilla: 0
- **Risk:** none

## 1875 KCD1 Enhanced Visuals - UBER Graphics ReShade (P4, Reshade / ENB / visual preset)

- **What the author says (Nexus summary):** A ReShade preset that aims to further enhance the visual fidelity and better immerse you in the gameworld.Works best with "UBER Quality Mod".(HDR Compatible)
- **File:** `KCD1 - Enhanced Visuals - R3MIND ReShade-1875-1-0-0-1739656641.rar` (archive, 0.0 MB, `c_reshade-enb-visual-preset`), full (scratch, deleted after reading)
- **Grade:** E visual, audio or UI only (no gameplay change) | **gameplay perceptibility:** none | **visual/audio impact:** high | **layers:** D0 content/text | **domain:** post-processing (ReShade/ENB)
- **How it installs:** unclear: read the archive's own instructions; manifest id `-`, supports `-`, loads on 1.9.8: no manifest (legacy install)
- **Where it changes things:** reshade/ENB (shaders, presets): 2; lua identical to vanilla: 0
- **Risk:** none

## 1900 Jiggle Physics (P4, Adult / nudity)

- **What the author says (Nexus summary):** Adds Jiggle Physics
- **File:** `Jiggle Physics 1900 1.2 2026-07-17T22-19Z lzEbrHFy3.zip` (archive, 0.01 MB, `c_adult-nudity`), full (scratch, deleted after reading)
- **Grade:** E visual, audio or UI only (no gameplay change) | **gameplay perceptibility:** low | **visual/audio impact:** high | **layers:** D0 content/text | **domain:** textures/models/animations
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `(none)`, loads on 1.9.8: yes (no version restriction)
- **Where it changes things:** models/animations/materials: 12; pak (container): 2; manifest: 1; lua identical to vanilla: 0
- **Risk:** none

## 1907 Visorless Helmets (P3, Weapons / armor / items)

- **What the author says (Nexus summary):** Visorless helmets to make Henry look normal in conversations
- **File:** `Visorless Helmets-1907-1-0-2-1741145962.zip` (archive, 4.47 MB, `c_weapons-armor-items`), full (scratch, deleted after reading)
- **Grade:** E visual, audio or UI only (no gameplay change) | **gameplay perceptibility:** low | **visual/audio impact:** medium | **layers:** D0 content/text | **domain:** textures/models/animations
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `1.9.*`, loads on 1.9.8: yes (wildcard)
- **Where it changes things:** pak (container): 5; textures: 5; manifest: 1; lua identical to vanilla: 0
- **Risk:** none

## 1918 KCD1 Reborn - Verdant Vegetation (P3, World / weather / visuals)

- **What the author says (Nexus summary):** This mod enriches KCD1 with lush, dense vegetation, bringing a more vibrant and immersive natural environment inspired by KCD2. Carefully optimized for performance and visual quality, it enhances forests, fields, and foliage for a more
- **File:** `Checkers Verdant Vegetation-1918-1-0-1743125688.zip` (archive, 177.03 MB, `c_world-weather-visuals`), full (scratch, deleted after reading)
- **Grade:** E visual, audio or UI only (no gameplay change) | **gameplay perceptibility:** low | **visual/audio impact:** high | **layers:** D0 content/text | **domain:** textures/models/animations
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `(none)`, loads on 1.9.8: yes (no version restriction)
- **Where it changes things:** textures: 66; manifest: 1; pak (container): 1; lua identical to vanilla: 0
- **Risk:** none

## 1927 KCD1 Reborn-Terrain and Structures (P3, World / weather / visuals)

- **What the author says (Nexus summary):** This mod brings a complete overhaul to the textures of both the terrain and structures in Kingdom Come: Deliverance.
- **File:** `Checkers Terrain and Structures-1927-1-3-5-1743121857 (1).zip` (archive, 1879.35 MB, `c_world-weather-visuals`), full (scratch, deleted after reading)
- **Grade:** E visual, audio or UI only (no gameplay change) | **gameplay perceptibility:** low | **visual/audio impact:** high | **layers:** D0 content/text | **domain:** textures/models/animations
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `(none)`, loads on 1.9.8: yes (no version restriction)
- **Where it changes things:** textures: 196; manifest: 1; pak (container): 1; lua identical to vanilla: 0
- **Risk:** none

## 1961 Unconscious Crime UI (P3, Crime / stealth / loot)

- **What the author says (Nexus summary):** I feel it's little too much that you can view map and see where your crime has been reported.
- **File:** `Unconscious Crime UI-1961-1-0-1742809272.zip` (archive, 0.0 MB, `c_crime-stealth-loot`), full (scratch, deleted after reading)
- **Grade:** E visual, audio or UI only (no gameplay change) | **gameplay perceptibility:** low | **visual/audio impact:** low | **layers:** D0 content/text | **domain:** textures/models/animations
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `1.9.6`, loads on 1.9.8: NO (disabled: lists 1.9.6)
- **Where it changes things:** textures: 2; manifest: 1; pak (container): 1; lua identical to vanilla: 0
- **Risk:** none

## 1964 KCD1 Reborn - Enhanced Faces and Skin (P3, World / weather / visuals)

- **What the author says (Nexus summary):** This mod not only improves face and skin textures with sharper details but completely eliminates the issue of slow loading and late face rendering. NPCs will always appear clear and natural, without blurry or delayed textures.
- **File:** `Checkers Enhanced Faces and Skin-1964-0-95-1743115948 (1).zip` (archive, 2001.68 MB, `c_world-weather-visuals`), full (scratch, deleted after reading)
- **Grade:** E visual, audio or UI only (no gameplay change) | **gameplay perceptibility:** low | **visual/audio impact:** high | **layers:** D0 content/text | **domain:** textures/models/animations
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `(none)`, loads on 1.9.8: yes (no version restriction)
- **Where it changes things:** textures: 155; manifest: 1; pak (container): 1; lua identical to vanilla: 0
- **Risk:** none

## 1980 Medieval Loading Screens (P3, Maps / UI / HUD)

- **What the author says (Nexus summary):** Turns some of the Codex images into loading screens.
- **File:** `MedievalLoadingScreens-1980-1-1-1744118421 (1).rar` (archive, 12.42 MB, `c_maps-ui-hud`), full (scratch, deleted after reading)
- **Grade:** E visual, audio or UI only (no gameplay change) | **gameplay perceptibility:** low | **visual/audio impact:** high | **layers:** D0 content/text | **domain:** textures/models/animations, UI
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `1.*`, loads on 1.9.8: yes (wildcard)
- **Where it changes things:** textures: 23; manifest: 1; pak (container): 1; ui: 1; lua identical to vanilla: 0
- **Risk:** none

## 2008 Perfection (P3, Other)

- **What the author says (Nexus summary):** Needs access to depth-buffer.
- **File:** `Preset-2008-1-0-1748032883.zip` (archive, 0.15 MB, `c_other`), full (scratch, deleted after reading)
- **Grade:** E visual, audio or UI only (no gameplay change) | **gameplay perceptibility:** none | **visual/audio impact:** high | **layers:** D0 content/text | **domain:** post-processing (ReShade/ENB)
- **How it installs:** unclear: read the archive's own instructions; manifest id `-`, supports `-`, loads on 1.9.8: no manifest (legacy install)
- **Where it changes things:** reshade/ENB (shaders, presets): 69; lua identical to vanilla: 0
- **Risk:** MEDIUM: MEDIUM: nested archive (not readable by the game): reshade-shaders/Shaders/dragoncosmico/BloomSat/BloomSat v1.0.zip / MEDIUM: nested archive (not readable by the game): reshade-shaders/Shaders/dragoncosmico/BloomSat/BloomSat v1.1.zip / MEDIUM: nested archive (not readable by the game): reshade-shaders/Shaders/dragoncosmico/BloomSat/BloomSat v2.0.zip / MEDIUM: nested archive (not readable by the game): reshade-shaders/Shaders/dragoncosmico/BloomSat/BloomSat v2.1.zip / MEDIUM: nested archive (not 

## 2030 Clean and Minimal HUD and Map (P3, Maps / UI / HUD)

- **What the author says (Nexus summary):** Makes vanilla HUD and Map elements smaller and transparent for less intrusive and more immersive experience.
- **File:** `Clean and Minimal HUD-2030-0-1-1749657994.zip` (archive, 0.94 MB, `c_maps-ui-hud`), full (scratch, deleted after reading)
- **Grade:** E visual, audio or UI only (no gameplay change) | **gameplay perceptibility:** low | **visual/audio impact:** high | **layers:** D0 content/text | **domain:** textures/models/animations
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `(none)`, loads on 1.9.8: yes (no version restriction)
- **Where it changes things:** textures: 97; manifest: 1; pak (container): 1; lua identical to vanilla: 0
- **Risk:** none

## 2031 Mud and Iron Kingdom Come Deliverance Reshade (P4, Reshade / ENB / visual preset)

- **What the author says (Nexus summary):** A Vanilla+ reshade for better colour, contrast and sharpness with 2 Versions.Each one has a brighter one.
- **File:** `Mud and Iron Kingdom Come Deliverance Reshade-2031-1-0-1749855727 (1).7z` (archive, 0.0 MB, `c_reshade-enb-visual-preset`), full (scratch, deleted after reading)
- **Grade:** E visual, audio or UI only (no gameplay change) | **gameplay perceptibility:** none | **visual/audio impact:** high | **layers:** D0 content/text | **domain:** post-processing (ReShade/ENB)
- **How it installs:** unclear: read the archive's own instructions; manifest id `-`, supports `-`, loads on 1.9.8: no manifest (legacy install)
- **Where it changes things:** reshade/ENB (shaders, presets): 1; lua identical to vanilla: 0
- **Risk:** none

## 2031 Mud and Iron Kingdom Come Deliverance Reshade (P4, Reshade / ENB / visual preset)

- **What the author says (Nexus summary):** A Vanilla+ reshade for better colour, contrast and sharpness with 2 Versions.Each one has a brighter one.
- **File:** `Mud and Iron Kingdom Come Deliverance Reshade-2031-1-0-1749855727.7z` (archive, 0.0 MB, `c_reshade-enb-visual-preset`), full (scratch, deleted after reading)
- **Grade:** E visual, audio or UI only (no gameplay change) | **gameplay perceptibility:** none | **visual/audio impact:** high | **layers:** D0 content/text | **domain:** post-processing (ReShade/ENB)
- **How it installs:** unclear: read the archive's own instructions; manifest id `-`, supports `-`, loads on 1.9.8: no manifest (legacy install)
- **Where it changes things:** reshade/ENB (shaders, presets): 1; lua identical to vanilla: 0
- **Risk:** none

## 2103 Pickpocket menu  from KCD2 (P3, Crime / stealth / loot)

- **What the author says (Nexus summary):** Replaces the original pickpocket wheel in Kingdom Come: Deliverance 1 with the updated, clean and beautiful version from Kingdom Come: Deliverance 2.
- **File:** `pickpocket_kcd2 1.1-2103-1-1-0-1764612642 (1).zip` (archive, 2.73 MB, `c_crime-stealth-loot`), full (scratch, deleted after reading)
- **Grade:** E visual, audio or UI only (no gameplay change) | **gameplay perceptibility:** low | **visual/audio impact:** medium | **layers:** D0 content/text | **domain:** textures/models/animations, UI
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `1.*`, loads on 1.9.8: yes (wildcard)
- **Where it changes things:** textures: 11; manifest: 1; pak (container): 1; ui: 1; lua identical to vanilla: 0
- **Risk:** none

## 2108 New KCD HUD 2.0 (P3, Maps / UI / HUD)

- **What the author says (Nexus summary):** This mod completely overhauls the look of the HUD in Kingdom Come: Deliverance, making it cleaner, more modern, and more visually appealing.
- **File:** `new_hud_2.0 1.3-2108-1-3-0-1770680449 (1).rar` (archive, 2.97 MB, `c_maps-ui-hud`), full (scratch, deleted after reading)
- **Grade:** E visual, audio or UI only (no gameplay change) | **gameplay perceptibility:** low | **visual/audio impact:** medium | **layers:** D0 content/text | **domain:** textures/models/animations, UI
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `1.*`, loads on 1.9.8: yes (wildcard)
- **Where it changes things:** textures: 15; manifest: 1; pak (container): 1; ui: 1; lua identical to vanilla: 0
- **Risk:** none

## 2152 Lighting and Shadow 2.0 - ENB for KCD (P4, Reshade / ENB / visual preset)

- **What the author says (Nexus summary):** ENB/ReShade graphics preset with two variants ENB Preset for KCD
- **File:** `ENB MartinSpielt Preset-2152-1-0-1770911762.zip` (archive, 0.03 MB, `c_reshade-enb-visual-preset`), full (scratch, deleted after reading)
- **Grade:** E visual, audio or UI only (no gameplay change) | **gameplay perceptibility:** none | **visual/audio impact:** high | **layers:** D0 content/text | **domain:** post-processing (ReShade/ENB)
- **How it installs:** unclear: read the archive's own instructions; manifest id `-`, supports `-`, loads on 1.9.8: no manifest (legacy install)
- **Where it changes things:** reshade/ENB (shaders, presets): 16; lua identical to vanilla: 0
- **Risk:** none

## 2196 ENHANCED Adult Bounce KCD I (P4, Adult / nudity)

- **What the author says (Nexus summary):** Add realistic breast physics to your game! Enjoy natural movements and animations that make gameplay more immersive and lifelike.
- **File:** `ENHANCED Adult Bounce KCD1-2196-2-0-1774424692.rar` (archive, 0.01 MB, `c_adult-nudity`), full (scratch, deleted after reading)
- **Grade:** E visual, audio or UI only (no gameplay change) | **gameplay perceptibility:** low | **visual/audio impact:** high | **layers:** D0 content/text | **domain:** textures/models/animations
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `enhancedadultbounce`, supports `(none)`, loads on 1.9.8: yes (no version restriction)
- **Where it changes things:** models/animations/materials: 12; manifest: 1; pak (container): 1; lua identical to vanilla: 0
- **Risk:** none

## 2199 DualSense Buttons (P3, Maps / UI / HUD)

- **What the author says (Nexus summary):** Adds visual representations of DualSense gamepad buttons to the game for more intuitive control.  Now, all actions are highlighted with the iconic DualSense button prompts, enhancing immersion and making the interface feel truly next-gen.
- **File:** `DualSense Buttons-2199-2-0-1778555602.rar` (archive, 0.68 MB, `c_maps-ui-hud`), full (scratch, deleted after reading)
- **Grade:** E visual, audio or UI only (no gameplay change) | **gameplay perceptibility:** low | **visual/audio impact:** high | **layers:** D0 content/text | **domain:** textures/models/animations
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `1.9.*`, loads on 1.9.8: yes (wildcard)
- **Where it changes things:** textures: 23; manifest: 1; pak (container): 1; lua identical to vanilla: 0
- **Risk:** none

## 2293 Bigger Hud (KCD1) (P3, Maps / UI / HUD)

- **What the author says (Nexus summary):** Increases the size of the Compass and QAM Bar
- **File:** `Bigger Hud KCD1 2.0 Update 2293 2 2026-07-19T03-12Z A6blGm0FF.zip` (archive, 0.2 MB, `c_maps-ui-hud`), full (scratch, deleted after reading)
- **Grade:** E visual, audio or UI only (no gameplay change) | **gameplay perceptibility:** none | **visual/audio impact:** medium | **layers:** D0 content/text | **domain:** UI
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `1.9.4 1.9.5 1.9.6 1.9.7 1.9.8`, loads on 1.9.8: yes (explicit)
- **Where it changes things:** ui: 2; manifest: 1; pak (container): 1; lua identical to vanilla: 0
- **Risk:** none

## 2297 Ultimate Loadingscreen Artwork Overhaul (P3, Animations / audio)

- **What the author says (Nexus summary):** Tired of staring at the same 6 loading screens? This mod adds 37 new artworks to the rotation and gives the existing ones a visual upgrade.
- **File:** `Ultimate Loadingscreen Overhaul 2297 1.1 2026-07-19T21-10Z 2jGTl3Qoz.zip` (archive, 45.66 MB, `c_animations-audio`), full (scratch, deleted after reading)
- **Grade:** E visual, audio or UI only (no gameplay change) | **gameplay perceptibility:** low | **visual/audio impact:** high | **layers:** D0 content/text | **domain:** textures/models/animations, UI
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `1.*`, loads on 1.9.8: yes (wildcard)
- **Where it changes things:** textures: 44; manifest: 1; pak (container): 1; ui: 1; lua identical to vanilla: 0
- **Risk:** none

## 2317 Enemy Health Bar (P3, Maps / UI / HUD)

- **What the author says (Nexus summary):** This mod displays the locked-on enemy's health bar at the top-center of the screen. ロックオンしている敵の体力が画面中央上に大きく表示されるMODです。
- **File:** `EnemyBar 2317 1 2026-07-31T06-38Z VnT2AzaAK.zip` (archive, 0.1 MB, `c_maps-ui-hud`), full (scratch, deleted after reading)
- **Grade:** E visual, audio or UI only (no gameplay change) | **gameplay perceptibility:** none | **visual/audio impact:** medium | **layers:** D0 content/text | **domain:** UI
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `(none)`, loads on 1.9.8: yes (no version restriction)
- **Where it changes things:** manifest: 1; pak (container): 1; ui: 1; lua identical to vanilla: 0
- **Risk:** none

## 2330 Compass and Map Upgrades - Wayfinder (P3, Maps / UI / HUD)

- **What the author says (Nexus summary):** Your map marker points the way and clears itself when you arrive, plus free map zoom
- **File:** `Wayfinder 1.0.2 (Compatibility Patched) 2330 2 2026-09-10T02-01Z 6b3zKD4Qh.zip` (archive, 0.32 MB, `c_maps-ui-hud`), full (scratch, deleted after reading)
- **Grade:** E visual, audio or UI only (no gameplay change) | **gameplay perceptibility:** none | **visual/audio impact:** medium | **layers:** D0 content/text | **domain:** UI
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `(none)`, loads on 1.9.8: yes (no version restriction)
- **Where it changes things:** ui: 9; manifest: 1; docs: 1; pak (container): 1; lua identical to vanilla: 0
- **Risk:** none

## 2349 KCD1 Map Cursor Contrast - Visible Ring and X (P3, Maps / UI / HUD)

- **What the author says (Nexus summary):** Makes the Kingdom Come: Deliverance map cursor easier to see while preserving the original ring-and-X shape. Includes a tested stable version and an optional bold variant.
- **File:** `MapCursorContrast Bold 2.1.0 2349 2.1.0 2026-09-05T04-03Z QeXoFvWUO.zip` (archive, 0.01 MB, `c_maps-ui-hud`), full (scratch, deleted after reading)
- **Grade:** E visual, audio or UI only (no gameplay change) | **gameplay perceptibility:** low | **visual/audio impact:** low | **layers:** D0 content/text | **domain:** textures/models/animations
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `map_cursor_contrast`, supports `(none)`, loads on 1.9.8: yes (no version restriction)
- **Where it changes things:** manifest: 1; docs: 1; pak (container): 1; textures: 1; lua identical to vanilla: 0
- **Mentions:** Vortex
- **Risk:** none

## 2384 KCD HI-Res Maps (P3, Maps / UI / HUD)

- **What the author says (Nexus summary):** All in-game maps from KCD (region and locations), extracted from game files, to be used as reference, wallpapers, RPG material, etc.
- **File:** `KCD In-game Maps 2384 1.0.0 2026-10-02T17-16Z LQeSByZ98.zip` (archive, 70.82 MB, `c_maps-ui-hud`), full (scratch, deleted after reading)
- **Grade:** E visual, audio or UI only (no gameplay change) | **gameplay perceptibility:** low | **visual/audio impact:** medium | **layers:** D0 content/text | **domain:** textures/models/animations
- **How it installs:** unclear: read the archive's own instructions; manifest id `-`, supports `-`, loads on 1.9.8: no manifest (legacy install)
- **Where it changes things:** textures: 18; lua identical to vanilla: 0
- **Risk:** none

## 797 Inventoried (P3, Maps / UI / HUD)

- **What the author says (Nexus summary):** Renames and tags every item for sorting (User Interface); per-language text This mod sorts 100% of all in-game items in your inventory by adding (Tags), and painstakingly renaming every single item for maximum utility and readability. // Expanding upon the original item categories, the result is a c
- **File:** `Inventoried - Standard-797-1-6-3-1605332384.zip` (archive, 0.02 MB, `c_maps-ui-hud`), full (scratch, deleted after reading)
- **Grade:** E text only (no gameplay change) | **gameplay perceptibility:** low | **visual/audio impact:** low | **layers:** D0 content/text | **domain:** text
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `1.9.*`, loads on 1.9.8: yes (wildcard)
- **Where it changes things:** localization: 2; manifest: 1; lua identical to vanilla: 0
- **Text:** 1393 strings changed, 2 new
- **Risk:** none

## 1780 Timed Quest Indicator (P3, Maps / UI / HUD)

- **What the author says (Nexus summary):** Add an indication to the quest log for quests that are time sensitive.
- **File:** `TimedQuestIndicator-1780-V1-1-1736764991.7z` (archive, 0.0 MB, `c_maps-ui-hud`), full (scratch, deleted after reading)
- **Grade:** E text only (no gameplay change) | **gameplay perceptibility:** low | **visual/audio impact:** low | **layers:** D0 content/text | **domain:** text
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `1.9.6`, loads on 1.9.8: NO (disabled: lists 1.9.6)
- **Where it changes things:** localization: 4; manifest: 2; docs: 1; lua identical to vanilla: 0
- **Text:** 22 strings changed, 0 new
- **Risk:** none

## 1944 Lore Of Die (P3, Quests / lore / content)

- **What the author says (Nexus summary):** Expand how die's experienced in the game.
- **File:** `Die Of Lore-1944-1-3-1756187796.zip` (archive, 0.0 MB, `c_quests-lore-content`), full (scratch, deleted after reading)
- **Grade:** E text only (no gameplay change) | **gameplay perceptibility:** low | **visual/audio impact:** low | **layers:** D0 content/text | **domain:** text
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `1.9.6`, loads on 1.9.8: NO (disabled: lists 1.9.6)
- **Where it changes things:** localization: 2; manifest: 1; lua identical to vanilla: 0
- **Text:** 1 strings changed, 0 new
- **Risk:** none

## 2005 Snarky Loading Screens PTF Edition (P3, Maps / UI / HUD)

- **What the author says (Nexus summary):** Inject some humour into your life, this time without replacing game files.
- **File:** `Snarky Loading Screens PTF-2005-1-0-1746781186.zip` (archive, 0.0 MB, `c_maps-ui-hud`), full (scratch, deleted after reading)
- **Grade:** E text only (no gameplay change) | **gameplay perceptibility:** low | **visual/audio impact:** low | **layers:** D0 content/text | **domain:** text
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `1.9.*`, loads on 1.9.8: yes (wildcard)
- **Where it changes things:** localization: 2; manifest: 1; lua identical to vanilla: 0
- **Text:** 28 strings changed, 0 new
- **Risk:** none

## 2100 Diseases - spolszczenie (P3, (unclassified))

- **What the author says (Nexus summary):** Pełne spolszczenie do moda Diseases. Tłumaczenie zachowuje klimat gry i jest zgodne z oficjalną polską lokalizacją.
- **File:** `Diseases - Spolszczenie-2100-1-0-1763742966.rar` (archive, 0.03 MB, `c_unclassified`), full (scratch, deleted after reading)
- **Grade:** E text only (no gameplay change) | **gameplay perceptibility:** low | **visual/audio impact:** low | **layers:** D0 content/text | **domain:** text
- **How it installs:** loose .pak (legacy: copy into Data); manifest id `-`, supports `-`, loads on 1.9.8: no manifest (legacy install)
- **Where it changes things:** localization: 2; lua identical to vanilla: 0
- **Text:** 8 strings changed, 382 new
- **Risk:** none

## 266 All Referenced Strings In Kingdom Come Deliverance (P3, Tools / reference)

- **What the author says (Nexus summary):** This contains console commands, as well as other things. Search for "wh_" to find Warhorse commands.
- **File:** `All Referenced Strings-266-1-0.7z` (archive, 0.95 MB, `c_tools-reference`), full (scratch, deleted after reading)
- **Grade:** E non-perceptive to gameplay (no effective change found) | **gameplay perceptibility:** none | **visual/audio impact:** none | **layers:** none found | **domain:** none
- **How it installs:** unclear: read the archive's own instructions; manifest id `-`, supports `-`, loads on 1.9.8: no manifest (legacy install)
- **Where it changes things:** docs: 1; lua identical to vanilla: 0
- **Risk:** none

## 502 zzzz_JCD_CLAM (unlisted, (not in the 365 index))

- **What the author says (Nexus summary):** -
- **File:** `CLAM-502-1-2-0.zip` (archive, 0.0 MB, `_unmatched`), full (scratch, deleted after reading)
- **Grade:** E non-perceptive to gameplay (no effective change found) | **gameplay perceptibility:** none | **visual/audio impact:** none | **layers:** none found | **domain:** none
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `1.*`, loads on 1.9.8: yes (wildcard)
- **Where it changes things:** docs: 2; config (.cfg): 1; manifest: 1; pak (container): 1; localization: 1; lua identical to vanilla: 0
- **Mentions:** unpack
- **Risk:** none

## 1367 Apostalus User Configs (P4, Graphics config (cfg))

- **What the author says (Nexus summary):** Enables Volumetric Fog, volumetric fog shadows, FOV 100, FPS Limit of 255, VSync, texture streaming improvements, etc...
- **File:** `Apostalus_User_Config_Mod-1367-1-2-1650769642.zip` (archive, 0.0 MB, `c_graphics-config-cfg`), full (scratch, deleted after reading)
- **Grade:** E non-perceptive to gameplay (no effective change found) | **gameplay perceptibility:** none | **visual/audio impact:** none | **layers:** none found | **domain:** none
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `1.9.*`, loads on 1.9.8: yes (wildcard)
- **Where it changes things:** manifest: 1; other: 1; lua identical to vanilla: 0
- **Risk:** none

## 1479 Batch files for all items sorted and easy to read (P3, Tools / reference)

- **What the author says (Nexus summary):** This is a set of batch files with approximately all item id's in the game.
- **File:** `KCD Batch files-1479-1-0-1676653419.rar` (archive, 0.07 MB, `c_tools-reference`), full (scratch, deleted after reading)
- **Grade:** E non-perceptive to gameplay (no effective change found) | **gameplay perceptibility:** none | **visual/audio impact:** none | **layers:** none found | **domain:** none
- **How it installs:** unclear: read the archive's own instructions; manifest id `-`, supports `-`, loads on 1.9.8: no manifest (legacy install)
- **Where it changes things:** docs: 18; lua identical to vanilla: 0
- **Risk:** none

## 1526 Force High Quality Trees in the distance (P4, Graphics config (cfg))

- **What the author says (Nexus summary):** Forces the game to render High Quality trees in the distance instead of the default 2D billboard trees.
- **File:** `KCD HQ Trees-1526-1-1690937203.zip` (archive, 0.0 MB, `c_graphics-config-cfg`), full (scratch, deleted after reading)
- **Grade:** E non-perceptive to gameplay (no effective change found) | **gameplay perceptibility:** none | **visual/audio impact:** none | **layers:** none found | **domain:** none
- **How it installs:** unclear: read the archive's own instructions; manifest id `-`, supports `-`, loads on 1.9.8: no manifest (legacy install)
- **Where it changes things:** config (.cfg): 3; docs: 1; lua identical to vanilla: 0
- **Mentions:** autoexec.cfg
- **Risk:** none

## 1528 Enchanced Shadows and Shadow Cascades (P4, Graphics config (cfg))

- **What the author says (Nexus summary):** Increased Shadow fidelity by increasing the LOD 0 Sun Shadow Cascade range and increased Shadow Map Resolution.
- **File:** `KCD 2K Shadow Cascades-1528-1-1691349516.zip` (archive, 0.0 MB, `c_graphics-config-cfg`), full (scratch, deleted after reading)
- **Grade:** E non-perceptive to gameplay (no effective change found) | **gameplay perceptibility:** none | **visual/audio impact:** none | **layers:** none found | **domain:** none
- **How it installs:** unclear: read the archive's own instructions; manifest id `-`, supports `-`, loads on 1.9.8: no manifest (legacy install)
- **Where it changes things:** config (.cfg): 2; docs: 1; lua identical to vanilla: 0
- **Mentions:** autoexec.cfg
- **Risk:** none

## 1538 Batch's Ultra Graphics Settings (P4, Graphics config (cfg))

- **What the author says (Nexus summary):** Many tweaks to CryEngine, huge visual impact while retaining the original KCD look that we all love.Read description for more info.
- **File:** `High Preset-1538-1-1692237999.zip` (archive, 0.0 MB, `c_graphics-config-cfg`), full (scratch, deleted after reading)
- **Grade:** E non-perceptive to gameplay (no effective change found) | **gameplay perceptibility:** none | **visual/audio impact:** none | **layers:** none found | **domain:** none
- **How it installs:** unclear: read the archive's own instructions; manifest id `-`, supports `-`, loads on 1.9.8: no manifest (legacy install)
- **Where it changes things:** config (.cfg): 2; docs: 1; lua identical to vanilla: 0
- **Mentions:** autoexec.cfg
- **Risk:** none

## 1538 Batch's Ultra Graphics Settings (P4, Graphics config (cfg))

- **What the author says (Nexus summary):** Many tweaks to CryEngine, huge visual impact while retaining the original KCD look that we all love.Read description for more info.
- **File:** `Medium Preset-1538-1-1692237905.zip` (archive, 0.0 MB, `c_graphics-config-cfg`), full (scratch, deleted after reading)
- **Grade:** E non-perceptive to gameplay (no effective change found) | **gameplay perceptibility:** none | **visual/audio impact:** none | **layers:** none found | **domain:** none
- **How it installs:** unclear: read the archive's own instructions; manifest id `-`, supports `-`, loads on 1.9.8: no manifest (legacy install)
- **Where it changes things:** config (.cfg): 2; docs: 1; lua identical to vanilla: 0
- **Mentions:** autoexec.cfg
- **Risk:** none

## 2132 MOD file override conflicts and PTF patch detection (P3, Fix bundle)

- **What the author says (Nexus summary):** 用于检测MOD中PAK文件里的文件覆盖冲突，以及查询所有PTF补丁文件Used to detect file coverage conflicts in PAK files within mods, and to query all PTF patch files
- **File:** `ModsCheckEng-2132-1-1-1768208612.7z` (archive, 0.0 MB, `c_fix-bundle`), full (scratch, deleted after reading)
- **Grade:** E non-perceptive to gameplay (no effective change found) | **gameplay perceptibility:** none | **visual/audio impact:** none | **layers:** none found | **domain:** none
- **How it installs:** unclear: read the archive's own instructions; manifest id `-`, supports `-`, loads on 1.9.8: no manifest (legacy install)
- **Where it changes things:** docs: 1; lua identical to vanilla: 0
- **Risk:** none

## 2180 Optimized CryEngine simple tweaks (P4, Graphics config (cfg))

- **What the author says (Nexus summary):** High-end CryEngine user.cfg that optimizes memory budgets, texture streaming and anti-aliasing for PCs. Reduces stutter and texture pop-in while keeping a sharp image.
- **File:** `cry engine tweaks-2180-1-1-1772892590.rar` (archive, 0.0 MB, `c_graphics-config-cfg`), full (scratch, deleted after reading)
- **Grade:** E non-perceptive to gameplay (no effective change found) | **gameplay perceptibility:** none | **visual/audio impact:** none | **layers:** none found | **domain:** none
- **How it installs:** unclear: read the archive's own instructions; manifest id `-`, supports `-`, loads on 1.9.8: no manifest (legacy install)
- **Where it changes things:** docs: 1; lua identical to vanilla: 0
- **Risk:** none

## 2216 KCD Mod Organizer Plugin (Steam - GOG - Epic) (P3, Tools / reference)

- **What the author says (Nexus summary):** An advanced MO2 plugin that automatically generates your mod_order.txt upon launch, repairs broken XML manifests on the fly, and enforces strict engine compatibility across all storefronts.
- **File:** `Plugins-2216-3-4-2-1778799500.7z` (archive, 0.0 MB, `_quarantine`), full (scratch, deleted after reading)
- **Grade:** E non-perceptive to gameplay (no effective change found) | **gameplay perceptibility:** none | **visual/audio impact:** none | **layers:** none found | **domain:** none
- **How it installs:** unclear: read the archive's own instructions; manifest id `-`, supports `-`, loads on 1.9.8: no manifest (legacy install)
- **Where it changes things:** other: 1; lua identical to vanilla: 0
- **Risk:** HIGH: HIGH: script or shortcut file: plugins/basic_games/games/game_kingdomcomedeliverance.py (quarantined)

## 2273 Address Library For KCSE (P3, Tools / reference)

- **What the author says (Nexus summary):** Database to make KCSE plugins platform independent
- **File:** `1.9.8 Steam Epic GOG 2273 1 2026-06-29T13-38Z U5RChtbYi.zip` (archive, 7.41 MB, `c_tools-reference`), full (scratch, deleted after reading)
- **Grade:** E non-perceptive to gameplay (no effective change found) | **gameplay perceptibility:** none | **visual/audio impact:** none | **layers:** none found | **domain:** none
- **How it installs:** unclear: read the archive's own instructions; manifest id `-`, supports `-`, loads on 1.9.8: no manifest (legacy install)
- **Where it changes things:** other: 3; lua identical to vanilla: 0
- **Risk:** none

## 2351 Keyboard Controls (P3, Maps / UI / HUD)

- **What the author says (Nexus summary):** If you prefer keyboard & mouse for any reason—especially if you struggle with selecting bottom-left and bottom-right stances using mouse movements—this mod is for you. 何らかの事情でキーボード＆マウス操作にこだわる方。特に戦闘で右下や左下をマウス操作で選ぶのが苦手な人のためのMODです
- **File:** `Keyboard Controls - Global 2351 1 2026-09-06T01-30Z 4yvkqUPWj.zip` (archive, 0.0 MB, `c_maps-ui-hud`), full (scratch, deleted after reading)
- **Grade:** E non-perceptive to gameplay (no effective change found) | **gameplay perceptibility:** none | **visual/audio impact:** none | **layers:** none found | **domain:** none
- **How it installs:** unclear: read the archive's own instructions; manifest id `-`, supports `-`, loads on 1.9.8: no manifest (legacy install)
- **Where it changes things:** other: 1; lua identical to vanilla: 0
- **Risk:** none

## 2367 Pray Animation KCD1 (P3, Quests / lore / content)

- **What the author says (Nexus summary):** This mod consists to Play Animation Sequences for Kingdom Come: Deliverance 1.
- **File:** `Pray Animation KCD1 2367 1 2026-09-18T23-43Z 8HMDLo1Kr.zip` (archive, 0.0 MB, `c_quests-lore-content`), full (scratch, deleted after reading)
- **Grade:** E non-perceptive to gameplay (no effective change found) | **gameplay perceptibility:** none | **visual/audio impact:** none | **layers:** none found | **domain:** none
- **How it installs:** unclear: read the archive's own instructions; manifest id `-`, supports `-`, loads on 1.9.8: no manifest (legacy install)
- **Where it changes things:** docs: 1; lua identical to vanilla: 0
- **Risk:** none

## 1568 Karnages_Shop_Prices (P3, Economy / merchants)

- **What the author says (Nexus summary):** Total Overhaul of shop costs and sell prices
- **File:** `Karnages_Shop_Prices-1568-1-0-0-1700623554.7z` (archive, 0.0 MB, `c_economy-merchants`), full (scratch, deleted after reading)
- **Grade:** X not analysed | **gameplay perceptibility:** unknown | **visual/audio impact:** none | **layers:** none found | **domain:** none
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `(none)`, loads on 1.9.8: yes (no version restriction)
- **Where it changes things:** manifest: 1; pak (container): 1; lua identical to vanilla: 0
- **Problems:** Karnages_Shop_Prices/Data/Karnages_Shop_Prices.pak: not a ZIP (the game cannot read it either)
- **Risk:** none

## 1683 Roads Are Dangerous - Redux (P3, Quests / lore / content)

- **What the author says (Nexus summary):** This mod aims to mimick what was done with the original mod from 2018 "Roads Are Dangerous" which hasn't been updated in quite a while.Intended modification: Increase the ambush and random combat encounters with Quick Travel and riding from
- **File:** `RAD_redix-1683-0-1-1721003439.zip` (archive, 0.0 MB, `c_quests-lore-content`), full (scratch, deleted after reading)
- **Grade:** X not analysed | **gameplay perceptibility:** unknown | **visual/audio impact:** none | **layers:** none found | **domain:** none
- **How it installs:** Mods/<mod folder> with mod.manifest (Vortex or manual); manifest id `-`, supports `(none)`, loads on 1.9.8: yes (no version restriction)
- **Where it changes things:** manifest: 1; pak (container): 1; lua identical to vanilla: 0
- **Problems:** RAD_redux/Data/RAD_redux.pak: not a ZIP (the game cannot read it either)
- **Risk:** none
