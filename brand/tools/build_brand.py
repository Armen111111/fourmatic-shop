"""Логотипы, аватар, наклейка, обложки и брендбук ZAPKIT → brand/svg/*.svg

Запуск:  python3 brand/tools/build_brand.py
PNG:     NODE_PATH=$(npm root -g) node brand/tools/render.js brand/svg brand/png
"""

from pathlib import Path

from zapkit import (BRAND, BRAND_CYR, INK, KRAFT, PAPER, STEEL, STEEL_LIGHT, TAGLINE, WHITE, YELLOW,
                    check_icon, lockup, lockup_width, svg, text, two_tone, whale)

OUT = Path(__file__).resolve().parent.parent / "svg"


def logo(fg, bg, uid, colors=None, word=BRAND, tagline_color=None, pad=14):
    """Горизонтальный логотип; если tagline_color задан — со слоганом снизу."""
    w = lockup_width(word)
    body = lockup(fg, bg, uid, word, colors)
    h = 134
    if tagline_color:
        body += text(176, 150, TAGLINE, 25, tagline_color, length=w - 176)
        h = 186
    vb = f"{-pad} -20 {w + 2 * pad} {h}"
    return body, vb, (w + 2 * pad) * 2, h * 2


def sticker(uid, size=400):
    """Круглая наклейка на коробку: жёлтый круг, кит, текст по кругу."""
    r = size / 2
    rt, rb = r - 56, r - 30  # радиусы строк: верхняя (буквы наружу), нижняя (буквы внутрь)
    return (
        f'<defs><path id="top-{uid}" d="M{r - rt},{r} A{rt},{rt} 0 0 1 {r + rt},{r}"/>'
        f'<path id="bot-{uid}" d="M{r - rb},{r} A{rb},{rb} 0 0 0 {r + rb},{r}"/></defs>'
        f'<circle cx="{r}" cy="{r}" r="{r}" fill="{YELLOW}"/>'
        f'<circle cx="{r}" cy="{r}" r="{r - 12}" fill="none" stroke="{INK}" stroke-width="4"/>'
        f'<text font-family="\'Liberation Sans\', Arial, sans-serif" font-size="46" font-weight="700" fill="{INK}" '
        f'letter-spacing="10"><textPath href="#top-{uid}" startOffset="50%" text-anchor="middle">{BRAND}</textPath></text>'
        f'<text font-family="\'Liberation Sans\', Arial, sans-serif" font-size="22" font-weight="700" fill="{INK}" '
        f'letter-spacing="3"><textPath href="#bot-{uid}" startOffset="50%" text-anchor="middle">{TAGLINE}</textPath></text>'
        f'<g transform="translate({r - 104} {r - 88}) scale(1.9)">{whale(INK, YELLOW, uid)}</g>'
    )


def cover_desktop():
    """Обложка магазина для компьютера: 1202×436 (нужна подписка Авито Pro)."""
    W, H = 1202, 436
    rows = "".join(check_icon(690, 150 + i * 62, YELLOW, INK, 28)
                   + text(730, 173 + i * 62, s, 24, PAPER)
                   for i, s in enumerate(["Всё до болта — в одной коробке",
                                          "Подбор по VIN с гарантией",
                                          "Не хватило детали — довезём"]))
    body = (f'<rect width="{W}" height="{H}" fill="{INK}"/>'
            f'<path d="M1060,0 H1120 L1202,82 V142 Z" fill="{YELLOW}"/>'
            f'<g transform="translate(80 150) scale(0.9)">{lockup(YELLOW, INK, "cd", word_colors=two_tone(PAPER, YELLOW))}</g>'
            + text(238, 300, TAGLINE, 27, PAPER, length=lockup_width() * 0.9 - 158)
            + text(238, 338, "Запчасти наборами под конкретный ремонт", 19, STEEL)
            + rows)
    return svg(W, H, body, "ZAPKIT — обложка магазина (компьютер)")


def cover_mobile():
    """Обложка магазина для телефона: 1242×936 (нужна подписка Авито Pro)."""
    W, H = 1242, 936
    lw = lockup_width() * 1.3
    rows = "".join(check_icon(260, 520 + i * 84, YELLOW, INK, 40)
                   + text(322, 552 + i * 84, s, 34, PAPER)
                   for i, s in enumerate(["Всё до последнего болта в коробке",
                                          "Подбор по VIN с гарантией",
                                          "Не хватило детали — довезём"]))
    body = (f'<rect width="{W}" height="{H}" fill="{INK}"/>'
            f'<path d="M1080,0 H1160 L1242,82 V162 Z" fill="{YELLOW}"/>'
            f'<path d="M0,780 L156,936 H76 L0,860 Z" fill="{YELLOW}"/>'
            f'<g transform="translate({(W - lw) / 2 - 10} 170) scale(1.3)">'
            f'{lockup(YELLOW, INK, "cm", word_colors=two_tone(PAPER, YELLOW))}</g>'
            + text(W / 2, 390, TAGLINE, 40, PAPER, anchor="middle", spacing=4)
            + rows)
    return svg(W, H, body, "ZAPKIT — обложка магазина (телефон)")


def avatar(bg, fg, uid):
    """Квадрат; Авито обрезает аватар в круг — кит вписан в безопасную зону."""
    return svg(1024, 1024,
               f'<rect width="100" height="100" fill="{bg}"/>'
               f'<g transform="translate(50 52) scale(0.8) translate(-55 -52)">{whale(fg, bg, uid)}</g>',
               "ZAPKIT — аватар", "0 0 100 100")


def brand_board():
    """Брендбук на одном листе 1600×1200."""
    W, H = 1600, 1200
    parts = [f'<rect width="{W}" height="{H}" fill="{PAPER}"/>',
             text(60, 80, "ZAPKIT · фирменный стиль", 34, INK),
             text(60, 116, "Запчасти наборами. Ремонт в одной коробке.", 22, STEEL, weight=400)]
    # основной логотип
    parts.append(f'<rect x="60" y="150" width="960" height="330" rx="24" fill="{WHITE}"/>')
    parts.append(f'<g transform="translate(128 232) scale(1.3)">{lockup(INK, WHITE, "bb1")}</g>')
    parts.append(text(90, 455, "Основной логотип", 18, STEEL, weight=400))
    # на тёмном и на жёлтом
    parts.append(f'<rect x="60" y="500" width="470" height="200" rx="24" fill="{INK}"/>')
    parts.append(f'<g transform="translate(92 562) scale(0.66)">{lockup(YELLOW, INK, "bb2", word_colors=two_tone(PAPER, YELLOW))}</g>')
    parts.append(text(90, 680, "На тёмном: KIT — жёлтым", 18, STEEL_LIGHT, weight=400))
    parts.append(f'<rect x="550" y="500" width="470" height="200" rx="24" fill="{YELLOW}"/>')
    parts.append(f'<g transform="translate(582 562) scale(0.66)">{lockup(INK, YELLOW, "bb3")}</g>')
    parts.append(text(580, 680, "На жёлтом", 18, INK, weight=400))
    # кириллический вариант
    parts.append(f'<rect x="60" y="720" width="960" height="150" rx="24" fill="{WHITE}"/>')
    parts.append(f'<g transform="translate(92 766) scale(0.55)">{lockup(INK, WHITE, "bb4", word=BRAND_CYR)}</g>')
    parts.append(text(560, 792, "Вариант кириллицей", 20, INK))
    parts.append(text(560, 822, "для тех, кто не читает латиницу:", 18, STEEL, weight=400))
    parts.append(text(560, 848, "вывески, печать для старшей аудитории", 18, STEEL, weight=400))
    # аватар и наклейка
    parts.append(f'<rect x="1050" y="150" width="490" height="330" rx="24" fill="{WHITE}"/>')
    for i, (d, x) in enumerate(((180, 1080), (84, 1290), (48, 1400))):
        parts.append(f'<g transform="translate({x} {290 - d / 2})"><clipPath id="av{i}"><circle cx="{d / 2}" cy="{d / 2}" r="{d / 2}"/></clipPath>'
                     f'<g clip-path="url(#av{i})"><rect width="{d}" height="{d}" fill="{YELLOW}"/>'
                     f'<g transform="scale({d / 100}) translate(50 52) scale(0.8) translate(-55 -52)">{whale(INK, YELLOW, f"av{i}")}</g></g></g>')
    parts.append(text(1080, 455, "Аватар на Авито: 180 / 84 / 48 px", 18, STEEL, weight=400))
    parts.append(f'<rect x="1050" y="500" width="490" height="370" rx="24" fill="{WHITE}"/>')
    parts.append(f'<g transform="translate(1155 520) scale(0.7)">{sticker("bbs")}</g>')
    parts.append(text(1080, 850, "Наклейка на коробку (Ø 6 см)", 18, STEEL, weight=400))
    # цвета
    swatches = [(YELLOW, "Жёлтый «скотч»", "#FFC72C", INK), (INK, "Графит", "#14161A", PAPER),
                (PAPER, "Тёплый белый", "#FAF7F0", INK), (KRAFT, "Крафт", "#C8925A", INK),
                (STEEL, "Сталь", "#8C929B", WHITE)]
    for i, (c, name, hexv, tc) in enumerate(swatches):
        x = 60 + i * 300
        parts.append(f'<rect x="{x}" y="900" width="280" height="200" rx="20" fill="{c}" stroke="#E4E0D8" stroke-width="2"/>')
        parts.append(text(x + 24, 1050, name, 22, tc))
        parts.append(text(x + 24, 1080, hexv, 20, tc, weight=400))
    parts.append(text(60, 1150, "Шрифт в объявлениях: Arial / Liberation Sans (жирный для заголовков). "
                               "Буквы логотипа нарисованы вручную — это не шрифт.", 18, STEEL, weight=400))
    return svg(W, H, "".join(parts), "ZAPKIT — фирменный стиль")


def build():
    OUT.mkdir(parents=True, exist_ok=True)
    for old in OUT.glob("*.svg"):
        old.unlink()
    files = {}
    for name, fg, bg, colors, tag in (
            ("zapkit-logo-dark", INK, PAPER, None, None),
            ("zapkit-logo-light", YELLOW, INK, two_tone(PAPER, YELLOW), None),
            ("zapkit-logo-on-yellow", INK, YELLOW, None, None),
            ("zapkit-lockup-dark", INK, PAPER, None, INK),
            ("zapkit-lockup-light", YELLOW, INK, two_tone(PAPER, YELLOW), PAPER)):
        body, vb, w, h = logo(fg, bg, name, colors, tagline_color=tag)
        files[f"{name}.svg"] = svg(w, h, body, "ZAPKIT", vb)
    body, vb, w, h = logo(INK, PAPER, "cyr", word=BRAND_CYR)
    files["zapkit-logo-cyrillic.svg"] = svg(w, h, body, "ЗАПКИТ", vb)
    files["zapkit-mark.svg"] = svg(512, 512, f'<g transform="translate(-3 -2)">{whale(INK, PAPER, "m")}</g>',
                                   "ZAPKIT — знак", "0 0 106 100")
    files["zapkit-avatar.svg"] = avatar(YELLOW, INK, "ay")
    files["zapkit-avatar-dark.svg"] = avatar(INK, YELLOW, "ad")
    files["zapkit-sticker.svg"] = svg(800, 800, sticker("st"), "ZAPKIT — наклейка", "0 0 400 400")
    files["avito-cover-desktop-1202x436.svg"] = cover_desktop()
    files["avito-cover-mobile-1242x936.svg"] = cover_mobile()
    files["zapkit-brand-board.svg"] = brand_board()
    for name, content in files.items():
        (OUT / name).write_text(content, encoding="utf-8")
        print("written", OUT / name)


if __name__ == "__main__":
    build()
