import requests
from telebot.types import Message

from tracking_habits_front import API_URL, bot


def add_title_habit(message: Message):
    title = message.text

    bot.send_message(message.chat.id, "Отлично. Теперь введите время для напоминаний.")
    bot.register_next_step_handler(message, add_time_habit, title)


def add_time_habit(message: Message, title: str):
    time = message.text

    bot.send_message(message.chat.id, "Добавьте дату для напоминаний.")
    bot.register_next_step_handler(message, create_habit, title, time)


def create_habit(message: Message, title: str, time: str):
    date = message.text

    response = requests.post(
        f"{API_URL}/api/habit",
        json={
            "title": title,
            "time": time,
            "date": date
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



def change_title_habit(message: Message):
    title = message.text
    response = requests.put(
        f"{API_URL}/api/habit",
        json={
            "title": title,
            "object": "title"
        }
    )

    data = response.json()
    if data["result"] == "false":
        bot.send_message(message.chat.id, data["message"])

    else:
        bot.send_message(message.chat.id, data["message"])


def change_date_habit(message: Message):
    date = message.text
    response = requests.put(
        f"{API_URL}/api/habit",
        json={
            "title": date,
            "object": "date"
        }
    )

    data = response.json()
    if data["result"] == "false":
        bot.send_message(message.chat.id, data["message"])

    else:
        bot.send_message(message.chat.id, data["message"])


def change_time_habit(message: Message):
    time = message.text
    response = requests.put(
        f"{API_URL}/api/habit",
        json={
            "title": time,
            "object": "time"
        }
    )

    data = response.json()
    if data["result"] == "false":
        bot.send_message(message.chat.id, data["message"])

    else:
        bot.send_message(message.chat.id, data["message"])