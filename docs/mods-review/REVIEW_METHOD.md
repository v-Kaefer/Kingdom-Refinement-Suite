# How a mod is reviewed and harvested

> **Status date:** 2026-10-05 | **Kind:** review | **Trust:** derived (files read statically) with the engine rules it rests on marked **measured** | **Game version:** 1.9.8

The method the perk review converged on, written down so the next batch follows the same steps.
It replaces "read the mod, form an opinion": every claim here has to come from a file, and the
parts that cannot be read from files are labelled as such.

**The rule that shapes everything:** a mod is not adopted or rejected as a package. It is read
line by line, and only the lines worth having are copied into our own module. A mod with one good
row and a destructive delivery still gives us that row.

## 0. Before anything: a workbench, not the download folder

```
Mods WIP folder/Perks/<area>-workbench/
    _sources/<id>_<name>/      the archive or folder exactly as downloaded, never touched again
    extracted/<id>_<name>/     opened for reading
    extracted/<id>_<name>/_pak/  the inner .pak opened as well
    notes/                     analysis.json, the balance dataset, the page
```

Extraction is done with a reader that **refuses any entry that climbs out of the target folder**.
This is not theoretical: mod 770 ships five `../../../Data/Libs/Tables/rpg/*.tbl` entries that
would overwrite the game's own files. They were blocked and the mod still read fine.

## 1. Inventory every file, by type - not just the tables

The first pass of the perk review read only the table XMLs and **missed things that changed the
conclusion**: mod 1990's two Lua scripts are what actually apply its perk, and mod 1563 ships a
6.4 MB animation database. Count the files by extension first, then decide what to open:

| Extension | What it means for the review |
|---|---|
| `.xml` under `Libs/Tables` | the data patch: the main subject |
| `.lua` | behaviour the tables do not show; read it, it often *is* the mod |
| `.pak` | a ZIP: open it, the tables are usually inside |
| `.tbl` | the old binary table format, normally a redundant copy of the `.xml` |
| `.adb`, `.bspace`, `animations/**` | animation data; whole-file replacements, conflict with every other animation mod |
| `.cfg` | engine config |
| `.txt`, `.md` | readme and changelog: the author's own claims, useful but not evidence |

## 2. The manifest decides whether any of it loads

- effective mod id = `<modid>`, or the lower-cased `<name>` with spaces as underscores (rule 2)
- `<supports>`: if the running version is not listed, the engine disables the mod. No `<supports>`
  block at all means no restriction.
- A mod that bundles several sub-mods has **one manifest per sub-folder**; comparing every file
  against a single derived id produces false positives.

## 3. Per table file, four questions with a yes/no answer

From the measured rules in [`../engine/ptf-rules.md`](../engine/ptf-rules.md):

1. Is it inside `Libs/Tables`? Outside it the file is never loaded.
2. Does the suffix equal the mod id? If not, the engine silently ignores the file (rule 1).
3. Does it have a suffix at all? A file named exactly like a vanilla table **replaces the whole
   table**, overriding every other mod on it and reverting the game's own later changes.
4. Does every row carry every column of the vanilla header? A missing column is blanked, not
   merged (rule 5).

## 4. Compare every row with the unmodified game

Load the vanilla table from `Data/Tables.pak` and classify each row of the patch by its key:
**new**, **changed** (with the before/after of each column), **identical**, and - for whole-table
files only - the vanilla rows that **disappear**. `dropped` is meaningless for a normal patch: a
patch legitimately contains only the rows it touches.

Watch the key columns; getting them wrong turns new rows into "changed" ones
(`perk2perk_exclusivity` is keyed by `first_perk_id`+`second_perk_id`, `perk_buff_override` by
`perk_id`+`source_buff_id`+`target_buff_id`).

## 5. Read effect codes from the game, never from memory

A buff's `params` is a short formula: three letters, an operator, a value (`wat*1.05`). To learn
what the letters mean, **find the vanilla buffs that already use that code** and read their names.
Record for each code: the meaning, whether a bigger number helps or hurts the player, the vanilla
buffs it was read from, and a confidence mark:

- **confirmed** - several vanilla buffs agree (`was` appears in `HC perk Shakes` and
  `perk_drinking_habit`, so it is aim shake)
- **deduced** - one or two uses only; it is a hypothesis and needs a game test before it drives a
  balance decision (`btw` appears in exactly one vanilla buff in the whole game)

Two codes were translated wrongly from memory in the first pass and corrected this way: `wac` is
the attack cost/time, not the hit chance; `mst` is maximum stamina, not draw speed.

### A perk with no buff is not a perk with no effect

**Measured in game** (the project author, 5 Oct 2026, with the Riposte perk un-hidden): the perk
works, and it decides between two techniques by the button pressed in the reaction window - block
gives the Master Strike, attack gives an automatic Riposte.

That perk has **zero rows in `perk_buff`**. Combat-behaviour perks (`Riposte`, `Hunt attack`, the
`ripo_*` family) carry no buff at all: the engine reads the perk id itself in native code. So
"no buff attached" says nothing about whether a perk does something, and must never be used as
evidence that it is inert - a mistake made in the first pass of this review. For that class of
perk the only way to know the effect is a game session.

## 6. Harvest line by line

For each candidate row, record what it changes, what that means in play, and whether it can be
carried over at all. Three outcomes:

- **portable** - the row can be copied into our module as a PTF patch
- **portable with a question** - the row works, but its value is a balance decision
- **not portable** - usually a removal: **PTF can add and overwrite rows, it cannot delete one**,
  so "take this perk away from the NPCs" has no patch form; only replacing the whole table does
  it, with all the cost that carries

## 7. Balance is never discarded in silence

Every change to a row that already exists in the game is a decision for the author, not for the
reviewer. A change that has not been confirmed is **kept visible and not shipped**: in
[`../../tools/build_krs_perks.py`](../../tools/build_krs_perks.py) the `BUFF_RULES` table holds
every one of them with `include=False`, the reason written beside it, so flipping one flag ships
it. Unconfirmed is parked, never dropped.

## 8. Record the decision and move the folder

A reviewed mod leaves `Installed_to_review/` and goes to the mirrored folder in
`Reviewed_Mods/`, with a line in `Reviewed_Mods/_reviewed.csv`: id, name, origin, decision,
reason, and **the verification that supports it** (for example "the six tables are byte-identical
to the other copy, sha256"). A decision without the check behind it is not recorded.

## 9. Report in the shared format

One page per workbench, in Portuguese, published as an Artifact and kept beside the data in
`notes/`: verdict per instance, what each one implements, the before/after of every change in the
same red-struck/green visual, a plain-language column for every effect, and the glossary with the
evidence and the confidence of each code.

## What this method cannot answer

Nothing here involves running the game. It establishes what the files say and what the engine does
with them. Whether a value is fun, balanced or even has the effect its author intends is a
question for `tools/gate.py` and a session in game. Where a conclusion needs that, it is written
as a question, not as a verdict.
