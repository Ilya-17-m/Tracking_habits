import os
import logging.config
from dotenv import load_dotenv

load_dotenv()

sentry_dsn = os.getenv("SENTRY_DSN")

user = os.getenv("DATABASE_USER")
password = os.getenv("DATABASE_PASSWORD")
database = os.getenv("DATABASE_NAME")


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