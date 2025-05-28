## Mods Required
* EarlyBirdNPC
* 30FPSCutsceneFixV2
* MGsStayCleanLongerGetDirtyGradually
* Persistentarrows
* 


## Mods Altered
* [Restore Riposte - Permission Granted](https://www.nexusmods.com/kingdomcomedeliverance/mods/1765)
* [Immersive Archery - Permission Granted](https://www.nexusmods.com/kingdomcomedeliverance/mods/1419)





### Changes

* Restore Riposte - Minimum level reequired 8 -> 10.




#### Big thanks to
* KNOX'S LABELLED ITEMS XML
* [benjaminfoo](https://github.com/benjaminfoo/kcd_coding_guide)


## For Scripts
Quick Start: Patching the Lua script
Unpack Data/Scripts.pak with 7-Zip.

Find the Bow script (likely in Scripts/Weapon/).

Copy it into your mod tree:

MyMod/
└─ Data/
   └─ Scripts.pak/         ← treat as a 7-Zip folder
      └─ Weapon/
         └─ Bow.lua

- Edit Bow.lua to inject your strength/agi formula around the existing charge-time calculation.
- Re-zip MyMod/Data/Scripts.pak (rename .zip→.pak).
- Drop it into your Mods/MyMod/Data/Scripts.pak (or pack it into your Nexus ZIP).