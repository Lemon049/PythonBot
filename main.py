import telebot
import webbrowser
import requests
from bs4 import BeautifulSoup
from telebot import types

bot = telebot.TeleBot('6572783840:AAGxAGKoDaxKE6-7fiqcxQPGfJvJ8JDIu3Q')
oldURL = "https://quotes.toscrape.com"
mytext = "https://quotes.toscrape.com,span,text"
URL = 0
oldTag = "span"
Tag = 0
oldClassName = "text"
ClassName = 0
page_to_scrape = requests.get(oldURL)
soup = BeautifulSoup(page_to_scrape.text, "html.parser")
quotes = soup.findAll(oldTag, attrs = {"class" : oldClassName})
authors = soup.findAll("small", attrs = {"class" : "author"})


for quote, author in zip(quotes, authors):
    print(quote.text + " - " + author.text)



@bot.message_handler(commands=['start'])
def start(message):
    StartMarkup = types.ReplyKeyboardMarkup()

    btn1 = types.KeyboardButton('Menu')
    btn2 = types.KeyboardButton('Authors')
    StartMarkup.row(btn1)
    StartMarkup.row(btn2)
    bot.send_message(message.chat.id, 'Please select option', reply_markup=StartMarkup)
    bot.register_next_step_handler(message, on_click)
    var1 = "g"

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

URL = 0
def process_first_option_input(message):

 inputString = message.text
 values = inputString.split(',')
 URL = values[0] if len(values) > 0 else None
 Tag = values[1] if len(values) > 1 else None
 ClassName = values[2] if len(values) > 2 else None
 bot.send_message(message.chat.id, f'You entered: {URL}')
 bot.send_message(message.chat.id, f'You entered: {Tag}')
 bot.send_message(message.chat.id, f'You entered: {ClassName}')
 parsing_function(message, URL, Tag, ClassName)


def parsing_function(message,URL,Tag,ClassName):

      page_to_scrape = requests.get(URL)
      soup = BeautifulSoup(page_to_scrape.text, "html.parser")
      quotes = soup.findAll(Tag, attrs={"class": ClassName})
      authors = soup.findAll("small", attrs={"class": "author"})

      for quote, author in zip(quotes, authors):
          bot.send_message(message.chat.id, quote.text + " - " + author.text)
      parsing_function(message, URL, Tag, ClassName)



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


if __name__ == '__main__':
    bot.polling()
