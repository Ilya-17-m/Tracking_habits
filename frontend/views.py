import requests
from telebot.types import Message

from config import API_URL, bot


def add_title_habit(message: Message):
    title = message.text

    bot.send_message(
        message.chat.id,
        "Отлично. Теперь введите время для напоминаний в формате 00:00"
    )
    bot.register_next_step_handler(message, add_time_habit, title)


def add_time_habit(message: Message, title: str):
    time = message.text

    response = requests.post(
        f"{API_URL}/api/habit",
        json={
            "title": title,
            "time": time,
            "user_id": message.from_user.id
        }
    )

    data = response.json()
    bot.send_message(message.chat.id, data["message"])


def delete_habit(message: Message):
    title = message.text
    response = requests.delete(
        f"{API_URL}/api/habit",
        json={
            "title": title
        }
    )

    data = response.json()
    bot.send_message(message.chat.id, data["message"])


def get_title_for_change_title_habit(message: Message):
    bot.send_message(message.chat.id, "Укажите название вашей привычки, которую хотите обновить.")
    bot.register_next_step_handler(message, get_new_title_for_change_title_habit)


def get_new_title_for_change_title_habit(message: Message):
    title = message.text
    bot.send_message(message.chat.id, "Укажите новое название для вашей привычки")
    bot.register_next_step_handler(message, change_title_habit, title)


def change_title_habit(message: Message, title: str):
    new_title = message.text
    response = requests.put(
        f"{API_URL}/api/habit",
        json={
            "title": title,
            "new_title": new_title,
        }
    )

    data = response.json()
    bot.send_message(message.chat.id, data["message"])


def get_title_for_change_time_habit(message: Message):
    bot.send_message(message.chat.id, "Укажите название вашей привычки, которую хотите обновить.")
    bot.register_next_step_handler(message, get_time_for_change_time_habit)


def get_time_for_change_time_habit(message: Message):
    title = message.text
    bot.send_message(message.chat.id, "Укажите время для напоминания, в формате 00:00")
    bot.register_next_step_handler(message, change_time_habit, title)


def change_time_habit(message: Message, title):
    time = message.text

    response = requests.put(
        f"{API_URL}/api/habit",
        json={
            "title": title,
            "time": time,
        }
    )

    data = response.json()
    bot.send_message(message.chat.id, data["message"])


def get_title_for_change_status_habit(message: Message):
    bot.send_message(message.chat.id, "Укажите название вашей привычки, которую хотите обновить.")
    bot.register_next_step_handler(message, get_status_for_change_status_habit)


def get_status_for_change_status_habit(message: Message):
    title = message.text
    bot.send_message(
        message.chat.id,
        "Если вы выполнили задание напишите: Выполнено. "
        "Если вы не выполнили напишите: Не выполнено"
    )
    bot.register_next_step_handler(message, change_status_habit, title)


def change_status_habit(message: Message, title):
    status = message.text
    response = requests.post(
        f"{API_URL}/api/habit",
        json={
            "title": title,
            "status": status,
        }
    )
    data = response.json()
    bot.send_message(message.chat.id, data["message"])