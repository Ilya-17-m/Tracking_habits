import os
import logging.config
from dotenv import load_dotenv
from authx import AuthX, AuthXConfig

load_dotenv()

sentry_dsn = os.getenv("SENTRY_DSN")

user = os.getenv("DATABASE_USER")
password = os.getenv("DATABASE_PASSWORD")
database = os.getenv("DATABASE_NAME")
SECRET_KEY = os.getenv("SECRET_KEY")
ACCESS_COOKIE_NAME = os.getenv("ACCESS_COOKIE_NAME")


config = AuthXConfig()
config.JWT_SECRET_KEY = SECRET_KEY
config.JWT_ACCESS_COOKIE_NAME = ACCESS_COOKIE_NAME
config.JWT_TOKEN_LOCATION = ["cookies"]

security = AuthX(config=config)


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