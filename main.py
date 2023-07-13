from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from constant import *
from start_commands import *
from utils import *
from btns import *
from msgs import *
from http.server import BaseHTTPRequestHandler, HTTPServer

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

@dp.message_handler(commands=['start'])
async def handle_start_wrapper(message: types.Message):
    await handle_start(message)

@dp.callback_query_handler(func=lambda call: True)
async def handle_btn_click_wrapper(call: types.CallbackQuery):
    await handle_btn_click(call)

@dp.message_handler(func=lambda message: message.chat.id in user_state and user_state[message.chat.id] == STATE_WAITING_BATCH_LINKS)
async def handle_batch_wrapper(message: types.Message):
    await handle_batch_links(message)

class WebhookHandler(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        update_data = self.rfile.read(content_length)
        update = types.Update.de_json(update_data.decode('utf-8'))
        dp.process_update(update)
        self._set_response()

def run_server():
    server_address = ('', 3000)  # Update port number if needed
    httpd = HTTPServer(server_address, WebhookHandler)
    httpd.serve_forever()

if __name__ == '__main__':
    bot.remove_webhook()
    bot.set_webhook(url=WEBHOOK_URL)

    run_server()
