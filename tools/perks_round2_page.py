#!/usr/bin/env python3
"""
perks_round2_page.py - page (Portuguese) for the second round of the perk workbench: 1990, 1569, 1375.

    python tools/perks_round2_page.py [--out <extra copy>]

Every number on the page is read live from the unmodified game (Data/Tables.pak and the English
localization) and from the mods themselves, so the page cannot drift from the files. Writes
<workbench>/notes/perks-round2.html.
"""
import argparse
import collections
import html
import os
import re
import sys
import xml.etree.ElementTree as ET
import zipfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import vanilla  # noqa: E402
from page_style import CSS as PAGE_CSS  # noqa: E402

WIP = r"E:\Kingdom-Refinement-Suite\Mods WIP folder"
WORKBENCH = os.path.join(WIP, "Perks", "perkaholic-riposte-workbench")
EX = os.path.join(WORKBENCH, "extracted")
# 1375 is archery, so it was moved out of the perk workbench into the bow one; the page still
# reports on it, so it reads from where the files now live.
BOW_EX = os.path.join(WIP, "Archery", "bow-workbench", "extracted")

MODS = {
    "1990": ("1990_veteran-hunting", EX),
    "1569": ("1569_karnages-shield", EX),
    "1375": ("1375_no-aim-spread", BOW_EX),
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
SCALE = 5  # the divisor krs_hunting ships, mirrored from tools/build_krs_hunting.py

SKILL_PT = {"16": "Espada", "17": "Machado", "20": "Escudo", "21": "Maça", "23": "Arma Longa"}


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
    folder, root = MODS[mid]
    return os.path.join(root, folder, "_pak", *parts)


def game_text(keys):
    """the English UI strings of the unmodified game, cleaned enough to show in a table."""
    loc = os.path.join(vanilla.DEFAULT_GAME, "Localization")
    want, out = set(keys), {}
    for pak in ("English_xml.pak", "English.pak"):
        p = os.path.join(loc, pak)
        if not os.path.exists(p):
            continue
        z = zipfile.ZipFile(p)
        for zi in z.infolist():
            if not zi.filename.lower().endswith(".xml"):
                continue
            raw = vanilla.read_member(z, zi).decode("utf-8-sig", "replace")
            for m in re.finditer(r"<Row><Cell>([^<]+)</Cell><Cell>(.*?)</Cell>", raw, re.S):
                k = m.group(1).strip()
                if k in want and k not in out:
                    v = html.unescape(html.unescape(m.group(2)))
                    v = re.sub(r"<img[^>]*>", "", v)
                    v = re.sub(r"<br\s*/?>", " · ", v)
                    v = re.sub(r"<[^>]+>", "", v)
                    v = re.sub(r"\s+", " ", v).strip(" ·").replace("\ufffd", "–")
                    out[k] = v
    return out


# --------------------------------------------------------------------------- facts read from files
def collect():
    f = {}
    z = zipfile.ZipFile(os.path.join(vanilla.DEFAULT_GAME, "Data", "Tables.pak"))
    tpath = {os.path.basename(n)[:-4]: n[len("Libs/Tables/"):-4]
             for n in z.namelist() if n.endswith(".xml")}

    # ---------------------------------------------------------------- soul / 1990
    souls_cols, souls = vanilla.load("rpg/soul")
    f["soul_total"] = len(souls)
    f["soul_cols"] = [c for c, _ in souls_cols]
    hv = [(int(r["hearing"] or 0), int(r["vision"] or 0)) for r in souls
          if (r.get("hearing") or "").isdigit()]
    f["hear_max"] = max(h for h, _ in hv)
    f["vis_max"] = max(v for _, v in hv)
    hear_nz = sorted(h for h, _ in hv if h > 0)
    vis_nz = sorted(v for _, v in hv if v > 0)
    f["hear_med"], f["vis_med"] = hear_nz[len(hear_nz) // 2], vis_nz[len(vis_nz) // 2]

    def pctile(vals, x):
        import bisect
        return bisect.bisect_right(vals, x) / len(vals) * 100

    vsoul = {r["soul_id"]: r for r in souls}
    mcols, mrows = read_table(modfile("1990", "Libs", "Tables", "rpg", "soul__VeteranHunting.xml"))
    f["soul_header_missing"] = [c for c in f["soul_cols"] if c not in mcols]
    mrow = {r["soul_id"]: r for r in mrows}
    f["animals"] = []
    for sid, name in ANIMALS:
        m, v = mrow[sid], vsoul[sid]
        h, s = int(m["hearing"]), int(m["vision"])
        f["animals"].append({
            "name": name, "key": v.get("soul_name"), "hear": h, "vis": s,
            "ship_hear": h // SCALE, "ship_vis": s // SCALE,
            "p_hear": pctile(hear_nz, h // SCALE), "p_vis": pctile(vis_nz, s // SCALE),
            "v_combat": v.get("combat_level") or "0",
        })
    f["animal_souls"] = sorted(
        (r.get("soul_name"), r.get("hearing"), r.get("vision")) for r in souls
        if (r.get("soul_name") or "").lower().startswith(("animal", "sheep")))
    f["untouched"] = [n for n, _, _ in f["animal_souls"]
                      if n not in {x["key"] for x in f["animals"]}]

    # ---------------------------------------------------------------- buffs
    _, buffs = vanilla.load("rpg/buff")
    B = {r["buff_id"]: r for r in buffs}
    f["btw_vanilla"] = [(r.get("buff_name"), r.get("params")) for r in buffs
                        if "btw" in (r.get("params") or "")]
    f["was_vanilla"] = [(r.get("buff_name"), r.get("params")) for r in buffs
                        if "was" in (r.get("params") or "")]

    # ---------------------------------------------------------------- perks
    _, perks = vanilla.load("rpg/perk")
    f["vis_counts"] = {v: sum(1 for r in perks if r.get("visibility") == v)
                       for v in ("0", "1", "2", "3")}
    f["autolearn_total"] = sum(1 for r in perks if r.get("autolearnable") == "True")
    f["hardcore_perk"] = next((r.get("perk_name") for r in perks
                               if r["perk_id"] == "1e53b07d-8012-44b1-ace6-3504558f04aa"), None)
    f["skill23_perks"] = [r for r in perks if r.get("skill_selector") == "23"]

    _, pcs = vanilla.load("rpg/perk_combo_step")
    combo_of = {r["perk_id"]: r.get("combo_id") for r in pcs}
    _, combos = vanilla.load(tpath["combat_combo"])
    _, steps = vanilla.load(tpath["combat_combo_step"])
    nsteps = collections.Counter(s["combat_combo_id"] for s in steps)
    combo_name = {r["combat_combo_id"]: r.get("combat_combo_name") for r in combos}

    # the shield tree, and the same combos as they exist on the other weapon skills
    shd = collections.defaultdict(list)
    for r in perks:
        n = r.get("perk_name") or ""
        if n.startswith("Combo shd"):
            shd[n.split(" (")[0]].append(r)
    f["shield_tree"] = []
    for r in sorted((x for x in perks if x.get("skill_selector") == "20"),
                    key=lambda x: int(x.get("level") or 0)):
        base = (r.get("perk_name") or "").split(" (")[0]
        cid = combo_of.get(r["perk_id"])
        f["shield_tree"].append({
            "row": r, "combo": combo_name.get(cid), "steps": nsteps.get(cid, 0),
            "siblings": sorted(((x.get("skill_selector"), x.get("level"))
                                for x in shd.get(base, []) if x.get("skill_selector") != "20"),
                               key=lambda t: int(t[0])),
        })
    f["ripo_family"] = sorted(
        ((r.get("perk_name"), r.get("visibility"), r.get("level") or "",
          r.get("skill_selector") or "") for r in perks
         if (r.get("perk_name") or "").startswith("ripo")), key=lambda t: t[0])

    # ---------------------------------------------------------------- skills / 1569
    scols, skills = vanilla.load("rpg/skill")
    scol_names = [c for c, _ in scols]
    f["hidden_skills"] = [(r["skill_id"], r.get("skill_name")) for r in skills
                          if r.get("hidden") == "True"]
    f["skill_rows"] = {r["skill_id"]: r for r in skills}
    k20cols, k20rows = read_table(modfile("1569", "Libs", "Tables", "rpg",
                                          "skill__Karnages_Shield_Restoration.xml"))
    v20 = f["skill_rows"]["20"]
    f["s1569_cols"] = (len(k20cols), len(scol_names))
    f["s1569_diff"] = {c: (v20.get(c, ""), k20rows[0].get(c, ""))
                       for c in k20cols if (v20.get(c, "") or "") != (k20rows[0].get(c, "") or "")}

    _, s2s = vanilla.load("rpg/soul2skill")
    per_skill = collections.Counter(r.get("skill_id") for r in s2s)
    f["npc_skill20"], f["npc_skill23"] = per_skill["20"], per_skill["23"]
    _, s2i = vanilla.load("rpg/skill2item_category")
    f["s2i_skills"] = sorted({r.get("skill_id") for r in s2i}, key=int)
    f["s2i_names"] = [f["skill_rows"][s].get("skill_name") for s in f["s2i_skills"]]

    _, wclass = vanilla.load("item/weapon_class")
    w20 = next((r for r in wclass if r.get("skill_id") == "20"), {})
    f["wclass20_name"] = w20.get("weapon_class_name", "?")
    draw = B.get(w20.get("draw_buff_id"), {})
    f["shield_draw_buff"] = (draw.get("buff_name"), draw.get("params"))
    _, weapons = vanilla.load(tpath["weapon"])
    shields = [r for r in weapons if r.get("weapon_class_id") == w20.get("weapon_class_id")]
    f["shield_items"] = len(shields)
    defs = sorted(float(r["defense"]) for r in shields if r.get("defense"))
    f["shield_def"] = (defs[0], defs[-1]) if defs else (0, 0)

    f["text"] = game_text([f"perk_w_shield_comb{i}{s}" for i in range(1, 6) for s in ("", "_desc")]
                          + ["ui_skill_weapon_shield", "ui_skill_weapon_shield_desc0",
                             "ui_skill_wpnshield_levelup"])

    # ---------------------------------------------------------------- 1375
    _, gmodes = vanilla.load("game_mode")
    f["game_mode"] = gmodes
    _, rparams = vanilla.load("rpg/rpg_param")
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


# --------------------------------------------------------------------------- charts
def _bars(rows, xmax, ticks, mark=None, mark_label=""):
    """horizontal bars, two series per row, every bar directly labelled.

    `mark` draws the game's own reference (its ceiling or its median) as a shaded band plus a
    dashed line, so each bar can be read against the range the engine actually uses.
    """
    W, LEFT, RIGHT = 760, 172, 64
    plot, rowh, barh, gap, top = W - LEFT - RIGHT, 40, 13, 4, 46
    H = top + rowh * len(rows) + 46
    x = lambda v: LEFT + v / xmax * plot
    p = [f'<svg viewBox="0 0 {W} {H}" role="img" width="100%" aria-label="{esc(mark_label)}">']
    if mark is not None:
        p.append(f'<rect x="{x(0):.1f}" y="{top - 16}" width="{x(mark) - x(0):.1f}" '
                 f'height="{rowh * len(rows) + 24}" fill="var(--band)" rx="2" />')
        p.append(f'<line x1="{x(mark):.1f}" y1="{top - 16}" x2="{x(mark):.1f}" '
                 f'y2="{top + rowh * len(rows) + 8}" stroke="var(--ink3)" stroke-width="1.5" '
                 f'stroke-dasharray="3 3" />')
        p.append(f'<text x="{x(mark) + 8:.1f}" y="{top - 20}" font-size="11.5" fill="var(--ink2)" '
                 f'font-family="var(--body)">{esc(mark_label)}</text>')
    for i, (label, a, b) in enumerate(rows):
        yb = top + i * rowh
        p.append(f'<text x="{LEFT - 12}" y="{yb + barh}" text-anchor="end" font-size="12.5" '
                 f'fill="var(--ink)" font-family="var(--body)">{esc(label)}</text>')
        for k, (v, col) in enumerate(((a, "var(--s1)"), (b, "var(--s2)"))):
            yy = yb + k * (barh + gap)
            p.append(f'<rect x="{x(0):.1f}" y="{yy}" width="{max(x(v) - x(0), 2):.1f}" '
                     f'height="{barh}" rx="3" fill="{col}" />')
            p.append(f'<text x="{x(v) + 7:.1f}" y="{yy + barh - 2}" font-size="11.5" '
                     f'fill="var(--ink2)" font-family="var(--body)" '
                     f'style="font-variant-numeric:tabular-nums">{v}</text>')
    base = top + rowh * len(rows) + 6
    p.append(f'<line x1="{x(0):.1f}" y1="{base}" x2="{x(xmax):.1f}" y2="{base}" '
             f'stroke="var(--line)" stroke-width="1" />')
    for t in ticks:
        p.append(f'<text x="{x(t):.1f}" y="{base + 18}" text-anchor="middle" font-size="11" '
                 f'fill="var(--ink3)" font-family="var(--body)">{t}</text>')
    p.append("</svg>")
    return '<div class="figure">' + "".join(p) + "</div>"


LEGEND = ('<div class="legend">'
          '<span><i style="background:var(--s1)"></i>ouvido (<code>hearing</code>)</span>'
          '<span><i style="background:var(--s2)"></i>visão (<code>vision</code>)</span></div>')


def chart_mod(f):
    rows = [(a["name"], a["hear"], a["vis"]) for a in f["animals"]]
    return LEGEND + _bars(rows, 100, (0, 20, 40, 60, 80, 100), mark=f["hear_max"],
                          mark_label=f"← a faixa inteira do jogo acaba em {f['hear_max']}")


def chart_shipped(f):
    rows = [(a["name"], a["ship_hear"], a["ship_vis"]) for a in f["animals"]]
    return LEGEND + _bars(rows, 20, (0, 5, 10, 15, 20), mark=f["hear_med"],
                          mark_label=f"mediana de ouvido dos NPCs: {f['hear_med']}")


# --------------------------------------------------------------------------- page
def build(f):
    a = f["animals"]
    hi = max(a, key=lambda r: r["hear"])
    boar = next(r["v_combat"] for r in a if r["name"] == "Javali")
    untouched = ", ".join(esc(n) for n in f["untouched"])
    hidden = ", ".join(f"{esc(n)} ({sid})" for sid, n in f["hidden_skills"])
    missing_cols = "</code>, <code>".join(esc(c) for c in f["soul_header_missing"])
    shield_desc = esc(f["text"].get("ui_skill_weapon_shield_desc0", ""))

    # ---- 1569: the shield tree
    tree = ""
    for e in f["shield_tree"]:
        r = e["row"]
        name = f["text"].get(r.get("perk_ui_name") or "", "")
        desc = f["text"].get(r.get("perk_ui_desc") or "", "")
        if r.get("visibility") == "0":
            tree += (f'<tr><td><b>{esc(r.get("perk_name"))}</b>'
                     f'<div class="muted">sem nome, sem ícone, sem descrição</div></td>'
                     f'<td class="num">{esc(r.get("level"))}</td><td>{chip("bad", "oculto")}</td>'
                     f'<td class="why">não tem combo nem buff: é o <b>Master Strike do escudo</b>, '
                     f'da mesma família <code>ripo_*</code> do Riposte — o motor lê o id do perk no '
                     f'código nativo</td></tr>')
            continue
        sib = ""
        if e["siblings"]:
            sib = ('<div class="muted">o mesmo combo existe em '
                   + ", ".join(f"{SKILL_PT.get(s, s)} nv {lv}" for s, lv in e["siblings"])
                   + " — lá <b>sem nome e sem ícone</b></div>")
        how = (chip("warn", "automático") if r.get("autolearnable") == "True"
               else chip("ok", "comprado"))
        tree += (f'<tr><td><b>{esc(name)}</b><div class="muted">{esc(r.get("perk_name"))} · '
                 f'ícone <code>{esc(r.get("icon_id"))}</code></div></td>'
                 f'<td class="num">{esc(r.get("level"))}</td><td>{how}</td>'
                 f'<td class="why">{esc(desc)}<div class="muted">combo real: {e["steps"]} passos '
                 f'em <code>combat_combo_step</code></div>{sib}</td></tr>')

    ripo = "".join(
        f'<tr><td class="mono">{esc(n)}</td>'
        f'<td>{chip("ok", "visível") if v == "1" else chip("bad", "oculto")}</td>'
        f'<td class="num">{esc(lv or "-")}</td><td>{esc(SKILL_PT.get(sk, sk or "-"))}</td></tr>'
        for n, v, lv, sk in f["ripo_family"])

    scaled = ""
    for r in a:
        mod = f'{r["hear"]} / {r["vis"]}'
        ship = f'{r["ship_hear"]} / {r["ship_vis"]}'
        scaled += (f'<tr><td>{esc(r["name"])}<div class="muted">{esc(r["key"])}</div></td>'
                   f'<td class="chg">{chg("0 / 0", mod)}</td>'
                   f'<td class="chg">{chg(mod, ship)}</td>'
                   f'<td class="why">ouvido no percentil <b>{r["p_hear"]:.0f}</b>, visão no '
                   f'percentil <b>{r["p_vis"]:.0f}</b> entre os NPCs do jogo</td></tr>')

    gm_rows = ""
    for r in f["game_mode"]:
        what = (f'<b>{esc(f["hardcore_perk"])}</b> — o jogo usa esta coluna para empilhar os males '
                f'do modo hardcore no jogador' if r["player_perk_id"]
                else "vazio no jogo; é a casa que o 1375 preenche")
        gm_rows += (f'<tr><td class="num">{esc(r["game_mode_id"])}</td>'
                    f'<td>{esc(r["game_mode_name"])}</td>'
                    f'<td class="mono">{esc(r["player_perk_id"] or "(vazio)")}</td>'
                    f'<td class="why">{what}</td></tr>')

    v20, v18 = f["skill_rows"]["20"], f["skill_rows"]["18"]
    skill_cmp = "".join(
        f'<tr><td class="mono">{esc(c)}</td><td class="mono">{esc(v18.get(c) or "—")}</td>'
        f'<td class="mono">{esc(v20.get(c) or "—")}</td>'
        f'<td>{chip("bad", "a única diferença") if c == "hidden" else chip("ok", "mesma forma")}</td></tr>'
        for c in ("hidden", "ui_string_name", "skill_desc_nolevel", "ui_levelup_string_name",
                  "induced_skill_id", "icon_id"))

    diff_rows = "".join(
        f'<tr><td class="mono">{esc(c)}</td><td class="chg">{chg(w, n)}</td>'
        f'<td class="why">a perícia Escudo deixa de ser escondida e aparece na ficha do Henry</td>'
        f'</tr>' for c, (w, n) in f["s1569_diff"].items())

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
<p class="lead">1990, 1569 e 1375, lidos arquivo por arquivo contra as tabelas do jogo. Esta versão
já traz as decisões tomadas: o <b>1569 destranca uma árvore pronta</b> que a Warhorse escondeu, o
<b>1990 virou módulo próprio</b> com os números trazidos para a escala do jogo, e o <b>1375 saiu</b>
para a bancada do arco.</p>

<div class="tiles">
  <div class="tile hi"><div class="n">5</div><div class="l">perks de combo prontos atrás da perícia Escudo</div></div>
  <div class="tile"><div class="n">{f['shield_items']}</div><div class="l">escudos já existem como arma no jogo</div></div>
  <div class="tile"><div class="n">{num(f['npc_skill20'])}</div><div class="l">NPCs já têm nível de Escudo</div></div>
  <div class="tile"><div class="n">{f['hear_max']}</div><div class="l">teto de ouvido e visão nas {num(f['soul_total'])} almas</div></div>
  <div class="tile"><div class="n">÷{SCALE}</div><div class="l">correção aplicada aos números do 1990</div></div>
</div>

<div class="tablebox"><table>
<thead><tr><th>Mod</th><th>O que entrega</th><th>Decisão</th><th>Onde foi parar</th></tr></thead>
<tbody>
<tr><td><b>1569</b> Karnages Shield Restoration</td>
<td class="why">desoculta a perícia <b>Escudo</b> (id 20)</td>
<td>{chip("ok", "adotar a linha")}</td>
<td class="why">aguarda o seu sim — iria para <code>krs_perks</code>, junto da perícia 23</td></tr>
<tr><td><b>1990</b> Veteran Hunting</td>
<td class="why">só a <b>percepção dos animais</b>; o perk silencioso, o buff novo e a inversão do
Coração Selvagem ficaram de fora</td>
<td>{chip("ok", "aplicado, escala corrigida")}</td>
<td class="why">módulo novo <code>krs_hunting</code>, na branch <code>krs-hunting</code></td></tr>
<tr><td><b>1375</b> No Aim Spread</td>
<td class="why">zera a oscilação do arco; a técnica <code>game_mode.player_perk_id</code> fica</td>
<td>{chip("bad", "fora dos perks")}</td>
<td class="why"><code>Mods WIP folder/Archery/bow-workbench</code>, com a nota de leitura</td></tr>
</tbody></table></div>

<h2>1569: a Warhorse escondeu uma árvore pronta</h2>
<p>O patch em si é a parte menos interessante — é só o que um patch PTF deveria sempre ser. A
linha traz <b>{f['s1569_cols'][0]} de {f['s1569_cols'][1]}</b> colunas, todas com o valor do jogo,
e uma única diferença:</p>
<div class="tablebox"><table>
<thead><tr><th>Coluna</th><th>Alteração</th><th>O que significa</th></tr></thead>
<tbody>{diff_rows}</tbody></table></div>

<h3>Por que isso não abre uma aba vazia</h3>
<p>Atrás da perícia escondida existe <b>conteúdo completo e terminado</b>: cinco perks de combo com
nome, ícone, descrição e o ritmo de botões escrito, cada um ligado a um combo de verdade em
<code>combat_combo_step</code>. Nada disso é invenção de mod — é texto e dado do jogo base.</p>
<div class="tablebox"><table>
<thead><tr><th>Perk da árvore do Escudo</th><th class="num">Nível</th><th>Como se obtém</th>
<th>O que é, no texto do próprio jogo</th></tr></thead>
<tbody>{tree}</tbody></table></div>
<p class="muted">“Automático” = <code>autolearnable=True</code>: concedido ao atingir o nível, sem
gastar ponto. Só {f['autolearn_total']} perks em todo o jogo são assim, e quatro deles estão aqui.
O único que custa ponto é o <b>Breath taker</b>.</p>

<div class="note ok"><div class="t">O achado: os combos foram espalhados, não apagados</div>
<p>Três desses cinco combos <b>também existem</b> nas perícias de Espada, Machado e Maça — e lá
estão com <code>visibility=0</code>, <b>sem nome, sem ícone e sem descrição</b>. Ou seja: hoje você
já aprende “Shield slam” e “Head Strike” em silêncio, pela perícia da arma, sem que a interface
diga nada. Desocultar a perícia 20 não inventa mecânica: devolve a <b>versão apresentada</b> dela,
na árvore que a Warhorse desenhou para isso.</p>
<p>E dois combos existem <b>só</b> na árvore do Escudo — <b>Breath taker</b> (nível 6) e
<b>Disbalance</b> (nível 12). Esses dois são conteúdo pronto que, no jogo base, <b>nenhum jogador
alcança</b>.</p></div>

<h3>A perícia está ligada ao motor, não só à interface</h3>
<div class="tablebox"><table>
<thead><tr><th>Onde</th><th>Evidência</th></tr></thead>
<tbody>
<tr><td class="mono">item/weapon_class</td>
<td class="why">a classe de arma <code>{esc(f['wclass20_name'])}</code> aponta
<code>skill_id=20</code> — a mesma coluna por onde Espada, Machado e Maça recebem XP. Não é uma
perícia órfã: é uma classe de arma do jogo</td></tr>
<tr><td class="mono">weapon</td>
<td class="why"><b>{f['shield_items']} escudos</b> já existem como arma, com <code>defense</code>
de {f['shield_def'][0]:.4g} a {f['shield_def'][1]:.4g}, <code>str_req</code> e durabilidade</td></tr>
<tr><td class="mono">draw_buff</td>
<td class="why">equipar um escudo já aplica o buff <code>{esc(f['shield_draw_buff'][0])}</code>
(<code>{esc(f['shield_draw_buff'][1])}</code>)</td></tr>
<tr><td class="mono">soul2skill</td>
<td class="why"><b>{num(f['npc_skill20'])}</b> NPCs carregam um valor de perícia de Escudo. O jogo
usa a perícia todo dia — só não a mostra para você</td></tr>
<tr><td class="mono">Localização do jogo</td>
<td class="why">“{esc(f['text'].get('ui_skill_weapon_shield', ''))}”, a descrição
(“{shield_desc}”) e a mensagem de subida de nível
(“{esc(f['text'].get('ui_skill_wpnshield_levelup', ''))}”) já estão escritas</td></tr>
</tbody></table></div>

<div class="note ok"><div class="t">Correção do que eu disse antes sobre o XP</div>
<p>Escrevi que “não há linha de <code>skill2item_category</code> para a perícia 20, então como ela
ganha XP é pergunta de teste”. Está errado por falta de contexto: essa tabela só tem linhas para
<b>{esc(", ".join(f['s2i_names']))}</b> — reparo, caça e os ofícios. <b>Nenhuma perícia de arma
aparece nela.</b> Espada, Machado, Maça e Arco também não, e sobem normalmente. O XP de arma vem
pelo <code>weapon_class.skill_id</code>, que o Escudo tem.</p></div>

<p>A comparação que fecha o argumento: a linha do Escudo e a do <b>Arco</b> — uma perícia visível e
funcionando — são estruturalmente a mesma coisa.</p>
<div class="tablebox"><table>
<thead><tr><th>Coluna</th><th>Arco (18, visível)</th><th>Escudo (20, oculto)</th><th></th></tr></thead>
<tbody>{skill_cmp}</tbody></table></div>
<p class="muted">Sword, Axe e Mace têm <code>induced_skill_id=2</code> (alimentam Esgrima); Arco e
Escudo não têm, e sobem sozinhos. O Escudo é idêntico ao Arco em todas as colunas que importam.</p>

<h3>O Master Strike do escudo</h3>
<p>Dentro da perícia 20 há ainda <code>ripo_shield_01</code>: nível 10, <code>visibility=0</code>,
sem combo e sem buff. É irmão do perk Riposte que você já destravou — a família
<code>ripo_*</code> inteira:</p>
<div class="tablebox"><table>
<thead><tr><th>Perk</th><th>Visível?</th><th class="num">Nível</th><th>Perícia</th></tr></thead>
<tbody>{ripo}</tbody></table></div>
<p>Só o trio <code>ripo_text_*</code> é visível (é o Master Strike que o Bernard ensina). Os três
numerados — espada longa, espada curta e <b>escudo</b> — estão trancados. Fica como <b>pergunta
para depois</b>: desocultar a perícia não destranca esse perk, e destrancá-lo é a mesma decisão que
você já tomou para o Riposte.</p>

<div class="note warn"><div class="t">O que o 1569 promete e não entrega</div>
<p>A descrição do manifest diz <q>adds xp gain parameters but they may not work</q>. Não há nenhum
parâmetro de XP no pacote — só a linha da perícia. Nada quebra; a promessa é que é falsa.</p></div>

<div class="note warn"><div class="t">E a perícia 23, que já está no nosso módulo</div>
<p>O <code>krs_perks</code> já desoculta a <b>Arma Longa</b> (23). Ao contrário do Escudo, ela tem
<b>{len(f['skill23_perks'])} perks</b> no jogo: a aba abre vazia. Os perks que faltam estão no
<b>1563</b>, com <code>skill_selector=23</code>. Vale o contraste: o Escudo é a perícia oculta mais
bem acabada do jogo, a Arma Longa é a mais incompleta.</p></div>
<p class="muted">As {len(f['hidden_skills'])} perícias que o jogo esconde: {hidden}.</p>

<h2>1990: o que foi aplicado, e o que ficou de fora</h2>
<p>O mod tinha três peças. Ficou <b>uma</b>, com os números corrigidos. Como o que sobrou não toca
nenhum perk, virou módulo próprio: <code>krs_hunting</code>, na branch <code>krs-hunting</code>.</p>
<div class="tablebox"><table>
<thead><tr><th>Peça do 1990</th><th>Decisão</th><th>Por quê</th></tr></thead>
<tbody>
<tr><td><b>Percepção dos animais</b><div class="muted">7 linhas de <code>soul</code></div></td>
<td>{chip("ok", "aplicada, ÷" + str(SCALE))}</td>
<td class="why">é a observação que vale o mod inteiro: no jogo, os {len(f['animal_souls'])} animais
têm ouvido e visão <b>zerados</b> — você caminha até o bicho</td></tr>
<tr><td><b>Perk oculto + buff <code>btw*3</code> + 2 scripts Lua</b></td>
<td>{chip("bad", "fora")}</td>
<td class="why">o script chama <code>player.soul:AddPerk()</code> ao fim de <b>cada</b> tela de
carregamento: efeito permanente que você nunca vê e não pode recusar. Com a rota
<code>game_mode.player_perk_id</code> do 1375 isso nem precisaria de Lua</td></tr>
<tr><td><b>Coração Selvagem invertido</b><div class="muted">perk do jogo</div></td>
<td>{chip("bad", "fora")}</td>
<td class="chg">{chg("btw*0.4", "btw*2", "o mod dobra o que o jogo reduz")}</td></tr>
</tbody></table></div>

<h3>Por que ÷{SCALE}, e não outro número</h3>
<p>Nas <b>{num(f['soul_total'])} almas</b> do jogo, <code>hearing</code> e <code>vision</code> nunca
passam de <b>{f['hear_max']}</b>. O 1990 escreve até <b>{hi['hear']}</b>: o autor leu as colunas
como porcentagem. Dividir por {SCALE} <b>mantém exatamente as proporções que ele escolheu entre os
animais</b> e põe o ouvido mais apurado — o da lebre — no teto do próprio jogo. Nenhum valor foi
inventado.</p>
{chart_mod(f)}
<p class="muted">O que o 1990 propõe, contra a faixa inteira do jogo (a área clara, até
{f['hear_max']}).</p>
{chart_shipped(f)}
<p class="muted">O que o <code>krs_hunting</code> grava, agora no eixo real do jogo (0 a
{f['hear_max']}).</p>
<div class="tablebox"><table>
<thead><tr><th>Animal</th><th>Jogo → 1990</th><th>1990 → enviado</th><th>Onde cai entre os NPCs</th></tr></thead>
<tbody>{scaled}</tbody></table></div>
<div class="note ok"><div class="t">O resultado passa no teste de plausibilidade</div>
<p>A lebre fica com o <b>ouvido mais apurado do jogo</b> e vista fraca; os cervídeos ficam no topo
dos dois sentidos; o javali ouve na média e é <b>praticamente cego</b>. Ninguém escolheu isso: são
as proporções do autor do mod caindo dentro da escala do jogo.</p></div>
<div class="note"><div class="t">Duas coisas que o módulo corrige no caminho</div>
<p><b>1.</b> O cabeçalho do <code>soul</code> no 1990 declara
{len(f['soul_cols']) - len(f['soul_header_missing'])} das {len(f['soul_cols'])} colunas, faltando
<code>{missing_cols}</code>. Pela regra 5, o que não vem é apagado — o javali perderia seu
<code>combat_level={esc(boar)}</code>. O <code>krs_hunting</code> envia as {len(f['soul_cols'])}
colunas completas.</p>
<p><b>2.</b> Ficam de fora, de propósito e registrado: <b>{untouched}</b> — gado que você não caça,
e o cão já tem visão 11.</p></div>

<h2>1375: saiu daqui, com a técnica anotada</h2>
<p>O conteúdo é arco e flecha e vai inteiro para o <code>krs_bow</code>. Os arquivos foram movidos
para <code>Mods WIP folder/Archery/bow-workbench</code>, com a leitura completa em
<code>notes/1375_no-aim-spread.md</code>, e a decisão está registrada no
<code>Reviewed_Mods/_reviewed.csv</code>.</p>
<div class="tablebox"><table>
<thead><tr><th>Arquivo</th><th>Alteração</th><th>O que significa</th><th>Funciona?</th></tr></thead>
<tbody>
<tr><td class="mono">rpg_param__NoAimSpread</td>
<td class="chg">{chg("AimSpreadMax = " + str(f['aim_vanilla']), "AimSpreadMax = " + str(f['m1375_aim']))}</td>
<td class="why"><b>idêntico ao jogo.</b> Carrega, é contado como <i>equal</i> pelo motor e não muda
nada</td><td>{chip("bad", "inerte")}</td></tr>
<tr><td class="mono">soul2perk__NoAimSpread</td>
<td class="chg">{chg("—", "perk → alma " + f['m1375_soul'][:8])}</td>
<td class="why">a alma é <code>{esc(f['m1375_soul_name'])}</code> — <b>a Theresa</b>. O Henry não
tem linha própria em <code>soul</code>, então esta rota não o alcança</td>
<td>{chip("bad", "alma errada")}</td></tr>
<tr><td class="mono">game_mode__NoAimSpread</td>
<td class="chg">{chg("player_perk_id vazio", "player_perk_id = ae32e325")}</td>
<td class="why"><b>a que funciona</b>, e a melhor descoberta das três instâncias</td>
<td>{chip("ok", "limpo")}</td></tr>
<tr><td class="mono">buff__NoAimSpread</td>
<td class="chg">{chg("não existe", f['m1375_buff']['params'])}</td>
<td class="why">no jogo, <code>was</code> só aparece como multiplicador (×1,6) ou deslocamento
pequeno (±0,25): <b>−15 não é ajuste, é interruptor</b></td>
<td>{chip("warn", "tudo ou nada")}</td></tr>
<tr><td class="mono">perk__NoAimSpread</td>
<td class="chg">{chg("não existe", "visibility=" + f['m1375_perk']['visibility'] + ", level=" + f['m1375_perk']['level'])}</td>
<td class="why"><code>visibility=2</code> é o perk comprável ({f['vis_counts']['2']} perks do jogo
são assim). Sem <code>skill_selector</code> cai na aba do Jogador — e já vem concedido pelo modo de
jogo</td><td>{chip("warn", "redundante")}</td></tr>
</tbody></table></div>

<div class="note ok"><div class="t">A coluna <code>player_perk_id</code> — o que levamos daqui</div>
<p>O jogo já usa essa coluna: no modo <b>hardcore</b> ela aponta para o perk
<b>{esc(f['hardcore_perk'])}</b>. No modo normal está <b>vazia</b>. Preenchê-la não reverte nada,
não precisa de Lua, não precisa de script de carregamento, e é <b>uma linha</b>. É assim que se dá
um efeito permanente ao jogador — e nenhum dos 129 mods A–E toca <code>game_mode</code>.</p></div>
<div class="tablebox"><table>
<thead><tr><th class="num">id</th><th>Modo</th><th>player_perk_id no jogo</th><th>O que é</th></tr></thead>
<tbody>{gm_rows}</tbody></table></div>

<h2>As três maneiras de conceder um perk ao jogador</h2>
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
<td class="why">só serve para almas que existem na tabela. O Henry <b>não tem</b> linha própria; o
1629 usa esta rota para as 2.423 almas de NPC, e aí funciona</td>
<td class="why">{chip("bad", "não alcança o Henry")} a linha do 1375 vai para a
<code>{esc(f['m1375_soul_name'])}</code></td></tr>
<tr><td><b><code>game_mode.player_perk_id</code></b><div class="muted">1375</div></td>
<td class="why">uma linha, na coluna que o motor lê para isso</td>
<td class="why">um perk por modo de jogo, e o último mod ganha</td>
<td class="why">{chip("ok", "a rota do jogo")} o próprio jogo a usa para
<b>{esc(f['hardcore_perk'])}</b></td></tr>
</tbody></table></div>

<h2>Glossário com a evidência</h2>
<p>Cada código é lido dos buffs do próprio jogo que já o usam. <b>Confirmado</b> = vários buffs
concordam; <b>deduzido</b> = um ou dois usos, é hipótese e precisa de teste antes de guiar
balanceamento.</p>
<div class="tablebox"><table>
<thead><tr><th>Código</th><th>Leitura</th><th>Lido de</th><th>Confiança</th></tr></thead>
<tbody>
<tr><td><code>btw</code></td>
<td class="why">percepção dos animais em relação a você. No jogo só existe como <b>redução</b>
(<code>*0.4</code>) num perk que ajuda a caçar, então <b>menor é melhor</b> para o jogador</td>
<td class="mono">{esc(", ".join(n for n, _ in f["btw_vanilla"]))} — {len(f['btw_vanilla'])} buff em todo o jogo</td>
<td>{chip("warn", "deduzido")}</td></tr>
<tr><td><code>was</code></td>
<td class="why">tremor da mira; quanto menor, mais firme a arma</td>
<td class="mono">{esc(", ".join(n for n, _ in f["was_vanilla"]))}</td>
<td>{chip("ok", "confirmado")}</td></tr>
<tr><td><code>hearing</code> / <code>vision</code></td>
<td class="why">colunas de <code>soul</code>: quanto a criatura percebe você por som e por imagem.
<b>Faixa do jogo: 0 a {f['hear_max']}</b>; mediana entre quem tem valor: {f['hear_med']} e
{f['vis_med']}</td>
<td class="mono">medido nas {num(f['soul_total'])} linhas de <code>soul</code></td>
<td>{chip("ok", "confirmado")}</td></tr>
<tr><td><code>visibility</code></td>
<td class="why">coluna de <code>perk</code>. <b>0</b> = oculto ({f['vis_counts']['0']});
<b>1</b> = concedido por treino ou missão, aparece mas não se compra ({f['vis_counts']['1']},
inclusive os três Master Strike); <b>2</b> = comprável na árvore ({f['vis_counts']['2']});
<b>3</b> = legado, marcado <i>OBSOLETE</i> ({f['vis_counts']['3']})</td>
<td class="mono">contado nas {num(sum(f['vis_counts'].values()))} linhas de <code>perk</code></td>
<td>{chip("ok", "confirmado")}</td></tr>
<tr><td><code>autolearnable</code></td>
<td class="why">o perk é concedido ao atingir o nível, <b>sem custar ponto</b>. Raro:
{f['autolearn_total']} perks em todo o jogo, quatro deles na árvore do Escudo</td>
<td class="mono">contado na tabela <code>perk</code></td>
<td>{chip("ok", "confirmado")}</td></tr>
<tr><td><code>player_perk_id</code></td>
<td class="why">coluna de <code>game_mode</code>: o perk que o jogador recebe ao jogar naquele
modo</td>
<td class="mono">o modo hardcore aponta para <b>{esc(f['hardcore_perk'])}</b></td>
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
<td class="why">o motor <b>desliga o mod</b> no 1.9.8 — o arquivo nunca rodou na sua versão</td></tr>
<tr><td>1375</td><td class="why">localização com <b>2 células</b> por linha</td>
<td class="why">o formato do jogo é 3 (chave, original, tradução)</td></tr>
<tr><td>1375</td><td class="why">um arquivo de patch idêntico ao jogo</td>
<td class="why">nada quebra, mas o mod aparenta mexer no que não mexe</td></tr>
<tr><td>1569</td><td class="why"><code>&lt;?xml version="2.0"?&gt;</code> no manifest; pasta
<code>data</code> em minúsculas</td>
<td class="why">inofensivo no Windows, e sem <code>&lt;supports&gt;</code> carrega em qualquer
versão</td></tr>
<tr><td>os três</td><td class="why">sufixo em caixa mista (<code>__VeteranHunting</code>) contra o
id derivado minúsculo</td>
<td class="why">pela regra 1 o sufixo tem de ser o id. Os três mods publicados e usados são a
evidência de que a comparação é <b>insensível a maiúsculas</b> — medimos que hífen não casa com
sublinhado, caixa não foi medida. Nos nossos módulos o <code>modid</code> é minúsculo</td></tr>
</tbody></table></div>

<h2>O que isto não responde</h2>
<p>Nada aqui envolve rodar o jogo. Quatro coisas só um teste em jogo decide:</p>
<ul>
<li>se a perícia Escudo desocultada <b>sobe de nível</b> na prática — as tabelas dizem que está
ligada como o Arco, mas isso é leitura, não medição;</li>
<li>se os dois combos exclusivos do Escudo (<b>Breath taker</b> e <b>Disbalance</b>) realmente
<b>saem</b> quando o ritmo é executado;</li>
<li>qual valor de ouvido e visão faz a caça ficar <b>difícil</b> em vez de <b>impossível</b>;</li>
<li>a <b>direção</b> do <code>btw</code> — um único buff do jogo o usa, e por isso o Coração
Selvagem ficou intocado.</li>
</ul>

<footer>Kingdom Refinement Suite · gerado por <code>tools/perks_round2_page.py</code> ·
cada número lido de <code>Data/Tables.pak</code> e da localização inglesa do jogo 1.9.8, e dos mods
em <code>Mods WIP folder</code>.</footer>
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
