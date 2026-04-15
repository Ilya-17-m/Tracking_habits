from pydantic import BaseModel


class ChangeTitleHabitSchema(BaseModel):
    title: str
    new_title: str


class ChangeTimeHabitSchema(BaseModel):
    title: str
    time: str


class ChangeStatusHabitSchema(BaseModel):
    title: str
    status: str


class CreateHabitSchema(BaseModel):
    title: str
    time: str
    user_id: int


class DeleteHabitSchema(BaseModel):
    title: str


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
from pydantic import BaseModel
from datetime import time


class HabitSchema(BaseModel):
    title: str
    status: bool
    time: time
    object: str
    user_id: int