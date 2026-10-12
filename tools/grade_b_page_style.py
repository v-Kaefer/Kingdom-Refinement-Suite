"""CSS and JS of the review pages (the display standard of the Grade D page), reused by tools/build_grade_b_page.py."""

CSS = r"""
:root{
  /* layout: faixa fixa de navegação no topo; uma coluna de leitura de até 72rem; tabelas rolam dentro do próprio bloco */
  --bg:#f3f5f8; --surface:#ffffff; --surface2:#eaeef3; --ink:#18212b; --muted:#566272; --line:#d5dce5; --accent:#1c6a86; --accent-ink:#ffffff;
  --ok:#17683f; --ok-bg:#dff2e7; --warn:#82540a; --warn-bg:#faedcf; --bad:#9c2b24; --bad-bg:#f7dedb; --info:#27527a; --info-bg:#dde9f6;
  --was:#9c2b24; --is:#17683f; --code-bg:#e9eef4;
  --f-display:"IBM Plex Sans Condensed","IBM Plex Sans","Segoe UI",system-ui,sans-serif; --f-body:"IBM Plex Sans","Segoe UI",system-ui,sans-serif; --f-mono:"IBM Plex Mono",ui-monospace,Consolas,monospace;
}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){
  --bg:#0e141a; --surface:#151d25; --surface2:#1c2630; --ink:#e4eaf1; --muted:#9aa7b6; --line:#2a3745; --accent:#59b4d3; --accent-ink:#06222c;
  --ok:#6fd19b; --ok-bg:#12301f; --warn:#e7bb68; --warn-bg:#35280d; --bad:#f09088; --bad-bg:#3a1714; --info:#8fbbe6; --info-bg:#14283d;
  --was:#f09088; --is:#6fd19b; --code-bg:#1d2833; color-scheme:dark}}
:root[data-theme="dark"]{
  --bg:#0e141a; --surface:#151d25; --surface2:#1c2630; --ink:#e4eaf1; --muted:#9aa7b6; --line:#2a3745; --accent:#59b4d3; --accent-ink:#06222c;
  --ok:#6fd19b; --ok-bg:#12301f; --warn:#e7bb68; --warn-bg:#35280d; --bad:#f09088; --bad-bg:#3a1714; --info:#8fbbe6; --info-bg:#14283d;
  --was:#f09088; --is:#6fd19b; --code-bg:#1d2833; color-scheme:dark}
body{background:var(--bg);color:var(--ink);font:15px/1.55 var(--f-body);padding-inline:16px}
*{box-sizing:border-box}
a{color:var(--accent)}
.top{position:sticky;top:env(safe-area-inset-top,0px);z-index:5;background:var(--bg);border-bottom:1px solid var(--line);margin-inline:-16px;padding:8px 16px;display:flex;gap:6px 14px;align-items:center;flex-wrap:wrap}
.top b{font-family:var(--f-display);font-size:1rem;letter-spacing:.02em;margin-right:6px}
.top nav{display:flex;gap:4px 12px;flex-wrap:wrap;min-width:0}
.top nav a{font-size:.85rem;text-decoration:none;color:var(--muted);padding:2px 0;border-bottom:2px solid transparent}
.top nav a:hover,.top nav a:focus-visible{color:var(--ink);border-color:var(--accent);outline:none}
main{max-width:76rem;margin-inline:auto;padding-block:20px 56px}
h1{font:600 clamp(1.7rem,4vw,2.4rem)/1.1 var(--f-display);margin:12px 0 6px;text-wrap:balance}
h2{font:600 1.45rem/1.2 var(--f-display);margin:44px 0 8px;padding-top:6px;border-top:2px solid var(--ink);text-wrap:balance}
h3{font:600 1.15rem/1.25 var(--f-display);margin:0 0 6px}
h4{font:600 .78rem/1.2 var(--f-display);text-transform:uppercase;letter-spacing:.07em;color:var(--muted);margin:0 0 4px}
p{margin:.3em 0}.lead{color:var(--muted);max-width:68ch}
.meta{color:var(--muted);font-size:.88rem}
code,.mono{font-family:var(--f-mono);font-size:.85em}
code{background:var(--code-bg);padding:0 .3em;border-radius:3px}
code.was{color:var(--was);text-decoration:line-through;background:transparent;padding:0}
code.is{color:var(--is);font-weight:600;background:transparent;padding:0}
.chip{display:inline-block;font:600 .72rem/1 var(--f-display);letter-spacing:.05em;text-transform:uppercase;padding:4px 7px;border-radius:3px;white-space:nowrap;text-decoration:none}
.chip.ok{background:var(--ok-bg);color:var(--ok)}.chip.warn{background:var(--warn-bg);color:var(--warn)}.chip.bad{background:var(--bad-bg);color:var(--bad)}.chip.info{background:var(--info-bg);color:var(--info)}
.cf{font:600 .62rem/1 var(--f-display);text-transform:uppercase;letter-spacing:.05em;padding:2px 4px;border-radius:2px;border:1px solid currentColor;vertical-align:1px;white-space:nowrap;margin-left:2px}
.cf-c{color:var(--ok)}.cf-d{color:var(--warn)}.cf-n{color:var(--bad)}
.legend{display:flex;gap:10px 18px;flex-wrap:wrap;margin:8px 0 0;font-size:.85rem;color:var(--muted)}
.scroll{overflow-x:auto;max-width:100%;border:1px solid var(--line);border-radius:4px;background:var(--surface)}
.t{border-collapse:collapse;width:100%;font-size:.88rem}
.t th{font:600 .72rem/1.2 var(--f-display);text-transform:uppercase;letter-spacing:.06em;text-align:left;color:var(--muted);background:var(--surface2);padding:8px 10px;position:sticky;top:0;white-space:nowrap}
.t td{padding:8px 10px;border-top:1px solid var(--line);vertical-align:top;min-width:0}
.t.compact td{padding:5px 8px}
.t td.num{font-variant-numeric:tabular-nums;white-space:nowrap}
.t td.wrap{overflow-wrap:anywhere;min-width:12rem}
.t td.mute{color:var(--muted)}
.t tr.conf td{background:color-mix(in srgb,var(--bad-bg) 40%,transparent)}
.cols{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,22rem),1fr));gap:14px;margin-top:14px}
.find{background:var(--surface);border:1px solid var(--line);border-radius:4px;padding:12px 14px;min-width:0}
.find h3{font-size:1rem}
.filters{display:flex;gap:10px;flex-wrap:wrap;align-items:end;margin:14px 0}
.filters label{display:flex;flex-direction:column;font-size:.75rem;color:var(--muted);gap:3px;text-transform:uppercase;letter-spacing:.05em}
.filters select,.filters input{font:inherit;font-size:.9rem;padding:6px 8px;border:1px solid var(--line);border-radius:3px;background:var(--surface);color:var(--ink);min-width:0}
.filters button{font:inherit;font-size:.85rem;padding:7px 10px;border:1px solid var(--line);border-radius:3px;background:var(--surface);color:var(--ink);cursor:pointer}
.filters button:hover{border-color:var(--accent)}
:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
.mod{background:var(--surface);border:1px solid var(--line);border-radius:4px;margin:8px 0}
.mod>summary{cursor:pointer;display:flex;gap:6px 12px;align-items:center;flex-wrap:wrap;padding:10px 12px;list-style:none}
.mod>summary::-webkit-details-marker{display:none}
.mod>summary::before{content:"▸";color:var(--muted);transition:transform .15s}
.mod[open]>summary::before{transform:rotate(90deg)}
.mod[open]>summary{border-bottom:1px solid var(--line)}
.mid{font:600 .9rem var(--f-mono);color:var(--accent)}
.mname{font:600 1rem var(--f-display);flex:1 1 14rem;min-width:0}
.msub{color:var(--muted);font-size:.8rem}
.mbody{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,21rem),1fr));gap:14px 22px;padding:14px}
.mbody section{min-width:0}.mbody .wide{grid-column:1/-1}
.mbody ul{margin:.2em 0;padding-left:1.1em}.mbody li{margin:.15em 0}
.none{color:var(--muted);font-style:italic;margin:.2em 0}
.snip{margin:8px 0;border:1px solid var(--line);border-radius:4px;overflow:hidden;background:var(--surface)}
.snip figcaption{font:600 .78rem var(--f-display);letter-spacing:.04em;padding:5px 10px;background:var(--surface2);color:var(--muted)}
.snip pre{margin:0;padding:10px;overflow-x:auto;font:.8rem/1.5 var(--f-mono);background:var(--code-bg)}
.snip pre code{background:none;padding:0}.snip .add{color:var(--is);display:block}
.snip p{padding:2px 10px 8px;color:var(--ink);font-size:.88rem}
.sub{margin:22px 0}.count{font:500 .8rem var(--f-body);color:var(--muted);margin-left:6px}
.bal{background:var(--surface);border:1px solid var(--line);border-radius:4px;padding:12px 14px;margin:12px 0;scroll-margin-top:70px}
.bal header{display:flex;gap:6px 12px;align-items:baseline;flex-wrap:wrap}
.bid{font:600 .85rem var(--f-mono);color:var(--accent)}.bmods{margin-left:auto;color:var(--muted);font-size:.82rem}
.dims{display:flex;gap:6px;flex-wrap:wrap;margin:6px 0}
.bal dl{display:grid;grid-template-columns:minmax(0,11rem) minmax(0,1fr);gap:6px 14px;margin:8px 0 0}
.bal dt{font:600 .74rem var(--f-display);text-transform:uppercase;letter-spacing:.06em;color:var(--muted);padding-top:2px}.bal dd{margin:0;min-width:0}
@media (max-width:640px){.bal dl{grid-template-columns:1fr}.bal dt{padding-top:8px}}
footer{margin-top:48px;color:var(--muted);font-size:.85rem;border-top:1px solid var(--line);padding-top:12px}
@media (prefers-reduced-motion:reduce){*{transition:none!important}}


/* --- additions for the Grade B page --- */
.t.matrix th.mod,.t.matrix td.mod{text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}
.t.matrix td.game{color:var(--muted);font-variant-numeric:tabular-nums;white-space:nowrap}
.t.matrix td.diff{background:color-mix(in srgb,var(--warn-bg) 55%,transparent)}
.t.matrix td.same{background:color-mix(in srgb,var(--ok-bg) 45%,transparent)}
.t.matrix td.na{color:var(--muted)}
.pdesc{display:block;color:var(--muted);font-size:.78rem;font-family:var(--f-body)}
.note{color:var(--muted);font-size:.85rem;margin:6px 0}
.badge{display:inline-block;font:600 .68rem/1 var(--f-display);letter-spacing:.05em;text-transform:uppercase;padding:2px 5px;border-radius:2px;background:var(--surface2);color:var(--muted);margin-right:4px}
.fam{border-left:4px solid var(--accent);padding:6px 12px;background:var(--surface);margin:10px 0}
.kv{display:grid;grid-template-columns:minmax(0,13rem) 1fr;gap:4px 14px;margin:6px 0}.kv dt{font-weight:600;color:var(--muted);font-size:.85rem}.kv dd{margin:0}
@media (max-width:640px){.kv{grid-template-columns:1fr}}
"""

JS = r"""
(function(){
  var sub=document.getElementById('f-sub'),ver=document.getElementById('f-ver'),q=document.getElementById('f-q'),cnt=document.getElementById('f-count');
  var mods=[].slice.call(document.querySelectorAll('details.mod'));
  function apply(){
    var s=sub.value,v=ver.value,t=q.value.trim().toLowerCase(),n=0;
    mods.forEach(function(m){
      var ok=(!s||m.dataset.sub===s)&&(!v||m.dataset.verdict===v)&&(!t||m.dataset.text.indexOf(t)>-1);
      m.hidden=!ok; if(ok)n++;
    });
    cnt.textContent=n+' de '+mods.length+' mods';
  }
  [sub,ver].forEach(function(e){e.addEventListener('change',apply)}); q.addEventListener('input',apply);
  document.getElementById('f-open').addEventListener('click',function(){mods.forEach(function(m){if(!m.hidden)m.open=true})});
  document.getElementById('f-close').addEventListener('click',function(){mods.forEach(function(m){m.open=false})});
  function openHash(){var h=location.hash.slice(1);if(!h)return;var el=document.getElementById(h);if(el&&el.tagName==='DETAILS'){el.open=true;el.hidden=false;}}
  window.addEventListener('hashchange',openHash);openHash();apply();
})();
"""
