import os
import random
import logging
import getpass
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

logging.basicConfig(level=logging.INFO)

TELEGRAM_TOKEN = "8124119601:AAEgnFwCalzIKU15uHpIyWlCRbu4wvNEAUw"
if not TELEGRAM_TOKEN:
    TELEGRAM_TOKEN = getpass.getpass("Введите TELEGRAM_TOKEN: ")

bot = Bot(token=TELEGRAM_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

menu_kb = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="📝 Сгенерировать РП-биографию")]],
    resize_keyboard=True,
)

gender_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Мужской"), KeyboardButton(text="Женский")]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
)

class BioStates(StatesGroup):
    waiting_fio = State()
    waiting_age = State()
    waiting_nationality = State()
    waiting_gender = State()

# ----------------- Справочники ------------------

CITIES = [
    "Арзамас", "Южный", "Батырево", "Лыткарино", "Морское",
    "Бусаево", "Горки", "Новый Арзамас", "Приволжск"
]

STREETS = [
    "Центральная", "Лесная", "Советская", "Солнечная", "Молодёжная",
    "Шоссейная", "Парковая", "Победы", "Гагарина", "Мира",
    "Озерная", "Набережная", "Заречная", "Трудовая", "Северная"
]

ORGANIZATIONS = [
    "СМИ", "Центральная Больница", "ГИБДД", "УМВД", "ФСБ", "Правительство", "ФСИН"
]

JOBS = [
    "рыболов", "таксист", "водолаз", "строитель", "заместитель строителя", "сотрудник МЧС",
    "работник шахты", "работник на заводе", "работник на ферме", "кладоискатель",
    "инкассатор", "дальнобойщик"
]

def generate_address():
    city = random.choice(CITIES)
    street = random.choice(STREETS)
    house = random.randint(1, 99)
    apt = random.randint(1, 120)
    address = f"г. {city}, ул. {street}, д. {house}, кв. {apt}"
    return address, city

def generate_bio(data: dict) -> str:
    fio = data.get("fio", "Не указано")
    age = data.get("age", "Не указано")
    nationality = data.get("nationality", "Не указано")
    gender = data.get("gender", "Мужской")  # по умолчанию мужской
    education = random.choice([
        "Среднее общее", "Средне-специальное", "Высшее", "Техническое", "Юридическое", "Медицинское"
    ])
    org = random.choice(ORGANIZATIONS)
    job = random.choice(JOBS)
    address, city = generate_address()
    parent_address, _ = generate_address()
    army_status = (
        random.choice([
            "Проходил срочную службу, уволен в запас.",
            "Службу не проходил по уважительной причине.",
            "Проходил альтернативную гражданскую службу.",
            "Проходил службу, получил благодарность от командования."
        ])
        if gender == "Мужской" else
        "Не проходила военную службу."
    )
    family = random.choice([
        "Отец — Александр, мать — Марина. Есть младшая сестра.",
        "Семья полная: родители и старший брат.",
        "Отец — ветеран, мать — преподаватель. Один ребёнок в семье.",
        "Мама — домохозяйка, отец — водитель. Братьев и сестёр нет."
    ])
    appearance = (
        random.choice([
            "Рост 180 см, спортивного телосложения, волосы тёмные, глаза карие.",
            "Среднего роста, крепкое телосложение, светлые волосы, голубые глаза.",
            "Крупного телосложения, волосы русые, глаза зелёные.",
            "Рост 175 см, тёмные волосы, аккуратная борода, открытый взгляд."
        ]) if gender == "Мужской" else
        random.choice([
            "Среднего роста, стройная фигура, светлые волосы, зелёные глаза.",
            "Рост 168 см, спортивное телосложение, длинные русые волосы, карие глаза.",
            "Хрупкая, невысокого роста, тёмные волосы, сдержанный взгляд.",
            "Рост 165 см, аккуратная причёска, выразительные черты лица, голубые глаза."
        ])
    )
    character = random.choice([
        "Спокойный, рассудительный, трудолюбивый, но умеет постоять за себя.",
        "Сдержанный, надёжный, дисциплинированный, не лезет в конфликты первым.",
        "Умный, целеустремлённый, внимательный, справедливый, общительный.",
        "Дружелюбный, амбициозный, честный, всегда готов помочь."
    ]) if gender == "Мужской" else random.choice([
        "Добрая, внимательная, целеустремлённая, всегда поддержит близких.",
        "Сдержанная, рассудительная, умеет постоять за себя и друзей.",
        "Ответственная, трудолюбивая, обладает сильным характером.",
        "Общительная, отзывчивая, умеет слушать и давать советы."
    ])
    marital_status = random.choice([
        "Не женат.", "В отношениях.", "Женат.", "Разведён."
    ]) if gender == "Мужской" else random.choice([
        "Не замужем.", "В отношениях.", "Замужем.", "Разведена."
    ])
    is_convicted = random.choice([
        "Нет.", "Не судим.", "Судимости отсутствуют."
    ])
    hobbies = random.choice([
        "Футбол, баскетбол, настольные игры.",
        "Чтение, плавание, походы на природу.",
        "Бокс, стрельба, рыбалка, путешествия.",
        "Вождение, автомобили, волонтёрство, музыка."
    ])
    achievements = random.choice([
        "Был отмечен благодарностью за инициативу на рабочем месте.",
        "Участвовал в организации городского мероприятия.",
        "Повышен до бригадира в коллективе.",
        "Победитель городского конкурса по профессии.",
        "Неоднократно награждён почётными грамотами за добросовестный труд.",
        "Имеет положительные отзывы руководства.",
        "Стал наставником для новых сотрудников.",
        ""
    ])

    childhood_blocks = [
        f"Я родился в городе {city}, в обычной семье. Родители всегда поддерживали мои начинания и прививали уважение к окружающим.",
        f"Детство провёл по адресу: {parent_address}. Часто играл во дворе с друзьями, занимался спортом, помогал родителям по хозяйству.",
        "С ранних лет проявлял интерес к ремеслу, участвовал в школьных мероприятиях, любил мастерить поделки.",
        "В школе учился хорошо, особенно нравились уроки ОБЖ и истории.",
        "Мой отец всегда учил меня держать слово и быть честным.",
        "Каждое лето проводил у бабушки в деревне, где научился ценить простой труд и уважать природу.",
        "С малых лет мечтал стать частью большой организации и приносить пользу обществу.",
        "В детстве часто участвовал в спортивных соревнованиях и олимпиадах."
    ]
    childhood = "\n".join(random.sample(childhood_blocks, k=5))

    youth_blocks = [
        f"После окончания школы поступил в учебное заведение по специальности: {education.lower()}.",
        f"В юности начал работать: сначала {job}, затем получил опыт в разных сферах.",
        "Серьёзно увлёкся спортом — посещал секцию бокса, участвовал в городских соревнованиях.",
        "Участвовал в волонтёрских движениях, помогал организовывать городские мероприятия.",
        "Интересовался техническими науками, участвовал в студенческих конференциях.",
        "Во время учёбы проходил практику в различных организациях, что дало ценный опыт.",
        "В 18 лет был призван на службу, где закалил характер и научился работать в коллективе.",
        "Параллельно с учёбой подрабатывал, чтобы поддерживать семью."
    ]
    youth = "\n".join(random.sample(youth_blocks, k=5))

    present_blocks = [
        f"Сейчас мне {age} лет. Проживаю по адресу: {address}.",
        f"Работаю в организации: {org}, занимаю должность по профилю: {job}.",
        "Стараюсь развиваться профессионально, посещаю курсы и тренинги.",
        "В коллективе пользуюсь уважением, всегда готов прийти на помощь.",
        f"В свободное время занимаюсь хобби: {hobbies.lower()}",
        "Планирую в будущем получить повышение и продолжить карьерный рост.",
        "Поддерживаю отношения с семьёй и друзьями, участвую в жизни района.",
        achievements if achievements else "Считаю главным достижением — уважение и доверие коллег."
    ]
    present = "\n".join(random.sample(present_blocks, k=5))

    result = (
        f"<b>ФИО:</b> {fio}\n"
        f"<b>Пол:</b> {gender}\n"
        f"<b>Дата рождения:</b> Не указана\n"
        f"<b>Возраст:</b> {age}\n"
        f"<b>Национальность:</b> {nationality}\n"
        f"<b>Место рождения:</b> {city}\n"
        f"<b>Образование:</b> {education}\n"
        f"<b>Организация:</b> {org}\n"
        f"<b>Должность/работа:</b> {job}\n"
        f"<b>Отношение к воинской службе:</b> {army_status}\n"
        f"<b>Семья:</b> {family}\n"
        f"<b>Место проживания с родителями:</b> {parent_address}\n"
        f"<b>Описание внешности:</b> {appearance}\n"
        f"<b>Особенности характера:</b> {character}\n"
        f"<b>Ваше фото:</b> Фото отсутствует\n\n"
        f"<b>Детство:</b>\n{childhood}\n\n"
        f"<b>Юность:</b>\n{youth}\n\n"
        f"<b>Настоящее время:</b>\n{present}\n\n"
        f"<b>Семейное положение:</b> {marital_status}\n"
        f"<b>Место текущего проживания:</b> {address}\n"
        f"<b>Имеется ли судимость?:</b> {is_convicted}\n"
        f"<b>Ваше хобби:</b> {hobbies}"
    )
    return result

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    text = (
        "👋 <b>Добро пожаловать в RP Biography Bot!</b>\n\n"
        "Этот бот поможет тебе <b>создать уникальную RP-биографию</b> для мира <b>Black Russia</b> по всем правилам сервера.\n"
        "Бот задаст тебе несколько вопросов и соберёт анкету — а дальше сгенерирует красивую, грамотную биографию твоего персонажа.\n\n"
        "Нажми кнопку ниже, чтобы начать:"
    )
    await message.answer(text, reply_markup=menu_kb, parse_mode="HTML")

@dp.message(lambda m: m.text == "📝 Сгенерировать РП-биографию")
async def start_bio(message: types.Message, state: FSMContext):
    await state.set_state(BioStates.waiting_fio)
    await message.answer(
        "<b>1️⃣ Укажите ФИО персонажа:</b>\n\n"
        "Пример: <i>Иванов Иван Иванович</i>\n"
        "Имя и фамилия должны быть на русском языке, без нижних подчёркиваний.",
        parse_mode="HTML"
    )

@dp.message(BioStates.waiting_fio)
async def bio_fio(message: types.Message, state: FSMContext):
    fio = message.text.strip()
    if "_" in fio or not all(x.isalpha() or x.isspace() for x in fio):
        await message.answer(
            "⚠️ <b>ФИО должно быть на русском языке, без нижних подчёркиваний и лишних символов.</b>\n"
            "Попробуй ещё раз.\n"
            "Пример: <i>Иванов Иван Иванович</i>",
            parse_mode="HTML"
        )
        return
    await state.update_data(fio=fio)
    await state.set_state(BioStates.waiting_age)
    await message.answer(
        "<b>2️⃣ Укажите возраст персонажа:</b>\n"
        "Возраст должен быть от <b>18</b> до <b>65</b> лет.",
        parse_mode="HTML"
    )

@dp.message(BioStates.waiting_age)
async def bio_age(message: types.Message, state: FSMContext):
    try:
        age = int(message.text.strip())
        if age < 18 or age > 65:
            raise ValueError
    except ValueError:
        await message.answer(
            "⚠️ <b>Возраст должен быть числом от 18 до 65.</b>\nПопробуй ещё раз.",
            parse_mode="HTML"
        )
        return
    await state.update_data(age=age)
    await state.set_state(BioStates.waiting_nationality)
    await message.answer(
        "<b>3️⃣ Укажите национальность персонажа:</b>\n"
        "Пример: <i>Русский, Татарин, Армянин, Чеченец, Итальянец и т.п.</i>",
        parse_mode="HTML"
    )

@dp.message(BioStates.waiting_nationality)
async def bio_nationality(message: types.Message, state: FSMContext):
    nationality = message.text.strip().capitalize()
    await state.update_data(nationality=nationality)
    await state.set_state(BioStates.waiting_gender)
    await message.answer(
        "<b>4️⃣ Выберите пол персонажа:</b>",
        reply_markup=gender_kb,
        parse_mode="HTML"
    )

@dp.message(BioStates.waiting_gender)
async def bio_gender(message: types.Message, state: FSMContext):
    gender = message.text.strip()
    if gender not in ("Мужской", "Женский"):
        await message.answer(
            "⚠️ <b>Пожалуйста, выберите пол с помощью кнопок: Мужской или Женский.</b>",
            reply_markup=gender_kb,
            parse_mode="HTML"
        )
        return
    await state.update_data(gender=gender)
    data = await state.get_data()
    bio_text = generate_bio(data)
    await message.answer(
        "<b>Ваша уникальная RP-биография:</b>\n\n" + bio_text,
        parse_mode="HTML",
        reply_markup=menu_kb
    )
    await state.clear()

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    import sys
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
