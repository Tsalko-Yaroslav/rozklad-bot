# rozklad-bot project
## English
## deployment guide

There is also Dockerfile, no exposing ports or serviers needed.

1. create .env file in src directory with the following content:
```
BOT_TOKEN=<telegram-bot-token>
LOGIN=<university login (example: ipz212_tsyav)>
PASSWORD=<password provided by A. Morozov>
```
2. For imgkit module we need to install <b>wkhtmltoimage</b> executable and add to $PATH.
3. run `pip install -r requirements.txt` in src directory
4. Run the project: `python bot.py`

## Українська
## Як розгорнути проєкт?

В репозиторії присутній Dockerfile, не потрібно відкривати порти або сервери.

1. Створіть .env file в src директорії і додайте дані до нього:
```
BOT_TOKEN=<токен-наданий-телеграмом>
LOGIN=<університетський логін (приклад: ipz212_tsyav)>
PASSWORD=<пароль від нашого улюбленого А. Морозова>
```
2. Для imgkit модуля нам потрібно встановити <b>wkhtmltoimage</b> та додати до змінної $PATH.
3. Запустіть `pip install -r requirements.txt` в src директорії
4. Запустіть проєкт: `python bot.py`
