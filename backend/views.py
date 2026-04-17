import uvicorn
import sentry_sdk
from fastapi import FastAPI, status, HTTPException, Response
from sqlalchemy import select, insert
from prometheus_fastapi_instrumentator import Instrumentator

from .database_conf import lifespan, SessionDep
from .models import ProfileORM, HabitORM, profile_habit_association_table
from .schemas import (
    ChangeTitleHabitSchema,
    ChangeTimeHabitSchema,
    ChangeStatusHabitSchema,
    ProfileSchema,
    UserLoginSchema,
    CreateHabitSchema,
    DeleteHabitSchema,
)
from .config import sentry_dsn, security, config


sentry_sdk.init(
    dsn=sentry_dsn,
    send_default_pii=True,
)

app = FastAPI(lifespan=lifespan)
Instrumentator().instrument(app).expose(app)


@app.post("/api/login")
async def login_user(session: SessionDep, schema: UserLoginSchema, response: Response) -> dict:
    get_profile = await session.execute(
        select(ProfileORM).where(
            ProfileORM.username==schema.username,
            ProfileORM.user_id==schema.user_id,
            ProfileORM.chat_id==schema.chat_id
        )
    )
    profile = get_profile.scalar_one_or_none()
    if profile is not None:
        token = security.create_access_token(
            username=schema.username,
            chat_id=schema.chat_id,
            user_id=schema.user_id
        )
        response.set_cookie(config.JWT_ACCESS_COOKIE_NAME, token)
        return {
            "message": f"Вы вошли в систему. Рады снова приветствовать вас {schema.username}"
        }

    return {
        "result": "false",
        "message": "Вы не смогли войти в систему. Профиль с вашими данными не был найден!"
    }


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

            return {"result": "true", "username": create_profile.first_name}

        except HTTPException:
            return {"result": "false", "message": "Что-то пошло не так..."}

    return {"username": profile.first_name}


@app.post("/api/habit", status_code=status.HTTP_201_CREATED)
async def create_habit(session: SessionDep, schema: CreateHabitSchema) -> dict:
    get_profile = await session.execute(
        select(ProfileORM.id).where(ProfileORM.user_id==schema.user_id)
    )
    my_id = get_profile.scalar_one_or_none()

    if my_id is not None:
        habit = HabitORM(
            title=schema.title,
            time=schema.time,
            status=False,
            archive=False
        )

        insert_habit_profile_table_values = insert(profile_habit_association_table).values(
            profile_id=my_id,
            habit_id=habit.id
        )

        session.add(habit)
        await session.commit()

        await session.execute(insert_habit_profile_table_values)
        await session.commit()

        return {"result": "true", "message": "Запись успешно добавлена!"}

    return {"result": "false", "message": "Что-то пошло не так..."}


@app.delete("/api/habit")
async def delete_my_habit(session: SessionDep, schema: DeleteHabitSchema) -> dict:
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


@app.patch("/api/habit/title")
async def change_title_habit(
        session: SessionDep,
        schema: ChangeTitleHabitSchema
) -> dict[str, str]:

    get_habit = await session.execute(
        select(HabitORM).where(
            HabitORM.title==schema.title
        )
    )
    habit = get_habit.scalar_one_or_none()
    if habit is not None:
        habit.title = schema.new_title
        await session.commit()
        return {"result": "true", "message": "Название привычки успешно изменено."}

    return {"result": "false", "message": "Что-то пошло не так."}


@app.patch("api/habit/time")
async def change_time_habit(
        session: SessionDep,
        schema: ChangeTimeHabitSchema
) -> dict[str, str]:

    get_habit = await session.execute(
        select(HabitORM).where(
            HabitORM.title==schema.title
        )
    )
    habit = get_habit.scalar_one_or_none()

    if habit is not None:

        habit.time = schema.time
        await session.commit()
        return {"result": "true", "message": "Время успешно изменено."}

    return {"result": "false", "message": "Что-то пошло не так."}


@app.patch("/api/habit/status")
async def change_status_habit(
        session: SessionDep,
        schema: ChangeStatusHabitSchema
) -> dict[str, str]:

    get_habit = await session.execute(
        select(HabitORM).where(
            HabitORM.title==schema.title,
            HabitORM.archive==False
        )
    )
    habit = get_habit.scalar_one_or_none()

    if habit is not None:
        if schema.status == "Выполнено":
            habit.status = True
            await session.commit()
            return {"result": "true", "message": "Вы выполнили задание. Продалжайте в том же духе!"}

        habit.status = False
        await session.commit()
        return {"result": "true", "message": "Вы не выполнили задание"}

    return {"result": "false", "message": "Что-то пошло не так."}


@app.get("/sentry-debug")
async def check_sentry():
    return 1 / 0


if __name__ == "__main__":
    uvicorn.run("backend.tracking_habits_logic:app")
