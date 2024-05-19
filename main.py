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
    StartMarkup.row(btn1,btn2)

    bot.send_message(message.chat.id, 'Please select option', reply_markup=StartMarkup)
    bot.register_next_step_handler(message, on_click)

def receive_game(message):

    bot.send_message(message.chat.id, f'You entered: {message.text}')
    validation_of_game(message,message.text)

def validation_of_game(message,user_input):
    print(user_input)
    if user_input == '1':
        bot.register_next_step_handler(message,process_first_option_input, user_input)
    else:
        bot.send_message(message.chat.id, f'You entered wrong name of a game, please try again {user_input}')
        bot.register_next_step_handler(message, receive_game)
def on_click(message):
    markup = types.ReplyKeyboardMarkup()

    btn1 = types.KeyboardButton('Data for specific region/platform of the game')
    btn2 = types.KeyboardButton('Data for all variants of the game')
    markup.row(btn1,btn2)


    markup2 = types.ReplyKeyboardMarkup()
    btn11 = types.KeyboardButton('Menu')
    markup2.row(btn11)

    if message.text == 'Menu':
        bot.send_message(message.chat.id, 'Please select option', reply_markup=markup)
        bot.register_next_step_handler(message, on_click)
    elif message.text == 'Data for specific region/platform of the game':
        bot.send_message(message.chat.id, 'Please provide name of the game', reply_markup=markup2)

        bot.register_next_step_handler(message, receive_game)

    elif message.text == 'Data for all variants of the game':
        bot.send_message(message.chat.id, 'Please provide name of the game', reply_markup=markup2)
        bot.register_next_step_handler(message, process_second_option_input)
    elif message.text == 'Authors':
        bot.send_message(message.chat.id, 'Four random people', reply_markup=markup2)
        bot.register_next_step_handler(message, on_click)


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
