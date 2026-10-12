"""Grade B, batch 1 (food and service prices): second-pass deep dive on 1483, 1639, 2011, 2345 and 1105.

Reads docs/mods-review/grade_b_cells.csv, grade_b_newrows.json and grade_b_scripts.json (made by grade_b_extract.py), the
unmodified game's tables, and writes:
  docs/mods-review/GRADE_B_LOTE1.html      Portuguese page (decision sheet)
  docs/mods-review/grade_b_lote1_food.csv  one row per food item: game value and what each mod sets
Nothing is run and nothing outside docs/ is written.
Run: python tools/build_grade_b_lote1.py
"""
import collections
import csv
import html
import json
import os
import re
import statistics as st
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
R = os.path.join(ROOT, "docs", "mods-review")
sys.path.insert(0, HERE)
import grade_b_extract as gx          # noqa: E402  (Game: vanilla tables and names)
import grade_b_page_style as S        # noqa: E402

CONF = {"c": ("confirmado", "lido nos arquivos, no jogo ou no log"), "d": ("deduzido", "inferido do nome, da ajuda ou do contexto"), "n": ("não verificado", "precisa de teste no jogo")}


def esc(t):
    return html.escape(str(t), quote=False)


def rich(t):
    t = esc(t)
    t = re.sub(r"`([^`]+)`", r"<code>\1</code>", t)
    t = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", t)
    return re.sub(r"\s*\^([cdn])\b", lambda m: f' <span class="cf cf-{m.group(1)}" title="{esc(CONF[m.group(1)][0])}: {esc(CONF[m.group(1)][1])}">{CONF[m.group(1)][0]}</span>', t)


def chip(kind, text):
    return f'<span class="chip {kind}">{esc(text)}</span>'


def num(x, nd=2):
    if x is None:
        return "-"
    if abs(x - round(x)) < 1e-9:
        return str(int(round(x)))
    return f"{x:.{nd}f}".rstrip("0").rstrip(".").replace(".", ",")


def fl(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def table(head, rows, cls="t compact", nums=()):
    th = "".join(f"<th>{esc(h)}</th>" for h in head)
    body = ""
    for r in rows:
        body += "<tr>" + "".join(f'<td class="{"num" if i in nums else ""}">{c if isinstance(c, str) and c.startswith("<") else rich(c)}</td>' for i, c in enumerate(r)) + "</tr>"
    return f'<div class="scroll"><table class="{cls}"><thead><tr>{th}</tr></thead><tbody>{body}</tbody></table></div>'


# ---------------------------------------------------------------- data
G = gx.Game()
VAN = {r["item_id"]: r for r in G.tables["food"]["rows"]}


def name_of(iid):
    return re.sub(r"\s*\[[0-9a-f]{8}\]$", "", G.label(iid))


cells = list(csv.DictReader(open(os.path.join(R, "grade_b_cells.csv"), encoding="utf-8")))


def mod_key(r):
    if r["id"] != "1483":
        return r["id"]
    return "1483_" + r["container"].split("/")[0].split("_")[-1]


# per item: {mod: {col: new}}
CH = collections.defaultdict(lambda: collections.defaultdict(dict))
for r in cells:
    if r["table"] == "food" and r["kind"] == "changed":
        CH[r["key_raw"]][mod_key(r)][r["column"]] = r["new"]

ITEMS = sorted(VAN, key=lambda i: name_of(i).lower())
# names of the game's own `food_type` table (fruit, meat, drink, bowel, vegetable, mushroom, pastry, dairy), in Portuguese
TYPE = {"2": "Carne (meat)", "3": "Bebida e poção (drink)", "5": "Miúdos (bowel)", "6": "Verdura (vegetable)", "7": "Cogumelo (mushroom)", "8": "Pão e massa (pastry)", "9": "Laticínio e ovo (dairy)", "0": "Fruta (fruit)", "": "Sem tipo"}


def value(iid, mod, col):
    """the value this mod leaves in the cell (vanilla when the mod does not change it)"""
    ch = CH.get(iid, {}).get(mod, {})
    if col in ch:
        return ch[col]
    return VAN[iid][col]


def v(iid, mod, col):
    return fl(value(iid, mod, col))


# decay: the perishable set of 1483
PER = [i for i in ITEMS if "decay_time_hours" in CH.get(i, {}).get("1483_2X", {})]
assert len(PER) == 111, len(PER)

# ---------------------------------------------------------------- csv
with open(os.path.join(R, "grade_b_lote1_food.csv"), "w", encoding="utf-8", newline="") as f:
    w = csv.writer(f, lineterminator="\n")
    w.writerow(["item", "item_id", "food_type_id", "food_subtype_id",
                "decay_game", "decay_1483_2x", "decay_1483_3x", "decay_1483_5x", "decay_1639", "decay_2011", "decay_2345", "decay_2179",
                "nutrition_game", "nutrition_2011", "nutrition_2345", "nutrition_2179",
                "refresh_game", "refresh_2011", "refresh_2345", "refresh_2179",
                "health_game", "health_2011", "health_2345", "health_2179", "other_2011_changes"])
    for i in ITEMS:
        if i not in CH:
            continue
        o = CH[i].get("2011", {})
        other = ";".join(f"{c}={o[c]}" for c in o if c not in ("decay_time_hours", "nutrition_benefit", "refresh_benefit", "health_benefit"))

        def cell(mod, col):
            ch = CH[i].get(mod, {})
            return ch[col] if col in ch else ""
        w.writerow([name_of(i), i, VAN[i]["food_type_id"], VAN[i]["food_subtype_id"],
                    VAN[i]["decay_time_hours"]] + [cell(m, "decay_time_hours") for m in ("1483_2X", "1483_3X", "1483_5X", "1639", "2011", "2345", "2179")] +
                   [VAN[i]["nutrition_benefit"]] + [cell(m, "nutrition_benefit") for m in ("2011", "2345", "2179")] +
                   [VAN[i]["refresh_benefit"]] + [cell(m, "refresh_benefit") for m in ("2011", "2345", "2179")] +
                   [VAN[i]["health_benefit"]] + [cell(m, "health_benefit") for m in ("2011", "2345", "2179")] + [other])

# ---------------------------------------------------------------- 1. decay
decay_groups = collections.OrderedDict()
for i in PER:
    decay_groups.setdefault(fl(VAN[i]["decay_time_hours"]), []).append(i)


def dist(vals):
    c = collections.Counter(vals)
    return "; ".join(f"{num(k)} h x{n}" if n > 1 else f"{num(k)} h" for k, n in sorted(c.items(), key=lambda kv: (kv[0] is None, kv[0])))


rows = []
for g0, its in sorted(decay_groups.items()):
    a2011 = [v(i, "2011", "decay_time_hours") if "decay_time_hours" in CH[i].get("2011", {}) else None for i in its]
    a2345 = [v(i, "2345", "decay_time_hours") if "decay_time_hours" in CH[i].get("2345", {}) else None for i in its]
    a1639 = [v(i, "1639", "decay_time_hours") for i in its]
    n2011 = sum(x is not None for x in a2011)
    n2345 = sum(x is not None for x in a2345)
    rows.append([f"{num(g0)} h ({num(g0 / 24, 1)} {'dia' if g0 == 24 else 'dias'})", str(len(its)),
                 f"{num(g0 * 2)} / {num(g0 * 3)} / {num(g0 * 5)} h",
                 f"{num(g0 * 2)} h, mas {sum(1 for x in a1639 if x != g0 * 2)} item com erro" if any(x != g0 * 2 for x in a1639) else f"{num(g0 * 2)} h",
                 (f"{n2011} de {len(its)}: " + dist([x for x in a2011 if x is not None])) if n2011 else "não muda",
                 (f"{n2345} de {len(its)}: " + dist([x for x in a2345 if x is not None])) if n2345 else "não muda"])
decay_group_table = table(["Valor do jogo", "Itens", "1483 (2X / 3X / 5X)", "1639", "2011", "2345"], rows, nums=(1,))

z2011 = [name_of(i) for i in ITEMS if i in CH and "decay_time_hours" in CH[i].get("2011", {}) and v(i, "2011", "decay_time_hours") == 0 and fl(VAN[i]["decay_time_hours"]) not in (0, None)]
newdec2011 = [(name_of(i), fl(VAN[i]["decay_time_hours"]), v(i, "2011", "decay_time_hours")) for i in ITEMS if i in CH and CH[i].get("2011", {}).get("decay_time_hours") not in (None, "") and i not in PER]
typo_rows = [name_of(i) for i in ITEMS if i in CH and CH[i].get("2011", {}).get("decay_time_hours") == ""]
below = [(name_of(i), fl(VAN[i]["decay_time_hours"]), v(i, "2011", "decay_time_hours")) for i in ITEMS if i in CH and CH[i].get("2011", {}).get("decay_time_hours") not in (None, "") and 0 < v(i, "2011", "decay_time_hours") < fl(VAN[i]["decay_time_hours"])]
both = [i for i in ITEMS if "decay_time_hours" in CH.get(i, {}).get("2011", {}) and "decay_time_hours" in CH.get(i, {}).get("2345", {})]
both_eq = sum(1 for i in both if CH[i]["2011"]["decay_time_hours"] == CH[i]["2345"]["decay_time_hours"])
x2011 = [i for i in PER if CH[i].get("2011", {}).get("decay_time_hours") not in (None, "")]
x2011_low = sum(1 for i in x2011 if v(i, "2011", "decay_time_hours") < v(i, "1483_2X", "decay_time_hours"))
x2345 = [i for i in PER if "decay_time_hours" in CH[i].get("2345", {})]
x2345_low = sum(1 for i in x2345 if v(i, "2345", "decay_time_hours") < v(i, "1483_2X", "decay_time_hours"))

sel = ["Beef_cooked", "Rabbit meat cooked", "hardboiled_egg", "carrot cooked", "Smoked Rabbit meat", "Smoked Cheese quarter", "herring", "Dead Chicken", "Beef", "Watermelon", "Lepiota cooked", "Bread", "Apple", "Smoked Salami_01"]
byname = {name_of(i): i for i in ITEMS}
rows = []
for n in sel:
    i = byname.get(n)
    if not i:
        continue
    gm = fl(VAN[i]["decay_time_hours"])
    row = [n, num(gm)]
    row += [num(gm * 2) if i in PER else "-", num(gm * 3) if i in PER else "-", num(gm * 5) if i in PER else "-"]
    row.append(num(v(i, "1639", "decay_time_hours")) if i in PER else "-")
    row.append(num(v(i, "2011", "decay_time_hours")) if "decay_time_hours" in CH[i].get("2011", {}) else "igual")
    row.append(num(v(i, "2345", "decay_time_hours")) if "decay_time_hours" in CH[i].get("2345", {}) else "igual")
    rows.append(row)
decay_examples = table(["Item", "Jogo (h)", "1483 2X", "3X", "5X", "1639", "2011", "2345"], rows, nums=(1, 2, 3, 4, 5, 6, 7))

# fine tuning: the 111 perishables grouped by (game value, type of food)
CLASS_NAME = {
    ("24", "2"): "Carne e peixe crus", ("24", "5"): "Miúdos crus", ("24", "7"): "Cogumelos crus", ("24", "3"): "Leite",
    ("48", "2"): "Carne e peixe cozidos", ("48", "5"): "Miúdos cozidos e sopas", ("48", "6"): "Verduras cozidas", ("48", "7"): "Cogumelos cozidos",
    ("48", "0"): "Frutas cozidas", ("48", "9"): "Ovos e creme", ("48", ""): "Mingaus, lanche e ovos de Páscoa",
    ("72", "2"): "Bacon e torresmo", ("72", "0"): "Melancia", ("72", "5"): "Miúdos (droby)",
    ("96", "8"): "Pães e bolinhos", ("96", "6"): "Verduras cruas e raízes",
    ("120", "2"): "Carne defumada e curada", ("120", "0"): "Frutas (maçã, pera)", ("120", "9"): "Queijo", ("120", "5"): "Banha de cão", ("120", ""): "Queijo defumado", ("120", "6"): "Beterraba crua",
}
cls = collections.OrderedDict()
for i in PER:
    key = (str(int(fl(VAN[i]["decay_time_hours"]))), VAN[i]["food_type_id"])
    cls.setdefault(key, []).append(i)
tune_rows = []
for key in sorted(cls, key=lambda k: (int(k[0]), CLASS_NAME.get(k, k[1]))):
    its = cls[key]
    g0 = fl(key[0])

    def med(mod):
        xs = [v(i, mod, "decay_time_hours") for i in its if CH[i].get(mod, {}).get("decay_time_hours") not in (None, "")]
        return (num(st.median(xs)) + f" h ({len(xs)}/{len(its)})") if xs else "não muda"
    tune_rows.append([CLASS_NAME.get(key, f"tipo {key[1]}"), str(len(its)), num(g0), num(g0 * 2), num(g0 * 3), med("2011"), med("2345"), "?"])
tune_table = table(["Classe (tipo do jogo + valor)", "Itens", "Jogo (h)", "2X", "3X", "2011 (mediana, itens)", "2345 (mediana, itens)", "Seu valor"], tune_rows, nums=(1, 2, 3, 4))
with open(os.path.join(R, "grade_b_lote1_spoilage_classes.csv"), "w", encoding="utf-8", newline="") as f:
    w = csv.writer(f, lineterminator="\n")
    w.writerow(["class", "game_decay_h", "food_type_id", "items", "item_names", "chosen_h"])
    for key in sorted(cls, key=lambda k: (int(k[0]), CLASS_NAME.get(k, k[1]))):
        w.writerow([CLASS_NAME.get(key, key[1]), key[0], key[1], len(cls[key]), "; ".join(name_of(i) for i in cls[key]), ""])

# full decay table (all 119 touched)
full = []
for i in ITEMS:
    if i not in CH or not any("decay_time_hours" in CH[i].get(m, {}) for m in ("1483_2X", "1639", "2011", "2345", "2179")):
        continue
    gm = fl(VAN[i]["decay_time_hours"])

    def c(m):
        ch = CH[i].get(m, {})
        return num(fl(ch["decay_time_hours"])) if "decay_time_hours" in ch else "-"
    full.append([name_of(i), TYPE.get(VAN[i]["food_type_id"], VAN[i]["food_type_id"]), num(gm), c("1483_2X"), c("1483_3X"), c("1483_5X"), c("1639"), c("2011"), c("2345"), c("2179")])
decay_full = table(["Item", "Tipo (inferido)", "Jogo", "1483 2X", "3X", "5X", "1639", "2011", "2345", "2179"], full, nums=(2, 3, 4, 5, 6, 7, 8, 9))

# ---------------------------------------------------------------- 2. nutrition / refresh / health
def ratios(mod, col):
    out = []
    for i in ITEMS:
        if col in CH.get(i, {}).get(mod, {}):
            g = fl(VAN[i][col])
            n = fl(CH[i][mod][col])
            if g not in (None, 0) and n is not None:
                out.append(n / g)
    return out


stats_rows = []
for col, lab in (("nutrition_benefit", "nutrição"), ("refresh_benefit", "refresco"), ("health_benefit", "saúde")):
    for mod in ("2011", "2345"):
        ch = [i for i in ITEMS if col in CH.get(i, {}).get(mod, {})]
        rr = ratios(mod, col)
        up = sum(1 for i in ch if fl(CH[i][mod][col]) is not None and fl(CH[i][mod][col]) > (fl(VAN[i][col]) or 0))
        dn = sum(1 for i in ch if fl(CH[i][mod][col]) is not None and fl(CH[i][mod][col]) < (fl(VAN[i][col]) or 0))
        diffs = [fl(CH[i][mod][col]) - (fl(VAN[i][col]) or 0) for i in ch if fl(CH[i][mod][col]) is not None]
        rr = [fl(CH[i][mod][col]) / fl(VAN[i][col]) for i in ch if fl(VAN[i][col]) and fl(VAN[i][col]) > 0 and fl(CH[i][mod][col]) is not None]
        stats_rows.append([lab, mod, str(len(ch)), str(up), str(dn), ("+" if st.median(diffs) > 0 else "") + num(st.median(diffs)), (num(st.median(rr)) + "x (" + str(len(rr)) + " itens)") if rr and col == "nutrition_benefit" else "-"])
nut_stats = table(["Coluna", "Mod", "Itens mudados", "Sobe", "Desce", "Mediana da diferença (novo − jogo)", "Mediana novo/jogo (só nutrição, onde o jogo é positivo)"], stats_rows, nums=(2, 3, 4, 5))

# agreement between 2011 and 2345 on shared items
shared = [i for i in ITEMS if i in CH and "2011" in CH[i] and "2345" in CH[i]]
agree = collections.Counter()
for i in shared:
    for col in ("nutrition_benefit", "refresh_benefit"):
        a = CH[i]["2011"].get(col)
        b = CH[i]["2345"].get(col)
        if a is None or b is None:
            continue
        g = fl(VAN[i][col])
        da, db = fl(a) - g, fl(b) - g
        agree[(col, "igual" if fl(a) == fl(b) else "mesma direção" if da * db > 0 else "direções opostas")] += 1
agree_rows = [[c.replace("_benefit", ""), k, str(n)] for (c, k), n in sorted(agree.items())]
agree_table = table(["Coluna", "Os dois mods no mesmo item", "Itens"], agree_rows, nums=(2,))

# by type
trows = []
for tid, tn in TYPE.items():
    its = [i for i in ITEMS if VAN[i]["food_type_id"] == tid]
    if not its:
        continue
    def med(mod, col):
        if col == "refresh_benefit":
            dd = [fl(CH[i][mod][col]) - (fl(VAN[i][col]) or 0) for i in its if col in CH.get(i, {}).get(mod, {}) and fl(CH[i][mod][col]) is not None]
            return (("+" if st.median(dd) > 0 else "") + num(st.median(dd))) if dd else "-"
        rr = [fl(CH[i][mod][col]) / fl(VAN[i][col]) for i in its if col in CH.get(i, {}).get(mod, {}) and fl(VAN[i][col]) and fl(VAN[i][col]) > 0 and fl(CH[i][mod][col]) is not None]
        return (num(st.median(rr)) + "x") if rr else "-"
    gn = [fl(VAN[i]["nutrition_benefit"]) for i in its if fl(VAN[i]["nutrition_benefit"]) is not None] or [0]
    trows.append([tn, str(len(its)), num(st.median(gn)), med("2011", "nutrition_benefit"), med("2345", "nutrition_benefit"), med("2011", "refresh_benefit"), med("2345", "refresh_benefit")])
type_table = table(["Tipo do jogo", "Itens", "Nutrição mediana do jogo", "2011 nutrição", "2345 nutrição", "2011 refresco (mediana da diferença)", "2345 refresco (idem)"], trows, nums=(1, 2, 3, 4, 5, 6))

# the biggest disagreements
dis = []
for i in shared:
    a = CH[i]["2011"].get("nutrition_benefit")
    b = CH[i]["2345"].get("nutrition_benefit")
    if a is not None and b is not None:
        dis.append((abs(fl(a) - fl(b)), i, a, b))
dis.sort(reverse=True)
dis_rows = [[name_of(i), TYPE.get(VAN[i]["food_type_id"], "-"), VAN[i]["nutrition_benefit"], a, b] for _, i, a, b in dis[:18]]
dis_table = table(["Item", "Tipo", "Nutrição no jogo", "2011", "2345"], dis_rows, nums=(2, 3, 4))

# representative items with hunger arithmetic
DIG_V = 0.000578704 * 86400
DIG_K = 0.001302 * 86400
rep = ["Bread", "Beef_cooked", "Rabbit meat cooked", "Smoked Rabbit meat", "carrot cooked", "Apple", "hardboiled_egg", "cheese", "Cheese quarter", "lentil_soup", "Salami_01"]
rows = []
for n in rep:
    i = byname.get(n)
    if not i:
        continue
    gn = fl(VAN[i]["nutrition_benefit"])
    n11 = v(i, "2011", "nutrition_benefit")
    n45 = v(i, "2345", "nutrition_benefit")
    h = lambda x, d: num(x / d * 24, 1)
    rows.append([n, num(gn), h(gn, DIG_V), h(n11, DIG_V), h(n45, DIG_V), h(gn, DIG_K), h(n11, DIG_K), h(n45, DIG_K)])
hunger_table = table(["Item", "Nutrição do jogo", "Jogo: horas de fome", "2011", "2345", "Com KRS Items: jogo", "2011", "2345"], rows, nums=(1, 2, 3, 4, 5, 6, 7))

# health added by 2011
hl = [(name_of(i), fl(VAN[i]["health_benefit"]), v(i, "2011", "health_benefit")) for i in ITEMS if "health_benefit" in CH.get(i, {}).get("2011", {})]
hl_vals = [b for _, a, b in hl]
QUEST = {"charl_horndust", "OintmentForMarta", "Mrchojedy Cure", "Mrchojedy Potion", "crystal meth", "Generic potion", "Test Potion: Invincible", "Abortion potion"}
hl_big = sorted([x for x in hl if x[0] not in QUEST], key=lambda x: -(x[2] or 0))[:8]
hl_table = table(["Item", "Saúde no jogo", "Saúde no 2011"], [[a, num(b), num(c)] for a, b, c in hl_big], nums=(1, 2))

# type changes by 2011
tc = []
for i in ITEMS:
    o = CH.get(i, {}).get("2011", {})
    if "food_type_id" in o or "food_subtype_id" in o:
        tc.append([name_of(i), f'{VAN[i]["food_type_id"] or "-"} / {VAN[i]["food_subtype_id"] or "-"}', f'{o.get("food_type_id", VAN[i]["food_type_id"]) or "-"} / {o.get("food_subtype_id", VAN[i]["food_subtype_id"]) or "-"}'])
tc_table = table(["Item", "Tipo / subtipo no jogo", "No 2011"], tc)

# ---------------------------------------------------------------- 3. test / quest items touched by 2011
OUT = ["Generic potion", "crystal meth", "charl_horndust", "OintmentForMarta", "Test Potion: Invincible", "Abortion potion", "Mrchojedy Cure", "Diarrhoea potion", "Dementia potion", "q_auschitz_alcohol"]
out_rows = []
for n in OUT:
    i = byname.get(n)
    if not i:
        continue
    o = CH.get(i, {}).get("2011", {})
    chg = ", ".join(f"`{c}` {VAN[i][c] or '-'} → {o[c] or '-'}" for c in o if c in ("nutrition_benefit", "refresh_benefit", "health_benefit", "decay_time_hours", "alcohol_content", "max_status"))
    if chg:
        out_rows.append([n, chg])
out_table = table(["Item de teste ou de missão", "Mudança do 2011 em `food`"], out_rows)

# ---------------------------------------------------------------- 4. snack system
newrows = json.load(open(os.path.join(R, "grade_b_newrows.json"), encoding="utf-8"))
nr = [r for r in newrows if r["id"] == "2011"]
bclass = {r["row"]["buff_class_id"]: r["row"]["buff_class_name"] for r in nr if r["table"] == "buff_class"}
buffs = [r["row"] for r in nr if r["table"] == "buff"]
by_class = collections.Counter(bclass.get(b["buff_class_id"], "classe " + b["buff_class_id"]) for b in buffs)
links = {r["row"]["buff_id"]: r["row"]["item_id"] for r in nr if r["table"] == "consumable_item"}
cons_changed = {r["key_raw"]: (r["old"], r["new"]) for r in cells if r["id"] == "2011" and r["table"] == "consumable_item" and r["kind"] == "changed"}
CODES = {"mst": "vigor máximo", "srg": "regeneração de vigor", "cap": "capacidade de carga", "mhe": "vida máxima", "health": "vida", "poi": "veneno"}
dur = [fl(b["duration"]) for b in buffs if fl(b["duration"]) is not None and b["buff_class_id"] in bclass]
snack_class_rows = [[k, str(by_class.get(k, 0))] for k in bclass.values()] + [[k, str(n)] for k, n in by_class.items() if k not in bclass.values()]
snack_class_table = table(["Classe de buff", "Buffs"], snack_class_rows, nums=(1,)) + '<p class="note">"classe 7" é uma classe que já existe no jogo: o buff `doomsday_poison`, ligado ao item de teste "Generic potion", que o 2011 transforma em veneno (`poi=1,health-175/t`). ^c</p>'
snack_dur = f"{num(min(dur))} a {num(max(dur))} s, mediana {num(st.median(dur))} s"
param_ex = collections.Counter(re.sub(r"[-+*/]?[0-9.]+(/t)?$", "", p.split(",")[0]) for p in (b["params"] for b in buffs))

# ---------------------------------------------------------------- 5. service prices (1105)
svc = json.load(open(os.path.join(R, "grade_b_scripts.json"), encoding="utf-8"))
svc1105 = [r for r in svc if r["id"] == "1105"]

# ---------------------------------------------------------------- page
FINDINGS = [
    ("Apodrecimento: o 1483 cobre tudo; os outros três divergem dele e entre si",
     f"O 1483 multiplica por 2, 3 ou 5 o apodrecimento das 111 comidas que estragam (91 de 202 nunca estragam). O 1639 repete o 2X, com um erro (frango morto 24 → 2400 h) e id inválido. O 2011 e o 2345 escolhem valores por item: ficam **abaixo do 2X** em quase todo item ({x2011_low} de {len(x2011)} e {x2345_low} de {len(x2345)}) e dão o mesmo valor entre si em só {both_eq} de {len(both)}. ^c"),
    ("Nutrição: os dois baixam a comida, mas o 2011 também sobe refresco e cura",
     "Em nutrição os dois baixam a mediana em 3 pontos (2011: 96 itens descem, 70 sobem; 2345: 121 descem, 18 sobem). Nos 123 itens que os dois tocam, 82 vão no mesmo sentido e 37 em sentidos opostos (20 deles carnes: o 2011 sobe a nutrição das defumadas e secas, o 2345 as baixa). Nas poções o sentido é o mesmo, mas a escala difere muito (2011 de -10 a -30; 2345 em 2,5). O 2011 vai bem além: refresco sobe em 155 de 168 itens (mediana +9) e a saúde passa de 0 a positiva em 127 comidas; o 2345 pouco mexe no refresco (mediana +1) e na saúde só em 5 itens. ^c"),
    ("O KRS Items já acelera a fome em 2,25 vezes",
     "`DigestionSpeed` 0,000579 → 0,001302 (mais ou menos 50 → 112 unidades por dia de jogo). Se também se aplicasse o 2345 (carne cozida de 21 para 5 de nutrição), essa refeição, que no jogo segura cerca de 10 horas de fome, passaria a cerca de 1 hora com o KRS Items (tabela na seção de nutrição). Isso é um acúmulo de efeitos, e é preciso decidir de propósito. ^d"),
    ("Os termos do 2011 proíbem uso em coleção",
     "O arquivo `terms of endearment.txt` permite modificação pública com crédito, mas veda 'used in ANY mod collection'. A Kingdom Refinement Suite é uma coleção: **copiar bytes ou linhas do 2011 está fora**. Só ideias, com números próprios, ou requisito externo. ^c (texto) / ^d (aplicação à suite)"),
    ("O 1105 não é um patch de tabela",
     "Só o preço do banho está numa tabela (6 linhas de `sequence`); quarto, treinador e cavalo estão em 3 scripts do jogo substituídos inteiros. Aproveitar os números exige decidir como (script próprio ou parâmetro). ^c"),
    ("Arrumação feita agora",
     "85, 770 e 1009 foram movidos para `Mods WIP folder/Perks`; o 770 foi para `Perks/_quarantine` porque o motivo da quarentena (caminho com `../..` dentro do pak) continua valendo. ^c"),
]

OPTS_DECAY = [
    ("A. 1483 2X, como o autor recomenda", "Todos os 111 perecíveis x2; cozidos 48 → 96 h (4 dias), defumados 120 → 240 h (10 dias). Um único multiplicador, fácil de explicar e de reverter."),
    ("B. 1483 3X", "Cozidos 6 dias, defumados 15 dias. O próprio autor do 1483 achou 3X irreal e excessivo."),
    ("C. Valores por item (2011 ou 2345)", "Exige escolher um dos dois por item (eles discordam) e decidir sobre os zeros do 2011. Dá mais trabalho e mais chance de erro."),
    ("D. 2X com ajustes pontuais", "2X como base e corrigir à mão só o que o jogo pedir (ex.: algum item de quest). Mantém a simplicidade e deixa a porta aberta."),
]
OPTS_NUT = [
    ("A. Não mexer na nutrição", "O KRS já deixa a fome mais exigente; deixar os valores do jogo evita acumular. Só a poção de Aesop (já no KRS Items)."),
    ("B. Só poções e venenos mais claros", "Por exemplo: Poison com nutrição e refresco -20 (jogo -10 e -10) e Witch potion com refresco -10 (jogo +8), como no 2345; deixa a comida comum intocada. O 2011 vai bem mais longe (Sleeping potion -30, Witch potion -20), o que não combina com o princípio 'poções, toque leve'."),
    ("C. Reescala própria, uniforme", "Um multiplicador nosso (por exemplo x0,8) em nutrição e refresco, com a digestão revista junto. É a única forma coerente de baixar nutrição sem dobrar o efeito."),
    ("D. Adotar o 2345 inteiro, como patch com sufixo", "Reempacotar as 155 linhas do 2345. É a mudança mais forte; exige rever `DigestionSpeed` do KRS Items."),
]
OPTS_SNACK = [
    ("A. Deixar de fora por enquanto", "Sistema grande (42 buffs, 9 classes, 38 itens e 94 textos), com termos que impedem copiar. Avaliar depois, com outro módulo."),
    ("B. Reimplementar uma versão pequena", "Poucas ideias (ex.: ovo → furtividade, cebola → regeneração de vigor) com números e textos próprios. Dá trabalho de interface e de localização."),
    ("C. Requisito externo", "Indicar o Chefs Kiss como mod recomendado, sem copiar nada. Mas ele reescreve 180 linhas de `food` e conflita com o que decidirmos nos outros três itens."),
]

SVC = [
    ["Banho, 6 serviços (sequence)", "10 / 20 / 30 / 40 / 20 / 15", "100 / 200 / 300 / 500 / 250 / 250", "tabela `sequence` (patchável)"],
    ["Quarto temporário (diária)", "20 em todas as cidades", "200 a 500 por cidade (Ledetchko 300, Mytinka 500, Rataje/Sasau 400, Talmberg/Uzice 200)", "script `Sleepover.lua`"],
    ["Quarto permanente", "2000 a 2500", "2000 a 6500 (Mytinka 6500)", "script `Sleepover.lua`"],
    ["Treinador, 1º nível", "600", "300 a 500 conforme a habilidade", "script `Trainers.lua`"],
    ["Treinador, 2º / 3º / 4º nível", "1800 / 5400 / 16200", "1250-1750 / 4500-7500 / 15000-25000", "script `Trainers.lua`"],
    ["Cavalo", "interpolação entre mínimo e máximo, com piso `HorseMinFinalPrice`", "soma² x 6 + 2500, sem piso", "script `Horsetraders.lua`"],
]


def sec(i, title, lead, body):
    return f'<h2 id="{i}">{esc(title)}</h2><p class="lead">{rich(lead)}</p>{body}'


def options(opts):
    return '<div class="cols">' + "".join(f'<div class="find"><h3>{esc(t)}</h3><p>{rich(d)}</p></div>' for t, d in opts) + "</div>"


def details(title, body):
    return f"<details><summary>{esc(title)}</summary>{body}</details>"


fhtml = "".join(f'<div class="find"><h3>{esc(t)}</h3><p>{rich(d)}</p></div>' for t, d in FINDINGS)
nav = "".join(f'<a href="#{i}">{t}</a>' for i, t in (("resumo", "Resumo"), ("mapa", "Os cinco mods"), ("apodrecimento", "Apodrecimento"), ("nutricao", "Nutrição"), ("lanches", "Lanches"), ("servicos", "Serviços"), ("decisoes", "Decisões"), ("metodo", "Método")))

mapa = table(["Mod", "Arquivos que mexem", "Linhas / células", "Lido"], [
    ["1483 Slower Food Spoil", "3 pastas (2X, 3X, 5X), cada uma com `food__slowerfoodspoil.xml`", "111 linhas de `food`, 1 coluna (`decay_time_hours`); 333 células", "tudo"],
    ["1639 Alternate Food Spoil 2X", "`food__AlternateFoodSpoil2X.xml` e `food.tbl` de 0 byte", "202 linhas, 111 mudam, 1 coluna; Dead Chicken com erro", "tudo"],
    ["2011 Chefs Kiss 3.7", "7 patches de tabela, textos (94 trocados, 44 novos), termos de uso", f"`food` 180 linhas; `buff` +{len(buffs)}; `buff_class` +{len(bclass)}; `consumable_item` +5 e 38 alteradas; `pickable_item` 44; `item` 4; `potion` 1", "tudo"],
    ["2345 Jesoo333 Food and Drinks", "`Libs/Tables/item/food.xml` (tabela inteira, sem sufixo) e `food.tbl` vazio", "202 linhas; 155 mudam; nutrição 139, refresco 98, saúde 5, apodrecimento 24", "tudo"],
    ["1105 Service Prices", "`sequence__service_prices.xml`, 3 scripts do jogo substituídos", "6 linhas de `sequence`; 521 + 263 + 238 linhas de Lua", "tudo"],
], nums=())

page = f"""<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Grau B, lote 1: comida e serviços</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=IBM+Plex+Sans+Condensed:wght@500;600&family=IBM+Plex+Sans:wght@400;500;600&display=swap">
<style>{S.CSS}
details>summary{{cursor:pointer;font-weight:600;margin:10px 0;color:var(--accent)}}
</style>
<div class="top"><b>Grau B, lote 1</b><nav>{nav}</nav></div>
<main>
<header>
<h1>Comida e serviços: 1483, 1639, 2011, 2345 e 1105</h1>
<p class="lead">Segunda passada, só leitura. Compara os cinco mods item por item, mostra o que se acumularia com o KRS Items e coloca as decisões que são suas. Nada foi construído, nenhum mod foi executado e nada foi movido para `Reviewed_Mods`.</p>
<p class="legend"><span><span class="cf cf-c">confirmado</span> lido nos arquivos</span><span><span class="cf cf-d">deduzido</span> inferido</span><span><span class="cf cf-n">não verificado</span> precisa de teste</span></p>
</header>

<h2 id="resumo">Resumo</h2>
<div class="cols">{fhtml}</div>

<h2 id="mapa">Os cinco mods</h2>
{mapa}

{sec("apodrecimento", "Apodrecimento: quanto a comida dura", "`decay_time_hours` é em horas de jogo; 0 significa que não estraga. Os quatro mods mexem na mesma coluna das mesmas linhas, então só um valor por linha pode valer (o último mod na ordem leva a linha inteira). ^c",
     "<h3>Por grupo de valor do jogo</h3>" + decay_group_table +
     "<h3>Itens de exemplo</h3>" + decay_examples +
     f'<p class="note">O 2011 põe **0** ("não estraga") em {len(z2011)} itens que estragam no jogo: {esc(", ".join(z2011))}. Quase todos são carne crua ou banha; só dá para saber se faz sentido (carne crua nunca apodrecer) testando no jogo. ^n</p>'.replace("**", "") +
     f'<p class="note">Itens fora dos 111 que o 2011 também mexe: {esc("; ".join(f"{a} {num(b)} → {num(c)} h" for a, b, c in newdec2011)) or "nenhum"}. A linha com o erro de digitação `decay_ime_hours` deixa o apodrecimento em branco: {esc(", ".join(typo_rows)) or "não localizada"} (item de teste). ^c</p>'
     f'<p class="note">Comparação com o 2X: o 2011 fica abaixo do 2X em {x2011_low} de {len(x2011)} itens e abaixo do próprio jogo em {len(below)} ({esc("; ".join(f"{a} {num(b)} → {num(c)} h" for a, b, c in below))}); o 2345 fica abaixo do 2X em {x2345_low} de {len(x2345)} itens. Entre si, o 2011 e o 2345 dão o mesmo valor em {both_eq} de {len(both)} itens. ^c</p>' +
     "<h3>Ajuste fino: por classe de alimento</h3>"
     '<p class="note">Rascunho para o ajuste fino. Nada foi escolhido nem consolidado: a coluna "Seu valor" está vazia de propósito. Cada classe pode receber um valor em horas (ou um multiplicador). Os itens de cada classe estão em `grade_b_lote1_spoilage_classes.csv`. ^d</p>' + tune_table +
     details("Os 119 itens de apodrecimento, um a um (inclui os que só o 2011 ou o 2179 mexem)", decay_full) +
     "<h3>Opções</h3>" + options(OPTS_DECAY) +
     '<p class="note">Como o jogo escolhe uma linha inteira por mod, qualquer coisa nossa em `food` (apodrecimento, nutrição, a poção de Aesop) precisa ficar no <b>mesmo arquivo</b> do módulo Items, com as colunas já combinadas. Dois arquivos de `food` no suite se sobrescreveriam.</p>')}

{sec("nutricao", "Nutrição, refresco e saúde", "`nutrition_benefit` é quanto a fome sobe ao comer, `refresh_benefit` o refresco (negativo = desidrata) e `health_benefit` a cura. O 2011 e o 2345 reescrevem as três, com filosofias diferentes. ^c",
     "<h3>O que cada mod muda, em números</h3>" + nut_stats +
     "<h3>Por tipo de alimento</h3><p class=\"note\">Os tipos são os da tabela `food_type` do jogo; \"sem tipo\" são as linhas com o campo em branco. ^c</p>" + type_table +
     "<h3>Onde os dois mods tocam o mesmo item</h3>" + agree_table +
     "<h3>As maiores divergências em nutrição</h3>" + dis_table +
     "<h3>Efeito sobre a fome, com e sem o KRS Items</h3>"
     f'<p class="note">Digestão do jogo: {num(DIG_V, 1)} unidades por dia de jogo; com o KRS Items (`DigestionSpeed` x2,25): {num(DIG_K, 1)}. A tabela divide a nutrição por esse ritmo e mostra quantas horas a refeição "segura" a fome. É uma conta simples: ignora a parcela de digestão rápida (`short_term_nutrition_benefit_ratio`), então vale como ordem de grandeza. ^d</p>' + hunger_table +
     "<h3>Saúde que o 2011 acrescenta à comida</h3>" +
     f'<p class="note">O 2011 muda `health_benefit` em {len(hl)} itens; {sum(1 for _, a, b in hl if (a or 0) == 0 and (b or 0) > 0)} deles passam de 0 a um valor positivo (carne cozida de 0 a 62-70: comer passa a curar de verdade). Maiores valores em comida comum (os itens de missão estão na seção de lanches): ^c</p>' + hl_table +
     "<h3>Mudanças de tipo do 2011</h3>" + tc_table +
     "<h3>Opções</h3>" + options(OPTS_NUT))}

{sec("lanches", "O sistema de lanches do Chefs Kiss", f"{len(buffs)} buffs novos em {len(bclass)} classes, ligados a 38 alimentos comuns, mais 94 textos trocados e 44 novos. Duração dos buffs: {snack_dur}. ^c",
     "<h3>Buffs por classe</h3>" + snack_class_table +
     "<h3>O que o 2011 também mexe fora de comida do dia a dia</h3>" + out_table +
     '<p class="note">Estes itens existem na tabela `food` do jogo, mas só se obtêm por quest ou console. Foram reescritos junto com o resto, provavelmente por varredura da tabela inteira. Não entram em nada que o KRS publique. ^d</p>'
     "<h3>Opções</h3>" + options(OPTS_SNACK) +
     '<p class="note">Termos do 2011 (`terms of endearment.txt`): uso em "ANY mod collection" é proibido. Para a suite, isso significa só ideias com números e textos próprios. ^c</p>')}

{sec("servicos", "Preços de serviços (1105)", "Todos os valores do mod, lado a lado com o jogo, e onde cada um mora. ^c",
     table(["Serviço", "Jogo", "1105", "Onde está"], SVC) +
     '<p class="note">Só o banho é tabela. Os outros três são scripts do jogo (`Sleepover.lua` 263 linhas, `Trainers.lua` 238, `Horsetraders.lua` 521) substituídos por inteiro, com os comentários apagados. Mudar um preço com um script próprio é possível, mas os scripts do suite ainda estão em fase de teste (ver `krs_exploration`). A fórmula do cavalo do mod é quadrática e sem piso: não foi simulada. ^d</p>'
     '<h3>Opções</h3>' + options([
         ("A. Só o banho", "Patch de 6 linhas de `sequence`, no estilo do suite. Quarto, treinador e cavalo ficam como no jogo."),
         ("B. Banho + quarto temporário", "O quarto é o serviço mais barato do jogo (20); subir para 200 a 500 pesa mais no início. Exige um script próprio ou outro mecanismo."),
         ("C. Deixar o 1105 de fora", "A economia de serviços fica com o 1558 e com o que o suite já decidir sobre preços. Reavaliar na revisão final."),
     ]))}

<h2 id="decisoes">Decisões</h2>
<p class="lead">Respostas de 9 de outubro de 2026. Nada será consolidado ainda.</p>
{table(["#", "Tema", "Resposta", "Estado"], [
    ["1", "Apodrecimento", "Ajuste fino. Não consolidar nada ainda.", "Em ajuste: preencher a coluna 'Seu valor' por classe"],
    ["2", "Nutrição e refresco", "Adicionar à revisão (final).", "Adiado para a revisão final"],
    ["3", "Sistema de lanches do 2011", "Sem preferência.", "Aberto (sugestão: fora por enquanto; os termos impedem copiar)"],
    ["4", "Preços de serviços (1105)", "Sem preferência.", "Aberto (sugestão: só o banho agora; o resto na revisão de economia)"],
])}

<h2 id="metodo">Método e limites</h2>
<ul>
<li>Tudo vem dos arquivos já lidos na primeira passada (`grade_b_cells.csv`, `grade_b_newrows.json`, `grade_b_scripts.json`) e da tabela `food` do jogo 1.9.8 da réplica, só leitura. Nenhum mod foi executado.</li>
<li>Planilha de apoio: <code>docs/mods-review/grade_b_lote1_food.csv</code> (um item por linha, valor do jogo e o que cada mod coloca).</li>
<li>Os nomes dos tipos de alimento são inferidos; a unidade da digestão (por segundo de jogo) vem de `Params Reference.md` e dos valores lidos no 1.9.6; a conta de horas é uma aproximação.</li>
<li>A leitura dos termos do 2011 é do texto do arquivo; se vale para a suite é uma interpretação, sem consulta ao autor.</li>
</ul>
<footer>Gerado por <code>tools/build_grade_b_lote1.py</code>.</footer>
</main>
"""
page = page.replace("`Reviewed_Mods`", "<code>Reviewed_Mods</code>")
page = re.sub(r"(?<![\w>])`([^`<]+)`(?![\w])", r"<code>\1</code>", page)
out = os.path.join(R, "GRADE_B_LOTE1.html")
open(out, "w", encoding="utf-8", newline="\n").write(page)
print("wrote", out, len(page), "bytes")
