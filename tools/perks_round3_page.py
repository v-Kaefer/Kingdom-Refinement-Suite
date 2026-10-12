#!/usr/bin/env python3
"""
perks_round3_page.py - page (Portuguese) for the third round: mod 1563 and the audit of krs_perks
before the perk work is closed.

    python tools/perks_round3_page.py [--out <extra copy>]

Every number is read live from the unmodified game (Data/Tables.pak and the English localization),
from mod 1563 in the workbench, and from modules/krs_perks itself, so the page cannot drift from
the files. Writes <workbench>/notes/perks-round3.html.
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
M1563 = os.path.join(WIP, "Perks", "perkaholic-riposte-workbench", "extracted",
                     "1563_karnages-polearm")
WORKBENCH = os.path.join(WIP, "Perks", "perkaholic-riposte-workbench")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODULE = os.path.join(ROOT, "modules", "krs_perks", "Data", "Libs", "Tables", "rpg")

KEY = {"perk": ["perk_id"], "buff": ["buff_id"], "perk_buff": ["buff_id", "perk_id"],
       "perk_buff_override": ["perk_id", "source_buff_id", "target_buff_id"],
       "perk2perk_exclusivity": ["first_perk_id", "second_perk_id"], "skill": ["skill_id"]}


def esc(t):
    return html.escape(str(t))


def num(n):
    return f"{n:,}".replace(",", ".")


def chip(kind, text):
    return f'<span class="chip {kind}">{esc(text)}</span>'


def chg(was, now, note=""):
    out = (f'<code class="was">{esc(was)}</code><span class="arrow">&#8594;</span>'
           f'<code class="is">{esc(now)}</code>')
    if note:
        out += f'<div class="muted">{esc(note)}</div>'
    return out


def read_table(path):
    raw = open(path, encoding="utf-8-sig", errors="replace").read()
    t = ET.fromstring(re.sub(r"^\s*<\?xml[^>]*\?>", "", raw)).find("table")
    return ([c.get("name") for c in t.findall("./header/column")],
            [dict(r.attrib) for r in t.findall("./rows/row")])


def game_text(keys):
    loc = os.path.join(vanilla.DEFAULT_GAME, "Localization")
    want, out = set(k for k in keys if k), {}
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
                    out[k] = html.unescape(html.unescape(m.group(2))).strip()
    return out


# --------------------------------------------------------------------------- facts
def collect():
    f = {}
    z = zipfile.ZipFile(os.path.join(vanilla.DEFAULT_GAME, "Data", "Tables.pak"))
    tp = {os.path.basename(n)[:-4]: n[len("Libs/Tables/"):-4]
          for n in z.namelist() if n.endswith(".xml")}
    f["tp"] = tp

    # ------------------------------------------------------------ 1563: inventory
    inv = collections.Counter()
    empty_tbl = 0
    biggest = []
    for root, _, files in os.walk(M1563):
        for fn in files:
            p = os.path.join(root, fn)
            size = os.path.getsize(p)
            ext = os.path.splitext(fn)[1].lower() or "(sem extensão)"
            inv[ext] += 1
            if ext == ".tbl" and size == 0:
                empty_tbl += 1
            biggest.append((size, os.path.relpath(p, M1563).replace("\\", "/")))
    f["inv"] = inv
    f["empty_tbl"] = empty_tbl
    f["biggest"] = sorted(biggest, reverse=True)[:5]

    # ------------------------------------------------------------ 1563: tables
    tbl_dir = os.path.join(M1563, "_pak", "Libs", "Tables")
    f["t1563"] = []
    for root, _, files in os.walk(tbl_dir):
        for fn in sorted(files):
            if not fn.endswith(".xml"):
                continue
            base = fn.split("__")[0]
            mcols, mrows = read_table(os.path.join(root, fn))
            vcols, vrows = vanilla.load(tp[base])
            vn = [c for c, _ in vcols]
            sig = {tuple((c, r.get(c, "") or "") for c in vn) for r in vrows}
            same = sum(1 for r in mrows
                       if tuple((c, r.get(c, "") or "") for c in vn) in sig)
            f["t1563"].append({"table": base, "rows": len(mrows), "same": same,
                               "cols": (len(mcols), len(vn)),
                               "miss": [c for c in vn if c not in mcols]})
    f["t1563"].sort(key=lambda r: -r["rows"])
    f["t1563_rows"] = sum(r["rows"] for r in f["t1563"])
    f["t1563_same"] = sum(r["same"] for r in f["t1563"])

    def m1563(*parts):
        return read_table(os.path.join(tbl_dir, *parts))[1]

    # the three perks, their stated prerequisite and the names they borrow
    _, vp = vanilla.load("rpg/perk")
    VP = {r["perk_id"]: r for r in vp}
    VNAME = {(r.get("perk_ui_name") or ""): r.get("perk_name") for r in vp}
    f["p1563"] = []
    for r in m1563("rpg", "perk__Karnages_Polearm_Restoration.xml"):
        f["p1563"].append({
            "name": r.get("perk_name"), "level": r.get("level"),
            "auto": r.get("autolearnable"), "parent": r.get("parent_id") or "",
            "ui": r.get("perk_ui_name"), "borrowed": VNAME.get(r.get("perk_ui_name") or ""),
            "icon": r.get("icon_id"),
        })

    # weapon class 7, the draw buff swap
    _, vwc = vanilla.load("item/weapon_class")
    W = {r["weapon_class_id"]: r for r in vwc}
    _, vbuf = vanilla.load("rpg/buff")
    B = {r["buff_id"]: r for r in vbuf}
    row = m1563("item", "weapon_class__Karnages_Polearm_Restoration.xml")[0]
    v = W[row["weapon_class_id"]]
    f["wc7"] = {c: (v.get(c, ""), row.get(c, "")) for c in row
                if (v.get(c, "") or "") != (row.get(c, "") or "")}
    f["buff_names"] = {bid: (B[bid].get("buff_name"), B[bid].get("params"))
                       for bid in ("8938ac5f-35d3-44dc-8251-97df7570b672",
                                   "bf861d60-b892-42a3-9c3b-d3787362f88b")}

    # the polearms: defence and durability
    _, pi = vanilla.load(tp["player_item"])
    uikey = {r["item_id"]: r.get("ui_name") for r in pi}
    txt = game_text(uikey.values())
    NAME = {i: txt.get(k, k or i) for i, k in uikey.items()}
    _, vw = vanilla.load(tp["weapon"])
    VW = {r["item_id"]: r for r in vw}
    f["polearms"] = []
    for r in m1563("item", "weapon__Karnages_Polearm_Restoration.xml"):
        v = VW[r["item_id"]]
        f["polearms"].append({
            "name": NAME.get(r["item_id"], r["item_id"]),
            "def": (v.get("defense"), r.get("defense")),
            "dur": (v.get("max_status"), r.get("max_status")),
        })
    f["polearms"].sort(key=lambda r: str(r["name"]))
    f["dur_changed"] = sum(1 for r in f["polearms"] if r["dur"][0] != r["dur"][1])

    _, vmw = vanilla.load(tp["melee_weapon"])
    VM = {r["item_id"]: r for r in vmw}
    f["attack"] = []
    for r in m1563("item", "melee_weapon__Karnages_Polearm_Restoration.xml"):
        v = VM.get(r["item_id"])
        if v and (v.get("attack") or "") != (r.get("attack") or ""):
            f["attack"].append((NAME.get(r["item_id"], r["item_id"]),
                                v.get("attack"), r.get("attack")))
    f["melee_rows"] = len(m1563("item", "melee_weapon__Karnages_Polearm_Restoration.xml"))

    shop = m1563("shop", "shop_type2item__Karnages_Polearm_Restoration.xml")
    byitem = collections.defaultdict(set)
    for r in shop:
        byitem[r["item_id"]].add(r["shop_type_id"])
    f["shop"] = sorted(((NAME.get(i, i), sorted(t)) for i, t in byitem.items()),
                       key=lambda x: str(x[0]))
    f["shop_rows"] = len(shop)

    # combat tables: which weapon class they target
    cdir = os.path.join(tbl_dir, "combat")
    f["combat"] = []
    for fn in sorted(os.listdir(cdir)):
        base = fn.split("__")[0]
        mcols, mrows = read_table(os.path.join(cdir, fn))
        cls = [c for c in ("l_weapon_class_id", "r_weapon_class_id") if c in mcols]
        if cls:
            vals = collections.Counter(v for c in cls for v in (r.get(c) for r in mrows))
            only7 = all(r.get(c) in ("7", "-1") for r in mrows for c in cls)
        else:
            vals, only7 = {}, None
        f["combat"].append({"table": base, "rows": len(mrows), "only7": only7,
                            "vals": dict(vals)})
    # the dangling animation fragments
    frag = {r["mn_fragment_id"] for r in
            m1563("animation", "mn_fragment__Karnages_Polearm_Restoration.xml")}
    _, vfrag = vanilla.load(tp["mn_fragment"])
    vfid = {r["mn_fragment_id"] for r in vfrag}
    hits = m1563("combat", "combat_sync_action_hit__Karnages_Polearm_Restoration.xml")
    f["frag_defined"] = sorted(frag, key=int)
    f["frag_dangling"] = sorted({r["mn_fragment_id"] for r in hits
                                 if r["mn_fragment_id"] not in frag
                                 and r["mn_fragment_id"] not in vfid}, key=int)

    _, vgw = vanilla.load(tp["combat_weapon_group_to_class"])
    f["groups_vanilla"] = sorted({r["combat_weapon_group_id"] for r in vgw}, key=int)
    mgw = m1563("combat", "combat_weapon_group_to_class__Karnages_Polearm_Restoration.xml")
    f["groups_mod"] = sorted({r["combat_weapon_group_id"] for r in mgw}, key=int)

    # ------------------------------------------------------------ krs_perks audit
    mod = {}
    for base in KEY:
        p = os.path.join(MODULE, f"{base}__krs_perks.xml")
        if os.path.exists(p):
            mod[base] = read_table(p)
    f["audit"] = []
    for base, (mcols, mrows) in mod.items():
        vcols, vrows = vanilla.load("rpg/" + base)
        vn = [c for c, _ in vcols]
        vi = {tuple(r.get(k, "") for k in KEY[base]): r for r in vrows}
        new = chgd = same = 0
        for r in mrows:
            v = vi.get(tuple(r.get(k, "") for k in KEY[base]))
            if v is None:
                new += 1
            elif any((v.get(c, "") or "") != (r.get(c, "") or "") for c in mcols):
                chgd += 1
            else:
                same += 1
        f["audit"].append({"table": base, "rows": len(mrows), "new": new, "chg": chgd,
                           "same": same, "cols": (len(mcols), len(vn)),
                           "miss": [c for c in vn if c not in mcols]})
    f["audit"].sort(key=lambda r: -r["rows"])

    VB = {r["buff_id"]: r for r in vbuf}
    f["touched"] = []
    for r in mod["perk"][1]:
        v = VP.get(r["perk_id"])
        if v:
            f["touched"].append(("perk", v.get("perk_name"),
                                 {c: (v.get(c, ""), r.get(c, "")) for c in r
                                  if (v.get(c, "") or "") != (r.get(c, "") or "")}))
    for r in mod["buff"][1]:
        v = VB.get(r["buff_id"])
        if v:
            f["touched"].append(("buff", v.get("buff_name"),
                                 {c: (v.get(c, ""), r.get(c, "")) for c in r
                                  if (v.get(c, "") or "") != (r.get(c, "") or "")}))
    srow = mod["skill"][1][0]
    _, vsk = vanilla.load("rpg/skill")
    VS = {r["skill_id"]: r for r in vsk}
    f["touched"].append(("skill", VS[srow["skill_id"]].get("skill_name"),
                         {c: (VS[srow["skill_id"]].get(c, ""), srow.get(c, "")) for c in srow
                          if (VS[srow["skill_id"]].get(c, "") or "") != (srow.get(c, "") or "")}))

    novos = [r for r in mod["perk"][1] if r["perk_id"] not in VP]
    f["new_perks"] = len(novos)
    SKN = {r["skill_id"]: r.get("skill_name") for r in vsk}
    f["per_skill"] = sorted(collections.Counter(
        SKN.get(r.get("skill_selector") or "", "(aba do Jogador)") for r in novos).items(),
        key=lambda x: -x[1])
    f["skill23"] = sorted(((r.get("level"), r.get("perk_name")) for r in novos
                           if r.get("skill_selector") == "23"), key=lambda t: int(t[0] or 0))
    vis2 = {(r.get("perk_name") or "").strip().lower(): r for r in vp if r.get("visibility") == "2"}
    f["collisions"] = [(r.get("perk_name"), vis2[(r.get("perk_name") or "").strip().lower()])
                       for r in novos
                       if (r.get("perk_name") or "").strip().lower() in vis2]
    f["skill_names"] = SKN

    # dangling references and perks with nothing attached
    P = set(VP) | {r["perk_id"] for r in mod["perk"][1]}
    B2 = set(VB) | {r["buff_id"] for r in mod["buff"][1]}
    bad = 0
    for r in mod["perk"][1]:
        for c in ("parent_id", "metaperk_id"):
            if r.get(c) and r[c] not in P:
                bad += 1
    for r in mod["perk_buff"][1]:
        bad += (r["perk_id"] not in P) + (r["buff_id"] not in B2)
    for r in mod["perk_buff_override"][1]:
        for c, ref in (("perk_id", P), ("source_buff_id", B2), ("target_buff_id", B2)):
            if r.get(c) and r[c] not in ref:
                bad += 1
    f["dangling"] = bad
    linked = {r["perk_id"] for r in mod["perk_buff"][1]} | \
             {r["perk_id"] for r in mod["perk_buff_override"][1]}
    f["unlinked"] = [r.get("perk_name") for r in novos if r["perk_id"] not in linked]
    _, vpb = vanilla.load("rpg/perk_buff")
    vset = {(r["buff_id"], r["perk_id"]) for r in vpb}
    f["noop_links"] = [(VP.get(r["perk_id"], {}).get("perk_name"),
                        VB.get(r["buff_id"], {}).get("buff_name"))
                       for r in mod["perk_buff"][1] if (r["buff_id"], r["perk_id"]) in vset]
    f["feather"] = []
    for r in mod["buff"][1]:
        if "feather" in (r.get("buff_name") or "").lower():
            v = VB.get(r["buff_id"])
            f["feather"].append((r.get("buff_name"),
                                 v.get("params") if v else None, r.get("params")))
    f["feather"].sort(key=lambda t: t[0])
    return f


# --------------------------------------------------------------------------- page
def build(f):
    inv = " · ".join(f"<b>{n}</b> {esc(e)}" for e, n in f["inv"].most_common())
    t1563 = "".join(
        f'<tr><td class="mono">{esc(r["table"])}</td><td class="num">{r["rows"]}</td>'
        f'<td class="num">{r["same"] or "—"}</td><td class="num">{r["rows"] - r["same"]}</td>'
        f'<td>{chip("ok", "completo") if not r["miss"] else chip("bad", "faltam " + str(len(r["miss"])))}'
        f' <span class="muted">{r["cols"][0]}/{r["cols"][1]}</span></td></tr>'
        for r in f["t1563"])
    perks = "".join(
        f'<tr><td><b>{esc(p["name"])}</b></td><td class="num">{esc(p["level"])}</td>'
        f'<td>{chip("warn", "automático") if p["auto"] == "True" else chip("ok", "comprado")}</td>'
        f'<td>{chip("bad", "vazio") if not p["parent"] else chip("ok", "tem")}</td>'
        f'<td class="why">{"empresta o nome de <b>" + esc(p["borrowed"]) + "</b> (perk de espada curta do jogo)" if p["borrowed"] else "chave própria <code>" + esc(p["ui"]) + "</code>"}</td></tr>'
        for p in f["p1563"])
    pole = "".join(
        f'<tr><td>{esc(r["name"])}</td>'
        f'<td class="chg">{chg(r["def"][0], r["def"][1])}</td>'
        f'<td class="chg">{chg(r["dur"][0], r["dur"][1]) if r["dur"][0] != r["dur"][1] else "<span class=muted>sem mudança</span>"}</td></tr>'
        for r in f["polearms"])
    atk = "".join(f'<tr><td>{esc(n)}</td><td class="chg">{chg(a, b)}</td></tr>'
                  for n, a, b in sorted(f["attack"]))
    shop = "".join(f'<tr><td>{esc(n)}</td><td class="mono">{", ".join(t)}</td></tr>'
                   for n, t in f["shop"])
    comb = "".join(
        f'<tr><td class="mono">{esc(r["table"])}</td><td class="num">{r["rows"]}</td>'
        f'<td>{chip("ok", "só a haste") if r["only7"] else (chip("warn", "toca outras classes") if r["only7"] is False else chip("warn", "sem coluna de arma"))}</td>'
        f'<td class="mono">{esc(", ".join(f"{k or chr(8212)}×{v}" for k, v in sorted(r["vals"].items())) or "—")}</td></tr>'
        for r in f["combat"])
    audit = "".join(
        f'<tr><td class="mono">{esc(r["table"])}</td><td class="num">{r["rows"]}</td>'
        f'<td class="num">{r["new"]}</td><td class="num">{r["chg"] or "—"}</td>'
        f'<td class="num">{r["same"] or "—"}</td>'
        f'<td>{chip("ok", f"{r["cols"][0]}/{r["cols"][1]}") if not r["miss"] else chip("bad", "incompleto")}</td></tr>'
        for r in f["audit"])
    touched = "".join(
        f'<tr><td class="mono">{esc(kind)}</td><td><b>{esc(name)}</b></td>'
        f'<td class="chg">{"".join(chg(a or "(vazio)", b or "(VAZIO)") + "<br>" for c, (a, b) in d.items())}</td>'
        f'<td class="mono">{esc(", ".join(d))}</td></tr>'
        for kind, name, d in f["touched"])
    s23 = "".join(f'<tr><td class="num">{esc(lv)}</td><td>{esc(n)}</td></tr>' for lv, n in f["skill23"])
    per_skill = "".join(
        f'<div class="bar"><span class="bl">{esc(s)}</span>'
        f'<span class="bt" style="width:{n / f["per_skill"][0][1] * 100:.0f}%"></span>'
        f'<span class="bn">{n}</span></div>' for s, n in f["per_skill"])
    feather = "".join(
        f'<tr><td class="mono">{esc(n)}</td>'
        f'<td class="mono">{esc(v) if v else "(não existe no jogo)"}</td>'
        f'<td class="mono">{esc(m)}</td>'
        f'<td>{chip("bad", "pior que o jogo") if v and float(m.split("*")[1]) > float(v.split("*")[1]) else chip("ok", "melhora")}</td></tr>'
        for n, v, m in f["feather"])
    col = f["collisions"][0] if f["collisions"] else None

    return f"""<title>Haste e o Fecho dos Perks</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo+Narrow:wght@500;700&family=Source+Sans+3:wght@400;600&family=JetBrains+Mono:wght@400;700&display=swap">
{PAGE_CSS}
<style>
td.mono, .mono {{ font-family:var(--mono); font-size:.8rem; word-break:break-all; }}
.bars {{ margin:1rem 0; }}
</style>

<div class="wrap">
<div class="eyebrow">Kingdom Refinement Suite · bancada de perks · rodada 3 · jogo 1.9.8</div>
<h1>Haste e o Fecho dos Perks</h1>
<p class="lead">O mod <b>1563</b> lido inteiro pela primeira vez — os {sum(f['inv'].values())}
arquivos, não só as tabelas — e uma <b>auditoria do <code>krs_perks</code></b> contra o jogo antes
de fechar esta parte. A auditoria achou três coisas que precisam da sua decisão, e uma delas é um
valor que ficou <b>pior que o do jogo</b>.</p>

<div class="tiles">
  <div class="tile"><div class="n">{sum(f['inv'].values())}</div><div class="l">arquivos no 1563</div></div>
  <div class="tile"><div class="n">{f['t1563_rows']}</div><div class="l">linhas de tabela, {f['t1563_same']} idênticas ao jogo</div></div>
  <div class="tile"><div class="n">{f['dur_changed']}</div><div class="l">armas de haste com durabilidade → 500</div></div>
  <div class="tile hi"><div class="n">3</div><div class="l">defeitos achados no krs_perks</div></div>
  <div class="tile"><div class="n">{f['dangling']}</div><div class="l">referências penduradas no krs_perks</div></div>
</div>

<h2>1563: o inventário completo</h2>
<p>{inv}.</p>
<div class="note warn"><div class="t">Correção do que eu disse antes</div>
<p>Escrevi que os quatro <code>.tbl</code> eram “cópias binárias das tabelas, formato antigo”.
Errado: os {f['empty_tbl']} arquivos <code>.tbl</code> têm <b>0 bytes</b>. São arquivos vazios que
o autor deixou no pacote.</p></div>
<div class="tablebox"><table>
<thead><tr><th>Os maiores arquivos</th><th class="num">Tamanho</th></tr></thead>
<tbody>{"".join(f'<tr><td class="mono">{esc(p)}</td><td class="num">{num(s // 1024)} KB</td></tr>' for s, p in f["biggest"])}</tbody>
</table></div>

<div class="note bad"><div class="t">O script Lua rouba a sua tecla R</div>
<p>Os dois scripts (entregues em dois caminhos, <code>Libs/Scripts</code> e <code>Scripts</code>,
quatro arquivos no total) não têm nada a ver com haste. Eles registram um comando de depuração e
então fazem isto:</p></div>
<div class="pre"><span class="cmt">-- polearm_startup.lua</span>
Script.ReloadScript("Scripts/polearm.lua")
System.ExecuteCommand(<span class="del">"bind 'r' unequipitem"</span>)   <span class="cmt">-- religa a tecla R do jogo</span>

<span class="cmt">-- polearm.lua</span>
function unequipItem(entity)
    local weapon = entity.human:GetItemInHand(0)
    ...
    entity.actor:UnequipInventoryItem(weapon)   <span class="cmt">-- "[Debug] test follower"</span>
end</div>
<p>Isso <b>não é documentado em lugar nenhum do mod</b>: quem instala passa a desembainhar/soltar a
arma ao apertar R. É resto de desenvolvimento esquecido no pacote, e é o motivo mais forte para
nunca copiar um mod inteiro.</p>

<h2>1563: as {len(f['t1563'])} tabelas, linha a linha</h2>
<p>Todas com o cabeçalho completo — nesse ponto o autor acertou em todas.</p>
<div class="tablebox"><table>
<thead><tr><th>Tabela</th><th class="num">Linhas</th><th class="num">Idênticas ao jogo</th>
<th class="num">Diferentes</th><th>Cabeçalho</th></tr></thead>
<tbody>{t1563}</tbody></table></div>
<p class="muted">O <code>melee_weapon</code> é o caso extremo: {f['melee_rows']} linhas das quais
só <b>{len(f['attack'])}</b> mudam alguma coisa. As outras são cópias exatas do jogo — carregam,
contam como <i>equal</i> e servem só para aumentar a superfície de colisão com outros mods.</p>

<h3>Os três perks de haste</h3>
<div class="tablebox"><table>
<thead><tr><th>Perk</th><th class="num">Nível</th><th>Como se obtém</th><th>Pré-requisito</th>
<th>Nome na interface</th></tr></thead>
<tbody>{perks}</tbody></table></div>
<div class="note warn"><div class="t">O pré-requisito que a descrição promete não existe</div>
<p>As três descrições dizem <q>REQUIRED PERK: Shortsword Blunt Strike</q>,
<q>Duplieren: Doubling</q> e <q>Shortsword Halfsword</q>. Nenhum dos três perks tem
<code>parent_id</code> preenchido: <b>o jogo não vai exigir nada</b>. E a localização do mod ainda
traz <code>perk_polearm_combo4_name</code> e <code>combo5_name</code>, nomes de dois perks que o
mod <b>não entrega</b>.</p></div>

<h3>A haste equipável com escudo</h3>
<div class="tablebox"><table>
<thead><tr><th>Coluna de <code>weapon_class</code> 7 (halberd)</th><th>Alteração</th>
<th>O que significa</th></tr></thead>
<tbody>
<tr><td class="mono">weapon_equip_slot_id</td>
<td class="chg">{chg(*f["wc7"]["weapon_equip_slot_id"])}</td>
<td class="why">é isto que tira a alabarda do slot de duas mãos e a torna equipável junto com um
escudo — o coração do mod</td></tr>
<tr><td class="mono">draw_buff_id</td>
<td class="chg">{chg(f["buff_names"]["8938ac5f-35d3-44dc-8251-97df7570b672"][0], "(vazio)")}</td>
<td class="why"><b>remove</b> o buff
<code>{esc(f["buff_names"]["8938ac5f-35d3-44dc-8251-97df7570b672"][1])}</code>: com o mod você
passa a <b>correr à vontade com uma alabarda nas mãos</b>. Isso não está na descrição do mod</td></tr>
<tr><td class="mono">alternative_draw_buff_id</td>
<td class="chg">{chg("(vazio)", f["buff_names"]["bf861d60-b892-42a3-9c3b-d3787362f88b"][0])}</td>
<td class="why">no lugar entra o buff da <b>espada longa empunhada com uma mão</b>
(<code>{esc(f["buff_names"]["bf861d60-b892-42a3-9c3b-d3787362f88b"][1])}</code>): custo de ataque
+50%, dano −20%, velocidade −0,4. É uma boa ideia — a penalidade de usar arma longa com uma mão
só</td></tr>
</tbody></table></div>

<h3>As armas: defesa, durabilidade e dano</h3>
<div class="note bad"><div class="t">A durabilidade é o que ninguém anunciou</div>
<p><b>{f['dur_changed']} das {len(f['polearms'])}</b> armas de haste vão para
<code>max_status = 500</code> — de 1, 15, 25, 50, 100. É um aumento de <b>5x a 500x</b>: na prática
a arma deixa de quebrar. A descrição do mod fala de perícia, lojas, escudo e combos; de
durabilidade, nada.</p></div>
<div class="tablebox"><table>
<thead><tr><th>Arma de haste</th><th>Defesa</th><th>Durabilidade</th></tr></thead>
<tbody>{pole}</tbody></table></div>
<p class="muted">A defesa sobe <b>+1,2 em todas</b>, de forma uniforme. Já o dano desce em quase
todas:</p>
<div class="tablebox"><table>
<thead><tr><th>Arma</th><th>Dano (<code>attack</code>)</th></tr></thead>
<tbody>{atk}</tbody></table></div>

<h3>As lojas</h3>
<p>{f['shop_rows']} linhas novas em <code>shop_type2item</code>, {len(f['shop'])} itens distintos.</p>
<div class="tablebox"><table>
<thead><tr><th>Item</th><th>Tipos de loja</th></tr></thead>
<tbody>{shop}</tbody></table></div>
<div class="note warn"><div class="t">Duas linhas que não são de haste</div>
<p>Entre elas estão <b>duas linhas do “House of Zoul helmet”</b> no tipo de loja 8. Um elmo não tem
nada a ver com este mod: é sujeira que ficou no pacote.</p></div>

<h3>O combate: aditivo, não destrutivo</h3>
<p>Esta era a pergunta de segurança: o 1563 muda o combate das <b>outras</b> armas? A resposta está
nas colunas de classe de arma de cada linha.</p>
<div class="tablebox"><table>
<thead><tr><th>Tabela de combate</th><th class="num">Linhas</th><th>Alvo</th>
<th>Classes de arma nas linhas</th></tr></thead>
<tbody>{comb}</tbody></table></div>
<p>Quase tudo aponta para a <b>classe 7 (alabarda)</b> ou para <code>-1</code> (qualquer).
E o mod cria <b>grupos de combate novos</b>: o jogo tem os grupos
{", ".join(f["groups_vanilla"])} e o mod acrescenta {", ".join(f["groups_mod"])} — ou seja, não
reescreve o comportamento existente, anexa um ao lado.</p>
<div class="note warn"><div class="t">Mas há duas referências penduradas</div>
<p>O <code>combat_sync_action_hit</code> aponta para os fragmentos de animação
<b>{", ".join(f["frag_dangling"])}</b>, que <b>não existem nem no jogo nem no mod</b> — o mod só
define {", ".join(f["frag_defined"])}. Duas linhas apontam para o nada.</p></div>

<div class="note"><div class="t">O que dá para garimpar do 1563</div>
<p>A parte de <b>dados</b> é garimpável e está isolada: a linha da perícia 23, os três perks (com o
<code>parent_id</code> preenchido e os nomes arrumados), o <code>weapon_equip_slot_id</code> da
classe 7, os grupos de combate novos e as tabelas de combate da classe 7. Ficam de fora os scripts
Lua, a durabilidade 500, as duas linhas do elmo, os fragmentos pendurados e as
{f['melee_rows'] - len(f['attack'])} linhas de <code>melee_weapon</code> que não mudam nada. A
parte de <b>animação</b> (o banco de 6,2 MB) continua sendo tudo-ou-nada e continua sendo pergunta
de teste em jogo.</p></div>

<h2>Auditoria do <code>krs_perks</code> antes de fechar</h2>
<p>O módulo como está hoje, lido contra as tabelas do jogo. <code>check_patch_names.py</code>:
<b>0 problemas</b>. Cabeçalhos completos em todas as tabelas, <b>{f['dangling']}</b> referências
penduradas, e nenhum dos {f['new_perks']} perks novos ficou sem efeito ligado.</p>
<div class="tablebox"><table>
<thead><tr><th>Tabela</th><th class="num">Linhas</th><th class="num">Novas</th>
<th class="num">Alteram o jogo</th><th class="num">Idênticas</th><th>Cabeçalho</th></tr></thead>
<tbody>{audit}</tbody></table></div>

<h3>Defeito 1 — a escada do Like a Feather começa pior que o jogo</h3>
<div class="tablebox"><table>
<thead><tr><th>Buff</th><th>No jogo</th><th>No módulo</th><th></th></tr></thead>
<tbody>{feather}</tbody></table></div>
<div class="note bad"><div class="t">Isto inverte a sua intenção</div>
<p>Você pediu a escada <b>0,75 → 0,60 → 0,45</b>. Mas o primeiro degrau <b>já existe no jogo
valendo 0,70</b>. Como em <code>fdm</code> <b>menor é melhor</b> (menos dano de queda), gravar 0,75
deixa o primeiro degrau <b>pior do que o Henry já tem sem mod</b>: quem comprar o perk passa a
cair pior. Os degraus II e III são novos e estão certos.</p>
<p><b>Sugestão:</b> escada <b>0,70 → 0,60 → 0,45</b> — o primeiro degrau fica como o jogo e os dois
novos continuam valendo a pena. Ou 0,65 se você quiser que o primeiro também melhore. Não mudei
nada: é a sua decisão.</p></div>

<h3>Defeito 2 — o Master Strike perde o nível</h3>
<div class="tablebox"><table>
<thead><tr><th>Tipo</th><th>Linha do jogo</th><th>Alteração</th><th>Colunas</th></tr></thead>
<tbody>{touched}</tbody></table></div>
<div class="note warn"><div class="t">O <code>ripo_lsw_01</code> fica sem nível</div>
<p>Essa linha vem do mod 1765. Ela pega o riposte oculto da <b>espada longa</b> (perícia 16, nível
14), move para a <b>Defesa</b> (perícia 15), torna visível — e <b>apaga o nível</b>. Perk com
<code>visibility=1</code> e sem nível é a forma dos perks <i>concedidos</i> (os três Master Strike
do Bernard são assim), então provavelmente é intencional. Mas é a única linha do módulo que
<b>apaga</b> um valor do jogo em vez de trocá-lo, e merece o seu aval.</p></div>

<h3>Defeito 3 — uma linha que não faz nada</h3>
<p>O <code>perk_buff</code> traz a ligação <b>{esc(f["noop_links"][0][0]) if f["noop_links"] else "—"}
→ {esc(f["noop_links"][0][1]) if f["noop_links"] else "—"}</b>, que <b>já existe no jogo</b>.
Inofensiva, mas é uma linha a mais disputando com outros mods sem motivo. Dá para tirar.</p>

<div class="note bad"><div class="t">E a colisão de nome que continua aberta</div>
<p>{"<b>" + esc(col[0]) + "</b> é o nome de um perk <b>comprável</b> do jogo (nível " + esc(col[1].get("level")) + ", perícia " + esc(f["skill_names"].get(col[1].get("skill_selector"), "—")) + "). Dois perks com o mesmo nome na interface. Entra na lista de renomeações." if col else "Nenhuma."}</p></div>

<h2>Correção: a perícia 23 <b>não</b> abre vazia</h2>
<div class="note ok"><div class="t">Eu te dei um conselho errado</div>
<p>Eu disse que desocultar a <b>Arma Longa</b> (perícia 23) abria uma aba vazia porque o jogo não
tem perks nela. O jogo não tem — mas <b>o nosso próprio módulo põe {len(f['skill23'])}</b>, vindos
do Perkaholic. A linha da perícia 23 no <code>krs_perks</code> está justificada pelo conteúdo que
ele mesmo entrega; o que eu disse valia só para o jogo puro.</p></div>
<div class="tablebox"><table>
<thead><tr><th class="num">Nível</th><th>Perk que o krs_perks põe na Arma Longa</th></tr></thead>
<tbody>{s23}</tbody></table></div>
<p>Distribuição dos {f['new_perks']} perks novos pelas perícias:</p>
<div class="bars">{per_skill}</div>

<h2>O que fica em aberto</h2>
<ul>
<li><b>A escada do Like a Feather</b> — 0,75 deixa o primeiro degrau pior que o jogo; precisa do
seu número.</li>
<li><b>Renomear os 56 perks</b> (nomes, descrições, ícones, ordem de interface), incluindo a
colisão do {esc(col[0]) if col else "—"}.</li>
<li><b>Os dois parados em <code>include=False</code></b>: <code>perk_art_admirer_reward</code>
(carisma +1 → +2) e <code>perk_against_all_odds</code> (só interface).</li>
<li><b>1569 e as árvores ocultas</b> — adiadas por sua decisão, para revisão futura.</li>
<li><b>1563</b> — garimpável, mas o banco de animação de 6,2 MB só se resolve com teste em
jogo.</li>
</ul>

<footer>Kingdom Refinement Suite · gerado por <code>tools/perks_round3_page.py</code> ·
cada número lido de <code>Data/Tables.pak</code>, da localização inglesa do jogo 1.9.8, do mod 1563
na bancada e de <code>modules/krs_perks</code>.</footer>
</div>
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out")
    args = ap.parse_args()
    page = build(collect())
    dest = os.path.join(WORKBENCH, "notes", "perks-round3.html")
    for p in [dest] + ([args.out] if args.out else []):
        os.makedirs(os.path.dirname(p), exist_ok=True)
        open(p, "w", encoding="utf-8", newline="\n").write(page)
        print(f"wrote {p} ({len(page) // 1024} KB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
