from utils import *
from telebot import types
from collections import deque

def handle_start(message):
    # Enqueue multiple messages
    message_queue.extend(["Message 1", "Message 2", "Message 3"])
    
    # Start sending messages
    send_next_message(message.chat.id)

def send_next_message(chat_id):
    if message_queue:
        # Dequeue and send the next message
        message = message_queue.popleft()
        bot.send_message(chat_id, message)
        
        # Call the function recursively to send the next message
        send_next_message(chat_id)
