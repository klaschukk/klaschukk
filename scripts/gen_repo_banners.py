#!/usr/bin/env python3
"""Animated README banners for individual repositories (same look as the profile banner).

    python3 scripts/gen_repo_banners.py            # writes build/banners/<repo>.svg

Self-contained SVG (CSS + SMIL only), so it works inside GitHub's <img> sandbox.
"""
from pathlib import Path
from xml.sax.saxutils import escape as esc

OUT = Path(__file__).resolve().parent.parent / 'build' / 'banners'
OUT.mkdir(parents=True, exist_ok=True)
SANS = "system-ui,-apple-system,'Segoe UI',Roboto,Helvetica,Arial,sans-serif"
MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,'Liberation Mono',monospace"
W, H = 1200, 300


# ── motifs (drawn in the right-hand area, x 740..1160, y 30..270) ────────────
def m_levels(c1, c2):
    """Language levels A1..C2 as a staircase; a dot hops up it."""
    bars, hops = [], []
    for i, lab in enumerate(['A1', 'A2', 'B1', 'B2', 'C1', 'C2']):
        x, h = 790 + i * 62, 40 + i * 26
        bars.append(f'<rect class="grow" style="animation-delay:{i*.18:.2f}s" x="{x}" y="{250-h}" width="46" height="{h}" rx="9" '
                    f'fill="{c1}" fill-opacity="{.16+i*.07:.2f}" stroke="{c1}" stroke-opacity=".5"/>'
                    f'<text x="{x+23}" y="{244}" text-anchor="middle" font-family="{MONO}" font-size="13" fill="#e6edf3">{lab}</text>')
        hops.append(f'{x+23},{250-h-14}')
    path = ';'.join(hops)
    return ''.join(bars) + (f'<circle r="8" fill="{c2}"><animateMotion dur="6s" repeatCount="indefinite" '
                            f'path="M{hops[0]} L{" L".join(hops[1:])} L{hops[-1]} L{hops[0]}" calcMode="linear"/></circle>')


def m_timeline(c1, c2):
    """Day planner: coloured time blocks and a moving 'now' line."""
    cols = ['#a78bfa', '#60a5fa', '#34d399', '#fbbf24', '#f472b6']
    blocks = [(770, 60, 120, 0), (770, 122, 70, 1), (900, 60, 90, 2), (900, 160, 130, 3), (1040, 92, 84, 4), (1040, 190, 60, 0)]
    out = ''.join(f'<rect class="slide" style="animation-delay:{i*.22:.2f}s" x="{x}" y="{y}" width="{w}" height="46" rx="11" '
                  f'fill="{cols[k]}" fill-opacity=".22" stroke="{cols[k]}" stroke-opacity=".7"/>'
                  for i, (x, y, w, k) in enumerate(blocks))
    grid = ''.join(f'<line x1="{x}" y1="44" x2="{x}" y2="256" stroke="#fff" stroke-opacity=".07"/>' for x in range(770, 1170, 100))
    now = (f'<g><line x1="0" y1="40" x2="0" y2="262" stroke="#f87171" stroke-width="2"/><circle cy="40" r="5" fill="#f87171"/>'
           f'<animateTransform attributeName="transform" type="translate" values="780 0;1150 0;780 0" dur="9s" repeatCount="indefinite"/></g>')
    return grid + out + now


def m_shop(c1, c2):
    """Shop: floating product cards and a cart counter that ticks."""
    cards = ''
    for i, (x, col) in enumerate([(770, '#34d399'), (900, '#60a5fa'), (1030, '#f472b6')]):
        cards += (f'<g class="float" style="animation-delay:{i*.5:.1f}s"><rect x="{x}" y="70" width="112" height="150" rx="16" fill="#fff" fill-opacity=".05" stroke="#fff" stroke-opacity=".16"/>'
                  f'<ellipse cx="{x+56}" cy="126" rx="34" ry="18" fill="{col}" fill-opacity=".35" stroke="{col}"/>'
                  f'<rect x="{x+16}" y="168" width="60" height="8" rx="4" fill="#fff" fill-opacity=".35"/>'
                  f'<rect x="{x+16}" y="186" width="38" height="8" rx="4" fill="{col}"/></g>')
    cart = (f'<g transform="translate(1090 40)"><circle r="17" fill="{c1}"><animate attributeName="r" values="15;19;15" dur="2.4s" repeatCount="indefinite"/></circle>'
            f'<text y="5" text-anchor="middle" font-family="{MONO}" font-size="14" font-weight="700" fill="#06251a">+1</text></g>')
    return cards + cart


def m_menu(c1, c2):
    """Restaurant menu: category chips scrolling past and a plate."""
    labels = ['Breakfast', 'Pasta', 'Pizza', 'Soups', 'Salads', 'Desserts', 'Cocktails', 'Wine list']
    chips, x = '', 0
    for lab in labels * 2:
        w = 30 + 9.2 * len(lab)
        chips += (f'<rect x="{x}" y="0" width="{w:.0f}" height="34" rx="17" fill="{c1}" fill-opacity=".12" stroke="{c1}" stroke-opacity=".6"/>'
                  f'<text x="{x+w/2:.0f}" y="22" text-anchor="middle" font-family="{SANS}" font-size="14" fill="#f5e6b3">{lab}</text>')
        x += w + 12
    total = x / 2
    marquee = (f'<clipPath id="mq"><rect x="750" y="48" width="410" height="40"/></clipPath><g clip-path="url(#mq)"><g transform="translate(750 52)">'
               f'<g><animateTransform attributeName="transform" type="translate" values="0 0;-{total:.0f} 0" dur="16s" repeatCount="indefinite"/>{chips}</g></g></g>')
    plate = (f'<g transform="translate(955 178)"><circle r="70" fill="#fff" fill-opacity=".04" stroke="#fff" stroke-opacity=".18"/>'
             f'<circle r="48" fill="none" stroke="{c1}" stroke-opacity=".5" stroke-dasharray="4 8"><animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="24s" repeatCount="indefinite"/></circle>'
             f'<circle r="26" fill="{c1}" fill-opacity=".22" stroke="{c1}"/>'
             f'<path d="M-104 -46 v92 M-112 -46 v26 M-96 -46 v26 M-112 -20 q8 8 16 0" stroke="#fff" stroke-opacity=".5" stroke-width="3" fill="none" stroke-linecap="round"/>'
             f'<path d="M104 -46 q22 30 0 60 v32" stroke="#fff" stroke-opacity=".5" stroke-width="3" fill="none" stroke-linecap="round"/></g>')
    return marquee + plate


def m_route(c1, c2):
    """Transit: a route with stops and a bus dot, plus rolling departure rows."""
    pts = [(775, 220), (870, 168), (975, 196), (1070, 132), (1150, 96)]
    d = 'M' + ' L'.join(f'{x},{y}' for x, y in pts)
    stops = ''.join(f'<circle cx="{x}" cy="{y}" r="7" fill="#0b1020" stroke="{c1}" stroke-width="2.5"/>' for x, y in pts)
    rows = ''.join(f'<g class="slide" style="animation-delay:{i*.3:.1f}s"><rect x="{770+i*40}" y="{46+i*30}" width="{190-i*20}" height="22" rx="8" fill="#fff" fill-opacity=".06" stroke="#fff" stroke-opacity=".14"/>'
                   f'<circle cx="{786+i*40}" cy="{57+i*30}" r="4" fill="{c1}"/></g>' for i in range(3))
    return (f'<path d="{d}" fill="none" stroke="{c1}" stroke-opacity=".55" stroke-width="3" stroke-dasharray="7 9"/>' + stops + rows +
            f'<circle r="9" fill="{c2}"><animateMotion dur="7s" repeatCount="indefinite" path="{d}"/></circle>')


def m_crosshair(c1, c2):
    """Valorant: a pulsing crosshair and stat bars."""
    cx, cy = 880, 150
    ch = (f'<g><circle cx="{cx}" cy="{cy}" r="74" fill="none" stroke="{c1}" stroke-opacity=".3"><animate attributeName="r" values="66;82;66" dur="3s" repeatCount="indefinite"/></circle>'
          f'<circle cx="{cx}" cy="{cy}" r="46" fill="none" stroke="#fff" stroke-opacity=".18" stroke-dasharray="3 7"><animateTransform attributeName="transform" type="rotate" from="0 {cx} {cy}" to="360 {cx} {cy}" dur="20s" repeatCount="indefinite"/></circle>'
          + ''.join(f'<line x1="{cx+dx*14}" y1="{cy+dy*14}" x2="{cx+dx*38}" y2="{cy+dy*38}" stroke="#fff" stroke-width="4" stroke-linecap="round"/>' for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]) +
          f'<circle cx="{cx}" cy="{cy}" r="4" fill="{c1}"/></g>')
    bars = ''
    for i, (lab, v) in enumerate([('K/D', .72), ('HS%', .55), ('WIN', .64)]):
        y = 92 + i * 46
        bars += (f'<text x="990" y="{y+12}" font-family="{MONO}" font-size="14" fill="#c9d1d9">{lab}</text>'
                 f'<rect x="1040" y="{y}" width="110" height="14" rx="7" fill="#fff" fill-opacity=".08"/>'
                 f'<rect class="fill" style="animation-delay:{i*.3:.1f}s;--w:{110*v:.0f}px" x="1040" y="{y}" width="{110*v:.0f}" height="14" rx="7" fill="{c1}"/>')
    return ch + bars


def m_flight(c1, c2):
    """Flights: a plane on an arc plus an on-time / delayed / very-late histogram."""
    arc = 'M770,150 Q900,20 1030,110'
    plane = (f'<g><path d="M-12 0 L12 0 M0 -9 L8 0 L0 9 L-3 0 Z" fill="{c2}" stroke="{c2}" stroke-width="2" stroke-linejoin="round"/>'
             f'<animateMotion dur="6s" repeatCount="indefinite" path="{arc}" rotate="auto"/></g>')
    bars = ''
    for i, (h, col) in enumerate([(78, '#34d399'), (46, '#fbbf24'), (20, '#f87171')]):
        x = 1040 + i * 40
        bars += f'<rect class="grow" style="animation-delay:{i*.25:.2f}s" x="{x}" y="{250-h-60}" width="28" height="{h}" rx="8" fill="{col}" fill-opacity=".8"/>'
    base = '<line x1="1032" y1="190" x2="1160" y2="190" stroke="#fff" stroke-opacity=".2"/>'
    return (f'<path d="{arc}" fill="none" stroke="{c1}" stroke-opacity=".5" stroke-width="3" stroke-dasharray="7 9"/>'
            f'<circle cx="770" cy="150" r="6" fill="#0b1020" stroke="{c1}" stroke-width="2.5"/><circle cx="1030" cy="110" r="6" fill="#0b1020" stroke="{c1}" stroke-width="2.5"/>'
            + plane + bars + base +
            f'<text x="770" y="235" font-family="{MONO}" font-size="14" fill="#8b98a9">arrival delay, settled flights only</text>')


REPOS = {
    'gramo': dict(label='DESKTOP APP · WORKS OFFLINE', title='Gramo', tag='Learn English grammar the Cambridge way — from your own textbook',
                  chips=['Electron', 'React', 'TypeScript', 'SQLite'], c1='#2dd4bf', c2='#22d3ee', motif=m_levels),
    'koda': dict(label='DESKTOP APP · macOS', title='Koda', tag='Plan your day in visual time blocks',
                 chips=['Electron', 'React', 'TypeScript', 'Tailwind'], c1='#a78bfa', c2='#60a5fa', motif=m_timeline),
    'tapocki-project': dict(label='FULL-STACK DEMO SHOP', title='BalconySlippers', tag='Catalogue, cart, checkout and an admin panel',
                            chips=['Flask', 'Jinja2', 'Flask-Login'], c1='#34d399', c2='#a7f3d0', motif=m_shop),
    'restaurant-menu': dict(label='MOBILE-FIRST TEMPLATE', title='Restaurant Menu', tag='Menu, gallery and contacts in plain HTML, CSS and JS',
                            chips=['HTML', 'CSS', 'JavaScript'], c1='#d4a72c', c2='#f59e0b', motif=m_menu),
    'prevozni.com': dict(label='LIVE · SERBIA & MONTENEGRO', title='Prevozni', tag='Bus, train and city-transit timetables in four languages',
                         chips=['Flask', 'DuckDB', 'nginx', 'Cloudflare'], c1='#2dd4bf', c2='#38bdf8', motif=m_route),
    'valocheck.com': dict(label='LIVE · VALORANT STATS', title='ValoCheck', tag='Instant profiles, leaderboards and a crosshair generator',
                          chips=['Flask', 'SQLite'], c1='#ff4655', c2='#fb923c', motif=m_crosshair),
    'flightpunctuality.online': dict(label='LIVE · EU261', title='Flight Punctuality', tag='Real delay statistics from public flight records',
                                     chips=['Python', 'DuckDB', 'systemd'], c1='#38bdf8', c2='#818cf8', motif=m_flight),
}


def banner(key: str, s: dict) -> str:
    c1, c2 = s['c1'], s['c2']
    chips, x = '', 76
    for t in s['chips']:
        w = 28 + 9 * len(t)
        chips += (f'<rect x="{x}" y="222" width="{w:.0f}" height="32" rx="11" fill="{c1}" fill-opacity=".13" stroke="{c1}" stroke-opacity=".5"/>'
                  f'<text x="{x+w/2:.0f}" y="243" text-anchor="middle" font-family="{MONO}" font-size="14" fill="#e6edf3">{esc(t)}</text>')
        x += w + 10
    size = 64 if len(s['title']) <= 12 else 52
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="{esc(s['title'])} — {esc(s['tag'])}">
<defs>
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0b1020"/><stop offset=".6" stop-color="#0d1526"/><stop offset="1" stop-color="{c1}" stop-opacity=".22"/></linearGradient>
<linearGradient id="tt" x1="0" x2="1"><stop offset="0" stop-color="{c1}"><animate attributeName="stop-color" values="{c1};{c2};{c1}" dur="8s" repeatCount="indefinite"/></stop><stop offset="1" stop-color="{c2}"/></linearGradient>
<radialGradient id="gl" cx=".2" cy=".1" r=".7"><stop offset="0" stop-color="{c1}" stop-opacity=".28"/><stop offset="1" stop-color="{c1}" stop-opacity="0"/></radialGradient>
<pattern id="gr" width="40" height="40" patternUnits="userSpaceOnUse"><path d="M40 0H0V40" fill="none" stroke="#fff" stroke-opacity=".04"/></pattern>
<clipPath id="r"><rect width="{W}" height="{H}" rx="22"/></clipPath>
</defs>
<style>
.grow{{transform-box:fill-box;transform-origin:bottom;animation:gr 3.2s ease-in-out infinite alternate}}@keyframes gr{{from{{transform:scaleY(.55)}}to{{transform:scaleY(1)}}}}
.slide{{animation:sl 4s ease-in-out infinite alternate}}@keyframes sl{{from{{transform:translateX(-10px);opacity:.55}}to{{transform:none;opacity:1}}}}
.float{{animation:fl 3.6s ease-in-out infinite alternate}}@keyframes fl{{from{{transform:translateY(6px)}}to{{transform:translateY(-6px)}}}}
.fill{{animation:fi 3s ease-in-out infinite alternate}}@keyframes fi{{from{{width:14px}}to{{width:var(--w)}}}}
.in{{opacity:0;animation:up .9s ease-out forwards}}@keyframes up{{from{{opacity:0;transform:translateY(10px)}}to{{opacity:1;transform:none}}}}
@media (prefers-reduced-motion:reduce){{*{{animation:none!important}}}}
</style>
<g clip-path="url(#r)">
<rect width="{W}" height="{H}" fill="#0b1020"/><rect width="{W}" height="{H}" fill="url(#bg)"/><rect width="{W}" height="{H}" fill="url(#gr)"/><rect width="{W}" height="{H}" fill="url(#gl)"/>
<g class="in"><text x="76" y="86" font-family="{MONO}" font-size="14" letter-spacing="4" fill="#8b98a9">{esc(s['label'])}</text></g>
<text class="in" style="animation-delay:.15s" x="74" y="{150 if size==64 else 146}" font-family="{SANS}" font-size="{size}" font-weight="800" letter-spacing="-1" fill="url(#tt)">{esc(s['title'])}</text>
<text class="in" style="animation-delay:.3s" x="76" y="196" font-family="{SANS}" font-size="21" fill="#c9d1d9">{esc(s['tag'])}</text>
<g class="in" style="animation-delay:.45s">{chips}</g>
{s['motif'](c1, c2)}
</g>
<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="22" fill="none" stroke="#fff" stroke-opacity=".12"/>
</svg>'''


if __name__ == '__main__':
    for key, spec in REPOS.items():
        svg = banner(key, spec)
        (OUT / f'{key}.svg').write_text(svg, encoding='utf-8')
        print(f'{key}.svg {len(svg):,}')
