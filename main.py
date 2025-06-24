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

# Главное меню
main_menu_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📝 Создать РП-биографию")],
        [KeyboardButton(text="📞 Связь с владельцем")]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

# Клавиатура выбора сервера
server_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="RED", callback_data="server_red")]
    ]
)

class MenuStates(StatesGroup):
    waiting_main_menu = State()
    choosing_server = State()

class RedBioStates(StatesGroup):
    waiting_name = State()
    waiting_gender = State()
    waiting_age = State()
    waiting_nationality = State()

# НАСЕЛЕННЫЕ ПУНКТЫ BLACK RUSSIA
CITIES = [
    "Арзамас", "Нижегородск", "Южный", "Лыткарино"
]
PGT = [
    "Батырево", "Корякино", "Горки"
]
VILLAGES = [
    "Гарель"
]
SPECIAL = [
    "Рублевка"
]
ALL_LOCATIONS = CITIES + PGT + VILLAGES + SPECIAL

# ОРГАНИЗАЦИИ/РАБОТЫ BLACK RUSSIA
JOBS = [
    "Инкассатор", "Рыболов", "Водолаз", "Механик", "Кладоискатель",
    "Работник на ферме", "Работник на заводе", "Работник на шахте",
    "МЧС", "Таксист", "Газовая служба", "Электрик", "Водитель автобуса"
]
ORGANIZATIONS = [
    "Центральная Больница", "ГИБДД", "УМВД", "СМИ", "Правительство",
    "ФСИН", "ФСБ", "Воинская Часть"
]

# Примеры для генерации родителей
MALE_NAMES = [
    "Алексей", "Максим", "Виктор", "Сергей", "Игорь", "Владимир", "Евгений", "Дмитрий", "Олег", "Георгий"
]
FEMALE_NAMES = [
    "Марина", "Екатерина", "Ирина", "Анна", "Татьяна", "Ольга", "Валентина", "Елена", "Наталья", "Галина"
]

# Черты характера/личные черты
PERSONALITY_TRAITS = [
    "Ответственный и трудолюбивый",
    "Общительный и дружелюбный",
    "Умеет быстро принимать решения",
    "Стрессоустойчивый, спокоен в сложных ситуациях",
    "Честный и открытый человек",
    "Имеет лидерские качества",
    "Умеет работать в команде",
    "Всегда готов прийти на помощь",
    "Обладает чувством юмора",
    "Стремится к развитию и новым знаниям"
]

APPEARANCES = [
    "Среднего роста, крепкого телосложения, тёмные волосы.",
    "Высокий, спортивный, светлые волосы, серые глаза.",
    "Невысокий, худощавый, русые волосы, карие глаза.",
    "Средний рост, выразительные черты лица, аккуратная стрижка.",
    "Крупного телосложения, сдержанный взгляд, черные волосы."
]

def get_random_location():
    # Генерируем тип населенного пункта и сам пункт
    location_type = random.choices(
        ["Город", "ПГТ", "Деревня", "Особое место"], [4, 3, 1, 1]
    )[0]
    if location_type == "Город":
        return random.choice(CITIES)
    elif location_type == "ПГТ":
        return random.choice(PGT)
    elif location_type == "Деревня":
        return random.choice(VILLAGES)
    else:
        return random.choice(SPECIAL)

def generate_address():
    # Пример: "г. Арзамас, ул. Гагарина, д. 12, кв. 56"
    city = get_random_location()
    streets = [
        "Гагарина", "Центральная", "Молодёжная", "Советская", "Парковая", "Заречная"
    ]
    street = random.choice(streets)
    house = random.randint(1, 99)
    apt = random.randint(1, 120)
    if city in CITIES:
        prefix = "г."
    elif city in PGT:
        prefix = "пгт"
    elif city in VILLAGES:
        prefix = "д."
    else:
        prefix = ""
    return f"{prefix} {city}, ул. {street}, д. {house}, кв. {apt}", city

def get_parent_fio(fam, gender):
    if gender == "мужской":
        name = random.choice(MALE_NAMES)
        return f"{name} {fam}"
    else:
        name = random.choice(FEMALE_NAMES)
        # Склоняем фамилию для матери (на -а/ая)
        fam_f = fam
        if fam.endswith("ий"):
            fam_f = fam[:-2] + "ая"
        elif fam.endswith("ов") or fam.endswith("ев") or fam.endswith("ин"):
            fam_f = fam + "а"
        elif fam.endswith("ый"):
            fam_f = fam[:-2] + "ая"
        elif fam.endswith("ский"):
            fam_f = fam[:-4] + "ская"
        elif fam.endswith("ой"):
            fam_f = fam[:-2] + "ая"
        elif not fam.endswith("а"):
            fam_f = fam + "а"
        return f"{name} {fam_f}"

def generate_parents(fam):
    father = get_parent_fio(fam, "мужской")
    mother = get_parent_fio(fam, "женский")
    father_job = random.choice(JOBS + ORGANIZATIONS)
    mother_job = random.choice(JOBS + ORGANIZATIONS)
    return {
        "father": father,
        "father_job": father_job,
        "mother": mother,
        "mother_job": mother_job
    }

def generate_birthdate(age: int) -> str:
    now = datetime.now()
    year = now.year - age
    month = random.randint(1, 12)
    days_in_month = [31, 29 if year % 4 == 0 and month == 2 else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    day = random.randint(1, days_in_month[month - 1])
    months_ru = [
        "января", "февраля", "марта", "апреля", "мая", "июня",
        "июля", "августа", "сентября", "октября", "ноября", "декабря"
    ]
    return f"{day:02d} {months_ru[month - 1]} {year} г."

def generate_traits():
    return ", ".join(random.sample(PERSONALITY_TRAITS, k=3))

def generate_bio(data: dict) -> str:
    fio = data.get("fio", "Не указано")
    fam = fio.split()[-1] if len(fio.split()) > 1 else fio
    gender = data.get("gender", "Не указано")
    age = int(data.get("age", 18))
    birthdate = generate_birthdate(age)
    nationality = data.get("nationality", "Не указано")
    appearance = random.choice(APPEARANCES)
    traits = generate_traits()
    parents = generate_parents(fam)
    residence, birthplace = generate_address()

    # Итоговое оформление по шаблону Black Russia
    result = (
        "<b>Основная информация</b>\n\n"
        f"1. Имя, фамилия: {fio}\n"
        f"2. Пол: {gender}\n"
        f"3. Дата рождения: {birthdate}\n"
        f"4. Национальность: {nationality}\n"
        f"5. Место рождения: {birthplace}\n"
        f"6. Место проживания: {residence}\n"
        f"7. Черты характера и личные черты: {traits}\n"
        f"8. Описание внешности: {appearance}\n"
        f"9. Родители:\n"
        f"   - Отец: {parents['father']} ({parents['father_job']})\n"
        f"   - Мать: {parents['mother']} ({parents['mother_job']})\n"
    )
    return result

# --- ХЕНДЛЕРЫ ---
@dp.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "<b>Привет! Я бот для создания уникальных RP-биографий Black Russia.</b>\n\n"
        "Выбери действие 👇",
        reply_markup=main_menu_kb,
        parse_mode="HTML"
    )
    await state.set_state(MenuStates.waiting_main_menu)

@dp.message(MenuStates.waiting_main_menu)
async def handle_main_menu(message: types.Message, state: FSMContext):
    if message.text == "📝 Создать РП-биографию":
        await message.answer(
            "Выберите сервер:",
            reply_markup=server_kb,
            parse_mode="HTML"
        )
        await state.set_state(MenuStates.choosing_server)
    elif message.text == "📞 Связь с владельцем":
        text = (
            "🌟 <b>Связь с владельцем бота</b> 🌟\n\n"
            "📬 Возникли вопросы, предложения или хочешь предложить идею?\n"
            "Пиши мне в Telegram! Не стесняйся, я не кусаюсь 😉\n\n"
            "👉 <a href='https://t.me/bunkoc'>@bunkoc</a> 👈\n\n"
            "<i>Всегда на связи с моими пользователями!</i>\n"
            "P.S. Иногда я могу быть в оффлайне, но обязательно отвечу!"
        )
        await message.answer(text, reply_markup=main_menu_kb, parse_mode="HTML")

@dp.callback_query(MenuStates.choosing_server)
async def choose_server(callback: types.CallbackQuery, state: FSMContext):
    if callback.data == "server_red":
        await state.clear()
        await state.set_state(RedBioStates.waiting_name)
        await callback.message.answer("<b>1️⃣ Введите имя и фамилию персонажа:</b>\nПример: Иван Иванов", parse_mode="HTML")
    await callback.answer()

@dp.message(RedBioStates.waiting_name)
async def redbio_name(message: types.Message, state: FSMContext):
    fio = message.text.strip()
    await state.update_data(fio=fio)
    await state.set_state(RedBioStates.waiting_gender)
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Мужской")],
            [KeyboardButton(text="Женский")],
            [KeyboardButton(text="🏠 Главное меню")]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    await message.answer("<b>2️⃣ Укажите пол персонажа:</b>", reply_markup=kb, parse_mode="HTML")

@dp.message(RedBioStates.waiting_gender)
async def redbio_gender(message: types.Message, state: FSMContext):
    if message.text == "🏠 Главное меню":
        await cmd_start(message, state)
        return
    gender = message.text.strip()
    if gender.lower() not in ["мужской", "женский"]:
        await message.answer("Пожалуйста, выберите пол кнопкой ниже.")
        return
    await state.update_data(gender=gender.capitalize())
    await state.set_state(RedBioStates.waiting_age)
    await message.answer("<b>3️⃣ Укажите возраст персонажа (от 18 до 65):</b>", reply_markup=types.ReplyKeyboardRemove(), parse_mode="HTML")

@dp.message(RedBioStates.waiting_age)
async def redbio_age(message: types.Message, state: FSMContext):
    if message.text == "🏠 Главное меню":
        await cmd_start(message, state)
        return
    try:
        age = int(message.text.strip())
        if age < 18 or age > 65:
            raise ValueError
    except ValueError:
        await message.answer("⚠️ Укажите возраст числом от 18 до 65.")
        return
    await state.update_data(age=age)
    await state.set_state(RedBioStates.waiting_nationality)
    await message.answer("<b>4️⃣ Укажите национальность персонажа:</b>", parse_mode="HTML")

@dp.message(RedBioStates.waiting_nationality)
async def redbio_nationality(message: types.Message, state: FSMContext):
    if message.text == "🏠 Главное меню":
        await cmd_start(message, state)
        return
    nationality = message.text.strip().capitalize()
    await state.update_data(nationality=nationality)
    data = await state.get_data()
    bio = generate_bio(data)
    await message.answer("<b>Ваша уникальная RP-биография для сервера RED:</b>\n\n" + bio, parse_mode="HTML", reply_markup=main_menu_kb)
    await state.set_state(MenuStates.waiting_main_menu)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    import sys
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
