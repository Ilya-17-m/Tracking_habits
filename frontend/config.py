import os
import logging.config
from dotenv import load_dotenv
from telebot import TeleBot, StateMemoryStorage

load_dotenv()


BOT_TOKEN = os.getenv("BOT_TOKEN")
API_URL = os.getenv("API_URL")

bot = TeleBot(BOT_TOKEN, state_storage=StateMemoryStorage())


logging.config.dictConfig({
    "version": 1,
    "disable_existing_loggers": False,

    "formatters": {
        "console": {
            "format": "%(asctime)s %(levelname)s: %(name)s %(module)s %(lineno)s %(message)s"
        },
    },

    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "console",
        },
    },

    "loggers": {
        "": {
            "level": "INFO",
            "handlers": [
                "console",
            ]
        }
    }
})import os
import logging.config
from dotenv import load_dotenv

load_dotenv()


BOT_TOKEN = os.getenv("BOT_TOKEN")
API_URL = os.getenv("API_URL")


logging.config.dictConfig({
    "version": 1,
    "disable_existing_loggers": False,

    "formatters": {
        "console": {
            "format": "%(asctime)s %(levelname)s: %(name)s %(module)s %(lineno)s %(message)s"
        },
    },

    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "console",
        },
    },

    "loggers": {
        "": {
            "level": "INFO",
            "handlers": [
                "console",
            ]
        }
    }
})
