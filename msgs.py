from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from utils import *

bot = Client(
    "my_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=API_TOKEN
)

@bot.on_message(filters.create(lambda message: message.chat.id in user_state and user_state[message.chat.id] == STATE_WAITING_BATCH_LINKS))
def handle_batch_wrapper(client, message):
    batch_links = message.text.strip().split('-')
    if len(batch_links) == 2:
        start_link = batch_links[0].strip()
        end_link = batch_links[1].strip()

        start_num = start_link.split('/')[-1]
        end_num = end_link.split('/')[-1]

        random_value = generate_random_value(8)
        unique_link = f"https://t.me/ensharebot?start={random_value}_{start_num}-{end_num}"
        batchgen_msg = "<b>🎉 Congratulations! You have created a new sharable batch.</b>\nAnyone accessing the bot from the provided link will get all the contents of the batch."

        keyboard = InlineKeyboardMarkup(
            [[InlineKeyboardButton("🔥 Copy Link 🔥", callback_data='copy')]]
        )

        client.send_message(message.chat.id, batchgen_msg, reply_markup=keyboard, parse_mode='HTML')

        user_state.pop(message.chat.id)

        unique_link = str(unique_link)

        user_state[message.chat.id] = unique_link
    else:
        client.send_message(message.chat.id, "Invalid input. Please provide both the start and end links separated by '-'.")
