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
import openai

logging.basicConfig(level=logging.INFO)

# Получаем токены из переменных окружения или через консольный ввод
TELEGRAM_TOKEN = os.environ.get("8124119601:AAEgnFwCalzIKU15uHpIyWlCRbu4wvNEAUw")
DEEPSEEK_API_KEY = os.environ.get("sk-fab5d466db514e5087656e9c49a7a03d")

if not TELEGRAM_TOKEN:
    TELEGRAM_TOKEN = getpass.getpass("Введите TELEGRAM_TOKEN: ")
if not DEEPSEEK_API_KEY:
    DEEPSEEK_API_KEY = getpass.getpass("Введите DEEPSEEK_API_KEY (DeepSeek): ")

bot = Bot(token=TELEGRAM_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# Создаём OpenAI client с DeepSeek endpoint
client = openai.OpenAI(
    api_key=DEEPSEEK_API_KEY,
    base_url="https://api.deepseek.com/v1"
)

menu_kb = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="✍️ Написать РП биографию")]],
    resize_keyboard=True,
)

class BioStates(StatesGroup):
    waiting_fio = State()
    waiting_age = State()
    waiting_gender = State()
    waiting_nationality = State()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    text = (
        "👋 Привет! Я бот для генерации RP-биографий по шаблону.\n"
        "Нажми кнопку ниже, чтобы начать:"
    )
    await message.answer(text, reply_markup=menu_kb)

@dp.message(lambda m: m.text == "✍️ Написать РП биографию")
async def start_bio(message: types.Message, state: FSMContext):
    await state.set_state(BioStates.waiting_fio)
    await message.answer("Введите ФИО персонажа (например: Иванов Иван Иванович):")

@dp.message(BioStates.waiting_fio)
async def bio_fio(message: types.Message, state: FSMContext):
    await state.update_data(fio=message.text)
    await state.set_state(BioStates.waiting_age)
    await message.answer("Введите возраст персонажа (например: 25):")

@dp.message(BioStates.waiting_age)
async def bio_age(message: types.Message, state: FSMContext):
    await state.update_data(age=message.text)
    await state.set_state(BioStates.waiting_gender)
    await message.answer("Укажите пол персонажа (Мужской/Женский):")

@dp.message(BioStates.waiting_gender)
async def bio_gender(message: types.Message, state: FSMContext):
    await state.update_data(gender=message.text)
    await state.set_state(BioStates.waiting_nationality)
    await message.answer("Укажите национальность персонажа:")

@dp.message(BioStates.waiting_nationality)
async def bio_nationality(message: types.Message, state: FSMContext):
    await state.update_data(nationality=message.text)
    data = await state.get_data()
    await state.clear()
    prompt = (
        f"Напиши RP-биографию персонажа на форум по шаблону, используя такие данные:\n"
        f"ФИО: {data.get('fio')}\n"
        f"Возраст: {data.get('age')}\n"
        f"Пол: {data.get('gender')}\n"
        f"Национальность: {data.get('nationality')}\n"
        "Остальные пункты (детство, юность, настоящее, характер, семья, хобби, внешность и т.д.) придумай сам, соблюдая правило написания от первого лица, без сверхспособностей, без известных личностей, без ошибок. Минимум 10 строк на раздел детство, юность, настоящее.\n"
        "Шаблон:\n"
        "ФИО:\nПол:\nДата рождения:\nВозраст:\nНациональность:\nМесто рождения:\nОбразование:\nОтношение к воинской службе(для мужчин):\nСемья:\nМесто проживания на момент проживания с родителями:\nОписание внешности:\nОсобенности характера:\nВаше фото:\nДетство(От десяти строк):\nЮность(От десяти строк):\nНастоящее время(От десяти строк):\nСемейное положение:\nМесто текущего проживания:\nИмеется ли судимость?:\nВаше хобби:"
    )
    await message.answer("Генерирую биографию, подождите...")

    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "Ты пишешь грамотные RP-биографии на русском языке по форумному шаблону."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1200,
        )
        bio_text = response.choices[0].message.content
    except Exception as e:
        await message.answer(f"Ошибка генерации биографии: {e}")
        return

    await message.answer("Вот ваша RP-биография:\n\n" + bio_text)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    import sys
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
