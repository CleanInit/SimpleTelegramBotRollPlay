import asyncio
import aiogram
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import Message, ContentType
from aiogram.enums import DiceEmoji
from aiogram.filters import Command

from dotenv import load_dotenv
import os 

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

waiting_for_user_dice = {}

@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer("Привет! Нажми /roll чтобы бросить кубик 🎲")

@dp.message(Command("roll"))
async def cmd_roll(message: Message):
    await message.reply(f"Кидаю кубик и после этого кидаешь ты, посмотрим кто выйграет!")
    dice = await message.answer_dice(emoji="🎲")
    waiting_for_user_dice[message.from_user.id] = dice.dice.value

@dp.message(F.content_type == ContentType.DICE)
async def handle_user_dice(message: Message):
    user_id = message.from_user.id
    if user_id in waiting_for_user_dice:
        if message.dice.emoji == DiceEmoji.DICE:
            await asyncio.sleep(3)
            user_value = message.dice.value
            bot_value = waiting_for_user_dice.get(user_id)
            if user_value == bot_value:
                await message.answer(f"Ничья! 🎲")
            elif user_value > bot_value:
                await message.answer(f"ТЫ выйграл у тебя выпало {user_value}, больше чем у бота (У бота выпало {bot_value})! 🎲")
            elif bot_value < user_value:
                await message.answer(f"ТЫ проиграл у тебя выпало {user_value}, меньше чем у бота (У бота выпало {bot_value})! 🎲")
            waiting_for_user_dice.pop(user_id)
        else:
            await message.reply(f"Вы выбрали не правильный эмодзи, выберите кубик! 🎲")
    else:
        await message.reply(f"Для начала игры напишите /roll")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
