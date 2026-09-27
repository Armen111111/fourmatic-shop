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


TO_ROWS = {  # иконка позиции кита → строка закупки
    "oil": "Масло моторное 4 л",
    "oil_filter": "Фильтр масляный",
    "air_filter": "Фильтр воздушный",
    "cabin_filter": "Фильтр салонный",
    "washer": "Шайба (прокладка) сливной пробки",
}


def rub(v):
    return f"{v:,.2f}".replace(",", " ").replace(".", ",")


def buy_rows(kit):
    """Закупочные позиции кита: (позиция, кол-во, комментарий, бренд, артикул).

    ТО-кит и собранные ГРМ- и тормоз-киты раскладываются ровно по своему составу из kits.json — ничего не добавляем.
    """
    chinese = kit["car"].startswith(CHINESE)
    if kit["kind"] == "to":
        rows = []
        for it in kit["items"]:
            if it["icon"] not in TO_ROWS:
                continue
            notes = [it["note"]] if it.get("note") else []
            if it.get("buy_price") is not None:
                notes.insert(0, f"Ваша закупка: {rub(it['buy_price'])} ₽ — впишите в колонку поставщика, у которого брали")
            if it["icon"] == "oil" and not notes:
                notes.append("Вязкость и допуск — по мануалу автомобиля")
            rows.append((TO_ROWS[it["icon"]], 1, ". ".join(notes), it.get("brand"), it.get("article")))
            if it["icon"] == "oil" and chinese:
                rows.append(("Масло моторное 1 л (если объём > 4 л)", 0,
                             "Поставьте 1, если объём заливки с фильтром больше 4 л (проверьте по VIN)", None, None))
        return rows
    optional = [("Помпа водяная (если потребуется)", 0, "Поставьте 1, если помпу меняют вместе с ГРМ", None, None),
                ("Масляный насос (если потребуется)", 0, "Поставьте 1, если требуется по каталогу / по состоянию", None, None)]
    if kit["kind"] != "grm":
        optional = []
    listed = [it for it in kit["items"] if it["icon"] != "card" and not it.get("in_kit")]
    if any(it.get("buy_price") is not None for it in listed):  # кит собран — строки ровно по его составу
        rows = []
        for it in listed:
            if it.get("buy_price") is not None:
                notes = [f"Ваша закупка: {rub(it['buy_price'])} ₽ — впишите в колонку поставщика, у которого брали"]
            else:
                notes = ["Цены пока нет — впишите в колонку поставщика, у которого берёте"]
            if it.get("note"):
                notes.append(it["note"])
            rows.append((it.get("listing_name") or it["name"], 1, ". ".join(notes), it.get("brand"), it.get("article")))
        return rows + optional
    if kit["drive"] == "цепь":
        return [("Комплект цепи ГРМ (цепь, натяжитель, успокоители)", 1,
                 "Если готового комплекта нет — добавьте строки и купите позиции отдельно", None, None),
                ("Сальник коленвала передний", 1, "", None, None), ("Герметик", 1, "", None, None)] + optional
    rows = [("Комплект ремня ГРМ (ремень, натяжной ролик)", 1, "", None, None)]
    if "помпы" in kit["drive"]:
        rows.append(("Ремень привода помпы", 1, "По регламенту меняется вместе с ремнём ГРМ", None, None))
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
        ("3. «Киты» — сами посчитаются закупка, цена на Авито и прибыль до налога в двух вариантах: оплата через Авито Доставку и прямым переводом.", False),
        ("    Впишите минимальную цену конкурентов — появится сравнение с рынком. Колонка Y «Своя цена по рынку» — если цену кита ставим по рынку, а не по наценке.", False),
        ("4. «Параметры» — наценка, комиссии, резерв на товар, постоянные расходы и план заказов. Поменяете там — пересчитается всё.", False),
        ("5. «Прогноз» — выручка и прибыль за месяц: ТО-киты и ГРМ-киты отдельно и вместе, точка безубыточности.", False),
        ("6. «Моторы» — справка: где цепь, где ремень, что входит в ГРМ-кит, источники.", False),
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
    header(wp, 1, ["Параметр", "Значение", "Пояснение / источник"], [44, 14, 96])
    params = [  # (ключ, название, значение, формат, пояснение)
        ("markup", "Наценка к закупке", 0.30, "0.0%",
         "Цена кита = (детали + упаковка) × (1 + наценка), вверх до шага округления, минус «вычесть». Ваше решение."),
        ("pack", "Упаковка на 1 кит, ₽", 50, RUB, "Коробка, наклейка, печать карты ремонта — оценка; уточните по факту."),
        ("step", "Шаг округления цены, ₽", 100, RUB, "Цена округляется вверх до этого шага."),
        ("minus", "Вычесть из округлённой цены, ₽", 10, RUB, "Чтобы цена заканчивалась на …90 (4 700 → 4 690)."),
        ("fee", "Комиссия Авито Доставки", 0.065, "0.0%",
         "Только для заказов через Авито Доставку. ≈6,5% по данным селлерских сервисов (SelSup, 2026) — сверьте в кабинете Авито."),
        ("views", "Показы объявления на 1 заказ, ₽", 180, RUB,
         "Оценка: ≈150 показов × 1,2 ₽. Клиент пришёл с Авито при любой оплате, поэтому вычитается всегда. "
         "После запуска: расход на показы за месяц ÷ число заказов."),
        ("reserve", "Резерв на товар (возвраты, брак, довоз), % от деталей", 0.05, "0.0%",
         "Ваше решение: 5% от стоимости деталей. Через 2–3 месяца сверьте с фактом и поправьте."),
        ("reserve_in_price", "Резерв включать в цену? (1 — да, 0 — нет)", 0, "0",
         "0 — резерв вычитается из прибыли, цена не меняется. 1 — резерв добавляется к закупке, и цена кита растёт."),
        ("bank", "Комиссия банка при оплате переводом", 0.007, "0.0%",
         "Для прямых переводов. Оплата по QR/СБП для бизнеса обычно 0,4–0,7%; обычный перевод на счёт ИП часто бесплатный — уточните у банка."),
        ("cdek", "СДЭК за ваш счёт при оплате переводом, ₽", 0, RUB,
         "0, если доставку оплачивает покупатель. Если отправляете бесплатно — впишите среднюю стоимость отправки."),
        ("f_ip", "Взносы ИП, ₽ в месяц", 4783, RUB, "57 390 ₽ за 2026 год ÷ 12 (фиксированные взносы ИП)."),
        ("f_kassa", "Онлайн-касса, ₽ в месяц", 1500, RUB,
         "При оплате переводом покупателю по закону нужен чек (54-ФЗ). Оценка облачной кассы — уточните у своего банка."),
        ("f_pro", "Подписка Авито Pro, ₽ в месяц", 0, RUB, "0, пока не подключена. Впишите ≈3 000, когда подключите (обложка, автозагрузка)."),
        ("f_bank", "Обслуживание счёта, ₽ в месяц", 0, RUB, "0 на бесплатном тарифе."),
        ("f_other", "Прочее (связь, печать, расходники), ₽ в месяц", 500, RUB, "Оценка."),
        ("orders", "План заказов в месяц", 20, "0", "На сколько заказов делятся постоянные расходы. Больше заказов — меньше расходов на один кит."),
    ]
    P = {}
    for i, (key, name, val, fmt, note) in enumerate(params, 2):
        cell(wp, i, 1, name)
        cell(wp, i, 2, val, inp=True, fmt=fmt)
        cell(wp, i, 3, note, wrap=True)
        P[key] = f"Параметры!$B${i}"
    r_fixed = len(params) + 2
    cell(wp, r_fixed, 1, "Постоянные расходы на 1 кит, ₽", bold=True)
    fixed_keys = ["f_ip", "f_kassa", "f_pro", "f_bank", "f_other"]
    cell(wp, r_fixed, 2, "=(" + "+".join(P[k].split("!")[1] for k in fixed_keys) + f")/MAX(1,{P['orders'].split('!')[1]})",
         fmt=RUB, bold=True)
    cell(wp, r_fixed, 3, "Считается сам: сумма постоянных расходов в месяц ÷ план заказов.", wrap=True)
    P["fixed"] = f"Параметры!$B${r_fixed}"
    cell(wp, r_fixed + 2, 1, "Налог в расчёт не входит: прибыль на листе «Киты» — до налога.", italic=True, color="8C929B")

    # --- Киты ------------------------------------------------------------
    wk = wb.create_sheet("Киты")
    cols = ["Кит", "Вид", "Машина", "Мотор", "Привод ГРМ", "Приоритет", "Заголовок для Авито",
            "Главное фото (avito/png/…)", "Детали, ₽", "Позиций без цены", "Упаковка, ₽", "Закупка, ₽",
            "Цена на Авито, ₽", "Мин. цена конкурентов, ₽", "Сравнение с рынком",
            "Комиссия Авито, ₽", "Комиссия банка, ₽", "Показы, ₽", "Резерв на товар, ₽", "Постоянные расходы, ₽",
            "Прибыль: Авито Доставка, ₽", "Прибыль: перевод, ₽", "Маржа (Авито Доставка)", "Статус",
            "Своя цена по рынку, ₽"]
    widths = [9, 8, 30, 15, 13, 11, 50, 34, 12, 11, 11, 12, 13, 14, 18, 12, 12, 11, 12, 13, 15, 14, 12, 14, 14]
    header(wk, 1, cols, widths)
    wk.row_dimensions[1].height = 44
    for i, k in enumerate(kits, 2):
        cell(wk, i, 1, k["sku"], bold=True)
        cell(wk, i, 2, {"to": "ТО", "grm": "ГРМ", "brake": "Тормоза"}[k["kind"]])
        cell(wk, i, 3, k["car"])
        cell(wk, i, 4, k["engine"])
        cell(wk, i, 5, k["drive"])
        cell(wk, i, 6, k["priority"])
        cell(wk, i, 7, k["title"], wrap=True)
        cell(wk, i, 8, f'{k["id"]}-1-main.png')
        s = f'SUMIFS(Состав!$R:$R,Состав!$A:$A,A{i})'
        cell(wk, i, 9, f'=IF({s}=0,"",{s})', fmt=RUB)                                        # I детали
        cell(wk, i, 10, f'=COUNTIFS(Состав!$A:$A,A{i},Состав!$P:$P,"",Состав!$D:$D,">0")')   # J
        cell(wk, i, 11, f'=IF(I{i}="","",{P["pack"]})', fmt=RUB)                               # K упаковка
        cell(wk, i, 12, f'=IF(I{i}="","",I{i}+K{i})', fmt=RUB)                                 # L закупка
        cell(wk, i, 13, f'=IF(I{i}="","",IF(Y{i}<>"",Y{i},CEILING((I{i}*(1+{P["reserve"]}*{P["reserve_in_price"]})+K{i})'
                        f'*(1+{P["markup"]}),{P["step"]})-{P["minus"]}))', fmt=RUB, bold=True)  # M цена
        cell(wk, i, 14, None, inp=True, fmt=RUB)                                               # N конкуренты
        cell(wk, i, 15, f'=IF(OR(M{i}="",N{i}=""),"",IF(M{i}<=N{i},"не дороже рынка","дороже рынка"))')
        cell(wk, i, 16, f'=IF(M{i}="","",M{i}*{P["fee"]})', fmt=RUB)                          # P Авито
        cell(wk, i, 17, f'=IF(M{i}="","",M{i}*{P["bank"]})', fmt=RUB)                         # Q банк
        cell(wk, i, 18, f'=IF(M{i}="","",{P["views"]})', fmt=RUB)                              # R показы
        cell(wk, i, 19, f'=IF(I{i}="","",I{i}*{P["reserve"]})', fmt=RUB)                       # S резерв
        cell(wk, i, 20, f'=IF(M{i}="","",{P["fixed"]})', fmt=RUB)                              # T постоянные
        cell(wk, i, 21, f'=IF(M{i}="","",M{i}-L{i}-P{i}-R{i}-S{i}-T{i})', fmt=RUB, bold=True)  # U
        cell(wk, i, 22, f'=IF(M{i}="","",M{i}-L{i}-Q{i}-R{i}-S{i}-T{i}-{P["cdek"]})', fmt=RUB, bold=True)  # V
        cell(wk, i, 23, f'=IF(U{i}="","",U{i}/M{i})', fmt="0.0%")
        cell(wk, i, 24, "не выложен", inp=True)
        fixed = k.get("fixed_price")                                                           # Y своя цена
        if fixed is not None:
            assert k.get("price") == f"{fixed:,} ₽".replace(",", " "), f'{k["sku"]}: price и fixed_price расходятся'
        cell(wk, i, 25, fixed, inp=True, fmt=RUB)
        if k.get("price_note"):
            wk.cell(row=i, column=25).comment = Comment(k["price_note"], "ZAPKIT")
    last_k = len(kits) + 1
    dv = DataValidation(type="list", formula1='"не выложен,выложен,есть продажи,снят"', allow_blank=True)
    wk.add_data_validation(dv)
    dv.add(f"X2:X{last_k}")
    wk.conditional_formatting.add(f"J2:J{last_k}", CellIsRule(operator="greaterThan", formula=["0"],
                                                               fill=PatternFill("solid", fgColor="FCE4D6")))
    wk.conditional_formatting.add(f"O2:O{last_k}", CellIsRule(operator="equal", formula=['"дороже рынка"'],
                                                               font=Font(name=FONT, color="C00000")))
    for col in ("U", "V"):
        wk.conditional_formatting.add(f"{col}2:{col}{last_k}", CellIsRule(operator="lessThan", formula=["0"],
                                                                         font=Font(name=FONT, color="C00000", bold=True)))
    wk.freeze_panes = "D2"
    wk["J1"].comment = Comment("Сколько позиций с кол-вом > 0 ещё без цены. 0 — кит полностью посчитан.", "ZAPKIT")
    wk["M1"].comment = Comment("Считается по наценке с листа «Параметры». Если в колонке Y «Своя цена по рынку» "
                               "есть число — берётся оно.", "ZAPKIT")
    wk["Y1"].comment = Comment("Для китов, где цену ставим по рынку, а не по наценке: впишите цену, "
                               "по которой конечный покупатель берёт то же самое на маркетплейсах. "
                               "Пусто — цена по наценке.", "ZAPKIT")
    wk["U1"].comment = Comment("До налога: цена − закупка − комиссия Авито − показы − резерв − постоянные расходы.", "ZAPKIT")
    wk["V1"].comment = Comment("До налога: цена − закупка − комиссия банка − показы − резерв − постоянные расходы − СДЭК за ваш счёт.", "ZAPKIT")

    # --- Прогноз на месяц -------------------------------------------------
    wf = wb.create_sheet("Прогноз")
    for col, w in zip("ABCDEFGHIJKLM", [44, 14, 14, 14, 14, 13, 13, 12, 12, 12, 13, 15, 13]):
        wf.column_dimensions[col].width = w
    c = wf.cell(row=1, column=1, value="Прогноз на месяц (до налога): ТО-киты и ГРМ-киты")
    c.font = f(bold=True, size=14)
    header(wf, 3, ["", "ТО-кит", "ГРМ-кит", "Пояснение"], [44, 14, 14, 14])
    wf.merge_cells(start_row=3, start_column=4, end_row=3, end_column=12)
    inputs = [  # (название, ТО, ГРМ, формат, пояснение)
        ("Средний чек кита, ₽", 4490, 9990, RUB,
         "ТО: среднее по Picanto (4 190) и Jetta (4 790). ГРМ: пока собран один — Coolray на Gates (9 990). "
         "Когда соберёте больше китов, возьмите средние из справки ниже."),
        ("Средняя стоимость деталей, ₽", 3365, 7056.23, RUB,
         "ТО: среднее по Picanto и Jetta. ГРМ: Coolray — Gates K0120529 6 066 + ремень помпы 990,23."),
    ]
    for i, (name, to, grm, fmt, note) in enumerate(inputs, 4):
        cell(wf, i, 1, name)
        cell(wf, i, 2, to, inp=True, fmt=fmt)
        cell(wf, i, 3, grm, inp=True, fmt=fmt)
        cell(wf, i, 4, note, wrap=True)
        wf.merge_cells(start_row=i, start_column=4, end_row=i, end_column=12)
        wf.row_dimensions[i].height = 30
    cell(wf, 6, 1, "Доля оплат через Авито Доставку")
    cell(wf, 6, 2, 0.5, inp=True, fmt="0%")
    cell(wf, 6, 4, "Общая для ТО и ГРМ. Остальные — прямым переводом. Ваша оценка; уточните по факту.", wrap=True)
    wf.merge_cells(start_row=6, start_column=4, end_row=6, end_column=12)
    for r, name, col in ((7, "Справка: средний чек по листу «Киты»", "M"),
                         (8, "Справка: средние детали по листу «Киты»", "I")):
        cell(wf, r, 1, name)
        for c_, kind in ((2, "ТО"), (3, "ГРМ")):
            cell(wf, r, c_, f'=IFERROR(AVERAGEIFS(Киты!${col}:${col},Киты!$B:$B,"{kind}",Киты!${col}:${col},">0"),"")',
                 fmt=RUB)
    fixed_sum = "(" + "+".join(P[k] for k in fixed_keys) + ")"
    cell(wf, 9, 1, "Постоянные расходы в месяц, ₽")
    cell(wf, 9, 2, f"={fixed_sum}", fmt=RUB)
    cell(wf, 9, 4, "Сумма постоянных расходов с листа «Параметры». Платятся один раз в месяц на весь магазин.", wrap=True)
    wf.merge_cells(start_row=9, start_column=4, end_row=9, end_column=12)
    cell(wf, 10, 1, "Прибыль с 1 заказа до постоянных расходов, ₽")
    for c_, L in ((2, "B"), (3, "C")):
        cell(wf, 10, c_, f"={L}4-({L}5+{P['pack']})-$B$6*{L}4*{P['fee']}-(1-$B$6)*({L}4*{P['bank']}+{P['cdek']})"
                         f"-{P['views']}-{L}5*{P['reserve']}", fmt=RUB, bold=True)
    cell(wf, 11, 1, "Точка безубыточности, заказов в месяц", bold=True)
    for c_, L in ((2, "B"), (3, "C")):
        cell(wf, 11, c_, f'=IF({L}10<=0,"не окупается",ROUNDUP($B$9/{L}10,0))', bold=True)
    cell(wf, 11, 4, "Сколько китов одного вида нужно продать, чтобы покрыть постоянные расходы.", wrap=True)
    wf.merge_cells(start_row=11, start_column=4, end_row=11, end_column=12)

    heads = ["Сценарий", "ТО-китов в месяц", "ГРМ-китов в месяц", "Выручка, ₽", "Детали и упаковка, ₽",
             "Комиссия Авито, ₽", "Комиссия банка, ₽", "Показы, ₽", "Резерв на товар, ₽", "СДЭК за ваш счёт, ₽",
             "Постоянные, ₽", "Прибыль до налога, ₽", "Прибыль на 1 заказ, ₽"]
    header(wf, 13, heads, [44, 14, 14, 14, 14, 13, 13, 12, 12, 12, 13, 15, 13])
    wf.row_dimensions[13].height = 44
    scenarios = [("Только ГРМ", 0, 5), ("Только ГРМ", 0, 10), ("Только ГРМ", 0, 15), ("Только ГРМ", 0, 20),
                 ("Только ГРМ", 0, 30), ("Только ТО — для сравнения", 20, 0), ("ТО + ГРМ", 20, 5),
                 ("ТО + ГРМ", 20, 10), ("ТО + ГРМ", 30, 15), ("ТО + ГРМ", 50, 20)]
    first = 14
    for j, (name, n_to, n_grm) in enumerate(scenarios, first):
        cell(wf, j, 1, name)
        cell(wf, j, 2, n_to, inp=True, bold=True)
        cell(wf, j, 3, n_grm, inp=True, bold=True)
        cell(wf, j, 4, f"=B{j}*$B$4+C{j}*$C$4", fmt=RUB)
        cell(wf, j, 5, f"=B{j}*($B$5+{P['pack']})+C{j}*($C$5+{P['pack']})", fmt=RUB)
        cell(wf, j, 6, f"=$B$6*D{j}*{P['fee']}", fmt=RUB)
        cell(wf, j, 7, f"=(1-$B$6)*D{j}*{P['bank']}", fmt=RUB)
        cell(wf, j, 8, f"=(B{j}+C{j})*{P['views']}", fmt=RUB)
        cell(wf, j, 9, f"=(B{j}*$B$5+C{j}*$C$5)*{P['reserve']}", fmt=RUB)
        cell(wf, j, 10, f"=(B{j}+C{j})*(1-$B$6)*{P['cdek']}", fmt=RUB)
        cell(wf, j, 11, "=$B$9", fmt=RUB)
        cell(wf, j, 12, f"=D{j}-SUM(E{j}:K{j})", fmt=RUB, bold=True)
        cell(wf, j, 13, f'=IF(B{j}+C{j}=0,"",L{j}/(B{j}+C{j}))', fmt=RUB)
    last = first + len(scenarios) - 1
    wf.conditional_formatting.add(f"L{first}:L{last}", CellIsRule(operator="lessThan", formula=["0"],
                                                                 font=Font(name=FONT, color="C00000", bold=True)))
    cell(wf, last + 2, 1, "Налог не учтён. Число китов в колонках B и C можно менять. При росте продаж впишите в «Параметры» "
                          "подписку Авито Pro, если подключите.", italic=True, color="8C929B")

    # --- Состав ----------------------------------------------------------
    wc = wb.create_sheet("Состав")
    sup_first, sup_last = 7, 6 + len(SUPPLIERS)            # G..O
    L_first, L_last = get_column_letter(sup_first), get_column_letter(sup_last)
    header(wc, 1, ["Кит", "Машина", "Позиция", "Кол-во", "Бренд", "Артикул"] + SUPPLIERS
           + ["Лучшая цена, ₽", "У кого", "Сумма, ₽", "Комментарий"],
           [9, 26, 44, 8, 14, 16] + [11] * len(SUPPLIERS) + [12, 13, 12, 60])
    wc.row_dimensions[1].height = 44

    def item_row(r, sku, pos, qty, note, example=None, brand=None, article=None):
        ex = example is not None
        cell(wc, r, 1, sku, bold=not ex, italic=ex, color="8C929B" if ex else None)
        car = "образец заполнения — строку можно удалить" if ex else \
            f'=IFERROR(INDEX(Киты!$C:$C,MATCH(A{r},Киты!$A:$A,0)),"")'
        cell(wc, r, 2, car, italic=ex, color="8C929B" if ex else None)
        cell(wc, r, 3, pos)
        cell(wc, r, 4, qty, inp=True)
        cell(wc, r, 5, example["brand"] if ex else brand, inp=True)
        cell(wc, r, 6, example["art"] if ex else article, inp=True)
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
        for pos, qty, note, brand, article in buy_rows(k):
            item_row(r, k["sku"], pos, qty, note, brand=brand, article=article)
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
    wb.move_sheet("Киты", offset=-1)      # Инструкция, Киты, Параметры, …
    wb.move_sheet("Прогноз", offset=-(wb.sheetnames.index("Прогноз") - 2))  # … Киты, Прогноз, Параметры
    wb.save(OUT)
    print("written", OUT, "rows:", r - 1)


if __name__ == "__main__":
    build()
