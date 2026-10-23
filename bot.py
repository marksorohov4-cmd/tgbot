import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, F, Router
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.types import CallbackQuery, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID") or 0)
CHANNEL_URL = "https://t.me/egor_physmat"

if not BOT_TOKEN:
    raise SystemExit("Не задан BOT_TOKEN в файле .env")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)
log = logging.getLogger("bot")

router = Router()


def main_menu():
    kb = InlineKeyboardBuilder()
    kb.button(text="ℹ️ О боте", callback_data="about")
    kb.button(text="🆔 Мой ID", callback_data="myid")
    kb.button(text="📢 Наш канал", url=CHANNEL_URL)
    kb.adjust(2, 1)  # первый ряд: 2 кнопки, второй ряд: 1 кнопка
    return kb.as_markup()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        f"Привет, {message.from_user.first_name}! 👋\nВыбери действие:",
        reply_markup=main_menu(),
    )


@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer(
        "/start — главное меню\n"
        "/help — эта справка\n"
        "/id — твой Telegram ID\n"
        "/admin — команда только для администратора\n\n"
        "Любой другой текст я просто повторю."
    )


@router.message(Command("id"))
async def cmd_id(message: Message):
    await message.answer(
        f"Твой ID: <code>{message.from_user.id}</code>",
        parse_mode=ParseMode.HTML,
    )


@router.message(Command("admin"))
async def cmd_admin(message: Message):
    if message.from_user.id != ADMIN_ID:
        await message.answer("⛔ Эта команда только для администратора.")
        return
    await message.answer("✅ Ты администратор. Здесь может быть твоя панель управления.")


@router.callback_query(F.data == "about")
async def cb_about(call: CallbackQuery):
    await call.message.answer("Это шаблон бота на aiogram 3. Добавляй свои команды в bot.py.")
    await call.answer()


@router.callback_query(F.data == "myid")
async def cb_myid(call: CallbackQuery):
    await call.message.answer(
        f"Твой ID: <code>{call.from_user.id}</code>",
        parse_mode=ParseMode.HTML,
    )
    await call.answer()


@router.message(F.text)
async def echo(message: Message):
    await message.answer(message.text)


async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(router)
    log.info("Бот запускается...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        log.info("Бот остановлен")
