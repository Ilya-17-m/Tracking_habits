from pydantic import BaseModel
from datetime import date, time


class HabitSchema(BaseModel):
    title: str
    status: bool
    date: date
    time: time
    object: str  # change habit


class ProfileSchema(BaseModel):
    username: str
    last_name: str
    first_name: str
    chat_id: int
    user_id: int