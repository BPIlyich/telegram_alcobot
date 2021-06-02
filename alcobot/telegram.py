import telebot
from dotenv import dotenv_values

from inshaker import get_random_recipe_url


API_TOKEN = dotenv_values(".env")["API_TOKEN"]


bot = telebot.TeleBot(API_TOKEN)


# Handle '/start' and '/help'
@bot.message_handler(commands=["help", "start"])
def send_welcome(message):
    bot.reply_to(
        message,
        """
        Привет! Я АлкоБот.
        На текущий момент умею выдавать случайный коктейль, состоящий из указанных через запятую ингредиентов, из базы сайта https://ru.inshaker.com.
        Если не нравится ингредиент, поставь перед ним "-", и коктейли, содержащие этот ингредиент будут проигнорированы в выдаче.

        Пример валидного ввода:
        ```
        Красный биттер, Красный вермут, -Лондонский сухой джин
        ```

        С полным списком доступных ингредиентов можно ознакомиться на странице https://ru.inshaker.com/goods
        """,
    )


# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    text = get_random_recipe_url(message.text)
    bot.reply_to(message, text)
