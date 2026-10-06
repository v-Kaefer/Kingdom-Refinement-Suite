# krs_perks - open points to check in game

Everything here was established by reading files. None of it has been seen running. The module is
considered **usable for a test session** as of 6 Oct 2026: `tools/check_patch_names.py` reports 0
problems, every row carries the complete vanilla column set, no reference dangles, every UI key
resolves in the module's own localization, and every icon is one the game already uses.

This file is the list of things to look at **while** that test runs, and the decisions that are
deliberately still open.

## 1. Master Strike - two things with almost the same name

The base game's Master Strike is untouched. The three perks `ripo_text_sword`, `ripo_text_axe` and
`ripo_text_mace` ("Master Strike: Sword / Axe / Mace") keep `visibility=1`, no level and no skill
requirement, and are still granted by **training with Captain Bernard**. The module does not write
a single row for them.

What the module does write is `ripo_lsw_01` (`61e98757`), the game's hidden longsword riposte:

| Column | Game | Module |
|---|---|---|
| `visibility` | 0 | 1 |
| `level` | 14 | *(blank)* |
| `skill_selector` | 16 (Sword) | 15 (Defence) |
| `perk_ui_name` | *(none)* | `perk_krs_ripo_text_sword` -> "Master Strike" |
| `icon_id` | *(none)* | `shield_slam` |

So in the perk screen there will be **four** entries reading "Master Strike …": the game's three
from Bernard, plus this one in the Defence tree. Three things to watch:

- **Does it appear at all?** `visibility=1` with no level is the shape the game uses for perks it
  *grants* (the Bernard trio, the hardcore perks). Nothing in the module grants this one, so it may
  simply never show up.
- **If it shows, is it obtainable?** A perk with no level cannot be bought in the tree.
- **If it is obtained, what does it do?** It has no buff and no combo row; like every `ripo_*` perk
  the engine reads the id in native code. The longsword riposte it corresponds to may or may not
  fire from the Defence tree.

This is the only row in the whole module that **blanks** a value the game has, rather than
replacing it. It came from mod 1765 and is kept by the author's decision.

Related and still hidden, not touched by the module: `ripo_short` (shortsword, level 15) and
`ripo_shield_01` (shield, level 10, inside the hidden shield skill).

## 2. Steady Shot I, II, III - may not survive the bow module

`perk_steady_shot_1/2/3` (Bow tree, levels 3 / 6 / 12) reduce aim shake by a flat
`was-0.05`, `was-0.075`, `was-0.1`.

The bow module (`krs_bow`, roadmap phase 4) is a **separate mod meant to be used in the same
collection**, and its whole subject is how spread, draw and stamina behave. Its working idea is to
make spread follow Strength and Agility instead of being a flat subtraction. If that lands, these
three perks either:

- **stop existing here** and move into `krs_bow`, or
- **change a lot**, because a flat `was` offset and a stat-driven spread are two ways of answering
  the same question and will fight each other.

Do not build anything on top of them. Mod 1375, read for the bow workbench, is the precedent: it
uses `was-15` against an `AimSpreadMax` of 15, which is an on/off switch rather than a tuning
value - the opposite of what the bow module wants.

## 3. Serration - a name the game already uses

One of the 56 Perkaholic perks is called **Serration**, which is also the name of a **buyable**
vanilla perk (level 9, Repairing). Two entries with the same name will show in the perk screen.
Kept on purpose for now, by the author's decision; it goes into the renaming pass together with
the other 55 names, their descriptions, their icons and their UI order.

## 4. The two ladders, after the 6 Oct corrections

Both ladders now start on a rung the game already owns, and the module only renames it:

| Ladder | I (the game's) | II | III |
|---|---|---|---|
| Fall damage | `fdm*0.7` = 30% less, shown as **Like a Feather I** | `fdm*0.60` = 40% | `fdm*0.45` = 55% |
| Block cost | `osb*1.15` = 15% more, shown as **Knock Knock I** | `osb*1.2` = 20% | `osb*1.25` = 25% |

The module ships **no buff row** for either tier I, so those values stay exactly as the game has
them. Tiers II and III arrive through `perk_buff_override`, which **replaces** the rung below
instead of stacking with it - worth confirming in game that owning III does not also apply II.

What to read on screen: all three rungs of each ladder should carry the same name with I, II and
III, and the percentage in each description should match the table above.

## 5. Parked balance decisions

Both sit at `include=False` in `tools/build_krs_perks.py`, visible and not shipped:

- `perk_art_admirer_reward` - the mod doubles the charisma reward (`cha+1` -> `cha+2`);
- `perk_against_all_odds` - icon and UI order only.

Also reverted to the game's own value and not shipped: `perk_reading_Cushion`.

## 6. What is shipped that changes the game rather than adding to it

Only two rows, and both are the author's decision:

- `perk_heavy_swing`: `wat*1.03,wac*1.1` -> `wat*1.07,wac*1.1` (the mod wanted `wat*1.2`);
- the skill row that un-hides skill 23, **Long Weapon**. Vanilla has no perk on that skill, but
  this module puts 10 Perkaholic perks there, so the tab is not empty. Mod 1563 would add three
  more combo perks to it; that mod has not been harvested.
