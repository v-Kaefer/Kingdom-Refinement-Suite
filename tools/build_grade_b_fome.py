"""Hunger, digestion and time: the base parameters (reference sheet for the spoilage / nutrition fine tuning).

Reads docs/engine/rpg_constants_runtime.csv (hidden constants read in game 1.9.6), Mods WIP folder/Params Reference.md (descriptions),
the unmodified game's tables (rpg_param, buff, food, food_type) and modules/krs_items (our values).
Writes docs/mods-review/GRADE_B_FOME.html. Nothing is run and nothing outside docs/ is written.
Run: python tools/build_grade_b_fome.py
"""
import collections
import csv
import html
import os
import re
import statistics as st
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
R = os.path.join(ROOT, "docs", "mods-review")
GAME = os.environ.get("KCD_GAME", r"E:\Kingdom-Refinement-Suite\WIP_Mods\KingdomComeDeliverance")
sys.path.insert(0, HERE)
import audit_tables as at          # noqa: E402
import grade_b_page_style as S     # noqa: E402

CONF = {"c": ("confirmado", "lido nos arquivos, no jogo ou no log"), "d": ("deduzido", "inferido do nome, da ajuda ou do contexto"), "n": ("não verificado", "precisa de teste no jogo")}


def esc(t):
    return html.escape(str(t), quote=False)


def rich(t):
    t = esc(t)
    t = re.sub(r"`([^`]+)`", r"<code>\1</code>", t)
    t = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", t)
    return re.sub(r"\s*\^([cdn])\b", lambda m: f' <span class="cf cf-{m.group(1)}" title="{esc(CONF[m.group(1)][0])}: {esc(CONF[m.group(1)][1])}">{CONF[m.group(1)][0]}</span>', t)


def num(x, nd=2):
    if abs(x - round(x)) < 1e-9:
        return str(int(round(x)))
    return f"{x:.{nd}f}".rstrip("0").rstrip(".").replace(".", ",")


def table(head, rows, cls="t compact", nums=()):
    th = "".join(f"<th>{esc(h)}</th>" for h in head)
    body = ""
    for r in rows:
        body += "<tr>" + "".join(f'<td class="{"num" if i in nums else ""}">{c if str(c).startswith("<") else rich(c)}</td>' for i, c in enumerate(r)) + "</tr>"
    return f'<div class="scroll"><table class="{cls}"><thead><tr>{th}</tr></thead><tbody>{body}</tbody></table></div>'


# ---------------------------------------------------------------- data
RUNTIME = {r["key"]: r for r in csv.DictReader(open(os.path.join(ROOT, "docs", "engine", "rpg_constants_runtime.csv"), encoding="utf-8"))}
T = at.load_vanilla(GAME)
VAN_PARAM = {r["rpg_param_key"]: r["rpg_param_value"] for r in T["rpg_param"]["rows"]}
KRS = dict(re.findall(r'rpg_param_key="([A-Za-z]+)" rpg_param_value="([^"]*)"', open(os.path.join(ROOT, "modules", "krs_items", "Data", "Libs", "Tables", "rpg", "rpg_param__krs_items.xml"), encoding="utf-8").read()))
DESC = {}
for line in open(os.path.join(ROOT, "Mods WIP folder", "Params Reference.md"), encoding="utf-8"):
    m = re.match(r"^([A-Za-z0-9_]+)\s+\*\s*(.*)$", line.rstrip())
    if m:
        DESC[m.group(1)] = m.group(2).strip()


def rt(k):
    v = RUNTIME[k]["runtime_value"]
    return float(v) if v != "" else None


DIG = rt("DigestionSpeed")
DIG_KRS = float(KRS["DigestionSpeed"])
FULL = rt("FoodFull")
OVER = rt("FoodOverEat")
THR = rt("StarvationThreshold")
HUGE = rt("StarvationHugeThreshold")
EXTR = rt("StarvationExtremeThreshold")
DAY = 86400.0


def hours(units, rate):
    """world hours that `units` of food last at `rate` units per world second"""
    return units / rate / 3600.0


# checks of the unit claim: SleepHealthRegenBaseSpeed is documented as "full regen after 8 world-time hours"
sleep_check = rt("SleepHealthRegenBaseSpeed") * 8 * 3600
assert abs(sleep_check - 100) < 0.5, sleep_check
assert abs(rt("ExhaustionSpeed") - DIG) < 1e-12

# ---------------------------------------------------------------- tables
PARAMS = [
    ("DigestionSpeed", "ritmo base da fome", "unidades de fome por segundo de mundo", "oculta (não está na tabela `rpg_param`); o KRS Items a define por linha de patch"),
    ("ExhaustionSpeed", "ritmo base do cansaço (energia/vigor de longo prazo)", "unidades por segundo de mundo", "oculta"),
    ("FoodFull", "valor de 'cheio'", "unidades da barra de fome", "oculta"),
    ("FoodOverEat", "teto absoluto ao comer: acima disso não se come mais", "unidades da barra de fome", "oculta"),
    ("StarvationThreshold", "abaixo disto o jogador está 'com fome' (começam os efeitos)", "unidades da barra de fome", "oculta"),
    ("StarvationHugeThreshold", "abaixo disto, fome grande", "unidades da barra de fome", "oculta"),
    ("StarvationExtremeThreshold", "abaixo disto (0), inanição", "unidades da barra de fome", "oculta"),
    ("StarvationHealthLossSpeed", "perda de vida por inanição ('por desenho, igual à digestão')", "unidade de vida por segundo, não verificada", "tabela"),
    ("ShortTermNutritionDigestionSpeedMultiplier", "a parte 'de curto prazo' de uma comida digere neste múltiplo do ritmo base", "multiplicador", "oculta"),
    ("StarvationPlayerEffectMinMin", "menor intervalo entre efeitos de fome, fome baixa", "unidade não verificada (segundos?)", "tabela"),
    ("StarvationPlayerEffectMaxMin", "maior intervalo, fome baixa", "idem", "tabela"),
    ("StarvationPlayerEffectMinMax", "menor intervalo, fome alta", "idem", "tabela"),
    ("StarvationPlayerEffectMaxMax", "maior intervalo, fome alta", "idem", "tabela"),
    ("FoodHealSpeed", "regeneração de vida da comida que cura", "unidade não verificada", "tabela"),
    ("FoodHealthThreshold", "limiar de vida entre efeito positivo e negativo da comida", "fração", "oculta"),
    ("FoodPoisoningThreshold", "desvio do início dos efeitos de intoxicação", "fração", "tabela"),
    ("FoodPoisoningMinHealthEffectSpeed", "perda mínima de vida por intoxicação", "por segundo", "oculta"),
    ("FoodPoisoningMaxHealthEffectSpeed", "perda máxima de vida por intoxicação", "por segundo", "oculta"),
    ("MetabolismDigestSpeed", "digestão de álcool e veneno", "unidades por segundo de mundo", "tabela"),
    ("MetabolismAbsorbSpeed", "absorção (remoção) de álcool e veneno", "unidades por segundo de mundo", "tabela"),
    ("SleepHealthRegenBaseSpeed", "regeneração de vida ao dormir ('cheia em 8 horas de mundo')", "unidades por segundo de mundo", "oculta"),
    ("FoodWitcherPerkNutritionModif", "fator de nutrição com a perk de bruxo", "multiplicador", "oculta"),
    ("FoodSaltOrSmokePerkDecayModif", "fator de apodrecimento com a perk de sal/defumação", "multiplicador", "oculta"),
    ("PerkProperDietActivationTime", "tempo de dieta para a perk 'Proper diet' ativar", "unidade não verificada", "oculta"),
    ("DefaultWorldTimeRatio", "razão de tempo 'padrão' usada no avanço rápido do tempo (não é necessariamente o ritmo normal)", "segundos de mundo por segundo real", "oculta"),
]
rows = []
for k, what, unit, where in PARAMS:
    cur = RUNTIME.get(k, {}).get("runtime_value", "")
    van = VAN_PARAM.get(k, "-")
    rows.append([f"`{k}`", what, unit, num(float(cur), 9) if cur != "" else "sem valor", van, num(float(KRS[k]), 9) if k in KRS else "-", where])
param_table = table(["Parâmetro", "O que faz", "Unidade", "Valor lido no jogo (1.9.6)", "Tabela do 1.9.8", "KRS Items", "Onde fica"], rows, nums=(3, 4, 5))
param_table = param_table.replace("<td class=\"num\">-</td>", "<td class=\"num\">-</td>")

# state table: hours from FULL
STATES = [("Cheio (100) → com fome (50)", FULL - THR), ("Cheio → fome grande (25)", FULL - HUGE), ("Cheio → inanição (0)", FULL - EXTR), ("Empanturrado (120) → com fome (50)", OVER - THR)]
state_rows = []
for lab, units in STATES:
    hv, hk = hours(units, DIG), hours(units, DIG_KRS)
    state_rows.append([lab, num(units), num(hv, 1) + " h", f'<span data-w="{hv:.4f}"></span>', num(hk, 1) + " h", f'<span data-w="{hk:.4f}"></span>'])
state_table = table(["Do estado ao estado", "Unidades", "Jogo (mundo)", "Jogo (tempo real)", "KRS Items (mundo)", "KRS Items (tempo real)"], state_rows, nums=(1, 2, 4))

# target table
tg_rows = []
for t in (3, 4, 6, 8, 12, 24):
    rate = (FULL - THR) / (t * 3600.0)
    tg_rows.append([f"{t} h", f"{rate:.6f}".replace(".", ","), num(rate / DIG, 2) + "x", num(rate / DIG_KRS, 2) + "x", f'<span data-w="{t}"></span>', num(2 * t) + " h"])
target_table = table(["Cheio → com fome em (mundo)", "`DigestionSpeed` necessário", "vs jogo", "vs KRS Items", "Em tempo real", "Cheio → inanição (mundo)"], tg_rows, nums=(1, 2, 3, 5))

# modifiers (buff codes)
buff = {r["buff_name"]: r for r in T["buff"]["rows"]}
MODS = [("perk_ascetic_digestion", "perk Ascetic"), ("perk_ascetic_digestion_hardcore", "perk Ascetic (Hardcore)"), ("HC perk Tapeworm", "perk Tapeworm (Hardcore)"), ("good_appetite", "buff Good appetite"),
        ("perk_reading_regen_improved", "ler com a perk de leitura melhorada"), ("perk_contemplative", "perk Contemplative (parado)"), ("healthEatSleep", "comer/dormir forçado"),
        ("forced_skiptime_protection", "proteção em avanço de tempo forçado"), ("jail", "prisão")]
mod_rows = []
for k, lab in MODS:
    b = buff.get(k)
    if b:
        mod_rows.append([lab + " ^d", f"`{b['buff_name']}`", f"`{b['params']}`", "permanente" if b["duration"] == "-1" else b["duration"] + " s"])
mod_table = table(["Efeito", "Buff no jogo", "Parâmetros", "Duração"], mod_rows)

# food rows
F = T["food"]["rows"]
ftype = {r["food_type_id"]: r["food_type_name"] for r in T["food_type"]["rows"]}
by_t = collections.defaultdict(list)
for r in F:
    by_t[r["food_type_id"]].append(r)
frows = []
NAMES_PT = {"fruit": "fruta", "meat": "carne", "drink": "bebida e poção", "bowel": "miúdos", "vegetable": "verdura", "mushroom": "cogumelo", "pastry": "pão e massa", "dairy": "laticínio e ovo"}
for tid in sorted(by_t, key=lambda x: (x == "", x)):
    rs = by_t[tid]
    nn = [float(r["nutrition_benefit"]) for r in rs if r["nutrition_benefit"] != ""]
    ms = [float(r["max_status"]) for r in rs if r["max_status"] != ""]
    frows.append([f"{NAMES_PT.get(ftype.get(tid, ''), 'sem tipo')} ({ftype.get(tid, '-')})", str(len(rs)), f"{num(min(nn))} a {num(max(nn))} (mediana {num(st.median(nn))})" if nn else "-",
                  f"{num(st.median(ms))}" if ms else "-"])
food_table = table(["Tipo (`food_type`)", "Itens", "`nutrition_benefit`", "`max_status` (mediana)"], frows, nums=(1,))

byname = {}
for r in F:
    byname[r["item_id"]] = r
ex = []
for iid, r in byname.items():
    pass
# a few named examples
G_names = {}
try:
    sys.path.insert(0, HERE)
    import grade_b_extract as gx
    G = gx.Game()
    for r in F:
        G_names[re.sub(r"\s*\[[0-9a-f]{8}\]$", "", G.label(r["item_id"]))] = r
except Exception:
    G_names = {}
EXAMPLES = ["Bread", "Beef_cooked", "Rabbit meat cooked", "Smoked Rabbit meat", "Salami_01", "lentil_soup", "Cheese quarter", "hardboiled_egg", "Apple", "carrot cooked", "water"]
ex_rows = []
for n in EXAMPLES:
    r = G_names.get(n)
    if not r:
        continue
    nu = float(r["nutrition_benefit"] or 0)
    ex_rows.append([n, num(nu), r["max_status"] or "-", r["short_term_nutrition_benefit_ratio"] or "-", num(hours(nu, DIG), 1) + " h", num(hours(nu, DIG_KRS), 1) + " h"])
ex_table = table(["Item", "`nutrition_benefit`", "`max_status`", "Parte de curto prazo", "Horas de fome no jogo", "No KRS Items"], ex_rows, nums=(1, 2, 3, 4, 5))

# ---------------------------------------------------------------- page
FIND = [
    ("A unidade é segundo de mundo, não segundo real", f"`DigestionSpeed` = {DIG:.9f} é igual a `ExhaustionSpeed`, e a ajuda do jogo diz que a regeneração de sono (`SleepHealthRegenBaseSpeed` = {rt('SleepHealthRegenBaseSpeed'):.8f}) enche em 8 horas 'de mundo': {num(rt('SleepHealthRegenBaseSpeed') * 8 * 3600)} unidades em 8 h. Com a mesma conta, a fome vai de 100 a 0 em 48 horas de mundo. Isso não depende da razão entre tempo real e tempo de jogo. ^d"),
    ("Do jogo: com fome em 24 h, inanição em 48 h", f"Cheio (100) chega a 50 ('com fome') em {num(hours(FULL - THR, DIG), 1)} h de mundo, a 25 em {num(hours(FULL - HUGE, DIG), 1)} h e a 0 em {num(hours(FULL - EXTR, DIG), 1)} h. Com o KRS Items (x2,25): {num(hours(FULL - THR, DIG_KRS), 1)}, {num(hours(FULL - HUGE, DIG_KRS), 1)} e {num(hours(FULL - EXTR, DIG_KRS), 1)} h. ^d"),
    ("A razão de tempo real não está nos dados", "O jogo a guarda no motor: o script de depuração do jogador só lê e grava `Calendar.GetWorldTimeRatio()` (e põe 600 no 'tempo rápido'), e a constante `DefaultWorldTimeRatio` vale 15 mas é descrita como base do avanço rápido. Os tempos reais da página usam o seu 1:360 e podem ser trocados no campo abaixo. Para confirmar, basta cronometrar quantos segundos reais dura uma hora do relógio do jogo. ^n"),
    ("'Com fome a cada 3 horas' é 8 vezes o ritmo do jogo", f"Para ficar com fome 3 horas de mundo depois de cheio, a digestão teria de ser {num(((FULL - THR) / (3 * 3600)) / DIG, 1)}x a do jogo ({num(((FULL - THR) / (3 * 3600)) / DIG_KRS, 1)}x a do KRS Items). A tabela de metas mostra o valor de `DigestionSpeed` para cada intervalo. ^d"),
]
fhtml = "".join(f'<div class="find"><h3>{esc(t)}</h3><p>{rich(d)}</p></div>' for t, d in FIND)

JS = r"""
(function(){
  var inp=document.getElementById('ratio');
  function fmt(s){ if(s<90) return Math.round(s)+' s'; if(s<5400) return (s/60).toFixed(1).replace('.',',')+' min'; return (s/3600).toFixed(1).replace('.',',')+' h'; }
  function upd(){
    var r=parseFloat((inp.value||'').replace(',','.')); if(!(r>0)) r=360;
    [].slice.call(document.querySelectorAll('[data-w]')).forEach(function(e){ e.textContent=fmt(parseFloat(e.dataset.w)*3600/r); });
    document.getElementById('ratio-day').textContent=fmt(86400/r);
  }
  inp.addEventListener('input',upd); upd();
})();
"""

nav = "".join(f'<a href="#{i}">{t}</a>' for i, t in (("resumo", "Resumo"), ("relogio", "Relógio"), ("parametros", "Parâmetros"), ("estados", "Tempo até a fome"), ("metas", "Metas"), ("modificadores", "Modificadores"), ("comidas", "Comida"), ("limites", "Limites")))
page = f"""<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Fome, digestão e tempo</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=IBM+Plex+Sans+Condensed:wght@500;600&family=IBM+Plex+Sans:wght@400;500;600&display=swap">
<style>{S.CSS}
.ratio{{display:flex;gap:10px;align-items:center;flex-wrap:wrap;background:var(--surface);border:1px solid var(--line);border-radius:4px;padding:10px 14px;margin:12px 0}}
.ratio input{{font:inherit;width:6rem;padding:4px 6px;background:var(--bg);color:var(--ink);border:1px solid var(--line);border-radius:3px}}
</style>
<div class="top"><b>Fome e tempo</b><nav>{nav}</nav></div>
<main>
<header>
<h1>Fome, digestão e tempo: os parâmetros de base</h1>
<p class="lead">Folha de referência para o ajuste fino de apodrecimento e nutrição. Reúne o relógio, o ritmo da fome, os limiares, os modificadores e os valores de comida, com o que o jogo traz e o que o KRS Items já muda. Só leitura: nada foi executado e nenhuma regra nova foi escolhida.</p>
<p class="legend"><span><span class="cf cf-c">confirmado</span> lido nos arquivos</span><span><span class="cf cf-d">deduzido</span> inferido</span><span><span class="cf cf-n">não verificado</span> precisa de teste</span></p>
</header>

<h2 id="resumo">Resumo</h2>
<div class="cols">{fhtml}</div>

<h2 id="relogio">Relógio: segundos de mundo e tempo real</h2>
<div class="ratio"><label for="ratio"><b>Segundos de mundo por segundo real</b> (o seu 1:360)</label><input id="ratio" type="text" inputmode="decimal" value="360"><span>Um dia de mundo dura <b id="ratio-day"></b> de tempo real.</span></div>
<p class="note">Todos os valores de tempo real das tabelas abaixo se recalculam com esse campo. A razão em si não está nos dados do jogo (ver o resumo). ^n</p>

<h2 id="parametros">Parâmetros de base</h2>
<p class="lead">Valor lido no jogo 1.9.6 (constantes ocultas, `rpg_constants_runtime.csv`), valor na tabela `rpg_param` do 1.9.8 quando existe, e o que o KRS Items já define. ^c</p>
{param_table}
<p class="note">`FoodTickInterval` aparece na referência de parâmetros, mas o motor 1.9.6 não a tem; não use. As descrições vêm de `Params Reference.md`; as unidades de vários limiares de efeito (StarvationPlayerEffect*) não estão documentadas. ^c</p>

<h2 id="estados">Quanto tempo leva até a fome</h2>
<p class="lead">Sem comer nada, a 100% de saciedade. A coluna em tempo real segue o campo do relógio acima. ^d</p>
{state_table}

<h2 id="metas">Metas: que `DigestionSpeed` dá 'fome a cada N horas'</h2>
<p class="lead">Conta direta: (100 − 50) unidades divididas pelas horas de mundo desejadas. O jogo está em 24 h e o KRS Items em 10,7 h. Isto é aritmética, não recomendação. ^d</p>
{target_table}

<h2 id="modificadores">Modificadores do ritmo (`dig`) e do cansaço (`exh`)</h2>
<p class="lead">No jogo, buffs multiplicam a digestão (`dig*x`) e o cansaço (`exh*x`); `dig*0` pausa a fome. Os parâmetros são lidos da tabela `buff`; o significado de `dig` é deduzido do nome dos buffs. ^d</p>
{mod_table}

<h2 id="comidas">Cada comida: quanto sacia</h2>
<p class="lead">O ganho de uma comida está em três colunas da tabela `food`: `nutrition_benefit` (quanto sobe a barra), `short_term_nutrition_benefit_ratio` (parte que digere {num(rt('ShortTermNutritionDigestionSpeedMultiplier'))}x mais rápido) e `max_status` (significado não verificado: a leitura como teto da barra não fecha, porque a carne assada tem 40, abaixo do limiar de fome de 50). ^n</p>
{food_table}
<h3>Exemplos, em horas de fome</h3>
<p class="note">Horas = nutrição ÷ ritmo. Ignora a parte de curto prazo, então é ordem de grandeza. ^d</p>
{ex_table}

<h2 id="limites">Limites</h2>
<ul>
<li>A razão entre tempo real e tempo de mundo não consta nos dados lidos; o valor 360 é o seu. As conversões são aritmética sobre os parâmetros.</li>
<li>O mecanismo exato da parte de curto prazo, o significado de `max_status` e as unidades dos efeitos de inanição vêm de nomes e da ajuda do jogo, sem teste.</li>
<li>Os valores 'do jogo' vêm da leitura de 1.9.6; no 1.9.8 o binário mudou e as constantes ocultas podem ter mudado.</li>
</ul>
<footer>Gerado por <code>tools/build_grade_b_fome.py</code> a partir de <code>docs/engine/rpg_constants_runtime.csv</code>, <code>Params Reference.md</code>, as tabelas do jogo e <code>modules/krs_items</code>.</footer>
</main>
<script>{JS}</script>
"""
page = re.sub(r"`([^`<]+)`", r"<code>\1</code>", page)
out = os.path.join(R, "GRADE_B_FOME.html")
open(out, "w", encoding="utf-8", newline="\n").write(page)
print("wrote", out, len(page), "bytes")
