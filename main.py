import os
import random
import logging
import getpass
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
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

class BioStates(StatesGroup):
    waiting_fio = State()
    waiting_age = State()
    waiting_nationality = State()

# ----------------- Генератор РП-Биографии ------------------

def generate_bio(data: dict) -> str:
    # Данные пользователя
    fio = data.get("fio", "Не указано")
    age = data.get("age", "Не указано")
    nationality = data.get("nationality", "Не указано")
    # Для примера генерируем остальное случайно — можно добавить больше вопросов
    gender = random.choice(["Мужской", "Женский"])
    photo = "Фото отсутствует"
    city_list = ["Арзамас", "Бусаево", "Южный", "Лыткарино", "Морское", "Батырево", "Горки", "Новый Арзамас"]
    city = random.choice(city_list)
    edu_list = [
        "Среднее общее", "Средне-специальное", "Высшее экономическое", "Высшее юридическое", "ПТУ", "Технический лицей"
    ]
    education = random.choice(edu_list)
    army_status = random.choice([
        "Отслужил срочную службу.", "Проходил службу, уволен в запас.", "Не служил по уважительной причине.",
        "Проходил альтернативную гражданскую службу."
    ])
    family = random.choice([
        "Отец — Сергей, мать — Марина. Братьев и сестер нет.",
        "Семья полная: родители и младшая сестра.",
        "Отец — ветеран МВД, мать — учительница. Есть старший брат.",
        "Мать — домохозяйка, отец — водитель. Единственный ребёнок."
    ])
    parent_address = city
    appearance = random.choice([
        "Спортивное телосложение, рост 180 см, волосы тёмные, глаза карие.",
        "Среднего роста, крепкое телосложение, голубые глаза, короткая стрижка.",
        "Крупного телосложения, светлые волосы, серо-зелёные глаза.",
        "Рост 175 см, тёмные волосы, аккуратная борода, выразительные брови."
    ])
    character = random.choice([
        "Спокойный, рассудительный, трудолюбивый, но умеет постоять за себя.",
        "Добрый, миролюбивый, справедливый, храбрый, смешной, амбициозный.",
        "Сдержанный, надёжный, дисциплинированный, не лезу в конфликты первым.",
        "Умный, целеустремлённый, внимательный, великодушный, вежливый."
    ])
    marital_status = random.choice([
        "Не женат.", "В отношениях.", "Женат.", "Разведён."
    ])
    current_address = city
    is_convicted = random.choice([
        "Нет, не имею.", "Нет.", "Не судим.", "Судимости отсутствуют."
    ])
    hobbies = random.choice([
        "Футбол, баскетбол, видеоигры.", "Чтение биографий, шахматы, плавание.",
        "Бокс, стрельба, кроссфит, рыбалка.", "Единоборства, автомобили, походы на природу."
    ])

    # --- Шаблоны для Детства ---
    childhood_blocks = [
        f"Я родился и вырос в городе {city}, одном из ключевых центров мира Black Russia. С ранних лет меня окружала атмосфера большого города — шум улиц, оживлённые рынки, дворовые баталии.",
        "Мои родители всегда старались привить мне трудолюбие и уважение к окружающим. Я помогал по дому, учился готовить, а в свободное время пропадал во дворе с друзьями.",
        "С малых лет я проявлял интерес к технике — разбирал старые компьютеры, собирал модели машин и участвовал в местных конкурсах.",
        "Детство было непростым, но тёплым: несмотря на скромные доходы семьи, у нас всегда находилось место для заботы и поддержки.",
        "Отец часто брал меня с собой на рыбалку или охоту за город. Там я учился выносливости, самостоятельности и уважению к природе.",
        "В школе я проявлял себя как активный ученик — участвовал в олимпиадах по истории и ОБЖ, был капитаном дворовой футбольной команды.",
        "Мечтал стать полицейским или бизнесменом, наблюдая за жизнью взрослых в нашем районе. Часто представлял себя владельцем собственного предприятия.",
        "Любил читать книги о героях Black Russia, вдохновляясь их историями и мечтая о своих подвигах."
    ]

    # --- Шаблоны для Юности ---
    youth_blocks = [
        f"После окончания школы поступил в {random.choice(['колледж', 'техникум', 'университет'])} в городе {city} по специальности '{education.lower()}'.",
        "В юности начал подрабатывать: сначала разносил газеты, затем устроился в автомастерскую и даже пробовал себя в доставке пиццы.",
        "Серьёзно увлёкся спортом — посещал секцию бокса и участвовал в городских соревнованиях.",
        f"В 18 лет пошёл служить — армия Black Russia закалила характер, научила работать в команде и принимать решения в сложных ситуациях.",
        "Параллельно с учёбой начал интересоваться предпринимательством: участвовал в стартапах, пробовал открыть свой небольшой бизнес.",
        "Вступил во фракцию — сначала обычным сотрудником, а спустя пару лет стал заместителем лидера. Этот опыт дал мне понимание настоящей командной работы.",
        "В университете был активистом, организовывал мероприятия, участвовал в RP-акциях и командных квестах.",
        "Учёба была непростой, но я справлялся: днём — лекции, вечером — подработка, ночью — подготовка к экзаменам."
    ]

    # --- Шаблоны для Настоящего времени ---
    present_blocks = [
        f"Сейчас мне {age} лет, и я живу в городе {current_address}. Работаю по специальности — {education.lower()}, развиваюсь в выбранном направлении.",
        "Служу во фракции (МВД/Армия/ОПГ/Бизнес) Black Russia, участвую в операциях, RP-сценариях, выполняю задания лидера.",
        "В свободное время занимаюсь спортом, поддерживаю физическую форму, слежу за новостями сервера.",
        "Планирую открыть собственный бизнес или занять лидерскую должность во фракции.",
        "Люблю проводить время с друзьями — вместе участвуем в рейдах, квестах и RP-мероприятиях.",
        "Постоянно учусь новому: прохожу курсы, изучаю экономику сервера, осваиваю новые профессии.",
        "Помогаю новичкам на сервере, делюсь опытом, участвую в жизни района.",
        "Верю, что впереди меня ждёт ещё много интересных событий и достижений в мире Black Russia."
    ]

    # Гарантия уникальности: случайное перемешивание и выбор 5–6 блоков для каждого раздела (можешь менять число)
    childhood = "\n".join(random.sample(childhood_blocks, k=6))
    youth = "\n".join(random.sample(youth_blocks, k=6))
    present = "\n".join(random.sample(present_blocks, k=6))

    # Итоговая биография — с красивым форматированием
    result = (
        f"<b>ФИО:</b> {fio}\n"
        f"<b>Пол:</b> {gender}\n"
        f"<b>Дата рождения:</b> Не указана\n"
        f"<b>Возраст:</b> {age}\n"
        f"<b>Национальность:</b> {nationality}\n"
        f"<b>Место рождения:</b> {city}\n"
        f"<b>Образование:</b> {education}\n"
        f"<b>Отношение к воинской службе:</b> {army_status}\n"
        f"<b>Семья:</b> {family}\n"
        f"<b>Место проживания на момент проживания с родителями:</b> {parent_address}\n"
        f"<b>Описание внешности:</b> {appearance}\n"
        f"<b>Особенности характера:</b> {character}\n"
        f"<b>Ваше фото:</b> {photo}\n\n"
        f"<b>Детство:</b>\n{childhood}\n\n"
        f"<b>Юность:</b>\n{youth}\n\n"
        f"<b>Настоящее время:</b>\n{present}\n\n"
        f"<b>Семейное положение:</b> {marital_status}\n"
        f"<b>Место текущего проживания:</b> {current_address}\n"
        f"<b>Имеется ли судимость?:</b> {is_convicted}\n"
        f"<b>Ваше хобби:</b> {hobbies}"
    )
    return result

# ----------------- Хендлеры ------------------

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
    data = await state.get_data()
    bio_text = generate_bio(data)
    await message.answer(
        "<b>Ваша уникальная RP-биография:</b>\n\n" + bio_text,
        parse_mode="HTML"
    )
    await state.clear()

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    import sys
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
