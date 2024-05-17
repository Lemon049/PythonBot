import telebot
import time
import webbrowser
import requests
from bs4 import BeautifulSoup
from telebot import types
import os
import pandas as pd
import json

with open(os.path.dirname(os.path.realpath(__file__)) + '/token.txt') as file:
    TOKEN = file.readline().strip()

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    print('here')
    print('https://api.telegram.org/bot63xxxxxx71:AAFoxxxxn0hwA-2TVSxxxNf4c/getUpdates')
    # Create the payload with JSON encoding for options
    parameters = {
        "chat_id": 567656225,
        "question": "What's your favorite programming language?",
        "options": json.dumps(["Python", "JavaScript", "C++", "Java", "Go"]),  # JSON encode the options array
        "allows_multiple_answers": True,
        "is_anonymous": False
    }
    resp = requests.post(base_url, data=parameters)
    print(resp.text)

    StartMarkup = types.ReplyKeyboardMarkup()

    btn1 = types.KeyboardButton('Menu')
    btn2 = types.KeyboardButton('Authors')
    StartMarkup.row(btn1)
    StartMarkup.row(btn2)
    bot.send_message(message.chat.id, 'Please select option', reply_markup=StartMarkup)
    bot.register_next_step_handler(message, on_click)


def on_click(message):
    markup = types.ReplyKeyboardMarkup()

    btn1 = types.KeyboardButton('First option')
    markup.row(btn1)
    btn2 = types.KeyboardButton('Second option')
    btn3 = types.KeyboardButton('Third option')
    markup.row(btn2, btn3)

    markup2 = types.ReplyKeyboardMarkup()
    btn11 = types.KeyboardButton('Menu')
    markup2.row(btn11)

    if message.text == 'Menu':
        bot.send_message(message.chat.id, 'Please select option', reply_markup=markup)
        bot.register_next_step_handler(message, on_click)
    elif message.text == 'First option':
        bot.send_message(message.chat.id, 'Please provide data', reply_markup=markup2)
        # Instead of using input(), use message.text to get user input
        bot.register_next_step_handler(message, process_first_option_input)
    elif message.text == 'Second option':
        bot.send_message(message.chat.id, 'Please provide data', reply_markup=markup2)
        bot.register_next_step_handler(message, process_second_option_input)
    elif message.text == 'Third option':
        bot.send_message(message.chat.id, 'Please provide data', reply_markup=markup2)
        bot.register_next_step_handler(message, process_third_option_input)
    elif message.text == 'Authors':
        bot.send_message(message.chat.id, 'Four random people', reply_markup=markup2)
        bot.register_next_step_handler(message, on_click)

def process_third_option_input(message):
    print('here2')
    # Call the send_poll function to activate the poll
    send_poll(message)
def process_first_option_input(message):
    send_poll(message)


def process_second_option_input(message):
    # User input for the second option
    user_input = message.text
    bot.send_message(message.chat.id, f'You entered: {user_input}')
    # Send the menu markup again
    start(message)




base_url = f"https://api.telegram.org/bot{TOKEN}/sendPoll"

# Define your chat_id and question






def send_poll(message):
    print('here')
    # Create the payload with JSON encoding for options
    parameters = {
        "chat_id": 6572783840,
        "question": "What's your favorite programming language?",
        "options": json.dumps(["Python", "JavaScript", "C++", "Java", "Go"]),  # JSON encode the options array

    }
    resp = requests.post(base_url, data=parameters)
    print(resp.text)








if __name__ == '__main__':
    bot.polling(none_stop=True)
