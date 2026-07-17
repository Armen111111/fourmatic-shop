# Магазин запчастей Mercedes-Benz в Telegram

Telegram-бот + Mini App (веб-витрина) для продажи оригинальных и аналоговых запчастей.
Архитектура — та же, что в проекте `perfume-shop`: aiogram-бот на polling + aiohttp
раздаёт Mini App и API, каталог хранится в `data/products.json`.

## Структура

- `bot/main.py` — точка входа: bot polling + aiohttp сервер.
- `bot/webserver.py` — `GET /api/config`, `GET /api/products`, `POST /api/checkout`.
- `bot/handlers/start.py` — `/start`, кнопка открытия Mini App.
- `bot/handlers/payments.py` — онлайн-оплата (когда появится провайдер).
- `bot/services/catalog.py` — чтение `data/products.json`.
- `bot/services/orders.py` — заказы в `data/orders.json`.
- `webapp/` — фронтенд (vanilla HTML/CSS/JS).

## Оплата

Как и в парфюм-магазине: без `PROVIDER_TOKEN` в `.env` магазин работает в режиме
ручного заказа (клиент оставляет контакты и способ доставки/оплаты, вы подтверждаете
вручную). Как только оформите ИП/самозанятость и подключите провайдера через
@BotFather — впишите `PROVIDER_TOKEN`, оплата картой включится сама.

## Каталог товаров

`data/products.json` — сейчас пустой (`[]`). Формат одной позиции:

```json
{
  "id": "unikalnyj-slug",
  "name": "Название детали",
  "brand": "Производитель (Bosch, Febi, Mercedes-Benz OEM...)",
  "category": "Тормозная система",
  "compatible_models": ["W212", "W211", "C-Class W205"],
  "price": 3500,
  "description": "Описание детали",
  "image": "images/имя-файла.jpg",
  "in_stock": true,
  "is_hit": false,
  "is_new": false
}
```

Поле `compatible_models` уже заложено — понадобится, когда будем подключать подбор
по VIN (сейчас отложили до появления реального каталога).

## Установка

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
```

Заполните `.env`: `BOT_TOKEN` (от @BotFather), `ADMIN_CHAT_ID`, `WEBAPP_URL`
(публичный HTTPS-адрес после деплоя).

## Продакшен

Как и с духами — Render.com (бесплатный тариф): подключить GitHub-репозиторий,
Build Command `pip install -r requirements.txt`, Start Command `python -m bot.main`.
