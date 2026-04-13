import requests
from telebot.types import Message

from views import API_URL, bot


def add_title_habit(message: Message):
    title = message.text

    bot.send_message(message.chat.id, "Отлично. Теперь введите время для напоминаний.")
    bot.register_next_step_handler(message, add_time_habit, title)


def add_time_habit(message: Message, title: str):
    time = message.text
    bot.register_next_step_handler(message, create_habit, title, time)


def create_habit(message: Message, title: str, time: str):

    response = requests.post(
        f"{API_URL}/api/habit",
        json={
            "title": title,
            "time": time,
            "user_id": message.from_user.id
        }
    )

    data = response.json()

    if data["result"] == "true":
        bot.send_message(message.chat.id, data["message"])

    else:
        bot.send_message(message.chat.id, "К сожалению что-то пошло не так...")


def delete_habit(message: Message):
    title = message.text
    response = requests.post(
        f"{API_URL}/api/delete",
        json={
            "title": title
        }
    )

    data = response.json()
    if data["result"] == "true":
        bot.send_message(message.chat.id, data["message"])

    else:
        bot.send_message(message.chat.id, data["message"])


def get_title_for_change_title_habit(message: Message):
    title = message.text
    bot.send_message(message.chat.id, "Укажите новое название для вашей привычки")
    bot.register_next_step_handler(message, change_title_habit, title)


def change_title_habit(message: Message, title: str):
    new_title = message.text
    response = requests.put(
        f"{API_URL}/api/habit",
        json={
            "title": new_title,
            "object": "title"
        }
    )

    data = response.json()
    if data["result"] == "false":
        bot.send_message(message.chat.id, data["message"])

    else:
        bot.send_message(message.chat.id, data["message"])


def get_title_for_change_time_habit(message: Message):
    title = message.text
    bot.send_message(message.chat.id, "Укажите время для напоминания, в формате 00:00")
    bot.register_next_step_handler(message, create_habit, title)


def change_time_habit(message: Message, title):
    time = message.text

    response = requests.put(
        f"{API_URL}/api/habit",
        json={
            "title": title,
            "object": "time",
            "time": time
        }
    )

    data = response.json()
    if data["result"] == "false":
        bot.send_message(message.chat.id, data["message"])

    else:
        bot.send_message(message.chat.id, data["message"])


def get_title_for_change_status_habit(message: Message):
    title = message.text