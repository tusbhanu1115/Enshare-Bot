from utils import *
from telebot import types

def handle_start(bot,message):
    if message.text.startswith('/start'):
        split_text = message.text.split('/start ')
        if len(split_text) > 1:
            start_value = ' '.join(split_text[1:])
            start_id, end_id = extract_nums(start_value)
            forward_posts(bot,message.chat.id, start_id, end_id)
        else:
            if message.from_user.id == OWNER_ID:
                keyboard = types.InlineKeyboardMarkup()

                aboutme = types.InlineKeyboardButton("😊 About Me", callback_data='about_me')
                close = types.InlineKeyboardButton("🔒 Close", callback_data='close')
                genbatch = types.InlineKeyboardButton("⚡️ Generate Batch ⚡️", callback_data='genbatch')

                keyboard.add(aboutme, close)
                keyboard.add(genbatch)

                # Welcome message sent to users
                WELCOME_MSG = "<b>Hello {name}.</b> I can store private files in a specified channel, and other users can access them from a special link."

                welcome_msg = WELCOME_MSG.format(name=message.from_user.first_name)
                # Sending the initial message
                bot.send_message(message.chat.id, welcome_msg, reply_markup=keyboard, parse_mode='HTML')
            else:
                unauthorized_msg = "<b>❌ Don't send me messages directly. You can only access me using special links provided on our channels.</b>"
                bot.send_message(message.chat.id, unauthorized_msg, parse_mode='HTML')

def forward_posts(bot, chat_id, start_id, end_id):
    message_ids = []
    for post_id in range(start_id, end_id + 1):
        try:
            message = bot.forward_message(chat_id, CHAT_ID, post_id)
            message_ids.append(message.message_id)
        except telebot.apihelper.ApiTelegramException as e:
            print(f"Error forwarding message: {e}")
    
    # Sending a single message that includes all the forwarded posts
    if message_ids:
        bot.send_message(chat_id, "\n".join([f"https://t.me/{CHAT_ID}/{message_id}" for message_id in message_ids]))
