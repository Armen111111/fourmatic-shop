"""Общие элементы бренда ZAPKIT: цвета, кит, буквы, иконки деталей, коробка.

Все фигуры нарисованы вручную геометрией — без шрифтов и чужих картинок.
Используется в brand/tools/build_brand.py и avito/tools/build_avito.py.
"""

import math
from xml.sax.saxutils import escape

# --- Цвета ----------------------------------------------------------------
YELLOW = "#FFC72C"       # жёлтый «скотч» — главный акцент
INK = "#14161A"          # графит
PAPER = "#FAF7F0"        # тёплый белый
WHITE = "#FFFFFF"
STEEL = "#8C929B"        # второстепенный текст
STEEL_LIGHT = "#C9CDD3"
STEEL_DARK = "#5E646C"
KRAFT = "#C8925A"        # картон
KRAFT_DARK = "#A87444"
KRAFT_MID = "#B98150"
KRAFT_LIGHT = "#D6A26C"
COPPER = "#C77B3F"

FONT = "'Liberation Sans', Arial, Helvetica, sans-serif"
TAGLINE = "РЕМОНТ В ОДНОЙ КОРОБКЕ"


# --- Служебное ------------------------------------------------------------
def svg(w, h, body, title, viewbox=None):
    vb = viewbox or f"0 0 {w} {h}"
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" width="{w}" height="{h}" '
            f'role="img" aria-label="{escape(title)}"><title>{escape(title)}</title>{body}</svg>\n')


def text(x, y, s, size, color, weight=700, anchor="start", spacing=None, length=None, opacity=None):
    extra = f' letter-spacing="{spacing}"' if spacing else ""
    if length:
        extra += f' textLength="{length}" lengthAdjust="spacing"'
    if opacity is not None:
        extra += f' opacity="{opacity}"'
    return (f'<text x="{x}" y="{y}" font-family="{FONT}" font-size="{size}" font-weight="{weight}" '
            f'fill="{color}" text-anchor="{anchor}"{extra}>{escape(s)}</text>')


def text_width(s, size, weight=700):
    """Грубая оценка ширины строки для Liberation Sans / Arial."""
    k = 0.6 if weight >= 700 else 0.54
    return len(s) * size * k


def fit_size(s, max_w, max_size, weight=700):
    return min(max_size, int(max_w / (len(s) * (0.6 if weight >= 700 else 0.54))))


def wrap(s, size, max_w, weight=700):
    words, lines, cur = s.split(), [], ""
    for w in words:
        cand = f"{cur} {w}".strip()
        if cur and text_width(cand, size, weight) > max_w:
            lines.append(cur)
            cur = w
        else:
            cur = cand
    if cur:
        lines.append(cur)
    return lines


def hexagon(cx, cy, r, rot=0):
    pts = [(cx + r * math.cos(math.radians(rot + 60 * i)),
            cy + r * math.sin(math.radians(rot + 60 * i))) for i in range(6)]
    return "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts) + " Z"


def circle_path(cx, cy, r):
    return f"M{cx - r},{cy} a{r},{r} 0 1 0 {2 * r},0 a{r},{r} 0 1 0 {-2 * r},0 Z"


def check_icon(x, y, color, mark, size=30):
    s = size / 30
    return (f'<g transform="translate({x} {y}) scale({s})"><rect width="30" height="30" rx="8" fill="{color}"/>'
            f'<path d="M8,15.5 L13,20.5 L22,10" fill="none" stroke="{mark}" stroke-width="3.6" '
            f'stroke-linecap="round" stroke-linejoin="round"/></g>')


# --- Кит (сетка 100×100) -------------------------------------------------
WHALE_BODY = ("M8,60 C8,43 23,34 42,34 C57,34 67,41 71,51 C76,47 79,41 81.5,31 "
              "L86.5,31 C88,48 81,60 70,64 C66,76 54,84 38,84 C20,84 8,75 8,60 Z")
WHALE_FLUKE = ("M84,36 C80,28 73,25 66,26 C70,19 79,19 84,27 "
               "C89,19 98,19 102,26 C95,25 88,28 84,36 Z")
WHALE_SPOUT = "M28,28 V18 M28,22 C24,18 20,18 17,20 M28,22 C32,18 36,18 39,20"


def whale(fg, bg, uid, spout=True):
    """Кит, перевязанный лентой, как посылка. bg — цвет ленты (обычно цвет фона)."""
    s = (f'<defs><clipPath id="wb-{uid}"><path d="{WHALE_BODY}"/></clipPath></defs>'
         f'<path fill="{fg}" d="{WHALE_BODY}"/><path fill="{fg}" d="{WHALE_FLUKE}"/>'
         f'<g clip-path="url(#wb-{uid})" fill="{bg}">'
         f'<rect x="40" y="30" width="8" height="60"/><rect x="0" y="64" width="90" height="7"/></g>'
         f'<circle cx="22" cy="55" r="3.6" fill="{bg}"/>')
    if spout:
        s += f'<path d="{WHALE_SPOUT}" fill="none" stroke="{fg}" stroke-width="4.4" stroke-linecap="round"/>'
    return s


# --- Буквы: осевые линии, штрих 18, высота 100 ---------------------------
LETTERS = {
    # латиница
    "Z": "M0,9 H57 L9,91 H66",
    "A": "M9,100 V36 L28,9 H38 L57,36 V100 M9,62 H57",
    "P": "M9,100 V9 H44 A13,13 0 0 1 57,22 V45 A13,13 0 0 1 44,58 H9",
    "K": "M9,0 V100 M9,64 L62,-6 M30,44 L66,106",
    "I": "M9,0 V100",
    "T": "M0,9 H66 M33,9 V100",
    # кириллица
    "З": "M0,9 H44 A13,13 0 0 1 57,22 V37 A13,13 0 0 1 44,50 H16 "
         "M16,50 H44 A13,13 0 0 1 57,63 V78 A13,13 0 0 1 44,91 H0",
    "А": "M9,100 V36 L28,9 H38 L57,36 V100 M9,62 H57",
    "П": "M9,100 V9 H44 A13,13 0 0 1 57,22 V100",
    "К": "M9,0 V100 M9,64 L62,-6 M30,44 L66,106",
    "И": "M9,0 V100 M57,0 V100 M9,100 L57,0",
    "Т": "M0,9 H66 M33,9 V100",
}
WIDTH = {"I": 18}
GAP = 14


def word_width(word):
    return sum(WIDTH.get(c, 66) for c in word) + GAP * (len(word) - 1)


def wordmark(word, colors, uid):
    """colors — один цвет или список цветов по буквам."""
    if isinstance(colors, str):
        colors = [colors] * len(word)
    parts = [f'<defs><clipPath id="c66-{uid}"><rect width="66" height="100"/></clipPath>'
             f'<clipPath id="c18-{uid}"><rect width="18" height="100"/></clipPath></defs>']
    x = 0
    for ch, color in zip(word, colors):
        w = WIDTH.get(ch, 66)
        parts.append(f'<g transform="translate({x} 0)"><path clip-path="url(#c{w}-{uid})" d="{LETTERS[ch]}" '
                     f'fill="none" stroke="{color}" stroke-width="18" stroke-linejoin="miter" '
                     f'stroke-miterlimit="10"/></g>')
        x += w + GAP
    return "".join(parts)


BRAND = "ZAPKIT"
BRAND_CYR = "ЗАПКИТ"
LOCK_WORD_X = 176


def lockup_width(word=BRAND):
    return LOCK_WORD_X + word_width(word)


def lockup(fg, bg, uid, word=BRAND, word_colors=None):
    """Кит (масштаб 1.5) + надпись. Габарит: x 12..lockup_width, y −3..100."""
    return (f'<g transform="translate(0 -30) scale(1.5)">{whale(fg, bg, uid)}</g>'
            f'<g transform="translate({LOCK_WORD_X} 0)">{wordmark(word, word_colors or fg, uid)}</g>')


def two_tone(fg, accent):
    """ZAP одним цветом, KIT — акцентом (для тёмного фона)."""
    return [fg, fg, fg, accent, accent, accent]


# --- Иконки деталей (коробка 120×120) ------------------------------------
def _zigzag(x0, x1, y0, y1, step):
    pts, up, x = [], True, x0
    while x <= x1:
        pts.append(f"{x},{y0 if up else y1}")
        up = not up
        x += step
    return " ".join(pts)


def icon(name):
    """Плоская иконка детали в квадрате 120×120."""
    I, Y, S, SL, SD = INK, YELLOW, STEEL, STEEL_LIGHT, STEEL_DARK
    if name == "oil":
        return (f'<rect x="28" y="38" width="64" height="72" rx="8" fill="{I}"/>'
                f'<rect x="34" y="24" width="18" height="16" fill="{I}"/>'
                f'<rect x="31" y="15" width="24" height="11" rx="3" fill="{Y}"/>'
                f'<path d="M62,40 V28 Q62,24 66,24 H82 Q86,24 86,28 V40" fill="none" stroke="{I}" stroke-width="7"/>'
                f'<rect x="38" y="58" width="44" height="38" rx="4" fill="{Y}"/>'
                f'<path d="M60,64 C60,64 50,76 50,82 A10,10 0 0 0 70,82 C70,76 60,64 60,64 Z" fill="{I}"/>')
    if name == "oil_filter":
        return (f'<rect x="32" y="30" width="56" height="76" rx="9" fill="{I}"/>'
                f'<rect x="29" y="20" width="62" height="14" rx="4" fill="{S}"/>'
                f'<rect x="32" y="54" width="56" height="16" fill="{Y}"/>'
                f'<rect x="32" y="76" width="56" height="4" fill="{SD}"/>')
    if name == "air_filter":
        return (f'<rect x="12" y="32" width="96" height="58" rx="6" fill="{I}"/>'
                f'<rect x="20" y="40" width="80" height="42" fill="{Y}"/>'
                f'<polyline points="{_zigzag(20, 100, 40, 82, 6.67)}" fill="none" stroke="{I}" stroke-width="2"/>')
    if name == "cabin_filter":
        return (f'<rect x="18" y="36" width="84" height="50" rx="5" fill="{S}"/>'
                f'<rect x="24" y="42" width="72" height="38" fill="{PAPER}"/>'
                f'<polyline points="{_zigzag(24, 96, 42, 80, 6)}" fill="none" stroke="{S}" stroke-width="2"/>')
    if name == "washer":
        return (f'<path fill="{COPPER}" fill-rule="evenodd" d="{circle_path(60, 60, 30)} {circle_path(60, 60, 13)}"/>'
                f'<circle cx="60" cy="60" r="22" fill="none" stroke="#A9612B" stroke-width="2"/>')
    if name == "card":
        qr = "".join(f'<rect x="{62 + (i % 3) * 7}" y="{70 + (i // 3) * 7}" width="5" height="5" fill="{I}"/>'
                     for i in range(9) if i not in (4,))
        return (f'<rect x="30" y="18" width="60" height="84" rx="6" fill="{PAPER}" stroke="{I}" stroke-width="3"/>'
                f'<rect x="30" y="18" width="60" height="14" rx="6" fill="{Y}"/>'
                f'<rect x="30" y="26" width="60" height="6" fill="{Y}"/>'
                + "".join(f'<rect x="38" y="{40 + i * 9}" width="5" height="5" fill="none" stroke="{I}" stroke-width="1.6"/>'
                          f'<rect x="47" y="{41 + i * 9}" width="34" height="3" fill="{SD}"/>' for i in range(3))
                + qr)
    if name == "disc":
        holes = "".join(f'<circle cx="{60 + 14 * math.cos(math.radians(a)):.1f}" cy="{60 + 14 * math.sin(math.radians(a)):.1f}" r="3" fill="{I}"/>'
                        for a in range(-90, 270, 72))
        return (f'<circle cx="60" cy="60" r="46" fill="{SL}"/>'
                f'<circle cx="60" cy="60" r="38" fill="none" stroke="{S}" stroke-width="2"/>'
                f'<circle cx="60" cy="60" r="23" fill="{S}"/>'
                f'<circle cx="60" cy="60" r="7" fill="{I}"/>' + holes)
    if name == "pads":
        pad = ('<path d="M16,{y} Q60,{a} 104,{y} V{b} Q60,{c} 16,{b} Z" fill="{f}"/>'
               '<path d="M22,{y2} Q60,{a2} 98,{y2} V{b} Q60,{c} 22,{b} Z" fill="{g}"/>')
        return (pad.format(y=34, a=16, b=58, c=42, y2=44, a2=28, f=S, g=I)
                + pad.format(y=70, a=52, b=94, c=78, y2=80, a2=64, f=S, g=I))
    if name == "grease":
        return (f'<path d="M26,44 H84 L100,52 V68 L84,76 H26 Z" fill="{Y}"/>'
                f'<rect x="16" y="42" width="12" height="36" rx="2" fill="{I}"/>'
                f'<rect x="100" y="54" width="10" height="12" rx="2" fill="{I}"/>'
                f'<rect x="42" y="52" width="32" height="16" rx="3" fill="{I}"/>')
    if name == "spray":
        return (f'<rect x="40" y="36" width="40" height="72" rx="7" fill="{I}"/>'
                f'<rect x="46" y="24" width="28" height="14" rx="3" fill="{S}"/>'
                f'<rect x="54" y="16" width="14" height="10" rx="2" fill="{I}"/>'
                f'<rect x="40" y="58" width="40" height="22" fill="{Y}"/>'
                f'<path d="M74,20 L94,12 M74,21 L96,21 M74,22 L94,30" stroke="{S}" stroke-width="3" stroke-linecap="round"/>')
    if name == "link":
        return (f'<rect x="28" y="54" width="64" height="12" rx="6" fill="{I}"/>'
                f'<rect x="20" y="26" width="8" height="24" fill="{S}"/>'
                f'<rect x="92" y="70" width="8" height="24" fill="{S}"/>'
                f'<circle cx="24" cy="60" r="13" fill="{I}"/><circle cx="96" cy="60" r="13" fill="{I}"/>'
                f'<circle cx="24" cy="60" r="6" fill="{S}"/><circle cx="96" cy="60" r="6" fill="{S}"/>')
    if name == "bushing":
        return (f'<path fill="{I}" fill-rule="evenodd" d="M24,40 H96 V64 C96,88 80,100 60,100 '
                f'C40,100 24,88 24,64 Z {circle_path(60, 66, 15)}"/>'
                f'<rect x="24" y="40" width="72" height="8" fill="{SD}"/>')
    if name == "nut":
        return (f'<path fill="{S}" fill-rule="evenodd" d="{hexagon(60, 60, 34)} {circle_path(60, 60, 14)}"/>'
                f'<circle cx="60" cy="60" r="19" fill="none" stroke="{SD}" stroke-width="2"/>')
    if name == "spark_plug":
        threads = "".join(f'<rect x="50" y="{80 + i * 5}" width="20" height="2" fill="{SD}"/>' for i in range(4))
        return (f'<rect x="55" y="8" width="10" height="12" rx="2" fill="{S}"/>'
                f'<path d="M50,20 H70 L68,56 H52 Z" fill="{PAPER}" stroke="{I}" stroke-width="3"/>'
                f'<rect x="44" y="56" width="32" height="20" rx="2" fill="{I}"/>'
                f'<rect x="50" y="76" width="20" height="24" fill="{S}"/>' + threads
                + f'<path d="M58,100 V110 H66" fill="none" stroke="{I}" stroke-width="3"/>')
    if name == "wiper":
        return (f'<g transform="rotate(-24 60 60)"><rect x="6" y="60" width="108" height="8" rx="3" fill="{I}"/>'
                f'<path d="M14,60 L40,50 H80 L106,60 Z" fill="{S}"/>'
                f'<rect x="52" y="42" width="16" height="12" rx="2" fill="{Y}"/></g>')
    if name == "bulb":
        return (f'<rect x="46" y="70" width="28" height="18" rx="3" fill="{S}"/>'
                f'<rect x="50" y="88" width="20" height="18" rx="2" fill="{I}"/>'
                f'<path d="M48,70 V40 Q48,18 60,18 Q72,18 72,40 V70 Z" fill="{PAPER}" stroke="{I}" stroke-width="3"/>'
                f'<path d="M55,64 V44 Q60,36 65,44 V64" fill="none" stroke="{Y}" stroke-width="3"/>'
                f'<path d="M84,30 L94,24 M86,44 L98,44 M84,58 L94,64" stroke="{Y}" stroke-width="4" stroke-linecap="round"/>')
    # --- ГРМ ---
    loop = "M36,38 L88,32 A28,28 0 0 1 88,88 L36,82 A22,22 0 0 1 36,38 Z"
    if name == "chain":
        return (f'<circle cx="36" cy="60" r="17" fill="{S}"/><circle cx="36" cy="60" r="6" fill="{I}"/>'
                f'<circle cx="88" cy="60" r="23" fill="{S}"/><circle cx="88" cy="60" r="8" fill="{I}"/>'
                f'<path d="{loop}" fill="none" stroke="{I}" stroke-width="9"/>'
                f'<path d="{loop}" fill="none" stroke="{WHITE}" stroke-width="3" stroke-dasharray="3 5"/>')
    if name == "belt":
        return (f'<circle cx="36" cy="60" r="17" fill="{SL}"/><circle cx="36" cy="60" r="6" fill="{SD}"/>'
                f'<circle cx="88" cy="60" r="23" fill="{SL}"/><circle cx="88" cy="60" r="8" fill="{SD}"/>'
                f'<path d="{loop}" fill="none" stroke="{I}" stroke-width="10"/>'
                f'<path d="{loop}" fill="none" stroke="{Y}" stroke-width="2"/>')
    if name == "tensioner":
        return (f'<rect x="20" y="34" width="16" height="52" rx="4" fill="{SD}"/>'
                f'<circle cx="28" cy="44" r="4" fill="{PAPER}"/><circle cx="28" cy="76" r="4" fill="{PAPER}"/>'
                f'<rect x="34" y="44" width="52" height="32" rx="6" fill="{I}"/>'
                f'<rect x="86" y="53" width="18" height="14" rx="3" fill="{S}"/>'
                f'<rect x="46" y="56" width="28" height="8" rx="2" fill="{Y}"/>')
    if name == "guide":
        return (f'<path d="M12,78 Q60,36 108,52 L106,64 Q60,52 16,90 Z" fill="{I}"/>'
                f'<path d="M12,72 Q60,30 108,46 L108,52 Q60,36 12,78 Z" fill="{S}"/>'
                f'<circle cx="30" cy="74" r="3.5" fill="{PAPER}"/><circle cx="90" cy="56" r="3.5" fill="{PAPER}"/>')
    if name == "seal":
        return (f'<path fill="{I}" fill-rule="evenodd" d="{circle_path(60, 60, 34)} {circle_path(60, 60, 14)}"/>'
                f'<circle cx="60" cy="60" r="24" fill="none" stroke="{S}" stroke-width="6"/>'
                f'<circle cx="60" cy="60" r="17" fill="none" stroke="{Y}" stroke-width="2"/>')
    if name == "sealant":
        return (f'<path d="M24,48 H82 L96,54 V66 L82,72 H24 Z" fill="{I}"/>'
                f'<rect x="14" y="46" width="12" height="28" rx="2" fill="{S}"/>'
                f'<path d="M96,56 L114,59 V61 L96,64 Z" fill="{S}"/>'
                f'<rect x="38" y="53" width="32" height="14" rx="3" fill="{Y}"/>')
    if name == "roller":
        return (f'<path d="M22,88 L52,34 L70,44 L40,98 Z" fill="{I}"/>'
                f'<circle cx="66" cy="58" r="30" fill="{SL}"/>'
                f'<circle cx="66" cy="58" r="20" fill="none" stroke="{S}" stroke-width="4"/>'
                f'<circle cx="66" cy="58" r="8" fill="{I}"/>')
    raise KeyError(name)


def place_icon(name, x, y, size):
    return f'<g transform="translate({x} {y}) scale({size / 120})">{icon(name)}</g>'


# --- Крафт-коробка с содержимым (для карточек) ---------------------------
def kraft_box(uid, peek=(), sticker=True):
    """Открытая коробка; peek — до 3 иконок, торчащих из коробки. Габарит ≈ x 10..470, y 20..400."""
    spots = [(118, 42, 120), (196, 18, 124), (282, 44, 118)]
    peeking = "".join(place_icon(n, x, y, s) for n, (x, y, s) in zip(peek, spots))
    out = (f'<path d="M60,150 L240,110 L420,150 L240,190 Z" fill="{KRAFT_DARK}"/>'
           + peeking
           + f'<path d="M60,150 L240,190 V400 L60,360 Z" fill="{KRAFT}"/>'
           f'<path d="M420,150 L240,190 V400 L420,360 Z" fill="{KRAFT_MID}"/>'
           f'<path d="M60,150 L10,205 L190,245 L240,190 Z" fill="{KRAFT_LIGHT}"/>'
           f'<path d="M420,150 L470,205 L290,245 L240,190 Z" fill="{KRAFT_LIGHT}"/>'
           f'<path d="M140,168 L162,173 V383 L140,378 Z" fill="{YELLOW}"/>')
    if sticker:
        out += (f'<g transform="translate(262 238) skewY(-12.5) scale(1.35)">'
                f'<rect x="-2" y="6" width="110" height="88" rx="10" fill="{PAPER}"/>'
                f'<g transform="translate(4 8)">{whale(INK, PAPER, uid)}</g></g>')
    return out
