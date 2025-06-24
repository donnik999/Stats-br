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

# Клавиатура выбора сервера (RED и GREEN)
server_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="RED", callback_data="server_red"),
            InlineKeyboardButton(text="GREEN", callback_data="server_green")
        ]
    ]
)

# Состояния меню и анкет
class MenuStates(StatesGroup):
    waiting_main_menu = State()
    choosing_server = State()

class RedBioStates(StatesGroup):
    waiting_name = State()
    waiting_gender = State()
    waiting_age = State()
    waiting_nationality = State()

class GreenBioStates(StatesGroup):
    waiting_name = State()
    waiting_surname = State()
    waiting_parents = State()
    waiting_age = State()
    waiting_nationality = State()
    waiting_birthplace = State()
    waiting_residence = State()
    waiting_marital = State()
    waiting_children = State()
    waiting_gender = State()
    waiting_height = State()
    waiting_weight = State()
    waiting_eyecolor = State()
    waiting_hair = State()
    waiting_badhabits = State()
    waiting_character = State()

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
HAIR_COLORS = [
    "темные", "светлые", "русые", "черные", "каштановые", "рыжие"
]
EYE_COLORS = [
    "карие", "голубые", "зеленые", "серые", "черные"
]
CHARACTERS = [
    "Вежливый, уравновешенный, всегда готов прийти на помощь.",
    "Целеустремленный, трудолюбивый, обладает чувством юмора.",
    "Спокойный, рассудительный, умеет находить общий язык с людьми.",
    "Доброжелательный, честный, немного застенчивый.",
    "Общительный, энергичный, любит работать в команде."
]
BAD_HABITS = [
    "нет", "редко курит", "иногда опаздывает", "часто забывает мелочи", "любит поспать допоздна"
]
MARITALS = [
    "Холост/не замужем", "Женат/замужем", "В разводе", "В гражданском браке"
]
CHILDREN = [
    "Нет", "Один ребенок", "Двое детей", "Многодетная семья"
]
HOBBIES = [
    "чтение книг и прогулки на свежем воздухе",
    "занятия спортом, особенно футболом",
    "игра на гитаре и сочинение стихов",
    "рисование и фотография",
    "рыбалка и путешествия"
]
PARENT_VARIANTS = [
    "Отец — Иван, мать — Мария",
    "Отец — Александр, мать — Елена",
    "Отец — Сергей, мать — Ольга",
    "Отец — Виктор, мать — Светлана",
    "Отец — Михаил, мать — Наталья"
]

# --- ФУНКЦИИ ---
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

def generate_green_bio(data: dict) -> str:
    name = data.get("name", "Не указано")
    surname = data.get("surname", "Не указано")
    parents = data.get("parents", random.choice(PARENT_VARIANTS))
    age = int(data.get("age", 18))
    nationality = data.get("nationality", "Не указано")
    birthplace = data.get("birthplace", random.choice(CITIES))
    residence = data.get("residence", generate_address()[0])
    marital = data.get("marital", random.choice(MARITALS))
    children = data.get("children", random.choice(CHILDREN))
    gender = data.get("gender", "Не указано")
    height = data.get("height", f"{random.randint(165, 195)} см")
    weight = data.get("weight", f"{random.randint(55, 100)} кг")
    eye = data.get("eyecolor", random.choice(EYE_COLORS))
    hair = data.get("hair", random.choice(HAIR_COLORS))
    bad = data.get("badhabits", random.choice(BAD_HABITS))
    character = data.get("character", random.choice(CHARACTERS))

    # Блоки биографии (рандомные, можно расширять)
    childhood_blocks = [
        f"Детство прошло в городе {birthplace}, где {name} с ранних лет проявлял интерес к изучению окружающего мира.",
        "С детства отличался активностью, любил играть с друзьями и помогать родителям по хозяйству.",
        "Родители всегда поддерживали начинания и поощряли любопытство.",
        "В детстве посещал различные кружки и секции, был активным и любознательным ребенком."
    ]
    youth_blocks = [
        "В юности начал проявлять самостоятельность и интерес к спорту.",
        "Успешно закончил школу и поступил в колледж.",
        "С юных лет участвовал в городских мероприятиях и олимпиадах.",
        "В подростковом возрасте начал задумываться о будущем и строить первые планы."
    ]
    adulthood_blocks = [
        "Поступил в высшее учебное заведение, где приобрел много новых друзей.",
        "В период взросления начал работать, набирался жизненного опыта.",
        "Стал более ответственным и самостоятельным, учился принимать важные решения.",
        "Во взрослой жизни начал строить карьеру и задумываться о создании семьи."
    ]
    maturity_blocks = [
        "В зрелости достиг профессиональных успехов, стал примером для окружающих.",
        "Зрелость принесла новые цели и стремления, появилось желание помогать другим.",
        "Стал авторитетом в своем окружении, приобрел уважение коллег и знакомых.",
        "В этот период жизни научился ценить простые радости и заботиться о близких."
    ]
    now_blocks = [
        "В настоящее время продолжает развиваться и ставить перед собой новые задачи.",
        "Старается поддерживать здоровый образ жизни и гармонию в семье.",
        "Планирует в будущем реализовать новые проекты и достичь поставленных целей.",
        "Считает важным оставаться честным, справедливым и открытым человеком."
    ]

    childhood = random.choice(childhood_blocks)
    youth = random.choice(youth_blocks)
    adulthood = random.choice(adulthood_blocks)
    maturity = random.choice(maturity_blocks)
    now = random.choice(now_blocks)

    bio = (
        f"<b>Имя:</b> {name}\n"
        f"<b>Фамилия:</b> {surname}\n"
        f"<b>Родители:</b> {parents}\n"
        f"<b>Возраст:</b> {age}\n"
        f"<b>Национальность:</b> {nationality}\n"
        f"<b>Место рождения:</b> {birthplace}\n"
        f"<b>Место проживания:</b> {residence}\n"
        f"<b>Семейное положение:</b> {marital}\n"
        f"<b>Дети:</b> {children}\n"
        f"<b>Пол:</b> {gender}\n"
        f"<b>Рост:</b> {height}\n"
        f"<b>Вес:</b> {weight}\n"
        f"<b>Цвет глаз:</b> {eye}\n"
        f"<b>Волосы:</b> {hair}\n"
        f"<b>Плохие привычки:</b> {bad}\n"
        f"<b>Черты характера и личные качества:</b> {character}\n"
        f"<b>Личное фото:</b> (прикрепите изображение в отдельном сообщении)\n\n"
        f"<b>Детство:</b> {childhood}\n"
        f"<b>Юность:</b> {youth}\n"
        f"<b>Взросление:</b> {adulthood}\n"
        f"<b>Зрелость:</b> {maturity}\n"
        f"<b>Наши дни:</b> {now}"
    )
    return bio

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
            "Пиши мне в Telegram!\n\n"
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
    elif callback.data == "server_green":
        await state.clear()
        await state.set_state(GreenBioStates.waiting_name)
        await callback.message.answer("<b>1️⃣ Введите имя персонажа:</b>", parse_mode="HTML")
    await callback.answer()

# ----------- GREEN АНКЕТА ПОШАГОВО -----------
@dp.message(GreenBioStates.waiting_name)
async def greenbio_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text.strip())
    await state.set_state(GreenBioStates.waiting_surname)
    await message.answer("<b>2️⃣ Введите фамилию персонажа:</b>", parse_mode="HTML")

@dp.message(GreenBioStates.waiting_surname)
async def greenbio_surname(message: types.Message, state: FSMContext):
    await state.update_data(surname=message.text.strip())
    await state.set_state(GreenBioStates.waiting_parents)
    await message.answer("<b>3️⃣ Укажите родителей персонажа (пример: Отец — Иван, мать — Мария):</b>", parse_mode="HTML")

@dp.message(GreenBioStates.waiting_parents)
async def greenbio_parents(message: types.Message, state: FSMContext):
    await state.update_data(parents=message.text.strip())
    await state.set_state(GreenBioStates.waiting_age)
    await message.answer("<b>4️⃣ Введите возраст персонажа (от 18 до 65):</b>", parse_mode="HTML")

@dp.message(GreenBioStates.waiting_age)
async def greenbio_age(message: types.Message, state: FSMContext):
    try:
        age = int(message.text.strip())
        if age < 18 or age > 65:
            raise ValueError
    except ValueError:
        await message.answer("⚠️ Введите возраст числом от 18 до 65.")
        return
    await state.update_data(age=age)
    await state.set_state(GreenBioStates.waiting_nationality)
    await message.answer("<b>5️⃣ Укажите национальность персонажа:</b>", parse_mode="HTML")

@dp.message(GreenBioStates.waiting_nationality)
async def greenbio_nationality(message: types.Message, state: FSMContext):
    await state.update_data(nationality=message.text.strip())
    await state.set_state(GreenBioStates.waiting_birthplace)
    await message.answer("<b>6️⃣ Укажите место рождения персонажа:</b>", parse_mode="HTML")

@dp.message(GreenBioStates.waiting_birthplace)
async def greenbio_birthplace(message: types.Message, state: FSMContext):
    await state.update_data(birthplace=message.text.strip())
    await state.set_state(GreenBioStates.waiting_residence)
    await message.answer("<b>7️⃣ Укажите место проживания персонажа:</b>", parse_mode="HTML")

@dp.message(GreenBioStates.waiting_residence)
async def greenbio_residence(message: types.Message, state: FSMContext):
    await state.update_data(residence=message.text.strip())
    await state.set_state(GreenBioStates.waiting_marital)
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Холост/не замужем")],
            [KeyboardButton(text="Женат/замужем")],
            [KeyboardButton(text="В разводе")],
            [KeyboardButton(text="В гражданском браке")]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    await message.answer("<b>8️⃣ Семейное положение:</b>", reply_markup=kb, parse_mode="HTML")

@dp.message(GreenBioStates.waiting_marital)
async def greenbio_marital(message: types.Message, state: FSMContext):
    await state.update_data(marital=message.text.strip())
    await state.set_state(GreenBioStates.waiting_children)
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Нет")],
            [KeyboardButton(text="Один ребенок")],
            [KeyboardButton(text="Двое детей")],
            [KeyboardButton(text="Многодетная семья")]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    await message.answer("<b>9️⃣ Дети:</b>", reply_markup=kb, parse_mode="HTML")

@dp.message(GreenBioStates.waiting_children)
async def greenbio_children(message: types.Message, state: FSMContext):
    await state.update_data(children=message.text.strip())
    await state.set_state(GreenBioStates.waiting_gender)
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Мужской")],
            [KeyboardButton(text="Женский")]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    await message.answer("<b>🔟 Пол персонажа:</b>", reply_markup=kb, parse_mode="HTML")

@dp.message(GreenBioStates.waiting_gender)
async def greenbio_gender(message: types.Message, state: FSMContext):
    await state.update_data(gender=message.text.strip())
    await state.set_state(GreenBioStates.waiting_height)
    await message.answer("<b>1️⃣1️⃣ Рост персонажа (в см):</b>", reply_markup=types.ReplyKeyboardRemove(), parse_mode="HTML")

@dp.message(GreenBioStates.waiting_height)
async def greenbio_height(message: types.Message, state: FSMContext):
    await state.update_data(height=message.text.strip() + " см")
    await state.set_state(GreenBioStates.waiting_weight)
    await message.answer("<b>1️⃣2️⃣ Вес персонажа (в кг):</b>", parse_mode="HTML")

@dp.message(GreenBioStates.waiting_weight)
async def greenbio_weight(message: types.Message, state: FSMContext):
    await state.update_data(weight=message.text.strip() + " кг")
    await state.set_state(GreenBioStates.waiting_eyecolor)
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Карие")],
            [KeyboardButton(text="Голубые")],
            [KeyboardButton(text="Зеленые")],
            [KeyboardButton(text="Серые")],
            [KeyboardButton(text="Черные")]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    await message.answer("<b>1️⃣3️⃣ Цвет глаз:</b>", reply_markup=kb, parse_mode="HTML")

@dp.message(GreenBioStates.waiting_eyecolor)
async def greenbio_eyecolor(message: types.Message, state: FSMContext):
    await state.update_data(eyecolor=message.text.strip())
    await state.set_state(GreenBioStates.waiting_hair)
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Темные")],
            [KeyboardButton(text="Светлые")],
            [KeyboardButton(text="Русые")],
            [KeyboardButton(text="Черные")],
            [KeyboardButton(text="Каштановые")],
            [KeyboardButton(text="Рыжие")]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    await message.answer("<b>1️⃣4️⃣ Цвет волос:</b>", reply_markup=kb, parse_mode="HTML")

@dp.message(GreenBioStates.waiting_hair)
async def greenbio_hair(message: types.Message, state: FSMContext):
    await state.update_data(hair=message.text.strip())
    await state.set_state(GreenBioStates.waiting_badhabits)
    await message.answer("<b>1️⃣5️⃣ Плохие привычки (если есть):</b>", reply_markup=types.ReplyKeyboardRemove(), parse_mode="HTML")

@dp.message(GreenBioStates.waiting_badhabits)
async def greenbio_badhabits(message: types.Message, state: FSMContext):
    await state.update_data(badhabits=message.text.strip())
    await state.set_state(GreenBioStates.waiting_character)
    await message.answer("<b>1️⃣6️⃣ Опишите черты характера и личные качества:</b>", parse_mode="HTML")

@dp.message(GreenBioStates.waiting_character)
async def greenbio_character(message: types.Message, state: FSMContext):
    await state.update_data(character=message.text.strip())
    data = await state.get_data()
    bio = generate_green_bio(data)
    await message.answer("<b>Ваша уникальная RP-биография для сервера GREEN:</b>\n\n" + bio, parse_mode="HTML", reply_markup=main_menu_kb)
    await message.answer("<b>Внимание!</b>\n\nВ пункте <b>«Личное фото»</b> обязательно прикрепите изображение персонажа отдельным сообщением.", parse_mode="HTML")
    await state.set_state(MenuStates.waiting_main_menu)

# --------- RED АНКЕТА ---------
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
    # Используем старую генерацию для RED
    bio = generate_bio(await state.get_data())
    await message.answer("<b>Ваша уникальная RP-биография для сервера RED:</b>\n\n" + bio, parse_mode="HTML", reply_markup=main_menu_kb)
    await state.set_state(MenuStates.waiting_main_menu)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    import sys
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
