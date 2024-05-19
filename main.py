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
import graph
import json
from telegram.ext import Updater
import os


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
    image_path2 = 'C:\\Users\\Yehor\\Documents\\GitHub\\PythonBot\\Table1.png'
    if os.path.exists(image_path2):
        print('remove')
        os.remove(image_path2)
        print('removed')

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

            parsing.funpay_parsing(str(user_input))

            process_first_option_input(message)

        else:
            parsing.funpay_parsing(str(user_input))

            process_second_option_input(message)
    else:
        bot.send_message(message.chat.id, f'You entered the wrong name of a game, please try again: {user_input}')
        bot.register_next_step_handler(message, receive_game, Option)


def process_first_option_input(message):
    df = pd.read_excel('C:\\Users\\Yehor\\Documents\\GitHub\\PythonBot\\scraped_data.xlsx')
    # Get unique platforms
    unique_platforms = df['Platform'].unique()
    platform_message = "Please select a platform from the following options:\n"
    for i, platform in enumerate(unique_platforms, start=1):
        platform_message += f"{i}. {platform}\n"
    bot.send_message(message.chat.id, platform_message)

    bot.register_next_step_handler(message, process_platform_selection, unique_platforms, df)


def process_platform_selection(message, unique_platforms, df):
    # Convert user_platform_choice to an integer
    user_platform_choice = int(message.text) - 1

    # Ensure user input is within valid range
    if 0 <= user_platform_choice < len(unique_platforms):
        selected_platform = unique_platforms[user_platform_choice]
        platform_df = df[df['Platform'] == selected_platform]

        bot.send_message(message.chat.id, f"Selected platform:{selected_platform}")
        # Get unique editions for the selected platform
        unique_editions = platform_df['Edition'].unique()

        editions_message = "Available editions for the selected platform:\n"
        for i, edition in enumerate(unique_editions, start=1):
            editions_message += f"{i}. {edition}\n"
        editions_message += "Please enter the number corresponding to your choice:"
        bot.send_message(message.chat.id, editions_message)

        # Register next step handler for edition selection
        bot.register_next_step_handler(message, process_edition_selection, selected_platform, unique_editions, df)
    else:
        # Handle invalid input
        bot.send_message(message.chat.id, "Invalid platform choice. Please select again.")
        process_first_option_input(message)

def process_edition_selection(message, selected_platform, unique_editions, df):
    user_edition_choice = int(message.text) - 1

    if 0 <= user_edition_choice < len(unique_editions):
        selected_edition = unique_editions[user_edition_choice]

        # 1. Write the selected edition
        bot.send_message(message.chat.id, f"Selected edition:{selected_edition}")

        # 2. Filter games based on selected platform and edition
        selected_games = df[(df['Platform'] == selected_platform) & (df['Edition'] == selected_edition)]

        if not selected_games.empty:
            # 3. Print their regions
            unique_regions = selected_games['Region'].unique()
            regions_message = "Available regions for the selected edition:\n"
            for i, region in enumerate(unique_regions, start=1):
                regions_message += f"{i}. {region}\n"
            regions_message += "Please enter the number corresponding to your choice:"
            bot.send_message(message.chat.id, regions_message)

            # Register next step handler for region selection
            bot.register_next_step_handler(message, process_region_selection, selected_games)
        else:
            bot.send_message(message.chat.id, "There are no games available for the selected platform and edition.")
            process_first_option_input(message)
    else:
        bot.send_message(message.chat.id, "Invalid edition choice. Please select again.")
        process_first_option_input(message)



def process_region_selection(message, selected_games):
    user_region_choice = int(message.text) - 1

    if 0 <= user_region_choice < len(selected_games):
        selected_region = selected_games.iloc[user_region_choice]['Region']

        # 4. Write the selected region
        bot.send_message(message.chat.id, f"Selected region:{selected_region}")

        # 5. Filter games based on the selected region
        selected_games = selected_games[selected_games['Region'] == selected_region]

        if not selected_games.empty:
            # 6. Print their Activation type
            unique_activation_types = selected_games['Activation type'].unique()
            activation_message = "Available activation types for the selected region:\n"
            for i, activation_type in enumerate(unique_activation_types, start=1):
                activation_message += f"{i}. {activation_type}\n"
            activation_message += "Please enter the number corresponding to your choice:"
            bot.send_message(message.chat.id, activation_message)

            # Register next step handler for activation type selection
            bot.register_next_step_handler(message, process_activation_selection, selected_games)
        else:
            bot.send_message(message.chat.id, "There are no games available for the selected region.")
            process_first_option_input(message)
    else:
        bot.send_message(message.chat.id, "Invalid region choice. Please select again.")
        process_first_option_input(message)

def process_activation_selection(message, selected_games):
    user_activation_choice = int(message.text) - 1

    if 0 <= user_activation_choice < len(selected_games):
        selected_activation = selected_games.iloc[user_activation_choice]['Activation type']

        # 7. Write the selected activation type
        max_links = min(len(selected_games), 10)  # Limit to maximum 10 links
        for index, game in selected_games.head(max_links).iterrows():
            game_info = f"Link: {game['Link']} - Price: {game['Price']} €"
            bot.send_message(message.chat.id, game_info)

        # 8. Save unique games that match the selected platform, edition, region, and activation type
        # Do whatever you need with the selected games
    else:
        bot.send_message(message.chat.id, "Invalid activation type choice. Please select again.")
        process_first_option_input(message)




def process_second_option_input(message):
    image_path = 'C:\\Users\\Yehor\\Documents\\GitHub\\PythonBot\\Table1.png'
    results_all = sorting.main_all_games()
    bot.send_message(message.chat.id, 'Games without filters:')
    for result in results_all:
        bot.send_message(message.chat.id, result)




    links = graph.create_plot_and_save(image_path)

    start_index = 7  # Assuming link numbering starts from 1
    reversed_links = links[start_index - 1:][::-1]

    # Print all links with numbering

    for i, link in enumerate(reversed(links), 1):
        bot.send_message(message.chat.id,f"{i}. {link}")



    # Send the image
    bot.send_photo(chat_id=message.chat.id, photo=open(image_path, 'rb'))

def on_click(message):
    markup = types.ReplyKeyboardMarkup()

    btn1 = types.KeyboardButton('Sorted prices')
    btn2 = types.KeyboardButton('All prices')
    markup.row(btn1,btn2)


    markup2 = types.ReplyKeyboardMarkup()
    btn11 = types.KeyboardButton('Menu')
    markup2.row(btn11)
    Option = None
    if message.text == 'Menu':
        bot.send_message(message.chat.id, 'Please select option', reply_markup=markup)
        bot.register_next_step_handler(message, on_click)
    elif message.text == 'Sorted prices':
        Option = 'first'

        bot.send_message(message.chat.id, 'Please provide name of the game')

        bot.register_next_step_handler(message, receive_game,Option)

    elif message.text == 'All prices':
        Option = 'second'

        bot.send_message(message.chat.id, 'Please provide name of the game')

        bot.register_next_step_handler(message, receive_game, Option)

    elif message.text == 'Authors':
        bot.send_message(message.chat.id, 'Four random people', reply_markup=markup2)
        bot.register_next_step_handler(message, on_click)




if __name__ == '__main__':
    bot.polling(none_stop=True)
