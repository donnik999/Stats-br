import random
from datetime import datetime
from aiogram import Bot, Dispatcher, types
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
import asyncio

API_TOKEN = "8124119601:AAEgnFwCalzIKU15uHpIyWlCRbu4wvNEAUw"

# ------------- Основные состояния FSM -------------

class MenuStates(StatesGroup):
    waiting_main_menu = State()
    choosing_server = State()

# Обычные серверы (примерные FSM, их можно копипастить)
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

class YellowBioStates(StatesGroup):
    waiting_name = State()
    waiting_surname = State()
    waiting_nationality = State()
    waiting_age = State()
    waiting_gender = State()
    waiting_childhood = State()
    waiting_youth = State()
    waiting_adult = State()
    waiting_present = State()

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

class PurpleBioStates(StatesGroup):
    waiting_nickname = State()
    waiting_nationality = State()
    waiting_age = State()
    waiting_gender = State()

class BrownBioStates(StatesGroup):
    waiting_name = State()
    waiting_surname = State()
    waiting_nationality = State()
    waiting_age = State()
    waiting_gender = State()
    waiting_childhood = State()
    waiting_youth = State()
    waiting_adult = State()
    waiting_present = State()

class CyanBioStates(StatesGroup):
    waiting_name = State()
    waiting_surname = State()
    waiting_nationality = State()
    waiting_age = State()
    waiting_gender = State()
    waiting_childhood = State()
    waiting_youth = State()
    waiting_adult = State()
    waiting_present = State()

class WhiteBioStates(StatesGroup):
    waiting_name = State()
    waiting_surname = State()
    waiting_nationality = State()
    waiting_age = State()
    waiting_gender = State()
    waiting_childhood = State()
    waiting_youth = State()
    waiting_adult = State()
    waiting_present = State()

# ------------- Кнопки -------------

main_menu_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🌟 Создать РП-Биографию")],
        [KeyboardButton(text="📩 Связь с разработчиком")]
    ],
    resize_keyboard=True
)

# Список серверов в один столбик, по порядку создания
server_names = [
    "RED", "GREEN", "BLUE", "YELLOW", "ORANGE",
    "PINK", "PURPLE", "BROWN", "CYAN", "WHITE"
]
server_callbacks = [
    "server_red", "server_green", "server_blue", "server_yellow", "server_orange",
    "server_pink", "server_purple", "server_brown", "server_cyan", "server_white"
]
server_kb = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text=server_names[i], callback_data=server_callbacks[i])] for i in range(10)]
)

contact_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Написать разработчику", url="https://t.me/BUNKOC")]
    ]
)

# ------------- Генерация внешности и прочих данных -------------

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

# ------------- Генераторы анкет -------------

def default_generate_bio(data):
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

# ------------- Хендлеры -------------

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "<b>👋 Добро пожаловать в генератор РП-Биографий для всех серверов!</b>\n\n"
        "Создай уникальную анкету для любого сервера и начни своё ролевое приключение!\n\n"
        "ℹ️ <i>Если возникнут вопросы — жми кнопку связи ниже.</i>",
        reply_markup=main_menu_kb,
        parse_mode="HTML"
    )
    await state.set_state(MenuStates.waiting_main_menu)

@dp.message(MenuStates.waiting_main_menu)
async def menu_handler(message: types.Message, state: FSMContext):
    if message.text == "🌟 Создать РП-Биографию":
        await message.answer(
            "<b>Выберите сервер для создания биографии:</b>",
            reply_markup=server_kb,
            parse_mode="HTML"
        )
        await state.set_state(MenuStates.choosing_server)
    elif message.text == "📩 Связь с разработчиком":
        await message.answer(
            "<b>Связаться с разработчиком:</b>\n"
            "Напиши свои пожелания или вопросы — всегда открыт к обратной связи!",
            reply_markup=contact_kb,
            parse_mode="HTML"
        )
    else:
        await message.answer("Пожалуйста, воспользуйтесь меню ниже 👇")

@dp.callback_query(MenuStates.choosing_server)
async def choose_server(callback: types.CallbackQuery, state: FSMContext):
    cdata = callback.data
    await callback.answer()
    # RED
    if cdata == "server_red":
        await state.clear()
        await state.set_state(RedBioStates.waiting_name)
        await callback.message.answer("📝 Введите имя персонажа:")
    # GREEN
    elif cdata == "server_green":
        await state.clear()
        await state.set_state(GreenBioStates.waiting_name)
        await callback.message.answer("📝 Введите имя персонажа:")
    # BLUE
    elif cdata == "server_blue":
        await state.clear()
        await state.set_state(BlueBioStates.waiting_name)
        await callback.message.answer("📝 Введите имя персонажа:")
    # YELLOW
    elif cdata == "server_yellow":
        await state.clear()
        await state.set_state(YellowBioStates.waiting_name)
        await callback.message.answer("📝 Введите имя персонажа:")
    # ORANGE
    elif cdata == "server_orange":
        await state.clear()
        await state.set_state(OrangeBioStates.waiting_name)
        await callback.message.answer("📝 Введите имя персонажа:")
    # PINK
    elif cdata == "server_pink":
        await state.clear()
        await state.set_state(PinkBioStates.waiting_name)
        await callback.message.answer("📝 Введите имя персонажа:")
    # PURPLE (уникальная логика)
    elif cdata == "server_purple":
        await state.clear()
        await state.set_state(PurpleBioStates.waiting_nickname)
        await callback.message.answer(
            "📝 Введите игровой никнейм (строго формат 'Имя Фамилия', например Sander Kligan):"
        )
    # BROWN
    elif cdata == "server_brown":
        await state.clear()
        await state.set_state(BrownBioStates.waiting_name)
        await callback.message.answer("📝 Введите имя персонажа:")
    # CYAN
    elif cdata == "server_cyan":
        await state.clear()
        await state.set_state(CyanBioStates.waiting_name)
        await callback.message.answer("📝 Введите имя персонажа:")
    # WHITE
    elif cdata == "server_white":
        await state.clear()
        await state.set_state(WhiteBioStates.waiting_name)
        await callback.message.answer("📝 Введите имя персонажа:")

# ---------------------- UNIVERSAL FSM HANDLER (кроме PURPLE) ----------------------

async def universal_fsm(message: types.Message, state: FSMContext, bio_states, server_name):
    state_map = [
        ('waiting_name', "Введите фамилию персонажа:"),
        ('waiting_surname', "Введите национальность персонажа:"),
        ('waiting_nationality', "Введите возраст персонажа (числом):"),
        ('waiting_age', "Укажите пол персонажа:", True),
        ('waiting_gender', "Детство персонажа:"),
        ('waiting_childhood', "Юность персонажа:"),
        ('waiting_youth', "Взрослая жизнь персонажа:"),
        ('waiting_adult', "Наше время персонажа:"),
    ]
    current_state = await state.get_state()
    idx = [s[0] for s in state_map].index(current_state.split(":")[-1])
    field_names = ['name', 'surname', 'nationality', 'age', 'gender', 'childhood', 'youth', 'adult', 'present']
    if idx == 3:  # возраст -> кнопки пола
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
        await state.set_state(getattr(bio_states, "waiting_gender"))
        await message.answer("Укажите пол персонажа:", reply_markup=kb)
        return
    if idx == 4:  # пол
        if message.text == "🏠 Главное меню":
            await cmd_start(message, state)
            return
        gender = message.text.strip()
        if gender.lower() not in ["мужской", "женский"]:
            await message.answer("Пожалуйста, выберите пол кнопкой ниже.")
            return
        await state.update_data(gender=gender.capitalize())
        await state.set_state(getattr(bio_states, "waiting_childhood"))
        await message.answer("Детство персонажа:")
        return
    if idx < len(state_map) - 1:
        await state.update_data(**{field_names[idx]: message.text.strip()})
        await state.set_state(getattr(bio_states, state_map[idx+1][0]))
        await message.answer(state_map[idx+1][1])
    else:
        await state.update_data(present=message.text.strip())
        data = await state.get_data()
        bio = default_generate_bio(data)
        await message.answer(
            f"<b>Ваша анкета для {server_name}:</b>\n\n" + bio,
            reply_markup=main_menu_kb, parse_mode="HTML"
        )
        await state.set_state(MenuStates.waiting_main_menu)

# FSM для обычных серверов (универсальный обработчик)
for bio_states, server_name in [
    (RedBioStates, "RED"), (GreenBioStates, "GREEN"), (BlueBioStates, "BLUE"), (YellowBioStates, "YELLOW"),
    (OrangeBioStates, "ORANGE"), (PinkBioStates, "PINK"), (BrownBioStates, "BROWN"),
    (CyanBioStates, "CYAN"), (WhiteBioStates, "WHITE")
]:
    for field in ["waiting_name", "waiting_surname", "waiting_nationality", "waiting_age", "waiting_gender",
                  "waiting_childhood", "waiting_youth", "waiting_adult", "waiting_present"]:
        dp.message.register(lambda m, s, b=bio_states, n=server_name: universal_fsm(m, s, b, n), getattr(bio_states, field))

# ---------------------- PURPLE FSM ----------------------

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
    await message.answer("<b>Ваша уникальная RP-биография для сервера PURPLE:</b>\n\n" + bio, reply_markup=main_menu_kb, parse_mode="HTML")
    await state.set_state(MenuStates.waiting_main_menu)

# ------------- Запуск -------------

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
