import pyperclip
from utils import *
from telebot import types

def handle_button_click(bot,call):
    if call.data == 'about_me':
        # Creating the custom keyboard with the "Back" button
        keyboard = types.InlineKeyboardMarkup()
        back = types.InlineKeyboardButton("👈 Back", callback_data='back')
        keyboard.add(back)

        text = "Created By: Tushar Bhanushali\nLanguage: Python"

        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=keyboard)
    elif call.data == 'close':
        # Delete the message sent by the bot
        bot.delete_message(call.message.chat.id, call.message.message_id)

        # Delete the replied-to message if available
        if call.message.reply_to_message:
            bot.delete_message(call.message.chat.id, call.message.reply_to_message.message_id)
    elif call.data == 'back':
        # Creating the custom keyboard with the "About Me" button
        keyboard = types.InlineKeyboardMarkup()
        aboutme = types.InlineKeyboardButton("😊 About Me", callback_data='about_me')
        close = types.InlineKeyboardButton("🔒 Close", callback_data='close')
        genbatch = types.InlineKeyboardButton("⚡️ Generate Batch ⚡️", callback_data='genbatch')

        keyboard.add(aboutme, close)
        keyboard.add(genbatch)

        # Sending the main start message with the "About Me" button
        bot.edit_message_text(WELCOME_MSG, call.message.chat.id, call.message.message_id, reply_markup=keyboard)
    elif call.data == 'genbatch':
        bot.send_message(call.message.chat.id, "Send me Batch Start & End Link (separated by '-')")
        user_state[call.message.chat.id] = STATE_WAITING_BATCH_LINKS
    elif call.data == 'copy':
        unique_link = user_state.get(call.message.chat.id)
        if unique_link:
            pyperclip.copy(unique_link)  # Copy the unique link to the clipboard

            copy_msg = "<b>✅ Sharable Batch link copied to clipboard.</b>"
            bot.send_message(call.message.chat.id, copy_msg, parse_mode='HTML')
        else:
            bot.send_message(call.message.chat.id, "Unable to copy the unique link. Please generate a valid batch first.")