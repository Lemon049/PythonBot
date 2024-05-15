import telebot
import time
import webbrowser
import requests
from bs4 import BeautifulSoup
from telebot import types
import os
import pandas as pd

with open(os.path.dirname(os.path.realpath(__file__)) + '/token.txt') as file:
    TOKEN = file.readline().strip()

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
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


def process_first_option_input(message):
    # User input for the second option
    user_input = message.text
    bot.send_message(message.chat.id, f'You entered: {user_input}')
    # Send the menu markup again
    start(message)


def process_second_option_input(message):
    # User input for the second option
    user_input = message.text
    bot.send_message(message.chat.id, f'You entered: {user_input}')
    # Send the menu markup again
    start(message)


def process_third_option_input(message):
    # User input for the third option
    user_input = message.text
    bot.send_message(message.chat.id, f'You entered: {user_input}')
    # Send the menu markup again
    start(message)

def sort_and_summarize_data(data):
    #create a DataFrame from the given data
    df = pd.DataFrame(data, columns=['Value'])

    sorted_df = df.sort_values(by='Value')
    lowest = sorted_df.iloc[0]['Value']
    biggest = sorted_df.iloc[-1]['Value']

    average = sorted_df['Value'].mean()

    return sorted_df, lowest, biggest, average

#example data
data = [23, 56, 12, 78, 45, 90, 34, 67, -1]

#sort data
sorted_df, lowest, biggest, average = sort_and_summarize_data(data)

print("Sorted Data:")
print(sorted_df)
print("Lowest Number:", lowest)
print("Biggest Number:", biggest)
print("Average Number:", average)



if __name__ == '__main__':
    bot.polling(none_stop=True)
