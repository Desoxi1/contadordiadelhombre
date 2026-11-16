"""Fondo collage de paneles (estilo portada de juego) con escenas originales en vector.
Uso: python gen_collage.py salida.svg ANCHO ALTO COLUMNAS FILAS SEMILLA
"""
import random
import sys

out_path = sys.argv[1]
W, H = int(sys.argv[2]), int(sys.argv[3])
COLS, ROWS = int(sys.argv[4]), int(sys.argv[5])
rnd = random.Random(int(sys.argv[6]))

GUTTER = 16
INK = '#120624'

o = []
a = o.append
defs = []
uid = [0]


def nid(p):
    uid[0] += 1
    return f'{p}{uid[0]}'


def lin(stops, x2=0, y2=1):
    i = nid('g')
    s = ''.join(f'<stop offset="{off}" stop-color="{c}"/>' for off, c in stops)
    defs.append(f'<linearGradient id="{i}" x1="0" y1="0" x2="{x2}" y2="{y2}">{s}</linearGradient>')
    return f'url(#{i})'


def rad(stops):
    i = nid('r')
    s = ''.join(f'<stop offset="{off}" stop-color="{c}" stop-opacity="{op}"/>' for off, c, op in stops)
    defs.append(f'<radialGradient id="{i}" cx="0.5" cy="0.5" r="0.5">{s}</radialGradient>')
    return f'url(#{i})'


def palm(x, base, h, color, flip=False, lean=0):
    """Palmera en silueta: tronco curvo + hojas."""
    top_x = x + lean
    top_y = base - h
    t = max(4, h * 0.035)
    p = [f'<path d="M{x - t:.1f} {base} Q{x + lean * 0.2 - t:.1f} {base - h * 0.5:.1f} {top_x - t * 0.6:.1f} {top_y:.1f} '
         f'L{top_x + t * 0.6:.1f} {top_y:.1f} Q{x + lean * 0.2 + t:.1f} {base - h * 0.5:.1f} {x + t:.1f} {base} Z" fill="{color}"/>']
    L = h * 0.42
    for ang, ln, droop in [(-170, 1, .55), (-140, .95, .35), (-110, .8, .2), (-70, .8, .2), (-40, .95, .35), (-10, 1, .55), (160, .6, .7), (20, .6, .7)]:
        import math
        r = math.radians(ang)
        ex = top_x + math.cos(r) * L * ln
        ey = top_y + math.sin(r) * L * ln + L * droop * 0.9
        cx = top_x + math.cos(r) * L * ln * 0.5
        cy = top_y + math.sin(r) * L * ln * 0.5 - L * 0.12
        w = L * 0.09
        p.append(f'<path d="M{top_x:.1f} {top_y:.1f} Q{cx:.1f} {cy - w:.1f} {ex:.1f} {ey:.1f} Q{cx:.1f} {cy + w:.1f} {top_x:.1f} {top_y + 3:.1f} Z" fill="{color}"/>')
    return ''.join(p)


# ---------- Escenas: cada una dibuja en la caja (x, y, w, h) ----------

def sc_sunset_sea(x, y, w, h):
    hz = y + h * 0.62
    s = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{lin([(0, "#2a0b5c"), (.45, "#c2276f"), (.8, "#ff8a3d"), (1, "#ffd27a")])}"/>']
    r = min(w, h) * 0.22
    s.append(f'<circle cx="{x + w * .5}" cy="{hz}" r="{r * 2.2}" fill="{rad([(0, "#ffd27a", .6), (1, "#ff3d9a", 0)])}"/>')
    s.append(f'<circle cx="{x + w * .5}" cy="{hz}" r="{r}" fill="{lin([(0, "#fff2a8"), (1, "#ff5f6d")])}"/>')
    s.append(f'<rect x="{x}" y="{hz}" width="{w}" height="{y + h - hz}" fill="{lin([(0, "#6a1f7a"), (1, "#1a0838")])}"/>')
    for i in range(9):
        yy = hz + 8 + i * (y + h - hz) / 10
        ww = w * (0.5 - i * 0.045)
        s.append(f'<rect x="{x + w / 2 - ww / 2:.0f}" y="{yy:.0f}" width="{ww:.0f}" height="3" fill="#ffb347" opacity="{.8 - i * .07:.2f}"/>')
    s.append(palm(x + w * .12, y + h + 10, h * .85, INK, lean=w * .08))
    return ''.join(s)


def sc_neon_city(x, y, w, h):
    s = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{lin([(0, "#0b1440"), (.6, "#3b1470"), (1, "#ff3d9a")])}"/>']
    for _ in range(int(w * h / 3000)):
        s.append(f'<circle cx="{x + rnd.random() * w:.0f}" cy="{y + rnd.random() * h * .4:.0f}" r="1.2" fill="#fff" opacity="{rnd.uniform(.3, .9):.2f}"/>')
    bx = x - 10
    while bx < x + w:
        bw = rnd.randint(28, 70)
        bh = rnd.uniform(.3, .85) * h
        top = y + h - bh
        s.append(f'<rect x="{bx}" y="{top:.0f}" width="{bw}" height="{bh:.0f}" fill="#160a2e"/>')
        c = rnd.choice(['#ff3d9a', '#2de2e6', '#ffd166'])
        s.append(f'<rect x="{bx}" y="{top:.0f}" width="{bw}" height="3" fill="{c}"/>')
        for wy in range(int(top) + 10, int(y + h) - 6, 12):
            for wx in range(bx + 5, bx + bw - 5, 10):
                if rnd.random() < .18:
                    s.append(f'<rect x="{wx}" y="{wy}" width="4" height="5" fill="{rnd.choice(["#ff7ab8", "#2de2e6", "#ffd166"])}" opacity=".85"/>')
        bx += bw + rnd.randint(2, 8)
    return ''.join(s)


def sc_palms(x, y, w, h):
    s = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{lin([(0, "#ff9a5a"), (.5, "#ff4f8b"), (1, "#7b2cbf")])}"/>']
    s.append(f'<circle cx="{x + w * .65}" cy="{y + h * .38}" r="{min(w, h) * .2}" fill="#ffe08a" opacity=".9"/>')
    s.append(palm(x + w * .25, y + h + 20, h * 1.0, INK, lean=w * .12))
    s.append(palm(x + w * .7, y + h + 20, h * .75, INK, lean=-w * .1))
    s.append(palm(x + w * .9, y + h + 20, h * .55, '#2a0b4a', lean=-w * .05))
    return ''.join(s)


def sc_road(x, y, w, h):
    hz = y + h * .45
    s = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{lin([(0, "#3a0f6b"), (.45, "#ff6a48"), (.46, "#2a0d3e"), (1, "#14062a")])}"/>']
    s.append(f'<circle cx="{x + w / 2}" cy="{hz}" r="{min(w, h) * .16}" fill="#ffd27a"/>')
    s.append(f'<rect x="{x}" y="{hz}" width="{w}" height="{y + h - hz}" fill="#1d0a33"/>')
    s.append(f'<path d="M{x + w * .47} {hz} L{x + w * .53} {hz} L{x + w * .95} {y + h} L{x + w * .05} {y + h} Z" fill="#2c1546"/>')
    for i in range(7):
        t1, t2 = (i / 7) ** 1.6, ((i + .5) / 7) ** 1.6
        y1, y2 = hz + (y + h - hz) * t1, hz + (y + h - hz) * t2
        ww1, ww2 = 2 + 10 * t1, 2 + 10 * t2
        cx = x + w / 2
        s.append(f'<path d="M{cx - ww1 / 2:.1f} {y1:.1f} L{cx + ww1 / 2:.1f} {y1:.1f} L{cx + ww2 / 2:.1f} {y2:.1f} L{cx - ww2 / 2:.1f} {y2:.1f} Z" fill="#ffd166"/>')
    for side in (-1, 1):
        for i, t in enumerate([.15, .35, .6, .95]):
            px = x + w / 2 + side * (w * .06 + w * .5 * t)
            base = hz + (y + h - hz) * t
            s.append(palm(px, base, h * (.18 + .55 * t), INK, lean=-side * w * .03))
    return ''.join(s)


def sc_ocean(x, y, w, h):
    s = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{lin([(0, "#2de2e6"), (.5, "#1388a8"), (1, "#0b2a5c")])}"/>']
    for i in range(14):
        yy = y + h * (i + 1) / 15
        amp = 6 + i * .6
        d = f'M{x} {yy:.0f}'
        step = 40
        xx = x
        while xx < x + w:
            d += f' q{step / 2} {-amp:.0f} {step} 0'
            xx += step
        s.append(f'<path d="{d}" stroke="#bff8ff" stroke-width="2" fill="none" opacity="{.25 + i * .03:.2f}"/>')
    # lancha genérica
    bx, by = x + w * .35, y + h * .55
    s.append(f'<path d="M{bx - w * .2:.0f} {by + 6} L{bx + w * .22:.0f} {by - 10} L{bx + w * .18:.0f} {by + 14} L{bx - w * .16:.0f} {by + 20} Z" fill="#ffffff"/>')
    s.append(f'<path d="M{bx - w * .2:.0f} {by + 6} L{bx + w * .22:.0f} {by - 10}" stroke="#ff3d9a" stroke-width="5"/>')
    s.append(f'<path d="M{bx - w * .26:.0f} {by + 22} q{-w * .1:.0f} -6 {-w * .2:.0f} 4 q{w * .08:.0f} 8 {w * .2:.0f} 2 Z" fill="#e8ffff" opacity=".8"/>')
    return ''.join(s)


def sc_night_hills(x, y, w, h):
    s = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{lin([(0, "#120630"), (.7, "#5a1a8a"), (1, "#ff3d9a")])}"/>']
    s.append(f'<circle cx="{x + w * .72}" cy="{y + h * .28}" r="{min(w, h) * .12}" fill="#fff4d6"/>')
    s.append(f'<circle cx="{x + w * .75}" cy="{y + h * .26}" r="{min(w, h) * .11}" fill="#2a0b5c" opacity=".35"/>')
    for _ in range(int(w * h / 2500)):
        s.append(f'<circle cx="{x + rnd.random() * w:.0f}" cy="{y + rnd.random() * h * .6:.0f}" r="1.1" fill="#fff" opacity="{rnd.uniform(.3, .9):.2f}"/>')
    s.append(f'<path d="M{x} {y + h * .75} Q{x + w * .3} {y + h * .55} {x + w * .55} {y + h * .72} T{x + w} {y + h * .65} L{x + w} {y + h} L{x} {y + h} Z" fill="#2a0b4a"/>')
    s.append(f'<path d="M{x} {y + h * .88} Q{x + w * .4} {y + h * .72} {x + w} {y + h * .85} L{x + w} {y + h} L{x} {y + h} Z" fill="{INK}"/>')
    return ''.join(s)


def sc_ferris(x, y, w, h):
    import math
    s = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{lin([(0, "#ff6a48"), (.55, "#ff3d9a"), (1, "#3b1470")])}"/>']
    cx, cy, r = x + w * .55, y + h * .45, min(w, h) * .32
    s.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" stroke="{INK}" stroke-width="6" fill="none"/>')
    for i in range(12):
        an = math.radians(i * 30)
        ex, ey = cx + math.cos(an) * r, cy + math.sin(an) * r
        s.append(f'<line x1="{cx}" y1="{cy}" x2="{ex:.0f}" y2="{ey:.0f}" stroke="{INK}" stroke-width="3"/>')
        s.append(f'<circle cx="{ex:.0f}" cy="{ey:.0f}" r="7" fill="{rnd.choice(["#ffd166", "#2de2e6", "#ffffff"])}"/>')
    s.append(f'<path d="M{cx} {cy} L{cx - r * .6:.0f} {y + h} M{cx} {cy} L{cx + r * .6:.0f} {y + h}" stroke="{INK}" stroke-width="7"/>')
    s.append(f'<rect x="{x}" y="{y + h * .88}" width="{w}" height="{h * .12}" fill="{INK}"/>')
    return ''.join(s)


def sc_neon_sign(x, y, w, h):
    s = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{lin([(0, "#1a0838"), (1, "#3b1470")])}"/>']
    for i in range(0, int(w), 26):
        s.append(f'<rect x="{x + i}" y="{y}" width="2" height="{h}" fill="#ffffff" opacity=".04"/>')
    cx, cy = x + w / 2, y + h / 2
    fs = min(w, h) * .32
    for sw, op in [(14, .25), (7, .5)]:
        s.append(f'<text x="{cx}" y="{cy + fs * .35:.0f}" text-anchor="middle" font-family="Arial Black, Arial" font-weight="900" font-size="{fs:.0f}" fill="none" stroke="#ff3d9a" stroke-width="{sw}" opacity="{op}">19·11</text>')
    s.append(f'<text x="{cx}" y="{cy + fs * .35:.0f}" text-anchor="middle" font-family="Arial Black, Arial" font-weight="900" font-size="{fs:.0f}" fill="none" stroke="#ffe0f0" stroke-width="2.5">19·11</text>')
    s.append(f'<rect x="{x + w * .15:.0f}" y="{cy + fs * .6:.0f}" width="{w * .7:.0f}" height="4" fill="#2de2e6"/>')
    return ''.join(s)


def sc_beach(x, y, w, h):
    hz = y + h * .4
    s = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{lin([(0, "#7fd6ff"), (.4, "#ffc0d9"), (1, "#ffc0d9")])}"/>']
    s.append(f'<rect x="{x}" y="{hz}" width="{w}" height="{h * .25}" fill="{lin([(0, "#2de2e6"), (1, "#1388a8")])}"/>')
    s.append(f'<path d="M{x} {hz + h * .2} Q{x + w * .5} {hz + h * .12} {x + w} {hz + h * .22} L{x + w} {y + h} L{x} {y + h} Z" fill="#ffd8a8"/>')
    ux, uy = x + w * .62, hz + h * .12
    s.append(f'<path d="M{ux - w * .18:.0f} {uy:.0f} Q{ux:.0f} {uy - h * .2:.0f} {ux + w * .18:.0f} {uy:.0f} Z" fill="#ff3d9a"/>')
    s.append(f'<path d="M{ux - w * .06:.0f} {uy:.0f} Q{ux:.0f} {uy - h * .2:.0f} {ux + w * .06:.0f} {uy:.0f} Z" fill="#ffffff"/>')
    s.append(f'<line x1="{ux:.0f}" y1="{uy:.0f}" x2="{ux + 6:.0f}" y2="{y + h * .92:.0f}" stroke="{INK}" stroke-width="4"/>')
    s.append(palm(x + w * .15, y + h + 10, h * .9, '#1d6b5c', lean=w * .1))
    return ''.join(s)


def sc_teal_sky(x, y, w, h):
    s = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{lin([(0, "#0e3a66"), (.5, "#1fa3b8"), (1, "#ff8a3d")])}"/>']
    for i in range(5):
        cy = y + h * (.2 + i * .12)
        s.append(f'<ellipse cx="{x + rnd.random() * w:.0f}" cy="{cy:.0f}" rx="{w * rnd.uniform(.2, .4):.0f}" ry="{h * .03:.0f}" fill="#ffd0e8" opacity=".45"/>')
    bx = x
    while bx < x + w:
        bw = rnd.randint(22, 50)
        bh = rnd.uniform(.15, .45) * h
        s.append(f'<rect x="{bx}" y="{y + h - bh:.0f}" width="{bw}" height="{bh:.0f}" fill="#0b1a33"/>')
        bx += bw + 3
    return ''.join(s)


# ---------- Escenas del Día del Hombre ----------

def neon(path_d, color, w=5):
    return (f'<path d="{path_d}" fill="none" stroke="{color}" stroke-width="{w * 3.2}" stroke-linecap="round" stroke-linejoin="round" opacity=".22"/>'
            f'<path d="{path_d}" fill="none" stroke="{color}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<path d="{path_d}" fill="none" stroke="#fff" stroke-width="{max(1.5, w * .35)}" stroke-linecap="round" stroke-linejoin="round" opacity=".8"/>')


def dark_wall(x, y, w, h, c1='#1a0838', c2='#3b1470'):
    s = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{lin([(0, c1), (1, c2)])}"/>'
    for i in range(0, int(w), 24):
        s += f'<rect x="{x + i}" y="{y}" width="2" height="{h}" fill="#fff" opacity=".035"/>'
    return s


def sc_asado(x, y, w, h):
    s = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{lin([(0, "#3a0f6b"), (.55, "#ff5a47"), (1, "#ffb347")])}"/>']
    cx, gy, gw = x + w * .5, y + h * .62, w * .62
    # humo
    for i in range(3):
        sx = cx - gw * .25 + i * gw * .25
        s.append(f'<path d="M{sx:.0f} {gy - 10:.0f} q-22 -40 0 -80 q22 -40 0 -80" stroke="#fff" stroke-width="10" fill="none" opacity=".25" stroke-linecap="round"/>')
    # brasas y parrilla
    s.append(f'<ellipse cx="{cx}" cy="{gy + 12:.0f}" rx="{gw * .48:.0f}" ry="16" fill="{rad([(0, "#ffd166", 1), (.6, "#ff5a1f", .9), (1, "#ff3d3d", 0)])}"/>')
    for i in range(6):
        sx = cx - gw * .4 + i * gw * .16
        s.append(f'<rect x="{sx:.0f}" y="{gy - 18:.0f}" width="{gw * .12:.0f}" height="15" rx="7" fill="{rnd.choice(["#8b2a1d", "#a5361f", "#6e1f18"])}" stroke="{INK}" stroke-width="2"/>')
    s.append(f'<rect x="{cx - gw / 2:.0f}" y="{gy - 2:.0f}" width="{gw:.0f}" height="8" fill="{INK}"/>')
    for i in range(9):
        s.append(f'<line x1="{cx - gw / 2 + i * gw / 8:.0f}" y1="{gy - 2:.0f}" x2="{cx - gw / 2 + i * gw / 8:.0f}" y2="{gy + 6:.0f}" stroke="#444" stroke-width="2"/>')
    s.append(f'<path d="M{cx - gw * .45:.0f} {gy + 6:.0f} L{cx - gw * .5:.0f} {y + h:.0f} M{cx + gw * .45:.0f} {gy + 6:.0f} L{cx + gw * .5:.0f} {y + h:.0f}" stroke="{INK}" stroke-width="8"/>')
    s.append(f'<rect x="{x}" y="{y + h * .9:.0f}" width="{w}" height="{h * .1:.0f}" fill="{INK}"/>')
    return ''.join(s)


def sc_futbol(x, y, w, h):
    import math
    s = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{lin([(0, "#0b1440"), (.55, "#2a0b5c"), (.56, "#1f8a4c"), (1, "#0e5a30")])}"/>']
    for lx in (x + w * .12, x + w * .88):
        s.append(f'<circle cx="{lx:.0f}" cy="{y + h * .12:.0f}" r="{w * .22:.0f}" fill="{rad([(0, "#fff8d6", .7), (1, "#fff8d6", 0)])}"/>')
        s.append(f'<rect x="{lx - 16:.0f}" y="{y + h * .08:.0f}" width="32" height="10" fill="#fff"/>')
    for i in range(6):
        s.append(f'<rect x="{x}" y="{y + h * (.56 + i * .08):.0f}" width="{w}" height="{h * .04:.0f}" fill="#fff" opacity=".05"/>')
    # arco con red
    gx, gy, gw, gh = x + w * .2, y + h * .32, w * .6, h * .26
    for i in range(11):
        s.append(f'<line x1="{gx + i * gw / 10:.0f}" y1="{gy:.0f}" x2="{gx + i * gw / 10:.0f}" y2="{gy + gh:.0f}" stroke="#fff" stroke-width="1.2" opacity=".35"/>')
    for i in range(6):
        s.append(f'<line x1="{gx:.0f}" y1="{gy + i * gh / 5:.0f}" x2="{gx + gw:.0f}" y2="{gy + i * gh / 5:.0f}" stroke="#fff" stroke-width="1.2" opacity=".35"/>')
    s.append(f'<path d="M{gx:.0f} {gy + gh:.0f} L{gx:.0f} {gy:.0f} L{gx + gw:.0f} {gy:.0f} L{gx + gw:.0f} {gy + gh:.0f}" stroke="#fff" stroke-width="7" fill="none"/>')
    # pelota
    bx, by, br = x + w * .55, y + h * .74, min(w, h) * .13
    s.append(f'<ellipse cx="{bx:.0f}" cy="{by + br * .95:.0f}" rx="{br:.0f}" ry="{br * .22:.0f}" fill="#000" opacity=".35"/>')
    s.append(f'<circle cx="{bx:.0f}" cy="{by:.0f}" r="{br:.0f}" fill="#fff" stroke="{INK}" stroke-width="3"/>')
    pts = ' '.join(f'{bx + math.cos(math.radians(-90 + i * 72)) * br * .38:.1f},{by + math.sin(math.radians(-90 + i * 72)) * br * .38:.1f}' for i in range(5))
    s.append(f'<polygon points="{pts}" fill="{INK}"/>')
    for i in range(5):
        an = math.radians(-90 + 36 + i * 72)
        px, py = bx + math.cos(an) * br * .86, by + math.sin(an) * br * .86
        s.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="{br * .2:.1f}" fill="{INK}"/>')
    s.append(f'<path d="M{bx - br * 1.2:.0f} {by - br * .2:.0f} l{-w * .18:.0f} 0 M{bx - br * 1.2:.0f} {by + br * .25:.0f} l{-w * .12:.0f} 0" stroke="#fff" stroke-width="4" opacity=".6" stroke-linecap="round"/>')
    return ''.join(s)


def car(cx, cy, s):
    body = (f'M{cx - s:.0f} {cy:.0f} L{cx - s * .96:.0f} {cy - s * .2:.0f} Q{cx - s * .6:.0f} {cy - s * .26:.0f} {cx - s * .36:.0f} {cy - s * .44:.0f} '
            f'L{cx + s * .18:.0f} {cy - s * .46:.0f} Q{cx + s * .48:.0f} {cy - s * .3:.0f} {cx + s * .96:.0f} {cy - s * .22:.0f} L{cx + s:.0f} {cy:.0f} Z')
    win = (f'M{cx - s * .3:.0f} {cy - s * .38:.0f} L{cx + s * .14:.0f} {cy - s * .4:.0f} Q{cx + s * .32:.0f} {cy - s * .3:.0f} {cx + s * .36:.0f} {cy - s * .26:.0f} '
           f'L{cx - s * .44:.0f} {cy - s * .26:.0f} Z')
    r = s * .18
    return (f'<path d="{body}" fill="{INK}" stroke="#ff3d9a" stroke-width="3"/>'
            f'<path d="{win}" fill="#2de2e6" opacity=".55"/>'
            f'<rect x="{cx + s * .86:.0f}" y="{cy - s * .18:.0f}" width="{s * .12:.0f}" height="{s * .05:.0f}" fill="#ffd166"/>'
            f'<rect x="{cx - s:.0f}" y="{cy - s * .16:.0f}" width="{s * .1:.0f}" height="{s * .05:.0f}" fill="#ff2f4d"/>'
            f'<circle cx="{cx - s * .6:.0f}" cy="{cy:.0f}" r="{r:.0f}" fill="#0b0418" stroke="#888" stroke-width="3"/>'
            f'<circle cx="{cx + s * .6:.0f}" cy="{cy:.0f}" r="{r:.0f}" fill="#0b0418" stroke="#888" stroke-width="3"/>')


def sc_auto(x, y, w, h):
    return sc_road(x, y, w, h) + car(x + w * .5, y + h * .86, min(w * .32, h * .5))


def sc_gym(x, y, w, h):
    s = [dark_wall(x, y, w, h)]
    cx, cy, L = x + w * .5, y + h * .5, w * .34
    s.append(neon(f'M{cx - L:.0f} {cy:.0f} L{cx + L:.0f} {cy:.0f}', '#2de2e6', 6))
    for side in (-1, 1):
        for k2, (off, ph) in enumerate([(.62, .5), (.78, .38)]):
            px = cx + side * L * off
            s.append(neon(f'M{px - 9:.0f} {cy - h * ph / 2:.0f} L{px + 9:.0f} {cy - h * ph / 2:.0f} L{px + 9:.0f} {cy + h * ph / 2:.0f} L{px - 9:.0f} {cy + h * ph / 2:.0f} Z', '#ff3d9a', 5))
    s.append(f'<text x="{cx:.0f}" y="{y + h * .88:.0f}" text-anchor="middle" font-family="Arial Black, Arial" font-weight="900" font-size="{min(w, h) * .12:.0f}" fill="#ffd166" opacity=".9">NO PAIN NO GAIN</text>')
    return ''.join(s)


def mug(mx, my, mw, mh, rot):
    return (f'<g transform="rotate({rot} {mx + mw / 2:.0f} {my + mh:.0f})">'
            f'<path d="M{mx + mw:.0f} {my + mh * .25:.0f} q{mw * .45:.0f} 0 {mw * .45:.0f} {mh * .3:.0f} q0 {mh * .3:.0f} {-mw * .45:.0f} {mh * .3:.0f}" stroke="{INK}" stroke-width="{mw * .14:.0f}" fill="none"/>'
            f'<rect x="{mx:.0f}" y="{my:.0f}" width="{mw:.0f}" height="{mh:.0f}" rx="8" fill="{lin([(0, "#ffd166"), (1, "#ff8a1f")])}" stroke="{INK}" stroke-width="5"/>'
            f'<rect x="{mx + mw * .15:.0f}" y="{my + mh * .2:.0f}" width="{mw * .12:.0f}" height="{mh * .65:.0f}" rx="4" fill="#fff" opacity=".45"/>'
            f'<path d="M{mx - 6:.0f} {my + 6:.0f} q{mw * .25:.0f} {-mh * .28:.0f} {mw * .5:.0f} {-mh * .12:.0f} q{mw * .3:.0f} {-mh * .18:.0f} {mw * .5 + 12:.0f} {mh * .1:.0f} L{mx + mw + 6:.0f} {my + 10:.0f} L{mx - 6:.0f} {my + 10:.0f} Z" fill="#fffaf0" stroke="{INK}" stroke-width="4"/>'
            '</g>')


def sc_schop(x, y, w, h):
    s = [dark_wall(x, y, w, h, '#3b1470', '#c2276f')]
    mw, mh = w * .22, h * .42
    base = y + h * .78
    s.append(mug(x + w * .26, base - mh, mw, mh, -14))
    s.append(mug(x + w * .52, base - mh, mw, mh, 14))
    for _ in range(10):
        s.append(f'<circle cx="{x + w * rnd.uniform(.3, .7):.0f}" cy="{y + h * rnd.uniform(.12, .3):.0f}" r="{rnd.uniform(3, 7):.0f}" fill="#fff" opacity=".6"/>')
    s.append(f'<text x="{x + w * .5:.0f}" y="{y + h * .95:.0f}" text-anchor="middle" font-family="Arial Black, Arial" font-weight="900" font-size="{min(w, h) * .14:.0f}" fill="#fff" stroke="{INK}" stroke-width="5" paint-order="stroke">¡SALUD!</text>')
    return ''.join(s)


def sc_pesca(x, y, w, h):
    hz = y + h * .55
    s = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{lin([(0, "#2a0b5c"), (.5, "#ff6a48"), (1, "#ffc15e")])}"/>']
    s.append(f'<circle cx="{x + w * .7:.0f}" cy="{hz:.0f}" r="{min(w, h) * .18:.0f}" fill="#ffe08a"/>')
    s.append(f'<path d="M{x} {hz - h * .08:.0f} L{x + w * .25:.0f} {hz - h * .2:.0f} L{x + w * .45:.0f} {hz:.0f} Z" fill="#4a1a5e"/>')
    s.append(f'<rect x="{x}" y="{hz:.0f}" width="{w}" height="{y + h - hz:.0f}" fill="{lin([(0, "#7a2a7e"), (1, "#1a0838")])}"/>')
    bx, by = x + w * .38, hz + h * .14
    s.append(f'<path d="M{bx - w * .18:.0f} {by:.0f} L{bx + w * .18:.0f} {by:.0f} L{bx + w * .12:.0f} {by + h * .07:.0f} L{bx - w * .13:.0f} {by + h * .07:.0f} Z" fill="{INK}"/>')
    s.append(f'<rect x="{bx - 7:.0f}" y="{by - h * .16:.0f}" width="16" height="{h * .16:.0f}" rx="5" fill="{INK}"/>')
    s.append(f'<circle cx="{bx + 1:.0f}" cy="{by - h * .19:.0f}" r="10" fill="{INK}"/>')
    s.append(f'<path d="M{bx - 14:.0f} {by - h * .21:.0f} L{bx + 16:.0f} {by - h * .21:.0f}" stroke="{INK}" stroke-width="6"/>')
    s.append(f'<path d="M{bx + 6:.0f} {by - h * .1:.0f} L{bx + w * .32:.0f} {by - h * .36:.0f}" stroke="{INK}" stroke-width="4"/>')
    s.append(f'<path d="M{bx + w * .32:.0f} {by - h * .36:.0f} Q{bx + w * .4:.0f} {by - h * .1:.0f} {bx + w * .38:.0f} {by + h * .12:.0f}" stroke="#fff" stroke-width="1.5" fill="none" opacity=".7"/>')
    for i in range(6):
        yy = hz + h * .06 + i * (y + h - hz) / 7
        s.append(f'<rect x="{x + w * .6:.0f}" y="{yy:.0f}" width="{w * (.3 - i * .03):.0f}" height="3" fill="#ffd27a" opacity="{.7 - i * .09:.2f}"/>')
    return ''.join(s)


def sc_guitarra(x, y, w, h):
    s = [dark_wall(x, y, w, h, '#120630', '#4a1478')]
    cx, cy, r = x + w * .42, y + h * .64, min(w, h) * .17
    body = (f'M{cx:.0f} {cy - r * 1.9:.0f} C{cx + r * 1.1:.0f} {cy - r * 1.9:.0f} {cx + r * .9:.0f} {cy - r * .8:.0f} {cx + r * .6:.0f} {cy - r * .55:.0f} '
            f'C{cx + r * 1.5:.0f} {cy - r * .3:.0f} {cx + r * 1.4:.0f} {cy + r * 1.1:.0f} {cx:.0f} {cy + r * 1.1:.0f} '
            f'C{cx - r * 1.4:.0f} {cy + r * 1.1:.0f} {cx - r * 1.5:.0f} {cy - r * .3:.0f} {cx - r * .6:.0f} {cy - r * .55:.0f} '
            f'C{cx - r * .9:.0f} {cy - r * .8:.0f} {cx - r * 1.1:.0f} {cy - r * 1.9:.0f} {cx:.0f} {cy - r * 1.9:.0f} Z')
    s.append(f'<g transform="rotate(28 {cx:.0f} {cy:.0f})">')
    s.append(neon(body, '#ff3d9a', 5))
    s.append(neon(f'M{cx:.0f} {cy - r * 1.9:.0f} L{cx:.0f} {cy - r * 4.4:.0f}', '#2de2e6', 7))
    s.append(neon(f'M{cx - 10:.0f} {cy - r * 4.4:.0f} L{cx + 10:.0f} {cy - r * 4.4:.0f} L{cx + 8:.0f} {cy - r * 5:.0f} L{cx - 8:.0f} {cy - r * 5:.0f} Z', '#2de2e6', 4))
    s.append(f'<circle cx="{cx:.0f}" cy="{cy - r * .2:.0f}" r="{r * .38:.0f}" fill="none" stroke="#ffd166" stroke-width="4"/>')
    s.append('</g>')
    return ''.join(s)


def sc_bigote(x, y, w, h):
    s = [dark_wall(x, y, w, h, '#2a0b5c', '#ff3d9a')]
    cx, cy, u = x + w * .5, y + h * .42, min(w, h) * .22
    m = (f'M{cx:.0f} {cy:.0f} C{cx - u * .3:.0f} {cy - u * .45:.0f} {cx - u * 1.1:.0f} {cy - u * .4:.0f} {cx - u * 1.3:.0f} {cy + u * .05:.0f} '
         f'C{cx - u * 1.6:.0f} {cy + u * .5:.0f} {cx - u * 2:.0f} {cy - u * .1:.0f} {cx - u * 1.7:.0f} {cy - u * .35:.0f} '
         f'C{cx - u * 1.9:.0f} {cy + u * .25:.0f} {cx - u * 1.4:.0f} {cy + u * .55:.0f} {cx - u * .9:.0f} {cy + u * .35:.0f} '
         f'C{cx - u * .5:.0f} {cy + u * .25:.0f} {cx - u * .2:.0f} {cy + u * .2:.0f} {cx:.0f} {cy + u * .05:.0f} '
         f'C{cx + u * .2:.0f} {cy + u * .2:.0f} {cx + u * .5:.0f} {cy + u * .25:.0f} {cx + u * .9:.0f} {cy + u * .35:.0f} '
         f'C{cx + u * 1.4:.0f} {cy + u * .55:.0f} {cx + u * 1.9:.0f} {cy + u * .25:.0f} {cx + u * 1.7:.0f} {cy - u * .35:.0f} '
         f'C{cx + u * 2:.0f} {cy - u * .1:.0f} {cx + u * 1.6:.0f} {cy + u * .5:.0f} {cx + u * 1.3:.0f} {cy + u * .05:.0f} '
         f'C{cx + u * 1.1:.0f} {cy - u * .4:.0f} {cx + u * .3:.0f} {cy - u * .45:.0f} {cx:.0f} {cy:.0f} Z')
    s.append(f'<path d="{m}" fill="{INK}" stroke="#fff" stroke-width="3"/>')
    by = y + h * .74
    s.append(f'<path d="M{cx:.0f} {by:.0f} L{cx - u * 1.1:.0f} {by - u * .5:.0f} L{cx - u * 1.1:.0f} {by + u * .5:.0f} Z M{cx:.0f} {by:.0f} L{cx + u * 1.1:.0f} {by - u * .5:.0f} L{cx + u * 1.1:.0f} {by + u * .5:.0f} Z" fill="#2de2e6" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>')
    s.append(f'<rect x="{cx - u * .22:.0f}" y="{by - u * .26:.0f}" width="{u * .44:.0f}" height="{u * .52:.0f}" rx="6" fill="#ffd166" stroke="{INK}" stroke-width="5"/>')
    return ''.join(s)


def sc_trofeo(x, y, w, h):
    s = [dark_wall(x, y, w, h, '#0b1440', '#3b1470')]
    s.append(f'<circle cx="{x + w * .5:.0f}" cy="{y + h * .45:.0f}" r="{min(w, h) * .42:.0f}" fill="{rad([(0, "#ffd166", .45), (1, "#ffd166", 0)])}"/>')
    cx, top, u = x + w * .5, y + h * .2, min(w, h) * .2
    gold = lin([(0, "#fff2a8"), (.5, "#ffc23d"), (1, "#c97a12")], 1, 0)
    s.append(f'<path d="M{cx - u:.0f} {top:.0f} L{cx + u:.0f} {top:.0f} Q{cx + u:.0f} {top + u * 1.6:.0f} {cx:.0f} {top + u * 1.7:.0f} Q{cx - u:.0f} {top + u * 1.6:.0f} {cx - u:.0f} {top:.0f} Z" fill="{gold}" stroke="{INK}" stroke-width="5"/>')
    s.append(f'<path d="M{cx - u:.0f} {top + u * .2:.0f} q{-u * .7:.0f} 0 {-u * .5:.0f} {u * .6:.0f} q{u * .15:.0f} {u * .35:.0f} {u * .6:.0f} {u * .4:.0f} M{cx + u:.0f} {top + u * .2:.0f} q{u * .7:.0f} 0 {u * .5:.0f} {u * .6:.0f} q{-u * .15:.0f} {u * .35:.0f} {-u * .6:.0f} {u * .4:.0f}" stroke="{INK}" stroke-width="7" fill="none"/>')
    s.append(f'<rect x="{cx - u * .15:.0f}" y="{top + u * 1.65:.0f}" width="{u * .3:.0f}" height="{u * .5:.0f}" fill="{gold}" stroke="{INK}" stroke-width="4"/>')
    s.append(f'<rect x="{cx - u * .7:.0f}" y="{top + u * 2.1:.0f}" width="{u * 1.4:.0f}" height="{u * .4:.0f}" rx="4" fill="{INK}"/>')
    s.append(f'<text x="{cx:.0f}" y="{top + u * .95:.0f}" text-anchor="middle" font-family="Arial Black, Arial" font-weight="900" font-size="{u * .7:.0f}" fill="{INK}">N°1</text>')
    return ''.join(s)


SCENES = [sc_asado, sc_futbol, sc_auto, sc_gym, sc_schop, sc_pesca,
          sc_guitarra, sc_bigote, sc_trofeo, sc_neon_sign, sc_palms, sc_sunset_sea]

# ---------- Rejilla con divisiones inclinadas ----------
xs = [[0] * (ROWS + 1) for _ in range(COLS + 1)]  # x de cada línea vertical en cada fila-límite
ys = [[0] * (COLS + 1) for _ in range(ROWS + 1)]
for c in range(COLS + 1):
    base = W * c / COLS
    for r in range(ROWS + 1):
        jitter = 0 if c in (0, COLS) else rnd.uniform(-W * .035, W * .035)
        xs[c][r] = base + jitter
for r in range(ROWS + 1):
    base = H * r / ROWS
    for c in range(COLS + 1):
        jitter = 0 if r in (0, ROWS) else rnd.uniform(-H * .04, H * .04)
        ys[r][c] = base + jitter


def corner(c, r):
    # intersección aproximada: x de la línea vertical c en la fila r, y de la línea horizontal r en la columna c
    return xs[c][r], ys[r][c]


a(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" preserveAspectRatio="xMidYMid slice">')
body = [f'<rect width="{W}" height="{H}" fill="{INK}"/>']
order = SCENES[:]
k = 0
for r in range(ROWS):
    for c in range(COLS):
        pts = [corner(c, r), corner(c + 1, r), corner(c + 1, r + 1), corner(c, r + 1)]
        poly = ' '.join(f'{px:.1f},{py:.1f}' for px, py in pts)
        cid = nid('c')
        defs.append(f'<clipPath id="{cid}"><polygon points="{poly}"/></clipPath>')
        minx = min(p[0] for p in pts); maxx = max(p[0] for p in pts)
        miny = min(p[1] for p in pts); maxy = max(p[1] for p in pts)
        if k % len(order) == 0:
            rnd.shuffle(order)
        scene = order[k % len(order)]
        k += 1
        body.append(f'<g clip-path="url(#{cid})">{scene(minx, miny, maxx - minx, maxy - miny)}</g>')
        body.append(f'<polygon points="{poly}" fill="none" stroke="{INK}" stroke-width="{GUTTER}" stroke-linejoin="round"/>')
        body.append(f'<polygon points="{poly}" fill="none" stroke="#ffffff" stroke-width="2" opacity=".25"/>')

a('<defs>' + ''.join(defs) + '</defs>')
o.extend(body)
a('</svg>')
open(out_path, 'w', encoding='utf-8').write('\n'.join(o))
print('ok', out_path, len(''.join(o)) // 1024, 'KB')
