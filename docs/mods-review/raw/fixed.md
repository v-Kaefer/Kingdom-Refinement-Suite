# "Fixed" category: mods whose bug may be officially fixed

## Confirmed fixed by an official update

**None.** This list is empty on purpose, not because nothing was fixed.

Confirming a fix needs the game's patch notes, and they could not be read: `store.steampowered.com` and `www.nexusmods.com` are both blocked in this environment, and web search does not return patch-note text. Without them, listing any mod as "fixed" would be a guess.

What the mod pages do show is that the game has moved past 1.9.6: pages reference **1.9.7** (2331, 2040, 2124) and **1.9.8** (2208, 2210, 1009; KCSE 2244 supports only 1.9.8.0). So official patches exist after the version your tested list targets, but their contents are unknown here.

## Candidates to check

Mods in your lists that fix a vanilla defect (as opposed to changing a design choice). For each, the open question is whether the bug still reproduces on a clean, unmodded install of the current game version.

| ID | Mod | Defect it fixes | Last update | Evidence it is still needed | Status |
|---|---|---|---|---|---|
| [591](https://www.nexusmods.com/kingdomcomedeliverance/mods/591) | Bushes - Collision Remover | Invisible collision on bushes and small vegetation | 2018-08 | **Likely still needed:** 2331 (Redux, updated 2026-08) was rebuilt against 1.9.7 to remove the same collision, so the problem seems to exist in 1.9.7 | Unconfirmed |
| [2331](https://www.nexusmods.com/kingdomcomedeliverance/mods/2331) | Bushes Collision Remover Redux | Same as 591, 26 models | 2026-08 | Built for 1.9.7 | Unconfirmed (current) |
| [1323](https://www.nexusmods.com/kingdomcomedeliverance/mods/1323) | Skalitz Shield Fix AWL | Blurry Skalitz Shield from Theresa (A Woman's Lot) | 2022-01 | None | Check patch notes |
| [1577](https://www.nexusmods.com/kingdomcomedeliverance/mods/1577) | Invisible hands FIX (UPDATE) | Forearms invisible with sleeveless clothes (`alphaTest` flag) | 2023-12 | Updated to v3.0 in late 2023, so it was still needed then | Check patch notes |
| [1693](https://www.nexusmods.com/kingdomcomedeliverance/mods/1693) | Ravens beak and Spiked warhammer icon swap | Two weapon icons mismatched | 2024-12 | None | Check patch notes |
| [2066](https://www.nexusmods.com/kingdomcomedeliverance/mods/2066) | Distant Smoke and Fire | Smoke and flames popping in near chimneys, campfires, torches | 2025-08 | None | Check patch notes |
| 1380 | Black Items Fix (your label; page not resolved) | Not known | n/a | None | Resolve the page first |

Fixes bundled inside content mods, not worth checking separately: 1566 (maces invisible when holstered), 796 (a horse item fix), 2243 (a wall/NPC pixelation fix through a config file).

## Not candidates (and why)

| ID | Why not |
|---|---|
| 1883 Better Pickpocket - FIXED | Fixes a bug in another *mod* (Marxis95's original doubled the catch chance), not in the game |
| 1259 Easy Assassination | v1.1 fixed the mod's own `mod.manifest` warning |
| 1327 Weather Overhaul | v1.1 fixed the mod's own missing-interior-shadow bug; the rain-for-days tuning is a design choice |
| 1671, 1951, 1647, 284, 2158, 2171 | Behaviour preferences (angriness, baths, slow motion, stolen status), not defects |
| 591 vs 2331 | Superseded by another mod, which is different from being fixed by the game |

## How to move a candidate to "fixed"

1. Read the patch notes for 1.9.7 and 1.9.8 (Steam news or the Warhorse forum), and the 1.9.6 notes if you also support that version.
2. Reproduce the original bug on a **clean install with no mods** at the current game version, using the mod page's own description of the symptom.
3. If it no longer reproduces, record the patch version and the note line, and move the row to a "Confirmed fixed" table here. If it still reproduces, keep it as a needed fix.

Once the Nexus host is allowed, each page's "Posts" and "Bugs" tabs may mention a game patch making the mod obsolete, which could speed up step 1.