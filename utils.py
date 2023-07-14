import random
import re
import string
from pyrogram import Client
from constant import *

bot = Client(
    "my_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=API_TOKEN
)

def generate_random_value(length):
    # Generate a random value of the specified length
    random_value = ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
    return random_value

def extract_nums(url):
    num1 = 0
    num2 = 0
    # Extract the number after '&'
    match = re.search(r'_(\d+)', url)
    if match:
        num1 = int(match.group(1))

    # Extract the number between '-' and get the number after '-'
    match = re.search(r'-(\d+)', url)
    if match:
        num2 = int(match.group(1))

    return num1, num2

def forward_posts(client, chat_id, start_id, end_id):
    for post_id in range(start_id, end_id + 1):
        try:
            message = client.forward_messages(chat_id, CHAT_ID, post_id)
        except Exception as e:
            print(f"Error forwarding message: {e}")
