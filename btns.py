from pyrogram import Client, filters
from utils import *
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

bot = Client(
    "my_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=API_TOKEN
)

@bot.on_callback_query()
def handle_button_click(client, callback_query):

    if callback_query.data == 'about_me':
        # Creating the custom keyboard with the "Back" button
        keyboard = InlineKeyboardMarkup(
            [[InlineKeyboardButton("👈 Back", callback_data='back')]]
        )

        text = "Created By: Tushar Bhanushali\nLanguage: Python"

        client.edit_message_text(callback_query.message.chat.id, callback_query.message.message_id, text, reply_markup=keyboard)

    elif callback_query.data == 'close':
        # Delete the message sent by the bot
        client.delete_messages(callback_query.message.chat.id, callback_query.message.message_id)

        # Delete the replied-to message if available
        if callback_query.message.reply_to_message:
            client.delete_messages(callback_query.message.chat.id, callback_query.message.reply_to_message.message_id)

    elif callback_query.data == 'back':
        # Creating the custom keyboard with the "About Me" button
        keyboard = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("😊 About Me", callback_data='about_me')],
                [InlineKeyboardButton("🔒 Close", callback_data='close')],
                [InlineKeyboardButton("⚡️ Generate Batch ⚡️", callback_data='genbatch')]
            ]
        )

        # Sending the main start message with the "About Me" button
        client.edit_message_text(callback_query.message.chat.id, callback_query.message.message_id, WELCOME_MSG, reply_markup=keyboard)

    elif callback_query.data == 'genbatch':
        client.send_message(callback_query.message.chat.id, "Send me Batch Start & End Link (separated by '-')")
        user_state[callback_query.message.chat.id] = STATE_WAITING_BATCH_LINKS

    elif callback_query.data == 'copy':
        unique_link = user_state.get(callback_query.message.chat.id)
        if unique_link:
            copy_msg = "<b>✅ Sharable Batch link copied to clipboard.</b>"
            bot.send_message(callback_query.message.chat.id, copy_msg, parse_mode='HTML')
        else:
            bot.send_message(callback_query.message.chat.id, "Unable to copy the unique link. Please generate a valid batch first.")

bot.start()
bot.run()
