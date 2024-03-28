import os
import imgkit
import re
import requests


def generate_png(group, cookies):
    try:
        response = requests.get(f"https://rozklad.ztu.edu.ua/schedule/group/{group}", cookies=cookies)

        print(os.getcwd())

        with open('scripts/generate_png/static/css/style.css', "r", encoding="utf-8") as css:
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
            temp = re.sub(r'<footer.*?>(.*?)</footer>', '', temp, flags=re.DOTALL)
            # print(temp)
            file.write(temp)
        file.close()

        imgkit.from_file('tmp/output.html', 'tmp/rozklad.jpg')
    except Exception as e:

        print("An error occurred:")
    return True
