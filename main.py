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
        [InlineKeyboardButton(text="RED", callback_data="server_red")],
        [InlineKeyboardButton(text="GREEN", callback_data="server_green")]
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

# --- НАБОРЫ ДАННЫХ BLACK RUSSIA ---
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

JOBS = [
    "Инкассатор", "Рыболов", "Водолаз", "Механик", "Кладоискатель",
    "Работник на ферме", "Работник на заводе", "Работник на шахте",
    "МЧС", "Таксист", "Газовая служба", "Электрик", "Водитель автобуса"
]
ORGANIZATIONS = [
    "Центральная Больница", "ГИБДД", "УМВД", "СМИ", "Правительство",
    "ФСИН", "ФСБ", "Воинская Часть"
]

MALE_NAMES = [
    "Алексей", "Максим", "Виктор", "Сергей", "Игорь", "Владимир", "Евгений", "Дмитрий", "Олег", "Георгий"
]
FEMALE_NAMES = [
    "Марина", "Екатерина", "Ирина", "Анна", "Татьяна", "Ольга", "Валентина", "Елена", "Наталья", "Галина"
]

EYE_COLORS = [
    "карие", "голубые", "серые", "зеленые", "черные", "янтарные"
]
HAIR_COLORS = [
    "темные", "светлые", "русые", "каштановые", "черные", "седые"
]
BAD_HABITS = [
    "нет", "курение", "алкоголь", "азартные игры", "сквернословие", "опоздания"
]
FAMILY_STATUSES = [
    "Холост", "Женат", "Не замужем", "В разводе", "Вдова/Вдовец"
]
CHILDREN = [
    "нет", "один ребенок", "двое детей", "трое детей"
]
PERSONALITY_TRAITS = [
    "Ответственный, трудолюбивый, честный",
    "Добрый, отзывчивый, коммуникабельный",
    "Упрямый, амбициозный, прямолинейный",
    "Весёлый, с чувством юмора, энергичный",
    "Лидер, умеет работать в команде, пунктуален",
    "Стрессоустойчивый, рассудительный, спокойный"
]
APPEARANCES = [
    "Среднего роста, крепкого телосложения",
    "Высокий, спортивный",
    "Невысокий, худощавый",
    "Средний рост, выразительные черты лица",
    "Крупного телосложения, сдержанный взгляд"
]

# --- ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ---

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

def get_parent_fio(fam, gender):
    if gender == "мужской":
        name = random.choice(MALE_NAMES)
        return f"{name} {fam}"
    else:
        name = random.choice(FEMALE_NAMES)
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
        "father": f"{father} ({father_job})",
        "mother": f"{mother} ({mother_job})"
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

def random_height():
    return f"{random.randint(165, 200)} см"
def random_weight():
    return f"{random.randint(55, 110)} кг"

def random_children():
    return random.choice(CHILDREN)

def random_family_status():
    return random.choice(FAMILY_STATUSES)

def generate_traits():
    return random.choice(PERSONALITY_TRAITS)

def generate_life_block(stage, city):
    templates = {
        "Детство": [
            f"Детство героя прошло в городе {city}, где он рос в заботливой и дружной семье. С ранних лет родители старались привить ему любовь к труду и уважение к окружающим. Большую часть времени он проводил на свежем воздухе, играя с друзьями во дворе, катаясь на велосипеде и помогая старшим по хозяйству. Учился в местной школе, где проявлял большой интерес к литературе и истории, участвовал в школьных олимпиадах и художественной самодеятельности. Родители часто брали его с собой на прогулки по паркам и окрестностям города, что формировало в нем любовь к природе и животным.",
            f"С ранних лет живя в {city}, персонаж отличался любознательностью и активностью. Он всегда стремился узнать что-то новое, задавал вопросы взрослым и пробовал заниматься разными хобби: от рисования до спортивных игр на школьном дворе. В семье поддерживали его начинания, а дома царила атмосфера уюта, взаимопомощи и понимания. В детстве его окружали настоящие друзья, с которыми они устраивали совместные походы, играли в футбол и строили шалаши в лесу на окраине города.",
            f"В {city} детство прошло насыщенно и ярко. Родители уделяли много внимания воспитанию, прививали уважение к старшим и помогали раскрывать таланты. Герой с удовольствием посещал кружки и секции, принимал участие в городских конкурсах и праздниках. Особое место в его жизни занимали семейные вечера, когда за столом собирались все родственники, делились новостями и строили планы на будущее."
        ],
        "Юность": [
            f"Юность была временем поиска себя и новых открытий. В школе герой проявлял лидерские качества, участвовал в работе школьного совета, организовывал мероприятия и спортивные состязания. В этот период он начал серьезно заниматься спортом, добился успехов на районных соревнованиях и приобрёл много друзей. Юность в {city} была наполнена яркими событиями: первые влюбленности, победы и поражения, совместные прогулки по вечерам, мечты о будущем и желание сделать жизнь ярче.",
            f"В юности персонаж продолжал развиваться, расширяя круг своих интересов. Он увлекся музыкой, играл в школьной группе и выступал на городских концертах. Важное место занимала учеба: он стремился к высоким результатам, чтобы поступить в престижный колледж. В свободное время занимался волонтерством, помогал организовывать праздники и активно участвовал в жизни города {city}.",
            f"Этот этап жизни был наполнен новыми знакомствами и испытаниями. Герой научился преодолевать трудности, стал более самостоятельным и ответственным. Юность стала временем первых серьёзных решений, когда выбирался путь на будущее, закладывались основы для профессионального роста и формировались жизненные ценности."
        ],
        "Взросление": [
            f"После окончания школы герой поступил в колледж, где получил востребованную специальность. Параллельно с учёбой начал подрабатывать, чтобы быть независимым и приобретать опыт. В этот период он впервые столкнулся с настоящими трудностями: самостоятельное ведение быта, распределение бюджета, совмещение работы и учёбы. Однако все испытания только укрепили его характер, научили ставить цели и добиваться их.",
            f"Став взрослее, персонаж нашёл первую серьёзную работу, начал строить карьеру и заводить новые знакомства. В работе проявил себя как ответственный и трудолюбивый сотрудник, за что получил признание коллег и руководства. Научился ценить дружбу, поддерживать отношения с близкими, заботиться о семье и помогать родителям.",
            f"Взросление сопровождалось постоянным саморазвитием: герой читал много профессиональной литературы, посещал тренинги, занимался спортом. В этот период появилась уверенность в себе, сформировались амбиции и стремление к достижению новых вершин."
        ],
        "Зрелость": [
            f"В зрелом возрасте герой добился многого: построил карьеру, обрёл уважение среди друзей и коллег. Он научился быть мудрым и рассудительным, помогать молодым сотрудникам, делиться опытом и поддерживать инициативы. Зрелость принесла стабильность, уверенность в завтрашнем дне и возможность реализовать давние мечты.",
            f"В этот период жизни герой активно участвовал в общественной жизни города {city}. Был организатором городских мероприятий, занимался благотворительностью и поддерживал социальные проекты. Зрелость стала временем гармонии, когда появились свои традиции, семейные праздники и уютный дом.",
            f"Став зрелым, персонаж нашёл баланс между работой и личной жизнью. Он с удовольствием проводил время с семьёй, путешествовал, занимался любимыми хобби. В этот период научился ценить простые радости, уделять внимание здоровью и заботиться о будущем детей."
        ],
        "Наши дни": [
            f"В настоящее время герой продолжает заниматься любимым делом, достигает новых успехов в работе и личной жизни. Он не забывает об интересах общества, помогает нуждающимся, участвует в волонтёрских программах и поддерживает молодое поколение. Уверенно смотрит в будущее, стремится к новым вершинам и верит, что впереди его ждёт много интересных событий.",
            f"Сегодня персонаж живёт насыщенной жизнью, реализует свои профессиональные и личные планы. Считает, что главное — это честность, трудолюбие и уважение к другим людям. Не боится перемен, легко адаптируется к новым условиям и всегда готов к новым вызовам.",
            f"В наши дни герой окружён любящими людьми, дорожит семейными ценностями и поддерживает тёплые отношения с друзьями. Он находит время для саморазвития, чтения и спорта, стремится быть полезным обществу и делает всё возможное для благополучия родных."
        ]
    }
    return random.choice(templates.get(stage, [""]))

def generate_bio_red(data: dict) -> str:
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
        f"   - Отец: {parents['father']}\n"
        f"   - Мать: {parents['mother']}\n"
    )
    return result

def generate_bio_green(data: dict) -> str:
    fio = data.get("fio", "Не указано")
    fam = fio.split()[-1] if len(fio.split()) > 1 else fio
    gender = data.get("gender", "Не указано")
    age = int(data.get("age", 18))
    nationality = data.get("nationality", "Не указано")
    parents = generate_parents(fam)
    residence, birthplace = generate_address()
    family_status = random_family_status()
    children = random_children()
    height = random_height()
    weight = random_weight()
    eyes = random.choice(EYE_COLORS)
    hair = random.choice(HAIR_COLORS)
    bad_habit = random.choice(BAD_HABITS)
    traits = generate_traits()
    appearance = random.choice(APPEARANCES)
    childhood = generate_life_block("Детство", birthplace)
    youth = generate_life_block("Юность", birthplace)
    adulthood = generate_life_block("Взросление", birthplace)
    maturity = generate_life_block("Зрелость", birthplace)
    present = generate_life_block("Наши дни", birthplace)
    result = (
        f"<b>Имя:</b> {fio.split()[0] if len(fio.split()) > 1 else fio}\n"
        f"<b>Фамилия:</b> {fam}\n"
        f"<b>Родители:</b>\n"
        f"   - Отец: {parents['father']}\n"
        f"   - Мать: {parents['mother']}\n"
        f"<b>Возраст:</b> {age}\n"
        f"<b>Национальность:</b> {nationality}\n"
        f"<b>Место рождения:</b> {birthplace}\n"
        f"<b>Место проживания:</b> {residence}\n"
        f"<b>Семейное положение:</b> {family_status}\n"
        f"<b>Дети:</b> {children}\n"
        f"<b>Пол:</b> {gender}\n"
        f"<b>Рост:</b> {height}\n"
        f"<b>Вес:</b> {weight}\n"
        f"<b>Цвет глаз:</b> {eyes}\n"
        f"<b>Волосы:</b> {hair}\n"
        f"<b>Плохие привычки:</b> {bad_habit}\n"
        f"<b>Черты характера и личные качества:</b> {traits}\n"
        f"<b>Личное фото:</b> <i>прикрепить фото...</i>\n\n"
        f"<b>Детство:</b> {childhood}\n"
        f"<b>Юность:</b> {youth}\n"
        f"<b>Взросление:</b> {adulthood}\n"
        f"<b>Зрелость:</b> {maturity}\n"
        f"<b>Наши дни:</b> {present}"
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
    elif callback.data == "server_green":
        await state.clear()
        await state.set_state(GreenBioStates.waiting_name)
        await callback.message.answer("<b>1️⃣ Введите имя и фамилию персонажа:</b>\nПример: Иван Иванов", parse_mode="HTML")
    await callback.answer()

# --- RED ---
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

# --- GREEN ---
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

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    import sys
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
