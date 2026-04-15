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
            "object": "title",
            "status": False,
            "time": "",
        }
    )

    data = response.json()
    bot.send_message(message.chat.id, data["message"])


def get_title_for_change_time_habit(message: Message):
    bot.send_message(message.chat.id, "Укажите название вашей привычки, которую хотите обновить.")
    bot.register_next_step_handler(message, get_time_for_change_time_habit(), title)


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
            "object": "time",
            "time": time,
            "new_title": "",
            "status": False
        }
    )

    data = response.json()
    bot.send_message(message.chat.id, data["message"])


def get_title_for_change_status_habit(message: Message):
    bot.send_message(message.chat.id, "Укажите название вашей привычки, которую хотите обновить.")
    bot.register_next_step_handler(message, get_status_for_chaange_status_habit)


def get_status_for_chaange_status_habit(message: Message):
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
            "object": "status",
            "new_title": "",
            "time": "",
        }
    )
    data = response.json()
    bot.send_message(message.chat.id, data["message"])import requests
import logging
from telebot import TeleBot, StateMemoryStorage
from telebot.types import Message

from .config import BOT_TOKEN, API_URL
from reply.keyboard import gen_keyboard_markup
from reply.inline import gen_inline_markup
from .states import add_title_habit, delete_habit


bot = TeleBot(BOT_TOKEN, state_storage=StateMemoryStorage())
logger = logging.getLogger(__name__)


@bot.message_handler(commands=["start"])
def handle_start(message: Message):
    get_user_profile = requests.post(
        f"{API_URL}/api/users",
        json={
            "user_id": message.from_user.id,
            "username": message.from_user.username,
            "last_name": message.from_user.last_name,
            "first_name": message.from_user.first_name,
            "chat_id": message.chat.id
            }
        )
    data = get_user_profile.json()

    bot.send_message(
        message.chat.id,
        f"Рады вас снова приветствовать, {data["username"]}"
        if "username" in data else "Добро пожаловать в менеджер задач!",
        reply_markup=gen_keyboard_markup(),
    )


@bot.message_handler(commands=["create_habit"])
def create_command_habit(message: Message):
    bot.send_message(message.chat.id, "Укажите название вашей заметки, для её создания.")
    bot.register_next_step_handler(message, add_title_habit)


@bot.message_handler(commands=["delete_habit"])
def delete_command_habit(message: Message):
    bot.send_message(message.chat.id, "Укажите название вашей заметки, для её удаления.")
    bot.register_next_step_handler(message, delete_habit)


@bot.message_handler(commands=["change_habit"])
def change_command_habit(message: Message):
    bot.send_message(
        message.chat.id,
        "Укажите что бы вы хотели изменить.",
        reply_markup=gen_inline_markup()
    )


@bot.message_handler(commands=["login"])
def login_user(message: Message):
    response = requests.post(
        f"{API_URL}/api/login",
        json={
            "username": message.from_user.username,
            "chat_id": message.chat.id,
            "user_id": message.from_user.id
        }
    )

    data = response.json()
    bot.send_message(message.chat.id, data["message"])


if __name__ == "__main__":
    bot.infinity_polling()
