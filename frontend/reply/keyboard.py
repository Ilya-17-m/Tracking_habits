from telebot.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    Message
)
from frontend.views import bot
from frontend.states import add_title_habit, delete_habit
from frontend.reply.inline import gen_inline_markup

"""
    Работа с Keyboard клавиатурой
"""

def gen_keyboard_markup():
    button_1 = KeyboardButton(text="Создать")
    button_2 = KeyboardButton(text="Удалить")
    button_3 = KeyboardButton(text="Изменить")

    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(
        button_1,
        button_2,
        button_3,
    )

    return keyboard


@bot.message_handler(fun=lambda message: message.text == "Создать")
def keyboard_reply_create_habit(message: Message):
    bot.send_message(message.chat.id, "Укажите название вашей заметки, для её удаления.")
    bot.register_next_step_handler(message, add_title_habit)


@bot.message_handler(func=lambda message: message.text == "Удалить")
def keyboard_reply_delete_habit(message: Message):
    bot.send_message(message.chat.id, "Укажите название вашей заметки, для её удаления.")
    bot.register_next_step_handler(message, delete_habit)


@bot.message_handler(func=lambda message: message.text == "Изменить")
def keyboard_reply_change_habit(message: Message):
    bot.send_message(
        message.chat.id,
        "Укажите название вашей заметки, для её удаления.",
        reply_markup=gen_inline_markup()
    )
