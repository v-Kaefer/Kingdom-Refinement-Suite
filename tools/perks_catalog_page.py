#!/usr/bin/env python3
"""
perks_catalog_page.py - the full catalogue of every perk modules/krs_perks ships, for the author
to check one by one.

    python tools/perks_catalog_page.py [--out <extra copy>]

One entry per row of perk__krs_perks.xml: whether the row is new or rewrites one the game already
has, every column of the row, the prerequisite and exclusivity, the icon, the name and description
as they will read in game, and the effect the perk grants with each code translated. Everything is
read live from modules/krs_perks, from the module's own English localization and from
Data/Tables.pak, so the page cannot drift from the files.

Writes <workbench>/notes/perks-catalog.html.
"""
import argparse
import collections
import html
import os
import re
import sys
import xml.etree.ElementTree as ET

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import vanilla  # noqa: E402
from page_style import CSS as PAGE_CSS  # noqa: E402
from perks_workbench_page import CODES, explain  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODULE = os.path.join(ROOT, "modules", "krs_perks")
TABLES = os.path.join(MODULE, "Data", "Libs", "Tables", "rpg")
OUT = os.path.join(r"E:\Kingdom-Refinement-Suite\Mods WIP folder\Perks"
                   r"\perkaholic-riposte-workbench", "notes", "perks-catalog.html")

TREE_PT = {
    "": "Jogador (sem perícia)", "0": "Furtividade", "1": "Equitação", "2": "Esgrima",
    "4": "Arrombamento", "5": "Batedor de carteiras", "6": "Alquimia", "8": "Reparo",
    "13": "Bebida", "14": "Caça", "15": "Defesa", "16": "Espada", "17": "Machado",
    "18": "Arco", "20": "Escudo", "21": "Maça", "23": "Arma Longa", "24": "Desarmado",
    "25": "Herbalismo", "26": "Leitura", "32": "Adestrador",
}
# order the trees appear on the page
TREE_ORDER = ["15", "16", "17", "21", "24", "18", "23", "2", "", "14", "26"]


def esc(t):
    return html.escape(str(t))


def chip(kind, text):
    return f'<span class="chip {kind}">{esc(text)}</span>'


def chg(was, now):
    return (f'<code class="was">{esc(was)}</code><span class="arrow">&#8594;</span>'
            f'<code class="is">{esc(now)}</code>')


def read(base, folder=TABLES, suffix="krs_perks"):
    p = os.path.join(folder, f"{base}__{suffix}.xml")
    raw = open(p, encoding="utf-8-sig", errors="replace").read()
    t = ET.fromstring(re.sub(r"^\s*<\?xml[^>]*\?>", "", raw)).find("table")
    return [dict(r.attrib) for r in t.findall("./rows/row")]


def clean(s):
    """the localization string as it will read on screen."""
    s = html.unescape(html.unescape(s or ""))
    s = re.sub(r"<img[^>]*>", "", s)
    s = re.sub(r"<br\s*/?>", " · ", s)
    s = re.sub(r"<[^>]+>", "", s)
    s = s.replace("\\n", " ").replace("\ufffd", "–")
    return re.sub(r"\s+", " ", s).strip(" ·· ").strip()


def pcts(text):
    """every percentage written in a string, as a set of numbers."""
    return {float(x) for x in re.findall(r"(\d+(?:[.,]\d+)?)\s*%", (text or "").replace(",", "."))}


def params_pcts(params):
    """the percentages a params formula really applies."""
    out = set()
    for part in re.split(r"[,;]", str(params or "")):
        m = re.match(r"^([A-Za-z_]+)([*+\-])(.+)$", part.strip())
        if not m:
            continue
        _code, op, val = m.groups()
        try:
            v = float(val)
        except ValueError:
            continue
        out.add(round(abs(v - 1) * 100, 4) if op == "*" else round(abs(v) * 100, 4))
    return out


# --------------------------------------------------------------------------- data
def collect():
    f = {}
    mp, mb = read("perk"), read("buff")
    mpb, mo, mx = read("perk_buff"), read("perk_buff_override"), read("perk2perk_exclusivity")

    _, vp = vanilla.load("rpg/perk")
    _, vb = vanilla.load("rpg/buff")
    _, vsk = vanilla.load("rpg/skill")
    VP = {r["perk_id"]: r for r in vp}
    VB = {r["buff_id"]: r for r in vb}
    P = {**VP, **{r["perk_id"]: r for r in mp}}
    B = {**VB, **{r["buff_id"]: r for r in mb}}
    f["skill_name"] = {r["skill_id"]: r.get("skill_name") for r in vsk}

    # the module's own English strings
    loc = {}
    raw = open(os.path.join(MODULE, "Localization", "English", "text__krs_perks.xml"),
               encoding="utf-8-sig", errors="replace").read()
    for m in re.finditer(r"<Row>\s*<Cell>([^<]*)</Cell>\s*<Cell>(.*?)</Cell>", raw, re.S):
        loc[m.group(1).strip()] = m.group(2)
    f["loc_keys"] = len(loc)

    import zipfile as _zip
    want = {P[p].get("perk_ui_name") for r in mp for p in [r.get("parent_id") or ""] if p in P}
    want |= {r.get("perk_ui_name") for r in vp}
    gtext = {}
    for pak in ("English_xml.pak", "English.pak"):
        pth = os.path.join(vanilla.DEFAULT_GAME, "Localization", pak)
        if not os.path.exists(pth):
            continue
        z = _zip.ZipFile(pth)
        for zi in z.infolist():
            if not zi.filename.lower().endswith(".xml"):
                continue
            t = vanilla.read_member(z, zi).decode("utf-8-sig", "replace")
            for m in re.finditer(r"<Row><Cell>([^<]+)</Cell><Cell>(.*?)</Cell>", t, re.S):
                k = m.group(1).strip()
                if k in want and k not in gtext:
                    gtext[k] = clean(m.group(2))

    link = collections.defaultdict(list)
    for r in mpb:
        link[r["perk_id"]].append(r["buff_id"])
    ovr = collections.defaultdict(list)
    for r in mo:
        ovr[r["perk_id"]].append(r)
    excl = collections.defaultdict(list)
    for r in mx:
        excl[r["first_perk_id"]].append(r["second_perk_id"])
        excl[r["second_perk_id"]].append(r["first_perk_id"])

    vis2 = {(r.get("perk_name") or "").strip().lower(): r for r in vp if r.get("visibility") == "2"}
    vicons = collections.Counter(r.get("icon_id") for r in vp if r.get("icon_id"))
    f["icon_uses"] = collections.Counter(r.get("icon_id") for r in mp if r.get("icon_id"))

    _, vpb = vanilla.load("rpg/perk_buff")
    vlink = {(r["buff_id"], r["perk_id"]) for r in vpb}

    def disp(pid):
        """the name a perk shows on screen: our override first, then the game's own text."""
        row = P.get(pid or "", {})
        key = row.get("perk_ui_name") or ""
        if key in loc:
            return clean(loc[key])
        return gtext.get(key) or row.get("perk_name") or pid

    entries = []
    for r in mp:
        v = VP.get(r["perk_id"])
        name = clean(loc.get(r.get("perk_ui_name") or "", "")) or r.get("perk_name")
        desc = clean(loc.get(r.get("perk_ui_desc") or "", ""))
        buffs = []
        for bid in link[r["perk_id"]]:
            b = B.get(bid, {})
            buffs.append({"id": bid, "name": b.get("buff_name"), "params": b.get("params"),
                          "new": bid not in VB, "duration": b.get("duration"),
                          "noop": (bid, r["perk_id"]) in vlink})
        ladder = [{"from": B.get(o["source_buff_id"], {}).get("buff_name"),
                   "to": B.get(o["target_buff_id"], {}).get("buff_name")} for o in ovr[r["perk_id"]]]
        d_p = pcts(desc)
        b_p = set().union(*[params_pcts(b["params"]) for b in buffs]) if buffs else set()
        mismatch = bool(d_p) and bool(b_p) and not (d_p & b_p)
        collide = vis2.get((r.get("perk_name") or "").strip().lower())
        entries.append({
            "id": r["perk_id"], "internal": r.get("perk_name"), "name": name, "desc": desc,
            "new": v is None,
            "diff": ({c: (v.get(c, ""), r.get(c, "")) for c in r
                      if (v.get(c, "") or "") != (r.get(c, "") or "")} if v else {}),
            "level": r.get("level") or "", "tree": r.get("skill_selector") or "",
            "vis": r.get("visibility"), "auto": r.get("autolearnable") == "True",
            "order": r.get("ui_priority") or "", "icon": r.get("icon_id") or "",
            "icon_vanilla": vicons.get(r.get("icon_id"), 0),
            "stat": r.get("stat_selector") or "", "excl_mode": r.get("exclude_in_game_mode") or "",
            "parent": disp(r.get("parent_id")) if r.get("parent_id") else "",
            "parent_new": (r.get("parent_id") or "") not in VP and bool(r.get("parent_id")),
            "meta": P.get(r.get("metaperk_id") or "", {}).get("perk_name") if r.get("metaperk_id") else "",
            "buffs": buffs, "ladder": ladder,
            "excl": [P.get(x, {}).get("perk_name") for x in excl[r["perk_id"]]],
            "mismatch": mismatch, "desc_pct": sorted(d_p), "buff_pct": sorted(b_p),
            "collide": collide,
            "ui_name_key": r.get("perk_ui_name") or "", "ui_desc_key": r.get("perk_ui_desc") or "",
        })
    entries.sort(key=lambda e: (TREE_ORDER.index(e["tree"]) if e["tree"] in TREE_ORDER else 99,
                                int(e["level"] or 0), e["name"]))
    f["entries"] = entries
    f["by_tree"] = collections.Counter(e["tree"] for e in entries)
    f["n_new"] = sum(1 for e in entries if e["new"])
    f["n_changed"] = sum(1 for e in entries if not e["new"])
    f["n_auto"] = sum(1 for e in entries if e["auto"])
    f["n_nobuff"] = sum(1 for e in entries if not e["buffs"])
    f["n_mismatch"] = sum(1 for e in entries if e["mismatch"])
    f["n_ladder"] = len(mo)
    f["buffs_new"] = sum(1 for r in mb if r["buff_id"] not in VB)
    f["buffs_changed"] = sum(1 for r in mb if r["buff_id"] in VB)
    ours = {r["perk_id"] for r in mp}
    f["orphans"] = []
    for r in mb:
        v = VB.get(r["buff_id"])
        if not v:
            continue
        owners = [VP.get(x["perk_id"], {}).get("perk_name") for x in vpb
                  if x["buff_id"] == r["buff_id"]]
        f["orphans"].append({
            "kind": "buff", "name": v.get("buff_name"),
            "diff": {c: (v.get(c, ""), r.get(c, "")) for c in r
                     if (v.get(c, "") or "") != (r.get(c, "") or "")},
            "owner": ", ".join(o for o in owners if o) or "—",
            "owned_by_us": any(VP.get(x["perk_id"], {}).get("perk_id") in ours for x in vpb
                               if x["buff_id"] == r["buff_id"]),
        })
    f["noop_rows"] = [(VP.get(r["perk_id"], {}).get("perk_name"),
                       B.get(r["buff_id"], {}).get("buff_name"))
                      for r in mpb if (r["buff_id"], r["perk_id"]) in vlink]
    srow = read("skill")[0]
    _, vskr = vanilla.load("rpg/skill")
    VS = {r["skill_id"]: r for r in vskr}
    f["skill_row"] = (srow["skill_id"], VS[srow["skill_id"]].get("skill_name"),
                      {c: (VS[srow["skill_id"]].get(c, ""), srow.get(c, "")) for c in srow
                       if (VS[srow["skill_id"]].get(c, "") or "") != (srow.get(c, "") or "")})
    f["codes_used"] = sorted({m.group(1) for e in entries for b in e["buffs"]
                              for m in re.finditer(r"([A-Za-z_]+)[*+\-]", str(b["params"] or ""))})
    return f


# --------------------------------------------------------------------------- page
def perk_card(e, f):
    tags = [chip("ok", "novo") if e["new"] else chip("warn", "altera linha do jogo")]
    if e["auto"]:
        tags.append(chip("warn", "automático"))
    if e["vis"] == "1":
        tags.append(chip("warn", "concedido"))
    if e["collide"] is not None:
        tags.append(chip("bad", "nome repetido"))
    if e["mismatch"]:
        tags.append(chip("bad", "texto x efeito"))
    if any(b["noop"] for b in e["buffs"]):
        tags.append(chip("bad", "ligação já existe"))

    efeito = ""
    for b in e["buffs"]:
        efeito += (f'<div>{explain(b["params"])}'
                   f'<div class="muted"><code>{esc(b["params"])}</code> · buff '
                   f'<code>{esc(b["name"])}</code> · '
                   f'{"novo" if b["new"] else "<b>do jogo</b>"} · '
                   f'{"permanente" if b["duration"] == "-1" else esc(b["duration"]) + "s"}</div></div>')
    if not e["buffs"] and e["ladder"]:
        efeito = ('<i>o efeito chega pela escada</i><div class="muted">não tem linha em '
                  '<code>perk_buff</code>: o degrau abaixo é substituído, e é essa substituição '
                  'que entrega o efeito</div>')
    elif not e["buffs"]:
        efeito = ('<i>nenhum buff ligado</i><div class="muted">perk de comportamento: o motor lê o '
                  'id do perk no código nativo</div>')
    for l in e["ladder"]:
        efeito += (f'<div class="muted">escada: substitui <code>{esc(l["from"])}</code> por '
                   f'<code>{esc(l["to"])}</code> em vez de somar</div>')

    req = []
    if e["parent"]:
        req.append(f'exige <b>{esc(e["parent"])}</b>'
                   + (' <span class="muted">(perk nosso)</span>' if e["parent_new"] else
                      ' <span class="muted">(perk do jogo)</span>'))
    if e["meta"]:
        req.append(f'metaperk <b>{esc(e["meta"])}</b>')
    for x in e["excl"]:
        req.append(f'exclui <b>{esc(x)}</b>')
    if e["excl_mode"]:
        req.append(f'fora do modo de jogo {esc(e["excl_mode"])}')
    if e["stat"]:
        req.append(f'stat_selector {esc(e["stat"])}')

    diff = ""
    if e["diff"]:
        diff = ('<div class="dif"><b>O que muda na linha do jogo:</b>'
                + "".join(f'<div><code>{esc(c)}</code> {chg(a or "(vazio)", b or "(VAZIO)")}</div>'
                          for c, (a, b) in e["diff"].items()) + "</div>")
    warn = ""
    if e["mismatch"]:
        warn += (f'<div class="dif bad"><b>A descrição e o efeito não batem:</b> o texto fala em '
                 f'{", ".join(f"{p:g}%" for p in e["desc_pct"])} e a fórmula aplica '
                 f'{", ".join(f"{p:g}%" for p in e["buff_pct"])}.</div>')
    if e["collide"] is not None:
        c = e["collide"]
        warn += (f'<div class="dif bad"><b>Nome repetido:</b> o jogo já tem um perk comprável '
                 f'chamado <b>{esc(e["internal"])}</b> (nível {esc(c.get("level"))}, '
                 f'{esc(TREE_PT.get(c.get("skill_selector") or "", "?"))}).</div>')
    if any(b["noop"] for b in e["buffs"]):
        warn += ('<div class="dif bad"><b>Ligação redundante:</b> o jogo já liga este perk a este '
                 'buff; a linha não acrescenta nada.</div>')

    return f"""<tr data-tree="{esc(e['tree'])}" data-kind="{'novo' if e['new'] else 'altera'}"
 data-flag="{'sim' if (e['mismatch'] or e['collide'] is not None or any(b['noop'] for b in e['buffs'])) else 'nao'}">
<td><b>{esc(e['name'])}</b> {' '.join(tags)}
  <div class="muted">interno <code>{esc(e['internal'])}</code></div>
  <div class="muted">chaves <code>{esc(e['ui_name_key'] or '—')}</code> / <code>{esc(e['ui_desc_key'] or '—')}</code></div></td>
<td class="num">{esc(e['level'] or '—')}</td>
<td class="why"><code>{esc(e['icon'] or '—')}</code>
  <div class="muted">{f"usado por {e['icon_vanilla']} perk(s) do jogo" if e['icon_vanilla'] else "não usado por nenhum perk do jogo"}</div></td>
<td class="why">{"<br>".join(req) or '<span class="muted">nenhum</span>'}</td>
<td class="why efeito">{efeito}</td>
<td class="why desc">{esc(e['desc']) or '<span class="muted">sem descrição</span>'}{diff}{warn}</td>
</tr>"""


def build(f):
    sections = ""
    for tree in sorted(f["by_tree"], key=lambda t: TREE_ORDER.index(t) if t in TREE_ORDER else 99):
        ents = [e for e in f["entries"] if e["tree"] == tree]
        sections += (f'<h3>{esc(TREE_PT.get(tree, f["skill_name"].get(tree, tree)))} '
                     f'<span class="muted">· {len(ents)} perk(s)</span></h3>'
                     '<div class="tablebox"><table>'
                     '<thead><tr><th>Perk</th><th class="num">Nível</th><th>Ícone</th>'
                     '<th>Requisito</th><th>Efeito</th><th>Descrição na interface</th></tr></thead>'
                     '<tbody>' + "".join(perk_card(e, f) for e in ents) + "</tbody></table></div>")

    gloss = "".join(
        f'<tr><td><code>{esc(c)}</code></td><td>{esc(CODES[c][0])}</td>'
        f'<td class="why">{esc(CODES[c][2])}</td>'
        f'<td class="muted">{esc(CODES[c][3])}</td>'
        f'<td>{chip("ok", "confirmado") if CODES[c][4] else chip("warn", "deduzido")}</td></tr>'
        for c in f["codes_used"] if c in CODES)
    unknown = [c for c in f["codes_used"] if c not in CODES]

    orphans = ""
    for o in f["orphans"]:
        d = "".join(chg(a or "(vazio)", b or "(VAZIO)") for _c, (a, b) in o["diff"].items())
        worse = any(c == "params" and "fdm" in (b or "") and
                    float((b or "0*0").split("*")[-1]) > float((a or "0*9").split("*")[-1])
                    for c, (a, b) in o["diff"].items())
        read_ = ("<b>o módulo deixa este degrau PIOR que o jogo</b>: em <code>fdm</code> menor é "
                 "melhor, então 0,75 dá mais dano de queda que os 0,70 que o Henry já tem"
                 if worse else
                 "o jogo já dava um bônus aqui; o módulo aumenta o bônus existente")
        orphans += (f'<tr><td class="mono">buff <code>{esc(o["name"])}</code></td>'
                    f'<td><b>{esc(o["owner"])}</b></td><td class="chg">{d}</td>'
                    f'<td class="why">{chip("bad", "decidir") if worse else chip("warn", "confirmar")} '
                    f'{read_}</td></tr>')
    sid, sname, sdiff = f["skill_row"]
    skill_diff = "".join(chg(a or "(vazio)", b or "(VAZIO)") for _c, (a, b) in sdiff.items())
    noop_perk, noop_buff = (f["noop_rows"][0] if f["noop_rows"] else ("—", "—"))

    return f"""<title>Catálogo dos Perks</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo+Narrow:wght@500;700&family=Source+Sans+3:wght@400;600&family=JetBrains+Mono:wght@400;700&display=swap">
{PAGE_CSS}
<style>
td.why {{ min-width:11rem; }}
td.desc {{ max-width:30rem; }}
td.efeito {{ max-width:19rem; }}
.dif {{ margin-top:.5rem; padding:8px 10px; border-radius:6px; background:var(--accent-soft);
  font-size:.82rem; line-height:1.6; }}
.dif.bad {{ background:var(--bad-soft); color:var(--bad); }}
.dif code {{ background:transparent; }}
table {{ font-size:.86rem; }}
thead th {{ position:sticky; top:0; background:var(--surface); z-index:1; }}
</style>

<div class="wrap">
<div class="eyebrow">Kingdom Refinement Suite · modules/krs_perks · jogo 1.9.8</div>
<h1>Catálogo dos Perks</h1>
<p class="lead">Os <b>{len(f['entries'])}</b> perks que o módulo entrega hoje, um por linha, para
você conferir um a um: se é novo ou reescreve uma linha do jogo, nível, árvore, ícone, requisito,
o efeito real com cada código traduzido, e o nome e a descrição como vão aparecer na tela.</p>

<div class="tiles">
  <div class="tile hi"><div class="n">{f['n_new']}</div><div class="l">perks novos</div></div>
  <div class="tile"><div class="n">{f['n_changed']}</div><div class="l">reescrevem linha do jogo</div></div>
  <div class="tile"><div class="n">{f['n_ladder']}</div><div class="l">degraus de escada (override)</div></div>
  <div class="tile"><div class="n">{f['n_nobuff']}</div><div class="l">sem buff próprio (comportamento ou escada)</div></div>
  <div class="tile"><div class="n">{f['n_mismatch'] + sum(1 for e in f['entries'] if e['collide'] is not None)}</div><div class="l">com algo a corrigir</div></div>
</div>

<div class="note"><div class="t">Como ler</div>
<p><b>Novo</b> = linha que não existe no jogo; nada é revertido. <b>Altera linha do jogo</b> = o
módulo reescreve uma linha existente, e aí o antes→depois aparece em azul dentro da célula.
<b>Automático</b> = <code>autolearnable=True</code>, concedido ao atingir o nível sem custar ponto.
<b>Concedido</b> = <code>visibility=1</code>, aparece na ficha mas não se compra. Tudo em vermelho
é coisa que eu marquei para você decidir.</p></div>

<div class="filters" role="group" aria-label="Filtros">
  <button class="f" aria-pressed="true" data-f="todos">Todos ({len(f['entries'])})</button>
  <button class="f" aria-pressed="false" data-f="novo">Só os novos ({f['n_new']})</button>
  <button class="f" aria-pressed="false" data-f="altera">Só os que alteram o jogo ({f['n_changed']})</button>
  <button class="f" aria-pressed="false" data-f="flag">Só os marcados ({sum(1 for e in f['entries'] if e['mismatch'] or e['collide'] is not None or any(b['noop'] for b in e['buffs']))})</button>
</div>

{sections}

<h2>O que o módulo muda fora do catálogo</h2>
<p>Estas linhas mexem em perks que o jogo já tem e que o módulo <b>não</b> entrega, então não
aparecem na lista acima — mas mudam o seu jogo do mesmo jeito.</p>
<div class="tablebox"><table>
<thead><tr><th>Linha</th><th>Perk do jogo afetado</th><th>Alteração</th><th>Leitura</th></tr></thead>
<tbody>{orphans}
<tr><td class="mono">skill {esc(sid)}</td><td><b>{esc(sname)}</b></td>
<td class="chg">{skill_diff}</td>
<td class="why">desoculta a árvore de <b>{esc(TREE_PT.get(sid, sname))}</b> na ficha. Faz sentido porque o próprio
módulo põe {f["by_tree"].get(sid, 0)} perks nela</td></tr>
<tr><td class="mono">perk_buff</td><td><b>{esc(noop_perk)}</b></td>
<td class="chg"><code class="is">{esc(noop_buff)}</code></td>
<td class="why">{chip("bad", "remover")} esta ligação <b>já existe no jogo</b>. Não muda nada; é só uma linha a
mais disputando com outros mods. Dá para tirar</td></tr>
</tbody></table></div>

<h2>Os códigos de efeito que aparecem acima</h2>
<p>Cada um é lido dos buffs do próprio jogo que já o usam. <b>Confirmado</b> = vários buffs
concordam; <b>deduzido</b> = um ou dois usos, é hipótese.</p>
<div class="tablebox"><table>
<thead><tr><th>Código</th><th>O que é</th><th>O que faz em jogo</th><th>Lido de</th>
<th>Confiança</th></tr></thead>
<tbody>{gloss}</tbody></table></div>
{"<p class='muted'>Códigos sem tradução no glossário: <code>" + "</code>, <code>".join(esc(c) for c in unknown) + "</code>.</p>" if unknown else ""}

<h2>Os números do módulo</h2>
<div class="tablebox"><table>
<thead><tr><th>Item</th><th class="num">Quantidade</th><th>Observação</th></tr></thead>
<tbody>
<tr><td>Linhas de <code>perk</code></td><td class="num">{len(f['entries'])}</td>
<td class="why">{f['n_new']} novas, {f['n_changed']} reescrevendo o jogo</td></tr>
<tr><td>Linhas de <code>buff</code></td><td class="num">{f['buffs_new'] + f['buffs_changed']}</td>
<td class="why">{f['buffs_new']} novas, {f['buffs_changed']} alterando buff do jogo</td></tr>
<tr><td>Degraus em <code>perk_buff_override</code></td><td class="num">{f['n_ladder']}</td>
<td class="why">o degrau de cima <b>substitui</b> o de baixo em vez de somar</td></tr>
<tr><td>Perks sem buff ligado</td><td class="num">{f['n_nobuff']}</td>
<td class="why">perks de comportamento de combate; o motor lê o id no código nativo</td></tr>
<tr><td>Chaves de texto na localização do módulo</td><td class="num">{f['loc_keys']}</td>
<td class="why">todas as {sum(1 for e in f['entries'] if e['ui_name_key'])} chaves de nome e
descrição usadas pelos perks resolvem aqui; nenhuma fica sem texto</td></tr>
<tr><td>Ícones distintos</td><td class="num">{len(f['icon_uses'])}</td>
<td class="why">todos já são usados por algum perk do jogo, então existem como textura</td></tr>
</tbody></table></div>

<footer>Kingdom Refinement Suite · gerado por <code>tools/perks_catalog_page.py</code> ·
lido de <code>modules/krs_perks</code>, da localização inglesa do módulo e de
<code>Data/Tables.pak</code> (jogo 1.9.8).</footer>
</div>

<script>
(function () {{
  var rows = Array.prototype.slice.call(document.querySelectorAll('tbody tr[data-kind]'));
  var btns = Array.prototype.slice.call(document.querySelectorAll('button.f'));
  function apply(k) {{
    rows.forEach(function (r) {{
      r.hidden = !(k === 'todos'
        || (k === 'flag' ? r.dataset.flag === 'sim' : r.dataset.kind === k));
    }});
    document.querySelectorAll('h3').forEach(function (h) {{
      var box = h.nextElementSibling;
      if (!box || !box.querySelector) return;
      var any = Array.prototype.slice.call(box.querySelectorAll('tbody tr'))
        .some(function (r) {{ return !r.hidden; }});
      h.hidden = !any; box.hidden = !any;
    }});
    btns.forEach(function (b) {{ b.setAttribute('aria-pressed', b.dataset.f === k); }});
  }}
  btns.forEach(function (b) {{ b.addEventListener('click', function () {{ apply(b.dataset.f); }}); }});
}})();
</script>
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out")
    args = ap.parse_args()
    page = build(collect())
    for p in [OUT] + ([args.out] if args.out else []):
        os.makedirs(os.path.dirname(p), exist_ok=True)
        open(p, "w", encoding="utf-8", newline="\n").write(page)
        print(f"wrote {p} ({len(page) // 1024} KB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
