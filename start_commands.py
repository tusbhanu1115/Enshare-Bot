from utils import *
from telebot import types

async def handle_start(bot, message):
    if message.text.startswith('/start'):
        split_text = message.text.split('/start ')
        if len(split_text) > 1:
            start_value = ' '.join(split_text[1:])
            start_id, end_id = extract_nums(start_value)
            await forward_posts(bot, message.chat.id, start_id, end_id)
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
                
                # Store the list of files to be sent in the user's state
                user_state[message.chat.id] = {
                    'files': ['file1.txt', 'file2.pdf', 'file3.jpg'],  # Replace with your list of file names
                    'current_index': 0
                }

                # Start sending files
                await send_next_file(bot, message.chat.id)
            else:
                unauthorized_msg = "<b>❌ Don't send me messages directly. You can only access me using special links provided on our channels.</b>"
                bot.send_message(message.chat.id, unauthorized_msg, parse_mode='HTML')

async def send_next_file(bot, chat_id):
    user_data = user_state.get(chat_id)
    if user_data:
        files = user_data.get('files')
        current_index = user_data.get('current_index')
        if files and current_index < len(files):
            file_name = files[current_index]
            # Send the file
            await bot.send_document(chat_id, open(file_name, 'rb'))

            # Update the current_index
            current_index += 1
            user_data['current_index'] = current_index

            # If there are more files, wait for a while and send the next one
            if current_index < len(files):
                await asyncio.sleep(2)  # Adjust the delay between sending files
                await send_next_file(bot, chat_id)
        else:
            # All files have been sent
            bot.send_message(chat_id, "All files have been sent.")
            # Clear the user's state
            del user_state[chat_id]
