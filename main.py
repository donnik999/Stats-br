import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.enums import ParseMode
import openai

TELEGRAM_TOKEN = "8124119601:AAEgnFwCalzIKU15uHpIyWlCRbu4wvNEAUw"  # Например: "1234567890:AA..."
OPENAI_API_KEY = "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"     # Например: "sk-..."

openai.api_key = OPENAI_API_KEY

bot = Bot(token=TELEGRAM_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Привет! Напиши мне что-нибудь, и я отвечу через OpenAI.")

@dp.message(F.text)
async def chat_with_gpt(message: types.Message):
    try:
        resp = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Ты дружелюбный ассистент."},
                {"role": "user", "content": message.text}
            ],
            max_tokens=150,
        )
        reply = resp['choices'][0]['message']['content']
    except Exception as e:
        reply = f"Ошибка OpenAI: {e}"
    await message.answer(reply)

if __name__ == "__main__":
    asyncio.run(dp.start_polling(bot))
