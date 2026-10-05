#!/usr/bin/env python3
"""
build_report_pdf.py - illustrated PDF report (Portuguese) of the A-E mod research.

    python tools/build_report_pdf.py
    python tools/build_report_pdf.py --out docs/mods-review/RELATORIO_MODS_A-E.pdf

Reads the generated CSVs (mod_subcategories.csv, mod_intersections.csv, mod_analysis.csv,
mod_overlap.csv, mod_tables.csv) plus two real files of the suite used as code examples
(modules/krs_qol/...), builds a self-contained HTML page with inline SVG charts and diagrams,
and prints it to PDF with a local Chromium (Edge or Chrome) in headless mode. No archive is
opened, nothing is downloaded and no network call is made.

Charts follow the data-viz rules: one axis, categorical hues in fixed order, every segment
directly labelled (the print surface has no hover), recessive axes.
"""
import argparse
import base64
import collections
import csv
import datetime
import glob
import html
import math
import os
import shutil
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paths  # noqa: E402

D = paths.MODS_REVIEW
TODAY = datetime.date.today()
MONTHS = ["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho", "agosto", "setembro",
          "outubro", "novembro", "dezembro"]

# ---------------------------------------------------------------- palette (validated, light surface)
SURFACE = "#fcfcfb"
INK = "#0b0b0b"
INK2 = "#52514e"
INK3 = "#8a8880"
GRID = "#e4e2dc"
PAPER = "#ffffff"
S1, S2, S3, S4, S5 = "#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4"
BLUE_SEQ = ["#cde2fb", "#9ec5f4", "#6da7ec", "#3987e5", "#2a78d6", "#256abf", "#1c5cab", "#184f95"]
RED = "#e34948"
GRADE_COLOR = {"A": S1, "B": S2, "C": S3, "D": S4, "E": S5}
BROWSERS = [
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
]


def read_csv(name):
    with open(os.path.join(D, name), encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def esc(t):
    return html.escape(str(t))


def clip_list(text, n, sep=", "):
    """Cut a separated list to whole items, never mid-word."""
    text = str(text)
    if len(text) <= n:
        return text
    head = text[:n].rsplit(sep, 1)[0]
    return (head or text[:n]) + " ..."


def clip_name(text, n):
    text = str(text)
    return text if len(text) <= n else text[:n].rstrip(" -_") + "..."


def num(v, cast=float):
    try:
        return cast(v)
    except (TypeError, ValueError):
        return cast(0)


# ---------------------------------------------------------------- SVG primitives
def bar_path(x, y, w, h, r=4):
    """Bar anchored at the baseline on the left, rounded only on the data end."""
    r = max(0, min(r, w, h / 2))
    return (f"M{x},{y} H{x + w - r} Q{x + w},{y} {x + w},{y + r} V{y + h - r} "
            f"Q{x + w},{y + h} {x + w - r},{y + h} H{x} Z")


def svg_open(w, h, label):
    return (f'<svg viewBox="0 0 {w} {h}" width="100%" role="img" aria-label="{esc(label)}" '
            f'xmlns="http://www.w3.org/2000/svg" font-family="Segoe UI, Arial, sans-serif">'
            f'<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" '
            f'markerHeight="7" orient="auto-start-reverse">'
            f'<path d="M0,1 L9,5 L0,9 z" fill="{INK2}"/></marker>'
            f'<marker id="ahr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" '
            f'markerHeight="7" orient="auto-start-reverse">'
            f'<path d="M0,1 L9,5 L0,9 z" fill="{RED}"/></marker>'
            f'<marker id="ahb" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" '
            f'markerHeight="7" orient="auto-start-reverse">'
            f'<path d="M0,1 L9,5 L0,9 z" fill="{S1}"/></marker></defs>')


def txt(x, y, s, size=11, fill=INK, anchor="start", weight="400", family=None, style=""):
    fam = f' font-family="{family}"' if family else ""
    return (f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" '
            f'font-weight="{weight}"{fam} style="{style}">{esc(s)}</text>')


def hbar_chart(rows, label, width=700, row_h=26, left=210, color=S1, unit="", note_fmt=None,
               highlight=None, max_val=None):
    """rows: [(label, value)] - one series, every bar directly labelled."""
    h = len(rows) * row_h + 34
    mx = max_val or max(v for _, v in rows) or 1
    step = 10 ** max(0, int(math.log10(mx)) - 1)          # round the axis up to a readable tick
    mx = math.ceil(mx / (4 * step)) * 4 * step
    plot = width - left - 70
    out = [svg_open(width, h, label)]
    for i in range(5):                                   # recessive grid
        gx = left + plot * i / 4
        out.append(f'<line x1="{gx:.1f}" y1="18" x2="{gx:.1f}" y2="{h - 22}" stroke="{GRID}" '
                   f'stroke-width="1"/>')
        out.append(txt(gx, h - 8, f"{mx * i / 4:,.0f}".replace(",", "."), 9, INK3, "middle"))
    for i, (name, v) in enumerate(rows):
        y = 18 + i * row_h
        w = max(2.0, plot * v / mx)
        c = highlight.get(name, color) if highlight else color
        out.append(f'<path d="{bar_path(left, y, w, row_h - 9)}" fill="{c}"/>')
        out.append(txt(left - 8, y + row_h - 15, name, 10.5, INK, "end"))
        lab = f"{v:,.0f}".replace(",", ".") + unit if not note_fmt else note_fmt(name, v)
        out.append(txt(left + w + 6, y + row_h - 15, lab, 10.5, INK2, weight="600"))
    out.append("</svg>")
    return "".join(out)


def stacked_chart(rows, series, colors, label, width=700, row_h=28, left=240):
    """rows: [(label, {serie: value})] - stacked with a 2px surface gap and labelled segments."""
    h = len(rows) * row_h + 44
    totals = {k: sum(d.values()) for k, d in rows}
    mx = max(totals.values()) or 1
    plot = width - left - 60
    out = [svg_open(width, h, label)]
    for i, (name, d) in enumerate(rows):
        y = 30 + i * row_h
        x = left
        for s in series:
            v = d.get(s, 0)
            if not v:
                continue
            w = plot * v / mx
            out.append(f'<path d="{bar_path(x + 1, y, max(1.0, w - 2), row_h - 10, 3)}" '
                       f'fill="{colors[s]}"/>')
            if w >= 16:                                   # relief rule: label every readable segment
                out.append(txt(x + w / 2, y + row_h - 16, str(v), 9.5, PAPER, "middle", "700"))
            x += w
        out.append(txt(left - 8, y + row_h - 16, name, 10.5, INK, "end"))
        out.append(txt(x + 7, y + row_h - 16, str(totals[name]), 11, INK, weight="700"))
    lx = left
    for s in series:                                     # legend, always present for >= 2 series
        out.append(f'<rect x="{lx}" y="8" width="10" height="10" rx="2" fill="{colors[s]}"/>')
        out.append(txt(lx + 14, 17, s, 10, INK2))
        lx += 34 + 7 * len(s)
    out.append("</svg>")
    return "".join(out)


def scatter_chart(points, label, width=700, height=390):
    """points: [(x, y, name, show)] - one series, selected direct labels, quadrants annotated."""
    l, r, t, b = 52, 18, 20, 40
    pw, ph = width - l - r, height - t - b
    out = [svg_open(width, height, label)]
    out.append(f'<rect x="{l}" y="{t}" width="{pw}" height="{ph}" fill="#f7f6f2"/>')
    out.append(f'<rect x="{l + pw / 2}" y="{t}" width="{pw / 2}" height="{ph / 2}" fill="#eef5fd"/>')
    for i in range(6):
        gx, gy = l + pw * i / 5, t + ph * i / 5
        out.append(f'<line x1="{gx:.1f}" y1="{t}" x2="{gx:.1f}" y2="{t + ph}" stroke="{GRID}"/>')
        out.append(f'<line x1="{l}" y1="{gy:.1f}" x2="{l + pw}" y2="{gy:.1f}" stroke="{GRID}"/>')
        out.append(txt(gx, t + ph + 15, str(i * 20), 9, INK3, "middle"))
        out.append(txt(l - 7, gy + 3, str(100 - i * 20), 9, INK3, "end"))
    for x, y, name, show in points:
        cx, cy = l + pw * x / 100, t + ph * (1 - y / 100)
        out.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="4.5" fill="{S1}" fill-opacity="0.55" '
                   f'stroke="{PAPER}" stroke-width="2"/>')
    for x, y, name, show in points:
        if not show:
            continue
        cx, cy = l + pw * x / 100, t + ph * (1 - y / 100)
        ax = "end" if cx > l + pw * 0.62 else "start"
        dx = -9 if ax == "end" else 9
        out.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="4.5" fill="{S1}" stroke="{PAPER}" '
                   f'stroke-width="2"/>')
        out.append(txt(cx + dx, cy + 3.5, name, 9.5, INK, ax, "600"))
    out.append(txt(l + pw - 8, t + ph / 2 - 9, "muda muito + bem feito", 10, S1, "end", "700"))
    out.append(txt(l + 8, t + ph - 10, "muda pouco + mal feito", 10, INK3, "start", "700"))
    out.append(txt(l + pw / 2, height - 6, "efeito  (quanto muda)", 10, INK2, "middle", "600"))
    out.append(f'<text x="14" y="{t + ph / 2}" font-size="10" fill="{INK2}" font-weight="600" '
               f'text-anchor="middle" transform="rotate(-90 14 {t + ph / 2})">'
               f'construção  (quão bem feito)</text>')
    out.append("</svg>")
    return "".join(out)


def code_svg(lines, width=700, fs=11.5, lh=17, pad=12, title=None, marks=None, arrows=None,
             height_extra=0):
    """A code block drawn as SVG so arrows and callouts sit exactly on the right line.

    lines:  [(text, colour)] ; marks: [(line_index, char_from, char_to, colour)]
    arrows: [(line_index, char_at, text, colour, side)]  side 'r' puts the note on the right
    """
    cw = fs * 0.6
    top = 26 if title else pad
    h = top + len(lines) * lh + pad + height_extra
    out = [svg_open(width, h, title or "código")]
    out.append(f'<rect x="0" y="0" width="{width}" height="{h}" rx="6" fill="#f7f6f2" '
               f'stroke="{GRID}"/>')
    if title:
        out.append(txt(pad, 17, title, 10, INK3, weight="700"))
    for i, j, k, c in (marks or []):
        y = top + i * lh
        out.append(f'<rect x="{pad + 10 + j * cw:.1f}" y="{y - lh + 5:.1f}" '
                   f'width="{max(cw, (k - j) * cw):.1f}" height="{lh - 1}" rx="3" fill="{c}" '
                   f'fill-opacity="0.16"/>')
    for i, (text, colour) in enumerate(lines):
        y = top + i * lh
        out.append(txt(pad + 10, y, text, fs, colour or INK, family="Consolas, monospace"))
    for i, at, note, colour, side in (arrows or []):
        y = top + i * lh - 4
        x = pad + 10 + at * cw
        if side == "r":
            x2 = width - pad - 8
            out.append(f'<path d="M{x2},{y + 9} H{x + 24} L{x + 6},{y + 2}" fill="none" '
                       f'stroke="{colour}" stroke-width="1.6" marker-end="url(#{"ahr" if colour == RED else "ahb"})"/>')
            out.append(txt(x2, y - 2, note, 9.5, colour, "end", "700"))
        else:
            out.append(f'<path d="M{pad + 4},{y + 16} L{x},{y + 3}" fill="none" stroke="{colour}" '
                       f'stroke-width="1.6" marker-end="url(#{"ahr" if colour == RED else "ahb"})"/>')
            out.append(txt(pad + 4, y + 26, note, 9.5, colour, "start", "700"))
    out.append("</svg>")
    return "".join(out)


def box(x, y, w, h, title, body, fill=PAPER, stroke=None, title_fill=INK, fs=10):
    stroke = stroke or GRID
    out = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="7" fill="{fill}" '
           f'stroke="{stroke}" stroke-width="1.5"/>',
           txt(x + w / 2, y + 19, title, 11.5, title_fill, "middle", "700")]
    for i, line in enumerate(body):
        out.append(txt(x + w / 2, y + 36 + i * 13, line, fs, INK2, "middle"))
    return "".join(out)


# ---------------------------------------------------------------- diagrams
def diagram_pipeline(width=700):
    h = 212
    out = [svg_open(width, h, "como a pesquisa foi feita")]
    steps = [("138 arquivos", ["dos 131 mods", "baixados (P1/P2)"]),
             ("leitura estática", ["listar, extrair em", "pasta temporária, ler,", "apagar"]),
             ("tabelas CSV", ["linhas vs. vanilla,", "risco, layout,", "nota A-E"]),
             ("sub-categorias", ["mesmo arquivo /", "mesma tabela PTF", "+ 2 notas"]),
             ("interseções", ["mesma linha,", "mesma tabela,", "substituição"])]
    bw, gap = (width - 4 * 26) / 5, 26
    for i, (t, body) in enumerate(steps):
        x = i * (bw + gap)
        fill = "#eef5fd" if i >= 3 else PAPER
        out.append(box(x, 40, bw, 96, t, body, fill, S1 if i >= 3 else GRID))
        if i < 4:
            out.append(f'<path d="M{x + bw + 3},88 H{x + bw + gap - 4}" stroke="{INK2}" '
                       f'stroke-width="1.8" marker-end="url(#ah)"/>')
    out.append(txt(0, 22, "Nada foi instalado nem executado; nenhuma partida do jogo foi aberta.",
                   11, INK2, weight="600"))
    out.append(f'<rect x="0" y="152" width="{width}" height="40" rx="6" fill="#f3f8f4" '
               f'stroke="{S3}"/>')
    out.append(txt(14, 170, "Confiança do resultado:", 10.5, INK, weight="700"))
    out.append(txt(14, 184, "o que está escrito nos arquivos (medido), não como o mod se joga "
                            "(isso exigiria testar no jogo).", 10, INK2))
    out.append("</svg>")
    return "".join(out)


def diagram_rule6(width=700):
    h = 250
    out = [svg_open(width, h, "duas modificações na mesma linha")]
    out.append(txt(0, 14, "A MESMA LINHA, DOIS MODS", 11, INK, weight="700"))
    out.append(box(0, 28, 196, 74, "Mod A  (carrega antes)",
                   ["food: Aqua Vitalis", "nutrition = 2,5", "ratio = 0,5"], PAPER, S1))
    out.append(box(0, 118, 196, 74, "Mod B  (carrega depois)",
                   ["food: Aqua Vitalis", "decay = 123", "(demais colunas: vanilla)"], PAPER, S2))
    out.append(f'<path d="M200,65 C250,65 250,110 288,110" fill="none" stroke="{S1}" '
               f'stroke-width="1.8" marker-end="url(#ahb)"/>')
    out.append(f'<path d="M200,155 C250,155 250,122 288,122" fill="none" stroke="{S2}" '
               f'stroke-width="1.8" marker-end="url(#ah)"/>')
    out.append(box(292, 74, 150, 86, "mod_order.txt",
                   ["a linha é trocada", "INTEIRA; o último", "a carregar vence"], "#fdf3ee", S2))
    out.append(f'<path d="M446,117 H494" stroke="{RED}" stroke-width="2" '
               f'marker-end="url(#ahr)"/>')
    out.append(box(498, 74, width - 498, 86, "Resultado no jogo",
                   ["nutrition = 10  (vanilla)", "ratio = 0,1  (vanilla)", "decay = 123"],
                   "#fdeeee", RED))
    out.append(txt(width - 8, 180, "O Mod A foi desfeito em silêncio", 10, RED, "end", "700"))
    out.append(f'<rect x="0" y="204" width="{width}" height="40" rx="6" fill="#f7f6f2" '
               f'stroke="{GRID}"/>')
    out.append(txt(14, 222, "Regra 5 piora o caso:", 10.5, INK, weight="700"))
    out.append(txt(14, 236, "uma linha que lista só algumas colunas zera as outras - o vencedor "
                            "pode apagar colunas que o outro mod nem tocou.", 10, INK2))
    out.append("</svg>")
    return "".join(out)


def diagram_replacement(width=700):
    h = 228
    out = [svg_open(width, h, "patch PTF contra substituição da tabela inteira")]
    out.append(f'<rect x="0" y="0" width="330" height="{h}" rx="7" fill="#f3f8f4" '
               f'stroke="{S3}"/>')
    out.append(f'<rect x="366" y="0" width="334" height="{h}" rx="7" fill="#fdeeee" '
               f'stroke="{RED}"/>')
    out.append(txt(16, 22, "CERTO - patch PTF", 12, INK, weight="700"))
    out.append(txt(16, 38, "food__meumod.xml  (com sufixo)", 10, INK2, family="Consolas, monospace"))
    out.append(txt(382, 22, "ERRADO - tabela inteira", 12, INK, weight="700"))
    out.append(txt(382, 38, "food.xml  (sem sufixo)", 10, INK2, family="Consolas, monospace"))
    for i, (xx, col, rows_desc) in enumerate([(16, S3, ["linha 7", "linha 41"]),
                                              (382, RED, ["TODAS", "as 202 linhas"])]):
        out.append(f'<rect x="{xx}" y="54" width="120" height="118" rx="5" fill="{PAPER}" '
                   f'stroke="{GRID}"/>')
        out.append(txt(xx + 60, 72, "tabela food", 10, INK3, "middle", "700"))
        for k in range(6):
            fill = col if (i == 1 or k in (1, 4)) else "#e9e7e1"
            out.append(f'<rect x="{xx + 10}" y="{80 + k * 14}" width="100" height="10" rx="2" '
                       f'fill="{fill}" fill-opacity="{0.85 if fill != "#e9e7e1" else 1}"/>')
        out.append(txt(xx + 60, 188, "escreve: " + rows_desc[0], 9.5, INK2, "middle"))
        out.append(txt(xx + 60, 200, rows_desc[1], 9.5, INK2, "middle"))
    out.append(f'<path d="M142,112 H186" stroke="{S3}" stroke-width="1.8" marker-end="url(#ah)"/>')
    out.append(box(190, 76, 126, 72, "outros mods", ["mantêm os", "patches deles", "nessa tabela"],
                   PAPER, S3))
    out.append(f'<path d="M508,112 H552" stroke="{RED}" stroke-width="1.8" '
               f'marker-end="url(#ahr)"/>')
    out.append(box(556, 76, 130, 72, "outros mods", ["PERDEM tudo", "nessa tabela,", "e o 1.9.8 também"],
                   PAPER, RED))
    out.append("</svg>")
    return "".join(out)


def diagram_funnel(total, loads, no_load, legacy, width=700):
    h = 150
    out = [svg_open(width, h, "quantos mods carregam na versão 1.9.8")]
    segs = [(f"carregam: {loads}", loads, S3), (f"desativados pelo manifest: {no_load}", no_load, RED),
            (f"sem manifest (cópia manual): {legacy}", legacy, S4)]
    x = 0
    for lab, v, c in segs:
        w = (width) * v / total
        out.append(f'<path d="{bar_path(x + 1, 30, max(2.0, w - 2), 44, 4)}" fill="{c}"/>')
        out.append(txt(x + w / 2, 58, str(v), 15, PAPER, "middle", "700"))
        x += w
    out.append(txt(0, 18, f"Dos {total} mods com nota A-E, quantos o jogo 1.9.8 realmente carrega",
                   11.5, INK, weight="700"))
    y = 96
    for lab, v, c in segs:
        out.append(f'<rect x="0" y="{y - 9}" width="10" height="10" rx="2" fill="{c}"/>')
        out.append(txt(16, y, lab, 10.5, INK2))
        y += 17
    out.append("</svg>")
    return "".join(out)


# ---------------------------------------------------------------- page assembly
CSS = """
@page { size: A4; margin: 0; }
* { box-sizing: border-box; }
html, body { margin: 0; padding: 0; background: %(PAPER)s; color: %(INK)s;
  font-family: "Segoe UI", Calibri, Arial, sans-serif; -webkit-print-color-adjust: exact;
  print-color-adjust: exact; }
.page { width: 210mm; height: 297mm; padding: 15mm 16mm 13mm 16mm; page-break-after: always;
  position: relative; overflow: hidden; background: %(PAPER)s; }
.page:last-child { page-break-after: auto; }
.kicker { font-size: 8.5pt; letter-spacing: .14em; text-transform: uppercase; color: %(INK3)s;
  font-weight: 700; }
h1 { font-size: 27pt; line-height: 1.1; margin: 4mm 0 3mm; font-weight: 700; letter-spacing: -.01em; }
h2 { font-size: 16pt; margin: 0 0 1mm; font-weight: 700; letter-spacing: -.01em; }
h3 { font-size: 11pt; margin: 6mm 0 2mm; font-weight: 700; }
h3:first-of-type { margin-top: 4mm; }
p { font-size: 9.7pt; line-height: 1.5; margin: 0 0 2.6mm; color: %(INK)s; }
p.lead { font-size: 11pt; color: %(INK2)s; line-height: 1.45; }
p.small { font-size: 8.6pt; color: %(INK2)s; line-height: 1.45; }
.sub { font-size: 9.7pt; color: %(INK2)s; margin: 0 0 4mm; }
b { font-weight: 700; }
code { font-family: Consolas, "Courier New", monospace; font-size: 9pt; background: #f2f1ec;
  padding: .6mm 1.2mm; border-radius: 2px; }
.fig { margin: 3mm 0 2mm; }
.cap { font-size: 8.4pt; color: %(INK3)s; margin: 1mm 0 4mm; }
.cap b { color: %(INK2)s; }
.tiles { display: flex; gap: 3mm; margin: 4mm 0; flex-wrap: wrap; }
.tile { flex: 1 1 0; min-width: 28mm; border: 1.5px solid %(GRID)s; border-radius: 3mm;
  padding: 3mm; background: %(SURFACE)s; }
.tile .n { font-size: 19pt; font-weight: 700; line-height: 1; letter-spacing: -.02em; }
.tile .l { font-size: 7.8pt; color: %(INK2)s; line-height: 1.3; margin-top: 1.5mm; }
.tile.hl { background: #eef5fd; border-color: %(S1)s; }
.tile.warn { background: #fdeeee; border-color: %(RED)s; }
table { width: 100%%; border-collapse: collapse; font-size: 8.5pt; margin: 2mm 0 3mm; }
th { text-align: left; font-size: 7.6pt; text-transform: uppercase; letter-spacing: .07em;
  color: %(INK3)s; border-bottom: 1.2px solid %(INK3)s; padding: 1.4mm 1.6mm; font-weight: 700; }
td { padding: 1.3mm 1.6mm; border-bottom: .8px solid %(GRID)s; vertical-align: top;
  line-height: 1.35; }
td.n { text-align: right; font-variant-numeric: tabular-nums; white-space: nowrap; }
tr.top td { background: #eef5fd; }
tr.bad td { background: #fdeeee; }
.mono { font-family: Consolas, monospace; font-size: 8.2pt; }
table.tight td { padding: .95mm 1.6mm; font-size: 8.2pt; }
.pill { display: inline-block; font-size: 7.4pt; font-weight: 700; padding: .5mm 1.6mm;
  border-radius: 6px; color: #fff; }
.callout { border-left: 3px solid %(S1)s; background: #f7f6f2; padding: 3mm 3.5mm; margin: 3mm 0;
  border-radius: 0 2mm 2mm 0; }
.callout.warn { border-color: %(RED)s; background: #fdeeee; }
.callout.ok { border-color: %(S3)s; background: #f3f8f4; }
.callout p { margin: 0; font-size: 9.2pt; }
.callout .t { font-size: 8pt; font-weight: 700; text-transform: uppercase; letter-spacing: .09em;
  color: %(INK3)s; margin-bottom: 1.2mm; }
.two { display: flex; gap: 5mm; }
.two > div { flex: 1; }
.foot { position: absolute; left: 16mm; right: 16mm; bottom: 7mm; display: flex;
  justify-content: space-between; font-size: 7.4pt; color: %(INK3)s;
  border-top: .8px solid %(GRID)s; padding-top: 1.6mm; }
.cover { background: #12100e; color: #fff; height: 297mm; padding: 0; }
.cover .inner { padding: 18mm 18mm 0; }
.cover h1 { font-size: 34pt; color: #fff; margin-top: 8mm; }
.cover .kicker { color: #c9c4b4; }
.cover p { color: #d8d4c8; font-size: 11pt; }
.cover img { width: 100%%; display: block; }
.cover .band { position: absolute; left: 0; right: 0; bottom: 0; height: 92mm; overflow: hidden; }
.cover .meta { position: absolute; left: 18mm; bottom: 100mm; font-size: 9.5pt; color: #b9b4a4; }
.cover .meta b { color: #fff; }
.cover .badges { margin-top: 6mm; display: flex; gap: 2.5mm; flex-wrap: wrap; }
.cover .badge { border: 1px solid #4a463d; border-radius: 10px; padding: 1.2mm 3mm;
  font-size: 8.4pt; color: #d8d4c8; }
.toc { font-size: 9.5pt; }
.toc div { display: flex; justify-content: space-between; border-bottom: .8px dotted %(GRID)s;
  padding: 1.8mm 0; }
.toc span:last-child { color: %(INK3)s; }
""" % dict(PAPER=PAPER, INK=INK, INK2=INK2, INK3=INK3, GRID=GRID, SURFACE=SURFACE, S1=S1, S3=S3,
           RED=RED)


def tile(n, label, cls=""):
    return f'<div class="tile {cls}"><div class="n">{n}</div><div class="l">{label}</div></div>'


def page(num_, title, body, kicker=None):
    head = f'<div class="kicker">{esc(kicker)}</div>' if kicker else ""
    head += f"<h2>{esc(title)}</h2>" if title else ""
    return (f'<div class="page">{head}{body}'
            f'<div class="foot"><span>Kingdom Refinement Suite - mods A-E</span>'
            f'<span>{num_}</span></div></div>')


def build_html(data, logo_b64):
    P = []
    d = data

    # ---------------------------------------------------------------- 1 capa
    P.append(f"""<div class="page cover"><div class="inner">
      <div class="kicker">Kingdom Come: Deliverance - versão 1.9.8</div>
      <h1>Os mods A-E:<br>o que mudam,<br>quem é melhor,<br>onde se cruzam</h1>
      <p>Relatório ilustrado da análise somente-leitura de {d['n_mods']} mods: notas, sub-categorias,
      ranking e {d['n_pairs']} interseções entre eles.</p>
      <div class="badges"><div class="badge">nenhum mod instalado</div>
      <div class="badge">nenhum arquivo executado</div>
      <div class="badge">nenhuma partida aberta</div>
      <div class="badge">{d['n_arch']} arquivos lidos estaticamente</div></div></div>
      <div class="meta">Gerado em <b>{TODAY.day} de {MONTHS[TODAY.month - 1]} de {TODAY.year}</b><br>
      Fonte: docs/mods-review/ (MOD_ANALYSIS, MOD_SUBCATEGORIES, MOD_INTERSECTIONS)</div>
      <div class="band"><img src="data:image/jpeg;base64,{logo_b64}" alt="Kingdom Refinement Suite"></div>
      </div>""")

    # ---------------------------------------------------------------- 2 sumário
    toc = [("1. O que foi feito, em uma página", "3"), ("2. Como a pesquisa foi feita", "4"),
           ("3. As notas A-E", "5"), ("4. As 17 sub-categorias", "6"),
           ("5. As duas notas: efeito e construção", "7"),
           ("6. O que separa um mod bem feito de um mal feito", "8"),
           ("7. A regra do sufixo: o patch que o jogo ignora", "9"),
           ("8. Onde os mods se cruzam", "10"), ("9. As tabelas mais disputadas", "11"),
           ("10. Substituir a tabela inteira: o caso 883", "12"),
           ("11. Interseções com os módulos do KRS", "13"),
           ("12. Como usar isto na prática", "14"), ("13. Limites desta pesquisa", "15")]
    P.append(page(2, "Sumário", f"""
      <p class="lead">Este relatório responde a três perguntas, na ordem em que foram feitas:
      <b>o que cada mod muda</b>, <b>qual é o melhor de cada grupo</b> e <b>onde eles se atropelam</b>.</p>
      <div class="toc">{''.join(f'<div><span>{esc(t)}</span><span>{p}</span></div>' for t, p in toc)}</div>
      <div class="callout"><div class="t">Como ler os números</div>
      <p>Tudo aqui vem da leitura dos arquivos dos mods comparados com as tabelas do jogo
      (<code>Tables.pak</code> da versão 1.9.8). Um número alto significa <b>muda muito</b>, nunca
      <b>é bom</b>: nenhum mod foi jogado.</p></div>""", "Relatório ilustrado"))

    # ---------------------------------------------------------------- 3 resumo executivo
    P.append(page(3, "O que foi feito, em uma página", f"""
      <div class="tiles">
        {tile(d['n_mods'], "mods com nota A-E analisados")}
        {tile(17, "sub-categorias por arquivo/tabela que alteram", "hl")}
        {tile(33, "grupos nota + sub-categoria, cada um com ranking")}
        {tile(d['n_pairs'], "pares de mods que se cruzam", "hl")}
      </div>
      <div class="tiles">
        {tile(d['same_rows_pairs'], "pares escrevem a MESMA linha: só um vence")}
        {tile(14, "mods substituem tabelas inteiras", "warn")}
        {tile(d['no_load'], "não carregam no 1.9.8 (manifest antigo)", "warn")}
        {tile(d['krs_mods'], "mods disputam linhas com o próprio KRS", "warn")}
      </div>
      <h3>As três conclusões que mudam decisões</h3>
      <p><b>1. Os grandes rebalanceamentos são excludentes entre si.</b> 2124 e 2299 disputam
      <b>2766 linhas</b>; 2299 e 2340, 1565. Escolha um e trate os outros como fonte de ideias,
      não como complemento.</p>
      <p><b>2. O que separa um mod bem feito de um mal feito não é o tamanho, é o empacotamento.</b>
      Dos 10 piores em construção, 7 substituem tabelas inteiras em vez de aplicar patches PTF.
      O 883 sozinho sobrescreve 87 dos outros 88 mods que escrevem tabelas.</p>
      <p><b>3. Há mod que não faz nada.</b> O 1883 "Better Pickpocket - FIXED" tem sufixo de arquivo
      diferente do id do manifest: pela regra medida, o jogo nunca carrega o patch. Outros três
      (1652, 1673, 1996) não alteram nenhuma linha em relação ao vanilla.</p>
      <div class="callout ok"><div class="t">Base de evidência</div>
      <p>{d['n_arch']} arquivos compactados, pastas e paks dos {d['n_mods_all']} mods baixados foram
      lidos sem execução: listados, extraídos para pasta temporária, lidos e apagados. As tabelas
      foram comparadas célula por célula com o vanilla.</p></div>""", "Resumo executivo"))

    # ---------------------------------------------------------------- 4 método
    P.append(page(4, "Como a pesquisa foi feita", f"""
      <p class="sub">Cinco etapas, todas sem rodar nada do mod.</p>
      <div class="fig">{diagram_pipeline()}</div>
      <div class="two"><div>
        <h3>O que é "PTF"</h3>
        <p>O jogo guarda os números em tabelas (dano de arma, preço, perk, XP). Um mod pode
        <b>remendar</b> linhas dessas tabelas: é o formato PTF. O arquivo precisa chamar-se
        <code>tabela__&lt;id do mod&gt;.xml</code> e ficar em <code>Libs/Tables</code>.</p>
        <p>Quem acerta isso convive com os outros mods. Quem erra, apaga o trabalho alheio - ou é
        ignorado pelo jogo.</p>
      </div><div>
        <h3>As quatro camadas de profundidade</h3>
        <table><tr><th>Camada</th><th>O que é</th></tr>
        <tr><td><b>D0</b></td><td>conteúdo e texto (textura, modelo, áudio, legenda)</td></tr>
        <tr><td><b>D1</b></td><td>tabelas de dados (PTF) - o grosso dos mods</td></tr>
        <tr><td><b>D2</b></td><td>configuração do motor (<code>.cfg</code>)</td></tr>
        <tr><td><b>D3</b></td><td>scripts Lua</td></tr>
        <tr><td><b>D4</b></td><td>código nativo (DLL/ASI) ou ferramenta externa</td></tr></table>
        <p class="small">Os quatro mods D4 (2246, 2326, 2348, 2359) estão em quarentena: o que fazem
        não se lê nos arquivos.</p>
      </div></div>""", "Método"))

    # ---------------------------------------------------------------- 5 notas
    P.append(page(5, "As notas A-E", f"""
      <p class="sub">A nota responde "<b>quanto</b> este mod muda o jogo", não "é bom".</p>
      <div class="fig">{d['chart_grades']}</div>
      <div class="cap"><b>Como a nota é dada:</b> A = código nativo, ou 400+ linhas, ou 15+ tabelas,
      ou 3000+ linhas de Lua · B = 100+ linhas, 6+ tabelas ou 600+ linhas de Lua · C = pouquíssimas
      linhas, mas pelo menos uma linha central muda 20% ou mais · D = ajuste pequeno ·
      E = só conteúdo/texto, ou nada perceptível.</div>
      <h3>C é o grupo mais interessante do projeto</h3>
      <p>Quase 40% dos mods estão em C: poucas linhas, efeito forte. É onde se aprende mais por
      linha lida - um mod de <b>uma linha</b> como o 1425 (<code>ShoeHealthDecrease</code> de 0,001
      para 0) ou o 1938 (raio de colheita de erva de 0,25 para 0,5).</p>
      <div class="fig">{diagram_funnel(d['n_mods'], d['loads'], d['no_load'], d['legacy'])}</div>
      <div class="cap">O manifest lista as versões suportadas. Se a versão em execução não está na
      lista, o jogo <b>desativa o mod</b> - editar a linha resolve, mas é uma decisão do usuário.</div>
      """, "Panorama"))

    # ---------------------------------------------------------------- 6 sub-categorias
    P.append(page(6, "As 17 sub-categorias", f"""
      <p class="sub">A sub-categoria é <b>o arquivo que o mod escreve</b>, não o que a página dele diz.
      Dois mods no mesmo grupo remendam as mesmas tabelas - por isso também brigam entre si.</p>
      <div class="fig">{d['chart_subs']}</div>
      <div class="cap">Cada barra é uma sub-categoria, dividida pela nota dos mods que a compõem.
      O número à direita é o total.</div>
      <div class="callout"><div class="t">Quando o rótulo e o arquivo discordam</div>
      <p>O 2338 "Horse Collision Mod" é listado como mod de cavalo, mas <b>todas</b> as linhas que
      ele escreve são de perk e buff: ele cai no grupo dos perks, porque é com mods de perk que ele
      vai colidir. O rótulo temático fica ao lado, nunca no lugar.</p></div>
      <h3>Os campeões dos maiores grupos</h3>
      <table><tr><th>Nota</th><th>Sub-categoria</th><th class="n">Mods</th><th>Campeão</th>
      <th class="n">Geral</th></tr>{d['rows_winners']}</table>
      <div class="cap">Ranking = 0,55 x efeito + 0,45 x construção. Os 33 grupos completos estão em
      <b>MOD_SUBCATEGORIES.md</b>.</div>""", "Agrupamento"))

    # ---------------------------------------------------------------- 7 as duas notas
    P.append(page(7, "As duas notas: efeito e construção", f"""
      <p class="sub">Separar "muda muito" de "é bem feito" é o que torna o ranking útil.</p>
      <div class="two"><div>
        <div class="callout"><div class="t">Efeito - quanto muda, de 0 a 100</div>
        <p>28% volume de linhas alteradas (escala log) · 14% quantas tabelas · 18% tamanho relativo
        da mudança em cada célula · 20% perceptibilidade · 10% camadas D0-D4 · 10% tamanho da parte
        Lua/config.</p></div>
      </div><div>
        <div class="callout ok"><div class="t">Construção - quão bem feito, de 0 a 100</div>
        <p>Começa em 100. Descontos: -40 pak que não é ZIP · -35 manifest que não permite 1.9.8 ·
        -30 patch fora de <code>Libs/Tables</code> · -30 sufixo diferente do id do manifest ·
        até -25 substituir tabela inteira · até -15 linhas do vanilla apagadas · -25 risco ALTO.
        Bônus: +5 todos os patches com sufixo correto, +4 textos próprios, +3 leia-me.</p></div>
      </div></div>
      <div class="fig">{d['chart_scatter']}</div>
      <div class="cap">Cada ponto é um mod. <b>Canto superior direito</b> = muda muito e é bem
      empacotado (os melhores alvos de estudo). <b>Base</b> = mal empacotado, independentemente do
      tamanho. Só alguns mods estão rotulados, para o gráfico continuar legível.</div>
      <h3>Os cinco piores em construção - e por quê</h3>
      <table><tr><th>Mod</th><th class="n">Const.</th><th>Motivo medido</th></tr>
      {d['rows_worst']}</table>""", "Como pontuamos"))

    # ---------------------------------------------------------------- 8 patch vs substituição
    P.append(page(8, "O que separa um mod bem feito de um mal feito", f"""
      <p class="sub">Quase sempre é uma coisa só: o mod remenda linhas, ou troca a tabela inteira.</p>
      <div class="fig">{diagram_replacement()}</div>
      <h3>Como é um patch PTF correto (arquivo real do próprio KRS)</h3>
      <div class="fig">{d['code_patch']}</div>
      <div class="cap">Três linhas escritas, o resto da tabela intacto. O nome do arquivo termina com
      <code>__krs_qol</code>, que é exatamente o <code>&lt;modid&gt;</code> do manifest - a regra 1
      medida em <code>ptf-rules.md</code>.</div>
      <div class="callout warn"><div class="t">O contraexemplo</div>
      <p>O 2345 "Food and Drinks rebalance" entrega o mesmo tipo de conteúdo como
      <code>food.xml</code>, sem sufixo. Resultado: ele vence os mods 1483, 1639 e 2011 em todas as
      {d['food_rows']} linhas da tabela <code>food</code>, mesmo nas que nem pretendia mudar - e
      também desfaz o que o próprio 1.9.8 mudou ali.</p></div>
      <h3>Os 14 mods que substituem tabelas inteiras</h3>
      <p class="small mono">{d['replacers_line']}</p>""", "A diferença decisiva"))

    # ---------------------------------------------------------------- 9 sufixo
    P.append(page(9, "A regra do sufixo: o patch que o jogo ignora", f"""
      <p class="sub">Medido no jogo: se o sufixo do arquivo não é igual ao id do mod, o motor
      <b>ignora o arquivo em silêncio</b>. Nenhum erro, nenhum aviso.</p>
      <div class="fig">{d['code_suffix']}</div>
      <div class="cap">O caso <b>1883 Better Pickpocket - FIXED</b>: o manifest declara o id
      <code>BetterPickpocket</code>, o arquivo de tabela termina em <code>__better_pickpocket</code>.
      São nomes diferentes - e o id, pela regra 4, só aceita minúsculas e sublinhado.</div>
      <div class="two"><div>
        <h3>Onde essa regra pega de verdade</h3>
        <p><b>1 falha confirmada:</b> 1883, cujo manifest declara o id.</p>
        <p><b>5 dúvidas a confirmar:</b> 284, 1578, 1736, 1893 e 2124. Nesses, o manifest não traz
        <code>&lt;modid&gt;</code>, a análise teve de deduzir o id pelo nome do mod, e o pacote
        reúne vários sub-mods com um manifest cada - então a comparação pode ser falso positivo.
        Peso menor no ranking (-12 em vez de -30).</p>
      </div><div>
        <h3>E o manifest de versão</h3>
        <div class="fig">{d['code_manifest']}</div>
        <p class="small">Os {d['no_load']} mods que não carregam no 1.9.8 têm esta lista sem a
        linha <code>1.9.8</code>. É a correção mais barata do lote: uma linha de texto.</p>
      </div></div>""", "Armadilha nº 1"))

    # ---------------------------------------------------------------- 10 interseções
    P.append(page(10, "Onde os mods se cruzam", f"""
      <p class="sub">Dos {d['n_mods']} mods, {d['n_touch']} escrevem linhas de tabela. Entre eles,
      <b>{d['n_pairs']} pares se cruzam</b> - de quatro maneiras bem diferentes.</p>
      <div class="tiles">
        {tile(d['k_rows'], "pares escrevem as MESMAS linhas", "warn")}
        {tile(d['k_both'], "mesmas linhas + substituição de tabela", "warn")}
        {tile(d['k_repl'], "substituição de tabela que atinge o outro")}
        {tile(d['k_table'], "mesma tabela, linhas diferentes: convivem", "hl")}
      </div>
      <div class="fig">{diagram_rule6()}</div>
      <h3>Os dez pares que mais disputam linhas</h3>
      <table><tr><th>Mod A</th><th>Mod B</th><th class="n">Linhas</th><th>Onde</th></tr>
      {d['rows_pairs']}</table>
      <div class="callout warn"><div class="t">A leitura prática</div>
      <p>Os quatro grandes rebalanceamentos (2124, 2299, 2340, 883) formam um bloco em que todos
      disputam centenas a milhares de linhas entre si. Não é questão de ordem de carga: é escolher
      <b>um</b>.</p></div>""", "Interseções"))

    # ---------------------------------------------------------------- 11 tabelas disputadas
    P.append(page(11, "As tabelas mais disputadas", f"""
      <p class="sub">Quantas linhas de cada tabela são escritas por dois ou mais mods.</p>
      <div class="fig">{d['chart_tables']}</div>
      <div class="cap">4605 linhas do jogo são disputadas. <code>pickable_item</code> (preço, peso e
      dono de cada objeto) lidera porque quase todo mod de economia, loot ou item passa por ela.</div>
      <h3>O caso mais nítido: as nove modificações de arco</h3>
      <div class="fig">{d['code_archery']}</div>
      <div class="cap">As mesmas dez linhas de <code>ammo</code> são escritas por nove mods. Dentro
      do grupo de arco eles são <b>alternativas</b>, nunca soma. E 802 e 804 ainda substituem
      <code>rpg_param</code> inteira, atingindo mods que nada têm a ver com arco.</div>
      <h3>As linhas individuais mais concorridas</h3>
      <table><tr><th>Tabela</th><th>Linha</th><th class="n">Mods</th><th>Quais</th></tr>
      {d['rows_contested']}</table>""", "Pontos de atrito"))

    # ---------------------------------------------------------------- 12 caso 883
    P.append(page(12, "Substituir a tabela inteira: o caso 883", f"""
      <p class="sub">Quantos <b>outros</b> mods cada substituidor sobrescreve (os 7 maiores).</p>
      <div class="fig">{d['chart_override']}</div>
      <div class="cap">O 883 "KingdomCome Rebalancing" entrega uma cópia completa das tabelas do
      jogo: <b>398 tabelas sem sufixo</b>. Qualquer mod que escreva qualquer uma delas perde tudo
      onde o 883 carregar depois.</div>
      <div class="callout warn"><div class="t">Dois efeitos colaterais menos óbvios</div>
      <p>Substituir a tabela também desfaz as correções que a Warhorse fez nas versões 1.9.7 e 1.9.8
      nela - o mod não só vence os outros mods, ele volta o jogo atrás. E não é privilégio de mod
      grande: 802, 804 e 1334 são mods pequenos, de nota C, que trocam <code>rpg_param</code> (a
      tabela global de parâmetros) e com isso sobrescrevem 38 outros mods cada um.</p></div>
      <h3>Todos os 14, com o alcance de cada um</h3>
      <table class="tight"><tr><th>Mod</th><th>Nota</th><th class="n">Tabelas trocadas</th>
      <th class="n">Outros mods atingidos</th><th>Tabelas em disputa</th></tr>
      {d['rows_replacers']}</table>""", "O pior caso"))

    # ---------------------------------------------------------------- 13 KRS
    P.append(page(13, "Interseções com os módulos do KRS", f"""
      <p class="sub">{d['krs_mods']} mods de terceiros escrevem {d['krs_rows']} linhas que os módulos
      do próprio suite também escrevem. Cada uma é uma decisão, não um defeito.</p>
      <div class="fig">{d['code_krs']}</div>
      <div class="cap">O arquivo real <code>modules/krs_qol/Data/Libs/Tables/rpg/rpg_param__krs_qol.xml</code>:
      suas três linhas são exatamente três pontos de disputa. As setas mostram quais mods de
      terceiros escrevem a mesma linha.</div>
      <h3>As linhas disputadas com o KRS, por frequência</h3>
      <table><tr><th>Módulo</th><th>Linha</th><th class="n">Mods</th><th>Quais</th></tr>
      {d['rows_krs']}</table>
      <div class="callout"><div class="t">Lacuna de dados registrada</div>
      <p>A lista de colisões com o KRS não é uma coluna de <code>mod_analysis.csv</code> e a linha
      correspondente em <code>MOD_PROFILES.md</code> é cortada em 300 caracteres - por isso a lista
      do mod 1950 está incompleta aqui. Fechá-la exige reexecutar a análise profunda, que relê os
      arquivos compactados.</p></div>""", "Contra o próprio projeto"))

    # ---------------------------------------------------------------- 14 prática
    P.append(page(14, "Como usar isto na prática", f"""
      <p class="sub">Quatro regras que saem direto dos dados.</p>
      <h3>1. Escolha um grande rebalanceamento, no máximo</h3>
      <p>2299 (melhor construção do lote: 100) ou 2124 (muda mais: efeito 79) ou 2340 ou 883 - nunca
      dois. Entre si disputam de 777 a 2766 linhas.</p>
      <h3>2. Dentro de uma sub-categoria, um mod por vez</h3>
      <p>Nos grupos de arco, comida e sono, todos os membros escrevem as mesmas linhas. O ranking de
      cada grupo já diz qual tem a melhor combinação de efeito e empacotamento.</p>
      <h3>3. Evite os substituidores de tabela quando houver alternativa</h3>
      <p>Exemplos diretos: prefira <b>1483</b> ou <b>1639</b> a <b>2345</b> (comida); prefira
      <b>1565/1419/1678</b> a <b>802/804</b> (arco); no sono não há alternativa limpa - 480, 1062 e
      1424 trocam todos a mesma tabela inteira.</p>
      <h3>4. Antes de instalar, resolva as três linhas do KRS</h3>
      <p><code>RepairPriceModif</code>, <code>HerbGatherSkillToRadius</code> e
      <code>StrengthToInventoryCapacity</code> são as linhas do suite mais disputadas. Decida, por
      linha, se quem manda é o KRS ou o mod.</p>
      <div class="callout ok"><div class="t">O que dá para corrigir de graça</div>
      <p>{d['no_load']} mods não carregam no 1.9.8 só porque o manifest não lista a versão. É uma
      linha de texto em cada um. Mas é uma edição do arquivo de terceiros: decisão do autor do
      projeto, não automática.</p></div>
      <h3>Arquivos que sustentam este relatório</h3>
      <table><tr><th>Arquivo</th><th>O que traz</th></tr>
      <tr><td class="mono">MOD_ANALYSIS.md</td><td>notas A-E, regras e risco dos 138 arquivos</td></tr>
      <tr><td class="mono">MOD_PROFILES.md</td><td>uma seção por arquivo compactado</td></tr>
      <tr><td class="mono">MOD_SUBCATEGORIES.md</td><td>17 sub-categorias, 33 grupos, ranking</td></tr>
      <tr><td class="mono">MOD_INTERSECTIONS.md</td><td>os {d['n_pairs']} pares e as linhas do KRS</td></tr>
      <tr><td class="mono">mod_overlap.csv</td><td>as 4605 linhas disputadas, uma por registro</td></tr>
      </table>""", "Decisões"))

    # ---------------------------------------------------------------- 15 limites
    P.append(page(15, "Limites desta pesquisa", f"""
      <p class="sub">O que estes números <b>não</b> dizem - lido junto com o resto, evita conclusão
      errada.</p>
      <div class="callout warn"><div class="t">Nenhum mod foi jogado</div>
      <p>Nada foi instalado nem executado e nenhuma partida foi aberta. Isto é o que está escrito nos
      arquivos. Se um mod é divertido, equilibrado ou estável no jogo, este relatório não sabe.</p></div>
      <div class="callout"><div class="t">Nota alta não é elogio</div>
      <p>Efeito alto significa "muda muito". Um mod A pode ser desequilibrado e um mod C de uma linha
      pode ser exatamente o que o projeto precisa.</p></div>
      <div class="callout"><div class="t">Três camadas são invisíveis a este método</div>
      <p>XML que não é tabela (entidades, partículas, áudio), código nativo e texturas não podem ser
      comparados com o vanilla por leitura. Os {d['no_tables']} mods sem nenhuma linha de tabela -
      incluindo os quatro nativos - recebem efeito baixo mesmo quando funcionam perfeitamente, e as
      colisões de Lua, <code>.cfg</code> e textura entre eles não aparecem.</p></div>
      <div class="callout"><div class="t">Popularidade e atualização ficaram fora</div>
      <p>Endossos, versões e datas do Nexus não estão nos dados (só alguns mods os têm), então nada
      no ranking reflete quão recente ou popular um mod é.</p></div>
      <div class="callout"><div class="t">Duas contagens foram corrigidas</div>
      <p><code>MOD_ANALYSIS.md</code> soma o mesmo patch quando o pacote traz opções alternativas
      (pastas 2X/3X/5X) e conta <b>arquivos</b> de tabela em vez de tabelas distintas. Aqui cada
      patch conta uma vez: o 2294 aparece com 2985 linhas em 55 arquivos lá e 1300 linhas em 10
      tabelas aqui. As duas contagens estão no CSV.</p></div>
      <div class="callout"><div class="t">A ordem de carga decide, e ela é local</div>
      <p>Toda interseção de linha é resolvida pelo <code>mod_order.txt</code> da instalação. Este
      relatório diz <b>onde</b> haverá disputa, não quem vence na sua máquina.</p></div>
      <p class="small">Relatório gerado por <code>tools/build_report_pdf.py</code> a partir dos CSVs
      de <code>docs/mods-review/</code>. Nenhum arquivo compactado foi aberto para produzi-lo.</p>
      """, "Honestidade do método"))
    return (f'<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">'
            f'<title>Relatório dos mods A-E</title><style>{CSS}</style></head><body>'
            f'{"".join(P)}</body></html>')


# ---------------------------------------------------------------- data
def gather():
    sub = read_csv("mod_subcategories.csv")
    ints = read_csv("mod_intersections.csv")
    analysis = read_csv("mod_analysis.csv")
    overlap = read_csv("mod_overlap.csv")
    by_id = {r["id"]: r for r in sub}
    d = {}
    d["n_mods"] = len(sub)
    d["n_mods_all"] = len({r["id"] for r in analysis})
    d["n_arch"] = len(analysis)
    d["n_pairs"] = len(ints)
    kinds = collections.Counter(r["kind"] for r in ints)
    d["k_rows"] = kinds["same rows"]
    d["k_both"] = kinds["same rows + whole-table replacement"]
    d["k_repl"] = kinds["whole-table replacement"]
    d["k_table"] = kinds["same table only"]
    d["same_rows_pairs"] = d["k_rows"] + d["k_both"]
    d["n_touch"] = len({r["mod_a"] for r in ints} | {r["mod_b"] for r in ints})
    loads = collections.Counter("no" if r["loads_on_1_9_8"].startswith("NO")
                                else "legacy" if r["loads_on_1_9_8"].startswith("no manifest")
                                else "yes" for r in sub)
    d["loads"], d["no_load"], d["legacy"] = loads["yes"], loads["no"], loads["legacy"]
    d["no_tables"] = sum(1 for r in sub if not num(r["tables_touched"], int))

    # grades
    gc = collections.Counter(r["grade"][0] for r in sub)
    names = {"A": "A  muda mais", "B": "B  grande", "C": "C  poucas linhas, efeito forte",
             "D": "D  ajuste pequeno", "E": "E  conteúdo/texto ou nada"}
    d["chart_grades"] = hbar_chart([(names[g], gc[g]) for g in "ABCDE"], "mods por nota",
                                   left=230, highlight={names[g]: GRADE_COLOR[g] for g in "ABCDE"},
                                   note_fmt=lambda n, v: f"{v:.0f} mods")

    # sub-categories stacked by grade
    sc = collections.defaultdict(collections.Counter)
    for r in sub:
        sc[r["subcategory"]][r["grade"][0]] += 1
    short = {"Non-table XML (entities, effects, audio definitions)": "XML que não é tabela",
             "Textures, models and other assets": "Texturas, modelos, assets",
             "Alchemy, food and survival": "Alquimia, comida, sobrevivência",
             "Economy, loot and item stats": "Economia, loot, atributos de item",
             "Perks, skills and XP": "Perks, perícias e XP",
             "Combat mechanics and AI": "Combate e IA", "Lua scripts only": "Só scripts Lua",
             "Archery: bows, arrows, aiming": "Arco, flechas e mira",
             "Weapons, armour and durability": "Armas, armadura, durabilidade",
             "Multi-system overhaul": "Revisão multi-sistema",
             "NPCs, quests and world content": "NPCs, missões, mundo",
             "Native code and external tools": "Código nativo / ferramenta",
             "UI text and localisation": "Texto de interface e tradução",
             "Nothing readable / no change found": "Nada legível / sem mudança",
             "Engine config (.cfg) only": "Só config do motor (.cfg)",
             "NPC perks, skills and archetypes": "Perks de NPC",
             "Crime, stealth and reputation": "Crime, furtividade, reputação"}
    rows = sorted(((short.get(k, k), dict(v)) for k, v in sc.items()),
                  key=lambda kv: -sum(kv[1].values()))
    d["chart_subs"] = stacked_chart(rows, list("ABCDE"), GRADE_COLOR, "sub-categorias por nota",
                                    left=230, row_h=26)

    # winners per big group
    groups = collections.defaultdict(list)
    for r in sub:
        groups[(r["grade"][0], r["subcategory"])].append(r)
    big = sorted(groups.items(), key=lambda kv: -len(kv[1]))[:7]
    out = []
    for (g, s), members in big:
        win = min(members, key=lambda r: int(r["rank"]))
        out.append(f'<tr><td><b>{g}</b></td><td>{esc(short.get(s, s))}</td>'
                   f'<td class="n">{len(members)}</td>'
                   f'<td><b>{win["id"]}</b> {esc(clip_name(win["name"], 34))}</td>'
                   f'<td class="n">{num(win["overall"]):.0f}</td></tr>')
    d["rows_winners"] = "".join(out)

    # scatter
    show = {"2299", "2124", "883", "2049", "85", "1424", "1736", "1629", "1883", "1040", "1660"}
    d["chart_scatter"] = scatter_chart(
        [(num(r["effect"]), num(r["build"]), f'{r["id"]}', r["id"] in show) for r in sub],
        "efeito contra construção")

    worst = sorted(sub, key=lambda r: num(r["build"]))[:5]
    reason = {"85": "6 de 6 arquivos trocam a tabela inteira; apagam 156 linhas do vanilla; "
                    "não carrega no 1.9.8",
              "1424": "troca a tabela inteira de pontos de dormir e não carrega no 1.9.8",
              "1629": "troca metade dos arquivos de tabela e apaga 4692 linhas do vanilla",
              "2124": "3 arquivos trocam tabelas inteiras, apagam 3344 linhas; não carrega no 1.9.8",
              "770": "5 de 5 arquivos trocam a tabela inteira; risco ALTO (quarentena)"}
    d["rows_worst"] = "".join(
        f'<tr class="bad"><td><b>{r["id"]}</b> {esc(clip_name(r["name"], 30))}</td>'
        f'<td class="n">{num(r["build"]):.0f}</td>'
        f'<td>{esc(reason.get(r["id"], r["build_notes"][:90]))}</td></tr>' for r in worst)

    # replacers
    repl = [r for r in sub if num(r["whole_table_replacements"], int)]
    d["replacers_line"] = " · ".join(f'{r["id"]} ({r["whole_table_replacements"]} de '
                                     f'{r["table_files"]})' for r in sorted(
                                         repl, key=lambda r: -num(r["whole_table_replacements"], int)))
    d["food_rows"] = 202

    # pairs table
    top = [r for r in ints if num(r["shared_rows"], int)][:10]
    d["rows_pairs"] = "".join(
        f'<tr{" class=top" if i < 4 else ""}><td><b>{r["mod_a"]}</b> {esc(clip_name(r["name_a"], 22))}</td>'
        f'<td><b>{r["mod_b"]}</b> {esc(clip_name(r["name_b"], 22))}</td>'
        f'<td class="n"><b>{int(num(r["shared_rows"]))}</b></td>'
        f'<td class="mono">{esc(clip_list(r["tables_with_shared_rows"], 52))}</td></tr>'
        for i, r in enumerate(top))

    # contested tables / rows
    tc = collections.Counter(r["table"] for r in overlap)
    d["chart_tables"] = hbar_chart([(t, n) for t, n in tc.most_common(10)],
                                   "linhas disputadas por tabela", left=190,
                                   color=BLUE_SEQ[4], note_fmt=lambda n, v: f"{v:,.0f}".replace(",", "."))
    hot = sorted(overlap, key=lambda r: -num(r["mods_changing_it"], int))[:8]
    d["rows_contested"] = "".join(
        f'<tr><td class="mono">{esc(r["table"])}</td>'
        f'<td class="mono">{esc(clip_name(r["key"], 34))}</td>'
        f'<td class="n"><b>{r["mods_changing_it"]}</b></td>'
        f'<td class="mono">{esc(clip_list(r["mod_ids"], 48, " "))}</td></tr>' for r in hot)

    # override chart
    rep_counts = []
    touch = collections.defaultdict(set)
    replace = collections.defaultdict(set)
    for r in read_csv("mod_tables.csv"):
        base = os.path.basename(r["file_in_mod"].replace("\\", "/"))
        name = base[:-4] if base.lower().endswith(".xml") else base
        if r["style"] == "exact" and "__" not in name:
            replace[r["id"]].add(r["vanilla_table"])
        if num(r["new"], int) + num(r["changed"], int) > 0:
            touch[r["id"]].add(r["vanilla_table"])
    for m, ts in replace.items():
        victims = {o for t in ts for o in touch if o != m and t in touch[o]}
        contested = sorted({t for t in ts if any(t in touch[o] for o in touch if o != m)})
        rep_counts.append((m, len(ts), len(victims), contested))
    rep_counts.sort(key=lambda x: (-x[2], -x[1]))
    d["chart_override"] = hbar_chart(
        [(f'{m} {by_id.get(m, {}).get("name", "")[:24]}', v) for m, _, v, _ in rep_counts[:7]],
        "mods sobrescritos por cada substituidor", left=230, color=S2,
        highlight={f'{rep_counts[0][0]} {by_id.get(rep_counts[0][0], {}).get("name", "")[:24]}': RED},
        note_fmt=lambda n, v: f"{v:.0f} mods")
    d["rows_replacers"] = "".join(
        f'<tr{" class=bad" if v >= 26 else ""}><td><b>{m}</b> '
        f'{esc(clip_name(by_id.get(m, {}).get("name", ""), 26))}</td>'
        f'<td>{by_id.get(m, {}).get("grade", " ")[:1]}</td><td class="n">{nt}</td>'
        f'<td class="n"><b>{v}</b></td>'
        f'<td class="mono">{esc(clip_list(", ".join(c), 46)) or "-"}</td></tr>'
        for m, nt, v, c in rep_counts)

    # KRS
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import mod_intersections as mi
    krs, krs_cut = mi.krs_rows()
    d["krs_mods"] = len(krs)
    d["krs_rows"] = sum(len(v) for t in krs.values() for v in t.values())
    per_row = collections.defaultdict(set)
    for m, mods_ in krs.items():
        for module, keys in mods_.items():
            for k in keys:
                per_row[(module, k)].add(m)
    hot_krs = sorted(per_row.items(), key=lambda kv: -len(kv[1]))[:8]
    d["rows_krs"] = "".join(
        f'<tr{" class=top" if len(v) >= 5 else ""}><td class="mono">{esc(mod)}</td>'
        f'<td class="mono">{esc(k[:40])}</td><td class="n"><b>{len(v)}</b></td>'
        f'<td class="mono">{esc(" ".join(sorted(v, key=int)))}</td></tr>'
        for (mod, k), v in hot_krs)

    # ---------------- code figures
    patch = open(os.path.join(paths.MODULES, "krs_qol", "Data", "Libs", "Tables", "rpg",
                              "rpg_param__krs_qol.xml"), encoding="utf-8").read().splitlines()
    d["code_patch"] = code_svg(
        [(ln.rstrip(), S1 if "row " in ln else INK2 if "<" in ln else INK) for ln in patch],
        title="modules/krs_qol/Data/Libs/Tables/rpg/rpg_param__krs_qol.xml  (real)",
        marks=[(8, 0, 92, S3), (9, 0, 92, S3), (10, 0, 92, S3)],
        arrows=[(2, 20, "só a tabela rpg_param é tocada", S1, "r"),
                (9, 50, "3 linhas escritas - as demais ficam vanilla", S1, "r")])

    d["code_suffix"] = code_svg(
        [("mod.manifest", INK3),
         ("   <modid>BetterPickpocket</modid>", INK),
         ("", INK),
         ("BetterPickpocket/Data/better_pickpocket.pak", INK3),
         ("   Libs/Tables/rpg/rpg_param__better_pickpocket.xml", INK),
         ("", INK),
         ("   regra 1 (medida):  sufixo == id do mod  ->  aplicado", INK2),
         ("   sufixo != id do mod                     ->  IGNORADO em silêncio", INK2)],
        title="1883 Better Pickpocket - FIXED",
        marks=[(1, 10, 35, S1), (4, 25, 55, RED), (7, 3, 70, RED)],
        arrows=[(1, 20, "id declarado", S1, "r"), (4, 40, "sufixo diferente", RED, "r")])

    manifest = open(os.path.join(paths.MODULES, "krs_qol", "mod.manifest"),
                    encoding="utf-8").read().splitlines()
    keep = [ln for ln in manifest if "kcd_version" in ln or "supports" in ln]
    d["code_manifest"] = code_svg(
        [(ln.strip(), S1 if "1.9.8" in ln else INK2) for ln in keep],
        title="mod.manifest - lista de versões", fs=10.5, lh=15,
        marks=[(3, 0, 34, S3)],
        arrows=[(3, 14, "sem esta linha o jogo desativa o mod", S1, "r")])

    arch = ["ammo:  as mesmas 10 linhas de flecha",
            "       1376  1419  1565  1678  2035  2049  2124  2179  2299",
            "",
            "rpg_param:  Aim* / Bow* (constantes ocultas)",
            "       802  804  1419  1564  1678  ...",
            "",
            "802 e 804 entregam  rpg_param.xml  (sem sufixo)"]
    d["code_archery"] = code_svg(
        [(ln, INK if not ln.startswith("    ") else INK2) for ln in arch],
        title="o grupo de arco: 9 mods, nota C, as mesmas linhas", fs=11, lh=17,
        marks=[(1, 0, 70, S4), (6, 0, 60, RED)],
        arrows=[(1, 30, "9 mods na mesma linha: um vence", S4, "r"),
                (6, 30, "atinge 38 mods, não só os de arco", RED, "r")])

    krs_lines = [("<row rpg_param_key=\"StrengthToInventoryCapacity\" value=\"5\" />", INK),
                 ("<row rpg_param_key=\"HerbGatherSkillToRadius\"     value=\"0.35\" />", INK),
                 ("<row rpg_param_key=\"RepairPriceModif\"            value=\"1.3\" />", INK)]
    d["code_krs"] = code_svg(
        krs_lines, title="as três linhas do krs_qol - e quem as disputa", fs=11, lh=34,
        marks=[(0, 0, 64, S1), (1, 0, 64, S1), (2, 0, 64, S1)],
        arrows=[(0, 40, "651  883  1839  1860", RED, "r"),
                (1, 40, "1260  1558  1938  2210  2299", RED, "r"),
                (2, 40, "883  1842  2173  2188  2340", RED, "r")],
        height_extra=6)
    return d


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(D, "RELATORIO_MODS_A-E.pdf"))
    ap.add_argument("--browser", default="")
    ap.add_argument("--keep-html", action="store_true")
    args = ap.parse_args()

    logo = os.path.join(paths.ROOT, "Kingdom_Refinement_Suite_Logo_Banner.jpg")
    logo_b64 = base64.b64encode(open(logo, "rb").read()).decode() if os.path.exists(logo) else ""
    page_html = build_html(gather(), logo_b64)

    work = tempfile.mkdtemp(prefix="krs_report_")
    src = os.path.join(work, "report.html")
    with open(src, "w", encoding="utf-8") as f:
        f.write(page_html)

    exe = args.browser or next((b for b in BROWSERS if os.path.exists(b)), "")
    if not exe:
        sys.exit("no Edge or Chrome found: pass --browser <path to msedge.exe or chrome.exe>")
    out = os.path.abspath(args.out)
    cmd = [exe, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
           f"--print-to-pdf={out}", "--virtual-time-budget=4000",
           f"--user-data-dir={os.path.join(work, 'profile')}", src]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=240)
    if not os.path.exists(out):
        sys.exit(f"the browser did not write the PDF (exit {r.returncode}):\n{r.stderr[:800]}")
    print(f"wrote {os.path.relpath(out, paths.ROOT)} ({os.path.getsize(out) / 1024:.0f} KB)")
    if args.keep_html:
        kept = os.path.join(os.path.dirname(out), "RELATORIO_MODS_A-E.html")
        shutil.copy(src, kept)
        print("wrote", os.path.relpath(kept, paths.ROOT))
    else:
        shutil.rmtree(work, ignore_errors=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
