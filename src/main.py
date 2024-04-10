import os

import telebot

import requests
from pymongo import MongoClient

from dotenv import load_dotenv
from scripts.validators import validate_group
from scripts.generate_png.generate_png import generate_png

user_data = {}
load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')

mongo_uri = os.getenv('MONGO_URI')
client = MongoClient(mongo_uri)
db = client["rozklad-bot"]

login_url = 'https://rozklad.ztu.edu.ua/login'
login = os.getenv('LOGIN')
password = os.getenv('PASSWORD')

# Define the data to be sent in the POST request for login
data = {
    'login': login,
    'password': password
}

# Send a POST request to login
response = requests.post(login_url, data=data)

if response.status_code == 200:

    cookies = response.cookies

    php_session_id = cookies.get('PHPSESSID')

    if php_session_id:
        print("Login successful.")
        print(f"PHPSESSID: {php_session_id}")
        cookies = {
            "PHPSESSID": f"{php_session_id}"
        }
    else:
        print("PHPSESSID cookie not found.")
else:
    print("Login failed. Status code:", response.status_code)

bot = telebot.TeleBot(BOT_TOKEN)

collection = db['users']
user_data = collection.find({})
for user in user_data:
    bot.send_message(user['id'], 'Бот стартанув!')


@bot.message_handler(commands=['start', 'hello', 'info'])
def send_welcome(message):
    chat_id = message.chat.id
    bot.reply_to(message,
                 "Доброго дня! Даний бот досі перебуває у розробці. Для зручнішого використання рекомендую використовувати кнопку menu. Якщо знайшли якісь баги, писати @Exzente . Дякую!")

    bot.register_next_step_handler(message, ask_group)


def ask_group(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, 'Введіть вашу групу(Приклад: ІПЗ-21-2):')
    bot.register_next_step_handler(message, save_user_to_db)


def save_user_to_db(message):
    if validate_group(cookies, message.text) is not True:
        ask_group(message)
        return
    collection = db["users"]
    user = {"id": message.chat.id, "group": message.text}
    collection.insert_one(user)
    bot.register_next_step_handler(message, my_rozklad)


@bot.message_handler(commands=['my_rozklad'])
def my_rozklad(message):
    chat_id = message.chat.id
    collection = db["users"]
    user = collection.find_one({"id": chat_id})
    if user is None:
        bot.send_message(chat_id, 'Вас ще немає в базі даних бота!')
        ask_group(message)
        return
    else:
        group = user["group"]
        send_png(message, str(group))


@bot.message_handler(commands=['rozklad'])
def rozklad(message):
    chat_id = message.chat.id
    print(message.text)
    print('-------chat_id-------')
    print(chat_id)
    print('---------------------')
    print(message.chat.username)
    print('---------------------')
    bot.send_message(chat_id, 'Введіть групу (Приклад: ІПЗ-21-2):')

    bot.register_next_step_handler(message, send_png)


def send_png(message, group=None):
    chat_id = message.chat.id
    if group is None:
        group = message.text
    if validate_group(cookies, group) is not True:
        bot.send_message(chat_id, 'Не коректні дані!')
        return
    bot.send_message(chat_id, 'Ваш розклад рендериться!')
    if generate_png(group, cookies) is not True:
        bot.send_message(chat_id, 'Не коректні дані!')
        return
    generate_png(group, cookies)

    with open('tmp/rozklad.jpg', 'rb') as file:

        bot.send_photo(chat_id, file)
        file.close()
    #clean_tmp()


bot.infinity_polling()
