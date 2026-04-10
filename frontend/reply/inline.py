from telebot.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message
)
from frontend.tracking_habits_front import bot
from frontend.states import (
    change_title_habit,
    change_time_habit,
    change_date_habit
)


def gen_inline_markup():
    button_1 = InlineKeyboardButton(text="Название")
    button_2 = InlineKeyboardButton(text="Время")
    button_3 = InlineKeyboardButton(text="Дата")

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


@bot.callback_query_handler(func=lambda callback_query: (callback_query.data == "Дата"))
def inline_reply_change_date_habit(message: Message):
    bot.send_message(
        message.chat.id, "Укажите текущее название привычки, которую хотите изменить."
    )
    bot.register_next_step_handler(message, change_date_habit)