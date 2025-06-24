import os
from aiogram import Bot, Dispatcher, executor, types

TOKEN = os.getenv("8124119601:AAEgnFwCalzIKU15uHpIyWlCRbu4wvNEAUw")
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=["start", "help"])
async def welcome(message: types.Message):
    await message.reply("Бот работает!")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True) logging
import re
import requests
from aiogram import Bot, Dispatcher, executor, types
from bs4 import BeautifulSoup

API_TOKEN = '8124119601:AAEgnFwCalzIKU15uHpIyWlCRbu4wvNEAUw'

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

def parse_forum_post(url):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(url, headers=headers, timeout=10)
    if response.status_code != 200:
        return "Не удалось получить страницу. Проверьте ссылку."

    soup = BeautifulSoup(response.text, 'html.parser')
    post = soup.find('article')
    if not post:
        return "Пост не найден."

    text = post.get_text(separator='\n')
    nickname_match = re.search(r'Ник[\s:—-]+([^\n\r]+)', text, re.IGNORECASE)
    level_match = re.search(r'Уровень[\s:—-]+(\d+)', text, re.IGNORECASE)

    nickname = nickname_match.group(1).strip() if nickname_match else "Не найден"
    level = level_match.group(1) if level_match else "Не найден"

    # Поиск всех картинок в посте
    images = [img['src'] for img in post.find_all('img') if img.get('src')]

    result = f"<b>Никнейм:</b> {nickname}\n<b>Уровень:</b> {level}\n\n"
    if images:
        result += "Скриншоты:\n" + "\n".join(images)
    else:
        result += "Скриншоты не найдены."

    return result

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply(
        "Привет! Отправь команду:\n"
        "/stats <ссылка_на_пост_с_форума>\n\n"
        "Пример:\n"
        "/stats https://forum.blackrussia.online/threads/.../post-53120478"
    )

@dp.message_handler(commands=['stats'])
async def stats_handler(message: types.Message):
    parts = message.text.strip().split()
    if len(parts) < 2:
        await message.reply("Пожалуйста, укажи ссылку на пост после команды /stats")
        return

    url = parts[1]
    await message.reply("Парсим данные, подожди пару секунд...")
    try:
        result = parse_forum_post(url)
        await message.reply(result, parse_mode='HTML')
    except Exception as e:
        await message.reply(f"Ошибка при парсинге: {e}")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
