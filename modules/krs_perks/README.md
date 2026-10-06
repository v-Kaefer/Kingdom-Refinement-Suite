# KRS Perks

Part of the Kingdom Refinement Suite. Brings back the Riposte perk and adds 56 perks across eight skill trees.

## What changes
- **56 new perks** in the Defence, Sword, Axe, Mace, Unarmed, Bow, Long Weapon and Fencing trees, plus the Player tab, each with its own buff, name, description and icon. Harvested line by line from Perkaholic; the full list is on the catalogue page and in `NOTES.md`.
- **Riposte** (perk `ec4c5274`) is visible in the perk list and unlocks at **level 10** (vanilla: hidden, level 5; the upstream restore mod used 8). Requires Perfect Block.
- **Master Strike** (perk `61e98757`, the game's hidden longsword riposte) is made visible in the Defence tree. The game's own Master Strike, taught by Captain Bernard, is **not touched** - see `NOTES.md`, which lists what to watch for.
- Two ladders where tier I is the game's own perk, only renamed: **Like a Feather I / II / III** (fall damage 30% / 40% / 55% less) and **Knock Knock I / II / III** (blocking costs the opponent 15% / 20% / 25% more stamina).
- The **Long Weapon** skill is un-hidden, because this module puts 10 perks in it.
- Perk names and descriptions for all 14 game languages (English text is used where the upstream mod had no translation).

Based on "Restore Riposte" by AcSiG (permission granted). Do not enable both mods: they patch the same rows, and the later mod wins.
If you keep both, load krs_perks after Riposte so level 10 applies.

## Install
Vortex: install `krs_perks-<version>.zip`. Manually: copy the `krs_perks` folder into `Mods/` and add `krs_perks` to `Mods/mod_order.txt`.
