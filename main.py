import telebot
import time
import webbrowser
import requests
from bs4 import BeautifulSoup
from telebot import types
import os
from telegram import Bot
import pandas as pd
import json
from telegram.ext import Updater


with open(os.path.dirname(os.path.realpath(__file__)) + '/token.txt') as file:
    TOKEN = file.readline().strip()

bot = telebot.TeleBot(TOKEN)
file_path = 'C:\\Users\\Yehor\\Documents\\GitHub\\PythonBot\\scraped_data.xlsx'

@bot.message_handler(commands=['start'])
def start(message):
     
    df = pd.read_excel(file_path)

    # Initialize dictionaries to store unique strings for each column
    unique_strings = {}





    # Process the 3rd, 4th, and 5th columns (indices 2, 3, and 4 respectively)
    for col_index in [1,2, 3, 4]:
        # Select the column
        column_data = df.iloc[:, col_index]

        # Convert to a list and filter unique strings
        unique_strings[col_index] = list(set(column_data.astype(str)))

    # Print the unique strings for each column
    for col_index in [1,2, 3, 4]:
        print(f"column {col_index + 1}:")
        print(unique_strings[col_index])
        print()



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
    start(message)
def process_first_option_input(message):
    start(message)


def process_second_option_input(message):
    # User input for the second option
    user_input = message.text
    bot.send_message(message.chat.id, f'You entered: {user_input}')
    # Send the menu markup again
    start(message)


if __name__ == '__main__':
    bot.polling(none_stop=True)
