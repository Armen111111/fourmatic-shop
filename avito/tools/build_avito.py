"""Фотокарточки объявлений, печать и макет магазина ZAPKIT → avito/svg/*.svg

Данные наборов: avito/kits.json
Запуск:  python3 avito/tools/build_avito.py
PNG:     NODE_PATH=$(npm root -g) node brand/tools/render.js avito/svg avito/png

Карточки 1600×1200 (4:3). В мобильной ленте Авито обрезает фото до квадрата
по центру, поэтому всё важное лежит в зоне x 200…1400.
"""

import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "brand" / "tools"))

from zapkit import (INK, PAPER, STEEL, STEEL_LIGHT, WHITE, YELLOW, check_icon,  # noqa: E402
                    fit_size, kraft_box, lockup, place_icon, svg, text, text_width, two_tone, whale, wrap)

OUT = ROOT / "avito" / "svg"
W, H = 1600, 1200
SAFE_L, SAFE_R = 230, 1370  # поля внутри квадрата 200…1400
BAR = "Подбор по VIN · Всё в одной коробке · СДЭК каждый вечер"


# --- Общие элементы карточек ---------------------------------------------
def decor(color=YELLOW):
    """Полосы «скотча» по углам — вне квадратной зоны, их не жалко обрезать."""
    return (f'<path d="M0,110 L110,0 H180 L0,180 Z" fill="{color}"/>'
            f'<path d="M1600,900 L1420,1080 H1490 L1600,970 Z" fill="{color}"/>')


def header(uid, dark=False):
    word = two_tone(PAPER, YELLOW) if dark else None
    return (f'<g transform="translate({SAFE_L} 76) scale(0.62)">'
            f'{lockup(YELLOW if dark else INK, INK if dark else PAPER, uid, word_colors=word)}</g>')


def pill(label, right=SAFE_R, y=78, bg=YELLOW, fg=INK):
    w = text_width(label, 36) + 60
    x = right - w
    return (f'<rect x="{x}" y="{y}" width="{w}" height="68" rx="34" fill="{bg}"/>'
            + text(x + w / 2, y + 47, label, 36, fg, anchor="middle"))


def bottom_bar(label, bg=INK, fg=YELLOW):
    return (f'<rect y="1080" width="{W}" height="120" fill="{bg}"/>'
            + text(W / 2, 1154, label, fit_size(label, 1120, 36), fg, anchor="middle"))


def item_label(item):
    q = item["qty"]
    if not q:
        return item["name"]
    return f'{item["name"]} {q}' if q.startswith("×") else f'{item["name"]}, {q}'


# --- Слайд 1: главная ----------------------------------------------------
def slide_main(kit, uid):
    """Крупное название машины сверху — его видно даже в маленьком превью ленты."""
    parts = [f'<rect width="{W}" height="{H}" fill="{PAPER}"/>', decor(), header(f"{uid}h"), pill(kit["type"]),
             text(SAFE_L, 262, kit["car"], fit_size(kit["car"], SAFE_R - SAFE_L, 84), INK),
             text(SAFE_L, 322, kit["job"], 34, STEEL, weight=400),
             f'<g transform="translate({SAFE_L} 372) scale(1.2)">{kraft_box(uid, kit["peek"])}</g>']
    x0, y = 850, 480
    for item in kit["items"]:
        label = item_label(item)
        size = min(30, fit_size(label, SAFE_R - x0 - 50, 30, 400))
        parts.append(check_icon(x0, y - 27, INK, YELLOW, 32) + text(x0 + 48, y, label, size, INK, weight=400))
        y += 64
    parts.append(bottom_bar(BAR))
    return "".join(parts)


# --- Слайд 2: что в коробке ----------------------------------------------
def slide_inside(kit, uid):
    items = kit["items"]
    n = len(items)
    cols = 3 if n > 4 else 2
    rows = math.ceil(n / cols)
    gx, gy, area_w, area_h, top = 30, 30, SAFE_R - SAFE_L, 680, 320
    tw = (area_w - gx * (cols - 1)) / cols
    th = (area_h - gy * (rows - 1)) / rows
    parts = [f'<rect width="{W}" height="{H}" fill="{PAPER}"/>', decor(), header(f"{uid}h"), pill(kit["type"]),
             text(SAFE_L, 240, "ЧТО В КОРОБКЕ", 56, INK),
             text(SAFE_L, 288, kit["car"], 30, STEEL, weight=400)]
    for i, item in enumerate(items):
        cx = SAFE_L + (i % cols) * (tw + gx)
        cy = top + (i // cols) * (th + gy)
        icon_s = min(150, th - 150)
        parts.append(f'<rect x="{cx}" y="{cy}" width="{tw}" height="{th}" rx="24" fill="{WHITE}"/>')
        parts.append(place_icon(item["icon"], cx + tw / 2 - icon_s / 2, cy + 26, icon_s))
        ly = cy + 26 + icon_s + 42
        for line in wrap(item["name"], 28, tw - 40)[:2]:
            parts.append(text(cx + tw / 2, ly, line, 28, INK, anchor="middle"))
            ly += 34
        if item["qty"]:
            qw = text_width(item["qty"], 28) + 32
            parts.append(f'<rect x="{cx + tw - qw - 16}" y="{cy + 16}" width="{qw}" height="46" rx="23" fill="{YELLOW}"/>'
                         + text(cx + tw - qw / 2 - 16, cy + 49, item["qty"], 28, INK, anchor="middle"))
    parts.append(text(W / 2, 1044, "Бренды и артикулы — в описании · Любую деталь заменим на оригинал",
                      26, STEEL, weight=400, anchor="middle"))
    parts.append(bottom_bar(BAR))
    return "".join(parts)


# --- Слайд 3: гарантии (общий) -------------------------------------------
def slide_guarantees(uid="g"):
    promises = [("Всё в одной коробке", "до последнего болта и прокладки"),
                ("Не хватило детали?", "Довезём бесплатно, если ошибка наша"),
                ("Не подошло по подбору?", "Вернём деньги и оплатим возврат")]
    parts = [f'<rect width="{W}" height="{H}" fill="{INK}"/>', decor(), header(f"{uid}h", dark=True),
             text(SAFE_L, 250, "3 ГАРАНТИИ ZAPKIT", 56, PAPER),
             f'<g transform="translate({SAFE_L - 20} 450) scale(3.3)">{whale(YELLOW, INK, uid)}</g>']
    for i, (head, sub) in enumerate(promises):
        y = 400 + i * 190
        parts.append(f'<circle cx="676" cy="{y}" r="38" fill="{YELLOW}"/>'
                     + text(676, y + 15, str(i + 1), 42, INK, anchor="middle")
                     + text(740, y - 2, head, 40, PAPER)
                     + text(740, y + 44, sub, 30, STEEL_LIGHT, weight=400))
    parts.append(bottom_bar("Подбор по VIN — просто пришлите VIN в чат", bg=YELLOW, fg=INK))
    return "".join(parts)


# --- Слайд 4: как заказать (общий) ---------------------------------------
def vin_icon():
    return (f'<rect x="10" y="40" width="220" height="150" rx="16" fill="{WHITE}" stroke="{INK}" stroke-width="7"/>'
            f'<rect x="10" y="40" width="220" height="38" rx="16" fill="{YELLOW}"/>'
            f'<rect x="10" y="60" width="220" height="18" fill="{YELLOW}"/>'
            + text(40, 134, "VIN", 50, INK)
            + "".join(f'<rect x="40" y="{150 + i * 14}" width="{150 - i * 40}" height="6" rx="3" fill="{STEEL_LIGHT}"/>'
                      for i in range(2)))


def slide_how(uid="h"):
    cols = [(420, "Пришлите VIN", "17 символов из СТС"),
            (800, "Соберём кит", "и пришлём фото коробки"),
            (1180, "Отправим СДЭКом", "каждый вечер до 20:00")]
    parts = [f'<rect width="{W}" height="{H}" fill="{PAPER}"/>', decor(), header(f"{uid}h"),
             text(W / 2, 270, "КАК ЗАКАЗАТЬ", 56, INK, anchor="middle")]
    icons = [f'<g transform="translate({420 - 120} 380)">{vin_icon()}</g>',
             f'<g transform="translate({800 - 135} 370) scale(0.57)">{kraft_box(uid + "b", ("oil", "oil_filter"))}</g>',
             f'<g transform="translate({1180 - 128} 390) scale(2.45)">{whale(INK, PAPER, uid + "w")}</g>'
             f'<path d="M1060,640 q30,-18 60,0 t60,0 t60,0 t60,0" fill="none" stroke="{YELLOW}" stroke-width="10" stroke-linecap="round"/>']
    parts += icons
    for i, (cx, head, sub) in enumerate(cols):
        parts.append(f'<circle cx="{cx - 150}" cy="370" r="34" fill="{YELLOW}"/>'
                     + text(cx - 150, 385, str(i + 1), 40, INK, anchor="middle")
                     + text(cx, 740, head, 36, INK, anchor="middle")
                     + text(cx, 786, sub, 28, STEEL, weight=400, anchor="middle"))
    for ax in (590, 970):
        parts.append(f'<path d="M{ax},520 H{ax + 60} M{ax + 44},504 L{ax + 62},520 L{ax + 44},536" fill="none" '
                     f'stroke="{STEEL_LIGHT}" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/>')
    parts.append(text(W / 2, 930, "Нет вашей машины в списке? Пришлите VIN — рассчитаем кит", 30, STEEL, weight=400, anchor="middle"))
    parts.append(bottom_bar("Нажмите «Написать» — подберём кит под вашу машину"))
    return "".join(parts)


# --- Печать: карта ремонта (A6, 300 dpi) ---------------------------------
CW, CH = 1240, 1748  # A6 при 300 dpi


def qr(url, x, y, size):
    """QR-код ссылкой на видео (квадратики, без шрифтов и картинок)."""
    import segno
    rows = list(segno.make(url, error="m").matrix)
    n = len(rows) + 8  # поле по 4 модуля с каждой стороны
    m = size / n
    cells = "".join(f'<rect x="{x + (c + 4) * m:.2f}" y="{y + (r + 4) * m:.2f}" width="{m + 0.3:.2f}" height="{m + 0.3:.2f}"/>'
                    for r, row in enumerate(rows) for c, v in enumerate(row) if v)
    return f'<rect x="{x}" y="{y}" width="{size}" height="{size}" fill="{WHITE}"/><g fill="{INK}">{cells}</g>'


def repair_card_body(kit, uid):
    """Вкладыш в коробку. VIN и артикулы вписываются от руки; бренды — из kits.json.
    Если у кита есть ссылка на видео ("video" в kits.json) — печатается QR-код."""
    parts = [f'<rect width="{CW}" height="{CH}" fill="{WHITE}"/>',
             f'<rect width="{CW}" height="280" fill="{YELLOW}"/>',
             f'<g transform="translate(90 86) scale(1.18)">{lockup(INK, YELLOW, uid)}</g>',
             text(90, 390, kit["type"], 64, INK),
             text(90, 450, kit["car"], 42, INK, weight=400),
             text(90, 540, "VIN: ________________________", 34, INK, weight=400),
             text(90, 640, "Что в коробке:", 38, INK)]
    y = 700
    for item in kit["items"]:
        if item["icon"] == "card":
            continue
        parts.append(f'<rect x="90" y="{y}" width="46" height="46" rx="8" fill="none" stroke="{INK}" stroke-width="4"/>'
                     + text(160, y + 36, item_label(item), 34, INK))
        brand = item.get("brand")
        if item.get("in_kit"):
            line = "входит в комплект"
        elif brand and item.get("article"):
            line = f"{brand} · артикул {item['article']}"
        elif brand:
            line = f"{brand} · артикул: __________________"
        else:
            line = "бренд / артикул: ______________________"
        parts.append(text(160, y + 80, line, 26, STEEL, weight=400))
        y += 118
    qy = 1440
    tx = 90
    if kit.get("video"):
        parts.append(qr(kit["video"], 90, qy - 10, 250))
        tx = 380
        parts.append(text(tx, qy + 40, "Видео: как сделать эту работу", 32, INK))
    lines = [("Всё на месте? Оставьте отзыв на Авито —", "это очень помогает."),
             ("Чего-то не хватает? Напишите нам в чат", "Авито — довезём бесплатно.")]
    ly = qy + 110 if kit.get("video") else qy + 40
    for a, b in lines:
        parts.append(text(tx, ly, a, 27, INK, weight=400) + text(tx, ly + 36, b, 27, INK, weight=400))
        ly += 90
    return "".join(parts)


def repair_card(kit, uid):
    return svg(CW, CH, repair_card_body(kit, uid), f"ZAPKIT — карта ремонта: {kit['type']} {kit['car']}")


def repair_cards_a4(kit, uid):
    """4 одинаковые карты на листе A4 — печать дома, потом разрезать по линиям."""
    AW, AH = CW * 2, CH * 2
    parts = [f'<rect width="{AW}" height="{AH}" fill="{WHITE}"/>']
    for i in range(4):
        x, y = (i % 2) * CW, (i // 2) * CH
        parts.append(f'<svg x="{x}" y="{y}" width="{CW}" height="{CH}" viewBox="0 0 {CW} {CH}">'
                     f'{repair_card_body(kit, f"{uid}c{i}")}</svg>')
    parts.append(f'<path d="M{CW},0 V{AH} M0,{CH} H{AW}" stroke="{STEEL_LIGHT}" stroke-width="3" stroke-dasharray="14 12"/>')
    return svg(AW, AH, "".join(parts), f"ZAPKIT — карты ремонта A4: {kit['type']} {kit['car']}")


# --- Печать: лист наклеек A4 (300 dpi) -----------------------------------
def sticker_sheet():
    from build_brand import sticker
    AW, AH, D = 2480, 3508, 700
    xs, ys = (95, 890, 1685), (141, 982, 1823, 2664)
    parts = [f'<rect width="{AW}" height="{AH}" fill="{WHITE}"/>']
    for j, y in enumerate(ys):
        for i, x in enumerate(xs):
            parts.append(f'<circle cx="{x + D / 2}" cy="{y + D / 2}" r="{D / 2 + 8}" fill="none" '
                         f'stroke="{STEEL_LIGHT}" stroke-width="3" stroke-dasharray="12 10"/>'
                         f'<g transform="translate({x} {y}) scale({D / 400})">{sticker(f"s{j}{i}")}</g>')
    parts.append(text(AW / 2, 3460, "Печать: А4, масштаб 100%. Вырезать по пунктиру и приклеить на коробку.",
                      34, STEEL, weight=400, anchor="middle"))
    return svg(AW, AH, "".join(parts), "ZAPKIT — наклейки A4")


# --- Макет магазина на телефоне ------------------------------------------
def card_thumb(kit, uid, x, y, s):
    """Квадратное превью главной карточки — так её обрежет лента Авито."""
    return (f'<clipPath id="tc-{uid}"><rect x="{x}" y="{y}" width="{s}" height="{s}" rx="12"/></clipPath>'
            f'<g clip-path="url(#tc-{uid})"><svg x="{x}" y="{y}" width="{s}" height="{s}" viewBox="200 0 1200 1200">'
            f'{slide_main(kit, uid)}</svg></g>')


def plain_thumb(icons, x, y, s, uid):
    """Превью «обычного» конкурента: серый фон и деталь без оформления."""
    inner = "".join(place_icon(n, x + 24 + k * (s - 48) / len(icons), y + s / 2 - 50, 100 * min(1, 2 / len(icons)))
                    for k, n in enumerate(icons))
    return (f'<clipPath id="pc-{uid}"><rect x="{x}" y="{y}" width="{s}" height="{s}" rx="12"/></clipPath>'
            f'<g clip-path="url(#pc-{uid})"><rect x="{x}" y="{y}" width="{s}" height="{s}" fill="#ECECEC"/>'
            f'<g opacity="0.85">{inner}</g></g>')


def tile(thumb, title, price, x, y, s=169, note=None):
    lines = wrap(title, 13, s, 400)[:2]
    out = thumb + "".join(text(x, y + s + 20 + k * 17, ln, 13, INK, weight=400) for k, ln in enumerate(lines))
    out += text(x, y + s + 64, price, 16, INK)
    if note:
        out += text(x, y + s + 82, note, 11, STEEL, weight=400)
    return out


def phone(screen, uid):
    return (f'<rect width="420" height="880" rx="58" fill="{INK}"/>'
            f'<clipPath id="ph-{uid}"><rect x="15" y="18" width="390" height="844" rx="44"/></clipPath>'
            f'<g clip-path="url(#ph-{uid})"><rect x="15" y="18" width="390" height="844" fill="{WHITE}"/>'
            f'<g transform="translate(15 18)">{screen}</g></g>'
            f'<rect x="160" y="30" width="100" height="26" rx="13" fill="{INK}"/>')


def status_bar():
    return (text(28, 40, "9:41", 15, INK)
            + f'<rect x="318" y="28" width="26" height="13" rx="3" fill="none" stroke="{INK}" stroke-width="1.6"/>'
            + f'<rect x="320" y="30" width="18" height="9" rx="1.5" fill="{INK}"/>')


def store_screen(kits):
    s = [status_bar(), text(20, 84, "‹", 30, INK, weight=400), text(195, 82, "Магазин", 17, INK, anchor="middle"),
         f'<clipPath id="avc"><circle cx="58" cy="148" r="38"/></clipPath>'
         f'<g clip-path="url(#avc)"><rect x="20" y="110" width="76" height="76" fill="{YELLOW}"/>'
         f'<g transform="translate(20 110) scale(0.76) translate(50 52) scale(0.8) translate(-55 -52)">'
         f'{whale(INK, YELLOW, "avs")}</g></g>',
         text(110, 136, "ZAPKIT — запчасти наборами", 17, INK),
         text(110, 160, "Магазин · СДЭК каждый вечер", 13, STEEL, weight=400),
         text(110, 182, "Пока нет отзывов", 13, STEEL, weight=400),
         f'<rect x="20" y="202" width="350" height="44" rx="12" fill="{INK}"/>',
         text(195, 230, "Написать", 16, PAPER, anchor="middle")]
    for k, ln in enumerate(["Наборы запчастей под конкретный ремонт:",
                            "всё до последнего болта в одной коробке.",
                            "Подбор по VIN с гарантией."]):
        s.append(text(20, 276 + k * 19, ln, 13, INK, weight=400))
    cx = 20
    for chip in ("Все", "ТО-киты", "ГРМ-киты", "Корея", "Китай"):
        w = text_width(chip, 13, 400) + 24
        on = chip == "Все"
        s.append(f'<rect x="{cx}" y="336" width="{w}" height="30" rx="15" fill="{INK if on else "#F1F1F1"}"/>'
                 + text(cx + w / 2, 356, chip, 13, PAPER if on else INK, weight=400, anchor="middle"))
        cx += w + 8
    for i, kit in enumerate(kits[:4]):
        x = 20 + (i % 2) * 181
        y = 384 + (i // 2) * 262
        s.append(tile(card_thumb(kit, f"st{i}", x, y, 169), kit["title"], MOCKUP_KITS.get(kit["id"], ""), x, y))
    return "".join(s)


def search_screen(kit):
    s = [status_bar(),
         f'<rect x="16" y="58" width="358" height="44" rx="12" fill="#F1F1F1"/>',
         f'<circle cx="40" cy="78" r="8" fill="none" stroke="{STEEL}" stroke-width="2.4"/>'
         f'<path d="M46,84 L52,90" stroke="{STEEL}" stroke-width="2.4" stroke-linecap="round"/>',
         text(62, 86, "то солярис", 16, INK, weight=400)]
    cx = 16
    for chip in ("Запчасти", "С доставкой", "Цена"):
        w = text_width(chip, 13, 400) + 24
        s.append(f'<rect x="{cx}" y="116" width="{w}" height="30" rx="15" fill="#F1F1F1"/>'
                 + text(cx + w / 2, 136, chip, 13, INK, weight=400, anchor="middle"))
        cx += w + 8
    tiles = [
        (card_thumb(kit, "ss0", 20, 164, 169), kit["title"], MOCKUP_KITS.get(kit["id"], ""), "Всё в одной коробке"),
        (plain_thumb(["oil_filter"], 201, 164, 169, "p1"), "Фильтр масляный Солярис", "690 ₽", None),
        (plain_thumb(["oil"], 20, 426, 169, "p2"), "Масло моторное 4 л", "3 290 ₽", None),
        (plain_thumb(["oil_filter", "air_filter"], 201, 426, 169, "p3"), "Комплект ТО Солярис, фильтры", "1 490 ₽", None),
    ]
    for i, (thumb, title, price, note) in enumerate(tiles):
        x = 20 + (i % 2) * 181
        y = 164 + (i // 2) * 262
        s.append(tile(thumb, title, price, x, y, note=note))
    return "".join(s)


# Витрина макета и условные цены (только для картинки; реальные цены — в avito/zapkit-zakupka.xlsx)
MOCKUP_KITS = {"to-01-solaris-2010": "4 990 ₽", "grm-12-coolray": "10 790 ₽",
               "to-07-jolion": "6 890 ₽", "grm-06-polo-cwva": "6 290 ₽"}


def store_mockup(kits):
    by_id = {k["id"]: k for k in kits}
    showcase = [by_id[i] for i in MOCKUP_KITS]
    MW, MH = 1800, 1420
    parts = [f'<rect width="{MW}" height="{MH}" fill="{PAPER}"/>',
             text(100, 90, "Так будет выглядеть ZAPKIT на Авито", 44, INK),
             text(100, 134, "Макет: интерфейс упрощён, цены условные", 24, STEEL, weight=400),
             text(100 + 273, 214, "Страница магазина", 26, INK, anchor="middle"),
             text(1000 + 273, 214, "Поиск «то солярис»: вас видно среди обычных объявлений", 26, INK,
                  anchor="middle"),
             f'<g transform="translate(100 240) scale(1.3)">{phone(store_screen(showcase), "a")}</g>',
             f'<g transform="translate(1000 240) scale(1.3)">{phone(search_screen(by_id["to-01-solaris-2010"]), "b")}</g>']
    return svg(MW, MH, "".join(parts), "ZAPKIT — макет магазина на Авито")


# --- Схема: путь клиента до заказа в работе --------------------------------
LOOP = [  # (этап, срок, что делаем, если что-то пошло не так) — как в docs/avito/client-loop.md
    ("Клиент написал", "до 5 минут", "Здороваемся и просим VIN (звонок — тоже)",
     "Работаем 9:00–20:00. В остальное время — автоответ, утром до 10:00"),
    ("Ждём VIN", "через 3 ч и завтра", "Напоминаем, если молчит — не больше 2 раз", "Нет ответа → «Отказ: не ответил»"),
    ("Подбор по VIN", "до 30 минут", "Проверяем каждую деталь, наличие и срок у поставщика",
     "Чего-то нет → предлагаем замену"),
    ("Предложение", "цена держится 24 ч", "Состав с брендами, цена, дата отправки, как оплатить",
     "«Дорого» → другой бренд или без масла"),
    ("Думает", "завтра и через 3 дня", "Два коротких напоминания, не больше", "Молчит → «Отказ» с причиной"),
    ("Оплата", "проверяем в банке", "Авито Доставка или перевод (СДЭК или самовывоз в Сочи)",
     "Скриншот — не оплата. Деньги пришли → шаг 7"),
    ("В обработке", "сразу после оплаты", "Заказываем детали до отсечки, пишем дату отправки",
     "Дальше: сборка → фото коробки → СДЭК до 20:00 или самовывоз"),
]


LOOP_ENTRY = "Купил сразу, без переписки → всё равно просим VIN и перепроверяем → шаг 3"

# --- Схема: путь заказа от «В обработке» до отзыва и следующего ТО ------------
ORDER_LOOP = [  # как в docs/avito/order-loop.md
    ("Детали у нас", "в день поставки", "Забираем у поставщика, сверяем артикулы, количество и целость",
     "Не то или брак → меняем у поставщика сразу, клиенту — честно о сроке"),
    ("Собран", "в тот же день", "Тяжёлое вниз, канистру в пакет, карта ремонта с VIN сверху",
     "Фото открытой коробки — клиенту в чат до отправки"),
    ("Отправлен", "до 20:00", "Сдаём в СДЭК, трек-номер клиенту в течение часа",
     "Самовывоз: встреча в Сочи с 9:00 до 20:00"),
    ("Получен", "следим за треком", "Пишем, когда посылка в пункте, напоминаем про срок хранения",
     "Спрашиваем пробег в месяц — для напоминания о ТО"),
    ("Закрыт", "на следующий день", "Спасибо и одна просьба об отзыве", "Отвечаем на каждый отзыв, даже плохой"),
]
ORDER_ENTRY = "Начало — шаг 7: оплачено, детали заказаны у поставщика до отсечки"
ORDER_AFTER = [
    ("Проблема: не хватило, не подошло, брак → довезём, заменим или вернём деньги", STEEL),
    ("За 2 недели до следующего ТО → напоминаем → снова шаг 1, уже как постоянный клиент", YELLOW),
]


def process_diagram(uid, title, subtitle, entry, stages, first_no, footer, after=()):
    """Вертикальная схема этапов: карточки с номером, сроком, действием и «если что-то пошло не так»."""
    LW, x0, cw, ch, gap, band = 1200, 60, 1080, 150, 22, 64
    top = 350
    stages_h = len(stages) * (ch + gap)
    LH = top + stages_h + len(after) * (band + 18) + 110
    parts = [f'<rect width="{LW}" height="{LH}" fill="{PAPER}"/>',
             f'<g transform="translate({x0} 50) scale(0.62)">{lockup(INK, YELLOW, uid)}</g>',
             text(x0, 190, title, 56, INK),
             text(x0, 234, subtitle, 28, STEEL, weight=400),
             f'<rect x="{x0}" y="262" width="{cw}" height="{band}" rx="18" fill="none" stroke="{YELLOW}" stroke-width="4"/>',
             text(x0 + 24, 303, entry, fit_size(entry, cw - 48, 25, 400), INK, weight=400)]
    bx = x0 + 64
    parts.append(f'<line x1="{bx}" y1="{top + ch / 2}" x2="{bx}" y2="{top + (len(stages) - 1) * (ch + gap) + ch / 2}" '
                 f'stroke="{STEEL_LIGHT}" stroke-width="6"/>')
    for i, (name, sla, action, branch) in enumerate(stages):
        y = top + i * (ch + gap)
        last = i == len(stages) - 1
        bg, fg, sub = (INK, PAPER, STEEL_LIGHT) if last else (WHITE, INK, STEEL)
        parts.append(f'<rect x="{x0}" y="{y}" width="{cw}" height="{ch}" rx="24" fill="{bg}"/>')
        parts.append(f'<circle cx="{bx}" cy="{y + ch / 2}" r="34" fill="{YELLOW}"/>'
                     + text(bx, y + ch / 2 + 12, str(first_no + i), 34 if first_no + i < 10 else 30, INK,
                            anchor="middle"))
        pw = text_width(sla, 22) + 36
        parts.append(f'<rect x="{x0 + cw - pw - 24}" y="{y + 22}" width="{pw}" height="42" rx="21" '
                     f'fill="{YELLOW if last else INK}"/>'
                     + text(x0 + cw - pw / 2 - 24, y + 50, sla, 22, INK if last else YELLOW, anchor="middle"))
        tx = x0 + 130
        parts.append(text(tx, y + 56, name, 34, fg))
        parts.append(text(tx, y + 96, action, fit_size(action, cw - 160, 25, 400), fg, weight=400))
        parts.append(text(tx, y + 130, branch, fit_size(branch, cw - 160, 22, 400), sub, weight=400))
    y = top + stages_h
    for label, color in after:
        parts.append(f'<rect x="{x0}" y="{y}" width="{cw}" height="{band}" rx="18" fill="none" '
                     f'stroke="{color}" stroke-width="4"/>'
                     + text(x0 + 24, y + 41, label, fit_size(label, cw - 48, 25, 400), INK, weight=400))
        y += band + 18
    parts.append(text(LW / 2, LH - 50, footer, 24, STEEL, weight=400, anchor="middle"))
    return svg(LW, LH, "".join(parts), f"ZAPKIT — {title.lower()}")


def process_loop():
    return process_diagram("pl", "ПУТЬ КЛИЕНТА", "от первого сообщения до заказа в работе", LOOP_ENTRY, LOOP, 1,
                           "Статусы 1–7 — те же, что на листе «Заявки» в таблице закупки")


def order_loop():
    return process_diagram("ol", "ПУТЬ ЗАКАЗА", "от «В обработке» до отзыва и следующего ТО", ORDER_ENTRY,
                           ORDER_LOOP, 8, "Статусы 8–12 и «Проблема» — те же, что на листе «Заявки»", ORDER_AFTER)


def build():
    kits = json.loads((ROOT / "avito" / "kits.json").read_text(encoding="utf-8"))["kits"]
    OUT.mkdir(parents=True, exist_ok=True)
    for old in OUT.glob("*.svg"):
        old.unlink()
    files = {}
    for n, kit in enumerate(kits, 1):
        files[f"{kit['id']}-1-main.svg"] = svg(W, H, slide_main(kit, f"m{n}"),
                                                            f"{kit['type']} {kit['car']}")
        files[f"{kit['id']}-2-inside.svg"] = svg(W, H, slide_inside(kit, f"i{n}"),
                                                              f"Что в коробке: {kit['type']} {kit['car']}")
        files[f"print-repair-card-{kit['id']}.svg"] = repair_card(kit, f"r{n}")
        if kit.get("price"):  # кит собран — готовим лист A4 на 4 карты
            files[f"print-repair-cards-a4-{kit['id']}.svg"] = repair_cards_a4(kit, f"a{n}")
    files["common-3-guarantees.svg"] = svg(W, H, slide_guarantees(), "3 гарантии ZAPKIT")
    files["common-4-how-to-order.svg"] = svg(W, H, slide_how(), "Как заказать в ZAPKIT")
    files["print-stickers-a4.svg"] = sticker_sheet()
    files["mockup-avito-store.svg"] = store_mockup(kits)
    files["process-client-loop.svg"] = process_loop()
    files["process-order-loop.svg"] = order_loop()
    for name, content in files.items():
        (OUT / name).write_text(content, encoding="utf-8")
        print("written", OUT / name)


if __name__ == "__main__":
    build()
