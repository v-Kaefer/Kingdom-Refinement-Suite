#!/usr/bin/env python3
"""page_style.py - the shared look of the review pages (one source of truth).

Light and dark are both chosen, not flipped: each mode has its own token values.
Used by tools/perks_workbench_page.py and tools/perks_round2_page.py.
"""

CSS = r"""<style>
/* layout: uma coluna de leitura, tabelas largas rolam dentro do próprio quadro */
:root {
  --bg:#f7f7f4; --surface:#ffffff; --line:#e0e0d8; --ink:#16181b; --ink2:#55585e;
  --ink3:#8b8e94; --accent:#2f6f9f; --accent-soft:#eaf2f8;
  --ok:#1a7f58; --ok-soft:#e9f5ef; --warn:#a9741a; --warn-soft:#fbf3e3;
  --bad:#b3372f; --bad-soft:#fbecea;
  --display:"Archivo Narrow",system-ui,sans-serif; --body:"Source Sans 3",system-ui,sans-serif;
  --mono:"JetBrains Mono",ui-monospace,Consolas,monospace;
  color-scheme: light;
}
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) {
  --bg:#15171a; --surface:#1c1f23; --line:#2e3237; --ink:#f2f3f4; --ink2:#b4b8bf;
  --ink3:#80858d; --accent:#6fa9d6; --accent-soft:#1d2a35;
  --ok:#5fc295; --ok-soft:#16281f; --warn:#d6a44f; --warn-soft:#2a2316;
  --bad:#e8847c; --bad-soft:#2c1a18; color-scheme: dark;
} }
:root[data-theme="dark"] {
  --bg:#15171a; --surface:#1c1f23; --line:#2e3237; --ink:#f2f3f4; --ink2:#b4b8bf;
  --ink3:#80858d; --accent:#6fa9d6; --accent-soft:#1d2a35;
  --ok:#5fc295; --ok-soft:#16281f; --warn:#d6a44f; --warn-soft:#2a2316;
  --bad:#e8847c; --bad-soft:#2c1a18; color-scheme: dark;
}
body { background:var(--bg); color:var(--ink); font-family:var(--body); font-size:16px;
  line-height:1.55; margin:0; }
.wrap { max-width:70rem; margin:0 auto; padding-inline:16px; padding-block:40px 64px; }
h1,h2,h3 { font-family:var(--display); text-wrap:balance; margin:0; letter-spacing:-.01em; }
h1 { font-size:clamp(2rem,5vw,3rem); line-height:1.05; }
h2 { font-size:1.6rem; margin-top:2.6rem; padding-top:1.4rem; border-top:2px solid var(--ink); }
h3 { font-size:1.12rem; margin-top:1.6rem; }
p { margin:.6rem 0; max-width:65ch; }
.lead { font-size:1.1rem; color:var(--ink2); }
.muted { color:var(--ink3); font-size:.84rem; line-height:1.35; }
.eyebrow { font-family:var(--display); text-transform:uppercase; letter-spacing:.14em;
  font-size:.78rem; color:var(--accent); font-weight:700; }
code { font-family:var(--mono); font-size:.84em; background:var(--accent-soft);
  padding:.1em .35em; border-radius:3px; }
.tiles { display:grid; grid-template-columns:repeat(auto-fit,minmax(150px,1fr)); gap:12px;
  margin:1.6rem 0; }
.tile { background:var(--surface); border:1px solid var(--line); border-radius:10px;
  padding:14px 16px; }
.tile .n { font-family:var(--display); font-size:2rem; line-height:1; font-variant-numeric:tabular-nums; }
.tile .l { font-size:.82rem; color:var(--ink2); margin-top:4px; }
.tile.hi { background:var(--accent-soft); border-color:var(--accent); }
.tablebox { overflow-x:auto; border:1px solid var(--line); border-radius:10px;
  background:var(--surface); margin:1rem 0; }
table { width:100%; border-collapse:collapse; font-size:.9rem; min-width:0; }
th { font-family:var(--display); text-align:left; text-transform:uppercase; font-size:.72rem;
  letter-spacing:.08em; color:var(--ink3); padding:10px 12px; border-bottom:1px solid var(--line);
  white-space:nowrap; }
td { padding:9px 12px; border-bottom:1px solid var(--line); vertical-align:top; }
tr:last-child td { border-bottom:0; }
td.num { text-align:right; font-variant-numeric:tabular-nums; }
.chip { display:inline-block; font-family:var(--display); font-weight:700; font-size:.72rem;
  letter-spacing:.06em; padding:3px 9px; border-radius:20px; white-space:nowrap; }
.chip.ok { background:var(--ok-soft); color:var(--ok); }
.chip.warn { background:var(--warn-soft); color:var(--warn); }
.chip.bad { background:var(--bad-soft); color:var(--bad); }
.why { font-size:.86rem; line-height:1.5; }
.chg { font-size:.8rem; line-height:1.7; white-space:nowrap; }
.chg .muted { white-space:normal; margin-top:2px; }
.why b { font-weight:600; }
.dim { color:var(--ink3); }
.was { background:var(--bad-soft); color:var(--bad); text-decoration:line-through; }
.is { background:var(--ok-soft); color:var(--ok); font-weight:700; }
.arrow { color:var(--ink3); margin:0 .45em; }
.note { border-left:3px solid var(--accent); background:var(--surface); padding:12px 16px;
  border-radius:0 8px 8px 0; margin:1.2rem 0; }
.note.warn { border-color:var(--warn); background:var(--warn-soft); }
.note.bad { border-color:var(--bad); background:var(--bad-soft); }
.note.ok { border-color:var(--ok); background:var(--ok-soft); }
.note .t { font-family:var(--display); text-transform:uppercase; letter-spacing:.1em;
  font-size:.74rem; color:var(--ink3); font-weight:700; }
.note p { margin:.35rem 0 0; }
.filters { display:flex; flex-wrap:wrap; gap:6px; margin:1rem 0 .4rem; }
button.f { font-family:var(--display); font-size:.84rem; font-weight:500; padding:5px 12px;
  border-radius:20px; border:1px solid var(--line); background:var(--surface); color:var(--ink2);
  cursor:pointer; }
button.f[aria-pressed="true"] { background:var(--accent); border-color:var(--accent);
  color:#fff; font-weight:700; }
button.f:focus-visible { outline:2px solid var(--accent); outline-offset:2px; }
.bars { display:grid; gap:6px; margin:1rem 0; }
.bar { display:grid; grid-template-columns:9rem 1fr 2.2rem; align-items:center; gap:10px; }
.bar .bl { font-size:.84rem; color:var(--ink2); }
.bar .bt { height:14px; background:var(--accent); border-radius:0 4px 4px 0; display:block; }
.bar .bn { font-family:var(--display); font-weight:700; font-variant-numeric:tabular-nums; }
.steps { counter-reset:s; display:grid; gap:14px; margin:1.2rem 0; }
.step { display:grid; grid-template-columns:2rem 1fr; gap:12px; }
.step::before { counter-increment:s; content:counter(s); font-family:var(--display);
  font-weight:700; color:var(--accent); background:var(--accent-soft); border-radius:50%;
  width:2rem; height:2rem; display:grid; place-items:center; }
.step h3 { margin:.1rem 0 .2rem; }
.pre { font-family:var(--mono); font-size:.8rem; background:var(--surface);
  border:1px solid var(--line); border-radius:8px; padding:12px 14px; overflow-x:auto;
  white-space:pre; margin:.8rem 0; }
.pre .add { color:var(--ok); } .pre .del { color:var(--bad); }
.pre .cmt { color:var(--ink3); }
footer { margin-top:3rem; padding-top:1rem; border-top:1px solid var(--line);
  font-size:.82rem; color:var(--ink3); }
@media (max-width:640px) { .bar { grid-template-columns:7rem 1fr 2rem; } }
</style>"""
