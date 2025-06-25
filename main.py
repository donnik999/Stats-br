import telebot
from telebot import types
import random

TOKEN = '8124119601:AAEgnFwCalzIKU15uHpIyWlCRbu4wvNEAUw'
bot = telebot.TeleBot(TOKEN)

# --- СПИСКИ ДЛЯ ГЕНЕРАЦИИ ---
JOBS = [
    "Таксист", "Рыболов", "Механик", "Работник на ферме", "Работник на Заводе", "Водолаз",
    "Электрик", "Газовщик", "Крупье", "Инкассатор", "Водитель автобуса", "Кладоискатель",
    "Охотник", "Курьер", "Строитель", "Дальнобойщик"
]
ORGS = [
    "ФСБ", "ГИБДД", "УМВД", "Правительство", "Больница", "СМИ", "ФСИН", "Воинская часть"
]
CHARACTERS = [
    "Спокойный", "Сдержанный", "Агрессивный", "Решительный", "Настойчивый", "Эмоциональный",
    "Легкомысленный", "Доброжелательный", "Ответственный", "Харизматичный", "Честный", "Целеустремлённый",
    "Добрый", "Злопамятный", "Упрямый", "Открытый", "Внимательный", "Терпеливый"
]
HOBBIES = [
    "Стрельба из лука", "Готовка блюд", "Езда на велосипеде", "Стрельба в тире", "Верховая езда",
    "Плавание", "Катание на коньках и роликах", "Чтение книг", "Слушать музыку", "Путешествия",
    "Рыбалка", "Футбол", "Волейбол", "Восстановление старых вещей", "Туризм"
]
PLACES = [
    "Арзамас", "Батырево", "Гарель", "Горки", "Рублевка", "Южный", "Нижегородск", "Бусаево", "Корякино", "Егоровка"
]
FAMILY_SAMPLES = [
    "Вырос в крепкой и дружной семье. Отец – водитель, мать – повар, есть младший брат и сестра.",
    "Воспитывался матерью, которая всю жизнь работала на заводе, отец ушёл из семьи рано.",
    "Родители – инженеры, с детства приучали к труду. Есть младший брат.",
    "Живу с женой Екатериной и двумя детьми, поддерживаем друг друга в трудные моменты.",
    "Семья небольшая, но дружная – мама, папа и младший брат."
]
EDUCATION_SAMPLES = [
    "Окончил колледж по специальности «техник-механик».",
    "Учился в политехническом колледже на автомеханика.",
    "Получил среднее профессиональное образование, выбрал инженерное направление.",
    "Закончил школу с уклоном на технические науки."
]
CHILDHOOD_SAMPLES = [
    "С детства помогал отцу в гараже, научился разбирать и собирать технику.",
    "Детство прошло в обычной семье, много времени проводил на улице, занимался спортом.",
    "Часто проводил время на автостоянках, увлекался машинами и техникой.",
    "В школе учился средне, но всегда помогал семье по хозяйству.",
    "С ранних лет работал, чтобы помочь семье, мыл машины, таскал сумки с рынка."
]
YOUTH_SAMPLES = [
    "В юности работал по разным специальностям – курьер, водитель, механик.",
    "Пробовал себя в различных работах – таксист, кладоискатель, водолаз.",
    "Учился и работал одновременно, чтобы накопить на собственный автомобиль.",
    "С юности мечтал открыть свой бизнес и постоянно совершенствовал навыки.",
    "Стал самостоятельным, начал зарабатывать собственные деньги."
]
ADULT_LIFE_SAMPLES = [
    "Сейчас работаю в крупной организации, совмещаю несколько профессий.",
    "Работаю на станции техобслуживания, планирую открыть свой автосервис.",
    "Занимаюсь перевозками ценных грузов, известен своей надёжностью.",
    "Стал менеджером в автосалоне, изучаю предпринимательство.",
    "Продолжаю профессионально развиваться, занимаюсь техническим обслуживанием."
]
APPEARANCE_SAMPLES = [
    "Рост 178 см, спортивное телосложение, карие глаза, короткие тёмные волосы.",
    "Худощавый, но выносливый, волосы русые, глаза серые, всегда аккуратная одежда.",
    "Среднего роста, крепкое телосложение, на лице заметный шрам.",
    "Внимательный взгляд, тёмные волосы, на плече татуировка.",
    "Ничем не примечательная внешность, что только помогает оставаться незаметным."
]

# --- ШАБЛОНЫ ДЛЯ СЕРВЕРОВ ---
BIO_TEMPLATES = {
    "Red": (
        "<b>Имя и Фамилия:</b> {name} {surname}\n"
        "<b>Пол:</b> {gender}\n"
        "<b>Возраст:</b> {age}\n"
        "<b>Национальность:</b> {nationality}\n"
        "<b>Семья:</b> {family}\n"
        "<b>Место рождения:</b> {place_birth}\n"
        "<b>Место проживания:</b> {place_live}\n"
        "<b>Образование:</b> {education}\n"
        "<b>Работа:</b> {job} ({org})\n"
        "<b>Внешность:</b> {appearance}\n"
        "<b>Характер:</b> {character}\n"
        "<b>Хобби:</b> {hobby}\n"
        "<b>Детство:</b> {childhood}\n"
        "<b>Юность:</b> {youth}\n"
        "<b>Взрослая жизнь:</b> {adultlife}\n"
    ),
    "Blue": (
        "<b>Имя:</b> {name}\n"
        "<b>Фамилия:</b> {surname}\n"
        "<b>Возраст:</b> {age}\n"
        "<b>Пол:</b> {gender}\n"
        "<b>Национальность:</b> {nationality}\n"
        "<b>Семья:</b> {family}\n"
        "<b>Город рождения:</b> {place_birth}\n"
        "<b>Город проживания:</b> {place_live}\n"
        "<b>Образование:</b> {education}\n"
        "<b>Профессия:</b> {job}\n"
        "<b>Организация:</b> {org}\n"
        "<b>Описание внешности:</b> {appearance}\n"
        "<b>Черты характера:</b> {character}\n"
        "<b>Хобби:</b> {hobby}\n"
        "<b>Детские годы:</b> {childhood}\n"
        "<b>Юность:</b> {youth}\n"
        "<b>Взрослая жизнь:</b> {adultlife}\n"
    ),
    "Orange": (
        "👤 <b>Биография персонажа:</b>\n"
        "Имя: {name} {surname}\n"
        "Возраст: {age} | Пол: {gender} | Нац.: {nationality}\n"
        "Семья: {family}\n"
        "Родом из: {place_birth} | Живёт: {place_live}\n"
        "Образование: {education}\n"
        "Работа: {job} ({org})\n"
        "Внешность: {appearance}\n"
        "Характер: {character}\n"
        "Хобби: {hobby}\n"
        "Детство: {childhood}\n"
        "Юность: {youth}\n"
        "Взрослая жизнь: {adultlife}\n"
    ),
    # Все остальные — как Red (можно добавить свои шаблоны по аналогии)
}

DEFAULT_TEMPLATE = (
    "<b>Имя и Фамилия:</b> {name} {surname}\n"
    "<b>Пол:</b> {gender}\n"
    "<b>Возраст:</b> {age}\n"
    "<b>Национальность:</b> {nationality}\n"
    "<b>Семья:</b> {family}\n"
    "<b>Место рождения:</b> {place_birth}\n"
    "<b>Место проживания:</b> {place_live}\n"
    "<b>Образование:</b> {education}\n"
    "<b>Работа:</b> {job} ({org})\n"
    "<b>Внешность:</b> {appearance}\n"
    "<b>Характер:</b> {character}\n"
    "<b>Хобби:</b> {hobby}\n"
    "<b>Детство:</b> {childhood}\n"
    "<b>Юность:</b> {youth}\n"
    "<b>Взрослая жизнь:</b> {adultlife}\n"
)

# --- СОСТОЯНИЕ ДЛЯ ДИАЛОГА ---
user_states = {}

def main_menu():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("📝 Написать РП биографию")
    btn2 = types.KeyboardButton("📬 Связь с автором")
    kb.add(btn1)
    kb.add(btn2)
    return kb

def servers_menu():
    kb = types.InlineKeyboardMarkup(row_width=2)
    for srv in ['Red', 'Green', 'Blue', 'Yellow', 'Orange', 'Purple', 'Lime', 'Pink', 'Cherry', 'Black']:
        kb.add(types.InlineKeyboardButton(text=srv, callback_data=f"server_{srv}"))
    return kb

@bot.message_handler(commands=['start', 'menu'])
def start_message(message):
    user_states.pop(message.chat.id, None)
    text = (
        "👋 <b>Добро пожаловать в RP Bio Бот!</b>\n\n"
        "📖 Здесь ты можешь создать уникальную RP-биографию для любого сервера.\n\n"
        "Выбери действие ниже:"
    )
    bot.send_message(message.chat.id, text, parse_mode='HTML', reply_markup=main_menu())

@bot.message_handler(func=lambda m: m.text == "📝 Написать РП биографию")
def write_bio(message):
    user_states[message.chat.id] = {"step": "choose_server"}
    bot.send_message(
        message.chat.id,
        "🌐 <b>Выбери сервер для своей биографии:</b>",
        parse_mode='HTML',
        reply_markup=servers_menu()
    )

@bot.message_handler(func=lambda m: m.text == "📬 Связь с автором")
def contact_author(message):
    text = (
        "💬 <b>Обратная связь с автором</b>\n\n"
        "Есть вопросы, идеи или предложения? Пиши в Telegram: "
        "<a href='https://t.me/bunkoc'>@bunkoc</a>\n\n"
        "🌟 Автор всегда рад новым знакомствам и идеям! "
        "Возможно, именно твоя мысль сделает бота ещё круче 🚀"
    )
    bot.send_message(message.chat.id, text, parse_mode='HTML', disable_web_page_preview=True)

@bot.callback_query_handler(func=lambda call: call.data.startswith("server_"))
def handle_server_choice(call):
    server = call.data.replace("server_", "")
    user_states[call.message.chat.id] = {"step": "ask_name", "server": server}
    bot.send_message(call.message.chat.id, "Введите <b>Имя</b> персонажа:", parse_mode='HTML')

@bot.message_handler(func=lambda m: user_states.get(m.chat.id, {}).get("step") == "ask_name")
def ask_surname(message):
    user_states[message.chat.id]["name"] = message.text.strip()
    user_states[message.chat.id]["step"] = "ask_surname"
    bot.send_message(message.chat.id, "Введите <b>Фамилию</b> персонажа:", parse_mode='HTML')

@bot.message_handler(func=lambda m: user_states.get(m.chat.id, {}).get("step") == "ask_surname")
def ask_age(message):
    user_states[message.chat.id]["surname"] = message.text.strip()
    user_states[message.chat.id]["step"] = "ask_age"
    bot.send_message(message.chat.id, "Введите <b>Возраст</b> персонажа:", parse_mode='HTML')

@bot.message_handler(func=lambda m: user_states.get(m.chat.id, {}).get("step") == "ask_age")
def ask_gender(message):
    user_states[message.chat.id]["age"] = message.text.strip()
    user_states[message.chat.id]["step"] = "ask_gender"
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    kb.add("Мужской", "Женский")
    bot.send_message(message.chat.id, "Выберите <b>Пол</b> персонажа:", parse_mode='HTML', reply_markup=kb)

@bot.message_handler(func=lambda m: user_states.get(m.chat.id, {}).get("step") == "ask_gender")
def ask_nationality(message):
    user_states[message.chat.id]["gender"] = message.text.strip()
    user_states[message.chat.id]["step"] = "ask_nationality"
    bot.send_message(message.chat.id, "Введите <b>Национальность</b> персонажа:", parse_mode='HTML', reply_markup=types.ReplyKeyboardRemove())

@bot.message_handler(func=lambda m: user_states.get(m.chat.id, {}).get("step") == "ask_nationality")
def generate_full_bio(message):
    user_states[message.chat.id]["nationality"] = message.text.strip()
    data = user_states.pop(message.chat.id)
    text = generate_bio(data)
    bot.send_message(message.chat.id, text, parse_mode='HTML', reply_markup=main_menu())
    # Если шаблон содержит фото — отдельное сообщение
    if data["server"] in ["Orange", "Blue"]:  # или добавить любые, где нужно фото
        bot.send_message(message.chat.id, "📸 <b>Пожалуйста, прикрепите своё фото для этого пункта биографии.</b>", parse_mode='HTML')

def generate_bio(data):
    name = data["name"]
    surname = data["surname"]
    age = data["age"]
    gender = data["gender"]
    nationality = data["nationality"]
    server = data["server"]

    family = random.choice(FAMILY_SAMPLES)
    place_birth = random.choice(PLACES)
    place_live = random.choice(PLACES)
    education = random.choice(EDUCATION_SAMPLES)
    job = random.choice(JOBS)
    org = random.choice(ORGS)
    appearance = random.choice(APPEARANCE_SAMPLES)
    character = ", ".join(random.sample(CHARACTERS, 3))
    hobby = ", ".join(random.sample(HOBBIES, 3))
    childhood = random.choice(CHILDHOOD_SAMPLES)
    youth = random.choice(YOUTH_SAMPLES)
    adultlife = random.choice(ADULT_LIFE_SAMPLES)

    template = BIO_TEMPLATES.get(server, DEFAULT_TEMPLATE)
    bio = template.format(
        name=name,
        surname=surname,
        age=age,
        gender=gender,
        nationality=nationality,
        family=family,
        place_birth=place_birth,
        place_live=place_live,
        education=education,
        job=job,
        org=org,
        appearance=appearance,
        character=character,
        hobby=hobby,
        childhood=childhood,
        youth=youth,
        adultlife=adultlife,
    )
    return f"📄 <b>RP-биография для сервера {server}:</b>\n\n{bio}"

@bot.message_handler(content_types=['text'])
def fallback(message):
    bot.send_message(
        message.chat.id,
        "Пожалуйста, выбери действие из меню ⬇️",
        reply_markup=main_menu()
    )

if __name__ == '__main__':
    print("Бот запущен!")
    bot.infinity_polling()
