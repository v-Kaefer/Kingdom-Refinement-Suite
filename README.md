[![Kingdom_Refinement_Suite_Logo_Banner](https://github.com/user-attachments/assets/5710c6cd-fd49-4e3f-9f54-78a075a46d69)](https://next.nexusmods.com/profile/vKaleb)

# Kingdom-Refinement-Suite
A curated set of non-intrusive PTF tweaks to polish your journey through Bohemia.


Added:

* EnhancedEyesByGrimsy {Request Permission}

## Changelog

### 2026-10-03 - Test install updated to KCD 1.9.8
The local test install (`Mods WIP folder/KingdomComeDeliverance`) was updated from 1.9.6 (`Build = 404-504czj3`) to match the main install, 1.9.8 (`Build = 404-504czj4`). Only files with actual changes were overwritten (28 files, ~2.3 GB):

* `Bin/Win64`: `KingdomCome.exe`, `WHGame.dll`; new `Bin/Win64Shared/pros.sdk.x64.dll`
* `Data`: `Tables.pak`, `Scripts.pak`, `Scripts_DLC2/3/4.pak`, `Sounds_HD.pak`, `videos-part0.pak`, `pak.cfg`; new `patch/ipl_patch_010903.pak`
* `Localization`: all 13 `*_xml.pak` files
* Root: `system.cfg` (`wh_sys_version`), `whdlversions.txt`

Left untouched: the test install's `user.cfg` (SQL/modding setup), its `Mods/` folder, logs and `logbackups/`, and test-only folders (`Editor`, `Tools`, `Data_reference`, `outputs`). The test install itself is git-ignored, so this entry only documents the update.
