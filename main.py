import random
from datetime import datetime
from aiogram import Bot, Dispatcher, types
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
import asyncio

API_TOKEN = "8124119601:AAEgnFwCalzIKU15uHpIyWlCRbu4wvNEAUw"

# --- СТАРТОВЫЕ СОСТОЯНИЯ И ГЛАВНОЕ МЕНЮ ---

class MenuStates(StatesGroup):
    waiting_main_menu = State()
    choosing_server = State()

# --- СОСТОЯНИЯ ДЛЯ КАЖДОГО СЕРВЕРА ---

class OrangeBioStates(StatesGroup):
    waiting_name = State()
    waiting_surname = State()
    waiting_nationality = State()
    waiting_age = State()
    waiting_gender = State()
    waiting_childhood = State()
    waiting_youth = State()
    waiting_adult = State()
    waiting_present = State()

class PinkBioStates(StatesGroup):
    waiting_name = State()
    waiting_surname = State()
    waiting_nationality = State()
    waiting_age = State()
    waiting_gender = State()
    waiting_childhood = State()
    waiting_youth = State()
    waiting_adult = State()
    waiting_present = State()

class RedBioStates(StatesGroup):
    waiting_name = State()
    waiting_surname = State()
    waiting_nationality = State()
    waiting_age = State()
    waiting_gender = State()
    waiting_childhood = State()
    waiting_youth = State()
    waiting_adult = State()
    waiting_present = State()

class BlueBioStates(StatesGroup):
    waiting_name = State()
    waiting_surname = State()
    waiting_nationality = State()
    waiting_age = State()
    waiting_gender = State()
    waiting_childhood = State()
    waiting_youth = State()
    waiting_adult = State()
    waiting_present = State()

class GreenBioStates(StatesGroup):
    waiting_name = State()
    waiting_surname = State()
    waiting_nationality = State()
    waiting_age = State()
    waiting_gender = State()
    waiting_childhood = State()
    waiting_youth = State()
    waiting_adult = State()
    waiting_present = State()

# --- FSM для PURPLE ---

class PurpleBioStates(StatesGroup):
    waiting_nickname = State()
    waiting_nationality = State()
    waiting_age = State()
    waiting_gender = State()

# --- КНОПКИ ---

main_menu_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Создать РП-Биографию")],
    ],
    resize_keyboard=True
)

# Делаем инлайн-клавиатуру с 6 серверами, 2 колонки по 3
server_names = [
    "ORANGE", "PINK", "RED",
    "BLUE", "GREEN", "PURPLE"
]
server_callbacks = [
    "server_orange", "server_pink", "server_red",
    "server_blue", "server_green", "server_purple"
]
server_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text=server_names[i], callback_data=server_callbacks[i]),
            InlineKeyboardButton(text=server_names[i+3], callback_data=server_callbacks[i+3])
        ] for i in range(3)
    ]
)

# --- ГЕНЕРАЦИЯ ДЛЯ КАЖДОГО СЕРВЕРА ---

def random_appearance():
    heights = [str(h) + " см" for h in range(160, 201, 5)]
    weights = [str(w) + " кг" for w in range(50, 101, 5)]
    eyes = ["Карие", "Голубые", "Серые", "Зеленые", "Черные"]
    hairs = ["Русые", "Каштановые", "Темные", "Светло-русые", "Черные", "Темно-русые", "Блонд"]
    body = ["Спортивное", "Крепкое", "Среднее", "Худощавое", "Плотное"]
    return (
        f"Рост: {random.choice(heights)}\n"
        f"Вес: {random.choice(weights)}\n"
        f"Цвет глаз: {random.choice(eyes)}\n"
        f"Волосы: {random.choice(hairs)}\n"
        f"Телосложение: {random.choice(body)}"
    )

def random_hobby():
    hobbies = [
        "Бокс", "Фотография", "Графический дизайн", "Видеомонтаж", "Музыка", 
        "Путешествия", "Чтение книг", "Спорт", "Программирование", 
        "Автомобили", "Рисование", "Плавание", "Игра на гитаре"
    ]
    return ", ".join(random.sample(hobbies, random.randint(1, 3)))

def random_education():
    return random.choice([
        "Высшее", "Среднее специальное", "Среднее", 
        "Высшее (экономика)", "Высшее (юриспруденция)", 
        "Высшее (информатика)", "Высшее (инженерное дело)"
    ])

def random_marital():
    return random.choice([
        "Не женат", "Женат", "Разведён", "В гражданском браке", "Вдова/вдовец"
    ])

def random_city():
    return random.choice([
        "Арзамас", "Южный", "Нижегородск", "Лыткарино", "Москва", "Санкт-Петербург", "Новосибирск"
    ])

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

# --- ГЕНЕРАТОРЫ КОНКРЕТНЫХ АНКЕТ ---

def orange_generate_bio(data):
    return (
        f"Имя: {data['name']}\n"
        f"Фамилия: {data['surname']}\n"
        f"Национальность: {data['nationality']}\n"
        f"Возраст: {data['age']} лет\n"
        f"Пол: {data['gender']}\n"
        f"{random_appearance()}\n"
        f"Увлечение: {random_hobby()}\n\n"
        f"Детство:\n{data['childhood']}\n\n"
        f"Юность:\n{data['youth']}\n\n"
        f"Взрослая жизнь:\n{data['adult']}\n\n"
        f"Наше время:\n{data['present']}"
    )

def pink_generate_bio(data):
    return orange_generate_bio(data)

def red_generate_bio(data):
    return orange_generate_bio(data)

def blue_generate_bio(data):
    return orange_generate_bio(data)

def green_generate_bio(data):
    return orange_generate_bio(data)

def purple_generate_bio(data):
    nickname = data.get("nickname", "Nick Name")
    nationality = data.get("nationality", "Русский")
    age = int(data.get("age", 18))
    gender = data.get("gender", "Мужской")
    city = random_city()
    birthdate = random_date_of_birth(age)
    marital = random_marital()
    education = random_education()
    height = random.randint(165, 200)
    weight = random.randint(55, 110)
    eyes = random.choice(["Карие", "Голубые", "Серые", "Зеленые", "Черные"])
    hair = random.choice(["Русые", "Каштановые", "Темные", "Светло-русые", "Черные", "Темно-русые", "Блонд"])
    bodytype = random.choice(["Спортивное", "Крепкое", "Среднее", "Худощавое", "Плотное"])
    hobby = random_hobby()
    childhood = (
        f"{nickname} родился в {city}. С ранних лет проявлял интерес к {hobby.split(',')[0].lower()}. "
        f"В школе отличался {random.choice(['любознательностью', 'трудолюбием', 'доброжелательностью'])}, "
        f"родители поддерживали его увлечения."
    )
    youth = (
        f"В подростковом возрасте {nickname.split()[0]} начал активно заниматься {hobby.split(',')[0].lower()}. "
        f"Он участвовал в школьных мероприятиях, проявлял инициативу и расширял кругозор."
    )
    adult_life = (
        f"Закончив школу, поступил в учебное заведение по направлению '{education}'. "
        f"Параллельно работал и совершенствовал навыки в {hobby.split(',')[0].lower()}."
    )
    present = (
        f"Сегодня {nickname} активно развивается в выбранной сфере, поддерживает здоровый образ жизни, "
        f"общается с единомышленниками и строит амбициозные планы на будущее."
    )
    return (
        f"Никнейм: {nickname}\n"
        f"Национальность: {nationality}\n"
        f"Возраст: {age} лет\n"
        f"Дата и место рождения: {birthdate}, г. {city}\n"
        f"Семейное положение: {marital}\n"
        f"Образование: {education}\n"
        f"Пол: {gender}\n"
        f"Рост: {height} см\n"
        f"Вес: {weight} кг\n"
        f"Цвет глаз: {eyes}\n"
        f"Волосы: {hair}\n"
        f"Телосложение: {bodytype}\n"
        f"Увлечение: {hobby}\n\n"
        f"Детство:\n{childhood}\n\n"
        f"Юность:\n{youth}\n\n"
        f"Взрослая жизнь:\n{adult_life}\n\n"
        f"Наше время:\n{present}"
    )

# --- FSM И ХЕНДЛЕРЫ ---

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "Добро пожаловать! Нажмите 'Создать РП-Биографию', чтобы начать.",
        reply_markup=main_menu_kb
    )
    await state.set_state(MenuStates.waiting_main_menu)

@dp.message(MenuStates.waiting_main_menu)
async def menu_handler(message: types.Message, state: FSMContext):
    if message.text == "Создать РП-Биографию":
        await message.answer(
            "Выберите сервер, для которого хотите создать анкету:",
            reply_markup=server_kb
        )
        await state.set_state(MenuStates.choosing_server)
    else:
        await message.answer("Пожалуйста, нажмите 'Создать РП-Биографию'.")

@dp.callback_query(MenuStates.choosing_server)
async def choose_server(callback: types.CallbackQuery, state: FSMContext):
    cdata = callback.data
    await callback.answer()
    if cdata == "server_orange":
        await state.clear()
        await state.set_state(OrangeBioStates.waiting_name)
        await callback.message.answer("Введите имя персонажа:")
    elif cdata == "server_pink":
        await state.clear()
        await state.set_state(PinkBioStates.waiting_name)
        await callback.message.answer("Введите имя персонажа:")
    elif cdata == "server_red":
        await state.clear()
        await state.set_state(RedBioStates.waiting_name)
        await callback.message.answer("Введите имя персонажа:")
    elif cdata == "server_blue":
        await state.clear()
        await state.set_state(BlueBioStates.waiting_name)
        await callback.message.answer("Введите имя персонажа:")
    elif cdata == "server_green":
        await state.clear()
        await state.set_state(GreenBioStates.waiting_name)
        await callback.message.answer("Введите имя персонажа:")
    elif cdata == "server_purple":
        await state.clear()
        await state.set_state(PurpleBioStates.waiting_nickname)
        await callback.message.answer(
            "1️⃣ Введите игровой никнейм (строго формат 'Имя Фамилия', например Sander Kligan):"
        )
    else:
        await callback.message.answer("Этот сервер пока не реализован.")

# --- ORANGE ---
@dp.message(OrangeBioStates.waiting_name)
async def orange_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text.strip().capitalize())
    await state.set_state(OrangeBioStates.waiting_surname)
    await message.answer("Введите фамилию персонажа:")

@dp.message(OrangeBioStates.waiting_surname)
async def orange_surname(message: types.Message, state: FSMContext):
    await state.update_data(surname=message.text.strip().capitalize())
    await state.set_state(OrangeBioStates.waiting_nationality)
    await message.answer("Введите национальность:")

@dp.message(OrangeBioStates.waiting_nationality)
async def orange_nationality(message: types.Message, state: FSMContext):
    await state.update_data(nationality=message.text.strip().capitalize())
    await state.set_state(OrangeBioStates.waiting_age)
    await message.answer("Введите возраст персонажа (числом):")

@dp.message(OrangeBioStates.waiting_age)
async def orange_age(message: types.Message, state: FSMContext):
    try:
        age = int(message.text.strip())
    except:
        await message.answer("Укажите возраст числом.")
        return
    await state.update_data(age=age)
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Мужской")],
            [KeyboardButton(text="Женский")],
            [KeyboardButton(text="🏠 Главное меню")],
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    await state.set_state(OrangeBioStates.waiting_gender)
    await message.answer("Укажите пол персонажа:", reply_markup=kb)

@dp.message(OrangeBioStates.waiting_gender)
async def orange_gender(message: types.Message, state: FSMContext):
    if message.text == "🏠 Главное меню":
        await cmd_start(message, state)
        return
    gender = message.text.strip()
    if gender.lower() not in ["мужской", "женский"]:
        await message.answer("Выберите пол кнопкой ниже.")
        return
    await state.update_data(gender=gender.capitalize())
    await state.set_state(OrangeBioStates.waiting_childhood)
    await message.answer("Детство персонажа:")

@dp.message(OrangeBioStates.waiting_childhood)
async def orange_childhood(message: types.Message, state: FSMContext):
    await state.update_data(childhood=message.text.strip())
    await state.set_state(OrangeBioStates.waiting_youth)
    await message.answer("Юность персонажа:")

@dp.message(OrangeBioStates.waiting_youth)
async def orange_youth(message: types.Message, state: FSMContext):
    await state.update_data(youth=message.text.strip())
    await state.set_state(OrangeBioStates.waiting_adult)
    await message.answer("Взрослая жизнь персонажа:")

@dp.message(OrangeBioStates.waiting_adult)
async def orange_adult(message: types.Message, state: FSMContext):
    await state.update_data(adult=message.text.strip())
    await state.set_state(OrangeBioStates.waiting_present)
    await message.answer("Наше время персонажа:")

@dp.message(OrangeBioStates.waiting_present)
async def orange_present(message: types.Message, state: FSMContext):
    await state.update_data(present=message.text.strip())
    data = await state.get_data()
    bio = orange_generate_bio(data)
    await message.answer("Ваша анкета для ORANGE:\n\n" + bio, reply_markup=main_menu_kb)
    await state.set_state(MenuStates.waiting_main_menu)

# --- PINK ---
@dp.message(PinkBioStates.waiting_name)
async def pink_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text.strip().capitalize())
    await state.set_state(PinkBioStates.waiting_surname)
    await message.answer("Введите фамилию персонажа:")

@dp.message(PinkBioStates.waiting_surname)
async def pink_surname(message: types.Message, state: FSMContext):
    await state.update_data(surname=message.text.strip().capitalize())
    await state.set_state(PinkBioStates.waiting_nationality)
    await message.answer("Введите национальность:")

@dp.message(PinkBioStates.waiting_nationality)
async def pink_nationality(message: types.Message, state: FSMContext):
    await state.update_data(nationality=message.text.strip().capitalize())
    await state.set_state(PinkBioStates.waiting_age)
    await message.answer("Введите возраст персонажа (числом):")

@dp.message(PinkBioStates.waiting_age)
async def pink_age(message: types.Message, state: FSMContext):
    try:
        age = int(message.text.strip())
    except:
        await message.answer("Укажите возраст числом.")
        return
    await state.update_data(age=age)
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Мужской")],
            [KeyboardButton(text="Женский")],
            [KeyboardButton(text="🏠 Главное меню")],
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    await state.set_state(PinkBioStates.waiting_gender)
    await message.answer("Укажите пол персонажа:", reply_markup=kb)

@dp.message(PinkBioStates.waiting_gender)
async def pink_gender(message: types.Message, state: FSMContext):
    if message.text == "🏠 Главное меню":
        await cmd_start(message, state)
        return
    gender = message.text.strip()
    if gender.lower() not in ["мужской", "женский"]:
        await message.answer("Выберите пол кнопкой ниже.")
        return
    await state.update_data(gender=gender.capitalize())
    await state.set_state(PinkBioStates.waiting_childhood)
    await message.answer("Детство персонажа:")

@dp.message(PinkBioStates.waiting_childhood)
async def pink_childhood(message: types.Message, state: FSMContext):
    await state.update_data(childhood=message.text.strip())
    await state.set_state(PinkBioStates.waiting_youth)
    await message.answer("Юность персонажа:")

@dp.message(PinkBioStates.waiting_youth)
async def pink_youth(message: types.Message, state: FSMContext):
    await state.update_data(youth=message.text.strip())
    await state.set_state(PinkBioStates.waiting_adult)
    await message.answer("Взрослая жизнь персонажа:")

@dp.message(PinkBioStates.waiting_adult)
async def pink_adult(message: types.Message, state: FSMContext):
    await state.update_data(adult=message.text.strip())
    await state.set_state(PinkBioStates.waiting_present)
    await message.answer("Наше время персонажа:")

@dp.message(PinkBioStates.waiting_present)
async def pink_present(message: types.Message, state: FSMContext):
    await state.update_data(present=message.text.strip())
    data = await state.get_data()
    bio = pink_generate_bio(data)
    await message.answer("Ваша анкета для PINK:\n\n" + bio, reply_markup=main_menu_kb)
    await state.set_state(MenuStates.waiting_main_menu)

# --- RED ---
@dp.message(RedBioStates.waiting_name)
async def red_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text.strip().capitalize())
    await state.set_state(RedBioStates.waiting_surname)
    await message.answer("Введите фамилию персонажа:")

@dp.message(RedBioStates.waiting_surname)
async def red_surname(message: types.Message, state: FSMContext):
    await state.update_data(surname=message.text.strip().capitalize())
    await state.set_state(RedBioStates.waiting_nationality)
    await message.answer("Введите национальность:")

@dp.message(RedBioStates.waiting_nationality)
async def red_nationality(message: types.Message, state: FSMContext):
    await state.update_data(nationality=message.text.strip().capitalize())
    await state.set_state(RedBioStates.waiting_age)
    await message.answer("Введите возраст персонажа (числом):")

@dp.message(RedBioStates.waiting_age)
async def red_age(message: types.Message, state: FSMContext):
    try:
        age = int(message.text.strip())
    except:
        await message.answer("Укажите возраст числом.")
        return
    await state.update_data(age=age)
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Мужской")],
            [KeyboardButton(text="Женский")],
            [KeyboardButton(text="🏠 Главное меню")],
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    await state.set_state(RedBioStates.waiting_gender)
    await message.answer("Укажите пол персонажа:", reply_markup=kb)

@dp.message(RedBioStates.waiting_gender)
async def red_gender(message: types.Message, state: FSMContext):
    if message.text == "🏠 Главное меню":
        await cmd_start(message, state)
        return
    gender = message.text.strip()
    if gender.lower() not in ["мужской", "женский"]:
        await message.answer("Выберите пол кнопкой ниже.")
        return
    await state.update_data(gender=gender.capitalize())
    await state.set_state(RedBioStates.waiting_childhood)
    await message.answer("Детство персонажа:")

@dp.message(RedBioStates.waiting_childhood)
async def red_childhood(message: types.Message, state: FSMContext):
    await state.update_data(childhood=message.text.strip())
    await state.set_state(RedBioStates.waiting_youth)
    await message.answer("Юность персонажа:")

@dp.message(RedBioStates.waiting_youth)
async def red_youth(message: types.Message, state: FSMContext):
    await state.update_data(youth=message.text.strip())
    await state.set_state(RedBioStates.waiting_adult)
    await message.answer("Взрослая жизнь персонажа:")

@dp.message(RedBioStates.waiting_adult)
async def red_adult(message: types.Message, state: FSMContext):
    await state.update_data(adult=message.text.strip())
    await state.set_state(RedBioStates.waiting_present)
    await message.answer("Наше время персонажа:")

@dp.message(RedBioStates.waiting_present)
async def red_present(message: types.Message, state: FSMContext):
    await state.update_data(present=message.text.strip())
    data = await state.get_data()
    bio = red_generate_bio(data)
    await message.answer("Ваша анкета для RED:\n\n" + bio, reply_markup=main_menu_kb)
    await state.set_state(MenuStates.waiting_main_menu)

# --- BLUE ---
@dp.message(BlueBioStates.waiting_name)
async def blue_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text.strip().capitalize())
    await state.set_state(BlueBioStates.waiting_surname)
    await message.answer("Введите фамилию персонажа:")

@dp.message(BlueBioStates.waiting_surname)
async def blue_surname(message: types.Message, state: FSMContext):
    await state.update_data(surname=message.text.strip().capitalize())
    await state.set_state(BlueBioStates.waiting_nationality)
    await message.answer("Введите национальность:")

@dp.message(BlueBioStates.waiting_nationality)
async def blue_nationality(message: types.Message, state: FSMContext):
    await state.update_data(nationality=message.text.strip().capitalize())
    await state.set_state(BlueBioStates.waiting_age)
    await message.answer("Введите возраст персонажа (числом):")

@dp.message(BlueBioStates.waiting_age)
async def blue_age(message: types.Message, state: FSMContext):
    try:
        age = int(message.text.strip())
    except:
        await message.answer("Укажите возраст числом.")
        return
    await state.update_data(age=age)
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Мужской")],
            [KeyboardButton(text="Женский")],
            [KeyboardButton(text="🏠 Главное меню")],
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    await state.set_state(BlueBioStates.waiting_gender)
    await message.answer("Укажите пол персонажа:", reply_markup=kb)

@dp.message(BlueBioStates.waiting_gender)
async def blue_gender(message: types.Message, state: FSMContext):
    if message.text == "🏠 Главное меню":
        await cmd_start(message, state)
        return
    gender = message.text.strip()
    if gender.lower() not in ["мужской", "женский"]:
        await message.answer("Выберите пол кнопкой ниже.")
        return
    await state.update_data(gender=gender.capitalize())
    await state.set_state(BlueBioStates.waiting_childhood)
    await message.answer("Детство персонажа:")

@dp.message(BlueBioStates.waiting_childhood)
async def blue_childhood(message: types.Message, state: FSMContext):
    await state.update_data(childhood=message.text.strip())
    await state.set_state(BlueBioStates.waiting_youth)
    await message.answer("Юность персонажа:")

@dp.message(BlueBioStates.waiting_youth)
async def blue_youth(message: types.Message, state: FSMContext):
    await state.update_data(youth=message.text.strip())
    await state.set_state(BlueBioStates.waiting_adult)
    await message.answer("Взрослая жизнь персонажа:")

@dp.message(BlueBioStates.waiting_adult)
async def blue_adult(message: types.Message, state: FSMContext):
    await state.update_data(adult=message.text.strip())
    await state.set_state(BlueBioStates.waiting_present)
    await message.answer("Наше время персонажа:")

@dp.message(BlueBioStates.waiting_present)
async def blue_present(message: types.Message, state: FSMContext):
    await state.update_data(present=message.text.strip())
    data = await state.get_data()
    bio = blue_generate_bio(data)
    await message.answer("Ваша анкета для BLUE:\n\n" + bio, reply_markup=main_menu_kb)
    await state.set_state(MenuStates.waiting_main_menu)

# --- GREEN ---
@dp.message(GreenBioStates.waiting_name)
async def green_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text.strip().capitalize())
    await state.set_state(GreenBioStates.waiting_surname)
    await message.answer("Введите фамилию персонажа:")

@dp.message(GreenBioStates.waiting_surname)
async def green_surname(message: types.Message, state: FSMContext):
    await state.update_data(surname=message.text.strip().capitalize())
    await state.set_state(GreenBioStates.waiting_nationality)
    await message.answer("Введите национальность:")

@dp.message(GreenBioStates.waiting_nationality)
async def green_nationality(message: types.Message, state: FSMContext):
    await state.update_data(nationality=message.text.strip().capitalize())
    await state.set_state(GreenBioStates.waiting_age)
    await message.answer("Введите возраст персонажа (числом):")

@dp.message(GreenBioStates.waiting_age)
async def green_age(message: types.Message, state: FSMContext):
    try:
        age = int(message.text.strip())
    except:
        await message.answer("Укажите возраст числом.")
        return
    await state.update_data(age=age)
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Мужской")],
            [KeyboardButton(text="Женский")],
            [KeyboardButton(text="🏠 Главное меню")],
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    await state.set_state(GreenBioStates.waiting_gender)
    await message.answer("Укажите пол персонажа:", reply_markup=kb)

@dp.message(GreenBioStates.waiting_gender)
async def green_gender(message: types.Message, state: FSMContext):
    if message.text == "🏠 Главное меню":
        await cmd_start(message, state)
        return
    gender = message.text.strip()
    if gender.lower() not in ["мужской", "женский"]:
        await message.answer("Выберите пол кнопкой ниже.")
        return
    await state.update_data(gender=gender.capitalize())
    await state.set_state(GreenBioStates.waiting_childhood)
    await message.answer("Детство персонажа:")

@dp.message(GreenBioStates.waiting_childhood)
async def green_childhood(message: types.Message, state: FSMContext):
    await state.update_data(childhood=message.text.strip())
    await state.set_state(GreenBioStates.waiting_youth)
    await message.answer("Юность персонажа:")

@dp.message(GreenBioStates.waiting_youth)
async def green_youth(message: types.Message, state: FSMContext):
    await state.update_data(youth=message.text.strip())
    await state.set_state(GreenBioStates.waiting_adult)
    await message.answer("Взрослая жизнь персонажа:")

@dp.message(GreenBioStates.waiting_adult)
async def green_adult(message: types.Message, state: FSMContext):
    await state.update_data(adult=message.text.strip())
    await state.set_state(GreenBioStates.waiting_present)
    await message.answer("Наше время персонажа:")

@dp.message(GreenBioStates.waiting_present)
async def green_present(message: types.Message, state: FSMContext):
    await state.update_data(present=message.text.strip())
    data = await state.get_data()
    bio = green_generate_bio(data)
    await message.answer("Ваша анкета для GREEN:\n\n" + bio, reply_markup=main_menu_kb)
    await state.set_state(MenuStates.waiting_main_menu)

# --- PURPLE ---
@dp.message(PurpleBioStates.waiting_nickname)
async def purple_nickname(message: types.Message, state: FSMContext):
    nickname = message.text.strip()
    if "_" in nickname or len(nickname.split()) != 2:
        await message.answer(
            "⚠️ Никнейм должен быть строго в формате 'Имя Фамилия' через пробел, без подчёркиваний. Пример: Sander Kligan"
        )
        return
    await state.update_data(nickname=nickname)
    await state.set_state(PurpleBioStates.waiting_nationality)
    await message.answer("2️⃣ Укажите национальность персонажа:")

@dp.message(PurpleBioStates.waiting_nationality)
async def purple_nationality(message: types.Message, state: FSMContext):
    await state.update_data(nationality=message.text.strip().capitalize())
    await state.set_state(PurpleBioStates.waiting_age)
    await message.answer("3️⃣ Укажите возраст персонажа (от 16 до 65):")

@dp.message(PurpleBioStates.waiting_age)
async def purple_age(message: types.Message, state: FSMContext):
    try:
        age = int(message.text.strip())
        if age < 16 or age > 65:
            raise ValueError
    except:
        await message.answer("⚠️ Укажите возраст числом от 16 до 65.")
        return
    await state.update_data(age=age)
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Мужской")],
            [KeyboardButton(text="Женский")],
            [KeyboardButton(text="🏠 Главное меню")]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    await state.set_state(PurpleBioStates.waiting_gender)
    await message.answer("4️⃣ Укажите пол персонажа:", reply_markup=kb)

@dp.message(PurpleBioStates.waiting_gender)
async def purple_gender(message: types.Message, state: FSMContext):
    if message.text == "🏠 Главное меню":
        await cmd_start(message, state)
        return
    gender = message.text.strip()
    if gender.lower() not in ["мужской", "женский"]:
        await message.answer("Пожалуйста, выберите пол кнопкой ниже.")
        return
    await state.update_data(gender=gender.capitalize())
    data = await state.get_data()
    bio = purple_generate_bio(data)
    await message.answer("Ваша уникальная RP-биография для сервера PURPLE:\n\n" + bio, reply_markup=main_menu_kb)
    await state.set_state(MenuStates.waiting_main_menu)

# --- ЗАПУСК ---

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
