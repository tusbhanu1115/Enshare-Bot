from pyrogram import Client, filters
from constant import *
from start_commands import *
from utils import *
from btns import *
from msgs import *
from http.server import BaseHTTPRequestHandler, HTTPServer

bot = Client(
    "my_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=API_TOKEN
)

@bot.on_message(filters.command(['start']))
def handle_start_wrapper(client, message):
    handle_start(client, message)

@bot.on_callback_query()
def handle_btn_click_wrapper(client, callback_query):
    handle_button_click(client, callback_query)

@bot.on_message(filters.create(lambda message: message.chat.id in user_state and user_state[message.chat.id] == STATE_WAITING_BATCH_LINKS))
def handle_batch_wrapper(client, message):
    handle_batch_links(client, message)

class WebhookHandler(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        update_data = self.rfile.read(content_length)
        update = bot.parse_update(update_data.decode('utf-8'))
        bot.process_update(update)
        self._set_response()

def run_server():
    server_address = ('', 3000)  # Update port number if needed
    httpd = HTTPServer(server_address, WebhookHandler)
    httpd.serve_forever()

if __name__ == '__main__':
    bot.start()

    bot.set_webhook(WEBHOOK_URL, certificate=open('cert.pem', 'r'))  # Provide the path to your SSL certificate

    run_server()
