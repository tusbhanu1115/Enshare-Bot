from utils import *
from telebot import types

def handle_start(bot,message):
    # Define the number of messages you want to send
    num_messages = 5
    
    # Loop to send multiple messages
    for i in range(num_messages):
        bot.send_message(message.chat.id, f"Message {i+1}")
        
    # Optionally, you can send a final message indicating completion
    bot.send_message(message.chat.id, "All messages sent!")


