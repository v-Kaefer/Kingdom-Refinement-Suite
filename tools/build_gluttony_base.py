"""Gluttony Rebalanced: base analysis (hunger, food shelf life, day length) against the game's own values.

Reads docs/engine/rpg_constants_runtime.csv, Params Reference.md, the unmodified game's tables (food, pickable_item) and
modules/krs_items. Writes docs/modules/gluttony/ANALISE_BASE.html (Portuguese). Nothing is run, nothing outside docs/ is written.
Run: python tools/build_gluttony_base.py
"""
import csv
import html
import os
import re
import statistics as st
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUTDIR = os.path.join(ROOT, "docs", "modules", "gluttony")
os.makedirs(OUTDIR, exist_ok=True)
sys.path.insert(0, HERE)
import grade_b_extract as gx          # noqa: E402
import grade_b_page_style as S        # noqa: E402

CONF = {"c": ("confirmado", "lido nos arquivos, no jogo ou no log"), "d": ("deduzido", "inferido do nome, da ajuda, de conhecimento geral ou de fonte externa"), "n": ("não verificado", "precisa de teste no jogo")}


def esc(t):
    return html.escape(str(t), quote=False)


def rich(t):
    t = esc(t)
    t = re.sub(r"`([^`]+)`", r"<code>\1</code>", t)
    t = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", t)
    t = re.sub(r"\[([^\]]+)\]\((https?://[^)]+)\)", r'<a href="\2" target="_blank" rel="noopener">\1</a>', t)
    return re.sub(r"\s*\^([cdn])\b", lambda m: f' <span class="cf cf-{m.group(1)}" title="{esc(CONF[m.group(1)][0])}: {esc(CONF[m.group(1)][1])}">{CONF[m.group(1)][0]}</span>', t)


def num(x, nd=2):
    if abs(x - round(x)) < 1e-9:
        return str(int(round(x)))
    t = f"{x:.{nd}f}"
    if "." in t:
        t = t.rstrip("0").rstrip(".")
    return t.replace(".", ",")


def table(head, rows, cls="t compact", nums=()):
    th = "".join(f"<th>{esc(h)}</th>" for h in head)
    body = ""
    for r in rows:
        body += "<tr>" + "".join(f'<td class="{"num" if i in nums else ""}">{c if str(c).startswith("<") else rich(c)}</td>' for i, c in enumerate(r)) + "</tr>"
    return f'<div class="scroll"><table class="{cls}"><thead><tr>{th}</tr></thead><tbody>{body}</tbody></table></div>'


def fmt_s(sec):
    if sec < 90:
        return f"{num(sec, 0)} s"
    if sec < 5400:
        return f"{num(sec / 60, 1)} min"
    return f"{num(sec / 3600, 1)} h"


def rt(w):
    """a span the script fills with the real time of `w` world hours, at the chosen day length"""
    return f'<span data-w="{w:.5f}"></span>'


# ---------------------------------------------------------------- data
RUNTIME = {r["key"]: r for r in csv.DictReader(open(os.path.join(ROOT, "docs", "engine", "rpg_constants_runtime.csv"), encoding="utf-8"))}
KRS = dict(re.findall(r'rpg_param_key="([A-Za-z]+)" rpg_param_value="([^"]*)"', open(os.path.join(ROOT, "modules", "krs_items", "Data", "Libs", "Tables", "rpg", "rpg_param__krs_items.xml"), encoding="utf-8").read()))


def rv(k):
    return float(RUNTIME[k]["runtime_value"])


DIG, DIG_K = rv("DigestionSpeed"), float(KRS["DigestionSpeed"])
FULL, THR, HUGE, EXTR, OVER = rv("FoodFull"), rv("StarvationThreshold"), rv("StarvationHugeThreshold"), rv("StarvationExtremeThreshold"), rv("FoodOverEat")
UPD, UPD_K = DIG * 86400, DIG_K * 86400          # units per world day


def hrs(units, rate):
    return units / rate / 3600.0


G = gx.Game()
PK = {r["item_id"]: r for r in G.tables["pickable_item"]["rows"]}
FOOD = {r["item_id"]: r for r in G.tables["food"]["rows"]}
NAME = {re.sub(r"\s*\[[0-9a-f]{8}\]$", "", G.label(i)): i for i in FOOD}

# ---------------------------------------------------------------- 1. calibration: what is one unit of nutrition worth
REF = [("Bread", 265, "pão de trigo"), ("Beef_cooked", 250, "carne bovina assada"), ("hardboiled_egg", 155, "ovo cozido"), ("Cheese quarter", 400, "queijo duro"),
       ("Apple", 52, "maçã"), ("lentil_soup", 100, "ensopado de lentilha"), ("Salami_01", 430, "salame seco"), ("porridge", 70, "mingau")]
cal_rows, kcal_units = [], []
for n, k100, lab in REF:
    i = NAME[n]
    w = float(PK[i]["weight"])
    nu = float(FOOD[i]["nutrition_benefit"])
    kcal = w * 10 * k100
    ku = kcal / nu
    kcal_units.append(ku)
    cal_rows.append([f"{n} ({lab})", num(w), num(nu), num(k100), num(kcal), num(ku, 0)])
K_MED = st.median(kcal_units)
K_LO, K_HI = min(kcal_units), max(kcal_units)
cal_table = table(["Item do jogo", "Peso no jogo (kg)", "Nutrição", "kcal por 100 g (referência)", "kcal do item inteiro", "kcal por unidade de nutrição"], cal_rows, nums=(1, 2, 3, 4, 5))

# ---------------------------------------------------------------- 2. what a person like Henry spends
W_KG, H_CM, AGE = 75, 175, 25
BMR = 10 * W_KG + 6.25 * H_CM - 5 * AGE + 5
LEVELS = [("Sedentário ou atividade leve", 1.55), ("Moderadamente ativo (exemplo da FAO)", 1.85), ("Muito ativo (trabalho braçal, marcha, combate)", 2.2)]
en_rows = []
for lab, pal in LEVELS:
    e = BMR * pal
    cells = [lab, num(pal), num(e, 0)]
    for k in (40, K_MED, 120):
        upd = e / k
        rate = upd / 86400
        cells.append(f"{num(upd, 0)} u/dia; {rate:.6f}".replace(".", ",") + f" ({num(rate / DIG, 2)}x jogo; {num(rate / DIG_K, 2)}x KRS)")
    en_rows.append(cells)
energy_table = table(["Atividade", "PAL", "kcal por dia", "Se 1 unidade = 40 kcal", f"Se 1 unidade = {num(K_MED, 0)} kcal (mediana)", "Se 1 unidade = 120 kcal"], en_rows, nums=(1, 2))

# ---------------------------------------------------------------- 3. meal interval in the bar
MEALS = [("Lanche (cerca de 500 kcal)", 500), ("Refeição (cerca de 900 kcal)", 900), ("Refeição grande (cerca de 1200 kcal)", 1200)]
meal_rows = []
for lab, kcal in MEALS:
    u = kcal / K_MED
    meal_rows.append([lab, num(u, 1), num(hrs(u, DIG), 1) + " h", rt(hrs(u, DIG)), num(hrs(u, DIG_K), 1) + " h", rt(hrs(u, DIG_K))])
meal_table = table(["Comida", f"Unidades (a {num(K_MED, 0)} kcal)", "Segura a fome no jogo", "Em tempo real", "Segura a fome no KRS Items", "Em tempo real"], meal_rows, nums=(1, 2, 4))

# game items as meals
item_rows = []
for n in ("Bread", "Beef_cooked", "Rabbit meat cooked", "lentil_soup", "Smoked Rabbit meat", "hardboiled_egg", "Apple"):
    i = NAME[n]
    nu = float(FOOD[i]["nutrition_benefit"])
    item_rows.append([n, num(nu), FOOD[i]["max_status"], num(hrs(nu, DIG), 1) + " h", num(hrs(nu, DIG_K), 1) + " h"])
item_table = table(["Item do jogo", "Nutrição", "`max_status`", "Horas de fome no jogo", "No KRS Items"], item_rows, nums=(1, 2, 3, 4))

U900 = 900 / K_MED
# ---------------------------------------------------------------- 4. states, game versus a real person
state_rows = [
    ["Fome volta depois de uma refeição mista", "4 a 6 h", f"{num(hrs(U900, DIG), 1)} h para uma refeição de {num(U900, 0)} unidades (cerca de 900 kcal)", f"{num(hrs(U900, DIG_K), 1)} h"],
    ["Fome forte, irritação", "12 a 24 h sem comer", f"{num(hrs(FULL - THR, DIG), 1)} h de cheio até 'com fome' (50)", f"{num(hrs(FULL - THR, DIG_K), 1)} h"],
    ["Fraqueza marcada", "2 a 3 dias sem comer", f"{num(hrs(FULL - HUGE, DIG), 1)} h até a fome grande (25)", f"{num(hrs(FULL - HUGE, DIG_K), 1)} h"],
    ["Inanição (efeito máximo no jogo)", "semanas sem comer até risco de vida", f"{num(hrs(FULL - EXTR, DIG), 1)} h até 0", f"{num(hrs(FULL - EXTR, DIG_K), 1)} h"],
]
state_table = table(["Estado", "Pessoa real (mesma atividade)", "Jogo (horas de mundo)", "KRS Items"], state_rows)

# ---------------------------------------------------------------- 5. shelf life
CLASSES = [  # name, game h, real low h, real high h, note
    ("Carne e peixe crus", 24, 12, 72, "ambiente 12 a 24 h; porão frio 2 a 3 dias; geladeira: aves e carne moída 1 a 2 dias, peças de boi, porco e cordeiro 3 a 5 dias"),
    ("Miúdos crus", 24, 12, 36, "como a carne crua, mais rápido"),
    ("Leite", 24, 12, 36, "sem refrigeração dura menos de um dia"),
    ("Cogumelos crus", 24, 24, 72, ""),
    ("Carne e peixe cozidos", 48, 24, 72, "ambiente 1 dia; porão 2 a 3 dias"),
    ("Verduras cozidas e sopas", 48, 24, 72, ""),
    ("Ovo cozido duro", 48, 72, 168, "1 semana na geladeira"),
    ("Ovo cru com casca", 48, 336, 840, "3 a 5 semanas na geladeira; 2 semanas ou mais em ambiente fresco"),
    ("Pão e massas", 96, 72, 168, "pão denso de centeio dura mais que o de trigo"),
    ("Raízes e repolho crus", 96, 336, 2160, "porão fresco: semanas a meses"),
    ("Carne defumada, curada e seca", 120, 336, 2160, "sal, fumaça e secagem: semanas a meses"),
    ("Maçã e pera", 120, 720, 2160, "porão: 1 a 3 meses"),
    ("Queijo duro", 120, 720, 4320, "1 a 6 meses"),
]
shelf_rows = []
for nme, g, lo, hi, note in CLASSES:
    shelf_rows.append([nme + " ^d", num(g), num(g * 2), f"{num(lo)} a {num(hi)}", f"{num(g / hi, 2)} a {num(g / lo, 2)}x", rt(g), rt(g * 2), note])
shelf_table = table(["Classe", "Jogo (h)", "2X (h)", "Realista (h, ambiente fresco a porão)", "Jogo ÷ realista", "Jogo em tempo real", "2X em tempo real", "Observação"], shelf_rows, nums=(1, 2, 3, 4))

# ---------------------------------------------------------------- 6. day length scenarios
DAYS = (4, 5, 6)          # minutes of real time per world hour: 4 is today (ratio 15, measured), 5 and 6 are the options


def real(h, d):
    return fmt_s(h * d * 60.0)


scen = [("Cheio até 'com fome', jogo", hrs(FULL - THR, DIG)), ("Cheio até 'com fome', KRS Items", hrs(FULL - THR, DIG_K)),
        (f"Refeição de {num(U900, 0)} unidades segura, jogo", hrs(U900, DIG)), (f"Refeição de {num(U900, 0)} unidades segura, KRS Items", hrs(U900, DIG_K)),
        ("Carne crua estraga (24 h)", 24), ("Carne cozida estraga (48 h)", 48), ("Carne defumada estraga (120 h)", 120), ("Mesma, com o 2X (240 h)", 240),
        ("Dormir 8 h (regeneração cheia)", 8), ("Item solto no chão some (2 dias)", 48), ("Reputação se propaga (3 h)", 3)]
scen_rows = [[lab, num(h, 1) + " h"] + [real(h, d) for d in DAYS] for lab, h in scen]
scen_table = table(["Duração em tempo de mundo", "Horas de mundo", "Hora de 4 min (hoje, dia de 96 min)", "Hora de 5 min (dia de 120 min)", "Hora de 6 min (dia de 144 min)"], scen_rows, nums=(1, 2, 3, 4))

keep_rows = []
for lab, rate in (("Jogo", DIG), ("KRS Items", DIG_K)):
    keep_rows.append([lab, f"{rate:.6f}".replace(".", ",")] + [f"{(rate * d / 4):.6f}".replace(".", ",") + f" ({num(d / 4, 2)}x)" for d in (5, 6)])
keep_table = table(["Base", "`DigestionSpeed` hoje (hora de 4 min)", "Para manter o mesmo ritmo em tempo real, hora de 5 min", "Hora de 6 min"], keep_rows)

ratio_rows = [[f"{d} min" + (" (hoje)" if d == 4 else ""), num(60 / d, 1), num(24 * d, 0) + " min (" + num(24 * d / 60, 1) + " h)", num(1 / d, 2) + " h"] for d in DAYS]
ratio_table = table(["Uma hora de mundo dura", "Segundos de mundo por segundo real (razão)", "O dia inteiro dura", "Horas de mundo por minuto real"], ratio_rows, nums=(1, 2, 3))

MECH = [
    ("Fome (`DigestionSpeed`) e cansaço (`ExhaustionSpeed`)", "segundo de mundo", "os valores não mudam; em tempo real, tudo fica 1,25x (5 min) ou 1,5x (6 min) mais devagar", "c"),
    ("Sono: regeneração (`SleepHealthRegenBaseSpeed`, 8 h de mundo), ficar acordado e dormir demais (12 h)", "hora de mundo", "idem; o avanço de tempo (dormir, esperar) é acelerado pelo motor, então o que o jogador espera na tela pode não mudar", "d"),
    ("Apodrecimento (`decay_time_hours`) e a perk Proper diet (120 h)", "hora de mundo", "idem: a carne crua (24 h) dura 96, 120 ou 144 minutos reais", "c"),
    ("Álcool, ressaca (4 h de mundo), intoxicação, veneno", "segundo de mundo", "idem", "c"),
    ("Itens soltos somem (2 dias), corpos reaparecem (800 min), reputação se propaga (3 h)", "tempo de mundo", "idem: duram 25% ou 50% mais em tempo real", "c"),
    ("Horários de NPCs, lojas, toque de recolher, dia e noite", "relógio do mundo", "cada atividade tem mais tempo real; cada noite dura mais; viagens a pé gastam menos horas de mundo por minuto andado (-20% ou -33%), logo menos fome e menos apodrecimento por viagem. O motor aceita a mudança de razão por script (medido)", "d"),
    ("Combate, buffs de comida e de poção (segundos), perks de combate (`PerkBerserkDuration` 30)", "segundo real", "não mudam; mas uma luta de 1 minuto gasta 15 min de mundo (hora de 4 min), 12 min (5 min) ou 10 min (6 min): a fome por luta cai", "d"),
    ("Sujeira da roupa, desgaste de armas e armaduras", "distância ou uso", "não dependem do relógio", "d"),
    ("Leitura de livros (10 a 25 h) e esperas", "hora de mundo no avanço de tempo", "mesma duração em horas de mundo; o tempo real do avanço depende do motor", "n"),
]
mech_table = table(["Mecânica", "Medida em", "Efeito de passar a hora de mundo de 4 para 5 ou 6 minutos reais", "Confiança"], [[a, b, c, f'<span class="cf cf-{k}">{CONF[k][0]}</span>'] for a, b, c, k in MECH])

STEPS = [
    "**Medido em 10 out 2026 (réplica 1.9.8, sem executar mais nada):** a razão é 15 segundos de mundo por segundo real (14,9 a 15,3 em 8 janelas de 20 s), ou seja, uma hora de mundo dura 4 minutos reais e o dia dura 96. A constante `DefaultWorldTimeRatio` também vale 15. O relógio do mundo fica parado (`paused=true`) no menu e só corre com o save carregado. ^c",
    "**Mudar a razão por script funciona.** `Calendar.SetWorldTimeRatio(x)` aceitou os valores 10, 6,67 e 4,44 e o jogo passou a andar a 4,5 e 6,8 segundos de mundo por segundo real, sem o motor devolver o valor em pelo menos 60 s. Falta ver se o valor sobrevive a carregar outro save, dormir, esperar e conversar. ^c",
    "**Escolher o que se ancora.** (a) por dia de mundo, para que o gasto de energia seja o de uma pessoa ativa; (b) por intervalo entre refeições, de 4 a 6 horas de mundo; (c) por minuto real de jogo, para a fome não atrapalhar o ritmo de quem joga.",
    "**Dizer os alvos em minutos reais** de cheio até 'com fome' e de 'com fome' até zero, já na escala certa (hora de 6 minutos): a seção do plano devolve o `DigestionSpeed` e os limiares. ^d",
    "**Se o valor sobreviver aos testes,** definir quem é dono do ritmo do dia (não é comida: afeta tudo) e afinar, juntos, `DigestionSpeed`, `ExhaustionSpeed` e o apodrecimento.",
]

FIND = [
    ("A taxa de fome do jogo já é de uma pessoa muito ativa; o KRS Items passa muito disso", f"Pelo peso e pela nutrição dos itens, 1 unidade vale {num(K_LO, 0)} a {num(K_HI, 0)} kcal (mediana {num(K_MED, 0)}). A {num(K_MED, 0)} kcal por unidade, o jogo gasta {num(UPD, 0)} unidades por dia de mundo, cerca de {num(UPD * K_MED, 0)} kcal, que é o que gasta quem faz trabalho braçal pesado (Henry: {num(BMR * 1.85, 0)} a {num(BMR * 2.2, 0)} kcal). Com o KRS Items (x2,25) seriam cerca de {num(UPD_K * K_MED, 0)} kcal por dia. A conta depende muito da calibração (o intervalo vai de 40 a 120 kcal por unidade), então não fecha sozinha uma decisão. ^d"),
    ("O intervalo entre refeições do jogo é o de uma pessoa real, se a refeição for de tamanho real", f"Uma refeição de cerca de 900 kcal vale {num(900 / K_MED, 1)} unidades e segura a fome por {num(hrs(900 / K_MED, DIG), 1)} h de mundo no jogo e {num(hrs(900 / K_MED, DIG_K), 1)} h no KRS Items. Uma pessoa real volta a sentir fome de 4 a 6 h depois de uma refeição mista (um estudo mediu cerca de 306 min para o estômago esvaziar após 800 kcal, em 9 jovens). O que afasta o jogo da realidade é a barra: de cheio (100) a 'com fome' (50) são 24 h, porque um pão inteiro (17) ou uma carne assada (21) valem 1.400 a 1.600 kcal. ^d"),
    ("Os conservados duram muito menos que na vida real; os crus são parecidos", "Carne crua em 24 h é o que se espera sem geladeira. Mas defumado, curado e seco (120 h), raízes (96 h), ovo cru (48 h), maçã (120 h) e queijo (120 h) duram de 3 a 50 vezes menos que na vida real. Como o jogo comprime o dia, um mês real de validade seria 2 horas de jogo (dia de 4 min): a validade realista literal não serve, e vale escolher valores comprimidos por classe. ^d"),
    ("Esticar a hora de mundo de 4 para 5 ou 6 minutos reais muda o tempo real de tudo que é medido em tempo de mundo", "Fome, cansaço, sono, apodrecimento, álcool, reputação e itens no chão passam a durar 25% ou 50% mais em tempo real, sem mexer em nenhum parâmetro. Combate e buffs ficam iguais. Para manter a cadência real de hoje, a digestão teria de subir na mesma proporção. ^d"),
    ("A razão do tempo foi medida: 15, o dia dura 96 minutos reais", "Dois testes na réplica 1.9.8 com um save carregado: a hora do dia andou 14,9 a 15,3 segundos de mundo por segundo real, e a constante `DefaultWorldTimeRatio` vale 15. Uma hora de mundo dura 4 minutos reais (os 4 minutos que você tinha em mente são por hora, não por dia). O comando `Calendar.SetWorldTimeRatio` funciona por script e o jogo andou nas razões pedidas. O relógio fica parado no menu. ^c"),
]
fhtml = "".join(f'<div class="find"><h3>{esc(t)}</h3><p>{rich(d)}</p></div>' for t, d in FIND)
steps_html = "<ol>" + "".join(f"<li>{rich(s)}</li>" for s in STEPS) + "</ol>"

# ---------------------------------------------------------------- 7. six minutes a day: compensate, then add the author's changes
D6 = 6.0                 # minutes of real time per world hour in the plan


def rt6(h):
    return real(h, 6)

F = 1.5
DIG_C = DIG * F
DIG_CK = DIG_C * (DIG_K / DIG)           # compensated, then the author's x2.25 on top
RATE = {"jogo": DIG, "comp": DIG_C, "compk": DIG_CK}
W_PER_MIN = 1 / D6                       # world hours per real minute at 6 min per world hour


def scn(label, rate):
    uph = rate * 3600
    to50, to25, to0 = hrs(FULL - THR, rate), hrs(FULL - HUGE, rate), hrs(FULL - EXTR, rate)
    return [label, f"{rate:.9f}".replace(".", ","), num(uph, 2), f"{num(to50, 1)} h; " + rt6(to50), f"{num(to25, 1)} h; " + rt6(to25), f"{num(to0, 1)} h; " + rt6(to0), f"{num(U900 / (rate * 3600), 1)} h; " + rt6(U900 / (rate * 3600))]


# the real-time pace is shown at the day length typed in the box, but the rows are built for 6 min a day
six_rows = [scn("A. Jogo sem compensar (hora de 6 min)", DIG), scn("B. Compensado (x1,5): o mesmo ritmo real de hoje (hora de 4 min)", DIG_C), scn("C. Compensado + as mudanças do autor (x2,25 do KRS Items)", DIG_CK)]
six_table = table(["Cenário", "`DigestionSpeed`", "Unidades por hora de mundo", "Cheio até 'com fome' (50)", "Até a fome grande (25)", "Até 0", f"Uma refeição de {num(U900, 0)} unidades segura"], six_rows, nums=(1, 2))

COMP = [  # key, factor kind, note
    ("DigestionSpeed", "mul", "fome; é a linha que o KRS Items já escreve (hoje 0,001302084)"),
    ("ExhaustionSpeed", "mul", "cansaço de longo prazo; mesmo valor da fome no jogo"),
    ("MetabolismDigestSpeed", "mul", "digestão de álcool e veneno"),
    ("MetabolismAbsorbSpeed", "mul", "absorção (remoção) de álcool e veneno"),
    ("AlcoholismDuration", "div", "duração do alcoolismo, em tempo de mundo"),
    ("AlcoholBaseHangoverDuration", "div", "ressaca, em tempo de mundo"),
    ("AlcoholBlackoutDuration", "div", "apagão por álcool; a unidade não está documentada"),
    ("ReputationPropagationTime", "div", "tempo para a reputação se espalhar, em tempo de mundo"),
    ("ReputationPropagationBiasTime", "div", "variação do tempo acima"),
    ("BaseItemDisappearingTime", "div", "item solto no chão some, em tempo de mundo"),
    ("MaxItemDisappearingTime", "div", "idem, limite"),
    ("RespawnTimeBase", "div", "corpo escondido reaparece, em minutos de jogo"),
    ("StillBuffDuration", "div", "ficar parado ativa o buff, em segundos de mundo"),
    ("PerkProperDietActivationTime", "div", "dieta que ativa a perk Proper diet, em horas"),
    ("ItemOwnerFadePriceToHours", "div", "horas de mundo por decigrosh para o dono esquecer um item"),
    ("ItemOwnerFadeConspicuousnessToHours", "div", "idem, por ponto de visibilidade"),
]
comp_rows = []
for k, kind, note in COMP:
    v0 = float(RUNTIME[k]["runtime_value"])
    v1 = v0 * F if kind == "mul" else v0 / F
    comp_rows.append([f"`{k}`", num(v0, 9), ("x1,5" if kind == "mul" else "÷1,5"), num(v1, 9 if v1 < 100 else 1), note])
comp_table = table(["Parâmetro", "Jogo", "Regra", "Compensado", "O que é"], comp_rows, nums=(1, 3))

SPOIL = [24, 48, 72, 96, 120]
spoil_rows = [[f"{num(g)} h", num(g / F, 1) + " h", rt6(g / F), "x2: " + num(2 * g / F, 1) + " h", rt6(2 * g / F)] for g in SPOIL]
spoil_table = table(["Jogo (`decay_time_hours`)", "Compensado (÷1,5)", "Em tempo real", "Com uma mudança do autor de x2 (exemplo)", "Em tempo real"], spoil_rows, nums=(0, 1, 3))

NOT = [
    ("`SleepHealthRegenBaseSpeed`, `OversleepnessFillTime`, `OversleepnessEmptyTime`, `MinPossibleSleepTime`", "acontecem durante o avanço de tempo (dormir, esperar), que o motor acelera: a duração em horas de mundo é o que importa, não o relógio"),
    ("`OverreadnessFillTime`, `OverreadnessEmptyTime` e `length_in_game_hours` dos livros", "leitura também é avanço de tempo"),
    ("`StarvationHealthLossSpeed`, `FoodHealSpeed`, `FoodPoisoning*HealthEffectSpeed`", "a unidade (segundo de mundo ou real) não está documentada; decidir depois de medir"),
    ("`StarvationPlayerEffect*` (90, 120, 45, 75)", "unidade não verificada; o KRS Items já mexe em três deles"),
    ("Buffs em segundos (comida, poção, perk de combate)", "tempo real, não mudam com o dia"),
    ("Horários de NPCs, lojas, noite", "seguem o relógio do mundo; o dia mais longo dá mais tempo real a cada atividade, e isso fica de bônus"),
]
not_table = table(["Fica como está", "Por quê"], [[a, b] for a, b in NOT])

# the bar: where the hungry line has to sit for a given real-time target, at the rate of scenario C
bar_rows = []
for t in (20.0, 30.0, 43.0, 60.0, 75.0, 90.0):
    wh = t * W_PER_MIN
    units = DIG_CK * 3600 * wh
    thr = FULL - units
    verdict = f"{num(thr, 0)}" if thr >= 0 else "impossível: gasta mais que a barra inteira"
    bar_rows.append([f"{num(t, 0)} min", num(wh, 1) + " h", num(units, 0), verdict])
bar_table = table(["Cheio até 'com fome' em (tempo real, hora de 6 min)", "Horas de mundo", "Unidades gastas", "Limiar `StarvationThreshold` necessário"], bar_rows, nums=(1, 2, 3))

CONS = []
for lab, rate in (("A. Jogo sem compensar", DIG), ("B. Compensado", DIG_C), ("C. Compensado + KRS Items", DIG_CK)):
    upm = rate * 3600 * W_PER_MIN
    CONS.append([lab, num(upm, 2), num(upm * 60 / 17, 1), num(upm * 60 / 21, 1), num(upm * 60 / 8, 1)])
cons_table = table(["Cenário (hora de 6 min)", "Unidades gastas por minuto real", "Pães (17) em 1 hora real", "Carnes assadas (21) em 1 hora real", "Sopas (8) em 1 hora real"], CONS, nums=(1, 2, 3, 4))
NUT_X = [(h, h * DIG_CK * 3600 / U900) for h in (3, 4, 5)]
nut_text = "; ".join(f"para a refeição segurar {h} h de mundo, a nutrição teria de ser x{num(x, 1)}" for h, x in NUT_X)

SIX = f"""
<h2 id="seis">Plano para a hora de mundo de 6 minutos</h2>
<p class="lead">Regra do autor (10 out 2026): tudo que fica 50% mais longo em tempo real com a hora de mundo de 6 minutos (dia de 144 minutos, razão 10) é compensado, e só depois entram as mudanças do autor, somadas por cima. Os tempos reais desta seção são sempre para a hora de mundo de 6 minutos. ^d</p>
<h3>1. Compensar o que estica</h3>
<p class="note">Taxas por segundo de mundo sobem x1,5; durações em tempo de mundo caem ÷1,5. Todas já existem como constantes do jogo; a primeira (`DigestionSpeed`) é escrita hoje pelo KRS Items por linha de patch de `rpg_param`. ^c</p>
{comp_table}
<h3>Apodrecimento</h3>
<p class="note">Todas as linhas de `decay_time_hours` (111 perecíveis) ÷1,5; as mudanças por classe, como o x2 do 1483, entram depois. Os 91 itens com 0 (não estragam) ficam como estão. ^d</p>
{spoil_table}
<h3>O que não se compensa</h3>
{not_table}
<h3>2. Fome: antes e depois das mudanças</h3>
{six_table}
<p class="note">B devolve o ritmo real de hoje (a hora de 4 minutos, sem compensar). C é B com a digestão x2,25 do KRS Items por cima: {f'{DIG_CK:.9f}'.replace('.', ',')}, que substituiria o 0,001302084 atual. ^d</p>
<h3>3. A barra de fome</h3>
<p class="lead">A taxa do cenário C esvazia {num(DIG_CK * 3600, 2)} unidades por hora de mundo. Com a barra de hoje (cheio 100, 'com fome' 50, grande 25, zero 0), isso dá {num(hrs(FULL - THR, DIG_CK), 1)} h de mundo (cerca de {num(hrs(FULL - THR, DIG_CK) / W_PER_MIN, 1)} min reais) de cheio até 'com fome'. A tabela mostra onde o limiar teria de ficar para outros tempos. ^d</p>
{bar_table}
<p class="note">Duas alavancas pareiam a barra com o ritmo: o limiar (e os de fome grande e zero) e o valor de nutrição dos alimentos. Quanto à segunda: {nut_text} (refeição de {num(U900, 0)} unidades, cerca de 900 kcal). Subir `StarvationThreshold` faz a fome chegar antes; descê-lo dá folga. `FoodFull` (100) e `FoodOverEat` (120) definem a barra inteira; mexer neles muda a reserva máxima. ^d</p>
<h3>4. O que isso pede do jogador</h3>
<p class="note">Consumo por minuto real de jogo, que é o que as quedas de drop de animais e os preços de mercado vão pressionar. ^d</p>
{cons_table}
<p class="note">Em C o jogador gasta o equivalente a um pão a cada cerca de {num(17 / (DIG_CK * 3600 * W_PER_MIN), 0)} minutos reais, andando ou lutando; nada disso considera dormir, esperar ou ler, que passam o relógio acelerado. Comparar com a oferta (drops e preços) é o próximo passo. ^d</p>
"""

MEAS = [
    ("Razão do tempo", "**15 segundos de mundo por segundo real** (8 janelas de 20 s, de 14,2 a 15,3, média 14,9); `Calendar.GetWorldTimeRatio()` devolve 15, igual a `DefaultWorldTimeRatio`. Uma hora de mundo dura 4 minutos reais; o dia, 96", "c"),
    ("O relógio no menu", "parado: `IsWorldTimePaused()` é verdadeiro e a hora do dia não anda (9,0 sem save; 4,99 com o save carregado ainda no menu). Só corre depois que o save abre", "c"),
    ("Mudar a razão por script", "`Calendar.SetWorldTimeRatio(x)` aceitou 10, 6,67 e 4,44; o jogo andou a 4,5 e 6,8 s de mundo por s real e o valor lido de volta foi o gravado. O motor não o devolveu em pelo menos 60 s. Não testado: carregar outro save, dormir, esperar, conversar", "c"),
    ("Fome e cansaço em jogo", "a barra de fome desce em degraus de 0,0122 a cada 2,04 s reais (30 s de mundo): 0,00039 unidade por segundo de mundo, 0,68x do `DigestionSpeed`; o cansaço, 0,73x do `ExhaustionSpeed`. A razão é parecida com a perk Ascetic (x0,7), que o personagem do save pode ter; não verificado. Depois de 36 s a barra parou de descer por mais de 3 minutos reais (0,5 h de mundo), com o jogo rodando: provável cena ou diálogo do save (digestão zerada), não verificado", "d"),
    ("Constantes na 1.9.8", "lidas em jogo, iguais às da 1.9.6: `DigestionSpeed` 0,000578704, `ExhaustionSpeed` 0,000578704, `FoodFull` 100, `FoodOverEat` 120, `StarvationThreshold` 50, `StarvationHugeThreshold` 25, `StarvationExtremeThreshold` 0, `ShortTermNutritionDigestionSpeedMultiplier` 5", "c"),
    ("Relógio real em Lua", "`os.time` existe (segundos inteiros); `os.clock` não. O `kcd.log` não traz hora por linha: o script que vigia o log marcou a hora de chegada de cada linha, com 0,4 s de precisão", "c"),
    ("Dia e noite", "a hora do dia (`GetWorldHourOfDay`, 0 a 24) e o comando `e_TimeOfDay` dão a mesma hora; não medi nascer e pôr do sol, só uma janela de 0,6 h de mundo (de 5,0 a 5,65). Com razão 15, uma volta completa leva 96 minutos reais", "d"),
    ("Testes que falharam", "o primeiro probe criou o sensor no menu e o nível o destruiu ao carregar o save; a segunda versão o recria, mas deixou várias cópias ativas, que repetiram o teste da razão em cascata (10, 6,67, 4,44, 2,96, 1,98). Os dados continuam válidos (cada linha traz a razão lida), mas o valor final da razão em memória ficou errado até o jogo fechar. Nenhum save foi gravado", "c"),
]
meas_table = table(["Etapa", "Estado", "Confiança"], [[a, b, f'<span class="cf cf-{k}">{CONF[k][0]}</span>'] for a, b, k in MEAS])

JS = r"""
(function(){
  var inp=document.getElementById('dmin');
  function fmt(s){ if(s<90) return Math.round(s)+' s'; if(s<5400) return (s/60).toFixed(1).replace('.',',')+' min'; return (s/3600).toFixed(1).replace('.',',')+' h'; }
  function upd(){
    var d=parseFloat((inp.value||'').replace(',','.')); if(!(d>0)) d=4;
    var R=60/d;
    [].slice.call(document.querySelectorAll('[data-w]')).forEach(function(e){ e.textContent=fmt(parseFloat(e.dataset.w)*3600/R); });
    document.getElementById('ratio-r').textContent=Math.round(R*10)/10;
    document.getElementById('ratio-h').textContent=fmt(86400/R);
  }
  inp.addEventListener('input',upd);
  [].slice.call(document.querySelectorAll('[data-set]')).forEach(function(b){ b.addEventListener('click',function(){ inp.value=b.dataset.set; upd(); }); });
  upd();
})();
"""

nav = "".join(f'<a href="#{i}">{t}</a>' for i, t in (("resumo", "Resumo"), ("relogio", "Relógio"), ("energia", "Energia"), ("fome", "Fome"), ("validade", "Validade"), ("dia", "Dia de 5 ou 6 min"), ("seis", "Plano de 6 min"), ("medir", "Medir o dia"), ("plano", "Plano"), ("fontes", "Fontes e limites")))
page = f"""<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Gluttony Rebalanced, análise de base</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=IBM+Plex+Sans+Condensed:wght@500;600&family=IBM+Plex+Sans:wght@400;500;600&display=swap">
<style>{S.CSS}
.ratio{{display:flex;gap:10px;align-items:center;flex-wrap:wrap;background:var(--surface);border:1px solid var(--line);border-radius:4px;padding:10px 14px;margin:12px 0}}
.ratio input{{font:inherit;width:5rem;padding:4px 6px;background:var(--bg);color:var(--ink);border:1px solid var(--line);border-radius:3px}}
.ratio button{{font:inherit;padding:4px 10px;background:var(--surface2);color:var(--ink);border:1px solid var(--line);border-radius:3px;cursor:pointer}}
</style>
<div class="top"><b>Gluttony Rebalanced</b><nav>{nav}</nav></div>
<main>
<header>
<h1>Gluttony Rebalanced: análise de base contra o jogo</h1>
<p class="lead">Quanto duram os alimentos, quanto tempo uma pessoa com a atividade de Henry aguenta sem fome, e o que muda ao esticar a hora de mundo de 4 para 5 ou 6 minutos reais (o dia de 96 para 120 ou 144). Compara tudo com os valores do jogo 1.9.8 e com o que o KRS Items já faz. Só leitura: nada foi alterado nem testado no jogo, e nenhum valor novo foi escolhido.</p>
<p class="legend"><span><span class="cf cf-c">confirmado</span> lido nos arquivos</span><span><span class="cf cf-d">deduzido</span> inferido, de conhecimento geral ou de fonte externa</span><span><span class="cf cf-n">não verificado</span> precisa de teste</span></p>
</header>

<h2 id="resumo">Resumo</h2>
<div class="cols">{fhtml}</div>

<h2 id="relogio">Relógio: quanto dura o dia</h2>
<div class="ratio"><label for="dmin"><b>Minutos reais por hora de mundo</b></label><input id="dmin" type="text" inputmode="decimal" value="4">
<button type="button" data-set="4">4</button><button type="button" data-set="5">5</button><button type="button" data-set="6">6</button>
<span>Razão: <b id="ratio-r"></b> segundos de mundo por segundo real; o dia inteiro dura <b id="ratio-h"></b>.</span></div>
<p class="note">Os valores marcados "em tempo real" mudam com este campo; o valor de hoje, 4, foi medido no jogo (razão 15). ^c</p>
{ratio_table}

<h2 id="energia">Energia: quanto vale uma unidade de nutrição</h2>
<p class="lead">O jogo mede a comida em unidades de nutrição (`nutrition_benefit`). Para compará-las com uma pessoa, convertemos o item inteiro (peso do jogo × kcal por 100 g de um alimento parecido) em kcal. Os kcal de referência são valores aproximados de conhecimento geral. ^d</p>
{cal_table}
<p class="note">A unidade vale de {num(K_LO, 0)} a {num(K_HI, 0)} kcal, mediana {num(K_MED, 0)}. A diferença vem de o jogo dar o mesmo tipo de peso a itens muito diferentes (um queijo de 0,6 kg dá só 10 unidades, um pão de 0,6 kg dá 17). ^d</p>
<h3>O que Henry gasta por dia</h3>
<p class="note">Estimativa para um homem de {W_KG} kg, {H_CM} cm e {AGE} anos (metabolismo basal de {num(BMR, 0)} kcal pela equação de Mifflin-St Jeor); a atividade vem do fator PAL da [FAO](https://www.fao.org/3/y5686e/y5686e08.htm): a faixa moderada tem 1,85 como exemplo e a muito ativa (trabalho braçal) fica entre 2,0 e 2,4 ([tabela de PAL](https://en.wikipedia.org/wiki/Physical_activity_level)). Henry anda, carrega equipamento e luta, então a faixa de 1,85 a 2,2 é a mais próxima. A FAO adverte que esses valores são para grupos, não para indivíduos. ^d</p>
{energy_table}
<p class="note">Cada célula mostra as unidades por dia e o `DigestionSpeed` que daria esse gasto, com o múltiplo do valor do jogo ({DIG:.9f}) e do KRS Items ({DIG_K:.9f}).</p>

<h2 id="fome">Fome: quanto tempo até sentir fome</h2>
<h3>Uma pessoa real e o jogo</h3>
{state_table}
<p class="note">A volta da fome em 4 a 6 horas é plausível, mas não há um número firme: [um estudo](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12534588/) mediu cerca de 306 minutos para o esvaziamento do estômago após uma refeição mista de 800 kcal em 9 adultos jovens, e a fome depende também de hormônios e da composição da refeição. As demais linhas são conhecimento geral, sem fonte aqui. ^d</p>
<h3>Quanto segura cada comida</h3>
<p class="note">Horas de mundo = unidades ÷ ritmo (`DigestionSpeed` × 3.600). Ignora a parte de curto prazo da comida (digere {num(rv('ShortTermNutritionDigestionSpeedMultiplier'))}x mais rápido), então é ordem de grandeza. ^d</p>
{meal_table}
{item_table}
<p class="note">`max_status` (pão 50, carne assada 40, queijo 30, sopa 20; bebidas 100) tem significado não verificado. Lido como teto da barra ele não fecha: a carne assada (40) nunca tiraria o jogador da fome, que começa em 50. Não use `max_status` para nenhuma conta até um teste no jogo. ^n</p>

<h2 id="validade">Validade: quanto duram os alimentos</h2>
<p class="lead">Jogo contra uma estimativa de validade sem geladeira (ambiente fresco a porão), em horas de mundo, e quanto isso dura em tempo real. Só os números de geladeira (carne, aves, ovos) têm fonte: [Minnesota Department of Health](https://www.health.mn.gov/people/foodsafety/store/cold.html) (carne de boi, porco e cordeiro 3 a 5 dias a 4 °C; aves e carne moída 1 a 2 dias; ovos com casca 3 a 5 semanas; ovos cozidos 1 semana). O resto é conhecimento geral e deve ser conferido antes de virar regra. ^d</p>
{shelf_table}
<p class="note">Sem refrigeração, uma regra prática é que a validade cai pela metade a cada 10 °C a mais; por isso o porão fresco é a coluna mais alta e o verão, a mais baixa. ^d</p>

<h2 id="dia">Hora de mundo de 5 ou 6 minutos: o que muda</h2>
<h3>Se só o dia mudar</h3>
<p class="lead">Nenhum parâmetro muda, só o relógio. Tempo real de cada duração em tempo de mundo. ^d</p>
{scen_table}
<h3>Se a cadência em tempo real de hoje for mantida</h3>
<p class="lead">Para a fome voltar no mesmo tempo real com o dia mais longo, a digestão sobe na proporção do dia. O custo é gastar mais energia por dia de mundo (x1,25 ou x1,5), o que afasta o jogo da realidade por dia. ^d</p>
{keep_table}
<h3>Outras mecânicas</h3>
{mech_table}

{SIX}
<h2 id="medir">Medido no jogo (10 out 2026)</h2>
<p class="lead">Execução única na réplica 1.9.8 com só o mod de teste `krs_timeprobe` carregado e o save mais recente (194, o que o Continue carregaria). O jogo abriu, mediu e fechou sozinho; o menu pedia Escape e Load Game porque não mostra Continue nesta instalação. ^c</p>
{meas_table}
<p class="note">Ferramentas novas: `tools/harness/build_timeprobe.py`, `run_time_probe.ps1`, `krs_timeprobe.lua` e `krs_timeprobe_entity.lua`. O `.ps1` marca a hora real de cada linha do log. A cópia do mod foi removida da réplica depois do teste. ^c</p>

<h2 id="plano">Plano</h2>
{steps_html}

<h2 id="fontes">Fontes e limites</h2>
<ul>
<li>Parâmetros do jogo: `rpg_constants_runtime.csv` (constantes ocultas lidas no 1.9.6), `Params Reference.md` (descrições) e as tabelas `food` e `pickable_item` do 1.9.8 da réplica, só leitura.</li>
<li>Fontes externas: [FAO, cálculo de necessidades de energia](https://www.fao.org/3/y5686e/y5686e08.htm); [Wikipedia, nível de atividade física](https://en.wikipedia.org/wiki/Physical_activity_level); [Minnesota Department of Health, tabela de armazenamento](https://www.health.mn.gov/people/foodsafety/store/cold.html); [esvaziamento gástrico e apetite após uma refeição mista](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12534588/). Nenhuma foi lida por inteiro; os números citados estão nos resumos.</li>
<li>A calibração de kcal por unidade usa pesos do jogo e kcal de referência de memória; o intervalo é largo de propósito.</li>
<li>Não há medição no jogo: nem do dia, nem do efeito de mudar a razão, nem da fome em jogo.</li>
</ul>
<footer>Gerado por <code>tools/build_gluttony_base.py</code> a partir do jogo 1.9.8 da réplica e de <code>modules/krs_items</code>.</footer>
</main>
<script>{JS}</script>
"""
page = re.sub(r"`([^`<]+)`", r"<code>\1</code>", page)
page = re.sub(r"\[([^\]]+)\]\((https?://[^)]+)\)", r'<a href="\2" target="_blank" rel="noopener">\1</a>', page)
page = re.sub(r"\s*\^([cdn])\b", lambda m: f' <span class="cf cf-{m.group(1)}" title="{esc(CONF[m.group(1)][0])}: {esc(CONF[m.group(1)][1])}">{CONF[m.group(1)][0]}</span>', page)
out = os.path.join(OUTDIR, "ANALISE_BASE.html")
open(out, "w", encoding="utf-8", newline="\n").write(page)
print("wrote", out, len(page), "bytes; kcal/unit", round(K_LO), round(K_MED), round(K_HI), "BMR", round(BMR))
