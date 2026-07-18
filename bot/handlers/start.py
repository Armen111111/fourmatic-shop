from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, WebAppInfo

from bot.config import Config

# Bump this on every frontend deploy. Telegram's WebView caches a Mini App
# by its exact URL, ignoring HTTP cache headers on the document itself —
# changing this query param is what actually forces a fresh load.
WEBAPP_BUILD = "8"


def register(config: Config) -> Router:
    router = Router(name="start")

    @router.message(CommandStart())
    async def start_handler(message: Message) -> None:
        webapp_url = f"{config.webapp_url}?build={WEBAPP_BUILD}"
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="🔧 Открыть каталог",
                        web_app=WebAppInfo(url=webapp_url),
                    )
                ]
            ]
        )
        await message.answer(
            "Добро пожаловать!\n\n"
            "Оригинальные и аналоговые запчасти для Mercedes-Benz.\n"
            "Нажмите кнопку ниже, чтобы открыть каталог.",
            reply_markup=keyboard,
        )

    return router
