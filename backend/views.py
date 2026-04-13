import uvicorn
import sentry_sdk
from fastapi import FastAPI, status, HTTPException
from sqlalchemy import select, insert
from prometheus_fastapi_instrumentator import Instrumentator

from .database_conf import lifespan, SessionDep
from .models import ProfileORM, HabitORM, profile_habit_association_table
from .schemas import HabitSchema, ProfileSchema
from .config import sentry_dsn


sentry_sdk.init(
    dsn=sentry_dsn,
    send_default_pii=True,
)

app = FastAPI(lifespan=lifespan)
Instrumentator().instrument(app).expose(app)


@app.post("/api/login")
async def login_user(session: SessionDep, schema: ProfileSchema) -> dict:
    ...


@app.post("/api/logout")
async def logout_user(session: SessionDep) -> dict:
    ...


@app.post("/api/user", status_code=status.HTTP_201_CREATED)
async def create_new_profile(session: SessionDep, schema: ProfileSchema) -> dict:
    get_profile = await session.execute(
        select(ProfileORM).where(
            ProfileORM.username==schema.username,
            ProfileORM.user_id==schema.user_id,
            ProfileORM.chat_id==schema.chat_id
        )
    )
    profile = get_profile.scalar_one_or_none()
    if profile is None:
        try:
            create_profile = ProfileORM(
                username=schema.username,
                last_name=schema.last_name,
                first_name=schema.first_name,
                chat_id=schema.chat_id,
                user_id=schema.user_id
            )

            session.add(create_profile)
            await session.commit()

            return {"result": "true"}

        except HTTPException:
            return {"result": "false", "message": "Что-то пошло не так..."}

    return {"username": profile.username}


@app.post("/api/habit", status_code=status.HTTP_201_CREATED)
async def create_habit(session: SessionDep, schema: HabitSchema) -> dict:
    try:
        habit = HabitORM(
            title=schema.title,
            time=schema.time,
        )

        insert_habit_profile_table_values = insert(profile_habit_association_table).values(
            profile_id=schema.user_id,
            habit_id=habit.id
        )

        session.add(habit)
        await session.commit()

        await session.execute(insert_habit_profile_table_values)
        await session.commit()

        return {"result": "true", "message": "Запись успешно добавлена!"}

    except HTTPException:
        return {"result": "false", "message": "Возникла ошибка создания!"}



@app.delete("/api/habit")
async def delete_my_habit(session: SessionDep, schema: HabitSchema) -> dict:
    try:
        get_habit = await session.execute(
            select(HabitORM).where(
                HabitORM.title==schema.title
            )
        )
        habit = get_habit.scalar_one_or_none()
        habit.archive = True
        await session.commit()

        return {"result": "true", "message": "Привычка успешно удалена."}

    except HTTPException:
        return {"result": "false", "message": "Не удалось удалить привычку."}
    

@app.put("/api/habit")
async def change_habit(session: SessionDep, schema: HabitSchema):
    get_habit = await session.execute(
        select(HabitORM).where(
            HabitORM.title==schema.title
        )
    )
    habit = get_habit.scalar_one_or_none()

    if schema.object == "title":
        habit.title = schema.title
        await session.commit()
        return {"result": "true", "message": "Название привычки успешно изменено."}

    elif schema.object == "time":
        habit.time = schema.time
        await session.commit()
        return {"result": "true", "message": "Время успешно изменено."}

    elif schema.object == "status":
        habit.status = True
        await session.commit()
        return {"result": "true", "message": "Вы выполнили задание. Продалжайте в том же духе!"}

    return {"result": "false", "message": "Что-то пошло не так."}


@app.get("/sentry-debug")
async def check_sentry():
    return 1 / 0


if __name__ == "__main__":
    uvicorn.run("backend.tracking_habits_logic:app")