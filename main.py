import random
from datetime import datetime
from aiogram import Bot, Dispatcher, types
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
import asyncio

API_TOKEN = "8124119601:AAEgnFwCalzIKU15uHpIyWlCRbu4wvNEAUw"

# --- FSM STATES ---
class MenuStates(StatesGroup):
    waiting_main_menu = State()
    choosing_server = State()

class UniversalBioStates(StatesGroup):
    waiting_name = State()
    waiting_surname = State()
    waiting_nationality = State()
    waiting_age = State()
    waiting_gender = State()

class PurpleBioStates(StatesGroup):
    waiting_nickname = State()
    waiting_nationality = State()
    waiting_age = State()
    waiting_gender = State()

# --- KEYBOARDS ---
exit_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="🏠 Главное меню")]], resize_keyboard=True)
main_menu_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🌟 Создать РП-Биографию")],
        [KeyboardButton(text="📩 Связь с разработчиком")]
    ],
    resize_keyboard=True
)
server_names = [
    "RED", "GREEN", "BLUE", "YELLOW", "ORANGE",
    "PURPLE", "LIME", "PINK", "CHERRY", "BLACK"
]
server_callbacks = [
    "server_red", "server_green", "server_blue", "server_yellow", "server_orange",
    "server_purple", "server_lime", "server_pink", "server_cherry", "server_black"
]
server_kb = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text=server_names[i], callback_data=server_callbacks[i])] for i in range(10)]
)
contact_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Написать разработчику", url="https://t.me/BUNKOC")]
    ]
)

# --- GENERATION UTILS ---

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
        "Автомобили", "Рисование", "Плавание", "Игра на гитаре", "Кулинария", "Лыжи", "Велоспорт"
    ]
    return ", ".join(random.sample(hobbies, random.randint(2, 4)))

def random_education():
    return random.choice([
        "Высшее", "Среднее специальное", "Среднее", 
        "Высшее (экономика)", "Высшее (юриспруденция)", 
        "Высшее (информатика)", "Высшее (инженерное дело)", "Высшее (журналистика)"
    ])

def random_marital():
    return random.choice([
        "Не женат", "Женат", "Разведён", "В гражданском браке", "Вдова/вдовец"
    ])

def random_city():
    return random.choice([
        "Арзамас", "Южный", "Нижегородск", "Лыткарино", "Москва", "Санкт-Петербург",
        "Новосибирск", "Казань", "Краснодар", "Владивосток", "Екатеринбург"
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

def extended_bio_blocks(name, surname):
    city = random_city()
    hobby = random_hobby()
    childhood = (
        f"{name} {surname} родился в городе {city} в дружной семье. "
        f"С ранних лет проявлял живой интерес к окружающему миру и много времени проводил на свежем воздухе. "
        "В детстве он часто играл с друзьями во дворе, строил шалаши, катался на велосипеде и собирал коллекции марок и монет. "
        "Родители поощряли его любознательность, покупали книги и развивающие игры. "
        f"В начальной школе {name} быстро освоил чтение и математику, а учителя отмечали его как одного из самых активных учеников класса."
    )
    youth = (
        f"В подростковом возрасте {name} стал заниматься {hobby.split(',')[0].lower()} и посещать различные секции и кружки. "
        "Он принимал участие в школьных олимпиадах, городских конкурсах и спортивных соревнованиях, часто занимая призовые места. "
        "У него сформировался круг близких друзей, с которыми они устраивали походы, совместные проекты и вечерние посиделки у костра. "
        f"В это время {name} начал интересоваться современными технологиями, записался на курсы программирования и даже собрал свой первый компьютер. "
        "Учителя и одноклассники уважали его за честность, ответственность и умение работать в команде."
    )
    adult = (
        f"Окончив школу с отличием, {name} поступил в университет, выбрав направление по душе. "
        "Во время учёбы он активно участвовал в студенческих конференциях, волонтёрских движениях и студсовете. "
        "Параллельно {name} подрабатывал по специальности, что позволило ему получить ценный опыт и обзавестись нужными связями. "
        "В университете он организовал несколько крупных мероприятий, а также подготовил научную работу, которая была отмечена на всероссийском уровне. "
        "После получения диплома {name} устроился на работу, где быстро зарекомендовал себя как инициативный и надёжный сотрудник."
    )
    present = (
        f"Сейчас {name} {surname} продолжает совершенствоваться в профессиональной и личной жизни. "
        "Он занимается самообразованием, посещает мастер-классы и тренинги, следит за новостями в своей области. "
        "В свободное время {name} любит путешествовать, изучать новые языки и культуры, заниматься спортом и творчеством. "
        "Друзья и близкие ценят его за отзывчивость, доброту и умение поддержать в трудную минуту. "
        f"В планах у {name} открыть собственный проект и реализовать несколько амбициозных идей, которые помогут сделать мир немного лучше."
    )
    return childhood, youth, adult, present

def extended_purple_blocks(nickname):
    city = random_city()
    hobby = random_hobby()
    childhood = (
        f"{nickname} родился в городе {city}, в творческой семье. "
        "С самых ранних лет отличался любознательностью и самостоятельностью: он с удовольствием исследовал окрестности, "
        "строил сложные конструкции из конструктора и любил слушать рассказы старших о жизни в прошлом. "
        f"В детстве {nickname} научился кататься на велосипеде, плавать и даже освоил азы {hobby.split(',')[0].lower()}. "
        "Школьные учителя отмечали его как активного, доброго и трудолюбивого ребёнка, который всегда помогал одноклассникам."
    )
    youth = (
        f"В подростковом возрасте {nickname} начал проявлять лидерские качества, стал капитаном спортивной команды и организатором школьных мероприятий. "
        f"Он всерьёз занялся {hobby.split(',')[0].lower()}, участвовал в олимпиадах и городских чемпионатах. "
        f"С друзьями {nickname} часто ездил в летние лагеря, участвовал в волонтёрских акциях и делал первые успехи в программировании. "
        "Учителя и наставники ценили его за ответственность, стремление к развитию и умение вдохновлять других."
    )
    adult = (
        f"После школы {nickname} поступил в один из лучших вузов страны, где быстро влился в студенческую жизнь. "
        "Он стал активным участником научных конференций, занимался исследовательскими проектами и нередко помогал младшим курсам осваивать учебный материал. "
        f"Параллельно {nickname} подрабатывал по специальности, участвовал в стартапах и расширял профессиональный круг знакомств. "
        "Полученные знания и опыт позволили ему успешно защитить диплом и найти интересную работу в престижной компании."
    )
    present = (
        f"Сегодня {nickname} продолжает активно развиваться, занимается спортом, путешествует по разным странам и осваивает новые навыки. "
        "Он участвует в профессиональных сообществах, делится опытом с коллегами и помогает начинающим специалистам. "
        f"В свободное время {nickname} увлекается творчеством, любит читать современные книги и изучать иностранные языки. "
        "Близкие ценят его за искренность, чувство юмора и готовность прийти на помощь в любой ситуации."
    )
    return childhood, youth, adult, present

def universal_generate_bio(data, server):
    name = data.get("name", "")
    surname = data.get("surname", "")
    childhood, youth, adult, present = extended_bio_blocks(name, surname)
    return (
        f"Имя: {name}\n"
        f"Фамилия: {surname}\n"
        f"Национальность: {data['nationality']}\n"
        f"Возраст: {data['age']} лет\n"
        f"Пол: {data['gender']}\n"
        f"{random_appearance()}\n"
        f"Увлечение: {random_hobby()}\n\n"
        f"Детство:\n{childhood}\n\n"
        f"Юность:\n{youth}\n\n"
        f"Взрослая жизнь:\n{adult}\n\n"
        f"Наше время:\n{present}"
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
    childhood, youth, adult, present = extended_purple_blocks(nickname)
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
        f"Взрослая жизнь:\n{adult}\n\n"
        f"Наше время:\n{present}"
    )

# --- FSM & HANDLERS ---

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "<b>👋 Добро пожаловать в генератор РП-Биографий!</b>\n\n"
        "Создай уникальную анкету для любого сервера и начни своё ролевое приключение.\n\n"
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
        await message.answer("Пожалуйста, воспользуйтесь меню ниже 👇", reply_markup=main_menu_kb)

@dp.callback_query(MenuStates.choosing_server)
async def choose_server(callback: types.CallbackQuery, state: FSMContext):
    cdata = callback.data
    await callback.answer()
    if cdata == "server_purple":
        await state.clear()
        await state.set_state(PurpleBioStates.waiting_nickname)
        await callback.message.answer(
            "📝 Введите игровой никнейм (строго формат 'Имя Фамилия', например Sander Kligan):",
            reply_markup=exit_kb
        )
        return
    # Универсальные сервера
    for idx, cb in enumerate(server_callbacks):
        if cdata == cb and cb != "server_purple":
            await state.clear()
            await state.set_state(UniversalBioStates.waiting_name)
            await state.update_data(server=server_names[idx])
            await callback.message.answer("Введите имя персонажа:", reply_markup=exit_kb)
            return

# --- UNIVERSAL FSM ---

@dp.message(UniversalBioStates.waiting_name)
async def universal_name(message: types.Message, state: FSMContext):
    if message.text == "🏠 Главное меню":
        await cmd_start(message, state)
        return
    await state.update_data(name=message.text.strip().capitalize())
    await state.set_state(UniversalBioStates.waiting_surname)
    await message.answer("Введите фамилию персонажа:", reply_markup=exit_kb)

@dp.message(UniversalBioStates.waiting_surname)
async def universal_surname(message: types.Message, state: FSMContext):
    if message.text == "🏠 Главное меню":
        await cmd_start(message, state)
        return
    await state.update_data(surname=message.text.strip().capitalize())
    await state.set_state(UniversalBioStates.waiting_nationality)
    await message.answer("Введите национальность персонажа:", reply_markup=exit_kb)

@dp.message(UniversalBioStates.waiting_nationality)
async def universal_nationality(message: types.Message, state: FSMContext):
    if message.text == "🏠 Главное меню":
        await cmd_start(message, state)
        return
    await state.update_data(nationality=message.text.strip().capitalize())
    await state.set_state(UniversalBioStates.waiting_age)
    await message.answer("Введите возраст персонажа (от 16 до 65):", reply_markup=exit_kb)

@dp.message(UniversalBioStates.waiting_age)
async def universal_age(message: types.Message, state: FSMContext):
    if message.text == "🏠 Главное меню":
        await cmd_start(message, state)
        return
    try:
        age = int(message.text.strip())
        if age < 16 or age > 65:
            raise ValueError
    except:
        await message.answer("Укажите возраст числом от 16 до 65.", reply_markup=exit_kb)
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
    await state.set_state(UniversalBioStates.waiting_gender)
    await message.answer("Укажите пол персонажа:", reply_markup=kb)

@dp.message(UniversalBioStates.waiting_gender)
async def universal_gender(message: types.Message, state: FSMContext):
    if message.text == "🏠 Главное меню":
        await cmd_start(message, state)
        return
    gender = message.text.strip()
    if gender.lower() not in ["мужской", "женский"]:
        await message.answer("Пожалуйста, выберите пол кнопкой ниже.", reply_markup=exit_kb)
        return
    await state.update_data(gender=gender.capitalize())
    data = await state.get_data()
    bio = universal_generate_bio(data, data.get("server", ""))
    await message.answer(
        f"<b>Ваша подробная анкета для сервера {data.get('server', '').upper()}:</b>\n\n" + bio,
        reply_markup=main_menu_kb, parse_mode="HTML"
    )
    await state.set_state(MenuStates.waiting_main_menu)

# --- PURPLE FSM ---

@dp.message(PurpleBioStates.waiting_nickname)
async def purple_nickname(message: types.Message, state: FSMContext):
    if message.text == "🏠 Главное меню":
        await cmd_start(message, state)
        return
    nickname = message.text.strip()
    if "_" in nickname or len(nickname.split()) != 2:
        await message.answer(
            "⚠️ Никнейм должен быть строго в формате 'Имя Фамилия' через пробел, без подчёркиваний. Пример: Sander Kligan",
            reply_markup=exit_kb
        )
        return
    await state.update_data(nickname=nickname)
    await state.set_state(PurpleBioStates.waiting_nationality)
    await message.answer("2️⃣ Укажите национальность персонажа:", reply_markup=exit_kb)

@dp.message(PurpleBioStates.waiting_nationality)
async def purple_nationality(message: types.Message, state: FSMContext):
    if message.text == "🏠 Главное меню":
        await cmd_start(message, state)
        return
    await state.update_data(nationality=message.text.strip().capitalize())
    await state.set_state(PurpleBioStates.waiting_age)
    await message.answer("3️⃣ Укажите возраст персонажа (от 16 до 65):", reply_markup=exit_kb)

@dp.message(PurpleBioStates.waiting_age)
async def purple_age(message: types.Message, state: FSMContext):
    if message.text == "🏠 Главное меню":
        await cmd_start(message, state)
        return
    try:
        age = int(message.text.strip())
        if age < 16 or age > 65:
            raise ValueError
    except:
        await message.answer("⚠️ Укажите возраст числом от 16 до 65.", reply_markup=exit_kb)
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
        await message.answer("Пожалуйста, выберите пол кнопкой ниже.", reply_markup=exit_kb)
        return
    await state.update_data(gender=gender.capitalize())
    data = await state.get_data()
    bio = purple_generate_bio(data)
    await message.answer("<b>Ваша подробная RP-биография для сервера PURPLE:</b>\n\n" + bio, reply_markup=main_menu_kb, parse_mode="HTML")
    await state.set_state(MenuStates.waiting_main_menu)

# --- ЗАПУСК ---

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
