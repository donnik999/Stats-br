import os
import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import openai

logging.basicConfig(level=logging.INFO)

TELEGRAM_TOKEN = os.environ.get("8124119601:AAEgnFwCalzIKU15uHpIyWlCRbu4wvNEAUw")
DEEPSEEK_API_KEY = os.environ.get("sk-fab5d466db514e5087656e9c49a7a03d")

bot = Bot(token=TELEGRAM_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

openai.api_base = "https://api.deepseek.com/v1"
openai.api_key = DEEPSEEK_API_KEY

# Клавиатура меню
menu_kb = ReplyKeyboardMarkup(resize_keyboard=True)
menu_kb.add(KeyboardButton("✍️ Написать РП биографию"))

class BioStates(StatesGroup):
    waiting_fio = State()
    waiting_age = State()
    waiting_gender = State()
    waiting_nationality = State()

@dp.message_handler(commands=["start"])
async def cmd_start(message: types.Message):
    text = (
        "👋 Привет! Я бот для генерации RP-биографий по шаблону.\n"
        "Нажми кнопку ниже, чтобы начать:"
    )
    await message.answer(text, reply_markup=menu_kb)

@dp.message_handler(lambda m: m.text == "✍️ Написать РП биографию")
async def start_bio(message: types.Message):
    await BioStates.waiting_fio.set()
    await message.answer("Введите ФИО персонажа (например: Иванов Иван Иванович):")

@dp.message_handler(state=BioStates.waiting_fio)
async def bio_fio(message: types.Message, state: FSMContext):
    await state.update_data(fio=message.text)
    await BioStates.waiting_age.set()
    await message.answer("Введите возраст персонажа (например: 25):")

@dp.message_handler(state=BioStates.waiting_age)
async def bio_age(message: types.Message, state: FSMContext):
    await state.update_data(age=message.text)
    await BioStates.waiting_gender.set()
    await message.answer("Укажите пол персонажа (Мужской/Женский):")

@dp.message_handler(state=BioStates.waiting_gender)
async def bio_gender(message: types.Message, state: FSMContext):
    await state.update_data(gender=message.text)
    await BioStates.waiting_nationality.set()
    await message.answer("Укажите национальность персонажа:")

@dp.message_handler(state=BioStates.waiting_nationality)
async def bio_nationality(message: types.Message, state: FSMContext):
    await state.update_data(nationality=message.text)
    data = await state.get_data()
    await state.finish()

    prompt = (
        f"Напиши RP-биографию персонажа на форум по шаблону, используя такие данные:\n"
        f"ФИО: {data['fio']}\n"
        f"Возраст: {data['age']}\n"
        f"Пол: {data['gender']}\n"
        f"Национальность: {data['nationality']}\n"
        "Остальные пункты (детство, юность, настоящее, характер, семья, хобби, внешность и т.д.) придумай сам, соблюдая правило написания от первого лица, без сверхспособностей, без известных личностей, без ошибок. Минимум 10 строк на раздел детство, юность, настоящее.\n"
        "Шаблон:\n"
        "ФИО:\nПол:\nДата рождения:\nВозраст:\nНациональность:\nМесто рождения:\nОбразование:\nОтношение к воинской службе(для мужчин):\nСемья:\nМесто проживания на момент проживания с родителями:\nОписание внешности:\nОсобенности характера:\nВаше фото:\nДетство(От десяти строк):\nЮность(От десяти строк):\nНастоящее время(От десяти строк):\nСемейное положение:\nМесто текущего проживания:.\nИмеется ли судимость?:\nВаше хобби:"
    )
    await message.answer("Генерирую биографию, подождите...")

    try:
        response = openai.ChatCompletion.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "Ты пишешь грамотные RP-биографии на русском языке по форумному шаблону."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1200,
        )
        bio_text = response.choices[0].message["content"]
    except Exception as e:
        await message.answer(f"Ошибка генерации биографии: {e}")
        return

    await message.answer("Вот ваша RP-биография:\n\n" + bio_text)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
