import telebot
from constant import *
from start_commands import *
from utils import *
from btns import *
from msgs import *
from http.server import BaseHTTPRequestHandler, HTTPServer

bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def handle_start_wrapper(message):
    handle_start(bot, message)

@bot.callback_query_handler(func=lambda call: True)
def handle_btn_click_wrapper(call):
    handle_button_click(bot,call)

@bot.message_handler(func=lambda message: message.chat.id in user_state and user_state[message.chat.id] == STATE_WAITING_BATCH_LINKS)
def handle_batch_wrapper(message):
    handle_batch_links(bot,message)

bot.polling()
