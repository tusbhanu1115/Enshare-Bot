import random
import re
import string
import telebot
from constant import *

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
