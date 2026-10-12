#!/usr/bin/env python3
"""
perks_report_pdf.py - short illustrated PDF (Portuguese) comparing every Perkaholic / Riposte
instance of the Perks workbench.

    python tools/analyze_perk_mods.py && python tools/perks_report_pdf.py

Reads <workbench>/notes/analysis.json and prints the page with the local Edge/Chrome, exactly like
tools/build_report_pdf.py, whose chart and diagram helpers it reuses.
"""
import argparse
import collections
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_report_pdf as R  # noqa: E402
import paths  # noqa: E402

WORKBENCH = r"E:\Kingdom-Refinement-Suite\Mods WIP folder\Perks\perkaholic-riposte-workbench"
OK, WARN, BAD = R.S3, R.S4, R.RED


def light(c):
    return {R.S3: "#f3f8f4", R.S4: "#fdf8ec", R.RED: "#fdeeee"}[c]


def verdict_row(inst, loads, how, note, colour):
    mark = {OK: "USAR", WARN: "CUIDADO", BAD: "NÃO USAR"}[colour]
    return (f'<tr><td><b>{R.esc(inst)}</b></td>'
            f'<td style="color:{"#1a7f58" if loads else R.RED};font-weight:700">'
            f'{"carrega" if loads else "não carrega"}</td>'
            f'<td>{R.esc(how)}</td><td>{R.esc(note)}</td>'
            f'<td><span class="pill" style="background:{colour}">{mark}</span></td></tr>')


def diagram_three_ways(width=700):
    """The three ways these five mods write the same tables."""
    h = 196
    o = [R.svg_open(width, h, "três maneiras de escrever a mesma tabela")]
    panels = [
        (0, OK, "PATCH PTF", ["perk__perkaholic.xml", "dentro de Libs/Tables", "num .pak"],
         "só as linhas do mod mudam", "1009 (.rar e pasta), 1765"),
        (240, BAD, "TABELA INTEIRA", ["perk.xml", "sem sufixo", "num .pak"],
         "apaga o patch de todo mundo", "85, 770"),
        (480, WARN, "FORA DO LUGAR", ["Data/Tables/rpg/...", "sem a pasta Libs/", "solto"],
         "o jogo nunca lê", "1009 (pasta), 1765"),
    ]
    for x, col, title, lines, effect, who in panels:
        w = 220
        o.append(f'<rect x="{x}" y="0" width="{w}" height="{h}" rx="7" fill="{light(col)}" '
                 f'stroke="{col}" stroke-width="1.5"/>')
        o.append(R.txt(x + w / 2, 22, title, 12, R.INK, "middle", "700"))
        for i, ln in enumerate(lines):
            o.append(R.txt(x + w / 2, 42 + i * 14, ln, 9.5, R.INK2, "middle",
                           family="Consolas, monospace" if i == 0 else None))
        o.append(f'<path d="M{x + w / 2},92 V112" stroke="{col}" stroke-width="2" '
                 f'marker-end="url(#{"ahr" if col == R.RED else "ah"})"/>')
        o.append(f'<rect x="{x + 16}" y="118" width="{w - 32}" height="34" rx="5" fill="#fff" '
                 f'stroke="{col}"/>')
        o.append(R.txt(x + w / 2, 139, effect, 10, R.INK, "middle", "700"))
        o.append(R.txt(x + w / 2, 174, who, 10, R.INK2, "middle", "600"))
    o.append("</svg>")
    return "".join(o)


def diagram_riposte(width=700):
    """What Riposte actually does: it unhides two rows that already exist."""
    h = 176
    o = [R.svg_open(width, h, "o que o Riposte faz")]
    o.append(R.box(0, 24, 200, 108, "No jogo original",
                   ["as duas linhas JÁ existem", "na tabela perk", "", "visibility = 0",
                    "(invisível no menu)"], "#f7f6f2", R.GRID))
    o.append(f'<path d="M206,78 H268" stroke="{R.S1}" stroke-width="2" marker-end="url(#ahb)"/>')
    o.append(R.box(272, 24, 170, 108, "O patch do mod",
                   ["NÃO cria perk novo", "", "muda 2 linhas:", "visibility 0 -> 2 e 1",
                    "+ nome e descrição"], "#eef5fd", R.S1))
    o.append(f'<path d="M448,78 H508" stroke="{R.S1}" stroke-width="2" marker-end="url(#ahb)"/>')
    o.append(R.box(512, 24, width - 512, 108, "Resultado",
                   ["as perks Riposte e", "ripo_lsw_01 aparecem", "na árvore de Defesa",
                    "(skill_selector 15)"], "#f3f8f4", OK))
    o.append(R.txt(0, 14, "RIPOSTE NÃO ADICIONA CONTEÚDO - ELE DESTRAVA O QUE JÁ ESTÁ NO JOGO",
                   11, R.INK, weight="700"))
    o.append(R.txt(0, 164, "Por isso é um patch de 2 linhas: o conteúdo (ícone, animação, texto) "
                           "já vem com o jogo.", 10, R.INK2))
    o.append("</svg>")
    return "".join(o)


def build(data, args):
    by = {i["id"]: i for i in data}
    P = []

    # ---- content of the Perkaholic payload (same in the three versions, read from 1009r)
    pf = [f for f in by["1009r"]["files"] if f["table"] == "perk"][0]
    raw = open(os.path.join(args.workbench, "extracted", "1009_perkaholic-ptf_rar", "_pak", "Libs",
                            "Tables", "rpg", "perk__perkaholic.xml"), encoding="utf-8").read()
    rows = [dict(r.attrib) for r in
            ET.fromstring(re.sub(r"^\s*<\?xml[^>]*\?>", "", raw).strip()).find("table")
            .findall("./rows/row")]
    skill_names = {"23": "Armas de haste", "18": "Arco", "24": "Desarmado", "17": "Machado",
                   "21": "Maça", "15": "Defesa", "2": "Esgrima", "": "sem perícia (atributo)"}
    per_skill = collections.Counter(r.get("skill_selector", "") for r in rows)
    chart_skills = R.hbar_chart(
        [(skill_names.get(s, s), n) for s, n in per_skill.most_common()],
        "perks novos por perícia", left=200, color=R.S1, note_fmt=lambda n, v: f"{v:.0f} perks")

    counts = {f["table"]: f["compare"] for f in by["1009r"]["files"]}
    chart_tables = R.hbar_chart(
        [("perk (perks)", len(counts["perk"]["new"])),
         ("buff (efeitos)", len(counts["buff"]["new"])),
         ("perk_buff (ligação)", len(counts["perk_buff"]["new"])),
         ("perk_buff_override", len(counts["perk_buff_override"]["new"])),
         ("perk2perk_exclusivity", len(counts["perk2perk_exclusivity"]["new"]))],
        "linhas novas por tabela", left=200, color=R.S3, note_fmt=lambda n, v: f"{v:.0f} novas")

    # ---- page 1: verdict
    rows_v = "".join([
        verdict_row("1009 .rar (2026)", True, "6 patches PTF corretos",
                    "única que carrega E aplica certo", OK),
        verdict_row("1009 pasta (2024)", False, "pak correto + 6 cópias mortas",
                    "mesmo conteúdo, manifest até 1.9.7", WARN),
        verdict_row("1765 Riposte", False, "1 patch PTF correto",
                    "conteúdo bom, manifest só 1.9.6", WARN),
        verdict_row("770 Perkaholic 1.07", True, "substitui 5 tabelas inteiras",
                    "e escreve FORA da pasta do mod", BAD),
        verdict_row("85 Perkaholic 1.05", False, "substitui 6 tabelas inteiras",
                    "derruba 66 perks do jogo atual", BAD),
    ])
    P.append(R.page(1, "Perkaholic e Riposte: as 5 instâncias", f"""
      <p class="lead">Tudo que existe de Perkaholic e Riposte em
      <code>Installed_to_review</code>, copiado para a bancada de trabalho, aberto e comparado com
      as tabelas do jogo 1.9.8. Nada foi instalado nem executado.</p>
      <table><tr><th>Instância</th><th>1.9.8</th><th>Como aplica</th><th>Observação</th>
      <th>Veredito</th></tr>{rows_v}</table>
      <div class="fig">{diagram_three_ways()}</div>
      <div class="callout ok"><div class="t">A resposta curta</div>
      <p><b>Para Perkaholic, use o 1009 (.rar de 2026) como base.</b> É o único que o jogo 1.9.8
      carrega e que aplica as mudanças como patch PTF, sem destruir o trabalho de outros mods.
      <b>Para Riposte, você já tem.</b> O seu próprio <code>modules/krs_perks</code> é uma cópia do
      1765 - melhor empacotada e já compatível com 1.9.8.</p></div>
      <div class="cap">Onde está tudo: <b>Mods WIP folder / Perks / perkaholic-riposte-workbench</b>
      - <code>_sources/</code> os originais intactos, <code>extracted/</code> aberto para leitura,
      <code>notes/analysis.json</code> os números desta página.</div>""", "Bancada de perks"))

    # ---- page 2: what Perkaholic implements
    P.append(R.page(2, "O que o Perkaholic implementa", f"""
      <p class="sub">As três versões entregam o mesmo pacote de conteúdo. Os números abaixo são
      da versão que funciona (1009 .rar).</p>
      <div class="tiles">
        {R.tile(len(counts['perk']['new']), "perks novos", "hl")}
        {R.tile(len(counts['buff']['new']), "efeitos (buffs) novos")}
        {R.tile(len(counts['perk_buff']['new']), "ligações perk → efeito")}
        {R.tile(1, "perícia destravada: Armas de haste", "hl")}
      </div>
      <div class="fig">{chart_skills}</div>
      <div class="cap">Os 56 perks novos espalhados pelas árvores de perícia. As 8 sem perícia são
      perks de atributo (força, vitalidade).</div>
      <div class="fig">{chart_tables}</div>
      <h3>Além dos perks novos, ele mexe em coisas existentes</h3>
      <table><tr><th>O quê</th><th>Mudança medida</th></tr>
      <tr><td><b>Perícia Armas de haste</b></td><td><code>hidden</code> de <b>True</b> para
      <b>False</b> - é o que faz a árvore aparecer no menu</td></tr>
      <tr><td><b>"Like a feather"</b></td><td>renomeado para <b>Featherweight I</b>, nível 4 → 5</td></tr>
      <tr><td><b>5 efeitos de perks do jogo</b></td><td>Heavy swing <code>wat*1.03</code> →
      <code>wat*1.2</code> · Art admirer <code>cha+1</code> → <code>cha+2</code> ·
      Reading cushion <code>erq*1.5</code> → <code>erq*2</code> · Like a feather
      <code>fdm*0.7</code> → <code>fdm*0.75</code> · Against all odds (só ícone/UI)</td></tr>
      <tr><td><b>3 exclusividades</b></td><td>pares de perks novos que não podem coexistir</td></tr>
      </table>
      <div class="callout"><div class="t">Para o seu mod</div>
      <p>Essas 5 alterações em perks do jogo são opinião de balanceamento, não parte do "adicionar
      perks". Dá para pegar só as linhas novas e deixar as 5 de fora.</p></div>""", "Conteúdo"))

    # ---- page 3: how they implement it (the problems)
    code_traversal = R.code_svg(
        [("Perkaholic.pak  (dentro do mod 770)", R.INK3),
         ("   Libs/Tables/rpg/perk.xml              <- substitui a tabela", R.INK),
         ("   ../../../Data/Libs/Tables/rpg/perk.tbl        <- SAI da pasta", R.INK),
         ("   ../../../Data/Libs/Tables/rpg/buff.tbl", R.INK),
         ("   ../../../Data/Libs/Tables/rpg/perk_buff.tbl", R.INK),
         ("   ... mais 2 arquivos .tbl", R.INK2)],
        title="770 - as 5 entradas que escrevem fora da pasta do mod", fs=10.5, lh=16,
        marks=[(2, 3, 60, BAD), (3, 3, 60, BAD), (4, 3, 60, BAD)],
        arrows=[(2, 45, "grava por cima dos arquivos do jogo", BAD, "r")])
    code_dead = R.code_svg(
        [("Perkaholic PTF-...-1714642782/   (instância 1009 pasta)", R.INK3),
         ("   Data/perkaholic.7zip", R.INK),
         ("        Libs/Tables/rpg/perk__perkaholic.xml   <- este o jogo lê", R.INK),
         ("   Data/Tables/rpg/perk__perkaholic.xml        <- este nunca", R.INK),
         ("   Data/Tables/rpg/buff__perkaholic.xml", R.INK),
         ("   ... mais 4 cópias mortas", R.INK2)],
        title="1009 pasta - seis cópias que o jogo nunca lê (falta Libs/)", fs=10.5, lh=16,
        marks=[(2, 3, 62, OK), (3, 3, 62, WARN), (4, 3, 62, WARN)],
        arrows=[(3, 48, "fora de Libs/Tables", WARN, "r")])
    P.append(R.page(3, "Como implementam - e onde erram", f"""
      <p class="sub">Três defeitos concretos, medidos nos arquivos.</p>
      <h3>1. O 85 apaga parte do jogo atual</h3>
      <p>Ele é um mod da era KCD 1.3 e entrega as tabelas inteiras daquela época. Instalado hoje,
      as linhas que o jogo ganhou depois simplesmente somem:</p>
      <table><tr><th>Tabela</th><th class="n">Linhas do jogo que desaparecem</th></tr>
      <tr class="bad"><td>perk</td><td class="n"><b>66 perks</b></td></tr>
      <tr class="bad"><td>buff</td><td class="n">61 efeitos</td></tr>
      <tr class="bad"><td>perk_buff</td><td class="n">22 ligações</td></tr>
      <tr><td>perk_buff_override / perk2perk_exclusivity / skill</td><td class="n">3 / 2 / 2</td></tr>
      </table>
      <p>E mais: <b>541 das linhas de perk não trazem as colunas <code>autolearnable</code> e
      <code>exclude_in_game_mode</code></b>, que o jogo preenche nas 551. Pela regra medida, coluna
      não listada vira vazia.</p>
      <h3>2. O 770 escreve fora da própria pasta</h3>
      <div class="fig">{code_traversal}</div>
      <div class="cap">É por isso que ele está em <code>_quarantine</code>. Na extração para a
      bancada essas 5 entradas foram <b>bloqueadas</b>: nada foi escrito fora da pasta.</div>
      <h3>3. O 1009 pasta carrega seis arquivos mortos</h3>
      <div class="fig">{code_dead}</div>""", "Defeitos"))

    # ---- page 4: Riposte
    rip = [f for f in by["1765"]["files"] if f["verdict"] == "patch"][0]
    diffs = rip["compare"]["changed"]
    rows_d = ""
    for c in diffs:
        for col, (v, m) in c["diff"].items():
            rows_d += (f'<tr><td class="mono">{R.esc(c["name"])}</td><td class="mono">{R.esc(col)}</td>'
                       f'<td class="mono">{R.esc(v) or "(vazio)"}</td>'
                       f'<td class="mono"><b>{R.esc(m) or "(vazio)"}</b></td></tr>')
    P.append(R.page(4, "Riposte em detalhe", f"""
      <div class="fig">{diagram_riposte()}</div>
      <h3>As duas linhas que ele altera, coluna por coluna</h3>
      <table><tr><th>Perk</th><th>Coluna</th><th>Jogo</th><th>Mod</th></tr>{rows_d}</table>
      <h3>Você já tem isso - e melhor empacotado</h3>
      <table><tr><th></th><th>1765 Restore Riposte</th><th>seu modules/krs_perks</th></tr>
      <tr><td>Carrega no 1.9.8</td><td style="color:{R.RED}"><b>não</b> (manifest só 1.9.6)</td>
      <td style="color:#1a7f58"><b>sim</b> (1.9.6, 1.9.7, 1.9.8)</td></tr>
      <tr><td><code>&lt;modid&gt;</code> declarado</td><td style="color:{R.RED}">não (deduzido do nome)</td>
      <td style="color:#1a7f58">sim: <code>krs_perks</code></td></tr>
      <tr><td>Colunas no cabeçalho</td><td>12 de 14</td><td>as 14</td></tr>
      <tr><td>Cópias soltas no pacote</td><td>sim, 2 fora do pak</td><td>não</td></tr>
      <tr><td>Nível da perk Riposte</td><td><b>8</b></td><td><b>10</b></td></tr></table>
      <div class="callout warn"><div class="t">A única decisão que sobra</div>
      <p>Conteúdo idêntico, exceto o nível exigido: <b>8 no mod original, 10 no seu módulo</b>.
      Escolha um. Fora isso, não há motivo para instalar o 1765 junto - os dois escrevem as mesmas
      duas linhas e a última a carregar vence.</p></div>""", "Riposte"))

    # ---- page 5: plan
    P.append(R.page(5, "Ponto de partida para o seu mod", f"""
      <p class="sub">O que copiar de quem, e em que ordem.</p>
      <h3>1. Base de conteúdo: 1009 (.rar de 2026)</h3>
      <p>Os seis arquivos <code>*__perkaholic.xml</code> dentro de
      <code>extracted/1009_perkaholic-ptf_rar/_pak/Libs/Tables/rpg/</code> já estão no formato certo.
      Para virarem seu mod, muda só o sufixo e o manifest:</p>
      <div class="fig">{R.code_svg([
        ("de:   perk__perkaholic.xml        + manifest sem <modid>", R.INK),
        ("para: perk__krs_perks.xml         + <modid>krs_perks</modid>", R.INK),
        ("", R.INK),
        ("e o cabeçalho com as 14 colunas da tabela vanilla,", R.INK2),
        ("porque coluna que falta vira vazia (regra 5).", R.INK2)],
        title="o que muda para virar seu mod", fs=11, lh=17,
        marks=[(1, 0, 62, OK)],
        arrows=[(1, 30, "sufixo = id do mod", R.S1, "r")])}</div>
      <h3>2. Riposte: nada a importar</h3>
      <p>Já está em <code>modules/krs_perks</code>. Só decida o nível (8 ou 10) e siga.</p>
      <h3>3. Cuidado conhecido: vocês disputam as mesmas linhas</h3>
      <p>Se o Perkaholic entrar no <code>krs_perks</code>, os 56 perks novos convivem sem conflito
      (são linhas que não existem no jogo). Mas as <b>5 alterações em perks existentes</b> e a
      <b>perícia destravada</b> são linhas compartilhadas: quem carregar por último vence.</p>
      <h3>4. O que deixar de fora</h3>
      <table><tr><th>Instância</th><th>Por quê</th></tr>
      <tr class="bad"><td>85 Perkaholic 1.05</td><td>tabelas da era 1.3; derruba 66 perks e apaga
      2 colunas de 541 linhas</td></tr>
      <tr class="bad"><td>770 Perkaholic 1.07</td><td>substitui 5 tabelas inteiras e grava fora da
      pasta do mod (quarentena)</td></tr>
      <tr><td>1009 pasta (2024)</td><td>mesmo conteúdo do .rar, manifest velho e 6 arquivos mortos</td></tr>
      </table>
      <div class="callout"><div class="t">Próximo passo sugerido</div>
      <p>Montar um <code>krs_perks</code> de teste com os 56 perks novos (sem as 5 alterações de
      balanceamento) e rodar <code>tools/check_patch_names.py</code> e depois
      <code>tools/gate.py</code> para ler as linhas de volta dentro do jogo.</p></div>""", "Plano"))

    return (f'<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">'
            f'<title>Perkaholic e Riposte</title><style>{R.CSS}</style></head><body>'
            f'{"".join(P)}</body></html>')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--workbench", default=WORKBENCH)
    ap.add_argument("--out", default="")
    args = ap.parse_args()
    out = os.path.abspath(args.out or os.path.join(args.workbench, "notes",
                                                   "PERKAHOLIC-RIPOSTE.pdf"))
    data = json.load(open(os.path.join(args.workbench, "notes", "analysis.json"), encoding="utf-8"))
    work = tempfile.mkdtemp(prefix="krs_perks_report_")
    src = os.path.join(work, "report.html")
    with open(src, "w", encoding="utf-8") as f:
        f.write(build(data, args))
    exe = next((b for b in R.BROWSERS if os.path.exists(b)), "")
    if not exe:
        sys.exit("no Edge or Chrome found")
    subprocess.run([exe, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                    f"--print-to-pdf={out}", "--virtual-time-budget=4000",
                    f"--user-data-dir={os.path.join(work, 'profile')}", src],
                   capture_output=True, text=True, timeout=240)
    if not os.path.exists(out):
        sys.exit("the browser did not write the PDF")
    shutil.copy(src, os.path.splitext(out)[0] + ".html")
    shutil.rmtree(work, ignore_errors=True)
    print(f"wrote {out} ({os.path.getsize(out) / 1024:.0f} KB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
