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


@dp.message_handler(Command("start"))
async def handle_start(message: types.Message):
    await handle_start(bot,message)


@dp.callback_query_handler()
async def handle_btn_click(call: types.CallbackQuery):
    await handle_button_click(call)


@dp.message_handler(state='*', func=lambda message: message.chat.id in user_state and user_state[message.chat.id] == STATE_WAITING_BATCH_LINKS)
async def handle_batch(message: types.Message, state: FSMContext):
    await handle_batch_links(bot,message)


if __name__ == '__main__':
    from aiogram import executor

    executor.start_polling(dp, skip_updates=True)
