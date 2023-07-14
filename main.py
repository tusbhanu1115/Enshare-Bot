import telebot
from constant import *
from start_commands import *
from utils import *
from btns import *
from msgs import *
from http.server import BaseHTTPRequestHandler, HTTPServer
import asyncio

bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
async def handle_start_wrapper(message):
    await handle_start(bot, message)

@bot.callback_query_handler(func=lambda call: True)
def handle_btn_click_wrapper(call):
    handle_button_click(bot, call)

@bot.message_handler(func=lambda message: message.chat.id in user_state and user_state[message.chat.id] == STATE_WAITING_BATCH_LINKS)
def handle_batch_wrapper(message):
    handle_batch_links(bot, message)

class WebhookHandler(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        update_data = self.rfile.read(content_length)
        update = telebot.types.Update.de_json(update_data.decode('utf-8'))
        asyncio.run(self.process_update(bot, update))  # Use asyncio.run to await the coroutine
        self._set_response()

    async def process_update(self, bot, update):
        await bot.process_new_updates([update])

