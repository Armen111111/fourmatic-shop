"""Генератор логотипа ВПОРУ.

Все буквы нарисованы вручную геометрией (без шрифтов), поэтому SVG
одинаково выглядит везде. Буква «О» — шестигранная гайка: отверстие
гайки и есть «О».

Запуск:  python3 brand/tools/build_brand.py
Результат: brand/svg/*.svg (PNG рендерит brand/tools/render.js)
"""

import math
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "svg"

INK = "#16191E"     # графит
ORANGE = "#FF6A1A"  # сигнальный оранжевый
PAPER = "#F4F2EE"   # тёплый белый
STEEL = "#9AA1AB"   # сталь (второстепенный текст)

TAGLINE = "ЗАПЧАСТИ, КОТОРЫЕ ПОДХОДЯТ"
FONT_STACK = "'Liberation Sans', Arial, Helvetica, sans-serif"

# Буквы — осевые линии, толщина штриха 18, высота 100.
STROKE = 18
LETTERS = {
    "В": "M9,100 V9 H38 A13,13 0 0 1 51,22 V37 A13,13 0 0 1 38,50 H9 "
         "M9,50 H44 A13,13 0 0 1 57,63 V78 A13,13 0 0 1 44,91 H0",
    "П": "M9,100 V9 H44 A13,13 0 0 1 57,22 V100",
    "Р": "M9,100 V9 H44 A13,13 0 0 1 57,22 V45 A13,13 0 0 1 44,58 H9",
    "У": "M9,0 V37 A13,13 0 0 0 22,50 H57 M57,0 V78 A13,13 0 0 1 44,91 H0",
}
LETTER_X = {"В": 0, "П": 80, "Р": 264, "У": 344}
NUT_CX, NUT_CY, NUT_R, NUT_HOLE = 205, 50, 52, 24
WORD_W, WORD_TOP, WORD_BOTTOM = 410, -2, 102  # гайка чуть выступает, как «О»


def hex_path(cx, cy, r):
    pts = []
    for i in range(6):
        a = math.radians(90 + 60 * i)
        pts.append((cx + r * math.cos(a), cy - r * math.sin(a)))
    return "M" + " L".join(f"{x:.2f},{y:.2f}" for x, y in pts) + " Z"


def circle_path(cx, cy, r):
    return (f"M{cx - r:.2f},{cy:.2f} a{r},{r} 0 1 0 {2 * r},0 "
            f"a{r},{r} 0 1 0 {-2 * r},0 Z")


def nut(cx, cy, r, hole, fill):
    return (f'<path fill="{fill}" fill-rule="evenodd" '
            f'd="{hex_path(cx, cy, r)} {circle_path(cx, cy, hole)}"/>')


def check(cx, cy, scale, color, width):
    s = scale
    return (f'<path d="M{cx - 11 * s:.2f},{cy + 1 * s:.2f} '
            f'L{cx - 3 * s:.2f},{cy + 9 * s:.2f} L{cx + 12 * s:.2f},{cy - 8 * s:.2f}" '
            f'fill="none" stroke="{color}" stroke-width="{width}" '
            f'stroke-linecap="round" stroke-linejoin="round"/>')


def wordmark(letters_color, nut_color=ORANGE):
    parts = [f'<g fill="none" stroke="{letters_color}" stroke-width="{STROKE}" '
             f'stroke-linejoin="miter" stroke-linecap="butt">']
    for ch, x in LETTER_X.items():
        parts.append(f'<path transform="translate({x} 0)" d="{LETTERS[ch]}"/>')
    parts.append("</g>")
    parts.append(nut(NUT_CX, NUT_CY, NUT_R, NUT_HOLE, nut_color))
    return "".join(parts)


def svg(w, h, body, title, viewbox=None):
    vb = viewbox or f"0 0 {w} {h}"
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" '
            f'width="{w}" height="{h}" role="img" aria-label="{title}">'
            f"<title>{title}</title>{body}</svg>\n")


def tagline(x, y, width, size, color):
    return (f'<text x="{x}" y="{y}" font-family="{FONT_STACK}" font-size="{size}" '
            f'font-weight="700" fill="{color}" textLength="{width}" '
            f'lengthAdjust="spacing">{TAGLINE}</text>')


def build():
    OUT.mkdir(parents=True, exist_ok=True)
    pad = 12
    vb = f"{-pad} {WORD_TOP - pad} {WORD_W + 2 * pad} {WORD_BOTTOM - WORD_TOP + 2 * pad}"
    files = {}

    # 1–2. Основной логотип (только буквы + гайка), прозрачный фон
    files["vporu-wordmark-dark.svg"] = svg(868, 256, wordmark(INK), "ВПОРУ", vb)
    files["vporu-wordmark-light.svg"] = svg(868, 256, wordmark(PAPER), "ВПОРУ", vb)

    # 3–4. Логотип со слоганом
    lock_vb = f"{-pad} {WORD_TOP - pad} {WORD_W + 2 * pad} {WORD_BOTTOM - WORD_TOP + 2 * pad + 44}"
    for name, color, sub in (("dark", INK, INK), ("light", PAPER, STEEL)):
        body = wordmark(color) + tagline(0, 138, WORD_W, 21, sub if name == "light" else INK)
        files[f"vporu-lockup-{name}.svg"] = svg(868, 344, body, "ВПОРУ — запчасти, которые подходят", lock_vb)

    # 5. Знак отдельно: гайка + галочка «подходит»
    files["vporu-mark.svg"] = svg(
        512, 512, nut(50, 50, 46, 21, ORANGE) + check(50, 50, 0.84, INK, 5.6),
        "ВПОРУ — знак", "0 0 100 100")

    # 6–7. Аватар для Авито (квадрат, Авито сам обрежет в круг —
    # знак вписан в безопасный круг)
    files["vporu-avatar.svg"] = svg(
        1024, 1024,
        f'<rect width="100" height="100" fill="{ORANGE}"/>'
        + nut(50, 50, 34, 15.5, INK) + check(50, 50, 0.62, PAPER, 4.2),
        "ВПОРУ — аватар", "0 0 100 100")
    files["vporu-avatar-dark.svg"] = svg(
        1024, 1024,
        f'<rect width="100" height="100" fill="{INK}"/>'
        + nut(50, 50, 34, 15.5, ORANGE) + check(50, 50, 0.62, PAPER, 4.2),
        "ВПОРУ — аватар (тёмный)", "0 0 100 100")

    # 8. Обложка магазина 1920×640: содержимое в центральной безопасной зоне
    W, H = 1920, 640
    pattern = []
    for row in range(-1, 8):
        for col in range(-1, 22):
            cx = col * 104 + (52 if row % 2 else 0)
            cy = row * 90
            pattern.append(f'<path d="{hex_path(cx, cy, 52)}"/>')
    usp = ["Подбор по VIN с гарантией",
           "Оригинал и проверенные аналоги",
           "Доставка по всей России"]
    chips = []
    for i, text in enumerate(usp):
        y = 214 + i * 84
        chips.append(
            f'<g transform="translate(1180 {y})">'
            f'<rect width="560" height="64" rx="12" fill="none" stroke="{STEEL}" stroke-opacity="0.35" stroke-width="2"/>'
            + nut(34, 32, 16, 7, ORANGE)
            + f'<text x="66" y="42" font-family="{FONT_STACK}" font-size="28" '
              f'font-weight="700" fill="{PAPER}">{text}</text></g>')
    body = (f'<rect width="{W}" height="{H}" fill="{INK}"/>'
            f'<g fill="none" stroke="{PAPER}" stroke-opacity="0.045" stroke-width="2">{"".join(pattern)}</g>'
            f'<g transform="translate(180 218) scale(2)">{wordmark(PAPER)}</g>'
            + tagline(180, 520, 820, 40, STEEL)
            + f'<text x="180" y="170" font-family="{FONT_STACK}" font-size="30" font-weight="700" '
              f'fill="{ORANGE}" letter-spacing="3">ДЛЯ MERCEDES-BENZ</text>'
            + "".join(chips))
    files["avito-cover.svg"] = svg(W, H, body, "ВПОРУ — обложка магазина")

    for name, content in files.items():
        (OUT / name).write_text(content, encoding="utf-8")
        print("written", OUT / name)


if __name__ == "__main__":
    build()
