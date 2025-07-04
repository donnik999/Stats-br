import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
import openai

TELEGRAM_TOKEN = "8124119601:AAEgnFwCalzIKU15uHpIyWlCRbu4wvNEAUw"   # <<-- ВСТАВЬ СВОЙ ТОКЕН
OPENAI_API_KEY = "hf_PCYhkBcvAAXOlVdeDDoQnztkhYaoxwgYfGywfMeMsOgA"      # <<-- ВСТАВЬ СВОЙ OpenAI ключ

openai.api_key = OPENAI_API_KEY

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Привет! Напиши мне что-нибудь, я спрошу у OpenAI.")

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
    await message.answer(reply, parse_mode="HTML")  # parse_mode здесь, а не при создании Bot

if __name__ == "__main__":
    asyncio.run(dp.start_polling(bot))
