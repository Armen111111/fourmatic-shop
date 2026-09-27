"""Генератор бренда ЗАПКИТ.

Знак — кит, перевязанный крест-накрест лентой, как посылка:
kit (англ.) = набор, «кит» (рус.) = кит. Буквы нарисованы вручную
геометрией (без шрифтов), поэтому SVG одинаково выглядит везде.

Запуск:  python3 brand/tools/build_brand.py
Результат: brand/svg/*.svg (PNG рендерит brand/tools/render.js)
"""

from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "svg"

YELLOW = "#FFC72C"  # жёлтый «скотч»
INK = "#14161A"     # графит
PAPER = "#FAF7F0"   # тёплый белый
KRAFT = "#C8925A"   # крафт-картон (второстепенный)
STEEL = "#8C929B"   # второстепенный текст

TAGLINE = "РЕМОНТ В ОДНОЙ КОРОБКЕ"
FONT = "'Liberation Sans', Arial, Helvetica, sans-serif"

# --- Кит (сетка 100×100) -------------------------------------------------
WHALE_BODY = ("M8,60 C8,43 23,34 42,34 C57,34 67,41 71,51 C76,47 79,41 81.5,31 "
              "L86.5,31 C88,48 81,60 70,64 C66,76 54,84 38,84 C20,84 8,75 8,60 Z")
WHALE_FLUKE = ("M84,36 C80,28 73,25 66,26 C70,19 79,19 84,27 "
               "C89,19 98,19 102,26 C95,25 88,28 84,36 Z")
WHALE_SPOUT = "M28,28 V18 M28,22 C24,18 20,18 17,20 M28,22 C32,18 36,18 39,20"


def whale(fg, bg, uid):
    """Кит, перевязанный лентой. uid — уникальный id для clipPath."""
    return (
        f'<defs><clipPath id="wb-{uid}"><path d="{WHALE_BODY}"/></clipPath></defs>'
        f'<path fill="{fg}" d="{WHALE_BODY}"/><path fill="{fg}" d="{WHALE_FLUKE}"/>'
        f'<g clip-path="url(#wb-{uid})" fill="{bg}">'
        f'<rect x="40" y="30" width="8" height="60"/><rect x="0" y="64" width="90" height="7"/></g>'
        f'<circle cx="22" cy="55" r="3.6" fill="{bg}"/>'
        f'<path d="{WHALE_SPOUT}" fill="none" stroke="{fg}" stroke-width="4.4" stroke-linecap="round"/>'
    )


# --- Буквы: осевые линии, штрих 18, высота 100 ---------------------------
LETTERS = {
    "З": "M0,9 H44 A13,13 0 0 1 57,22 V37 A13,13 0 0 1 44,50 H16 "
         "M16,50 H44 A13,13 0 0 1 57,63 V78 A13,13 0 0 1 44,91 H0",
    "А": "M9,100 V36 L28,9 H38 L57,36 V100 M9,62 H57",
    "П": "M9,100 V9 H44 A13,13 0 0 1 57,22 V100",
    "К": "M9,0 V100 M9,64 L62,-6 M30,44 L66,106",
    "И": "M9,0 V100 M57,0 V100 M9,100 L57,0",
    "Т": "M0,9 H66 M33,9 V100",
}
ORDER = ["З", "А", "П", "К", "И", "Т"]
ADVANCE = 80
WORD_W = ADVANCE * (len(ORDER) - 1) + 66  # 466


def wordmark(color, uid):
    parts = [f'<defs><clipPath id="lc-{uid}"><rect width="66" height="100"/></clipPath></defs>',
             f'<g fill="none" stroke="{color}" stroke-width="18" stroke-linejoin="miter" stroke-miterlimit="10">']
    for i, ch in enumerate(ORDER):
        parts.append(f'<g transform="translate({i * ADVANCE} 0)">'
                     f'<path clip-path="url(#lc-{uid})" d="{LETTERS[ch]}"/></g>')
    parts.append("</g>")
    return "".join(parts)


# Горизонтальный логотип: кит (масштаб 1.5) + надпись
LOCK_WORD_X = 176
LOCK_W = LOCK_WORD_X + WORD_W  # 642


def lockup(fg, bg, uid):
    return (f'<g transform="translate(0 -30) scale(1.5)">{whale(fg, bg, uid)}</g>'
            f'<g transform="translate({LOCK_WORD_X} 0)">{wordmark(fg, uid)}</g>')


def text(x, y, s, size, color, weight=700, anchor="start", spacing=None, length=None):
    extra = f' letter-spacing="{spacing}"' if spacing else ""
    if length:
        extra += f' textLength="{length}" lengthAdjust="spacing"'
    return (f'<text x="{x}" y="{y}" font-family="{FONT}" font-size="{size}" font-weight="{weight}" '
            f'fill="{color}" text-anchor="{anchor}"{extra}>{s}</text>')


def svg(w, h, body, title, viewbox=None):
    vb = viewbox or f"0 0 {w} {h}"
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" width="{w}" height="{h}" '
            f'role="img" aria-label="{title}"><title>{title}</title>{body}</svg>\n')


def check_icon(x, y, color, bg):
    return (f'<g transform="translate({x} {y})"><rect width="30" height="30" rx="8" fill="{color}"/>'
            f'<path d="M8,15.5 L13,20.5 L22,10" fill="none" stroke="{bg}" stroke-width="3.6" '
            f'stroke-linecap="round" stroke-linejoin="round"/></g>')


def kraft_box(uid):
    """Иллюстрация: открытая крафт-коробка с наклейкой-китом (для карточки товара)."""
    return (
        f'<path d="M60,150 L240,110 L420,150 L240,190 Z" fill="#A87444"/>'           # дно/тень внутри
        f'<path d="M60,150 L240,190 V400 L60,360 Z" fill="{KRAFT}"/>'                  # левая грань
        f'<path d="M420,150 L240,190 V400 L420,360 Z" fill="#B98150"/>'               # правая грань
        f'<path d="M60,150 L10,205 L190,245 L240,190 Z" fill="#D6A26C"/>'             # клапан слева
        f'<path d="M420,150 L470,205 L290,245 L240,190 Z" fill="#D6A26C"/>'           # клапан справа
        f'<path d="M140,168 L162,173 V383 L140,378 Z" fill="{YELLOW}"/>'              # скотч
        f'<g transform="translate(262 238) skewY(-12.5) scale(1.35)">'
        f'<rect x="-2" y="6" width="110" height="88" rx="10" fill="{PAPER}"/>'
        f'<g transform="translate(4 8)">{whale(INK, PAPER, uid)}</g></g>'
    )


def build():
    OUT.mkdir(parents=True, exist_ok=True)
    files = {}
    pad = 14

    # 1–3. Горизонтальный логотип
    lvb = f"{-pad} -20 {LOCK_W + 2 * pad} 134"
    for name, fg, bg in (("dark", INK, PAPER), ("light", YELLOW, INK), ("on-yellow", INK, YELLOW)):
        files[f"zapkit-logo-{name}.svg"] = svg(1340, 268, lockup(fg, bg, name), "ЗАПКИТ", lvb)

    # 4–5. Логотип со слоганом (на прозрачном фоне; «прорези» ленты — цвет фона)
    tvb = f"{-pad} -20 {LOCK_W + 2 * pad} 186"
    files["zapkit-lockup-dark.svg"] = svg(
        1340, 372, lockup(INK, PAPER, "ld") + text(LOCK_WORD_X, 150, TAGLINE, 25, INK, length=WORD_W),
        "ЗАПКИТ — ремонт в одной коробке", tvb)
    files["zapkit-lockup-light.svg"] = svg(
        1340, 372, lockup(YELLOW, INK, "ll") + text(LOCK_WORD_X, 150, TAGLINE, 25, PAPER, length=WORD_W),
        "ЗАПКИТ — ремонт в одной коробке", tvb)

    # 6. Знак отдельно
    files["zapkit-mark.svg"] = svg(512, 512, f'<g transform="translate(-3 -2)">{whale(INK, PAPER, "m")}</g>',
                                   "ЗАПКИТ — знак", "0 0 106 100")

    # 7–8. Аватары для Авито: квадрат, кит вписан в безопасный круг
    def avatar(bg, fg, uid):
        return svg(1024, 1024,
                   f'<rect width="100" height="100" fill="{bg}"/>'
                   f'<g transform="translate(50 52) scale(0.8) translate(-55 -52)">{whale(fg, bg, uid)}</g>',
                   "ЗАПКИТ — аватар", "0 0 100 100")
    files["zapkit-avatar.svg"] = avatar(YELLOW, INK, "ay")
    files["zapkit-avatar-dark.svg"] = avatar(INK, YELLOW, "ad")

    # 9. Обложка магазина 1920×640
    W, H = 1920, 640
    tape = (f'<g opacity="0.9"><path d="M1540,0 H1620 L1920,300 V380 Z" fill="{YELLOW}"/>'
            f'</g>')
    usp = ["Всё для работы — до последнего болта",
           "Подбор по VIN с гарантией",
           "Не хватило детали — довезём бесплатно"]
    rows = "".join(check_icon(1050, 236 + i * 76, YELLOW, INK)
                   + text(1098, 260 + i * 76, s, 32, PAPER) for i, s in enumerate(usp))
    cover = (f'<rect width="{W}" height="{H}" fill="{INK}"/>{tape}'
             f'<g transform="translate(150 230) scale(1.25)">{lockup(YELLOW, INK, "cv")}</g>'
             + text(370, 450, TAGLINE, 40, PAPER, length=582)
             + text(370, 510, "Наборы запчастей для корейских, китайских и европейских авто", 24, STEEL)
             + rows)
    files["avito-cover.svg"] = svg(W, H, cover, "ЗАПКИТ — обложка магазина")

    # 10. Пример карточки набора для объявления (1200×900)
    items = ["Масло моторное, 4 л", "Фильтр масляный", "Фильтр воздушный",
             "Фильтр салонный", "Шайба сливной пробки", "Карта ремонта с QR-видео"]
    lst = "".join(check_icon(640, 318 + i * 62, INK, YELLOW)
                  + text(686, 342 + i * 62, s, 30, INK, weight=400) for i, s in enumerate(items))
    card = (f'<rect width="1200" height="900" fill="{PAPER}"/>'
            f'<g transform="translate(60 210)">{kraft_box("kc")}</g>'
            f'<g transform="translate(60 56) scale(0.62)">{lockup(INK, PAPER, "kl")}</g>'
            f'<rect x="640" y="150" width="170" height="52" rx="26" fill="{YELLOW}"/>'
            + text(725, 186, "ТО-КИТ", 28, INK, anchor="middle")
            + text(640, 272, "Hyundai Solaris 1.6", 50, INK)
            + lst
            + f'<rect y="790" width="1200" height="110" fill="{INK}"/>'
            + text(600, 858, "Подбор по VIN  ·  Всё в одной коробке  ·  Отправка 1–2 дня", 32, YELLOW,
                   anchor="middle"))
    files["kit-card-example.svg"] = svg(1200, 900, card, "ЗАПКИТ — пример карточки набора")

    for name, content in files.items():
        (OUT / name).write_text(content, encoding="utf-8")
        print("written", OUT / name)


if __name__ == "__main__":
    build()
