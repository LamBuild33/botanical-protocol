import os
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.makedirs(os.path.join(ROOT,"build"),exist_ok=True)
import re
base=open(os.path.join(ROOT,'src','protocol.html')).read()
def common(s):
    s=s.replace('<section class="before" aria-label="Before you start">','<section class="before" id="start" aria-label="Before you start">',1)
    return s
NAV_ITEMS=[('start','Start'),('doses','Amounts'),('buy','Shop'),('instructions','Make'),('cautions','Cautions'),('more','More')]
CSS_COMMON='''
.topnav { min-width: 0; position: sticky; top: env(safe-area-inset-top, 0px); z-index: 20; background: var(--bg); border-bottom: 1px solid var(--line); padding: 6px 0; }
body::before { content: ""; position: fixed; inset: 0 0 auto; height: env(safe-area-inset-top, 0px); z-index: 30; background: var(--bg); }
.topnav ul { list-style: none; margin: 0; padding: 0; display: flex; justify-content: space-between; gap: 2px; overflow-x: auto; scrollbar-width: none; }
.topnav ul::-webkit-scrollbar { display: none; }
.topnav a, .topnav button { display: inline-flex; align-items: center; font: inherit; font-size: 0.82rem; font-weight: 600; color: var(--muted); text-decoration: none; padding: 0 6px; height: 40px; border-radius: 999px; white-space: nowrap; border: 0; background: none; cursor: pointer; }
.topnav a.on, .topnav button.on { background: var(--accent-soft); color: var(--accent); }
.topnav a:focus-visible, .topnav button:focus-visible { outline: 2px solid var(--accent); outline-offset: 1px; }
section[id], div[id="more"] { scroll-margin-top: calc(env(safe-area-inset-top, 0px) + 64px); }
.steplist { font-size: 1.02rem; }
.steplist li { line-height: 1.55; }
.sgroup li { font-size: 1rem; }
.totop { position: fixed; right: calc(16px + env(safe-area-inset-right, 0px)); bottom: calc(16px + env(safe-area-inset-bottom, 0px)); z-index: 25; width: 46px; height: 46px; border-radius: 50%; border: 1px solid var(--line); background: var(--surface); color: var(--accent); font-size: 1.3rem; box-shadow: 0 2px 10px rgba(0,0,0,.15); cursor: pointer; }
'''
def wrap_more(s):
    i=s.index('  <details class="fold research" id="research">')
    j=s.index('  <p class="disclaimer">')
    return s[:i]+'  <div id="more" class="morewrap">\n    <h2>More</h2>\n'+s[i:j]+'  </div>\n'+s[j:]
def insert_nav(s, nav):
    k=s.index('</header>\n')+len('</header>\n')
    return s[:k]+nav+s[k:]
def add_css(s, css):
    return s.replace('</style>', css+'\n</style>',1)
def add_js(s, js):
    i=s.rindex('</script>')
    return s[:i]+js+'\n'+s[i:]

# ---------- Version A: jump bar ----------
a=wrap_more(common(base))
navA='  <nav class="topnav" aria-label="Sections"><ul>'+''.join(f'<li><a href="#{i}" data-sec="{i}">{t}</a></li>' for i,t in NAV_ITEMS)+'</ul></nav>\n'
a=insert_nav(a,navA)
a=a.replace('</div>\n\n<script>','</div>\n<button class="totop" id="totop" type="button" aria-label="Back to top" hidden>↑</button>\n\n<script>',1)
a=add_css(a,CSS_COMMON+'.morewrap { display: grid; gap: 22px; }\n.morewrap > h2 { margin-bottom: -10px; }\n')
jsA='''
(function () {
  const links = [...document.querySelectorAll('.topnav a')];
  const secs = links.map((l) => document.getElementById(l.dataset.sec)).filter(Boolean);
  const mark = (id) => links.forEach((l) => { const on = l.dataset.sec === id; l.classList.toggle('on', on); if (on) { l.setAttribute('aria-current', 'true'); const bar = l.closest('ul'); const r = l.getBoundingClientRect(), br = bar.getBoundingClientRect(); if (r.left < br.left || r.right > br.right) bar.scrollLeft += r.left - br.left - 24; } else l.removeAttribute('aria-current'); });
  const top = document.getElementById('totop');
  function onScroll() {
    const y = window.scrollY + 90; let cur = secs[0] ? secs[0].id : null;
    for (const s of secs) if (s.getBoundingClientRect().top + window.scrollY <= y) cur = s.id;
    mark(cur);
    if (top) top.hidden = window.scrollY < 600;
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  if (top) top.addEventListener('click', () => window.scrollTo({ top: 0, behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth' }));
  onScroll();
})();
'''
a=add_js(a,jsA)
a=a.replace('<title>Botanical Protocol</title>','<title>Botanical Protocol</title>',1)
open(os.path.join(ROOT,'build','jump.html'),'w').write(a)

# ---------- Version B: tabs ----------
b=wrap_more(common(base))
# group panels
def panel(s, start_marker, end_marker_after, pid):
    i=s.index(start_marker); j=s.index(end_marker_after,i)+len(end_marker_after)
    return s[:i]+f'  <div class="panel" id="{pid}" data-panel="{pid}">\n'+s[i:j]+'  </div>\n'+s[j:]
# Start panel = photo figure + before section
i=s0=b.index('  <figure class="photos"'); j=b.index('  </section>\n', b.index('id="start"'))+len('  </section>\n')
b=b[:i]+'  <div class="panel" data-panel="start">\n'+b[i:j]+'  </div>\n'+b[j:]
for pid,start in [('doses','  <section class="doses" id="doses">'),('buy','  <section class="steps" id="buy">'),('instructions','  <section class="steps" id="instructions">'),('cautions','  <section class="cautions" id="cautions">')]:
    i=b.index(start)
    # find matching section end (doses section contains nested sections; use depth count)
    k=i; depth=0
    for m in re.finditer(r'<(/?)section\b', b[i:]):
        depth += -1 if m.group(1) else 1
        if depth==0: k=i+m.end(); break
    k=b.index('>',k)+1; k=b.index('\n',k)+1
    b=b[:i]+f'  <div class="panel" data-panel="{pid}">\n'+b[i:k]+'  </div>\n'+b[k:]
b=b.replace('  <div id="more" class="morewrap">','  <div class="panel" data-panel="more">\n  <div id="more" class="morewrap">',1)
b=b.replace('  </div>\n  <p class="disclaimer">','  </div>\n  </div>\n  <p class="disclaimer">',1)
navB='  <nav class="topnav" aria-label="Sections"><ul role="tablist">'+''.join(f'<li><a href="#{i}" data-tab="{i}" role="tab">{t}</a></li>' for i,t in NAV_ITEMS)+'</ul></nav>\n'
b=insert_nav(b,navB)
b=add_css(b,CSS_COMMON+'.js-tabs .panel:not(.show) { display: none; }\n.panel { display: grid; gap: 22px; }\n.morewrap { display: grid; gap: 22px; }\n.morewrap > h2 { margin-bottom: -10px; }\n.tabnext { justify-self: end; font: inherit; font-weight: 600; color: var(--accent); background: var(--accent-soft); border: 0; border-radius: 999px; padding: 10px 16px; cursor: pointer; }\n')
jsB='''
(function () {
  const order = ['start','doses','buy','instructions','cautions','more'];
  const names = { start: 'Start', doses: 'Amounts', buy: 'Shop', instructions: 'Make', cautions: 'Cautions', more: 'More' };
  const panels = {}; document.querySelectorAll('.panel').forEach((p) => panels[p.dataset.panel] = p);
  const tabs = [...document.querySelectorAll('.topnav a')];
  document.documentElement.classList.add('js-tabs');
  order.forEach((id, i) => { const nxt = order[i + 1]; if (!nxt || !panels[id]) return; const btn = document.createElement('button'); btn.type = 'button'; btn.className = 'tabnext'; btn.textContent = 'Next: ' + names[nxt] + ' \\u2192'; btn.addEventListener('click', () => show(nxt, true)); panels[id].appendChild(btn); });
  function show(id, scroll) {
    if (!panels[id]) id = 'start';
    order.forEach((k) => panels[k] && panels[k].classList.toggle('show', k === id));
    tabs.forEach((t) => { const on = t.dataset.tab === id; t.classList.toggle('on', on); t.setAttribute('aria-selected', on ? 'true' : 'false'); if (on) { const bar = t.closest('ul'); const r = t.getBoundingClientRect(), br = bar.getBoundingClientRect(); if (r.left < br.left || r.right > br.right) bar.scrollLeft += r.left - br.left - 24; } });
    try { localStorage.setItem('bp-tab', id); } catch (e) {}
    if (scroll) { const nav = document.querySelector('.topnav'); window.scrollTo({ top: Math.max(0, nav.offsetTop - 4), behavior: 'auto' }); }
  }
  tabs.forEach((t) => t.addEventListener('click', (e) => { e.preventDefault(); show(t.dataset.tab, true); }));
  // Source links jump into the More tab first
  document.addEventListener('click', (e) => { const a = e.target.closest('a[href="#sources"]'); if (a) { show('more', false); } }, true);
  let start = 'start'; try { start = localStorage.getItem('bp-tab') || 'start'; } catch (e) {}
  const h = (location.hash || '').slice(1); if (order.includes(h)) start = h;
  show(start, false);
})();
'''
b=add_js(b,jsB)
open(os.path.join(ROOT,'build','tabs.html'),'w').write(b)
print('ok')
