import asyncio
import logging
import requests
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.enums import ParseMode
from aiogram.utils.markdown import hcode

# 🧠 Вставь свои токены сюда
TELEGRAM_BOT_TOKEN = "8124119601:AAEgnFwCalzIKU15uHpIyWlCRbu4wvNEAUw"
HUGGINGFACE_API_TOKEN = "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"
HUGGINGFACE_MODEL = "gpt2"  # можно сменить на другую модель

# --- Hugging Face API ---
HF_API_URL = f"https://api-inference.huggingface.co/models/{HUGGINGFACE_MODEL}"
HEADERS = {"Authorization": f"Bearer {HUGGINGFACE_API_TOKEN}"}


# --- Обработка команды /start ---
async def cmd_start(message: Message):
    await message.answer("Привет! Напиши мне что-нибудь, и я отвечу с помощью Hugging Face 🤖")


# --- Обработка текстовых сообщений ---
async def handle_text(message: Message):
    user_input = message.text
    payload = {"inputs": user_input}

    try:
        await message.chat.do("typing")
        response = requests.post(HF_API_URL, headers=HEADERS, json=payload, timeout=30)
        data = response.json()

        if isinstance(data, dict) and "error" in data:
            await message.answer(f"Ошибка: {hcode(data['error'])}", parse_mode=ParseMode.HTML)
        elif isinstance(data, list) and "generated_text" in data[0]:
            generated = data[0]["generated_text"]
            reply = generated[len(user_input):].strip()
            await message.answer(reply or "Модель вернула пустой ответ 🤔")
        else:
            await message.answer("Что-то пошло не так. Попробуй снова.")
    except Exception as e:
        await message.answer(f"Ошибка при обращении к API: {e}")


# --- Основной запуск ---
async def main():
    logging.basicConfig(level=logging.INFO)

    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    dp = Dispatcher()

    dp.message.register(cmd_start, CommandStart())
    dp.message.register(handle_text, F.text & ~F.command)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
