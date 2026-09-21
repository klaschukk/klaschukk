#!/usr/bin/env python3
"""Generate every image of the profile README as self-contained animated SVG.

No third-party widgets (github-readme-stats & co. are rate-limited and go down,
and they cannot see private repos). Stats come from `gh api graphql` run by the
repo owner, so private contributions are counted (counts only, nothing leaks).

    gh api graphql -f query='...' > data/stats.json   # see refresh.sh
    python3 scripts/gen_assets.py
"""
import json
import math
from collections import Counter
from datetime import date, timedelta
from pathlib import Path
from xml.sax.saxutils import escape as esc

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'assets'
OUT.mkdir(exist_ok=True)
SANS = "system-ui,-apple-system,'Segoe UI',Roboto,Helvetica,Arial,sans-serif"
MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,'Liberation Mono',monospace"


def write(name: str, svg: str) -> None:
    (OUT / name).write_text(svg, encoding='utf-8')
    print(f'{name}: {len(svg):,} bytes')


def bez(p0, p1, p2, p3, t):
    u = 1 - t
    return tuple(u**3 * a + 3 * u * u * t * b + 3 * u * t * t * c + t**3 * d
                 for a, b, c, d in zip(p0, p1, p2, p3))


# ── banner ────────────────────────────────────────────────────────────────
def banner() -> str:
    W, H = 1200, 320
    p0, p1, p2, p3 = (-10, 292), (280, 190), (640, 340), (1210, 252)
    path = f'M{p0[0]},{p0[1]} C{p1[0]},{p1[1]} {p2[0]},{p2[1]} {p3[0]},{p3[1]}'
    stops = ''.join(
        f'<circle cx="{x:.0f}" cy="{y:.0f}" r="5" fill="#0b1020" stroke="#5eead4" stroke-width="2"/>'
        for x, y in (bez(p0, p1, p2, p3, t) for t in (0.12, 0.3, 0.5, 0.7, 0.88)))
    lines = [
        'Building products that ship, end to end.',
        'Data pipelines · Flask backends · programmatic SEO',
        'Now: growing prevozni.com across the Balkans',
    ]
    sub = ''.join(
        f'<text class="line l{i+1}" x="76" y="222" font-family="{MONO}" font-size="21" fill="#c9d1d9">'
        f'<tspan fill="#5eead4">$ </tspan>{esc(t)}<tspan class="caret" fill="#5eead4"> ▌</tspan></text>'
        for i, t in enumerate(lines))
    doms = [('prevozni.com', 96), ('valocheck.com', 146), ('flightpunctuality.online', 196)]
    chips = ''.join(
        f'<g class="chip" style="animation-delay:{i*0.25:.2f}s">'
        f'<rect x="800" y="{y}" width="340" height="38" rx="12" fill="#ffffff" fill-opacity=".05" '
        f'stroke="#ffffff" stroke-opacity=".14"/>'
        f'<circle cx="826" cy="{y+19}" r="4.5" fill="#34d399"><animate attributeName="r" values="3.5;6;3.5" '
        f'dur="2.4s" begin="{i*0.4:.1f}s" repeatCount="indefinite"/><animate attributeName="opacity" '
        f'values="1;.35;1" dur="2.4s" begin="{i*0.4:.1f}s" repeatCount="indefinite"/></circle>'
        f'<text x="844" y="{y+24}" font-family="{MONO}" font-size="16" fill="#e6edf3">{esc(d)}</text></g>'
        for i, (d, y) in enumerate(doms))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="klaschuk — builder of live web products">
<defs>
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0a0f1e"/><stop offset=".55" stop-color="#0d2233"/><stop offset="1" stop-color="#1a1245"/></linearGradient>
<linearGradient id="ttl" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#5eead4"/><stop offset=".5" stop-color="#38bdf8"/><stop offset="1" stop-color="#a78bfa"/></linearGradient>
<filter id="blur" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="46"/></filter>
<pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse"><path d="M40 0H0V40" fill="none" stroke="#ffffff" stroke-opacity=".045"/></pattern>
<clipPath id="r"><rect width="{W}" height="{H}" rx="22"/></clipPath>
</defs>
<style>
.line{{opacity:0;animation:cyc 15s infinite}} .l2{{animation-delay:5s}} .l3{{animation-delay:10s}}
@keyframes cyc{{0%{{opacity:0;transform:translateY(10px)}}4%{{opacity:1;transform:none}}30%{{opacity:1;transform:none}}34%{{opacity:0;transform:translateY(-10px)}}100%{{opacity:0}}}}
.caret{{animation:blink 1s steps(2,start) infinite}} @keyframes blink{{to{{opacity:0}}}}
.flow{{stroke-dasharray:7 9;animation:flow 1.6s linear infinite}} @keyframes flow{{to{{stroke-dashoffset:-16}}}}
.chip{{opacity:0;animation:up .9s ease-out forwards}} @keyframes up{{from{{opacity:0;transform:translateY(12px)}}to{{opacity:1;transform:none}}}}
.hi{{opacity:0;animation:up .9s .1s ease-out forwards}} .nm{{opacity:0;animation:up 1s .25s ease-out forwards}}
</style>
<g clip-path="url(#r)">
<rect width="{W}" height="{H}" fill="url(#bg)"/><rect width="{W}" height="{H}" fill="url(#grid)"/>
<g filter="url(#blur)">
<circle r="120" fill="#14b8a6" opacity=".35"><animate attributeName="cx" values="180;420;180" dur="16s" repeatCount="indefinite"/><animate attributeName="cy" values="70;260;70" dur="13s" repeatCount="indefinite"/></circle>
<circle r="140" fill="#6366f1" opacity=".32"><animate attributeName="cx" values="980;760;980" dur="19s" repeatCount="indefinite"/><animate attributeName="cy" values="260;60;260" dur="15s" repeatCount="indefinite"/></circle>
<circle r="90" fill="#0ea5e9" opacity=".25"><animate attributeName="cx" values="600;700;600" dur="11s" repeatCount="indefinite"/><animate attributeName="cy" values="300;140;300" dur="17s" repeatCount="indefinite"/></circle>
</g>
<path d="{path}" fill="none" stroke="#5eead4" stroke-opacity=".55" stroke-width="2" class="flow"/>
{stops}
<circle r="6" fill="#5eead4"><animateMotion dur="8s" repeatCount="indefinite" path="{path}"/></circle>
<circle r="14" fill="#5eead4" opacity=".25"><animateMotion dur="8s" repeatCount="indefinite" path="{path}"/></circle>
<text class="hi" x="78" y="104" font-family="{MONO}" font-size="14" letter-spacing="5" fill="#7d8590">HELLO, I'M</text>
<text class="nm" x="74" y="176" font-family="{SANS}" font-size="78" font-weight="800" fill="url(#ttl)">klaschuk</text>
{sub}
{chips}
</g>
<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="22" fill="none" stroke="#ffffff" stroke-opacity=".12"/>
</svg>'''


def divider() -> str:
    return '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 12" width="1200" height="12" role="presentation">
<defs><linearGradient id="g" x1="0" x2="1"><stop offset="0" stop-color="#5eead4" stop-opacity="0"/><stop offset=".5" stop-color="#5eead4"/><stop offset="1" stop-color="#a78bfa" stop-opacity="0"/></linearGradient></defs>
<style>.m{animation:mv 5s ease-in-out infinite alternate}@keyframes mv{from{transform:translateX(-420px)}to{transform:translateX(420px)}}</style>
<rect x="0" y="5" width="1200" height="2" fill="#ffffff" opacity=".08"/>
<rect class="m" x="390" y="4" width="420" height="4" rx="2" fill="url(#g)"/></svg>'''


# ── stack chips ───────────────────────────────────────────────────────────
def stack() -> str:
    rows = [
        [('Python', '#3776ab'), ('Flask', '#e6edf3'), ('DuckDB', '#fff000'), ('SQLite', '#0f80cc'),
         ('Jinja2', '#b41717'), ('Gunicorn', '#499848')],
        [('nginx', '#009639'), ('Cloudflare', '#f38020'), ('systemd', '#a78bfa'), ('TypeScript', '#3178c6'),
         ('React', '#61dafb'), ('Electron', '#47848f'), ('HTML · CSS', '#e34f26')],
    ]
    W, gap, h = 900, 12, 38
    body, k = [], 0
    for ri, row in enumerate(rows):
        widths = [30 + 8.2 * len(n) for n, _ in row]
        x = (W - (sum(widths) + gap * (len(row) - 1))) / 2
        y = 14 + ri * (h + 14)
        for (name, col), w in zip(row, widths):
            body.append(
                f'<g class="c" style="animation-delay:{k*0.35:.2f}s"><rect x="{x:.1f}" y="{y}" width="{w:.1f}" height="{h}" rx="12" '
                f'fill="#111827" stroke="#263244"/><circle cx="{x+16:.1f}" cy="{y+h/2}" r="5" fill="{col}"/>'
                f'<text x="{x+29:.1f}" y="{y+h/2+5}" font-family="{MONO}" font-size="14" fill="#e6edf3">{esc(name)}</text></g>')
            x += w + gap
            k += 1
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} 118" width="{W}" height="118" role="img" aria-label="Tech stack">
<style>.c{{animation:bob 4.4s ease-in-out infinite}}@keyframes bob{{50%{{transform:translateY(-4px)}}}}</style>
{''.join(body)}</svg>'''


# ── project cards ─────────────────────────────────────────────────────────
def card(uid, title, domain, l1, l2, chips, c1, c2) -> str:
    cx, chip_svg = 24, []
    for t in chips:
        w = 26 + 8.7 * len(t)
        chip_svg.append(f'<rect x="{cx}" y="170" width="{w:.0f}" height="30" rx="10" fill="{c1}" fill-opacity=".14" stroke="{c1}" stroke-opacity=".45"/>'
                        f'<text x="{cx+w/2:.0f}" y="190" text-anchor="middle" font-family="{MONO}" font-size="14" fill="#e6edf3">{esc(t)}</text>')
        cx += w + 8
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 226" width="400" height="226" role="img" aria-label="{esc(title)} — {esc(domain)}">
<defs><linearGradient id="a{uid}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{c1}"/><stop offset="1" stop-color="{c2}"/></linearGradient>
<linearGradient id="s{uid}" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".9"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
<radialGradient id="g{uid}" cx=".85" cy="0" r="1"><stop offset="0" stop-color="{c1}" stop-opacity=".35"/><stop offset="1" stop-color="{c1}" stop-opacity="0"/></radialGradient>
<clipPath id="k{uid}"><rect x="1" y="1" width="398" height="224" rx="20"/></clipPath></defs>
<style>.sh{{animation:sh 3.6s ease-in-out infinite}}@keyframes sh{{from{{transform:translateX(-160px)}}to{{transform:translateX(420px)}}}}
.in{{opacity:0;animation:u .8s ease-out forwards}}@keyframes u{{from{{opacity:0;transform:translateY(8px)}}to{{opacity:1;transform:none}}}}</style>
<rect x="1" y="1" width="398" height="224" rx="20" fill="#0d1421" stroke="#ffffff" stroke-opacity=".12"/>
<g clip-path="url(#k{uid})"><rect width="400" height="226" fill="url(#g{uid})"/>
<rect y="218" width="400" height="8" fill="url(#a{uid})"/><rect class="sh" y="218" width="160" height="8" fill="url(#s{uid})" opacity=".55"/></g>
<g class="in"><rect x="24" y="22" width="{34+8.8*len(domain):.0f}" height="30" rx="15" fill="#34d399" fill-opacity=".12" stroke="#34d399" stroke-opacity=".45"/>
<circle cx="42" cy="37" r="4.5" fill="#34d399"><animate attributeName="opacity" values="1;.3;1" dur="2s" repeatCount="indefinite"/></circle>
<text x="55" y="42" font-family="{MONO}" font-size="14" fill="#a7f3d0">{esc(domain)}</text></g>
<text class="in" style="animation-delay:.15s" x="24" y="98" font-family="{SANS}" font-size="36" font-weight="800" fill="url(#a{uid})">{esc(title)}</text>
<text class="in" style="animation-delay:.3s" x="24" y="128" font-family="{SANS}" font-size="17" fill="#c9d1d9">{esc(l1)}</text>
<text class="in" style="animation-delay:.4s" x="24" y="151" font-family="{SANS}" font-size="15" fill="#8b98a9">{esc(l2)}</text>
<g class="in" style="animation-delay:.55s">{''.join(chip_svg)}</g></svg>'''


# ── quotes ────────────────────────────────────────────────────────────────
def quotes() -> str:
    qs = [
        (['Talk is cheap. Show me the code.'], 'Linus Torvalds'),
        (['Make it work, make it right, make it fast.'], 'Kent Beck'),
        (['Perfection is achieved, not when there is nothing more to add,',
          'but when there is nothing left to take away.'], 'Antoine de Saint-Exupéry'),
    ]
    items = []
    for i, (ls, who) in enumerate(qs):
        y0 = 78 if len(ls) == 1 else 62
        t = ''.join(f'<text x="600" y="{y0+j*36}" text-anchor="middle" font-family="Georgia,\'Times New Roman\',serif" '
                    f'font-style="italic" font-size="28" fill="#e6edf3">{esc(l)}</text>' for j, l in enumerate(ls))
        items.append(f'<g class="q q{i+1}">{t}<text x="600" y="{y0+len(ls)*36+8}" text-anchor="middle" font-family="{MONO}" '
                     f'font-size="15" fill="#5eead4">— {esc(who)}</text></g>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 170" width="1200" height="170" role="img" aria-label="Quote">
<defs><linearGradient id="qb" x1="0" x2="1"><stop offset="0" stop-color="#0d1421"/><stop offset="1" stop-color="#121a33"/></linearGradient></defs>
<style>.q{{opacity:0;animation:qc 18s infinite}}.q2{{animation-delay:6s}}.q3{{animation-delay:12s}}
@keyframes qc{{0%{{opacity:0;transform:translateY(10px)}}3%{{opacity:1;transform:none}}30%{{opacity:1;transform:none}}33%{{opacity:0;transform:translateY(-10px)}}100%{{opacity:0}}}}
.mk{{animation:pl 5s ease-in-out infinite}}@keyframes pl{{50%{{opacity:.35}}}}</style>
<rect x=".5" y=".5" width="1199" height="169" rx="20" fill="url(#qb)" stroke="#ffffff" stroke-opacity=".12"/>
<text class="mk" x="46" y="128" font-family="Georgia,serif" font-size="140" fill="#5eead4" opacity=".22">“</text>
<text class="mk" x="1110" y="150" font-family="Georgia,serif" font-size="140" fill="#a78bfa" opacity=".22">”</text>
{''.join(items)}</svg>'''


# ── stats + heatmap (from real API data, private contributions included) ─
def stats(data: dict) -> str:
    v = data['data']['viewer']
    cc = v['contributionsCollection']
    cal = cc['contributionCalendar']
    days = [d for w in cal['weeks'] for d in w['contributionDays']]
    active = sum(1 for d in days if d['contributionCount'] > 0)
    streak = best = 0
    for d in days:
        streak = streak + 1 if d['contributionCount'] > 0 else 0
        best = max(best, streak)
    langs, colors = Counter(), {}
    for r in v['repositories']['nodes']:
        for e in r['languages']['edges']:
            langs[e['node']['name']] += e['size']
            colors[e['node']['name']] = e['node']['color'] or '#8b949e'
    total = sum(langs.values())
    top = [(n, 100 * s / total) for n, s in langs.most_common(5)]
    tiles = [(str(cal['totalContributions']), 'contributions · 12 mo'),
             (str(active), 'active days'),
             (str(best), 'day longest streak'),
             (str(v['repositories']['totalCount']), 'repositories')]
    tsv = ''.join(
        f'<g class="t" style="animation-delay:{i*0.12:.2f}s"><rect x="{28+i*212}" y="66" width="200" height="72" rx="14" fill="#111827" stroke="#263244"/>'
        f'<text x="{46+i*212}" y="108" font-family="{SANS}" font-size="34" font-weight="800" fill="#e6edf3">{esc(n)}</text>'
        f'<text x="{46+i*212}" y="127" font-family="{MONO}" font-size="12" fill="#7d8590">{esc(l)}</text></g>'
        for i, (n, l) in enumerate(tiles))
    lvl = ['#161e2c', '#0e4f4a', '#0f766e', '#14b8a6', '#5eead4']
    def level(c):
        return 0 if c == 0 else 1 if c <= 2 else 2 if c <= 6 else 3 if c <= 14 else 4
    cells, months, lastm = [], [], None
    for wi, w in enumerate(cal['weeks']):
        for d in w['contributionDays']:
            dt = date.fromisoformat(d['date'])
            cells.append(f'<rect class="h" style="animation-delay:{wi*0.028:.2f}s" x="{28+wi*15}" y="{176+d["weekday"]*15}" width="12" height="12" rx="3" fill="{lvl[level(d["contributionCount"])]}"><title>{d["date"]}: {d["contributionCount"]}</title></rect>')
        first = date.fromisoformat(w['contributionDays'][0]['date'])
        if first.month != lastm:
            if wi < 51 and not (wi == 0 and first.day > 7):
                months.append(f'<text x="{28+wi*15}" y="168" font-family="{MONO}" font-size="10.5" fill="#7d8590">{first.strftime("%b")}</text>')
            lastm = first.month
    bar, x, legend = [], 28.0, []
    for i, (n, p) in enumerate(top):
        w = 844 * p / sum(pp for _, pp in top)
        bar.append(f'<rect class="g" style="animation-delay:{0.9+i*0.15:.2f}s" x="{x:.1f}" y="304" width="{w:.1f}" height="10" fill="{colors[n]}"/>')
        lx = 28 + i * 168
        legend.append(f'<circle cx="{lx+5}" cy="334" r="5" fill="{colors[n]}"/><text x="{lx+16}" y="338" font-family="{MONO}" font-size="12" fill="#c9d1d9">{esc(n)} {p:.0f}%</text>')
        x += w
    since = v['createdAt'][:4]
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 356" width="900" height="356" role="img" aria-label="GitHub activity: {cal['totalContributions']} contributions in the last year">
<style>.t{{opacity:0;animation:u .7s ease-out forwards}}.h{{opacity:0;animation:f .5s ease-out forwards}}
.g{{transform-box:fill-box;transform-origin:left;transform:scaleX(0);animation:gr .8s ease-out forwards}}
@keyframes u{{from{{opacity:0;transform:translateY(10px)}}to{{opacity:1;transform:none}}}}@keyframes f{{to{{opacity:1}}}}@keyframes gr{{to{{transform:scaleX(1)}}}}</style>
<rect x=".5" y=".5" width="899" height="355" rx="20" fill="#0d1117" stroke="#ffffff" stroke-opacity=".12"/>
<text x="28" y="36" font-family="{SANS}" font-size="20" font-weight="700" fill="#e6edf3">Activity</text>
<text x="112" y="36" font-family="{MONO}" font-size="12" fill="#7d8590">last 12 months · private repos counted (numbers only) · on GitHub since {since}</text>
{tsv}{''.join(months)}{''.join(cells)}
<text x="28" y="296" font-family="{MONO}" font-size="12" fill="#7d8590">languages across all repositories</text>
<rect x="28" y="304" width="844" height="10" rx="5" fill="#161e2c"/><clipPath id="lc"><rect x="28" y="304" width="844" height="10" rx="5"/></clipPath><g clip-path="url(#lc)">{''.join(bar)}</g>
{''.join(legend)}</svg>'''


if __name__ == '__main__':
    data = json.loads((ROOT / 'data' / 'stats.json').read_text())
    write('banner.svg', banner())
    write('divider.svg', divider())
    write('stack.svg', stack())
    write('quote.svg', quotes())
    write('stats.svg', stats(data))
    write('card-prevozni.svg', card('p', 'Prevozni', 'prevozni.com', 'Free timetables for Serbia & Montenegro',
                                    '500+ routes · 3,400+ stops · 4 languages', ['Flask', 'DuckDB', 'SEO'], '#2dd4bf', '#38bdf8'))
    write('card-valocheck.svg', card('v', 'ValoCheck', 'valocheck.com', 'Fast Valorant stat checker',
                                     'Profiles, leaderboards, crosshairs', ['Flask', 'SQLite', 'SEO'], '#ff4655', '#fb923c'))
    write('card-flight.svg', card('f', 'Flight Punctuality', 'flightpunctuality.online', 'Real delay stats for flights & routes',
                                  'EU261 calculator · 8,700+ routes', ['Python', 'DuckDB', 'systemd'], '#38bdf8', '#818cf8'))
