import os
import requests
import logging
from sqlalchemy import select
from datetime import datetime

from celery_conf import celery_app
from models import HabitORM
from database_conf import SessionDep
from dotenv import load_dotenv


load_dotenv()

logger = logging.getLogger(__name__)
BOT_TOKEN = os.getenv("BOT_TOKEN")


@celery_app.task
def send_a_reminder_message_to_the_user(chat_id, text):
    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        json={
            "chat_id": chat_id,
            "text": f"Напоминание о вашей заметке: \n{text}"
        }
    )


@celery_app.task
async def check_status_habit(session: SessionDep):
    now = datetime.now()
    get_habits = await session.execute(
        select(HabitORM)
    )
    habits = get_habits.scalar().all()
    for habit in habits:
        if habit.status == False and habit.time == now:
            send_a_reminder_message_to_the_user.delay(
                habit.profile.chat_id, habit.title
            )

        elif habit.status == True:
            await session.delete(habit)
            await session.commit()
