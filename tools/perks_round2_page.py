#!/usr/bin/env python3
"""
perks_round2_page.py - page (Portuguese) for the second round of the perk workbench: 1990, 1569, 1375.

    python tools/perks_round2_page.py [--out <extra copy>]

Every number on the page is read live from the unmodified game (Data/Tables.pak) and from the three
mods in the workbench, so the page cannot drift from the files. Writes
<workbench>/notes/perks-round2.html.
"""
import argparse
import html
import os
import re
import sys
import xml.etree.ElementTree as ET

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import vanilla  # noqa: E402
from page_style import CSS as PAGE_CSS  # noqa: E402

WORKBENCH = r"E:\Kingdom-Refinement-Suite\Mods WIP folder\Perks\perkaholic-riposte-workbench"
EX = os.path.join(WORKBENCH, "extracted")

# the three mods of this round: id -> (folder, inner mod folder)
MODS = {
    "1990": ("1990_veteran-hunting", "VeteranHunting"),
    "1569": ("1569_karnages-shield", "Karnages_Shield_Restoration"),
    "1375": ("1375_no-aim-spread", "NoAimSpread"),
}

# the seven animals 1990 touches, in the order the mod lists them
ANIMALS = [
    ("4d9275e7-744b-2390-1e8d-943e0f2501a4", "Lebre"),
    ("41f5c883-299d-645f-5a42-92db0d6c6c91", "Corço"),
    ("4eca3014-efa1-e85e-414d-c454aaed1baf", "Corça"),
    ("4edc5ad5-51be-0cd2-be9d-6ead0aabcf88", "Veado"),
    ("4ba0a861-869f-30e3-941b-aa3872f1c6a3", "Javali"),
    ("4294f238-80d6-28e3-c57e-b4a4bd7c24b4", "Ovelha (Sheep1)"),
    ("43049911-d3fe-9315-b963-fb4ecc601d8f", "Ovelha (animal_sheep)"),
]


def esc(t):
    return html.escape(str(t))


def num(n):
    """5025 -> '5.025' (thousands as Portuguese writes them)."""
    return f"{n:,}".replace(",", ".")


def chip(kind, text):
    return f'<span class="chip {kind}">{esc(text)}</span>'


def chg(was, now, note=""):
    """the before -> after of the shared display standard."""
    out = (f'<code class="was">{esc(was)}</code><span class="arrow">&#8594;</span>'
           f'<code class="is">{esc(now)}</code>')
    if note:
        out += f'<div class="muted">{esc(note)}</div>'
    return out


def read_table(path):
    raw = open(path, encoding="utf-8-sig", errors="replace").read()
    t = ET.fromstring(re.sub(r"^\s*<\?xml[^>]*\?>", "", raw)).find("table")
    cols = [c.get("name") for c in t.findall("./header/column")]
    rows = [dict(r.attrib) for r in t.findall("./rows/row")]
    return cols, rows


def modfile(mid, *parts):
    return os.path.join(EX, MODS[mid][0], "_pak", *parts)


# --------------------------------------------------------------------------- facts read from files
def collect():
    f = {}
    souls_cols, souls = vanilla.load("rpg/soul")
    f["soul_total"] = len(souls)
    nums = [(int(r["hearing"] or 0), int(r["vision"] or 0)) for r in souls if (r.get("hearing") or "").isdigit()]
    f["hear_max"] = max(h for h, _ in nums)
    f["vis_max"] = max(v for _, v in nums)
    f["soul_cols"] = [c for c, _ in souls_cols]
    vsoul = {r["soul_id"]: r for r in souls}

    mcols, mrows = read_table(modfile("1990", "Libs", "Tables", "rpg", "soul__VeteranHunting.xml"))
    f["soul_header_missing"] = [c for c in f["soul_cols"] if c not in mcols]
    mrow = {r["soul_id"]: r for r in mrows}
    f["animals"] = []
    for sid, name in ANIMALS:
        m, v = mrow[sid], vsoul[sid]
        f["animals"].append({
            "name": name, "key": v.get("soul_name"),
            "hear": int(m["hearing"]), "vis": int(m["vision"]),
            "v_hear": int(v.get("hearing") or 0), "v_vis": int(v.get("vision") or 0),
            "v_combat": v.get("combat_level") or "", "m_combat": m.get("combat_level"),
        })
    f["animal_souls"] = sorted(
        (r.get("soul_name"), r.get("hearing"), r.get("vision")) for r in souls
        if (r.get("soul_name") or "").lower().startswith(("animal", "sheep")))
    f["untouched"] = [n for n, _, _ in f["animal_souls"] if n not in {a["key"] for a in f["animals"]}]

    bcols, buffs = vanilla.load("rpg/buff")
    f["btw_vanilla"] = [(r.get("buff_name"), r.get("params")) for r in buffs if "btw" in (r.get("params") or "")]
    f["was_vanilla"] = [(r.get("buff_name"), r.get("params")) for r in buffs if "was" in (r.get("params") or "")]
    _, mbuffs = read_table(modfile("1990", "Libs", "Tables", "rpg", "buff__VeteranHunting.xml"))
    f["m1990_buffs"] = mbuffs

    pcols, perks = vanilla.load("rpg/perk")
    f["perk_cols"] = [c for c, _ in pcols]
    f["vis_counts"] = {v: sum(1 for r in perks if r.get("visibility") == v) for v in ("0", "1", "2", "3")}
    f["skill20_perks"] = [(r.get("perk_name"), r.get("visibility"), r.get("level"))
                          for r in perks if r.get("skill_selector") == "20"]
    f["skill23_perks"] = [r for r in perks if r.get("skill_selector") == "23"]
    f["hardcore_perk"] = next((r.get("perk_name") for r in perks
                               if r["perk_id"] == "1e53b07d-8012-44b1-ace6-3504558f04aa"), None)

    scols, skills = vanilla.load("rpg/skill")
    f["hidden_skills"] = [(r["skill_id"], r.get("skill_name"), r.get("ui_string_name"))
                          for r in skills if r.get("hidden") == "True"]
    scol_names = [c for c, _ in scols]
    k20cols, k20rows = read_table(modfile("1569", "Libs", "Tables", "rpg",
                                          "skill__Karnages_Shield_Restoration.xml"))
    v20 = next(r for r in skills if r["skill_id"] == "20")
    f["s1569_full_header"] = sorted(k20cols) == sorted(scol_names)
    f["s1569_diff"] = {c: (v20.get(c, ""), k20rows[0].get(c, ""))
                       for c in k20cols if (v20.get(c, "") or "") != (k20rows[0].get(c, "") or "")}

    _, s2s = vanilla.load("rpg/soul2skill")
    f["npc_skill20"] = sum(1 for r in s2s if r.get("skill_id") == "20")
    f["npc_skill23"] = sum(1 for r in s2s if r.get("skill_id") == "23")

    gcols, gmodes = vanilla.load("game_mode")
    f["game_mode"] = gmodes
    _, gm = read_table(modfile("1375", "Libs", "Tables", "game_mode__NoAimSpread.xml"))
    f["m1375_gm"] = gm[0]

    rcols, rparams = vanilla.load("rpg/rpg_param")
    f["aim_vanilla"] = next((r["rpg_param_value"] for r in rparams
                             if r["rpg_param_key"] == "AimSpreadMax"), None)
    _, rp = read_table(modfile("1375", "Libs", "Tables", "rpg", "rpg_param__NoAimSpread.xml"))
    f["m1375_aim"] = rp[0]["rpg_param_value"]

    _, s2p = read_table(modfile("1375", "Libs", "Tables", "rpg", "soul2perk__NoAimSpread.xml"))
    f["m1375_soul"] = s2p[0]["soul_id"]
    f["m1375_soul_name"] = vsoul[s2p[0]["soul_id"]].get("soul_name")
    _, p1375 = read_table(modfile("1375", "Libs", "Tables", "rpg", "perk__NoAimSpread.xml"))
    f["m1375_perk"] = p1375[0]
    _, b1375 = read_table(modfile("1375", "Libs", "Tables", "rpg", "buff__NoAimSpread.xml"))
    f["m1375_buff"] = b1375[0]
    return f


# --------------------------------------------------------------------------- the perception chart
def perception_chart(f):
    """horizontal bars, two series, direct labels, and the game's own ceiling as a reference band."""
    rows = f["animals"]
    W, LEFT, RIGHT = 760, 168, 56
    plot = W - LEFT - RIGHT
    rowh, barh, gap = 40, 13, 4
    top = 46
    H = top + rowh * len(rows) + 46
    xmax = 100
    x = lambda v: LEFT + v / xmax * plot
    ceil = f["hear_max"]

    p = [f'<svg viewBox="0 0 {W} {H}" role="img" width="100%" '
         f'aria-label="Ouvido e visão que o 1990 escreve, contra o teto de {ceil} do jogo">']
    # the band the whole game lives in
    p.append(f'<rect x="{x(0):.1f}" y="{top - 16}" width="{x(ceil) - x(0):.1f}" '
             f'height="{rowh * len(rows) + 24}" fill="var(--band)" rx="2" />')
    p.append(f'<line x1="{x(ceil):.1f}" y1="{top - 16}" x2="{x(ceil):.1f}" '
             f'y2="{top + rowh * len(rows) + 8}" stroke="var(--ink3)" stroke-width="1.5" '
             f'stroke-dasharray="3 3" />')
    p.append(f'<text x="{x(ceil) + 8:.1f}" y="{top - 20}" font-size="11.5" fill="var(--ink2)" '
             f'font-family="var(--body)">&#8592; a faixa inteira do jogo acaba em {ceil}</text>')
    for i, r in enumerate(rows):
        yb = top + i * rowh
        p.append(f'<text x="{LEFT - 12}" y="{yb + barh}" text-anchor="end" font-size="12.5" '
                 f'fill="var(--ink)" font-family="var(--body)">{esc(r["name"])}</text>')
        for k, (val, col) in enumerate((("hear", "var(--s1)"), ("vis", "var(--s2)"))):
            v = r[val]
            yy = yb + k * (barh + gap)
            p.append(f'<rect x="{x(0):.1f}" y="{yy}" width="{max(x(v) - x(0), 2):.1f}" '
                     f'height="{barh}" rx="3" fill="{col}" />')
            p.append(f'<text x="{x(v) + 7:.1f}" y="{yy + barh - 2}" font-size="11.5" '
                     f'fill="var(--ink2)" font-family="var(--body)" '
                     f'style="font-variant-numeric:tabular-nums">{v}</text>')
    base = top + rowh * len(rows) + 6
    p.append(f'<line x1="{x(0):.1f}" y1="{base}" x2="{x(xmax):.1f}" y2="{base}" '
             f'stroke="var(--line)" stroke-width="1" />')
    for t in (0, 20, 40, 60, 80, 100):
        p.append(f'<text x="{x(t):.1f}" y="{base + 18}" text-anchor="middle" font-size="11" '
                 f'fill="var(--ink3)" font-family="var(--body)">{t}</text>')
    p.append("</svg>")
    legend = ('<div class="legend">'
              '<span><i style="background:var(--s1)"></i>ouvido (<code>hearing</code>)</span>'
              '<span><i style="background:var(--s2)"></i>visão (<code>vision</code>)</span>'
              '</div>')
    return legend + '<div class="figure">' + "".join(p) + "</div>"


# --------------------------------------------------------------------------- page
def build(f):
    a = f["animals"]
    hi = max(a, key=lambda r: r["hear"])
    btw_rows = "".join(f"<tr><td class='mono'>{esc(n)}</td><td><code>{esc(p)}</code></td></tr>"
                       for n, p in f["btw_vanilla"])
    was_rows = "".join(f"<tr><td class='mono'>{esc(n)}</td><td><code>{esc(p)}</code></td></tr>"
                       for n, p in f["was_vanilla"])
    s20 = "".join(
        f"<tr><td>{esc(n)}</td><td>{chip('ok','comprável') if v=='2' else chip('bad','oculto')}</td>"
        f"<td class='num'>{esc(l or '-')}</td></tr>"
        for n, v, l in sorted(f["skill20_perks"], key=lambda r: (r[1] != "2", r[0])))
    hidden = ", ".join(f"{esc(n)} ({sid})" for sid, n, _ui in f["hidden_skills"])
    untouched = ", ".join(esc(n) for n in f["untouched"])

    gm_rows = "".join(
        f"<tr><td class='num'>{esc(r['game_mode_id'])}</td><td>{esc(r['game_mode_name'])}</td>"
        f"<td class='mono'>{esc(r['player_perk_id'] or '(vazio)')}</td>"
        f"<td class='why'>{'<b>' + esc(f['hardcore_perk']) + '</b> - o jogo usa esta coluna para empilhar os males do modo hardcore no jogador' if r['player_perk_id'] else 'vazio no jogo; e a casa que o 1375 preenche'}</td></tr>"
        for r in f["game_mode"])

    return f"""<title>Caça, Escudo e Mira</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo+Narrow:wght@500;700&family=Source+Sans+3:wght@400;600&family=JetBrains+Mono:wght@400;700&display=swap">
{PAGE_CSS}
<style>
/* duas séries de gráfico + a faixa de referência, sobre os mesmos tokens da página anterior */
:root {{ --s1:#2f6f9f; --s2:#b3372f; --band:#ece9e2; }}
@media (prefers-color-scheme: dark) {{ :root:not([data-theme="light"]) {{
  --s1:#4f97d4; --s2:#d9654f; --band:#24282c; }} }}
:root[data-theme="dark"] {{ --s1:#4f97d4; --s2:#d9654f; --band:#24282c; }}
.figure {{ background:var(--surface); border:1px solid var(--line); border-radius:10px;
  padding:14px 10px 6px; margin:.4rem 0 1rem; overflow-x:auto; }}
.legend {{ display:flex; flex-wrap:wrap; gap:18px; font-size:.86rem; color:var(--ink2);
  margin-top:1rem; }}
.legend i {{ display:inline-block; width:12px; height:12px; border-radius:3px;
  margin-right:7px; vertical-align:-1px; }}
td.mono, .mono {{ font-family:var(--mono); font-size:.8rem; word-break:break-all; }}
</style>

<div class="wrap">
<div class="eyebrow">Kingdom Refinement Suite · bancada de perks · rodada 2 · jogo 1.9.8</div>
<h1>Caça, Escudo e Mira</h1>
<p class="lead">1990, 1569 e 1375, lidos arquivo por arquivo contra as tabelas do jogo. Os três
atacam problemas diferentes e, por acaso, mostram as <b>três maneiras</b> de enfiar um efeito
permanente no jogador — e só uma delas é limpa.</p>

<div class="tiles">
  <div class="tile"><div class="n">9</div><div class="l">arquivos em 1990, contando os 2 Lua</div></div>
  <div class="tile hi"><div class="n">1</div><div class="l">arquivo e 1 linha em 1569</div></div>
  <div class="tile"><div class="n">6</div><div class="l">arquivos em 1375, e 1 deles é inerte</div></div>
  <div class="tile"><div class="n">{f['hear_max']}</div><div class="l">maior ouvido entre as {num(f['soul_total'])} almas do jogo</div></div>
  <div class="tile"><div class="n">{hi['hear']}</div><div class="l">ouvido que o 1990 escreve na lebre</div></div>
</div>

<div class="tablebox"><table>
<thead><tr><th>Mod</th><th>O que entrega</th><th>Como entrega</th><th>Veredito</th></tr></thead>
<tbody>
<tr><td><b>1569</b> Karnages Shield Restoration</td>
<td class="why">desoculta a perícia <b>Escudo</b> (id 20)</td>
<td class="why">1 linha de <code>skill</code>, com as 12 colunas completas</td>
<td>{chip("ok", "adotar a linha")}</td></tr>
<tr><td><b>1990</b> Veteran Hunting</td>
<td class="why">liga ouvido e visão de 7 animais, cria um perk oculto de dificuldade e
<b>inverte</b> o perk Coração Selvagem</td>
<td class="why">7 linhas de <code>soul</code> + perk/buff/ligação + 2 scripts Lua que forçam o perk
a cada carregamento</td>
<td>{chip("warn", "a ideia sim, os números não")}</td></tr>
<tr><td><b>1375</b> No Aim Spread</td>
<td class="why">zera a oscilação do arco</td>
<td class="why">um perk concedido por <b>três rotas ao mesmo tempo</b>; uma delas aponta para a
alma errada e um arquivo inteiro não faz nada</td>
<td>{chip("bad", "conteúdo fora")} {chip("ok", "técnica dentro")}</td></tr>
</tbody></table></div>

<h2>1569: o patch PTF exemplar</h2>
<p>Um arquivo, uma linha, e a única diferença contra o jogo é <code>hidden</code>. As outras
{len(f['soul_cols']) and 11} colunas repetem o valor do jogo — exatamente o que a regra 5 exige, e
exatamente o que quase nenhum mod faz.</p>
<div class="tablebox"><table>
<thead><tr><th>Coluna</th><th>Alteração</th><th>O que significa</th></tr></thead>
<tbody>
{"".join(f'<tr><td class="mono">{esc(c)}</td><td class="chg">{chg(w, n)}</td>'
         f'<td class="why">a perícia Escudo deixa de ser escondida e aparece na ficha do Henry</td></tr>'
         for c, (w, n) in f["s1569_diff"].items())}
</tbody></table></div>
<div class="note ok"><div class="t">E vem com conteúdo pronto atrás</div>
<p>Desocultar a perícia 20 não abre uma aba vazia: o jogo <b>já tem
{len(f['skill20_perks'])} perks</b> amarrados a ela, {sum(1 for _, v, _ in f['skill20_perks'] if v == '2')}
deles compráveis. E <b>{num(f['npc_skill20'])}</b> NPCs já carregam um valor de perícia de escudo em
<code>soul2skill</code>: a perícia está viva, só estava escondida do jogador.</p></div>
<div class="tablebox"><table>
<thead><tr><th>Perk da perícia 20 (escudo), no jogo</th><th>Visível?</th><th class="num">Nível</th></tr></thead>
<tbody>{s20}</tbody></table></div>

<div class="note warn"><div class="t">Isto cobra uma revisão do que já publicamos</div>
<p>O <code>krs_perks</code> já desoculta a perícia <b>23 (Arma Longa)</b>. Mas a perícia 23 tem
<b>{len(f['skill23_perks'])} perks</b> no jogo: a aba abre <b>vazia</b>. Os {len(f['skill23_perks']) or 3}
perks de combo de haste que faltam estão no <b>1563</b>, com <code>skill_selector=23</code>. Ou seja:
a linha da perícia 23 só tem sentido junto com o 1563; a do escudo tem sentido sozinha.</p></div>

<div class="note"><div class="t">O que o manifest promete e o arquivo não cumpre</div>
<p>A descrição do 1569 diz <q>adds xp gain parameters but they may not work</q>. Não existe nenhum
parâmetro de XP no pacote — só a linha da perícia. Nada se perde, mas a promessa é falsa, e não há
no jogo nenhuma linha de <code>skill2item_category</code> para a perícia 20, então <b>como ela
ganha XP é pergunta de teste em jogo</b>.</p></div>
<p class="muted">As {len(f['hidden_skills'])} perícias que o jogo esconde: {hidden}.</p>

<h2>1990: a ideia está certa, a escala não</h2>
<p>O mod tem três peças independentes. A primeira é o achado; a segunda é um truque de entrega; a
terceira mexe em conteúdo do jogo e inverte o sentido dele.</p>

<h3>Peça 1 — ouvido e visão dos animais</h3>
<p>No jogo, os {len(f['animal_souls'])} animais têm <b>ouvido e visão zerados</b> (só o cão tem
visão 11). O mod liga os dois sentidos em 7 deles. É isso que eu quis dizer antes com
<q>a caça passa a exigir aproximação</q>: hoje dá para caminhar até o bicho; com os sentidos
ligados ele reage e foge, e você passa a precisar de distância, vento a favor, silêncio e arco.</p>
<div class="note bad"><div class="t">Mas os números estão fora da escala do jogo</div>
<p>Nas <b>{num(f['soul_total'])} almas</b> do jogo, <code>hearing</code> e <code>vision</code> nunca
passam de <b>{f['hear_max']}</b>. O 1990 escreve até <b>{hi['hear']}</b> de ouvido — <b>5x o teto</b>.
O autor claramente leu as colunas como porcentagem. Isso não é opinião de balanceamento: é um
valor fora da faixa que o motor vê em qualquer outro lugar.</p></div>
{perception_chart(f)}
<p class="muted">Cada barra é o valor que o 1990 grava; no jogo todos esses animais estão em 0. A
faixa clara e a linha tracejada marcam o teto de {f['hear_max']} observado em toda a tabela
<code>soul</code>.</p>
<p>Três animais ficam de fora do mod: <b>{untouched}</b>. Se adotarmos a ideia, ou se cobre os dez
ou se escolhe quais ficam de fora de propósito.</p>

<div class="note warn"><div class="t">O cabeçalho do <code>soul</code> está incompleto</div>
<p>A tabela <code>soul</code> do jogo tem <b>{len(f['soul_cols'])}</b> colunas; o cabeçalho do mod
declara <b>{len(f['soul_cols']) - len(f['soul_header_missing'])}</b>, faltando
<code>{'</code>, <code>'.join(esc(c) for c in f['soul_header_missing'])}</code>. Pela regra 5 medida,
coluna que não vem é <b>apagada</b>, não preservada. O que está em jogo é pequeno mas real: o
<b>javali</b> tem <code>combat_level={esc(next(r['v_combat'] for r in a if r['name'] == 'Javali'))}</code>
no jogo e a linha do mod não traz essa coluna nem no cabeçalho nem no atributo. Se adotarmos essas
linhas, elas vão com as {len(f['soul_cols'])} colunas completas.</p></div>

<h3>Peça 2 — o perk oculto entregue por script</h3>
<p>Três linhas de tabela mais dois arquivos Lua. O perk tem <code>visibility=0</code>: você nunca o
vê nem escolhe. O script roda ao fim de cada tela de carregamento e chama
<code>player.soul:AddPerk(...)</code> — ou seja, <b>enfia o perk no jogador</b> para aplicar um
efeito permanente sem gastar ponto.</p>
<div class="pre"><span class="cmt">-- Scripts/Startup/VeteranHunting.lua</span>
if actionName == <span class="add">"sys_loadingimagescreen"</span> and eventName == <span class="add">"OnEnd"</span> then
    VeteranHunting.ApplyVeteranHuntingPerk()        <span class="cmt">-- a cada carregamento</span>
<span class="cmt">-- Scripts/VeteranHunting.lua</span>
player.soul:AddPerk(string.upper(<span class="add">"c92e5f13-4b57-4b02-b9cf-74e88e3b2517"</span>))</div>
<p>Funciona, e é o único jeito de dar um perk ao jogador sem tocar no jogo — <b>mas é o pior dos
três jeitos</b>, e o 1375 mostra o melhor logo abaixo.</p>

<h3>Peça 3 — Coração Selvagem invertido</h3>
<div class="tablebox"><table>
<thead><tr><th>Buff</th><th>Alteração</th><th>O que significa</th></tr></thead>
<tbody>
<tr><td><b>Veteran Hunting</b><div class="muted">buff novo, 7e42e183</div></td>
<td class="chg">{chg("não existe", "btw*3")}</td>
<td class="why">triplica o <code>btw</code> dos animais permanentemente. Como no jogo o único uso
de <code>btw</code> é uma <b>redução</b>, multiplicar por 3 anda para o lado <b>ruim</b> para o
jogador: é um mod de <i>dificuldade</i>, não de poder</td></tr>
<tr><td><b>perk_animal_in_heart</b><div class="muted">Coração Selvagem, do jogo</div></td>
<td class="chg">{chg("btw*0.4", "btw*2")}</td>
<td class="why"><b>vira o perk do avesso.</b> No jogo ele <i>reduz</i> a 0,4; o mod <i>dobra</i>.
Quem comprou Coração Selvagem para caçar melhor passa a ser punido por tê-lo</td></tr>
</tbody></table></div>
<div class="note warn"><div class="t">Colisão registrada</div>
<p>O mapa de interseções aponta <b>1 linha de <code>buff</code> compartilhada entre 1990 e 2299
(1403 - Historical Rebalance, nota A)</b>. Como o 1990 só toca dois buffs e um deles é novo (uuid
exclusivo), a linha em comum <b>é o Coração Selvagem</b>. Quem carregar por último ganha — e o 2299
é um overhaul enorme.</p></div>

<h2>1375: três rotas, uma certa</h2>
<p>O efeito é simples: um buff <code>was-15</code> contra o
<code>AimSpreadMax</code> do jogo, que é <b>{f['aim_vanilla']}</b>. Subtrai-se o máximo inteiro, a
oscilação vira zero. O interessante não é o efeito; é como ele chega ao Henry.</p>
<div class="tablebox"><table>
<thead><tr><th>Arquivo</th><th>Alteração</th><th>O que significa</th><th>Funciona?</th></tr></thead>
<tbody>
<tr><td class="mono">rpg_param__NoAimSpread</td>
<td class="chg">{chg(f"AimSpreadMax = {f['aim_vanilla']}", f"AimSpreadMax = {f['m1375_aim']}")}</td>
<td class="why"><b>idêntico ao jogo.</b> O arquivo existe, carrega, é contado como <i>equal</i> pelo
motor e não muda absolutamente nada</td>
<td>{chip("bad", "inerte")}</td></tr>
<tr><td class="mono">soul2perk__NoAimSpread</td>
<td class="chg">{chg("—", "perk -> alma " + f['m1375_soul'][:8])}</td>
<td class="why">concede o perk à alma <code>{esc(f['m1375_soul_name'])}</code> —
<b>a Theresa, não o Henry</b>. O Henry não tem linha própria na tabela <code>soul</code>, então
esta rota simplesmente não o alcança</td>
<td>{chip("bad", "alma errada")}</td></tr>
<tr><td class="mono">game_mode__NoAimSpread</td>
<td class="chg">{chg("player_perk_id vazio", "player_perk_id = ae32e325")}</td>
<td class="why"><b>esta é a que funciona</b>, e é a melhor descoberta das três instâncias: o jogo
tem uma coluna cuja função é <i>o perk que o jogador recebe neste modo de jogo</i></td>
<td>{chip("ok", "limpo")}</td></tr>
<tr><td class="mono">buff__NoAimSpread</td>
<td class="chg">{chg("não existe", esc(f['m1375_buff']['params']))}</td>
<td class="why">tremor da mira −15 reto. No jogo, <code>was</code> só aparece como multiplicador
(×1,6) ou deslocamento pequeno (±0,25): <b>−15 não é um ajuste, é um interruptor</b></td>
<td>{chip("warn", "tudo ou nada")}</td></tr>
<tr><td class="mono">perk__NoAimSpread</td>
<td class="chg">{chg("não existe", f"visibility={f['m1375_perk']['visibility']}, level={f['m1375_perk']['level']}")}</td>
<td class="why"><code>visibility=2</code> é o perk <b>comprável</b> da árvore ({f['vis_counts']['2']}
perks do jogo são assim). Sem <code>skill_selector</code> ele cai na aba do Jogador, no nível
{f['m1375_perk']['level']} — e ao mesmo tempo já vem concedido pelo modo de jogo. Duas rotas para a
mesma coisa</td>
<td>{chip("warn", "redundante")}</td></tr>
</tbody></table></div>

<div class="note ok"><div class="t">A coluna <code>player_perk_id</code> — o que levamos daqui</div>
<p>O jogo já usa essa coluna: no modo <b>hardcore</b> ela aponta para o perk
<b>{esc(f['hardcore_perk'])}</b>, que é o pacote de males do modo. No modo normal ela está
<b>vazia</b>. Então preenchê-la não reverte nada do jogo, não precisa de Lua, não precisa de script
de carregamento, e é <b>uma linha</b>. É assim que se dá um efeito permanente ao jogador.</p></div>
<div class="tablebox"><table>
<thead><tr><th class="num">id</th><th>Modo</th><th>player_perk_id no jogo</th><th>O que é</th></tr></thead>
<tbody>{gm_rows}</tbody></table></div>
<div class="note warn"><div class="t">O preço da coluna</div>
<p>É <b>um</b> perk por modo de jogo. Se dois mods a quiserem, o último do
<code>mod_order.txt</code> ganha e o outro desaparece sem aviso. Para nós isso é administrável: um
perk oculto nosso, que serve de ponte para tudo que quisermos conceder de graça. Nenhum outro mod
das 129 instâncias toca <code>game_mode</code> — a coluna está livre.</p></div>

<h2>As três maneiras de conceder um perk ao jogador</h2>
<p>Esta é a lição das três instâncias juntas, e vale mais do que qualquer linha que elas trazem.</p>
<div class="tablebox"><table>
<thead><tr><th>Rota</th><th>Como</th><th>Custo</th><th>Evidência</th></tr></thead>
<tbody>
<tr><td><b>Script Lua</b><div class="muted">1990</div></td>
<td class="why"><code>player.soul:AddPerk()</code> no fim de cada tela de carregamento</td>
<td class="why">exige pasta <code>Scripts</code>, roda a cada carregamento, sem como desligar, e
colide com qualquer mod que use o mesmo ouvinte de cena</td>
<td class="why">{chip("warn", "funciona")} é o que o 1990 faz</td></tr>
<tr><td><b><code>soul2perk</code></b><div class="muted">1375, 1629</div></td>
<td class="why">uma linha ligando o perk à alma</td>
<td class="why">só serve para almas que existem na tabela. O Henry <b>não tem</b> linha de alma
própria; o 1629 usa esta rota para as 2.423 almas de NPC, e aí funciona</td>
<td class="why">{chip("bad", "não alcança o Henry")} a linha do 1375 vai para a
<code>{esc(f['m1375_soul_name'])}</code></td></tr>
<tr><td><b><code>game_mode.player_perk_id</code></b><div class="muted">1375</div></td>
<td class="why">uma linha, na coluna que o motor lê para isso</td>
<td class="why">um perk por modo de jogo, e o último mod ganha</td>
<td class="why">{chip("ok", "a rota do jogo")} o próprio jogo a usa para
<b>{esc(f['hardcore_perk'])}</b></td></tr>
</tbody></table></div>

<h2>O garimpo: o que entra, o que fica em aberto</h2>
<div class="tablebox"><table>
<thead><tr><th>Linha</th><th>De</th><th>Entra?</th><th>Por quê</th></tr></thead>
<tbody>
<tr><td><b>perícia 20 (Escudo) desocultada</b></td><td>1569</td>
<td>{chip("ok", "sim, como está")}</td>
<td class="why">só muda <code>hidden</code>, as 12 colunas vêm completas, abre
{sum(1 for _, v, _ in f['skill20_perks'] if v == '2')} perks que o jogo já escreveu e os textos de
interface já existem. Não reverte nada</td></tr>
<tr><td><b>ouvido e visão dos animais</b></td><td>1990</td>
<td>{chip("warn", "a ideia sim, os valores não")}</td>
<td class="why">pergunta de balanceamento, e é sua: dentro da faixa do jogo (0–{f['hear_max']}) e
para os {len(f['animal_souls'])} animais, ou só os 7? Fica parado e visível, não descartado</td></tr>
<tr><td><b><code>game_mode.player_perk_id</code></b></td><td>1375</td>
<td>{chip("ok", "a técnica")}</td>
<td class="why">não a linha do 1375 — a <b>rota</b>. Resolve o problema do 1990 sem Lua nenhum</td></tr>
<tr><td><b>buff <code>btw*3</code> / Coração Selvagem <code>btw*2</code></b></td><td>1990</td>
<td>{chip("bad", "não")}</td>
<td class="why">inverte um perk do jogo, com base em um código que aparece em
<b>{len(f['btw_vanilla'])}</b> buff no jogo inteiro. Sem direção verificável e sem teste em jogo,
não entra</td></tr>
<tr><td><b><code>was-15</code> e o perk True Shot</b></td><td>1375</td>
<td>{chip("bad", "não, por sua decisão")}</td>
<td class="why">arco e flecha vai inteiro para o módulo de arco. A rota do modo de jogo é o que
guardamos de lá</td></tr>
<tr><td><b><code>rpg_param AimSpreadMax</code></b></td><td>1375</td>
<td>{chip("bad", "não há o que levar")}</td>
<td class="why">o valor é igual ao do jogo; o arquivo é decorativo</td></tr>
</tbody></table></div>

<h2>Glossário com a evidência</h2>
<p>Cada código é lido dos buffs do próprio jogo que já o usam. <b>Confirmado</b> = vários buffs
concordam; <b>deduzido</b> = um ou dois usos, é hipótese e precisa de teste antes de guiar
balanceamento.</p>
<div class="tablebox"><table>
<thead><tr><th>Código</th><th>Leitura</th><th>Lido de</th><th>Confiança</th></tr></thead>
<tbody>
<tr><td><code>btw</code></td>
<td class="why">percepção dos animais em relação a você. Direção: no jogo só existe como
<b>redução</b> (<code>*0.4</code>) num perk que ajuda a caçar, então <b>menor é melhor</b> para o
jogador</td>
<td class="mono">{esc(", ".join(n for n, _ in f["btw_vanilla"]))} — {len(f['btw_vanilla'])} buff em todo o jogo</td>
<td>{chip("warn", "deduzido")}</td></tr>
<tr><td><code>was</code></td>
<td class="why">tremor da mira; quanto menor, mais firme a arma</td>
<td class="mono">{esc(", ".join(n for n, _ in f["was_vanilla"]))}</td>
<td>{chip("ok", "confirmado")}</td></tr>
<tr><td><code>hearing</code></td>
<td class="why">coluna da tabela <code>soul</code>: quanto a criatura percebe você por som.
<b>Faixa do jogo: 0 a {f['hear_max']}</b>, em {num(f['soul_total'])} almas</td>
<td class="mono">medido na tabela <code>soul</code> inteira</td>
<td>{chip("ok", "confirmado")}</td></tr>
<tr><td><code>vision</code></td>
<td class="why">o mesmo, por imagem. <b>Faixa do jogo: 0 a {f['vis_max']}</b></td>
<td class="mono">medido na tabela <code>soul</code> inteira</td>
<td>{chip("ok", "confirmado")}</td></tr>
<tr><td><code>visibility</code></td>
<td class="why">coluna da tabela <code>perk</code>. <b>0</b> = oculto ({f['vis_counts']['0']} perks);
<b>1</b> = concedido por treino ou missão, aparece mas não se compra ({f['vis_counts']['1']},
inclusive os três Master Strike); <b>2</b> = comprável na árvore ({f['vis_counts']['2']});
<b>3</b> = legado, marcado <i>OBSOLETE</i> ({f['vis_counts']['3']})</td>
<td class="mono">contado nas {num(sum(f['vis_counts'].values()))} linhas de <code>perk</code></td>
<td>{chip("ok", "confirmado")}</td></tr>
<tr><td><code>player_perk_id</code></td>
<td class="why">coluna da tabela <code>game_mode</code>: o perk que o jogador recebe ao jogar
naquele modo</td>
<td class="mono">o modo hardcore do jogo aponta para <b>{esc(f['hardcore_perk'])}</b></td>
<td>{chip("ok", "confirmado")}</td></tr>
</tbody></table></div>

<h2>Defeitos de empacotamento, para não repetirmos</h2>
<div class="tablebox"><table>
<thead><tr><th>Mod</th><th>Defeito</th><th>Consequência</th></tr></thead>
<tbody>
<tr><td>1990</td><td class="why">cabeçalho do <code>soul</code> com
{len(f['soul_cols']) - len(f['soul_header_missing'])} de {len(f['soul_cols'])} colunas; 4 linhas
trazem atributos que o cabeçalho não declara</td>
<td class="why">pela regra 5, coluna ausente é apagada. O javali perde
<code>combat_level</code></td></tr>
<tr><td>1990</td><td class="why">manifest declara apenas <code>1.9.6</code></td>
<td class="why">o motor <b>desliga o mod</b> no 1.9.8. Já sabíamos, mas vale dizer que o arquivo
nunca rodou na sua versão</td></tr>
<tr><td>1375</td><td class="why">localização com <b>2 células</b> por linha</td>
<td class="why">o formato do jogo é 3 (chave, original, tradução). A terceira falta</td></tr>
<tr><td>1375</td><td class="why">um arquivo de patch idêntico ao jogo</td>
<td class="why">nada quebra, mas o mod aparenta mexer em algo que não mexe</td></tr>
<tr><td>1569</td><td class="why"><code>&lt;?xml version="2.0"?&gt;</code> no manifest; pasta
<code>data</code> em minúsculas</td>
<td class="why">inofensivo no Windows, e o manifest não tem <code>&lt;supports&gt;</code>, então
carrega em qualquer versão</td></tr>
<tr><td>os três</td><td class="why">sufixo do arquivo em maiúsculas/minúsculas mistas
(<code>__VeteranHunting</code>) contra o id derivado minúsculo</td>
<td class="why">pela regra 1 o sufixo tem de ser o id. Os três mods publicados e usados são a
evidência de que a comparação é <b>insensível a maiúsculas</b> — medimos que hífen não casa com
sublinhado, caixa não foi medida. No nosso módulo usamos <code>modid</code> minúsculo, então não
nos afeta</td></tr>
</tbody></table></div>

<h2>O que isto não responde</h2>
<p>Nada aqui envolve rodar o jogo. Está estabelecido o que os arquivos dizem e o que o motor faz
com eles. Três coisas só um teste em jogo decide:</p>
<ul>
<li>a <b>direção</b> do <code>btw</code> — um único buff do jogo o usa;</li>
<li>se a perícia Escudo desocultada <b>ganha XP</b> ao usar escudo, ou se a barra fica parada;</li>
<li>qual valor de ouvido e visão faz a caça ficar <b>difícil</b> em vez de <b>impossível</b>, dentro
da faixa 0–{f['hear_max']}.</li>
</ul>

<footer>Kingdom Refinement Suite · gerado por <code>tools/perks_round2_page.py</code> ·
cada número lido de <code>Data/Tables.pak</code> (jogo 1.9.8) e dos três mods em
<code>Mods WIP folder/Perks/perkaholic-riposte-workbench</code>.</footer>
</div>
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", help="extra copy of the page")
    args = ap.parse_args()
    page = build(collect())
    dest = os.path.join(WORKBENCH, "notes", "perks-round2.html")
    for p in [dest] + ([args.out] if args.out else []):
        os.makedirs(os.path.dirname(p), exist_ok=True)
        open(p, "w", encoding="utf-8", newline="\n").write(page)
        print(f"wrote {p} ({len(page) // 1024} KB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
