import logging
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
import aiohttp
from bs4 import BeautifulSoup

import os

API_TOKEN = os.environ.get("API_TOKEN", "8124119601:AAEgnFwCalzIKU15uHpIyWlCRbu4wvNEAUw")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher(storage=MemoryStorage())

FORUM_SEARCH_URL = "https://forum.blackrussia.online/index.php?search/&q={query}&type=post"

WELCOME_TEXT = (
    "👋 Привет! Я помогу найти информацию об игроке Black Russia по никнейму.\n"
    "Просто отправь мне ник, и я покажу, что нашёл на форуме Black Russia."
)

@dp.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(WELCOME_TEXT)

@dp.message(F.text)
async def search_player(message: Message):
    nickname = message.text.strip()
    if len(nickname) < 3:
        await message.answer("⚠️ Никнейм должен содержать не менее 3 символов.")
        return
    await message.answer(f"🔎 Ищу информацию о <b>{nickname}</b> на форуме Black Russia...")

    info = await search_on_forum(nickname)
    if info:
        await message.answer(info, disable_web_page_preview=True)
    else:
        await message.answer(f"😔 Не удалось найти информацию о <b>{nickname}</b> на форуме.")

async def search_on_forum(nickname: str) -> str:
    url = FORUM_SEARCH_URL.format(query=nickname.replace(" ", "+"))
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as resp:
            if resp.status != 200:
                return None
            text = await resp.text()
            soup = BeautifulSoup(text, "lxml")

            # Поиск блоков с результатами
            items = soup.select(".structItem--post")
            if not items:
                # fallback на старую версию форума/темы
                items = soup.select(".structItem")

            results = []
            for item in items[:3]:  # максимум 3 результата
                title_a = item.select_one(".structItem-title a")
                if not title_a:
                    continue
                title = title_a.get_text(strip=True)
                link = title_a["href"]
                if link.startswith("/"):
                    link = "https://forum.blackrussia.online" + link

                # Отрывок сообщения
                snippet = item.select_one(".structItem-snippet")
                snippet_text = snippet.get_text(strip=True) if snippet else ""

                # Краткая информация об авторе/времени, если есть
                user_info = item.select_one(".structItem-minor")
                user_text = user_info.get_text(strip=True) if user_info else ""

                # Собираем результат
                result = f"🔗 <a href='{link}'>{title}</a>"
                if snippet_text:
                    result += f"\n📝 <i>{snippet_text}</i>"
                if user_text:
                    result += f"\n👤 {user_text}"
                results.append(result)

            if results:
                return "<b>Результаты поиска:</b>\n\n" + "\n\n".join(results)
            return None

if __name__ == "__main__":
    import asyncio
    asyncio.run(dp.start_polling(bot))
