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

def random_appearance():
    return random.choice(APPEARANCES)

# ========== RED RP BIO (оставить как было ранее) ==========
def generate_bio_red(data: dict) -> str:
    fio = data.get("fio", "Не указано")
    fam = fio.split()[-1] if len(fio.split()) > 1 else fio
    gender = data.get("gender", "Не указано")
    age = int(data.get("age", 18))
    birthdate = generate_birthdate(age)
    nationality = data.get("nationality", "Не указано")
    appearance = random_appearance()
    traits = generate_traits()
    parents = generate_parents(fam)
    residence, birthplace = generate_address()
    childhood = "С самого рождения был окружён любовью и заботой родителей. В детстве учился ценить труд, уважать других, много времени проводил с семьёй, был любознателен и активен."
    adulthood = "После окончания школы поступил в колледж, затем служил в армии. Вернувшись, начал трудовую деятельность, строил карьеру и заводил новые знакомства. Постепенно нашёл своё призвание."
    present = "В настоящее время работаю по профессии, есть круг друзей и родных. Живу в гармонии с собой, стремлюсь к развитию и помогаю близким."
    result = (
        "<b>Основная информация</b>\n\n"
        f"1. Имя, фамилия: {fio}\n"
        f"2. Пол: {gender}\n"
        f"3. Дата рождения: {birthdate}\n"
        f"4. Национальность: {nationality}\n"
        f"5. Место рождения: {birthplace}\n"
        f"6. Место проживания: {residence}\n"
        f"7. Описание внешности: {appearance}\n"
        f"8. Особенности характера: {traits}\n"
        f"9. Родители:\n"
        f"   - Отец: {parents['father']}\n"
        f"   - Мать: {parents['mother']}\n\n"
        "<b>Биография гражданина</b>\n\n"
        f"1. Детство и юность: {childhood}\n"
        f"2. Взрослая жизнь: {adulthood}\n"
        f"3. Настоящее время: {present}\n"
    )
    return result

# ========== GREEN RP BIO (НОВЫЙ ФОРУМНЫЙ СТИЛЬ) ==========
# Примеры для каждого этапа жизни
GREEN_CHILDHOOD = [
    "С самого рождения был окружён любовью родителей, которые делали всё, чтобы я вырос достойным человеком. Наш дом отличался уютом и теплом. Отец с детства учил меня ценить труд, а мама — быть добрым и справедливым. Я часто бывал с отцом на его работе и помогал маме в её кондитерской лавке. Уже в детстве понял: чтобы чего-то добиться, нужно много работать.",
    "Родился и вырос в городе {city}, окружённом живописной природой. Был энергичным мальчиком: с друзьями гулял на улице, исследовал лесные тропинки. В детском саду завёл много друзей, а в школе учёба давалась легко благодаря поддержке семьи, особенно бабушки, которая приучила меня к ответственности.",
    "Я родился в семье, где папа работал дальнобойщиком, а мама была педагогом. С ранних лет привык к трудолюбию и ответственности, наблюдая за родителями. Папины рассказы о дальних рейсах и мамины уроки всегда вдохновляли меня учиться и развиваться."
]

GREEN_YOUTH = [
    "В школьные годы быстро нашёл общий язык с одноклассниками, всегда был в центре внимания. Отец приучал к самостоятельности, давал карманные деньги, а я вместе с друзьями устраивал пиршества в столовой. После школы поступил в институт, сохранив лучшие воспоминания о школьных годах.",
    "После окончания девятого класса поступил в Академию ФСБ — исполнил мечту детства. Учёба была непростой, но я совмещал занятия с футболом и дружескими встречами. Легко находил общий язык с однокурсниками и строил планы на будущее.",
    "Подростковый возраст стал временем поиска себя: увлекался спортом и музыкой, много времени проводил с друзьями. Учился запоминать важные уроки жизни, строил мечты о самостоятельности и будущей профессии."
]

GREEN_MATURING = [
    "В восемнадцать лет поступил в институт по бизнес-специальности, учёба давалась спокойно. Там встретил свою первую любовь, но отношения были недолгими. В университете приобрёл ценный опыт, научился принимать решения.",
    "В 18 лет был отчислен из академии из-за неуспеваемости. В это время судьба свела меня с дедушкой, с которым мы сблизились. Попробовал себя в новых увлечениях, встретил девушку, но отношения оказались недолгими. Этот период стал временем личностного роста.",
    "При вступлении во взрослую жизнь я познал много нового. Работа в различных сферах, общение с необычными людьми значительно расширили мой кругозор. Я выбрал путь, который позволил бы мне развиваться и принимать вызовы. В этот период я стал более уверенным в себе, научился принимать решения и ответственность за свои поступки."
]

GREEN_MATURITY = [
    "Зрелость стала временем ответственности: получил профессию, начал карьеру, приобрёл новых друзей и наставников. Иногда сталкивался с тяжелыми утратами, но именно они дали новый смысл жизни и профессиональный толчок. Обрёл уважение окружающих, завёл полезные знакомства.",
    "Я закончил институт с отличием, открыл свой бизнес или нашёл стабильную работу. Подружился с влиятельными людьми, которые поддерживали меня в начинаниях. Терял близких, но эти испытания сделали меня сильнее и самостоятельнее.",
    "Сегодня мне {age}. Я не женат и у меня нет детей, но я наслаждаюсь независимой жизнью в родном городе. За эти годы я прекрасно усвоил важность отношений с людьми, а также ценность времени. Нет вредных привычек, горжусь своей физической формой и стараюсь вести активный образ жизни."
]

GREEN_PRESENT = [
    "Сейчас продолжаю работать и развиваться, живу в родном городе, часто встречаюсь с друзьями и провожу время с семьёй. Не забываю о старых традициях и мечтаю однажды сменить профессию на более важную для общества. С удовольствием ухаживаю за домом и огородом, радуюсь каждому дню.",
    "Сегодня мне {age}, я живу рядом с родителями, работаю по специальности и строю планы на будущее. Остаюсь верен своим принципам, поддерживаю родных и друзей, надеюсь реализовать детские мечты и добиться ещё большего в жизни.",
    "Я продолжаю учиться и развиваться. Мои черты характера позволили мне быть внимательным к мелочам и запоминать важные события. Поддерживаю связи с друзьями и семьей, углубляю знания в разных областях и наслаждаюсь жизнью, помня о том, что каждый миг уникален."
]

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
    appearance = random_appearance()
    photo = "<i>прикрепить фото...</i>"

    # Блоки жизненного пути с примерами
    childhood = random.choice(GREEN_CHILDHOOD).format(city=birthplace)
    youth = random.choice(GREEN_YOUTH)
    maturing = random.choice(GREEN_MATURING)
    maturity = random.choice(GREEN_MATURITY).format(age=age)
    present = random.choice(GREEN_PRESENT).format(age=age)

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
        f"<b>Личное фото:</b> {photo}\n\n"
        f"<b>Детство:</b> {childhood}\n"
        f"<b>Юность:</b> {youth}\n"
        f"<b>Взросление:</b> {maturing}\n"
        f"<b>Зрелость:</b> {maturity}\n"
        f"<b>Наши дни:</b> {present}"
    )
    return result

GREEN_PHOTO_NOTICE = "Пожалуйста, не забудьте прикрепить фото к биографии для подачи на сервер GREEN!"

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
    await message.answer(f"⚠️ <b>{GREEN_PHOTO_NOTICE}</b>", parse_mode="HTML")
    await state.set_state(MenuStates.waiting_main_menu)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    import sys
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
