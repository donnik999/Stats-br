import os
import random
import logging
import getpass
import asyncio
from datetime import datetime
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

logging.basicConfig(level=logging.INFO)

TELEGRAM_TOKEN = ("8124119601:AAEgnFwCalzIKU15uHpIyWlCRbu4wvNEAUw")
if not TELEGRAM_TOKEN:
    TELEGRAM_TOKEN = getpass.getpass("Введите TELEGRAM_TOKEN: ")

bot = Bot(token=TELEGRAM_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# Клавиатура выбора сервера
server_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="RED", callback_data="server_red")]
        # Будут другие сервера? Добавь сюда новые кнопки!
    ]
)

class ServerState(StatesGroup):
    choosing_server = State()

class RedBioStates(StatesGroup):
    waiting_name = State()
    waiting_gender = State()
    waiting_age = State()
    waiting_nationality = State()

# Приветствие и выбор сервера
@dp.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    await state.clear()
    text = (
        "👋 <b>Добро пожаловать в RP Biography Bot!</b>\n\n"
        "Выбери сервер, для которого хочешь сгенерировать РП-биографию:"
    )
    await message.answer(text, reply_markup=server_kb, parse_mode="HTML")
    await state.set_state(ServerState.choosing_server)

# Обработка выбора сервера (пока только RED)
@dp.callback_query(ServerState.choosing_server)
async def choose_server(callback: types.CallbackQuery, state: FSMContext):
    if callback.data == "server_red":
        await state.clear()
        await state.set_state(RedBioStates.waiting_name)
        await callback.message.answer(
            "<b>1️⃣ Введите имя и фамилию персонажа:</b>\nПример: Иван Иванов",
            parse_mode="HTML"
        )
    await callback.answer()

# Далее — блок анкеты и генерации (ШАГ 2) добавим после твоего подтверждения!
# Жду: ок ли структура выбора сервера и старт анкеты?

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    import sys
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
