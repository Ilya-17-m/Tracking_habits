from pydantic import BaseModel
from datetime import time


class HabitSchema(BaseModel):
    title: str
    status: bool
    time: time
    object: str
    user_id: int


class ProfileSchema(BaseModel):
    username: str
    last_name: str
    first_name: str
    chat_id: int
    user_id: int


class UserLoginSchema(BaseModel):
    username: str
    last_name: str
    first_name: str
    chat_id: int
    user_id: int
