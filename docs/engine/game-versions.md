# Game versions: what differs between 1.9.6 and 1.9.8

> **Status date:** 2026-10-03 | **Kind:** engine | **Trust:** measured (sections 2, 3, 5) and reported (section 4) | **Game version:** 1.9.6 and 1.9.8

## 1. What was run

| Date | Game | Evidence |
|---|---|---|
| 2 Oct 2026 | 1.9.6 (log: `supports game version '1.9.6' explicitly, it will be enabled`) | `../tests/logs/gate_krs_items_tables.log` and the other `gate_*` logs without `1.9.8` in the name |
| 3 Oct 2026 | 1.9.8 (log: `doesn't support game version '1.9.8', it will be disabled`) | `../tests/logs/gate_*1.9.8*.log` |

The 1.9.8 install is the same replica folder, updated by the author. Data files seen there: `Data/Tables.pak`, `Scripts*.pak` and `Localization/*_xml.pak` dated 27 Feb 2026 (the 1.9.7 build), a new `Data/patch/ipl_patch_010903.pak` (275 KB, 9 Mar 2026) that contains only start-menu and EULA UI (`Libs/UI/Menus_Eula.gfx`, `Menus_ProsQr.gfx`, `MM_Eula.xml`, a Deep Silver account QR screen), and `whdlversions.txt` with build `404-504czj4`.

## 2. Manifest `<supports>`: measured behaviour on 1.9.8

The engine reads the `<kcd_version>` lines of `mod.manifest` and decides before loading anything. Run of 3 Oct 2026 (`../tests/logs/gate_manifest_probe_1.9.8_tables.log`), five synthetic mods that differ only in this block, each patching one different `food` row, plus a real third-party mod:

| Manifest | Engine message | Patch applied? |
|---|---|---|
| `1.9.6` only (`krs_probe_blocked`) | `doesn't support game version '1.9.8', it will be disabled` | **no** |
| same mod, line edited to `1.9.8` (`krs_probe_edited`) | `supports game version '1.9.8' explicitly, it will be enabled` | yes (`modified: 1`) |
| `1.9.6`, `1.9.7`, `1.9.8` (`krs_probe_range`) | `explicitly ... enabled` | yes |
| `1.9.x` (`krs_probe_wild`) | `doesn't support game version '1.9.8', it will be disabled` | **no** |
| no `<supports>` block (`krs_probe_none`) | `has no version restrictions in manifest` / `is not limited to any game version, it will be enabled` | yes |
| Restore Riposte (1765, manifest `1.9.6` only), copy with only that line changed to `1.9.8` | `explicitly ... enabled` | yes (`perk__riposte`, `modified: 2`) |

Consequences:

- The check is a **label comparison, not a compatibility test**. Changing the version line is enough for the engine to load and run the mod, with no error in the log. Whether the mod then behaves correctly is a separate question the manifest cannot answer (the Riposte copy was only checked at the table level; its in-game perk screen needs a loaded level).
- A mod with no `<supports>` block is always loaded, so it can also be loaded when it is really incompatible.
- The only wildcard form that matched was `1.9.*` (seen in the log for Persistent Arrows and Volumetric Fog Shadows: `supports game version '1.9.8' by wildcard '1.9.*'`). **`1.9.x` does not match.** The legacy KRS-Items manifest used `1.9.x`, so it would have been disabled on 1.9.8.
- Mods of the author's Vortex list on 1.9.8 (log `../tests/logs/gate_compat_user_mods_1.9.8_tables.log`): **disabled** `Riposte` (1765, `1.9.6` only) and `DrinkSoundEffects`; **enabled** Persistent Arrows and Volumetric Fog Shadows (`1.9.*`) and Cheat, Solid Helmet Visors, Time HD, MGs Stay Clean, 30 FPS Cutscene Fix, More Responsive Targeting, Early Bird NPC (no restriction). `MinimalModTools` and `MoreResponsiveTargeting` report `mod.manifest not found` and still load.
- KRS manifests now list 1.9.6, 1.9.7 and 1.9.8 (`modules/*/mod.manifest`). Vortex does not read this block; the engine does.

## 3. Startup and tests on 1.9.8

- The main-menu event `mm_main/OnStart` is **not sent** on 1.9.8 (the new start screens come first); events seen: `health_stamina`, `sys_startup`, `sys_loadingvideoscreen` (start, end), `sys_startup/OnEnd`. The harness now runs its table stage on `sys_startup/OnEnd` as well. With that, the module gate passes on 1.9.8: 73 of 73 reachable checks, all 8 patch files applied (`../tests/logs/gate_manifest_probe_1.9.8_tables.log`).
- `--mode full` (level tables, perks) needs the Continue button; screen control was not available for that run, so it is untested on 1.9.8. It may also need the new EULA screen accepted, which only the author should do.
- Rules in `ptf-rules.md` that were re-observed on 1.9.8: suffix equals mod id (module patches applied). Not re-measured on 1.9.8: partial rows blanking columns, last mod wins, ZIP-only paks.

## 4. Official changes (reported, not measured)

| Version | Date | Notes as published (summaries; the full official text could not be fetched) |
|---|---|---|
| 1.9.7 | 13 Feb 2026 | PC stability overhaul; fixed infinite loads (bench sleep, siege trebuchet, continue menu), vegetation/model/texture-system crashes, physics deadlocks, memory leaks, language-swap crash; achievements and dice fix; **Quilted Vest transparent arms fixed** (Deep Silver page); text/icon overlap in several languages; Deep Silver account horse caparison; new localizations |
| 1.9.8 | 14 Apr 2026 | Minor: delete key lock-up in menus, items carried over when starting a new game from the pause menu, HD Sounds / HD Voiceover DLC paks not used, HD Sounds banks updated; Microsoft Store DLC offline; a ground-foliage distortion fix is attributed to PS5 by one source |

Sources: [Deep Silver patch 1.9.7](https://www.deepsilver.com/games/kingdom-come-deliverance/kingdom-come-deliverance-patch-197-playstation-5-xbox-series-x-s), [md-eksperiment 1.9.7 notes](https://md-eksperiment.org/en/post/20260214-kingdom-come-deliverance-1-9-7-patch-notes-60-fps-fixes-rewards-breakdown), [twistedvoxel 1.9.7](https://twistedvoxel.com/kingdom-come-deliverance-update-1-9-7/), wiki summary of 1.9.8 via web search. The two pages named by the wiki (fandom, Steam news) could not be read from this environment.
Nothing in these notes mentions modding support, tables, bush collision, shield textures, weapon icons or particles.

## 5. Facts read from the 1.9.8 data

- Current `Tables.pak`, `player_item`: Raven's beak (`e16b0af6...`) has `icon_id` 152 and the spiked warhammer (`488d9792...`) 150; the mod 1693 sets them the other way round, so the mismatch it fixes is still in the data.
- The 26 vegetation models the old bushes mod (591) replaces exist at the same paths in the current `Objects.pak` and are byte-identical in every pak that holds them (`Objects.pak`, up to `ipl_patch_010400.pak`; checked by CRC for all 26), so no patch up to 1.9.8 changed them; their sizes are 3 to 1,598 bytes larger than the mod's copies (consistent with the collision data being present). That is circumstantial: collision itself was not inspected.
