import os
import requests


def validate_group(cookies, group):
    response = requests.get(f"https://rozklad.ztu.edu.ua/schedule/group/{group}", cookies=cookies)
    if 'Сторінку не зайдено' in response.text:
        return False
    return True


