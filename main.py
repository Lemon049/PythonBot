import telebot
import time
import webbrowser
import requests
from bs4 import BeautifulSoup
from telebot import types
import os
from telegram import Bot
import pandas as pd
import parsing
import sorting
import json
from telegram.ext import Updater


with open(os.path.dirname(os.path.realpath(__file__)) + '/token.txt') as file:
    TOKEN = file.readline().strip()

bot = telebot.TeleBot(TOKEN)

df2 = pd.read_excel('C:\\Users\\Yehor\\Documents\\GitHub\\PythonBot\\games.xlsx')

@bot.message_handler(commands=['start'])
def start(message):

    StartMarkup = types.ReplyKeyboardMarkup()

    btn1 = types.KeyboardButton('Menu')
    btn2 = types.KeyboardButton('Authors')
    StartMarkup.row(btn1,btn2)

    bot.send_message(message.chat.id, 'Please select option', reply_markup=StartMarkup)
    bot.register_next_step_handler(message, on_click)

def receive_game(message,Option):

    bot.send_message(message.chat.id, f'You entered: {message.text}')
    validation_of_game(message,message.text,Option)

def find_game_url(game_name):
    url = None
    for index, row in df2.iterrows():
        if row['Game Title'] == game_name:
            url = row['Link']
            break
    return url


def validation_of_game(message, user_input, Option):
    print(user_input)
    url = find_game_url(user_input)
    print(user_input)
    print(url)
    print(Option)
    if url is not None:
        if Option == 'first':
            print('ok')
            parsing.parsing_function(str(url))
            print('nice')
            process_first_option_input(message)
        else:
            print('not ok')
            parsing.parsing_function(str(url))
            process_second_option_input(message)
    else:
        bot.send_message(message.chat.id, f'You entered the wrong name of a game, please try again: {user_input}')
        bot.register_next_step_handler(message, receive_game, Option)

def process_first_option_input(message):
    df = pd.read_excel('C:\\Users\\Yehor\\Documents\\GitHub\\PythonBot\\scraped_data.xlsx')
    # Initialize dictionaries to store unique strings for each column
    unique_strings = {}

    # Process the 3rd, 4th, and 5th columns (indices 2, 3, and 4 respectively)
    for col_index in [1, 2, 3, 4]:
        # Select the column
        column_data = df.iloc[:, col_index]

        # Convert to a list and filter unique strings
        unique_strings[col_index] = list(set(column_data.astype(str)))

    # Print the unique strings for each column
    for col_index in [1, 2, 3, 4]:
        if col_index == 1:
            text = 'Platforms'
        elif col_index == 2:
            text = 'Editions'
        elif col_index == 3:
            text = 'Regions'
        else:
            text = 'Ways of accepting'

        bot.send_message(message.chat.id,
    f' {text}: \n'
         f'{unique_strings[col_index]}')
    bot.send_message(message.chat.id, 'Please provide data in the following format: Platforms,Editions,Regions,Ways of accepting')
    bot.register_next_step_handler(message, process_first_option_answer)
def process_first_option_answer(message):

    elements = message.text.split(',')

    # Convert the elements into an array
    data_array = list(elements)

    results_filtered = sorting.main_filtered_games(data_array[0], data_array[1], data_array[2], data_array[3])
    bot.send_message(message.chat.id, 'Filtered games:')
    for result in results_filtered:
        bot.send_message(message.chat.id, result)



def process_second_option_input(message):
    results_all = sorting.main_all_games()
    bot.send_message(message.chat.id, 'Games without filters:')
    for result in results_all:
        bot.send_message(message.chat.id, result)

def on_click(message):
    markup = types.ReplyKeyboardMarkup()

    btn1 = types.KeyboardButton('Data for specific region/platform of the game')
    btn2 = types.KeyboardButton('Data for all variants of the game')
    markup.row(btn1,btn2)


    markup2 = types.ReplyKeyboardMarkup()
    btn11 = types.KeyboardButton('Menu')
    markup2.row(btn11)
    Option = None
    if message.text == 'Menu':
        bot.send_message(message.chat.id, 'Please select option', reply_markup=markup)
        bot.register_next_step_handler(message, on_click)
    elif message.text == 'Data for specific region/platform of the game':
        Option = 'first'

        bot.send_message(message.chat.id, 'Please provide name of the game')

        bot.register_next_step_handler(message, receive_game,Option)

    elif message.text == 'Data for all variants of the game':
        Option = 'second'

        bot.send_message(message.chat.id, 'Please provide name of the game')

        bot.register_next_step_handler(message, receive_game, Option)

    elif message.text == 'Authors':
        bot.send_message(message.chat.id, 'Four random people', reply_markup=markup2)
        bot.register_next_step_handler(message, on_click)




if __name__ == '__main__':
    bot.polling(none_stop=True)
