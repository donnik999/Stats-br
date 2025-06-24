import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, Router, types, F
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import openai

from config import TELEGRAM_TOKEN, DEEPSEEK_API_KEY

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Создаем бота и диспетчер
bot = Bot(token=TELEGRAM_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)
router = Router()

openai.api_base = "https://api.deepseek.com/v1"
openai.api_key = DEEPSEEK_API_KEY

# Клавиатура меню
menu_kb = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="✍️ Написать РП биографию")]],
    resize_keyboard=True
)

# FSM состояния
class BioStates(StatesGroup):
    waiting_fio = State()
    waiting_age = State()
    waiting_gender = State()
    waiting_nationality = State()

# /start
@router.message(Command("start"))
async def cmd_start(message: types.Message):
    text = (
        "👋 Привет! Я бот для создания RP-биографий по шаблону.\n"
        "Нажми кнопку ниже, чтобы начать:"
    )
    await message.answer(text, reply_markup=menu_kb)

# Обработка кнопки
@router.message(F.text == "✍️ Написать РП биографию")
async def start_bio(message: types.Message, state: FSMContext):
    await state.set_state(BioStates.waiting_fio)
    await message.answer("Введите ФИО персонажа (пример: Иванов Иван Иванович):")

@router.message(BioStates.waiting_fio)
async def bio_fio(message: types.Message, state: FSMContext):
    await state.update_data(fio=message.text)
    await state.set_state(BioStates.waiting_age)
    await message.answer("Введите возраст персонажа (18-65):")

@router.message(BioStates.waiting_age)
async def bio_age(message: types.Message, state: FSMContext):
    await state.update_data(age=message.text)
    await state.set_state(BioStates.waiting_gender)
    await message.answer("Укажите пол персонажа (Мужской/Женский):")

@router.message(BioStates.waiting_gender)
async def bio_gender(message: types.Message, state: FSMContext):
    await state.update_data(gender=message.text)
    await state.set_state(BioStates.waiting_nationality)
    await message.answer("Укажите национальность персонажа:")

@router.message(BioStates.waiting_nationality)
async def bio_nationality(message: types.Message, state: FSMContext):
    await state.update_data(nationality=message.text)
    data = await state.get_data()
    await state.clear()

    # Генерация промпта для DeepSeek
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

# Регистрация роутера
dp.include_router(router)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
