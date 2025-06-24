import os
import logging
import getpass
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

logging.basicConfig(level=logging.INFO)

TELEGRAM_TOKEN = "8124119601:AAEgnFwCalzIKU15uHpIyWlCRbu4wvNEAUw"
if not TELEGRAM_TOKEN:
    TELEGRAM_TOKEN = getpass.getpass("Введите TELEGRAM_TOKEN: ")

bot = Bot(token=TELEGRAM_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# Кнопка меню
menu_kb = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="📝 Сгенерировать РП-биографию")]],
    resize_keyboard=True,
)

class BioStates(StatesGroup):
    waiting_fio = State()
    waiting_age = State()
    waiting_nationality = State()

# Приветствие и описание бота
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    text = (
        "👋 <b>Добро пожаловать в RP Biography Bot!</b>\n\n"
        "Этот бот поможет тебе <b>создать уникальную RP-биографию</b> для мира <b>Black Russia</b> по всем правилам сервера.\n"
        "Бот задаст тебе несколько вопросов и соберёт анкету — а дальше сгенерирует красивую, грамотную биографию твоего персонажа.\n\n"
        "Нажми кнопку ниже, чтобы начать:"
    )
    await message.answer(text, reply_markup=menu_kb, parse_mode="HTML")

# Кнопка запуска анкеты
@dp.message(lambda m: m.text == "📝 Сгенерировать РП-биографию")
async def start_bio(message: types.Message, state: FSMContext):
    await state.set_state(BioStates.waiting_fio)
    await message.answer(
        "<b>1️⃣ Укажите ФИО персонажа:</b>\n\n"
        "Пример: <i>Иванов Иван Иванович</i>\n"
        "Имя и фамилия должны быть на русском языке, без нижних подчёркиваний.",
        parse_mode="HTML"
    )

# Ввод ФИО
@dp.message(BioStates.waiting_fio)
async def bio_fio(message: types.Message, state: FSMContext):
    fio = message.text.strip()
    if "_" in fio or not all(x.isalpha() or x.isspace() for x in fio):
        await message.answer(
            "⚠️ <b>ФИО должно быть на русском языке, без нижних подчёркиваний и лишних символов.</b>\n"
            "Попробуй ещё раз.\n"
            "Пример: <i>Иванов Иван Иванович</i>",
            parse_mode="HTML"
        )
        return
    await state.update_data(fio=fio)
    await state.set_state(BioStates.waiting_age)
    await message.answer(
        "<b>2️⃣ Укажите возраст персонажа:</b>\n"
        "Возраст должен быть от <b>18</b> до <b>65</b> лет.",
        parse_mode="HTML"
    )

# Ввод возраста
@dp.message(BioStates.waiting_age)
async def bio_age(message: types.Message, state: FSMContext):
    try:
        age = int(message.text.strip())
        if age < 18 or age > 65:
            raise ValueError
    except ValueError:
        await message.answer(
            "⚠️ <b>Возраст должен быть числом от 18 до 65.</b>\nПопробуй ещё раз.",
            parse_mode="HTML"
        )
        return
    await state.update_data(age=age)
    await state.set_state(BioStates.waiting_nationality)
    await message.answer(
        "<b>3️⃣ Укажите национальность персонажа:</b>\n"
        "Пример: <i>Русский, Татарин, Армянин, Чеченец, Итальянец и т.п.</i>",
        parse_mode="HTML"
    )

# Ввод национальности — после этого можешь добавить генерацию биографии!
@dp.message(BioStates.waiting_nationality)
async def bio_nationality(message: types.Message, state: FSMContext):
    nationality = message.text.strip().capitalize()
    await state.update_data(nationality=nationality)
    data = await state.get_data()
    # Здесь вызов генератора биографии (функция будет ниже)
    await message.answer(
        f"✅ <b>Анкета заполнена!</b>\n\n"
        f"ФИО: <i>{data['fio']}</i>\n"
        f"Возраст: <i>{data['age']}</i>\n"
        f"Национальность: <i>{data['nationality']}</i>\n\n"
        f"Генерация биографии скоро будет доступна...",
        parse_mode="HTML"
    )
    await state.clear()

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    import sys
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
