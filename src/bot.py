import os

import telebot

import re
import requests

import imgkit
from dotenv import load_dotenv
user_data = {}
load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')


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




@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, "Доброго дня! Даний бот досі перебуває в розробці. Для зручнішого використання рекомендую використовувати кнопку menu. Якщо знайшли якісь баги, писати @Exzente . Дякую!")



@bot.message_handler(commands=['rozklad'])
def rozklad(message):
    chat_id = message.chat.id
    print(message.text)
    print(chat_id)
    bot.send_message(chat_id, 'Введіть групу (Приклад: ІПЗ-21-2):')
    bot.register_next_step_handler(message, generate_pdf)


def generate_pdf(message):
    chat_id = message.chat.id
    try:
        response = requests.get(f"https://rozklad.ztu.edu.ua/schedule/group/{message.text}", cookies=cookies)
        if 'Сторінку не зайдено' in response.text:
            bot.send_message(chat_id, 'Невірно введено групу!')
            return
        with open('style.css', "r", encoding="utf-8") as css:
            css_text = css.read()

        css.close()
        # print(css_text)
        with open("tmp/output.html", "w", encoding="utf-8") as file:

            temp = re.sub(r"<style.*?>(.*?)</style>", f"<style>{css_text}</style>", response.text, flags=re.DOTALL)
            temp = re.sub(r'<div>[\w\d\s,-]+<\/div>', f"----------------", temp, flags=re.DOTALL)

            match = re.search(r'<h2>І тиждень</h2>(?<=\bсьогодні\b)(?![^<>]*>)</table>', temp)
            if match:
                temp = re.sub(r'<h2>ІІ тиждень</h2>(.*?)</table>', "", temp, flags=re.DOTALL)
            else:
                temp = re.sub(r'<h2>І тиждень</h2>(.*?)</table>', "", temp, flags=re.DOTALL)

            # print(temp)
            file.write(temp)
        file.close()

        imgkit.from_file('tmp/output.html', 'tmp/rozklad.jpg')
    except Exception as e:

        print("An error occurred:", e)
    with open('tmp/rozklad.jpg', 'rb') as file:

        bot.send_photo(chat_id, file)
        file.close()
        os.remove('tmp/rozklad.jpg')
        os.remove('tmp/output.html')


bot.infinity_polling()