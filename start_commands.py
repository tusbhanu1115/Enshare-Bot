from utils import *
from telebot import types
from collections import deque
import asyncio
from aiogram import Bot, Dispatcher, types

async def send_multiple_messages(chat_id):
    messages = ["Message 1", "Message 2", "Message 3"]

    for message in messages:
        await bot.send_message(chat_id, message)
        await asyncio.sleep(1)  # Add a delay between messages (optional)

async def handle_start(bot,message: types.Message):
    # Start sending messages asynchronously
    await send_multiple_messages(message.chat.id)


