from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from utils import *

bot = Client(
    "my_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=API_TOKEN
)

@bot.on_message(filters.command(['start']))
def handle_start_wrapper(client, message):
    if len(message.command) > 1:
        start_value = ' '.join(message.command[1:])
        start_id, end_id = extract_nums(start_value)
        forward_posts(client, message.chat.id, start_id, end_id)
    else:
        if message.from_user.id == OWNER_ID:
            keyboard = InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("😊 About Me", callback_data='about_me')],
                    [InlineKeyboardButton("🔒 Close", callback_data='close')],
                    [InlineKeyboardButton("⚡️ Generate Batch ⚡️", callback_data='genbatch')]
                ]
            )

            WELCOME_MSG = "<b>Hello {name}.</b> I can store private files in a specified channel, and other users can access them from a special link."

            welcome_msg = WELCOME_MSG.format(name=message.from_user.first_name)
            client.send_message(message.chat.id, welcome_msg, reply_markup=keyboard, parse_mode='HTML')
        else:
            unauthorized_msg = "<b>❌ Don't send me messages directly. You can only access me using special links provided on our channels.</b>"
            client.send_message(message.chat.id, unauthorized_msg, parse_mode='HTML')
