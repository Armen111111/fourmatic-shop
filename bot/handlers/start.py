from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, WebAppInfo

from bot.config import Config


def register(config: Config) -> Router:
    router = Router(name="start")

    @router.message(CommandStart())
    async def start_handler(message: Message) -> None:
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="🔧 Открыть каталог",
                        web_app=WebAppInfo(url=config.webapp_url),
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
