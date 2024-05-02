import os
import imgkit
import re
import requests
import datetime


def is_friday_night():
    now = datetime.datetime.now()
    return now.weekday() == 4 and now.hour >= 18  # Friday (weekday 4) and hour is 18 or later


def is_1_september():
    now = datetime.datetime.now()
    return now.month == 9 and now.day == 1


def generate_png(group, cookies):
    WEEK = 1
    if is_friday_night():
        print("Now is friday")
        if int(WEEK) == 1:
            WEEK += 1
        else:
            WEEK -= 1
        if is_1_september():
            print("Now is september")
            WEEK=1
    try:
        response = requests.get(f"https://rozklad.ztu.edu.ua/schedule/group/{group}", cookies=cookies)

        # print(os.getcwd())

        with open('scripts/generate_png/static/css/style.css', "r", encoding="utf-8") as css:
            css_text = css.read()

        css.close()
        # print(css_text)
        with open("tmp/output.html", "w", encoding="utf-8") as file:

            temp = re.sub(r"<style.*?>(.*?)</style>", f"<style>{css_text}</style>", response.text, flags=re.DOTALL)
            temp = re.sub(r'<div>[\w\d\s,-]+<\/div>', f"----------------", temp, flags=re.DOTALL)

            if WEEK == 1:
                temp = re.sub(r'<h2>ІІ тиждень</h2>(.*?)</table>', "", temp, flags=re.DOTALL)
            else:
                temp = re.sub(r'<h2>І тиждень</h2>(.*?)</table>', "", temp, flags=re.DOTALL)
            temp = re.sub(r'<footer.*?>(.*?)</footer>', '', temp, flags=re.DOTALL)
            # print(temp)
            file.write(temp)
        file.close()

        imgkit.from_file('tmp/output.html', 'tmp/rozklad.jpg')
    except Exception as e:

        print("An error occurred:")
    return True
