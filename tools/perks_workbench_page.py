#!/usr/bin/env python3
"""
perks_workbench_page.py - interactive page (Portuguese) for the perk-mod workbench.

    python tools/analyze_perk_mods.py && python tools/perks_workbench_page.py

Reads <workbench>/notes/analysis.json and perkaholic_balance.json and writes
<workbench>/notes/perks-workbench.html: one page with the verdict of every instance and the full
balance detail of Perkaholic (every new perk with the effect it grants, every change to an existing
perk or buff, every collision). Opens no archive.
"""
import argparse
import html
import json
import re
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paths  # noqa: E402

WORKBENCH = r"E:\Kingdom-Refinement-Suite\Mods WIP folder\Perks\perkaholic-riposte-workbench"

# Effect codes as they appear in buff params. Each one is read from the vanilla buffs that already
# use it, so the meaning has evidence behind it:
#   short  - the name used in the perk table
#   better - "up" when a bigger number helps the player, "down" when a smaller one does
#   what   - what the stat does in play
#   seen   - the vanilla buffs the meaning was read from
#   sure   - True when several vanilla buffs agree; False when it rests on one or two
CODES = {
    "wat":    ("dano da arma", "up", "multiplica o dano que a sua arma causa", "perk_huntsman, perk_furious, weapon_bivojs_rage", True),
    "wac":    ("custo/tempo do ataque", "down", "quanto menor, mais barato ou mais rápido sai o golpe; 'encumbered' (sobrecarregado) piora esse mesmo valor", "perk_fast_striker, perk_heavy_swing, encumbered", True),
    "asp":    ("velocidade de ataque", "up", "rapidez da animação de ataque", "debuffSpeed, injured_right_arm, encumbered", True),
    "was":    ("tremor da mira", "down", "oscilação da arma ao mirar; quanto menor, mais firme", "HC perk Shakes, perk_drinking_habit", True),
    "mst":    ("estamina máxima", "up", "tamanho da barra de estamina", "potion_stamina, weapon_stamina", True),
    "srg":    ("regeneração de estamina", "up", "velocidade com que a estamina volta", "potion_stamina, perk_blood_rush, perk_berserk", True),
    "hlh":    ("dano recebido na vida", "down", "quanto do golpe inimigo chega à sua saúde", "resistent_fella, post_combat_protection, potion_aqua_vitalis", True),
    "slh":    ("dano recebido na estamina", "down", "quanto do golpe inimigo drena da estamina", "stamina_frenzy, resistent_fella, potion_aqua_vitalis", True),
    "hko":    ("chance de nocaute", "up", "probabilidade de derrubar o inimigo sem matá-lo", "perk_headcracker", True),
    "ain":    ("perfuração de armadura", "up", "quanto do golpe ignora a armadura do alvo", "perk_bloodletter, perk_serration", True),
    "ibi":    ("sangramento causado", "up", "intensidade do sangramento que você provoca", "bleeding_thickblooded, HC perk Haemophilia", True),
    "pac":    ("efeito de veneno", "up", "potência do veneno que você aplica", "perk_rusty_edge, veneno do torneio", True),
    "fdm":    ("dano de queda", "down", "dano que você sofre ao cair", "perk_like_a_feather, HC perk Brittle bones", True),
    "noi":    ("ruído ao se mover", "down", "quanto barulho você faz andando", "perk_slim_fit", True),
    "spc":    ("eloquência (fala)", "up", "sucesso em persuasão, intimidação e preço", "perk_merchants_wit, perk_highborn, potion_bard", True),
    "str":    ("força", "up", "atributo: dano corpo a corpo e capacidade de carga", "perk_general_ken, perk_local_hero, injured_torso", True),
    "agi":    ("agilidade", "up", "atributo: velocidade, arco e furtividade", "perk_local_hero, perk_burgess, injured_torso", True),
    "Sprint": ("velocidade de corrida", "up", "quanto mais rápido você corre esprintando", "perk_sprinter, perk_marathon_man", True),
    "Run":    ("velocidade correndo", "up", "corrida normal", "injured_left_leg, encumbered", True),
    "Walk":   ("velocidade caminhando", "up", "passo normal", "injured_right_leg, encumbered", True),
    "rms":    ("velocidade do cavalo", "up", "quão rápido a montaria corre", "perk_dread_steed, item_horse_shoe", True),
    "cli":    ("agarrão (clinch)", "up", "vantagem quando os corpos se chocam", "perk_clinch_master", False),
    "bad":    ("dano contra alvo específico", "up", "bônus contra um tipo de inimigo", "perk_cuman_killer", False),
    "dee":    ("efeito da ponta/estocada", "up", "lido do perk de haste que o usa", "perk_heavy_tip", False),
    "osb":    ("firmeza ao bloquear", "up", "lido do único perk do jogo que o usa", "perk_firm_hand", False),
    "ade":    ("defesa da armadura", "up", "lido do buff de teste que o usa", "test_turtle_skin", False),
    "dsl":    ("deslocamento em armadura leve", "up", "lido do perk de armadura leve", "perk_light_armor, encumbered", False),
    "cha":    ("carisma", "up", "atributo: como os NPCs reagem a você, preço e diálogo", "perk_general_ken, potion_love, alpha_male (29 buffs do jogo)", True),
    "erq":    ("velocidade de leitura", "up", "quanto você aproveita por hora lendo um livro", "perk_reading_Cushion", False),
}


def esc(t):
    return html.escape(str(t))


def pct(op, val):
    """'*1.05' -> '+5%'; '*0.9' -> '-10%'; '+0.05' -> '+0,05'."""
    try:
        v = float(val)
    except ValueError:
        return f"{op}{val}"
    if op == "*":
        d = (v - 1) * 100
        return f"{'+' if d >= 0 else '-'}{abs(d):.4g}%".replace(".", ",")
    return f"{op}{str(val).replace('.', ',')}"


def explain(params, long=True):
    """'wat*1.05' -> 'dano da arma +5% (multiplica o dano que a sua arma causa)'."""
    out = []
    for part in re.split(r"[,;]", str(params)):
        part = part.strip()
        if not part:
            continue
        m = re.match(r"^([A-Za-z_]+)([*+\-])(.+)$", part)
        if not m:
            out.append(esc(part))
            continue
        code, op, val = m.groups()
        info = CODES.get(code) or CODES.get(code.lower())
        if not info:
            out.append(f"<b>{esc(code)}</b> {esc(op + val)} <i>(código não identificado)</i>")
            continue
        name, better, what, _seen, _sure = info
        change = pct(op, val)
        helps = ((op == "*" and float(val) > 1) or op == "+") if better == "up" else \
                ((op == "*" and float(val) < 1) or op == "-")
        mark = "melhora" if helps else "piora"
        text = f"<b>{esc(name)} {esc(change)}</b>"
        if long:
            text += f' <span class="dim">— {esc(what)}; {mark} para o jogador</span>'
        out.append(text)
    return "<br>".join(out)


def chip(kind, text):
    return f'<span class="chip {kind}">{esc(text)}</span>'


def build(analysis, balance):
    by = {i["id"]: i for i in analysis}

    # ---------------------------------------------------------------- verdicts
    VERD = [
        ("1009r", "Perkaholic PTF (.rar, 2026)", "ok", "APLICADO",
         "6 patches PTF corretos, carrega no 1.9.8", "conteúdo já escrito em modules/krs_perks"),
        ("1563", "Karnages Polearm Restoration 2.0", "ok", "USAR",
         "19 patches corretos, sem restrição de versão", "mesma perícia que o Perkaholic destrava"),
        ("1569", "Karnages Shield Restoration", "ok", "USAR",
         "1 patch correto, sem restrição de versão", "destrava a perícia Escudo"),
        ("1009f", "Perkaholic PTF (pasta, 2024)", "bad", "DESCARTADO",
         "tabelas byte-idênticas ao .rar", "revisado e movido para Reviewed_Mods"),
        ("1765", "Restore Riposte", "bad", "DESCARTADO",
         "só difere no nível (8 contra 10)", "revisado e movido para Reviewed_Mods"),
        ("1990", "Veteran Hunting", "warn", "AVALIAR",
         "4 patches corretos, manifest só 1.9.6", "1 perk de caça + 7 almas alteradas"),
        ("1375", "No Aim Spread", "warn", "AVALIAR",
         "6 patches corretos, manifest até 1.9.7", "usa a rota perk em vez de rpg_param"),
        ("1629", "Exclusive Master Strikes", "bad", "NÃO USAR",
         "substitui soul2perk inteira (44 mil linhas)", "e o manifest só lista 1.9.6"),
        ("770", "Perkaholic 1.07", "bad", "NÃO USAR",
         "substitui 5 tabelas e grava fora da pasta", "quarentena: path traversal"),
        ("85", "Perkaholic 1.05", "bad", "NÃO USAR",
         "tabelas da era 1.3: derruba 66 perks", "e apaga 2 colunas de 541 linhas"),
    ]
    rows_v = "".join(
        f'<tr class="v-{k}"><td><b>{esc(lbl)}</b><div class="muted">id {i}</div></td>'
        f'<td>{chip(k, tag)}</td><td>{esc(how)}</td><td class="muted">{esc(note)}</td></tr>'
        for i, lbl, k, tag, how, note in VERD)

    # ---------------------------------------------------------------- perks
    perks = sorted(balance["new_perks"], key=lambda p: (p["skill"], int(p["level"] or 0),
                                                        p["name"]))
    skills = sorted({p["skill"] for p in perks})
    rows_p = ""
    for p in perks:
        # the change this perk makes, shown like the table of changes to existing content:
        # a higher tier replaces the value of the tier below; a first-tier perk starts from nothing
        if p.get("replaces"):
            change = "<br>".join(
                f'<code class="was">{esc(s["from"])}</code><span class="arrow">→</span>'
                f'<code class="is">{esc(s["to"])}</code>'
                f'<div class="muted">substitui {esc(s["from_buff"])}</div>'
                for s in p["replaces"])
        elif any(e["params"] for e in p["effects"]):
            change = "<br>".join(
                f'<code class="was">sem o perk</code><span class="arrow">→</span>'
                f'<code class="is">{esc(e["params"])}</code>'
                for e in p["effects"] if e["params"])
        else:
            change = '<span class="muted">nada mensurável nesta tabela</span>'
        eff = " · ".join(e["params"] for e in p["effects"] if e["params"])
        human = "<br>".join(filter(None, (explain(e["params"]) for e in p["effects"])))
        if not human:
            human = ('<i>sem efeito numérico nesta tabela</i> <span class="dim">— o perk existe, '
                     'mas o que ele faz não vem de <code>params</code>: é script ou uma regra de '
                     'sobreposição entre perks</span>')
        rows_p += (f'<tr data-skill="{esc(p["skill"])}">'
                   f'<td>{esc(p["skill"])}</td>'
                   f'<td class="num">{esc(p["level"] or "-")}</td>'
                   f'<td><b>{esc(p["name"])}</b></td>'
                   f'<td class="chg">{change}</td>'
                   f'<td class="why">{human}</td>'
                   f'</tr>')
    filters = "".join(f'<button class="f" data-skill="{esc(s)}">{esc(s)}</button>'
                      for s in skills)

    # ---------------------------------------------------------------- balance changes
    NOTE = {
        "perk_heavy_swing": ("Golpe pesado", "+3% de dano vira +20% de dano. É a maior "
                             "alteração do pacote e vale para QUALQUER arma com o perk."),
        "perk_art_admirer_reward": ("Apreciador de arte", "+1 vira +2 de carisma. Afeta preços e "
                                    "diálogos o jogo inteiro."),
        "perk_reading_Cushion": ("Almofada de leitura", "leitura 1,5x vira 2x. Combina com o "
                                 "ReadingXpPerHour que o krs_items já ajusta."),
        "perk_like_a_feather": ("Leve como pena", "dano de queda 0,7 vira 0,75: uma suavização "
                                "(menos proteção que o vanilla do perk)."),
        "perk_against_all_odds": ("Contra todas as chances", "só ícone e ordem na interface; "
                                  "nenhum número de jogo muda."),
    }
    rows_b = ""
    for b in balance["changed_buffs"]:
        d = b["diff"]
        name, note = NOTE.get(b["name"], (b["name"], ""))
        if "params" in d:
            before, after = d["params"]
            change = (f'<code class="was">{esc(before)}</code>'
                      f'<span class="arrow">→</span><code class="is">{esc(after)}</code>')
            human = (f'{explain(before, long=False)}<span class="arrow">→</span>'
                     f'{explain(after, long=False)}')
            m = re.match(r"^([A-Za-z_]+)[*+\-]", before.strip())
            info = CODES.get(m.group(1)) if m else None
            if info:
                human += f'<div class="dim" style="margin-top:4px">{esc(info[2])}</div>'
        else:
            change = "<code>" + esc(", ".join(f"{k}: {v[0] or '—'}→{v[1] or '—'}"
                                              for k, v in d.items())) + "</code>"
            human = "só interface"
        rows_b += (f'<tr><td><b>{esc(name)}</b><div class="muted">{esc(b["name"])}</div></td>'
                   f'<td>{change}</td><td>{human}</td>'
                   f'<td class="muted">{esc(note)}</td></tr>')

    cp = balance["changed_perks"][0] if balance["changed_perks"] else None
    rename = ""
    if cp:
        rename = (f'<code class="was">{esc(cp["was"]["perk_name"])} (nível '
                  f'{esc(cp["was"]["level"])})</code><span class="arrow">→</span>'
                  f'<code class="is">{esc(cp["name"])} (nível {esc(cp["level"])})</code>')

    # ---------------------------------------------------------------- glossary of effect codes
    used = set()
    for p in perks:
        for e in p["effects"]:
            for part in re.split(r"[,;]", e["params"] or ""):
                m = re.match(r"^([A-Za-z_]+)[*+\-]", part.strip())
                if m:
                    used.add(m.group(1))
    rows_g = ""
    for code in sorted(used, key=str.lower):
        info = CODES.get(code) or CODES.get(code.lower())
        if not info:
            continue
        name, better, what, seen, sure = info
        rows_g += (
            f'<tr><td><code>{esc(code)}</code></td>'
            f'<td><b>{esc(name)}</b><div class="muted">{"maior é melhor" if better == "up" else "menor é melhor"}</div></td>'
            f'<td>{esc(what)}</td>'
            f'<td class="muted">lido de: {esc(seen)}</td>'
            f'<td>{chip("ok", "confirmado") if sure else chip("warn", "deduzido")}</td></tr>')

    counts = {s: sum(1 for p in perks if p["skill"] == s) for s in skills}
    bars = "".join(
        f'<div class="bar"><span class="bl">{esc(s)}</span>'
        f'<span class="bt" style="width:{counts[s] / max(counts.values()) * 100:.0f}%"></span>'
        f'<span class="bn">{counts[s]}</span></div>' for s in
        sorted(skills, key=lambda s: -counts[s]))

    return f"""<title>Bancada de Perks</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo+Narrow:wght@500;700&family=Source+Sans+3:wght@400;600&family=JetBrains+Mono:wght@400;700&display=swap">
<style>
/* layout: uma coluna de leitura, tabelas largas rolam dentro do próprio quadro */
:root {{
  --bg:#f7f7f4; --surface:#ffffff; --line:#e0e0d8; --ink:#16181b; --ink2:#55585e;
  --ink3:#8b8e94; --accent:#2f6f9f; --accent-soft:#eaf2f8;
  --ok:#1a7f58; --ok-soft:#e9f5ef; --warn:#a9741a; --warn-soft:#fbf3e3;
  --bad:#b3372f; --bad-soft:#fbecea;
  --display:"Archivo Narrow",system-ui,sans-serif; --body:"Source Sans 3",system-ui,sans-serif;
  --mono:"JetBrains Mono",ui-monospace,Consolas,monospace;
  color-scheme: light;
}}
@media (prefers-color-scheme: dark) {{ :root:not([data-theme="light"]) {{
  --bg:#15171a; --surface:#1c1f23; --line:#2e3237; --ink:#f2f3f4; --ink2:#b4b8bf;
  --ink3:#80858d; --accent:#6fa9d6; --accent-soft:#1d2a35;
  --ok:#5fc295; --ok-soft:#16281f; --warn:#d6a44f; --warn-soft:#2a2316;
  --bad:#e8847c; --bad-soft:#2c1a18; color-scheme: dark;
}} }}
:root[data-theme="dark"] {{
  --bg:#15171a; --surface:#1c1f23; --line:#2e3237; --ink:#f2f3f4; --ink2:#b4b8bf;
  --ink3:#80858d; --accent:#6fa9d6; --accent-soft:#1d2a35;
  --ok:#5fc295; --ok-soft:#16281f; --warn:#d6a44f; --warn-soft:#2a2316;
  --bad:#e8847c; --bad-soft:#2c1a18; color-scheme: dark;
}}
body {{ background:var(--bg); color:var(--ink); font-family:var(--body); font-size:16px;
  line-height:1.55; margin:0; }}
.wrap {{ max-width:70rem; margin:0 auto; padding-inline:16px; padding-block:40px 64px; }}
h1,h2,h3 {{ font-family:var(--display); text-wrap:balance; margin:0; letter-spacing:-.01em; }}
h1 {{ font-size:clamp(2rem,5vw,3rem); line-height:1.05; }}
h2 {{ font-size:1.6rem; margin-top:2.6rem; padding-top:1.4rem; border-top:2px solid var(--ink); }}
h3 {{ font-size:1.12rem; margin-top:1.6rem; }}
p {{ margin:.6rem 0; max-width:65ch; }}
.lead {{ font-size:1.1rem; color:var(--ink2); }}
.muted {{ color:var(--ink3); font-size:.84rem; line-height:1.35; }}
.eyebrow {{ font-family:var(--display); text-transform:uppercase; letter-spacing:.14em;
  font-size:.78rem; color:var(--accent); font-weight:700; }}
code {{ font-family:var(--mono); font-size:.84em; background:var(--accent-soft);
  padding:.1em .35em; border-radius:3px; }}
.tiles {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(150px,1fr)); gap:12px;
  margin:1.6rem 0; }}
.tile {{ background:var(--surface); border:1px solid var(--line); border-radius:10px;
  padding:14px 16px; }}
.tile .n {{ font-family:var(--display); font-size:2rem; line-height:1; font-variant-numeric:tabular-nums; }}
.tile .l {{ font-size:.82rem; color:var(--ink2); margin-top:4px; }}
.tile.hi {{ background:var(--accent-soft); border-color:var(--accent); }}
.tablebox {{ overflow-x:auto; border:1px solid var(--line); border-radius:10px;
  background:var(--surface); margin:1rem 0; }}
table {{ width:100%; border-collapse:collapse; font-size:.9rem; min-width:0; }}
th {{ font-family:var(--display); text-align:left; text-transform:uppercase; font-size:.72rem;
  letter-spacing:.08em; color:var(--ink3); padding:10px 12px; border-bottom:1px solid var(--line);
  white-space:nowrap; }}
td {{ padding:9px 12px; border-bottom:1px solid var(--line); vertical-align:top; }}
tr:last-child td {{ border-bottom:0; }}
td.num {{ text-align:right; font-variant-numeric:tabular-nums; }}
.chip {{ display:inline-block; font-family:var(--display); font-weight:700; font-size:.72rem;
  letter-spacing:.06em; padding:3px 9px; border-radius:20px; white-space:nowrap; }}
.chip.ok {{ background:var(--ok-soft); color:var(--ok); }}
.chip.warn {{ background:var(--warn-soft); color:var(--warn); }}
.chip.bad {{ background:var(--bad-soft); color:var(--bad); }}
.why {{ font-size:.86rem; line-height:1.5; }}
.chg {{ font-size:.8rem; line-height:1.7; white-space:nowrap; }}
.chg .muted {{ white-space:normal; margin-top:2px; }}
.why b {{ font-weight:600; }}
.dim {{ color:var(--ink3); }}
.was {{ background:var(--bad-soft); color:var(--bad); text-decoration:line-through; }}
.is {{ background:var(--ok-soft); color:var(--ok); font-weight:700; }}
.arrow {{ color:var(--ink3); margin:0 .45em; }}
.note {{ border-left:3px solid var(--accent); background:var(--surface); padding:12px 16px;
  border-radius:0 8px 8px 0; margin:1.2rem 0; }}
.note.warn {{ border-color:var(--warn); background:var(--warn-soft); }}
.note.bad {{ border-color:var(--bad); background:var(--bad-soft); }}
.note.ok {{ border-color:var(--ok); background:var(--ok-soft); }}
.note .t {{ font-family:var(--display); text-transform:uppercase; letter-spacing:.1em;
  font-size:.74rem; color:var(--ink3); font-weight:700; }}
.note p {{ margin:.35rem 0 0; }}
.filters {{ display:flex; flex-wrap:wrap; gap:6px; margin:1rem 0 .4rem; }}
button.f {{ font-family:var(--display); font-size:.84rem; font-weight:500; padding:5px 12px;
  border-radius:20px; border:1px solid var(--line); background:var(--surface); color:var(--ink2);
  cursor:pointer; }}
button.f[aria-pressed="true"] {{ background:var(--accent); border-color:var(--accent);
  color:#fff; font-weight:700; }}
button.f:focus-visible {{ outline:2px solid var(--accent); outline-offset:2px; }}
.bars {{ display:grid; gap:6px; margin:1rem 0; }}
.bar {{ display:grid; grid-template-columns:9rem 1fr 2.2rem; align-items:center; gap:10px; }}
.bar .bl {{ font-size:.84rem; color:var(--ink2); }}
.bar .bt {{ height:14px; background:var(--accent); border-radius:0 4px 4px 0; display:block; }}
.bar .bn {{ font-family:var(--display); font-weight:700; font-variant-numeric:tabular-nums; }}
.steps {{ counter-reset:s; display:grid; gap:14px; margin:1.2rem 0; }}
.step {{ display:grid; grid-template-columns:2rem 1fr; gap:12px; }}
.step::before {{ counter-increment:s; content:counter(s); font-family:var(--display);
  font-weight:700; color:var(--accent); background:var(--accent-soft); border-radius:50%;
  width:2rem; height:2rem; display:grid; place-items:center; }}
.step h3 {{ margin:.1rem 0 .2rem; }}
.pre {{ font-family:var(--mono); font-size:.8rem; background:var(--surface);
  border:1px solid var(--line); border-radius:8px; padding:12px 14px; overflow-x:auto;
  white-space:pre; margin:.8rem 0; }}
.pre .add {{ color:var(--ok); }} .pre .del {{ color:var(--bad); }}
.pre .cmt {{ color:var(--ink3); }}
footer {{ margin-top:3rem; padding-top:1rem; border-top:1px solid var(--line);
  font-size:.82rem; color:var(--ink3); }}
@media (max-width:640px) {{ .bar {{ grid-template-columns:7rem 1fr 2rem; }} }}
</style>

<div class="wrap">
<div class="eyebrow">Kingdom Refinement Suite · bancada de perks · jogo 1.9.8</div>
<h1>Perkaholic e os outros mods de perk</h1>
<p class="lead">As 10 instâncias que existem em <code>Installed_to_review</code>, abertas e
comparadas com as tabelas do jogo. O foco desta página é o <b>balanceamento</b>: cada perk novo com
o efeito que concede, e cada alteração em conteúdo que já existe, para você confirmar ou recusar
uma por uma.</p>

<div class="tiles">
  <div class="tile hi"><div class="n">56</div><div class="l">perks novos do Perkaholic</div></div>
  <div class="tile"><div class="n">5</div><div class="l">efeitos do jogo alterados</div></div>
  <div class="tile"><div class="n">2</div><div class="l">perícias destravadas</div></div>
  <div class="tile"><div class="n">2</div><div class="l">instâncias revisadas e descartadas</div></div>
</div>

<h2>Veredito de cada instância</h2>
<div class="tablebox"><table>
<thead><tr><th>Instância</th><th>Veredito</th><th>Como aplica</th><th>Observação</th></tr></thead>
<tbody>{rows_v}</tbody></table></div>
<p class="muted">Cópias em <code>Mods WIP folder\\Perks\\perkaholic-riposte-workbench</code>:
<code>_sources/</code> originais intactos, <code>extracted/</code> abertos para leitura,
<code>notes/</code> os dados desta página.</p>

<h2>O conteúdo do Perkaholic</h2>
<p>Os 56 perks novos, distribuídos pelas árvores de perícia. Nenhum deles existe no jogo, então
<b>não há conflito de linha</b> com outros mods — eles só somam.</p>
<div class="bars">{bars}</div>

<h3>Cada perk e o efeito que ele concede</h3>
<div class="note"><div class="t">Em pausa</div>
<p>Os 56 perks do Perkaholic já foram decididos e aplicados, com as suas correções pontuais. A
tabela completa sai de cena por enquanto — ela volta aqui, <b>só com as linhas envolvidas</b>, se
alguma instância futura colidir com elas. A última revisão (1563) não colidiu: nenhum
<code>perk_id</code> em comum.</p></div>

<h3>Como ler os códigos de efeito</h3>
<p>O jogo guarda o efeito como uma fórmula curta: três letras de estatística, um operador e um
valor. <code>wat*1.05</code> multiplica por 1,05, ou seja <b>+5%</b>; <code>wac*0.9</code>
multiplica por 0,9, ou seja <b>−10%</b> — e nesse caso menos é melhor, porque o código é um
<i>custo</i>. Por isso a coluna acima diz sempre se a mudança <b>melhora</b> ou <b>piora</b> para
o jogador, em vez de só mostrar o sinal.</p>
<p class="muted">O significado de cada código foi lido dos buffs que o <b>próprio jogo</b> já usa
com ele — a coluna "lido de" mostra quais. Onde vários buffs concordam, está marcado como
confirmado; onde só um ou dois usam o código, está marcado como deduzido e merece um teste em jogo
antes de virar decisão de balanceamento.</p>
<div class="tablebox"><table>
<thead><tr><th>Código</th><th>Estatística</th><th>O que faz em jogo</th><th>Evidência</th>
<th>Confiança</th></tr></thead>
<tbody>{rows_g}</tbody></table></div>

<h2>As alterações em conteúdo que já existe</h2>
<p>Esta é a parte que exige decisão. São poucas linhas, mas valem para o jogo inteiro e
<b>disputam a linha</b> com qualquer outro mod que as toque.</p>

<h3>Cinco efeitos de perks do jogo</h3>
<div class="tablebox"><table>
<thead><tr><th>Perk do jogo</th><th>Mudança</th><th>Leitura</th><th>Questão de balanceamento</th></tr></thead>
<tbody>{rows_b}</tbody></table></div>

<h3>Um perk renomeado e movido de nível</h3>
<p>{rename}</p>
<p class="muted">Mesmo <code>perk_id</code>, nome e descrição novos. Quem já tem o perk na partida
continua com ele; muda o rótulo e o nível exigido.</p>

<h3>A perícia Armas de haste</h3>
<div class="pre"><span class="cmt">skill__perkaholic.xml — uma linha</span>
&lt;row skill_id="23" skill_name="weapon_large" <span class="del">hidden="True"</span> <span class="add">hidden="False"</span> ... /&gt;</div>
<div class="note warn"><div class="t">Colisão direta</div>
<p>O <b>1563 Karnages Polearm Restoration</b> escreve <b>exatamente esta linha</b>, com o mesmo
valor. Os dois destravam a mesma perícia. Não quebra nada — mas instalar os dois é redundante, e
quem carregar por último manda. O 1563 ainda traz 3 perks de combo de haste e 93 armas ajustadas;
o Perkaholic traz 10 perks de haste. Escolha de qual lado vem a árvore de haste.</p></div>

<h3>Três exclusividades e 17 sobreposições</h3>
<p>Três pares de perks novos que não podem coexistir (<code>perk2perk_exclusivity</code>) e 17
regras de <code>perk_buff_override</code>, em que um perk de nível maior substitui o efeito do
menor — o padrão que o jogo usa para linhas I/II/III, como os três Steady Shot.</p>

<h2>Duas perguntas respondidas</h2>

<h3>Os níveis escalam junto com o jogo?</h3>
<p>Sim, e sem inflar poder. Os 56 perks ficam entre os níveis <b>3 e 14</b>, exatamente a faixa que
o jogo já usa (2 a 15). Três árvores — <b>Arco, Armas de haste e Desarmado</b> — não tinham
<i>nenhum</i> perk visível no jogo: o mod as cria do zero. Em <b>Machado</b> e <b>Maça</b> o jogo só
tem perks dos níveis 7 ao 14, e o mod preenche justamente a faixa vazia de 3 a 6.</p>
<div class="tablebox"><table>
<thead><tr><th>Perícia</th><th class="num">Perks do jogo</th><th>Níveis do jogo</th>
<th class="num">Novos</th><th>Níveis novos</th></tr></thead>
<tbody>
<tr><td>Arco</td><td class="num">0</td><td class="muted">—</td><td class="num">9</td><td>3–12</td></tr>
<tr><td>Armas de haste</td><td class="num">0</td><td class="muted">—</td><td class="num">10</td><td>3–12</td></tr>
<tr><td>Desarmado</td><td class="num">0</td><td class="muted">—</td><td class="num">8</td><td>3–12</td></tr>
<tr><td>Machado</td><td class="num">7</td><td>7–14</td><td class="num">7</td><td>3–12</td></tr>
<tr><td>Maça</td><td class="num">7</td><td>7–14</td><td class="num">7</td><td>3–12</td></tr>
<tr><td>Esgrima</td><td class="num">8</td><td>4–12</td><td class="num">4</td><td>6–9</td></tr>
<tr><td>Defesa</td><td class="num">6</td><td>4–12</td><td class="num">4</td><td>8–13</td></tr>
<tr><td>Atributo / geral</td><td class="num">73</td><td>2–14</td><td class="num">7</td><td>3–14</td></tr>
</tbody></table></div>
<div class="note ok"><div class="t">O ponto que importa</div>
<p>O pacote <b>não altera nenhum <code>rpg_param</code></b> — não existe arquivo desse tipo no
patch. Ou seja, você não ganha pontos de perk a mais: são 56 <b>opções</b> a mais para os mesmos
pontos. O efeito é mais escolha, não mais poder.</p></div>

<h3>Os nomes dos perks foram inventados?</h3>
<p><b>Sim, os 56 são do autor do mod.</b> O pacote traz 124 chaves de texto próprias (56 nomes +
56 descrições + as do Featherweight) em 13 idiomas, e <b>nenhuma</b> delas existe nas 81.033 chaves
do jogo. Não são nomes de conteúdo cortado da Warhorse: são criações do autor, com tradução feita
por ele.</p>
<div class="note warn"><div class="t">Uma colisão de nome</div>
<p><b>Serration</b> é o único nome que já existe como perk visível do jogo. Dois perks diferentes
vão aparecer com o mesmo nome na interface. Vale renomear o novo.</p></div>
<p class="muted">A wiki que você indicou não abriu (o servidor respondeu 402), então a verificação
foi feita contra os arquivos do próprio jogo — evidência mais forte de qualquer modo.</p>

<h2>O que entrou no seu módulo</h2>
<p>O conteúdo do Perkaholic foi escrito em <code>modules/krs_perks</code> com as suas correções.
Todas as linhas saem com as 14 colunas da tabela vanilla e sufixo <code>__krs_perks</code>;
<code>check_patch_names.py</code> passou com <b>0 problemas</b>.</p>
<div class="tablebox"><table>
<thead><tr><th>Item</th><th>Alteração</th><th>Decisão</th></tr></thead>
<tbody>
<tr><td><b>Golpe pesado</b><div class="muted">perk_heavy_swing</div></td>
<td class="chg"><code class="was">wat*1.2,wac*1.1</code><span class="arrow">→</span><code class="is">wat*1.07,wac*1.1</code>
<div class="muted">o jogo tem wat*1.03</div></td>
<td>sua correção: +20% virou +7%</td></tr>
<tr><td><b>Almofada de leitura</b><div class="muted">perk_reading_Cushion</div></td>
<td class="chg"><code class="was">erq*2</code><span class="arrow">→</span><code class="is">erq*1.5</code></td>
<td>revertido ao valor do jogo: a linha não é enviada</td></tr>
<tr><td><b>Like a feather</b><div class="muted">nível 1 da escada</div></td>
<td class="chg"><code class="was">Featherweight I, nível 5</code><span class="arrow">→</span><code class="is">Like a feather, nível 4</code></td>
<td>nome e nível do jogo restaurados: a linha não é enviada</td></tr>
<tr><td><b>Like a Feather II / III</b></td>
<td class="chg"><code class="was">fdm*0.5 / fdm*0.25</code><span class="arrow">→</span><code class="is">fdm*0.60 / fdm*0.45</code>
<div class="muted">a escada ficou 0,75 → 0,60 → 0,45</div></td>
<td>seus valores; nomes revertidos em 13 idiomas</td></tr>
<tr><td><b>Townsman</b></td>
<td class="chg"><code class="was">sem pré-requisito</code><span class="arrow">→</span><code class="is">parent = Highborn</code></td>
<td>sua regra</td></tr>
<tr><td><b>Yokel</b></td>
<td class="chg"><code class="was">sem pré-requisito</code><span class="arrow">→</span><code class="is">parent = Lowborn</code></td>
<td>sua regra</td></tr>
</tbody></table></div>
<div class="note warn"><div class="t">Duas alterações que ficaram de fora esperando você</div>
<p>O Perkaholic também mexe em <b>Apreciador de arte</b> (<code>cha+1</code> → <code>cha+2</code>,
dobra o carisma) e em <b>Contra todas as chances</b> (só ícone e ordem de interface). Você não se
pronunciou sobre elas, e como balanceamento não se decide sozinho, elas <b>não foram enviadas</b> —
mas também não foram descartadas: estão em <code>tools/build_krs_perks.py</code>, na tabela
<code>BUFF_RULES</code>, com <code>include=False</code>. Trocar para <code>True</code> as inclui.</p></div>
<div class="tablebox"><table>
<thead><tr><th>Arquivo gerado</th><th class="num">Linhas</th><th>Conteúdo</th></tr></thead>
<tbody>
<tr><td class="mono">perk__krs_perks.xml</td><td class="num">58</td><td>56 perks novos + as 2 linhas do Riposte que já eram suas</td></tr>
<tr><td class="mono">buff__krs_perks.xml</td><td class="num">58</td><td>56 efeitos novos + Golpe pesado e Like a feather corrigidos</td></tr>
<tr><td class="mono">perk_buff__krs_perks.xml</td><td class="num">56</td><td>ligações perk → efeito</td></tr>
<tr><td class="mono">perk_buff_override__krs_perks.xml</td><td class="num">17</td><td>as escadas I/II/III</td></tr>
<tr><td class="mono">perk2perk_exclusivity__krs_perks.xml</td><td class="num">3</td><td>pares mutuamente exclusivos</td></tr>
<tr><td class="mono">skill__krs_perks.xml</td><td class="num">1</td><td>destrava Armas de haste</td></tr>
</tbody></table></div>

<h2>Master Strike x Riposte: a diferenca real</h2>
<div class="note ok"><div class="t">Medido em jogo pelo autor do projeto</div>
<p>Com o perk Riposte destravado, <b>as duas tecnicas funcionam</b>, e o que escolhe entre elas e
a acao que voce toma no momento-chave:</p></div>
<div class="tablebox"><table>
<thead><tr><th>No momento-chave voce...</th><th>Sai</th><th>Como e</th></tr></thead>
<tbody>
<tr><td><b>defende</b> (botao de bloqueio)</td><td><b>Master Strike</b></td>
<td class="why">bloqueio e contra-ataque na mesma acao, sem defesa possivel para o oponente</td></tr>
<tr><td><b>ataca</b> (botao de ataque)</td><td><b>Riposte</b></td>
<td class="why">o contra-ataque sai automatico tambem - nao e o "bloqueio perfeito e depois eu
ataco" manual</td></tr>
</tbody></table></div>
<p>Ou seja: o perk que o <code>krs_perks</code> destrava e o <b>riposte de verdade</b>, e ele
convive com o Master Strike em vez de substitui-lo. A janela de tempo e a mesma; muda o botao.</p>

<div class="note bad"><div class="t">Onde eu errei, e por que</div>
<p>Eu disse que esse perk "nao tem efeito ligado" porque ele nao tem <b>nenhuma linha em
<code>perk_buff</code></b>. O raciocinio estava errado: <b>perks de comportamento de combate nao
carregam buff</b> - o motor le o proprio id do perk e muda o comportamento no codigo nativo. Riposte,
Hunt attack e a familia <code>ripo_*</code> sao todos assim. Ausencia de buff nao e ausencia de
efeito, e esse teste ficou registrado no metodo de review para nao se repetir.</p></div>

<div class="tablebox"><table>
<thead><tr><th>No jogo</th><th>Como se obtem</th><th>Nos arquivos</th></tr></thead>
<tbody>
<tr><td><b>Master Strike</b></td>
<td class="why">treino com o <b>Capitao Bernard</b> em "Train Hard, Fight Easy"; destrava para
todas as armas de uma vez</td>
<td class="why"><code>ripo_text_sword</code>, <code>_axe</code>, <code>_mace</code> -
<code>visibility=1</code>, <b>sem nivel</b> (nao se compra na arvore), em <b>0</b> almas de NPC.
Os textos "Master Strike: Sword/Axe/Mace" ja existem no jogo</td></tr>
<tr><td><b>Riposte</b></td>
<td class="why">no jogo base, <b>nao se obtem</b>: <code>visibility=0</code>. Destravado pelo
<code>krs_perks</code> na arvore de Defesa, nivel 10</td>
<td class="why"><code>ec4c5274</code>, arvore de <b>Defesa</b>, em <b>1937</b> almas de NPC. O nome
<code>perk_riposte_name</code> = "Riposte" existe no jogo; a descricao, nao - a que o modulo usa
foi escrita pelo autor do mod 1765</td></tr>
<tr><td><b>Hunt attack</b></td>
<td class="why">nao se obtem: <code>visibility=0</code></td>
<td class="why"><code>1627a1b6</code>, sem pericia e sem nivel, em <b>2392</b> almas. Tambem sem
buff - pelo mesmo motivo dos outros dois. O que ele faz exatamente continua desconhecido</td></tr>
</tbody></table></div>
<p class="muted">A wiki diz que <q>mods nao conseguem adicionar o Master Strike corretamente</q>.
Isso vale para o Master Strike; o Riposte, que e o que destravamos, voce ja confirmou funcionando.</p>

<h2>Garimpo: o que vale tirar de cada um</h2>

<h3>1629 Exclusive Master Strikes <span class="chip bad">fora</span></h3>
<p>Fora. O mecanismo dele e tirar o Hunt attack de 2391 almas e o riposte de outras ~712 -
exatamente o que voce <b>nao</b> quer, e e realista que os NPCs tenham. As duas linhas de perk que
sobrariam nao valem nada sozinhas: uma e um perk vazio de proposito, a outra torna visivel um
sinalizador sem efeito.</p>

<h3>1990 Veteran Hunting - tres pecas separadas</h3>
<p>O mod tem tres coisas independentes, e so a primeira e claramente boa.</p>
<div class="tablebox"><table>
<thead><tr><th>Peca</th><th>Alteracao</th><th>O que faz</th><th>Veredito</th></tr></thead>
<tbody>
<tr><td><b>1. Percepcao dos animais</b><div class="muted">7 linhas de soul</div></td>
<td class="chg"><code class="was">hearing=0, vision=0</code><span class="arrow">&#8594;</span><code class="is">hearing=40-100, vision=20-80</code></td>
<td class="why">No jogo, lebre, corco, corca, veado, javali e as duas ovelhas tem audicao e visao
<b>zeradas</b>: nao percebem voce por som nem por imagem. O mod liga os dois sentidos. E isso que
eu quis dizer com "exige aproximacao": hoje da para caminhar ate o bicho; com os sentidos ligados
ele reage e foge, entao voce precisa de distancia, silencio e arco</td>
<td><span class="chip ok">sim</span> 7 linhas, so adiciona</td></tr>
<tr><td><b>2. O perk oculto</b><div class="muted">perk + buff + ligacao + 2 arquivos Lua</div></td>
<td class="chg"><code class="was">nao existe</code><span class="arrow">&#8594;</span><code class="is">btw*3 permanente</code></td>
<td class="why">Sao tres linhas de tabela mais um script. O perk tem <code>visibility=0</code>:
voce nunca o ve nem escolhe. O Lua roda ao carregar a cena e faz
<code>player.soul:AddPerk(...)</code> - ou seja, <b>enfia o perk no jogador a forca</b>, para
aplicar um efeito permanente sem gastar ponto. E um truque de entrega, nao um perk de verdade</td>
<td><span class="chip warn">atencao</span> funciona, mas e efeito escondido</td></tr>
<tr><td><b>3. Wild at Heart</b><div class="muted">perk_animal_in_heart, do jogo</div></td>
<td class="chg"><code class="was">btw*0.4</code><span class="arrow">&#8594;</span><code class="is">btw*2</code></td>
<td class="why"><b>inverte o perk</b>: de uma reducao para um aumento. Provavelmente
<code>btw</code> e o quanto os animais percebem voce, e ai o perk deixaria de ajudar e passaria a
atrapalhar. Mas <code>btw</code> aparece em <b>um unico</b> lugar em todo o jogo - justamente
neste perk - entao a direcao nao e verificavel por leitura</td>
<td><span class="chip warn">atencao</span> precisa de teste em jogo</td></tr>
</tbody></table></div>
<div class="note"><div class="t">Sua nota sobre pontos de perk</div>
<p>Registrada para depois: conceder 1 ponto extra a cada 2 ou 3 niveis, para acompanhar as novas
opcoes. Isso e <code>rpg_param</code>, nao perk - fica fora deste modulo e entra quando voce
decidir o numero.</p></div>

<h3>1375 No Aim Spread <span class="chip bad">fora</span></h3>
<p>Fora, por sua decisao: o assunto arco e flecha vai inteiro para o modulo de arco. A tecnica que
ele usa - conceder o perk direto a alma do Henry por <code>soul2perk</code> - fica anotada para
la.</p>

<h3>770 e 85 <span class="chip bad">fora</span></h3>
<p>Fora, oficialmente. Mesmos 56 perks do 1009, mais regressoes de 2018/2019.</p>

<h2>1563 e 1569: as pericias que o jogo escondeu</h2>
<div class="note ok"><div class="t">O achado desta revisao</div>
<p>O jogo tem <b>15 pericias marcadas como ocultas</b>, quase todas com nome e descricao ja
escritos: Bardo, Cozinha, Ferraria, Pesca, Mineracao, Primeiros Socorros, Besta, <b>Escudo</b>,
Adaga, <b>Arma Longa</b>, Alfaiataria, Armadura, Forja de Armas, Sapataria e Jogatina. Nao e
conteudo que o mod inventa: e conteudo pronto que a Warhorse desligou.</p></div>
<div class="tablebox"><table>
<thead><tr><th>Mod</th><th>O que entrega</th><th>Leitura</th><th>Veredito</th></tr></thead>
<tbody>
<tr><td><b>1569</b> Shield Restoration</td>
<td class="chg"><code class="was">hidden=True</code><span class="arrow">&#8594;</span><code class="is">hidden=False</code>
<div class="muted">pericia 20, weapon_shield</div></td>
<td class="why"><b>1 arquivo, 1 linha.</b> Os textos <code>ui_skill_weapon_shield</code> e a
descricao ja existem no jogo - a pericia aparece pronta</td>
<td><span class="chip ok">sim</span> candidata mais limpa do lote</td></tr>
<tr><td><b>1563</b> Polearm Restoration</td>
<td class="chg"><code class="was">hidden=True</code><span class="arrow">&#8594;</span><code class="is">hidden=False</code>
<div class="muted">pericia 23 + 3 perks de combo + 16 tabelas</div></td>
<td class="why">restaura a arvore <b>e</b> o combate de haste: animacoes de alabarda, combos,
classes de arma, presets e 93 armas ajustadas</td>
<td><span class="chip warn">atencao</span> otimo conteudo, mas pesado</td></tr>
</tbody></table></div>
<h3>O que eu tinha deixado passar no 1563</h3>
<p>Voce perguntou se eu estava olhando todos os arquivos. <b>Nao estava</b> - eu vinha lendo so as
tabelas. O 1563 tem bem mais:</p>
<div class="tablebox"><table>
<thead><tr><th>Arquivo</th><th>O que e</th><th>Risco</th></tr></thead>
<tbody>
<tr><td class="mono">animations/.../kcd_male_database.adb</td>
<td>banco de animacoes masculinas inteiro, <b>6,4 MB</b></td>
<td><span class="chip bad">nao</span> substitui o arquivo do jogo: conflita com qualquer outro mod de animacao</td></tr>
<tr><td class="mono">kcd_male_controllerdefs.xml</td><td>definicoes do mannequin, 98 KB</td>
<td><span class="chip bad">nao</span> mesmo problema</td></tr>
<tr><td class="mono">4 x .bspace</td><td>blend spaces dos ataques de alabarda</td>
<td><span class="chip warn">atencao</span> especificos, risco baixo</td></tr>
<tr><td class="mono">4 x polearm.lua / _startup.lua</td>
<td>script; o conteudo lido e um comando de debug (<code>unequipitem</code>)</td>
<td><span class="chip warn">atencao</span> entregue em dois caminhos (Libs/Scripts e Scripts)</td></tr>
<tr><td class="mono">4 x .tbl</td><td>copias binarias das tabelas, formato antigo</td>
<td><span class="chip warn">atencao</span> redundantes com os .xml</td></tr>
</tbody></table></div>
<div class="note warn"><div class="t">A decisao do 1563</div>
<p>A parte de <b>dados</b> (pericia, 3 perks de combo, tabelas de arma e combate) e garimpavel
linha a linha. A parte de <b>animacao</b> nao: sao arquivos inteiros do jogo substituidos, e e
isso que faz o combate de haste existir. Da para pegar so os dados, mas ai as armas de haste
funcionam com as animacoes que o jogo ja tem - isso e teste em jogo, nao conclusao de leitura.</p></div>
<div class="note ok"><div class="t">Sem colisao com o Perkaholic</div>
<p>Comparei os <code>perk_id</code>: <b>nenhum em comum</b>. Os 3 do 1563 sao perks de
<b>combo</b> (pommelstrike, doublestab); os 10 do Perkaholic sao de atributo (Hypertrophy,
Regimental Training...). E a linha da pericia 23 e <b>identica</b> nos dois - quem carregar por
ultimo escreve o mesmo valor.</p></div>

<h2>Riposte: fica o seu</h2>
<p>Decidido. O <code>modules/krs_perks</code> continua dono das duas linhas do Riposte: declara
<code>&lt;modid&gt;</code>, traz as 14 colunas no cabeçalho e suporta 1.9.8 — o mod 1765 não faz
nenhuma das três coisas. A única diferença de conteúdo era o nível exigido (8 no mod, 10 no seu).</p>

<h2>Como montar o seu mod</h2>
<div class="steps">
  <div class="step"><div><h3>Copiar as linhas novas</h3>
  <p>Os 56 perks, 56 buffs, 55 ligações e 17 sobreposições do 1009 (.rar). São linhas inéditas:
  entram sem disputar nada.</p></div></div>
  <div class="step"><div><h3>Renomear o sufixo e completar o cabeçalho</h3>
  <div class="pre"><span class="del">perk__perkaholic.xml</span>  →  <span class="add">perk__krs_perks.xml</span>
<span class="cmt">e o &lt;header&gt; com as 14 colunas da tabela vanilla,
porque coluna que falta vira vazia (regra 5 medida)</span></div></div></div>
  <div class="step"><div><h3>Decidir as 5 alterações de balanceamento, uma a uma</h3>
  <p>Nenhuma é obrigatória para os perks novos funcionarem. A mais forte é o Golpe pesado
  (+3% → +20% de dano).</p></div></div>
  <div class="step"><div><h3>Escolher de onde vem a árvore de haste</h3>
  <p>Perkaholic ou 1563 — os dois destravam a perícia 23.</p></div></div>
  <div class="step"><div><h3>Validar antes de jogar</h3>
  <p><code>tools/check_patch_names.py</code> para nomes e linhas completas, depois
  <code>tools/gate.py</code> para ler as linhas de volta dentro do jogo.</p></div></div>
</div>

<div class="note"><div class="t">Limite desta leitura</div>
<p>Tudo aqui é o que está escrito nos arquivos, comparado com as tabelas do jogo 1.9.8. Nenhum mod
foi instalado ou executado, e nenhuma partida foi aberta: se um número é divertido ou equilibrado
em jogo, isto não diz.</p></div>

<footer>Gerado de <code>notes/analysis.json</code> e <code>notes/perkaholic_balance.json</code>
por <code>tools/perks_workbench_page.py</code>.</footer>
</div>

<script>
const btns = [...document.querySelectorAll("button.f")];
const rows = [...document.querySelectorAll("#perks tbody tr")];
btns.forEach(b => b.addEventListener("click", () => {{
  btns.forEach(o => o.setAttribute("aria-pressed", String(o === b)));
  const s = b.dataset.skill;
  rows.forEach(r => {{ r.hidden = Boolean(s) && r.dataset.skill !== s; }});
}}));
</script>
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--workbench", default=WORKBENCH)
    args = ap.parse_args()
    notes = os.path.join(args.workbench, "notes")
    analysis = json.load(open(os.path.join(notes, "analysis.json"), encoding="utf-8"))
    balance = json.load(open(os.path.join(notes, "perkaholic_balance.json"), encoding="utf-8"))
    out = os.path.join(notes, "perks-workbench.html")
    with open(out, "w", encoding="utf-8") as f:
        f.write(build(analysis, balance))
    print("wrote", out, f"({os.path.getsize(out) / 1024:.0f} KB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
