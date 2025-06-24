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

main_menu_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📝 Создать РП-биографию")],
        [KeyboardButton(text="📞 Связь с владельцем")]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

server_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="RED", callback_data="server_red")],
        [InlineKeyboardButton(text="GREEN", callback_data="server_green")],
        [InlineKeyboardButton(text="BLUE", callback_data="server_blue")],
        [InlineKeyboardButton(text="YELLOW", callback_data="server_yellow")],
        [InlineKeyboardButton(text="ORANGE", callback_data="server_orange")]
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

class GreenBioStates(StatesGroup):
    waiting_name = State()
    waiting_gender = State()
    waiting_age = State()
    waiting_nationality = State()

class BlueBioStates(StatesGroup):
    waiting_name = State()
    waiting_gender = State()
    waiting_age = State()
    waiting_nationality = State()

class YellowBioStates(StatesGroup):
    waiting_name = State()
    waiting_gender = State()
    waiting_age = State()
    waiting_nationality = State()

class OrangeBioStates(StatesGroup):
    waiting_name = State()
    waiting_age = State()
    waiting_nationality = State()

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

MALE_PARENT_NAMES = [
    "Иван", "Сергей", "Александр", "Виктор", "Денис", "Максим", "Дмитрий", "Павел", "Андрей", "Владимир",
    "Егор", "Анатолий", "Олег", "Георгий", "Григорий", "Петр", "Николай", "Константин", "Ярослав", "Артём"
]
FEMALE_PARENT_NAMES = [
    "Мария", "Екатерина", "Ирина", "Анна", "Татьяна", "Ольга", "Валентина", "Елена", "Наталья", "Галина",
    "Светлана", "Любовь", "Вера", "Людмила", "Дарья", "Ксения", "Алиса", "Полина", "Василиса", "Яна"
]

EYE_COLORS = [
    "карие", "голубые", "серые", "зеленые", "черные", "янтарные", "синие"
]
HAIR_COLORS = [
    "темные", "светлые", "русые", "каштановые", "черные", "седые", "темно-русые"
]

def get_random_location():
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

def get_female_last_name(fam):
    fam = fam.strip()
    if fam.endswith("ий"):
        fam_f = fam[:-2] + "ая"
    elif fam.endswith("ый"):
        fam_f = fam[:-2] + "ая"
    elif fam.endswith("ой"):
        fam_f = fam[:-2] + "ая"
    elif fam.endswith("ов") or fam.endswith("ев") or fam.endswith("ин"):
        fam_f = fam + "а"
    elif fam.endswith("ский"):
        fam_f = fam[:-4] + "ская"
    else:
        fam_f = fam
        if not fam_f.endswith("а"):
            fam_f += "а"
    return fam_f

def random_date_of_birth(age: int):
    today = datetime.today()
    year = today.year - age
    month = random.randint(1, 12)
    if month == 2:
        days = 29 if year % 4 == 0 else 28
    elif month in [4, 6, 9, 11]:
        days = 30
    else:
        days = 31
    day = random.randint(1, days)
    return f"{day:02d}.{month:02d}.{year}"

def random_height():
    return f"{random.randint(165, 200)} см"
def random_weight():
    return f"{random.randint(55, 110)} кг"

def random_appearance():
    return f"Глаза {random.choice(EYE_COLORS)}, волосы {random.choice(HAIR_COLORS)}, вес {random.randint(60, 90)} кг, рост {random.randint(165, 195)} см."

def random_character():
    return (
        f"{random.choice(['Спокойный', 'Оптимистичный', 'Решительный', 'Доброжелательный', 'Честный', 'Настойчивый'])}, "
        f"{random.choice(['целеустремленный', 'отзывчивый', 'аккуратный', 'эмпатичный', 'трудолюбивый'])}, "
        f"{random.choice(['с поддерживающим характером', 'с чувством юмора', 'умеет слушать', 'иногда бывает замкнутым'])}."
    )

CHILDHOOD_BLOCKS = [
    "Мое детство прошло в небольшом городе, где все друг друга знали. Я был активным и любознательным ребенком — играл во дворе, катался на велосипеде, устраивал с друзьями состязания на скорость. Отец часто брал меня на рыбалку, а мама поддерживала любые мои увлечения, развивая мои таланты. В садике у меня было немало друзей, а воспитательница стала для меня второй мамой. В школе я был любознательным мальчиком, участвовал в олимпиадах, много читал. За шалости бывало получал выговор, но всегда оставался любимчиком класса.",
    "Я родился в дружной семье, где меня окружали заботой и вниманием. Мои родители всегда старались дать мне все самое лучшее. С раннего детства я был очень энергичным: устраивал во дворе соревнования, играл в футбол, помогал родителям по хозяйству. Отец научил меня рыбалке, а мама поддерживала мои творческие увлечения. В школе учился хорошо, любил участвовать в конкурсах, иногда хулиганил с друзьями. Особое удовольствие мне доставляло чтение приключенческих книг.",
]

YOUTH_BLOCKS = [
    "Юность была временем открытий и формирования характера. Я все больше увлекался спортом, особенно футболом — мы играли до темноты, забывая обо всем. В старших классах полюбил точные науки и решил связать свою жизнь с инженерией. Поступил в университет, где много учился и участвовал в проектах. После вуза устроился на работу мечты, научился ответственности и самостоятельности, начал путешествовать по разным странам, знакомился с интересными людьми и культурами.",
    "В 18 лет я отправился в армию, где прошел через множество испытаний — служба закалила характер и научила принимать решения. После армии поступил на работу в силовые структуры, где быстро продвигался по службе благодаря упорству. Параллельно нашел любовь, создал семью, начал арендовать квартиру для будущих детей. Каждый этап взрослой жизни приносил новые знания и опыт, укрепляя веру в себя.",
]

PRESENT_BLOCKS = [
    "Сейчас я работаю по специальности, занимаюсь любимым делом и продолжаю учиться. Активно занимаюсь спортом, участвую в забегах, поддерживаю здоровье. Люблю путешествовать и открывать новые места. В кругу друзей и семьи черпаю вдохновение и силы, а в редкие минуты отдыха читаю или занимаюсь кулинарией. Чувствую себя уверенно и с оптимизмом смотрю в будущее.",
    "Сегодня я счастливый семьянин, строю карьеру, воспитываю детей, продолжаю развиваться личностно и профессионально. Веду активную жизнь, бегаю, изучаю новые науки, отдыхаю на природе. Люблю проводить время с близкими, а хобби помогают мне отвлечься от рутины и получать радость от жизни.",
]

# === Генераторы (примерно как выше, для каждого сервера) ===
def generate_bio_red(data):
    fio = data.get("fio", "Не указано")
    fam = fio.split()[-1] if len(fio.split()) > 1 else fio
    gender = data.get("gender", "Не указано")
    age = int(data.get("age", 18))
    nationality = data.get("nationality", "Не указано")
    birthdate = random_date_of_birth(age)
    residence, birthplace = generate_address()
    appearance = random_appearance()
    character = random_character()
    childhood = random.choice(CHILDHOOD_BLOCKS)
    youth = random.choice(YOUTH_BLOCKS)
    present = random.choice(PRESENT_BLOCKS)
    return (
        f"<b>Имя Фамилия:</b> {fio}\n"
        f"<b>Пол:</b> {gender}\n"
        f"<b>Национальность:</b> {nationality}\n"
        f"<b>Возраст:</b> {age}\n"
        f"<b>Дата рождения:</b> {birthdate}\n"
        f"<b>Место рождения:</b> {birthplace}\n"
        f"<b>Место проживания:</b> {residence}\n"
        f"<b>Описание внешности:</b> {appearance}\n"
        f"<b>Особенности характера:</b> {character}\n"
        f"<b>Детство:</b> {childhood}\n"
        f"<b>Юность и взрослая жизнь:</b> {youth}\n"
        f"<b>Настоящее время:</b> {present}"
    )

def generate_bio_green(data):
    # Просто пример — можешь заменить содержимое на свой вариант
    return generate_bio_red(data)

def generate_bio_blue(data):
    # Просто пример — можешь заменить содержимое на свой вариант
    return generate_bio_red(data)

def generate_bio_yellow(data):
    fio = data.get("fio", "Не указано")
    fam = fio.split()[-1] if len(fio.split()) > 1 else fio
    gender = data.get("gender", "Не указано")
    nationality = data.get("nationality", "Не указано")
    age = int(data.get("age", 18))
    birth_and_place = f"{random_date_of_birth(age)} г., {get_random_location()}"
    residence, _ = generate_address()
    appearance = random_appearance()
    character = random_character()
    childhood = random.choice(CHILDHOOD_BLOCKS)
    youth_life = random.choice(YOUTH_BLOCKS)
    present = random.choice(PRESENT_BLOCKS)
    return (
        f"<b>Имя Фамилия:</b> {fio}\n"
        f"<b>Пол:</b> {gender}\n"
        f"<b>Национальность:</b> {nationality}\n"
        f"<b>Возраст:</b> {age}\n"
        f"<b>Дата и место рождения:</b> {birth_and_place}\n"
        f"<b>Место текущего проживания:</b> {residence}\n"
        f"<b>Описание внешности:</b> {appearance}\n"
        f"<b>Особенности характера:</b> {character}\n"
        f"<b>Детство:</b> {childhood}\n"
        f"<b>Юность и взрослая жизнь:</b> {youth_life}\n"
        f"<b>Настоящее время:</b> {present}"
    )

def generate_bio_orange(data):
    fio = data.get("fio", "Не указано")
    age = int(data.get("age", 18))
    nationality = data.get("nationality", "Не указано")
    birth_and_place = f"{random_date_of_birth(age)} г., {get_random_location()}"
    residence, _ = generate_address()
    appearance = random_appearance()
    character = random_character()
    childhood = random.choice(CHILDHOOD_BLOCKS)
    youth_life = random.choice(YOUTH_BLOCKS)
    present = random.choice(PRESENT_BLOCKS)
    return (
        f"<b>Имя Фамилия:</b> {fio}\n"
        f"<b>Национальность:</b> {nationality}\n"
        f"<b>Возраст:</b> {age}\n"
        f"<b>Дата и место рождения:</b> {birth_and_place}\n"
        f"<b>Место текущего проживания:</b> {residence}\n"
        f"<b>Описание внешности:</b> {appearance}\n"
        f"<b>Особенности характера:</b> {character}\n"
        f"<b>Детство:</b> {childhood}\n"
        f"<b>Юность и взрослая жизнь:</b> {youth_life}\n"
        f"<b>Настоящее время:</b> {present}"
    )

# === FSM для всех серверов ===
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
    elif callback.data == "server_green":
        await state.clear()
        await state.set_state(GreenBioStates.waiting_name)
        await callback.message.answer("<b>1️⃣ Введите имя и фамилию персонажа:</b>\nПример: Иван Иванов", parse_mode="HTML")
    elif callback.data == "server_blue":
        await state.clear()
        await state.set_state(BlueBioStates.waiting_name)
        await callback.message.answer("<b>1️⃣ Введите имя и фамилию персонажа:</b>\nПример: Иван Иванов", parse_mode="HTML")
    elif callback.data == "server_yellow":
        await state.clear()
        await state.set_state(YellowBioStates.waiting_name)
        await callback.message.answer("<b>1️⃣ Введите имя и фамилию персонажа:</b>\nПример: Иван Иванов", parse_mode="HTML")
    elif callback.data == "server_orange":
        await state.clear()
        await state.set_state(OrangeBioStates.waiting_name)
        await callback.message.answer("<b>1️⃣ Введите имя и фамилию персонажа:</b>\nПример: Иван Иванов", parse_mode="HTML")
    await callback.answer()

# RED
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
    bio = generate_bio_red(data)
    await message.answer("<b>Ваша уникальная RP-биография для сервера RED:</b>\n\n" + bio, parse_mode="HTML", reply_markup=main_menu_kb)
    await state.set_state(MenuStates.waiting_main_menu)

# GREEN
@dp.message(GreenBioStates.waiting_name)
async def greenbio_name(message: types.Message, state: FSMContext):
    fio = message.text.strip()
    await state.update_data(fio=fio)
    await state.set_state(GreenBioStates.waiting_gender)
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

@dp.message(GreenBioStates.waiting_gender)
async def greenbio_gender(message: types.Message, state: FSMContext):
    if message.text == "🏠 Главное меню":
        await cmd_start(message, state)
        return
    gender = message.text.strip()
    if gender.lower() not in ["мужской", "женский"]:
        await message.answer("Пожалуйста, выберите пол кнопкой ниже.")
        return
    await state.update_data(gender=gender.capitalize())
    await state.set_state(GreenBioStates.waiting_age)
    await message.answer("<b>3️⃣ Укажите возраст персонажа (от 18 до 65):</b>", reply_markup=types.ReplyKeyboardRemove(), parse_mode="HTML")

@dp.message(GreenBioStates.waiting_age)
async def greenbio_age(message: types.Message, state: FSMContext):
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
    await state.set_state(GreenBioStates.waiting_nationality)
    await message.answer("<b>4️⃣ Укажите национальность персонажа:</b>", parse_mode="HTML")

@dp.message(GreenBioStates.waiting_nationality)
async def greenbio_nationality(message: types.Message, state: FSMContext):
    if message.text == "🏠 Главное меню":
        await cmd_start(message, state)
        return
    nationality = message.text.strip().capitalize()
    await state.update_data(nationality=nationality)
    data = await state.get_data()
    bio = generate_bio_green(data)
    await message.answer("<b>Ваша уникальная RP-биография для сервера GREEN:</b>\n\n" + bio, parse_mode="HTML", reply_markup=main_menu_kb)
    await state.set_state(MenuStates.waiting_main_menu)

# BLUE
@dp.message(BlueBioStates.waiting_name)
async def bluebio_name(message: types.Message, state: FSMContext):
    fio = message.text.strip()
    await state.update_data(fio=fio)
    await state.set_state(BlueBioStates.waiting_gender)
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

@dp.message(BlueBioStates.waiting_gender)
async def bluebio_gender(message: types.Message, state: FSMContext):
    if message.text == "🏠 Главное меню":
        await cmd_start(message, state)
        return
    gender = message.text.strip()
    if gender.lower() not in ["мужской", "женский"]:
        await message.answer("Пожалуйста, выберите пол кнопкой ниже.")
        return
    await state.update_data(gender=gender.capitalize())
    await state.set_state(BlueBioStates.waiting_age)
    await message.answer("<b>3️⃣ Укажите возраст персонажа (от 16 до 65):</b>", reply_markup=types.ReplyKeyboardRemove(), parse_mode="HTML")

@dp.message(BlueBioStates.waiting_age)
async def bluebio_age(message: types.Message, state: FSMContext):
    if message.text == "🏠 Главное меню":
        await cmd_start(message, state)
        return
    try:
        age = int(message.text.strip())
        if age < 16 or age > 65:
            raise ValueError
    except ValueError:
        await message.answer("⚠️ Укажите возраст числом от 16 до 65.")
        return
    await state.update_data(age=age)
    await state.set_state(BlueBioStates.waiting_nationality)
    await message.answer("<b>4️⃣ Укажите национальность персонажа:</b>", parse_mode="HTML")

@dp.message(BlueBioStates.waiting_nationality)
async def bluebio_nationality(message: types.Message, state: FSMContext):
    if message.text == "🏠 Главное меню":
        await cmd_start(message, state)
        return
    nationality = message.text.strip().capitalize()
    await state.update_data(nationality=nationality)
    data = await state.get_data()
    bio = generate_bio_blue(data)
    await message.answer("<b>Ваша уникальная RP-биография для сервера BLUE:</b>\n\n" + bio, parse_mode="HTML", reply_markup=main_menu_kb)
    await state.set_state(MenuStates.waiting_main_menu)

# YELLOW
@dp.message(YellowBioStates.waiting_name)
async def yellowbio_name(message: types.Message, state: FSMContext):
    fio = message.text.strip()
    await state.update_data(fio=fio)
    await state.set_state(YellowBioStates.waiting_gender)
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

@dp.message(YellowBioStates.waiting_gender)
async def yellowbio_gender(message: types.Message, state: FSMContext):
    if message.text == "🏠 Главное меню":
        await cmd_start(message, state)
        return
    gender = message.text.strip()
    if gender.lower() not in ["мужской", "женский"]:
        await message.answer("Пожалуйста, выберите пол кнопкой ниже.")
        return
    await state.update_data(gender=gender.capitalize())
    await state.set_state(YellowBioStates.waiting_age)
    await message.answer("<b>3️⃣ Укажите возраст персонажа (от 16 до 65):</b>", reply_markup=types.ReplyKeyboardRemove(), parse_mode="HTML")

@dp.message(YellowBioStates.waiting_age)
async def yellowbio_age(message: types.Message, state: FSMContext):
    if message.text == "🏠 Главное меню":
        await cmd_start(message, state)
        return
    try:
        age = int(message.text.strip())
        if age < 16 or age > 65:
            raise ValueError
    except ValueError:
        await message.answer("⚠️ Укажите возраст числом от 16 до 65.")
        return
    await state.update_data(age=age)
    await state.set_state(YellowBioStates.waiting_nationality)
    await message.answer("<b>4️⃣ Укажите национальность персонажа:</b>", parse_mode="HTML")

@dp.message(YellowBioStates.waiting_nationality)
async def yellowbio_nationality(message: types.Message, state: FSMContext):
    if message.text == "🏠 Главное меню":
        await cmd_start(message, state)
        return
    nationality = message.text.strip().capitalize()
    await state.update_data(nationality=nationality)
    data = await state.get_data()
    bio = generate_bio_yellow(data)
    await message.answer("<b>Ваша уникальная RP-биография для сервера YELLOW:</b>\n\n" + bio, parse_mode="HTML", reply_markup=main_menu_kb)
    await state.set_state(MenuStates.waiting_main_menu)

# ORANGE
@dp.message(OrangeBioStates.waiting_name)
async def orangebio_name(message: types.Message, state: FSMContext):
    fio = message.text.strip()
    await state.update_data(fio=fio)
    await state.set_state(OrangeBioStates.waiting_age)
    await message.answer("<b>2️⃣ Укажите возраст персонажа (от 16 до 65):</b>", parse_mode="HTML")

@dp.message(OrangeBioStates.waiting_age)
async def orangebio_age(message: types.Message, state: FSMContext):
    try:
        age = int(message.text.strip())
        if age < 16 or age > 65:
            raise ValueError
    except ValueError:
        await message.answer("⚠️ Укажите возраст числом от 16 до 65.")
        return
    await state.update_data(age=age)
    await state.set_state(OrangeBioStates.waiting_nationality)
    await message.answer("<b>3️⃣ Укажите национальность персонажа:</b>", parse_mode="HTML")

@dp.message(OrangeBioStates.waiting_nationality)
async def orangebio_nationality(message: types.Message, state: FSMContext):
    nationality = message.text.strip().capitalize()
    await state.update_data(nationality=nationality)
    data = await state.get_data()
    bio = generate_bio_orange(data)
    await message.answer("<b>Ваша уникальная RP-биография для сервера ORANGE:</b>\n\n" + bio, parse_mode="HTML", reply_markup=main_menu_kb)
    await state.set_state(MenuStates.waiting_main_menu)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    import sys
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
