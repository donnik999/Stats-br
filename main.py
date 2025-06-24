import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
import aiohttp
from bs4 import BeautifulSoup

API_TOKEN = "8124119601:AAEgnFwCalzIKU15uHpIyWlCRbu4wvNEAUw"

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher(storage=MemoryStorage())

FORUM_SEARCH_URL = "https://forum.blackrussia.online/index.php?search/&q={query}&type=post"

WELCOME_TEXT = (
    "👋 Привет! Я — бот для поиска информации об игроках Black Russia по NickName.\n"
    "Просто отправь мне никнейм, и я найду информацию с форума Black Russia.\n\n"
    "<i>Пожалуйста, указывай точный NickName для лучшего результата.</i>"
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
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status != 200:
                return None
            text = await resp.text()
            soup = BeautifulSoup(text, "html.parser")
            results = soup.select(".structItem-title a")
            if not results:
                return None
            result = results[0]
            title = result.get_text(strip=True)
            href = result["href"]
            if href.startswith("/"):
                href = "https://forum.blackrussia.online" + href
            # Поиск краткой информации в посте (если есть)
            post_preview = result.find_parent("div", class_="structItem").select_one(".structItem-snippet")
            post_text = post_preview.get_text(strip=True) if post_preview else "Без превью"
            return (f"<b>Найдено:</b>\n"
                    f"🔗 <a href='{href}'>{title}</a>\n"
                    f"📝 {post_text}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(dp.start_polling(bot))
