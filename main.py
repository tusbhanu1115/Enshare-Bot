import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from constant import *
from start_commands import *
from utils import *
from btns import *
from msgs import *

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())


@dp.message_handler(commands=['start'])
async def handle_start(message: types.Message):
    # Send six messages to the user
    for i in range(1, 7):
        await message.answer(f"This is message {i}")

        # Add a small delay between each message (optional)
        await asyncio.sleep(1)

if __name__ == '__main__':
    from aiogram import executor

    executor.start_polling(dp, skip_updates=True)
