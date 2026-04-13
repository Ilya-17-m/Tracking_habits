import requests
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