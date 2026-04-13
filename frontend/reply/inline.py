import requests
from telebot.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message
)
from frontend.views import bot, API_URL
from frontend.states import (
    change_title_habit,
    change_time_habit,
)
"""
    Работа с Inline клавиатурой
"""


def gen_inline_markup():
    button_1 = InlineKeyboardButton(text="Название")
    button_2 = InlineKeyboardButton(text="Время")
    button_3 = InlineKeyboardButton(text="Подтверждение выполнения привычки")

    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        button_1,
        button_2,
        button_3,
    )

    return keyboard


@bot.callbeck_query_handler(func=lambda callback_query: (callback_query.data == "Название"))
def inline_reply_change_title_habit(message: Message):
    bot.send_message(
        message.chat.id, "Укажите текущее название привычки, которую хотите изменить."
    )
    bot.register_next_step_handler(message, change_title_habit)


@bot.callback_query_handler(func=lambda callback_query: (callback_query.data == "Время"))
def inline_reply_change_time_habit(message: Message):
    bot.send_message(
        message.chat.id, "Укажите текущее название привычки, которую хотите изменить."
    )
    bot.register_next_step_handler(message, change_time_habit)


@bot.callback_query_handler(func=lambda callback_query: (
        callback_query.data == "Подтверждение статуса привычки"
))
def inline_reply_change_status_habit(message: Message):
    bot.send_message(
        message.chat.id, "Укажите текущее название привычки, которую хотите изменить."
    )
    bot.register_next_step_handler(message, )




    response = requests.put(
        f"{API_URL}/api/habit",
        json={
            "object": "status"
        }
    )
    data = response.json()
    if data["result"] == "true":
        bot.send_message(message.chat.id, data["message"])
    else:
        bot.send_message(message.chat.id, data["message"])