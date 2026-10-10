#!/usr/bin/env python3
"""
build_grade_b_page.py - builds the Grade B review page (Portuguese, one self-contained HTML file) and the two generated companions.

    python tools/build_grade_b_page.py [--out docs/mods-review/GRADE_B_REVIEW.html]

Reads the machine-derived files written by tools/grade_b_extract.py (grade_b_files.csv, grade_b_cells.csv, grade_b_text.csv, grade_b_newrows.json,
grade_b_scripts.json, grade_b_summary.json), the overlap tables of the whole graded set (mod_overlap.csv, mod_subcategories.csv) and the curated
text in tools/grade_b_data*.py. Opens no archive and runs nothing. Also writes docs/mods-review/GRADE_B.md and grade_b_intersections.csv.

Display standard of the project (memory 'feedback-display-padrao'): Portuguese, before -> after tables, a glossary with the evidence of each
code and a confidence mark on every claim (confirmado / deduzido / nao verificado).
"""
import argparse
import collections
import csv
import html
import itertools
import json
import os
import re
import statistics
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paths  # noqa: E402
import audit_tables as at  # noqa: E402
import params_info  # noqa: E402
import grade_b_data as D  # noqa: E402
from grade_b_page_style import CSS, JS  # noqa: E402

R = paths.MODS_REVIEW
GAME = os.environ.get("KCD_GAME", r"E:\Kingdom-Refinement-Suite\WIP_Mods\KingdomComeDeliverance")
CONF = {"c": ("confirmado", "lido nos arquivos, no jogo ou no log"), "d": ("deduzido", "inferido do nome, da ajuda ou do contexto"), "n": ("não verificado", "precisa de teste no jogo")}


def esc(t):
    return html.escape(str(t), quote=False)


def rich(t):
    t = esc(t)
    t = re.sub(r"`([^`]+)`", r"<code>\1</code>", t)
    t = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", t)

    def badge(m):
        k = m.group(1)
        return f'<span class="cf cf-{k}" title="{esc(CONF[k][0])}: {esc(CONF[k][1])}">{CONF[k][0]}</span>'
    return re.sub(r"\s*\^([cdn])\b", lambda m: " " + badge(m), t)


def chip(kind, text):
    return f'<span class="chip {kind}">{re.sub(r"`([^`]+)`", r"<code></code>", esc(text))}</span>'


def human(n):
    n = int(n)
    if n < 1024:
        return f"{n} B"
    if n < 1048576:
        return f"{n / 1024:.1f} KB".replace(".", ",")
    return f"{n / 1048576:.1f} MB".replace(".", ",")


def num(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def csvrows(name):
    return list(csv.DictReader(open(os.path.join(R, name), encoding="utf-8", newline="")))


# ------------------------------------------------------------------ data
FILES = csvrows("grade_b_files.csv")
CELLS = csvrows("grade_b_cells.csv")
TEXT = csvrows("grade_b_text.csv")
NEWROWS = json.load(open(os.path.join(R, "grade_b_newrows.json"), encoding="utf-8"))
SCRIPTS = json.load(open(os.path.join(R, "grade_b_scripts.json"), encoding="utf-8"))
SUMMARY = {(s["id"], s["archive"]): s for s in json.load(open(os.path.join(R, "grade_b_summary.json"), encoding="utf-8"))}
SUBC = {r["id"]: r for r in csvrows("mod_subcategories.csv")}
OVERLAP = {}
for _r in csvrows("mod_overlap.csv"):
    OVERLAP[(_r["table"], _r["key"])] = _r["mod_ids"].split()
IDS = [i for _, _, _, ids in D.SUBCATS for i in ids]
BIDS = set(IDS)

VAN = at.load_vanilla(GAME)
PARAMS = params_info.load(VAN["rpg_param"]["rows"])
SKILL = {r["skill_id"]: r["skill_name"] for r in VAN["skill"]["rows"]}
ROLE_PT = {"manifest": "manifest", "container (.pak)": "contêiner .pak", "table patch": "tabela", "localization": "texto", "Lua script": "script Lua", "config": "configuração",
           "documentation": "documentação", "texture or image": "textura/imagem", "model or material": "modelo/material", "animation": "animação", "audio": "áudio",
           "UI (flash)": "interface (flash)", "other xml": "outro xml", "nested archive": "arquivo aninhado", "other": "outro", "native or script (risk)": "nativo/script (risco)"}


def rel_pt(v):
    if v.startswith("new file"):
        return "arquivo novo (não existe no jogo)"
    if v.startswith("identical"):
        return "idêntico ao do jogo"
    if v.startswith("replaces the whole"):
        return "substitui a tabela inteira do jogo"
    if v.startswith("replaces the game"):
        return "substitui arquivo do jogo"
    if v.startswith("patches a game table"):
        return "patch de tabela (" + v[v.find("suffix"):].rstrip(")") + ")" if "suffix" in v else "patch de tabela"
    if v.startswith("patch of the game"):
        return "patch de texto do jogo"
    if v == "container":
        return "contêiner"
    if v in ("not readable", "table not in the game"):
        return "não legível" if v == "not readable" else "tabela inexistente no jogo"
    return v


def note_pt(n):
    n = re.sub(r"(\d+) new, (\d+) changed, (\d+) identical rows", r"\1 novas, \2 alteradas, \3 iguais ao jogo", n)
    n = re.sub(r", (\d+) game rows dropped", r", \1 linhas do jogo ausentes", n)
    n = re.sub(r"(\d+) strings changed, (\d+) new \(compared with the game's English text\)", r"\1 textos alterados, \2 novos (comparados com o inglês do jogo)", n)
    n = n.replace("Lua: new", "Lua: nova").replace("Lua: differs", "Lua: difere do jogo").replace("Lua: identical", "Lua: igual à do jogo")
    n = n.replace("malformed XML or not a table", "XML malformado ou não é tabela").replace("malformed XML", "XML malformado")
    return n


def role_pt(r):
    if r["path"].lower().endswith(".tbl"):
        return "tabela binária (.tbl)"
    return ROLE_PT.get(r["role"], r["role"])


def mod_name(i):
    if i in D.MODS:
        return D.MODS[i]["name"]
    return SUBC.get(i, {}).get("name", "(mod " + i + ")")


def mod_grade(i):
    return SUBC.get(i, {}).get("grade", "?")[:1]


# ------------------------------------------------------------------ per-mod machine facts
def files_of(mid):
    return [f for f in FILES if f["id"] == mid]


def row_signature(c):
    return (c["table"], c["key_raw"].replace("|", "/"))


def cells_of(mid):
    return [c for c in CELLS if c["id"] == mid]


def others_of(mid, limit=10):
    """other graded mods that write the same table rows, with counts"""
    cnt = collections.Counter()
    tabs = collections.defaultdict(collections.Counter)
    seen = set()
    for c in cells_of(mid):
        sig = row_signature(c)
        if sig in seen:
            continue
        seen.add(sig)
        for o in OVERLAP.get(sig, []):
            if o != mid:
                cnt[o] += 1
                tabs[o][c["table"]] += 1
    out = []
    for o, n in cnt.most_common(limit):
        out.append((o, n, ", ".join(f"{t} {k}" for t, k in tabs[o].most_common(3))))
    return out, len(cnt)


def table_summary(mid):
    tabs = collections.OrderedDict()
    for (i, arc), s in SUMMARY.items():
        if i != mid:
            continue
        for t, v in s["tables"].items():
            e = tabs.setdefault(t, {"new": 0, "changed": 0, "same": 0, "dropped": 0, "whole": False, "files": 0})
            for k in ("new", "changed", "same", "dropped", "files"):
                e[k] += v[k]
            e["whole"] = e["whole"] or v["whole"]
    return tabs


def problems_of(mid):
    out = []
    for (i, arc), s in SUMMARY.items():
        if i == mid:
            out += s.get("problems", [])
            out += [f"listagem: {x}" for x in s.get("listing_findings", [])]
    return out


def row_values():
    """(mod, table, key_raw) -> {column: new value}; new rows carry their full row"""
    vals = collections.defaultdict(dict)
    for c in CELLS:
        if c["kind"] == "changed" and (c["id"] != "1483" or "2X" in c["container"]):
            vals[(c["id"], c["table"], c["key_raw"].replace("|", "/"))][c["column"]] = c["new"]
    for n in NEWROWS:
        if n["id"] == "1483" and "2X" not in n["container"]:
            continue
        vals[(n["id"], n["table"], n["key_raw"].replace("|", "/"))] = {k: v for k, v in n["row"].items()}
    return vals


ROWVALS = row_values()
WHOLE = {}
for (_i, _arc), _s in SUMMARY.items():
    for _t, _v in _s["tables"].items():
        if _v["whole"]:
            WHOLE[(_i, _t)] = True


def same_val(a, b):
    x, y = num(a), num(b)
    if x is not None and y is not None:
        return abs(x - y) < 1e-9
    return str(a) == str(b)


def pair_stats():
    by_mod = collections.defaultdict(lambda: collections.defaultdict(set))
    for (m, t, k), _ in ROWVALS.items():
        by_mod[m][t].add(k)
    out = []
    for a, b in itertools.combinations(IDS, 2):
        shared_tabs = sorted(set(by_mod[a]) & set(by_mod[b]))
        if not shared_tabs:
            continue
        rows = same = diff = comp = 0
        per_table = collections.Counter()
        cells_same = cells_diff = 0
        for t in shared_tabs:
            for k in by_mod[a][t] & by_mod[b][t]:
                va, vb = ROWVALS[(a, t, k)], ROWVALS[(b, t, k)]
                cols = set(va) & set(vb)
                rows += 1
                per_table[t] += 1
                if not cols:
                    comp += 1
                    continue
                d = [c for c in cols if not same_val(va[c], vb[c])]
                cells_same += len(cols) - len(d)
                cells_diff += len(d)
                if d:
                    diff += 1
                else:
                    same += 1
        whole = sorted(t for t in shared_tabs if WHOLE.get((a, t)) or WHOLE.get((b, t)))
        out.append({"a": a, "b": b, "tables": shared_tabs, "rows": rows, "rows_identical": same, "rows_conflict": diff, "rows_complementary": comp,
                    "cells_same": cells_same, "cells_diff": cells_diff, "per_table": per_table, "whole": whole})
    return out


def pair_kind(p):
    """Redundante / Redundante com divergência / Tabela inteira / Conflito direto / Complementar"""
    n = max(p["rows"], 1)
    if p["rows_identical"] / n >= 0.9:
        return "Redundante" if p["rows_conflict"] == 0 else "Redundante com divergência"
    if p["rows_identical"] / n >= 0.5 and p["rows_conflict"] / n <= 0.1:
        return "Redundante com divergência"
    if p["whole"]:
        return "Tabela inteira"
    if p["rows_conflict"]:
        return "Conflito direto"
    return "Complementar"


KIND_CHIP = {"Conflito direto": "bad", "Tabela inteira": "warn", "Redundante": "info", "Redundante com divergência": "info", "Complementar": "ok"}


PAIRS = pair_stats()


# ------------------------------------------------------------------ html pieces
def listing(items, empty="Nenhum encontrado."):
    if not items:
        return f'<p class="none">{esc(empty)}</p>'
    return "<ul>" + "".join(f"<li>{rich(i)}</li>" for i in items) + "</ul>"


def snippets(items):
    if not items:
        return '<p class="none">Nenhum trecho relevante.</p>'
    out = ""
    for title, code, expl in items:
        lines = []
        for ln in code.split("\n"):
            lines.append(f'<span class="add">{esc(ln)}</span>' if ln[:1] == "+" else esc(ln))
        out += (f'<figure class="snip"><figcaption>{rich(title)}</figcaption><pre><code>{chr(10).join(lines)}</code></pre><p>{rich(expl)}</p></figure>')
    return out


def file_table(rows):
    body = ""
    for r in rows:
        cont = r["container"].split("/")[-1] if r["container"] else ""
        body += (f'<tr><td class="mono wrap">{esc(cont)}</td><td class="mono wrap">{esc(r["path"])}</td><td>{esc(role_pt(r))}</td>'
                 f'<td class="num">{human(r["bytes"])}</td><td class="mono">{esc(r["sha256"][:12])}</td><td>{esc(rel_pt(r["vs_game"]))}</td><td class="wrap">{esc(note_pt(r["note"]))}</td></tr>')
    return ('<div class="scroll"><table class="t compact"><thead><tr><th>Pak / pasta</th><th>Caminho</th><th>Tipo</th><th>Tamanho</th><th>sha256</th><th>Em relação ao jogo</th><th>Observação</th></tr></thead>'
            f'<tbody>{body}</tbody></table></div>')


def ba_cell(v, kind):
    v = str(v)
    if v in ("-", ""):
        return "-"
    return f'<code class="{kind}">{rich(v)}</code>'


def fmt_val(v):
    if v is None:
        return "-"
    v = str(v)
    m = re.match(r'^\{"rpg_param_value": "([^"]*)"\}$', v)
    if m:
        v = m.group(1)
    return v if v != "" else "(vazio)"


def matrix(headers, rows, game_col=True):
    """rows: [(label, sublabel, game, [values])]; marks cells different from the game"""
    head = "".join(f'<th class="mod">{esc(h)}</th>' for h in headers)
    body = ""
    for label, sub, game, vals in rows:
        cells = ""
        for v in vals:
            if v is None:
                cells += '<td class="mod na">-</td>'
            else:
                cls = "same" if (game not in (None, "") and same_val(fmt_val(v).split(" ")[0], game)) else "diff"
                cells += f'<td class="mod {cls}">{esc(fmt_val(v))}</td>'
        sub_html = f'<span class="pdesc">{esc(sub)}</span>' if sub else ""
        body += f'<tr><td class="wrap"><b>{esc(label)}</b>{sub_html}</td><td class="game">{esc(game if game not in (None, "") else "-")}</td>{cells}</tr>'
    return (f'<div class="scroll"><table class="t compact matrix"><thead><tr><th>Item</th><th>Jogo 1.9.8</th>{head}</tr></thead><tbody>{body}</tbody></table></div>')


def resolve_params(spec):
    mods = spec["mods"]
    pc = {}
    hc = {}
    for c in CELLS:
        if c["id"] in mods and c["table"] == "rpg_param":
            pc[(c["id"], c["key"])] = fmt_val(c["new"])
        if c["id"] in mods and c["table"] == "perk_rpg_param_override" and c["key"].startswith("Hardcore Mode"):
            hc[(c["id"], c["key"].split(" / ")[-1])] = fmt_val(c["new"])
    rows = []
    for p in spec["params"]:
        info = PARAMS.get(p, {})
        game = info.get("default", "")
        vals = []
        for m in mods:
            v = pc.get((m, p))
            h = hc.get((m, p))
            if v is None and h is None:
                vals.append(None)
            else:
                vals.append((v if v is not None else "-") + (f" (HC {h})" if h is not None else ""))
        desc = info.get("desc") or "sem descrição na referência"
        src = info.get("source", "")
        rows.append((p, desc + (f" [{src}]" if src else ""), game, vals))
    out = matrix(mods, rows)
    if spec.get("extra"):
        out += _extra_table(spec["extra"])
    return out + '<p class="note">Valor do jogo: o da tabela `rpg_param` 1.9.8 quando existe; senão o valor que o motor devolveu na leitura de 1.9.6 (`rpg_constants_runtime.csv`). (HC) é a linha de `perk_rpg_param_override` do modo Hardcore. Célula amarela: valor diferente do jogo; verde: igual.</p>'.replace("`", "")


def _extra_table(extra):
    body = "".join(f'<tr><td>{rich(a)}</td><td>{ba_cell(b, "was")}</td><td>{ba_cell(c, "is")}</td></tr>' for a, b, c in extra)
    return f'<div class="scroll" style="margin-top:8px"><table class="t compact ba"><thead><tr><th>Outras linhas</th><th>Jogo</th><th>Mod</th></tr></thead><tbody>{body}</tbody></table></div>'


def resolve_cells(spec):
    mods = spec["mods"]
    table, column = spec["table"], spec["column"]
    var = spec.get("variant", {})
    data = collections.defaultdict(dict)
    labels, old = {}, {}
    for c in CELLS:
        if c["id"] in mods and c["table"] == table and c["column"] == column and c["kind"] == "changed":
            if c["id"] in var and var[c["id"]] not in c["container"]:
                continue
            data[c["key_raw"]][c["id"]] = c["new"]
            labels[c["key_raw"]] = c["key"]
            old[c["key_raw"]] = c["old"]
    keys = spec.get("keys")
    chosen = []
    if keys:
        for k in keys:
            for kr, lab in labels.items():
                if k.lower() in lab.lower() and kr not in chosen:
                    chosen.append(kr)
                    break
    else:
        chosen = sorted(labels, key=lambda x: labels[x])
    chosen = chosen[:spec.get("limit", 20)]
    rows = [(labels[k], "", old[k] if old[k] != "" else "(vazio)", [data[k].get(m) for m in mods]) for k in chosen]
    headers = [m + (" (" + var[m] + ")" if m in var else "") for m in mods]
    note = f'<p class="note">Coluna <code>{esc(column)}</code> da tabela <code>{esc(table)}</code>; {len(chosen)} itens escolhidos entre os que os mods tocam. Célula amarela: diferente do jogo.</p>'
    return matrix(headers, rows) + note


def resolve_wide(spec):
    mid = spec["mod"]
    cols = [tuple(c) for c in spec["cols"]]
    data = collections.defaultdict(dict)
    label = {}
    for c in CELLS:
        if c["id"] == mid and (c["table"], c["column"]) in cols and c["kind"] == "changed":
            data[c["key_raw"]][(c["table"], c["column"])] = (c["old"], c["new"])
            label[c["key_raw"]] = c["key"]
    keys = sorted(data, key=lambda k: label[k])[:spec.get("limit", 20)]
    head = "".join(f"<th>{esc(t)}.{esc(c)}</th>" for t, c in cols)
    body = ""
    for k in keys:
        cells = ""
        for col in cols:
            v = data[k].get(col)
            cells += f'<td class="num">{ba_cell(v[0] or "(vazio)", "was")} → {ba_cell(v[1] or "(vazio)", "is")}</td>' if v else '<td class="mute">-</td>'
        body += f'<tr><td class="wrap"><b>{esc(label[k])}</b></td>{cells}</tr>'
    return f'<div class="scroll"><table class="t compact ba"><thead><tr><th>Item</th>{head}</tr></thead><tbody>{body}</tbody></table></div>'


BUFF_CODES = [("wat", "dano da arma"), ("wac", "custo de vigor do ataque"), ("hlh / slh", "dano que a vida / o vigor sofrem"), ("srg", "regeneração de vigor"), ("mst", "vigor máximo"), ("ade", "eficácia da armadura"),
              ("dee", "dano ao equipamento do adversário"), ("bad", "ameaça (o inimigo foge)"), ("hko", "nocaute com tiro na cabeça"), ("ain", "chance de sangramento"), ("pac", "chance de envenenar"),
              ("was", "precisão (dispersão de tiro)"), ("asp", "velocidade do golpe"), ("cli", "clinch"), ("osb", "custo de bloqueio ao adversário"), ("spc", "fala"), ("str/agi", "atributos"), ("fdm", "dano de queda"),
              ("ibi", "tempo para sangrar até morrer"), ("dsl", "esquiva bêbado"), ("noi", "ruído"), ("rms", "velocidade de corrida")]


def resolve_perkcat(spec):
    mid = spec["mod"]
    perks = [n for n in NEWROWS if n["id"] == mid and n["table"] == "perk"]
    buff = {n["row"]["buff_id"]: n["row"] for n in NEWROWS if n["id"] == mid and n["table"] == "buff"}
    pb = collections.defaultdict(list)
    for n in NEWROWS:
        if n["id"] == mid and n["table"] == "perk_buff":
            pb[n["row"]["perk_id"]].append(n["row"]["buff_id"])
    txt = {t["key"]: t["new"] for t in TEXT if t["id"] == mid and "English" in t["container"]}
    rows = []
    for n in perks:
        p = n["row"]
        sk = SKILL.get(p["skill_selector"], "") if p.get("skill_selector") else ""
        who = sk if sk else (f"atributo (seletor {p['stat_selector']})" if p.get("stat_selector") else "-")
        formula = "; ".join(buff[b]["params"] for b in pb.get(p["perk_id"], []) if b in buff) or "(cadeia: troca o buff da perk anterior)"
        d = re.sub(r"<[^>]+>|&nbsp;|&lt;br/&gt;", " ", txt.get(p["perk_ui_desc"], ""))
        rows.append((who, int(p["level"] or 0), p["perk_name"], formula, " ".join(d.split())))
    rows.sort(key=lambda r: (r[0], r[1], r[2]))
    body = "".join(f'<tr><td>{esc(a)}</td><td class="num">{b}</td><td><b>{esc(c)}</b></td><td class="mono wrap">{esc(d)}</td><td class="wrap">{esc(e)}</td></tr>' for a, b, c, d, e in rows)
    legend = " ".join(f'<span class="badge">{esc(a)}</span> {esc(b)};' for a, b in BUFF_CODES)
    return (f'<div class="scroll"><table class="t compact"><thead><tr><th>Habilidade ou atributo</th><th>Nível</th><th>Perk</th><th>Fórmula do buff</th><th>Texto do jogo (inglês)</th></tr></thead><tbody>{body}</tbody></table></div>'
            f'<p class="note"><b>Legenda dos códigos:</b> {legend}</p>')


def balance_rows(b):
    r = b["rows"]
    if isinstance(r, list):
        if not r:
            return ""
        body = "".join(f'<tr><td>{rich(a)}</td><td>{ba_cell(x, "was")}</td><td>{ba_cell(y, "is")}</td></tr>' for a, x, y in r)
        return f'<div class="scroll"><table class="t compact ba"><thead><tr><th>Valor</th><th>Antes</th><th>Depois</th></tr></thead><tbody>{body}</tbody></table></div>'
    return {"params": resolve_params, "cells": resolve_cells, "wide": resolve_wide, "perkcat": resolve_perkcat}[r["type"]](r)


def balance_section():
    out = ""
    for b in D.BALANCE:
        dims = " ".join(chip("info", d) for d in b["dims"])
        scope_kind = "warn" if ("Propaga" in b["scope"]) else "ok"
        table = balance_rows(b)
        out += (f'<article class="bal" id="{b["id"]}"><header><span class="bid">{b["id"]}</span><h3>{rich(b["title"])}</h3><span class="bmods">mods {esc(b["mods"])}</span></header>'
                f'<p class="dims">{dims} {chip(scope_kind, "alcance: " + b["scope"])}</p>'
                f'<dl><dt>O que é</dt><dd>{rich(b["what"])}</dd>'
                + (f'<dt>Antes → depois</dt><dd>{table}</dd>' if table else "")
                + f'<dt>O que o valor representa</dt><dd>{rich(b["meaning"])}</dd><dt>Por que o autor mudou</dt><dd>{rich(b["why"])}</dd>'
                + f'<dt>Efeito prático esperado</dt><dd>{rich(b["effect"])}</dd><dt>Outros mods no mesmo parâmetro</dt><dd>{rich(b["others"])}</dd>'
                + f'<dt>Avaliação</dt><dd>{rich(b["verdict"])}</dd></dl></article>')
    return out


def classify_files(rows):
    added, patched, replaced = [], [], []
    for r in rows:
        if r["role"] in ("manifest", "container (.pak)"):
            continue
        if r["vs_game"].startswith("replaces"):
            replaced.append(r)
        elif r["role"] in ("table patch", "localization"):
            patched.append(r)
        elif r["vs_game"].startswith("new file"):
            added.append(r)
    return added, patched, replaced


def text_examples(mid, n=4):
    tx = [t for t in TEXT if t["id"] == mid]
    cnt = collections.Counter((t["container"].split("/")[-1], t["kind"]) for t in tx)
    langs = len({k[0] for k in cnt})
    ch = sum(v for k, v in cnt.items() if k[1] == "changed string")
    nw = sum(v for k, v in cnt.items() if k[1] == "new string")
    out = []
    if tx:
        out.append(f"{ch} textos alterados e {nw} novos, em {langs} pacote(s) de idioma.")
        seen = set()
        for t in tx:
            if t["key"] in seen or len(out) > n:
                continue
            seen.add(t["key"])
            out.append(f"`{t['key']}`: {t['old'][:60] or '(novo)'} → {t['new'][:90]}")
    return out


def overlap_html(mid):
    others, total = others_of(mid)
    pairs = [p for p in PAIRS if mid in (p["a"], p["b"])]
    h = ""
    if pairs:
        body = ""
        for p in sorted(pairs, key=lambda p: -p["rows"]):
            o = p["b"] if p["a"] == mid else p["a"]
            kind = pair_kind(p)
            body += (f'<tr><td class="mono">{o}</td><td>{esc(mod_name(o))}</td><td class="num">{p["rows"]}</td><td class="num">{p["cells_same"]} / {p["cells_diff"]}</td>'
                     f'<td>{chip(KIND_CHIP[kind], kind)}</td><td class="wrap">{esc(", ".join(f"{t} {n}" for t, n in p["per_table"].most_common(4)))}</td></tr>')
        h += ('<h5 style="margin:8px 0 4px">Com os outros mods do grau B (célula a célula)</h5><div class="scroll"><table class="t compact"><thead><tr><th>Mod</th><th>Nome</th><th>Linhas em comum</th><th>Células iguais / diferentes</th><th>Tipo</th><th>Tabelas</th></tr></thead>'
              f'<tbody>{body}</tbody></table></div>')
    if others:
        body = "".join(f'<tr><td class="mono">{o}</td><td>{esc(mod_name(o))}</td><td>{esc(mod_grade(o))}</td><td class="num">{n}</td><td class="wrap">{esc(t)}</td></tr>' for o, n, t in others)
        h += (f'<h5 style="margin:10px 0 4px">Com os outros 129 mods graduados (só linha em comum; {total} mods ao todo)</h5><div class="scroll"><table class="t compact"><thead><tr><th>Mod</th><th>Nome</th><th>Grau</th><th>Linhas em comum</th><th>Tabelas</th></tr></thead>'
              f'<tbody>{body}</tbody></table></div>')
    return h or '<p class="none">Nenhuma linha de tabela em comum com outro mod graduado.</p>'


def mod_card(mid, m, bidx):
    files = files_of(mid)
    added, patched, replaced = classify_files(files)
    subtitle = {k: n for k, n, _, _ in D.SUBCATS}[m["subcat"]]
    tabs = table_summary(mid)
    nfiles = len([f for f in files if f["role"] != "container (.pak)"])
    tabs_list = []
    for t, v in tabs.items():
        extra = []
        if v["whole"]:
            extra.append("**substitui a tabela inteira**" + (f", {v['dropped']} linhas do jogo ausentes" if v["dropped"] else ""))
        tabs_list.append(f"`{t}`: {v['new']} novas, {v['changed']} alteradas, {v['same']} iguais ao jogo" + (f" ({'; '.join(extra)})" if extra else ""))
    problems = problems_of(mid)
    fam = f'<span class="badge">família {esc(m["family"])}</span>' if m.get("family") else ""
    h = []
    fields = [("Status da revisão", [m["status"]]), ("Categoria e subcategoria", [f"Grau B (grande) › {subtitle}" + (f" · família {m['family']}" if m.get("family") else "")]),
              ("Carrega no 1.9.8?", [m["loads"]]), ("Propósito declarado", [m["purpose"]]), ("Comportamento observado (o que de fato faz)", m["observed"])]
    for label, items in fields:
        h.append(f'<section><h4>{esc(label)}</h4>{listing(items)}</section>')
    h.append(f'<section class="wide"><h4>Todos os arquivos ({nfiles})</h4>{file_table(files)}</section>')
    h.append('<section><h4>Arquivos adicionados</h4>' + listing([f"{r['path']} ({role_pt(r)})" for r in added]) + '</section>')
    h.append('<section><h4>Arquivos modificados (patches de tabela e de texto)</h4>' + listing([f"{r['path']}: {note_pt(r['note'])}" for r in patched[:40]] + ([f"... e mais {len(patched) - 40}"] if len(patched) > 40 else [])) + '</section>')
    h.append('<section><h4>Arquivos substituídos (do jogo)</h4>' + listing([r["path"] for r in replaced]) + '</section>')
    dropped = [f"`{t}`: {v['dropped']} linhas do jogo ausentes" for t, v in tabs.items() if v["whole"] and v["dropped"]]
    h.append('<section><h4>Arquivos / linhas removidos</h4>' + listing(dropped, "Nenhum arquivo do jogo é removido; nenhuma linha do jogo é apagada.") + '</section>')
    h.append('<section><h4>Tabelas tocadas</h4>' + listing(tabs_list, "Nenhuma tabela.") + '</section>')
    for label, key in (("Sistemas e mecânicas afetados", "systems"), ("Conteúdo novo introduzido", "newcontent"), ("Mudanças de status e valores", "stats"), ("Descrições e textos", "text"),
                       ("Ícones e assets", "assets"), ("Parâmetros importantes", "params")):
        items = list(m[key])
        if key == "text":
            items = items + text_examples(mid, 3)
        h.append(f'<section><h4>{esc(label)}</h4>{listing(items)}</section>')
    bal = "".join(f'<a class="chip info" href="#{b}">{b} {esc(bidx[b]["title"].split(" (")[0].replace("`", ""))}</a> ' for b in m["balance"])
    h.append(f'<section class="wide"><h4>Mudanças de balanceamento</h4><p>{bal or "<span class=none>Nenhuma mudança de balanceamento (mod de interface ou de conteúdo).</span>"}</p></section>')
    h.append(f'<section class="wide"><h4>Trechos relevantes e o que significam</h4>{snippets(m["snippets"])}</section>')
    for label, key in (("Dependências", "deps"), ("Sobreposição de arquivos com outros mods", "file_overlap"), ("Sobreposição funcional", "func_overlap"), ("Conflitos possíveis", "conflicts")):
        h.append(f'<section><h4>{esc(label)}</h4>{listing(m[key])}</section>')
    h.append(f'<section class="wide"><h4>Sobreposição medida (linhas e células)</h4>{overlap_html(mid)}</section>')
    h.append(f'<section><h4>Erros possíveis (a mão)</h4>{listing(m["errors"])}</section>')
    h.append(f'<section><h4>Achados automáticos de estrutura</h4>{listing([p[:260] for p in problems], "Nenhum achado automático.")}</section>')
    for label, key in (("Mudanças únicas e interessantes", "unique"), ("Possivelmente vale integrar", "keep"), ("Provavelmente rejeitar", "reject"), ("Perguntas para confirmar", "questions")):
        h.append(f'<section><h4>{esc(label)}</h4>{listing(m[key])}</section>')
    pos = next(p for sid, lst in D.RANK.items() for i, p, w in lst if i == mid)
    why = next(w for sid, lst in D.RANK.items() for i, p, w in lst if i == mid)
    h.append(f'<section class="wide"><h4>Posição na subcategoria</h4><p><b>{esc(m["rank_note"])}.</b> {rich(why)}</p></section>')
    h.append(f'<section class="wide"><h4>Ação recomendada</h4><p>{rich(m["action"])}</p></section>')
    return (f'<details class="mod" id="m{mid}" data-sub="{m["subcat"]}" data-verdict="{m["verdict"]}" data-text="{esc((mid + " " + m["name"] + " " + m["author"]).lower())}">'
            f'<summary><span class="mid">{mid}</span><span class="mname">{esc(m["name"])}</span>{fam}<span class="msub">{esc(subtitle)}</span>{chip(m["verdict"], m["verdict_text"])}</summary>'
            f'<div class="mbody">{"".join(h)}</div></details>')


def summary_table():
    rows = ""
    for sid, name, _, ids in D.SUBCATS:
        for i in ids:
            m = D.MODS[i]
            fs = [f for f in files_of(i) if f["role"] not in ("container (.pak)",)]
            tabs = table_summary(i)
            nrows = sum(v["new"] + v["changed"] for v in tabs.values())
            rows += (f'<tr data-sub="{sid}"><td class="mono">{i}</td><td><a href="#m{i}">{esc(m["name"])}</a></td><td>{esc(name)}</td><td class="num">{len(fs)}</td><td class="num">{nrows}</td>'
                     f'<td>{chip(m["verdict"], m["verdict_text"])}</td><td>{rich(m["purpose"][:150])}</td></tr>')
    return ('<div class="scroll"><table class="t"><thead><tr><th>Id</th><th>Mod</th><th>Subcategoria</th><th>Arquivos</th><th>Linhas novas+alteradas</th><th>Ação</th><th>Propósito</th></tr></thead>'
            f'<tbody>{rows}</tbody></table></div>')


def table_matrix(ids):
    tabs = collections.OrderedDict()
    for i in ids:
        for t, v in table_summary(i).items():
            tabs.setdefault(t, {})[i] = v
    head = "".join(f'<th class="mod">{i}</th>' for i in ids)
    body = ""
    for t, d in sorted(tabs.items(), key=lambda kv: (-len(kv[1]), kv[0])):
        cells = ""
        for i in ids:
            v = d.get(i)
            cells += (f'<td class="mod {"diff" if v["whole"] else "same"}">{v["new"] + v["changed"]}{"*" if v["whole"] else ""}</td>' if v else '<td class="mod na">-</td>')
        body += f'<tr><td class="mono">{esc(t)}</td>{cells}</tr>'
    return (f'<div class="scroll"><table class="t compact matrix"><thead><tr><th>Tabela</th>{head}</tr></thead><tbody>{body}</tbody></table></div>'
            '<p class="note">Cada número é linhas novas + alteradas do mod na tabela. Asterisco (amarelo): o mod substitui a tabela inteira (sem sufixo).</p>')


def subcat_section():
    out = ""
    for sid, name, blurb, ids in D.SUBCATS:
        rows = ""
        for mid, pos, why in D.RANK[sid]:
            m = D.MODS[mid]
            rows += f'<tr><td class="num">{pos}</td><td><a href="#m{mid}">{mid} {esc(m["name"])}</a></td><td>{chip(m["verdict"], m["verdict_text"])}</td><td>{rich(why)}</td></tr>'
        lead, feats = D.FEATURES[sid]
        fb = "".join(f"<tr><td>{rich(a)}</td><td><b>{esc(b)}</b></td><td>{esc(c)}</td><td>{rich(d)}</td></tr>" for a, b, c, d in feats)
        pairs = [p for p in PAIRS if p["a"] in ids and p["b"] in ids]
        pb = ""
        for p in sorted(pairs, key=lambda p: -p["rows"]):
            kind = pair_kind(p)
            pb += (f'<tr><td class="mono">{p["a"]} × {p["b"]}</td><td class="num">{p["rows"]}</td><td class="num">{p["rows_identical"]}</td><td class="num">{p["rows_conflict"]}</td><td class="num">{p["cells_same"]} / {p["cells_diff"]}</td>'
                   f'<td>{chip(KIND_CHIP[kind], kind)}</td><td class="wrap">{esc(", ".join(f"{t} {n}" for t, n in p["per_table"].most_common(3)))}</td></tr>')
        pair_html = ("<h4 style=\"margin-top:12px\">Interseções dentro do grupo (medidas célula a célula)</h4>"
                     f'<div class="scroll"><table class="t compact"><thead><tr><th>Par</th><th>Linhas em comum</th><th>Linhas idênticas</th><th>Linhas em conflito</th><th>Células iguais / diferentes</th><th>Tipo</th><th>Tabelas</th></tr></thead><tbody>{pb}</tbody></table></div>') if pb else ""
        out += (f'<article class="sub" id="s-{sid}"><h3>{esc(name)} <span class="count">{len(ids)} mod{"s" if len(ids) > 1 else ""}</span></h3><p class="lead">{rich(blurb)}</p>'
                f'<div class="scroll"><table class="t"><thead><tr><th>#</th><th>Mod</th><th>Ação</th><th>Por que nesta posição</th></tr></thead><tbody>{rows}</tbody></table></div>'
                f'<h4 style="margin-top:12px">Quem faz melhor cada recurso</h4><p class="lead">{rich(lead)}</p>'
                f'<div class="scroll"><table class="t compact"><thead><tr><th>Recurso</th><th>Implementação mais forte</th><th>Também implementam</th><th>Observação</th></tr></thead><tbody>{fb}</tbody></table></div>'
                f'<h4 style="margin-top:12px">Quais tabelas cada mod toca</h4>{table_matrix(ids)}{pair_html}</article>')
    return out


def inter_section():
    kinds = {"Conflito direto": "bad", "Conflito potencial (arquivo)": "warn", "Redundante": "info", "Redundante com divergência": "info", "Tabela inteira": "warn", "Funcional leve": "info", "Independente": "ok", "Complementar": "ok"}
    rows = ""
    for a, b, t, d in D.INTERS:
        rows += f'<tr data-kind="{esc(t)}"><td class="mono">{esc(a)}</td><td class="mono">{esc(b)}</td><td>{chip(kinds.get(t, "info"), t)}</td><td>{rich(d)}</td></tr>'
    cur = ('<div class="scroll"><table class="t" id="inter"><thead><tr><th>Mod</th><th>Com</th><th>Tipo</th><th>O que acontece (curado, com a medição)</th></tr></thead>'
           f'<tbody>{rows}</tbody></table></div>')
    body = ""
    for p in sorted(PAIRS, key=lambda p: -p["rows"]):
        kind = pair_kind(p)
        body += (f'<tr><td class="mono">{p["a"]} × {p["b"]}</td><td>{esc(mod_name(p["a"]))[:28]} / {esc(mod_name(p["b"]))[:28]}</td><td class="num">{p["rows"]}</td><td class="num">{p["rows_identical"]}</td><td class="num">{p["rows_conflict"]}</td>'
                 f'<td class="num">{p["cells_same"]} / {p["cells_diff"]}</td><td>{chip(KIND_CHIP[kind], kind)}</td><td class="wrap">{esc(", ".join(f"{t} {n}" for t, n in p["per_table"].most_common(3)))}</td></tr>')
    auto = ('<h3 style="margin-top:22px">Todos os pares do grau B que escrevem a mesma linha (medido)</h3>'
            '<p class="lead">Calculado das linhas e células lidas. "Linha idêntica" = todas as colunas que os dois escrevem têm o mesmo valor; "em conflito" = pelo menos uma coluna difere (vale a linha do último na ordem, e a regra 5 pode esvaziar colunas que o vencedor não declara).</p>'
            f'<div class="scroll"><table class="t compact"><thead><tr><th>Par</th><th>Mods</th><th>Linhas em comum</th><th>Idênticas</th><th>Em conflito</th><th>Células iguais / diferentes</th><th>Tipo</th><th>Tabelas</th></tr></thead><tbody>{body}</tbody></table></div>')
    return cur + auto


def questions_table():
    rows = "".join(f'<tr><td class="mono">{q}</td><td class="mono">{esc(m)}</td><td>{rich(t)}</td><td>{rich(h)}</td></tr>' for q, m, t, h in D.QUESTIONS)
    return f'<div class="scroll"><table class="t"><thead><tr><th>#</th><th>Mods</th><th>Pergunta</th><th>Como confirmar</th></tr></thead><tbody>{rows}</tbody></table></div>'


def glossary_table():
    rows = "".join(f'<tr><td class="wrap"><b>{rich(t)}</b></td><td>{rich(d)}</td><td>{rich(e)}</td><td>{rich("^" + c)}</td></tr>' for t, d, e, c in D.GLOSSARY)
    return f'<div class="scroll"><table class="t"><thead><tr><th>Termo</th><th>O que significa</th><th>Evidência</th><th>Confiança</th></tr></thead><tbody>{rows}</tbody></table></div>'


def errors_table():
    rows = ""
    for sid, name, _, ids in D.SUBCATS:
        for i in ids:
            for e in D.MODS[i]["errors"]:
                if e.startswith("Nenhum erro"):
                    continue
                rows += f'<tr><td class="mono"><a href="#m{i}">{i}</a></td><td>{esc(D.MODS[i]["name"])[:40]}</td><td>{rich(e)}</td></tr>'
    return ('<div class="scroll"><table class="t compact"><thead><tr><th>Mod</th><th>Nome</th><th>Erro ou suspeita</th></tr></thead>' f'<tbody>{rows}</tbody></table></div>')


def keep_reject_table():
    rows = ""
    for sid, name, _, ids in D.SUBCATS:
        for i in ids:
            m = D.MODS[i]
            k = [x for x in m["keep"] if not x.startswith("Nada")]
            r = [x for x in m["reject"] if not x.startswith("Nada")]
            if k or r:
                rows += (f'<tr><td class="mono"><a href="#m{i}">{i}</a></td><td>{esc(m["name"])[:36]}</td><td>{"<br>".join(rich(x) for x in k) or "-"}</td><td>{"<br>".join(rich(x) for x in r) or "-"}</td></tr>')
    return ('<div class="scroll"><table class="t compact"><thead><tr><th>Mod</th><th>Nome</th><th>Possivelmente vale integrar</th><th>Provavelmente rejeitar</th></tr></thead>' f'<tbody>{rows}</tbody></table></div>')


FINDINGS = [
    ("Três pacotes não carregam como empacotados",
     "**85** (manifest só lista 1.3 e 1.3.1, o motor o desativa), **1639** (o id derivado do nome, `AlternateFoodSpoil2X`, tem dígito: pela regra 4 o patch provavelmente é ignorado) e **1384** (sem manifest: pak solto, aplicação por patch não medida). O 770 está em quarentena por caminhos `../` no pak. ^c"),
    ("Erros de digitação e de empacotamento reais",
     "1639: Dead Chicken 24 → **2400** (era 48). 2011: atributo `decay_ime_hours`, cabeçalho `Weight` com W maiúsculo (provável peso vazio em 44 itens), zeros em carne crua. 1558: **14 chaves de XP de escudo** que nenhuma lista conhece, e `ShoeHealthDecrease` 10x maior contra o leia-me ('botas gastam mais devagar'). 85: cabeçalho de `perk.xml` sem duas colunas do jogo. ^c"),
    ("Os quatro mods de combate se contradizem",
     "`CombatAutoMaxAttackDelay`: jogo 6, 1112 e 1384 **0,01**, 2179 **3**, 1558 **1,5**. `SkillToDmgConstA`: jogo 250, 1384 **700**, 1558 **100**. `SkillToDefense`: jogo 0,02857, 2179 **0,2857**, 1558 **0,01**. Cada um escreve a mesma linha: vale o último na ordem. ^c"),
    ("Mudanças fora do escopo declarado",
     "2045 liga a tecla **3** a um comando de depuração; 2011 reescreve itens de teste e 'Generic potion' vira veneno (`doomsday_poison`); 85 regrava 63 buffs e 19 habilidades do jogo com valores de 2018; 1112 muda o NPC `rat_bernard`; 2323 deixa o comando `alchemy_give_all`; 2343 e 2318 substituem arquivos de interface do inventário; 2173 apaga colunas de editor. ^c"),
    ("Tabelas substituídas inteiras",
     "85, 770 (perks), 2345 (`food`) e 1062 (`sleeping_spot_type`). Uma tabela inteira vence qualquer patch de outro mod e desfaz as mudanças do 1.9.7/1.9.8 nela. ^d"),
    ("Perkaholic: três empacotamentos das mesmas 56 perks",
     "85, 770 e 1009 trazem as mesmas perks e os mesmos buffs: 85 e 770 são idênticos entre si nas 186 linhas em comum; o 1009 difere em 15 a 16 linhas (campos de interface do buff e `mst*1.1`). Só o **1009** (patch, 13 idiomas, código correto) é utilizável. ^c"),
    ("Valores extremos a testar antes de qualquer decisão",
     "Atraso entre ataques 0,01 (1112, 1384); alcance do arco 3,3x (2035); quarto 10 a 25x mais caro (1105); `RepairKitCapacity` 8000 e sujeira desligada (1558); `MaxDamage` 100 em quatro mods (em acordo). ^d"),
    ("Ideias únicas do grau B",
     "Buffs de lanche e textos de efeito (2011); estado do equipamento e moral dos NPCs (2179); linhas de bloqueio perfeito por direção (1112/1384); armas de haste (2045); acampamento (1062); ligar ingredientes de estoques e cavalo à alquimia (2323); 56 perks (1009). ^d"),
]


def build():
    bidx = {b["id"]: b for b in D.BALANCE}
    sub_opts = '<option value="">Todas</option>' + "".join(f'<option value="{s}">{esc(n)}</option>' for s, n, _, _ in D.SUBCATS)
    ver_opts = ('<option value="">Todas</option><option value="ok">Candidato</option><option value="info">Conteúdo / outro escopo</option><option value="warn">Investigar / decidir</option><option value="bad">Rejeitar</option>')
    cards = "".join(mod_card(i, D.MODS[i], bidx) for _, _, _, ids in D.SUBCATS for i in ids)
    fhtml = "".join(f'<div class="find"><h3>{esc(t)}</h3><p>{rich(d)}</p></div>' for t, d in FINDINGS)
    nav = "".join(f'<a href="#{i}">{t}</a>' for i, t in (("resumo", "Resumo"), ("subcategorias", "Subcategorias"), ("mods", "Mods"), ("balanceamento", "Balanceamento"), ("intersecoes", "Interseções"),
                                                          ("erros", "Erros"), ("integrar", "Integrar ou rejeitar"), ("perguntas", "Perguntas"), ("glossario", "Glossário"), ("metodo", "Método")))
    n_files = len([f for f in FILES if f["role"] != "container (.pak)"])
    page = f"""<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Revisão do Grau B</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=IBM+Plex+Sans+Condensed:wght@500;600&family=IBM+Plex+Sans:wght@400;500;600&display=swap">
<style>{CSS}</style>
<div class="top"><b>Revisão do Grau B</b><nav>{nav}</nav></div>
<main>
<header>
<h1>Revisão do Grau B: 21 mods, o que fazem de verdade</h1>
<p class="lead">Primeira passada, só leitura. Cada arquivo de cada mod ({n_files} arquivos, mais os conteúdos dos paks) foi aberto e comparado com o jogo 1.9.8 e com as tabelas de referência de 2020, linha por linha e célula por célula. Nenhum mod foi executado, nenhum foi movido para <code>Reviewed_Mods</code> e nenhum balanceamento foi decidido: tudo fica registrado para a revisão final.</p>
<p class="legend"><span><span class="cf cf-c">confirmado</span> lido nos arquivos, no jogo ou no log</span><span><span class="cf cf-d">deduzido</span> inferido do nome, da ajuda ou do contexto</span><span><span class="cf cf-n">não verificado</span> precisa de teste no jogo</span></p>
</header>

<h2 id="resumo">Resumo</h2>
<p class="lead">Grau B é um rótulo de <b>tamanho</b> (100 ou mais linhas, 6 ou mais tabelas, ou 600 ou mais linhas de Lua), não de qualidade. Os 21 mods se agrupam em 8 subcategorias; só dois grupos (comida e combate) competem por valores; o resto, ou é redundante (Perkaholic) ou independente.</p>
<div class="cols">{fhtml}</div>
<h3 style="margin-top:22px">Os 21 mods</h3>
{summary_table()}

<h2 id="subcategorias">Subcategorias, comparação e ranking</h2>
<p class="lead">Agrupadas pelo sistema do jogo que mexem. A posição compara qualidade técnica, completude e risco dentro do grupo (não valor de jogo); cada posição tem o motivo escrito. Depois do ranking, a tabela "quem faz melhor cada recurso" compara mod a mod e a matriz de tabelas mostra onde se cruzam.</p>
{subcat_section()}

<h2 id="mods">Ficha de cada mod</h2>
<div class="filters">
<label>Subcategoria<select id="f-sub">{sub_opts}</select></label>
<label>Ação<select id="f-ver">{ver_opts}</select></label>
<label>Buscar<input id="f-q" type="search" placeholder="id, nome ou autor"></label>
<button id="f-open" type="button">Abrir os visíveis</button><button id="f-close" type="button">Fechar todos</button><span class="meta" id="f-count"></span>
</div>
{cards}

<h2 id="balanceamento">Balanceamento: cada mudança questionada</h2>
<p class="lead">Nada foi aceito nem descartado. Cada valor aparece com o antes e o depois, o que ele controla, por que o autor provavelmente o mudou, o efeito esperado e os outros mods no mesmo parâmetro. "Jogo" é o valor do 1.9.8 (ou, para constantes ocultas, o valor que o jogo devolveu na leitura de 1.9.6). Descrições entre colchetes vêm do arquivo de referência do próprio jogo.</p>
{balance_section()}

<h2 id="intersecoes">Interseções e conflitos</h2>
<p class="lead">Arquivo em comum não é conflito automático: cada linha diz o que de fato acontece (linha idêntica, valores diferentes, colunas diferentes). Dois mods também entram em conflito lógico sem tocar o mesmo arquivo.</p>
{inter_section()}

<h2 id="erros">Erros, suspeitas e achados de estrutura</h2>
<p class="lead">Todos os pontos marcados como erro nas fichas, juntos. "Confirmado" é fato do arquivo; o efeito no jogo quase sempre é "deduzido" ou "não verificado".</p>
{errors_table()}

<h2 id="integrar">O que vale integrar e o que rejeitar (candidatos)</h2>
<p class="lead">Lista de trabalho para a revisão final. Nenhum item foi copiado.</p>
{keep_reject_table()}

<h2 id="perguntas">Perguntas para confirmar e para a revisão final</h2>
{questions_table()}

<h2 id="glossario">Glossário com evidência</h2>
{glossary_table()}

<h2 id="metodo">Método e limites</h2>
<ul>
<li>Cada arquivo foi listado antes de extrair (sem executáveis nem scripts do sistema), extraído para uma pasta de rascunho, lido e apagado. Nenhum conteúdo foi executado nem carregado pelo jogo. O mod 770 está em quarentena e foi lido do mesmo jeito, só leitura.</li>
<li>O jogo de comparação é o 1.9.8 da réplica (<code>Tables.pak</code>, <code>Scripts.pak</code>, <code>GameData.pak</code>, paks de texto), só leitura. Cada membro de pak foi comparado por CRC com os do jogo; tabelas, linha a linha e célula a célula; scripts, por diferença de linhas.</li>
<li><code>Data/Tables_reference.pak</code> (2020) serviu para separar valor <b>obsoleto</b> (igual à referência antiga) de mudança <b>deliberada</b>. Só o 2173 tem 40 células obsoletas; as outras são deliberadas.</li>
<li>A versão declarada no manifest não foi usada como prova: o que vale é a estrutura (sufixo igual ao id, linhas completas, caminho <code>Libs/Tables</code>, cabeçalho) e a comparação com as tabelas do 1.9.8. A leitura do manifest só serve para saber se o motor o carrega.</li>
<li>Valores de constantes ocultas vêm de <code>rpg_constants_runtime.csv</code> (lidas no jogo 1.9.6): podem diferir no 1.9.8 (o binário mudou na 1.9.7).</li>
<li>A chave de linha usada para comparar usa as colunas <code>*_id</code> (e <code>soul_id</code> para <code>soul</code>); linhas "novas" são as que não casam com nenhuma do jogo por essa chave, o que pode esconder uma linha alterada em coluna-chave.</li>
<li>Nada foi testado no jogo. As perguntas Q1 a Q18 dizem como confirmar cada ponto. Não houve execução de mod nem teste de jogo nesta passada.</li>
</ul>
<footer>Dados: <code>docs/mods-review/grade_b_files.csv</code> ({len(FILES)} arquivos com sha256), <code>grade_b_cells.csv</code> ({len(CELLS)} células), <code>grade_b_text.csv</code> ({len(TEXT)} textos), <code>grade_b_newrows.json</code>, <code>grade_b_scripts.json</code>; curadoria em <code>tools/grade_b_data*.py</code>. Gerado por <code>tools/build_grade_b_page.py</code> a partir de <code>tools/grade_b_extract.py</code>.</footer>
</main>
<script>{JS}</script>
"""
    return page


def write_companions():
    # intersections csv
    with open(os.path.join(R, "grade_b_intersections.csv"), "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["mod_a", "mod_b", "kind", "shared_rows", "identical_rows", "conflict_rows", "complementary_rows", "cells_same", "cells_different", "whole_table_in", "tables"])
        for p in sorted(PAIRS, key=lambda p: -p["rows"]):
            w.writerow([p["a"], p["b"], pair_kind(p), p["rows"], p["rows_identical"], p["rows_conflict"], p["rows_complementary"], p["cells_same"], p["cells_diff"], " ".join(p["whole"]),
                        "; ".join(f"{t} {n}" for t, n in p["per_table"].most_common())])
    # overview csv
    with open(os.path.join(R, "grade_b_overview.csv"), "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["id", "name", "subcategory", "rank", "verdict", "files", "rows_new", "rows_changed", "whole_table_replacements", "balance_entries"])
        for sid, name, _, ids in D.SUBCATS:
            rk = {i: p for i, p, _ in D.RANK[sid]}
            for i in ids:
                tabs = table_summary(i)
                w.writerow([i, D.MODS[i]["name"], name, rk[i], D.MODS[i]["verdict_text"], len([x for x in files_of(i) if x["role"] != "container (.pak)"]),
                            sum(v["new"] for v in tabs.values()), sum(v["changed"] for v in tabs.values()), sum(1 for v in tabs.values() if v["whole"]), " ".join(D.MODS[i]["balance"])])


def write_md():
    L = ["# Grade B mods: first-pass review", "",
         "> **Status date:** 2026-10-08 | **Kind:** review | **Trust:** measured (files, game tables, 2020 reference tables) and derived (counts, readings of values) | **Game version:** 1.9.8", "",
         "The 21 mods graded B (\"large\") in [`MOD_ANALYSIS.md`](MOD_ANALYSIS.md), opened file by file and compared cell by cell with the 1.9.8 install. First pass only: what each mod really changes, how they relate, what looks wrong, what is worth keeping later. No balance decision is taken, nothing is moved to `Reviewed_Mods`, and nothing was run.", "",
         "The full review is the page [`GRADE_B_REVIEW.html`](GRADE_B_REVIEW.html) (Portuguese, the author's display standard: before-and-after tables, a glossary with evidence and a confidence mark on every claim). It is built by `tools/build_grade_b_page.py` from `grade_b_*.csv/json` (written by `tools/grade_b_extract.py`) and the curated text in `tools/grade_b_data*.py`. [`grade_b_intersections.csv`](grade_b_intersections.csv) has every pair of mods that write the same row, and [`grade_b_overview.csv`](grade_b_overview.csv) one line per mod.", "",
         "## Sub-categories and ranking", "", "| Sub-category | Ranking (best made first) |", "|---|---|"]
    for sid, name, _, ids in D.SUBCATS:
        L.append(f"| {name} | " + ", ".join(f"{i} ({p})" for i, p, _ in sorted(D.RANK[sid], key=lambda x: x[1])) + " |")
    L += ["", "## What stands out", ""]
    for t, d in FINDINGS:
        L.append(f"- **{t}.** " + re.sub(r"`", "`", re.sub(r"\s*\^[cdn]\b", "", d)))
    L += ["", "## Open questions", "", f"{len(D.QUESTIONS)} questions with a way to confirm each are in the page (section \"Perguntas\")."]
    L += ["", "## Safety and scope", "",
          "The archives were listed before extraction, extracted to a scratch folder, read and deleted; nothing was run, installed or loaded by the game. Mod 770 is in quarantine and was read the same way. The comparison used the replica install (`Mods WIP folder/KingdomComeDeliverance`, read only).", ""]
    open(os.path.join(R, "GRADE_B.md"), "w", encoding="utf-8", newline="\n").write("\n".join(L))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(R, "GRADE_B_REVIEW.html"))
    a = ap.parse_args()
    page = build()
    open(a.out, "w", encoding="utf-8").write(page)
    write_companions()
    write_md()
    print("wrote", a.out, len(page), "bytes;", len(PAIRS), "pairs")


if __name__ == "__main__":
    main()
