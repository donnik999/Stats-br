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
        [KeyboardButton("📝 Создать РП-биографию")],
        [KeyboardButton("📞 Связь с владельцем")]
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

# --- СПРАВОЧНИКИ ---
CITIES = [
    "Арзамас", "Южный", "Батырево", "Лыткарино", "Морское",
    "Бусаево", "Горки", "Новый Арзамас", "Приволжск"
]
STREETS = [
    "Центральная", "Лесная", "Советская", "Солнечная", "Молодёжная",
    "Шоссейная", "Парковая", "Победы", "Гагарина", "Мира",
    "Озерная", "Набережная", "Заречная", "Трудовая", "Северная"
]
APPEARANCES = [
    "Высокий, стройный, темные волосы, карие глаза, аккуратная стрижка.",
    "Среднего роста, крепкое телосложение, светлые волосы, голубые глаза.",
    "Крупного телосложения, русые волосы, выразительные черты лица.",
    "Невысокий, спортивный, короткие темные волосы, серые глаза.",
    "Средний рост, светлая кожа, добродушная улыбка, зеленые глаза."
]
CHARACTERS = [
    "Вежливый и уравновешенный, всегда готов прийти на помощь.",
    "Целеустремленный, трудолюбивый, обладает чувством юмора.",
    "Спокойный, рассудительный, умеет находить общий язык с людьми.",
    "Доброжелательный, честный, немного застенчивый.",
    "Общительный, энергичный, любит работать в команде."
]
HOBBIES = [
    "чтение книг и прогулки на свежем воздухе",
    "занятия спортом, особенно футболом",
    "игра на гитаре и сочинение стихов",
    "рисование и фотография",
    "рыбалка и путешествия"
]

def generate_address():
    city = random.choice(CITIES)
    street = random.choice(STREETS)
    house = random.randint(1, 99)
    apt = random.randint(1, 120)
    return f"г. {city}, ул. {street}, д. {house}, кв. {apt}", city

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

def generate_bio(data: dict) -> str:
    fio = data.get("fio", "Не указано")
    gender = data.get("gender", "Не указано")
    age = int(data.get("age", 18))
    birthdate = generate_birthdate(age)
    nationality = data.get("nationality", "Не указано")
    residence, birthplace = generate_address()
    appearance = random.choice(APPEARANCES)
    character = random.choice(CHARACTERS)
    hobby = random.choice(HOBBIES)

    # Блоки биографии (без повторов адреса!)
    childhood_youth_blocks = [
        f"Родился в городе {birthplace}. С ранних лет проявлял интерес к новым знаниям, много времени проводил на улице с друзьями.",
        "В детстве отличался любопытством и активностью, любил играть в подвижные игры и помогать родителям по дому.",
        "Школьные годы прошли насыщенно: участвовал в олимпиадах, занимался спортом и был активистом в классе.",
        "С самого раннего возраста проявлял уважение к окружающим, был воспитан в атмосфере взаимопомощи и поддержки.",
        "В подростковом возрасте начал интересоваться техникой и творчеством, посещал кружки и секции."
    ]
    adulthood_blocks = [
        "После окончания школы поступил в колледж, где получил профессию по душе.",
        "Начал строить карьеру, трудился на разных работах, набирался опыта и знаний.",
        "Взрослая жизнь принесла свои испытания, но благодаря настойчивости удалось добиться первых успехов.",
        "Стремился к саморазвитию, продолжал учиться и совершенствовать свои навыки.",
        "В этот период приобрёл много друзей и единомышленников, участвовал в общественной жизни города."
    ]
    present_blocks = [
        f"Продолжает заниматься любимым делом, не забывая уделять время {hobby}.",
        "Старается быть полезным обществу и поддерживать добрые отношения с окружающими.",
        "Планирует в будущем реализовать свои идеи и внести вклад в развитие города.",
        "Считает, что главное — это честность, трудолюбие и уважение к другим людям."
    ]

    childhood_youth = "\n".join(random.sample(childhood_youth_blocks, 3))
    adulthood = "\n".join(random.sample(adulthood_blocks, 2))
    present = "\n".join(random.sample(present_blocks, 2))

    # Итоговое оформление по шаблону, без повторов адреса!
    result = (
        "<b>Основная информация</b>\n\n"
        f"1. Имя, фамилия: {fio}\n"
        f"2. Пол: {gender}\n"
        f"3. Дата рождения: {birthdate}\n"
        f"4. Национальность: {nationality}\n"
        f"5. Место рождения: {birthplace}\n"
        f"6. Место проживания: {residence}\n"
        f"7. Описание внешности: {appearance}\n"
        f"8. Особенности характера: {character}\n"
        f"9. Хобби: {hobby}\n\n"
        "<b>Биография гражданина</b>\n\n"
        f"1. Детство и юность:\n{childhood_youth}\n\n"
        f"2. Взрослая жизнь:\n{adulthood}\n\n"
        f"3. Настоящее время:\n{present}"
    )
    return result

# --- ХЕНДЛЕРЫ ---
@dp.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "<b>Привет! Я бот для создания уникальных RP-биографий.</b>\n\n"
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
        keyboard=[[KeyboardButton("Мужской")], [KeyboardButton("Женский")], [KeyboardButton("🏠 Главное меню")]],
        resize_keyboard=True, one_time_keyboard=True
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
