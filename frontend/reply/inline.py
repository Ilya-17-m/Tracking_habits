from telebot.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    CallbackQuery
)
from config import bot
from states import (
    get_title_for_change_title_habit,
    get_title_for_change_time_habit,
    get_title_for_change_status_habit
)
"""
    Работа с Inline клавиатурой
"""


def gen_inline_markup():
    button_1 = InlineKeyboardButton(text="Название", callback_data="title")
    button_2 = InlineKeyboardButton(text="Время", callback_data="time")
    button_3 = InlineKeyboardButton(text="Подтверждение выполнения привычки", callback_data="status")

    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        button_1,
        button_2,
        button_3,
    )

    return keyboard


@bot.callback_query_handler(func=lambda callback_query: (callback_query.data == "title"))
def inline_reply_change_title_habit(call: CallbackQuery):
    bot.register_next_step_handler(call.message, get_title_for_change_title_habit)


@bot.callback_query_handler(func=lambda callback_query: (callback_query.data == "time"))
def inline_reply_change_time_habit(call: CallbackQuery):
    bot.register_next_step_handler(call.message, get_title_for_change_time_habit)


@bot.callback_query_handler(func=lambda callback_query: (callback_query.data == "status"))
def inline_reply_change_status_habit(call: CallbackQuery):
    bot.register_next_step_handler(call.message, get_title_for_change_status_habit)