"""Рабочая таблица закупки ZAPKIT → avito/zapkit-zakupka.xlsx

Берёт список китов из avito/kits.json и раскладывает каждый кит на закупочные
позиции. Цены у поставщиков заполняются вручную, остальное считают формулы.

Запуск:  python3 avito/tools/build_sheet.py [--force]   (--force перезапишет файл с ценами)
Затем пересчитать формулы (LibreOffice), см. brand/README.md.
"""

import json
import sys
from pathlib import Path

from openpyxl import Workbook
from openpyxl.comments import Comment
from openpyxl.formatting.rule import CellIsRule
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "avito" / "zapkit-zakupka.xlsx"

SUPPLIERS = ["Фаворит", "Микадо", "Профит Лига", "Росско", "Автосоюз",
             "Автоспутник", "Автоформула", "Армтек", "Автотрейд"]
CHINESE = ("Haval", "Chery", "Geely")

FONT = "Arial"
HEAD_FILL = PatternFill("solid", fgColor="14161A")
INPUT_FILL = PatternFill("solid", fgColor="FFF4C2")
EXAMPLE_FILL = PatternFill("solid", fgColor="F2F2F2")
thin = Side(style="thin", color="D9D9D9")
BORDER = Border(left=thin, right=thin, top=thin, bottom=thin)
RUB = '#,##0" ₽";-#,##0" ₽";"-"'


def f(bold=False, color="000000", italic=False, size=10):
    return Font(name=FONT, bold=bold, color=color, italic=italic, size=size)


def header(ws, row, titles, widths):
    for col, (t, w) in enumerate(zip(titles, widths), 1):
        c = ws.cell(row=row, column=col, value=t)
        c.font = f(bold=True, color="FFFFFF")
        c.fill = HEAD_FILL
        c.alignment = Alignment(wrap_text=True, vertical="center")
        c.border = BORDER
        ws.column_dimensions[get_column_letter(col)].width = w
    ws.row_dimensions[row].height = 32


def cell(ws, row, col, value, *, inp=False, fmt=None, bold=False, italic=False, color=None, wrap=False):
    c = ws.cell(row=row, column=col, value=value)
    c.font = f(bold=bold, italic=italic, color=color or ("0000FF" if inp else "000000"))
    if inp:
        c.fill = INPUT_FILL
    if fmt:
        c.number_format = fmt
    c.border = BORDER
    c.alignment = Alignment(wrap_text=wrap, vertical="top")
    return c


def buy_rows(kit):
    """Закупочные позиции кита: (позиция, кол-во, комментарий)."""
    chinese = kit["car"].startswith(CHINESE)
    if kit["kind"] == "to":
        rows = [("Масло моторное 4 л", 1, "Вязкость и допуск — по мануалу автомобиля")]
        if chinese:
            rows.append(("Масло моторное 1 л (если объём > 4 л)", 0,
                         "Поставьте 1, если объём заливки с фильтром больше 4 л (проверьте по VIN)"))
        rows += [("Фильтр масляный", 1, ""), ("Фильтр воздушный", 1, ""), ("Фильтр салонный", 1, ""),
                 ("Шайба (прокладка) сливной пробки", 1, "")]
        return rows
    optional = [("Помпа водяная (если потребуется)", 0, "Поставьте 1, если помпу меняют вместе с ГРМ"),
                ("Масляный насос (если потребуется)", 0, "Поставьте 1, если требуется по каталогу / по состоянию")]
    if kit["drive"] == "цепь":
        return [("Комплект цепи ГРМ (цепь, натяжитель, успокоители)", 1,
                 "Если готового комплекта нет — добавьте строки и купите позиции отдельно"),
                ("Сальник коленвала передний", 1, ""), ("Герметик", 1, "")] + optional
    rows = [("Комплект ремня ГРМ (ремень, натяжной ролик)", 1, "")]
    if "помпы" in kit["drive"]:
        rows.append(("Ремень привода помпы", 1, "По регламенту меняется вместе с ремнём ГРМ"))
    return rows + optional


def build():
    if OUT.exists() and "--force" not in sys.argv:
        sys.exit(f"{OUT} уже есть — в нём могут быть ваши цены. Чтобы создать заново, запустите с --force.")
    kits = json.loads((ROOT / "avito" / "kits.json").read_text(encoding="utf-8"))["kits"]
    wb = Workbook()

    # --- Инструкция -------------------------------------------------------
    ws = wb.active
    ws.title = "Инструкция"
    ws.column_dimensions["A"].width = 110
    lines = [
        ("ZAPKIT — таблица закупки и цен", True),
        ("", False),
        ("Как пользоваться:", True),
        ("1. «Поставщики» — заполните условия каждого поставщика: склад в Сочи/Адлере, отсечка, срок, возврат.", False),
        ("2. «Состав» — для каждой позиции подберите по VIN/каталогу бренд и артикул и впишите цены у тех поставщиков, где она есть.", False),
        ("    Лучшая цена, поставщик и сумма посчитаются сами. Кол-во 0 = позиция не входит (например, помпа); поставьте 1, если нужна.", False),
        ("3. «Киты» — сами посчитаются закупка, цена на Авито и прибыль. Впишите минимальную цену конкурентов — появится сравнение.", False),
        ("4. «Параметры» — наценка, упаковка, комиссия Авито. Поменяете там — пересчитается всё.", False),
        ("5. «Моторы» — справка: где цепь, где ремень, что входит в ГРМ-кит, источники.", False),
        ("", False),
        ("Обозначения:", True),
        ("Жёлтая заливка и синий текст — ячейки, которые заполняете вы.", False),
        ("Чёрный текст без заливки — формулы, их не трогайте.", False),
        ("Серая строка «ПРИМЕР» на листах — образец заполнения, её можно удалить.", False),
    ]
    for i, (t, b) in enumerate(lines, 1):
        c = ws.cell(row=i, column=1, value=t)
        c.font = f(bold=b, size=14 if i == 1 else 10)
    ws.cell(row=12, column=1).fill = INPUT_FILL
    ws.cell(row=12, column=1).font = f(color="0000FF")

    # --- Параметры -------------------------------------------------------
    wp = wb.create_sheet("Параметры")
    header(wp, 1, ["Параметр", "Значение", "Пояснение / источник"], [38, 14, 90])
    params = [
        ("Наценка к закупке", 0.30, "0.0%", "Цена кита = закупка × (1 + наценка), вверх до шага округления, минус «вычесть». Ваше решение, можно менять."),
        ("Упаковка на 1 кит, ₽", 50, RUB, "Коробка, наклейка, печать карты ремонта — оценка; уточните по факту."),
        ("Шаг округления цены, ₽", 100, RUB, "Цена округляется вверх до этого шага."),
        ("Вычесть из округлённой цены, ₽", 10, RUB, "Чтобы цена заканчивалась на …90 (4 700 → 4 690)."),
        ("Комиссия Авито Доставки", 0.065, "0.0%", "≈6,5% для профессиональных продавцов по данным селлерских сервисов (SelSup, 2026). Сверьте ставку в кабинете Авито."),
        ("Расход на просмотры на 1 заказ, ₽", 180, RUB, "Оценка: ≈150 просмотров × 1,2 ₽. После запуска замените на своё значение из статистики Авито."),
    ]
    for i, (name, val, fmt, note) in enumerate(params, 2):
        cell(wp, i, 1, name)
        cell(wp, i, 2, val, inp=True, fmt=fmt)
        cell(wp, i, 3, note, wrap=True)
    # адреса параметров
    P_MARKUP, P_PACK, P_STEP, P_MINUS, P_FEE, P_VIEWS = (f"Параметры!$B${r}" for r in range(2, 8))

    # --- Киты ------------------------------------------------------------
    wk = wb.create_sheet("Киты")
    header(wk, 1, ["Кит", "Вид", "Машина", "Мотор", "Привод ГРМ", "Приоритет", "Заголовок для Авито",
                   "Главное фото (avito/png/…)", "Закупка, ₽", "Позиций без цены", "Цена на Авито, ₽",
                   "Мин. цена конкурентов, ₽", "Сравнение с рынком", "Прибыль с кита, ₽", "Маржа", "Статус"],
           [9, 8, 30, 15, 13, 11, 50, 34, 12, 11, 13, 14, 18, 13, 9, 14])
    for i, k in enumerate(kits, 2):
        cell(wk, i, 1, k["sku"], bold=True)
        cell(wk, i, 2, "ТО" if k["kind"] == "to" else "ГРМ")
        cell(wk, i, 3, k["car"])
        cell(wk, i, 4, k["engine"])
        cell(wk, i, 5, k["drive"])
        cell(wk, i, 6, k["priority"])
        cell(wk, i, 7, k["title"], wrap=True)
        cell(wk, i, 8, f'{k["id"]}-1-main.png')
        s = f'SUMIFS(Состав!$R:$R,Состав!$A:$A,A{i})'
        cell(wk, i, 9, f'=IF({s}=0,"",{s}+{P_PACK})', fmt=RUB)
        cell(wk, i, 10, f'=COUNTIFS(Состав!$A:$A,A{i},Состав!$P:$P,"",Состав!$D:$D,">0")')
        cell(wk, i, 11, f'=IF(I{i}="","",CEILING(I{i}*(1+{P_MARKUP}),{P_STEP})-{P_MINUS})', fmt=RUB, bold=True)
        cell(wk, i, 12, None, inp=True, fmt=RUB)
        cell(wk, i, 13, f'=IF(OR(K{i}="",L{i}=""),"",IF(K{i}<=L{i},"не дороже рынка","дороже рынка"))')
        cell(wk, i, 14, f'=IF(K{i}="","",K{i}-I{i}-K{i}*{P_FEE}-{P_VIEWS})', fmt=RUB)
        cell(wk, i, 15, f'=IF(N{i}="","",N{i}/K{i})', fmt="0.0%")
        cell(wk, i, 16, "не выложен", inp=True)
    last_k = len(kits) + 1
    dv = DataValidation(type="list", formula1='"не выложен,выложен,есть продажи,снят"', allow_blank=True)
    wk.add_data_validation(dv)
    dv.add(f"P2:P{last_k}")
    wk.conditional_formatting.add(f"J2:J{last_k}", CellIsRule(operator="greaterThan", formula=["0"],
                                                               fill=PatternFill("solid", fgColor="FCE4D6")))
    wk.conditional_formatting.add(f"M2:M{last_k}", CellIsRule(operator="equal", formula=['"дороже рынка"'],
                                                               font=Font(name=FONT, color="C00000")))
    wk.freeze_panes = "D2"
    wk["J1"].comment = Comment("Сколько позиций с кол-вом > 0 ещё без цены. 0 — кит полностью посчитан.", "ZAPKIT")
    wk["N1"].comment = Comment("Прибыль до налога: цена − закупка − комиссия Авито − просмотры (см. «Параметры»).", "ZAPKIT")

    # --- Состав ----------------------------------------------------------
    wc = wb.create_sheet("Состав")
    sup_first, sup_last = 7, 6 + len(SUPPLIERS)            # G..O
    L_first, L_last = get_column_letter(sup_first), get_column_letter(sup_last)
    header(wc, 1, ["Кит", "Машина", "Позиция", "Кол-во", "Бренд", "Артикул"] + SUPPLIERS
           + ["Лучшая цена, ₽", "У кого", "Сумма, ₽", "Комментарий"],
           [9, 26, 44, 8, 14, 16] + [11] * len(SUPPLIERS) + [12, 13, 12, 60])
    wc.row_dimensions[1].height = 44

    def item_row(r, sku, pos, qty, note, example=None):
        ex = example is not None
        cell(wc, r, 1, sku, bold=not ex, italic=ex, color="8C929B" if ex else None)
        car = "образец заполнения — строку можно удалить" if ex else \
            f'=IFERROR(INDEX(Киты!$C:$C,MATCH(A{r},Киты!$A:$A,0)),"")'
        cell(wc, r, 2, car, italic=ex, color="8C929B" if ex else None)
        cell(wc, r, 3, pos)
        cell(wc, r, 4, qty, inp=True)
        cell(wc, r, 5, example["brand"] if ex else None, inp=True)
        cell(wc, r, 6, example["art"] if ex else None, inp=True)
        for j in range(len(SUPPLIERS)):
            v = example["prices"][j] if ex else None
            cell(wc, r, sup_first + j, v, inp=True, fmt=RUB)
        rng = f"{L_first}{r}:{L_last}{r}"
        cell(wc, r, sup_last + 1, f'=IF(COUNT({rng})=0,"",MIN({rng}))', fmt=RUB)
        cell(wc, r, sup_last + 2,
             f'=IF({get_column_letter(sup_last + 1)}{r}="","",INDEX(${L_first}$1:${L_last}$1,'
             f'MATCH({get_column_letter(sup_last + 1)}{r},{rng},0)))')
        cell(wc, r, sup_last + 3,
             f'=IF({get_column_letter(sup_last + 1)}{r}="",0,{get_column_letter(sup_last + 1)}{r}*D{r})', fmt=RUB)
        cell(wc, r, sup_last + 4, note, wrap=True)
        if ex:
            for col in range(1, sup_last + 5):
                wc.cell(row=r, column=col).fill = EXAMPLE_FILL

    item_row(2, "ПРИМЕР", "Фильтр масляный", 1, "Цены — у тех поставщиков, где позиция есть; пустые ячейки не учитываются",
             example={"brand": "Бренд А", "art": "ABC-123",
                      "prices": [460, None, 445, 430, None, None, None, 470, None]})
    r = 3
    for k in kits:
        for pos, qty, note in buy_rows(k):
            item_row(r, k["sku"], pos, qty, note)
            r += 1
    wc.freeze_panes = "D2"
    assert get_column_letter(sup_last + 3) == "R", "SUMIFS на листе «Киты» ссылается на колонку R"
    assert get_column_letter(sup_last + 1) == "P", "COUNTIFS на листе «Киты» ссылается на колонку P"

    # --- Поставщики -------------------------------------------------------
    wsu = wb.create_sheet("Поставщики")
    header(wsu, 1, ["Поставщик", "Статус", "Склад / пункт выдачи в Сочи или Адлере", "Отсечка заказа (до …)",
                    "Срок до вас, дней", "Доставка до вас", "Возврат «не подошло» (срок, удержание)",
                    "Отсрочка платежа", "Прайс / API", "Менеджер (имя, телефон)", "Комментарий"],
           [16, 14, 24, 14, 11, 20, 24, 16, 14, 24, 40])
    example = ["ПРИМЕР", "подключён", "да, Адлер", "12:00", 1, "бесплатно от 3 000 ₽", "14 дней, без удержания",
               "после 3 мес., 14 дней", "API", "Иван, +7 …", "образец заполнения — строку можно удалить"]
    for col, v in enumerate(example, 1):
        c = cell(wsu, 2, col, v, italic=True, color="8C929B")
        c.fill = EXAMPLE_FILL
    for i, name in enumerate(SUPPLIERS, 3):
        cell(wsu, i, 1, name, bold=True)
        cell(wsu, i, 2, "в процессе" if name == "Автоформула" else "подключён", inp=True)
        for col in range(3, 12):
            cell(wsu, i, col, None, inp=True, wrap=True)
    dv2 = DataValidation(type="list", formula1='"подключён,в процессе,нет"', allow_blank=True)
    wsu.add_data_validation(dv2)
    dv2.add(f"B3:B{2 + len(SUPPLIERS)}")
    wsu.freeze_panes = "B2"

    # --- Моторы (справка) -----------------------------------------------
    wm = wb.create_sheet("Моторы")
    header(wm, 1, ["Машина", "Годы", "Мотор", "Привод ГРМ", "Что берём в ГРМ-кит", "Масло (объём)", "Источник / уверенность"],
           [30, 12, 26, 22, 52, 30, 70])
    chain_kit = "Комплект цепи (цепь, натяжитель, успокоители), сальник коленвала, герметик; помпа и маслонасос — если требуется"
    motors = [
        ("Hyundai Solaris / Kia Rio", "2010–2017", "G4FA 1.4 / G4FC 1.6 (Gamma)", "цепь", chain_kit,
         "≈3,3 л — хватает канистры 4 л; проверьте по VIN", "Данные каталогов производителя. Проверяйте по VIN в каталоге поставщика."),
        ("Hyundai Solaris / Kia Rio", "2017–2022", "G4LC 1.4 (Kappa) / G4FG 1.6 (Gamma II)", "цепь", chain_kit,
         "до 4 л — проверьте по VIN", "Данные каталогов производителя. Проверяйте по VIN."),
        ("VW Polo седан", "2010–2015", "CFNA / CFNB 1.6", "цепь", chain_kit,
         "≈3,6 л — проверьте по VIN", "Данные каталогов производителя. Проверяйте по VIN."),
        ("VW Polo седан / лифтбек", "2015+", "CWVA / CWVB 1.6", "ремень",
         "Комплект ремня (ремень, натяжной ролик); помпа — по желанию", "≈3,6 л — проверьте по VIN",
         "Данные каталогов производителя. Проверяйте по VIN."),
        ("Haval Jolion", "2021+", "GW4B15A 1.5T", "цепь", chain_kit, "уточните по VIN (может быть > 4 л)",
         "Цепь: drive2.ru/l/726006979138433863, bus-tech.ru (замена цепи Jolion 1.5T)"),
        ("Haval F7 / F7x", "2019+", "GW4B15 1.5T / GW4C20 2.0T", "цепь", chain_kit, "уточните по VIN (может быть > 4 л)",
         "Цепь; у 1.5T внимания требует к 100–120 тыс. км, у 2.0T часто 150+ тыс. км: bus-tech.ru/haval1/remont-f7/zamena-tsepi-grm-f7-f7x"),
        ("Chery Tiggo 7 Pro / 4 Pro", "2020+", "SQRE4T15C 1.5T", "цепь", chain_kit, "уточните по VIN (может быть > 4 л)",
         "Цепь; ресурс часто 200+ тыс. км, поэтому ГРМ-кит — «позже». Комплекты Gates под SQRE4T15C продаются на Яндекс Маркете"),
        ("Geely Coolray", "2020+", "JLH-3G15TD 1.5T", "ремень + ремень помпы",
         "Ремень ГРМ, натяжной ролик, ремень привода помпы (по регламенту меняют вместе); помпа — если требуется",
         "уточните по VIN (может быть > 4 л)",
         "Ремень; регламент 100–120 тыс. км или 5–6 лет, на практике ≈80 тыс.: motorhunter.ru/engine/geely/jlh-3g15td/, avtogermes.ru"),
    ]
    for i, row in enumerate(motors, 2):
        for col, v in enumerate(row, 1):
            cell(wm, i, col, v, wrap=True)
    wm.freeze_panes = "B2"

    for sheet in wb.worksheets:
        sheet.sheet_view.zoomScale = 110
    wb.move_sheet("Киты", offset=-1)  # Инструкция, Киты, Параметры, …
    wb.save(OUT)
    print("written", OUT, "rows:", r - 1)


if __name__ == "__main__":
    build()
