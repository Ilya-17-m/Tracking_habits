import pytest

from backend.models import ProfileORM, HabitORM


@pytest.mark.asyncio
async def test_user_login(client, session):
    user = ProfileORM(
        username="ilya",
        last_name="M",
        first_name="Ilya",
        chat_id=2132213,
        user_id=8437878539782983,
    )
    await session.add(user)
    await session.commit()
    response = await client.post(
        url="/api/login",
        json={
            "username": "ilya",
            "chat_id": 2132213,
            "user_id": 8437878539782983,
        }
    )
    data = response.json()
    assert response.status_code == 200
    assert data == {
        "message": f"Вы вошли в систему. Рады снова приветствовать вас ilya"
    }


@pytest.mark.asyncio
async def test_register_user(client, session):
    response = client.post(
        url="/api/user",
        json={
            "username": "ilya",
            "chat_id": 2132213,
            "user_id": 8437878539782983,
            "last_name": "M",
            "first_name": "Ilya"
        }
    )
    data = response.json()
    assert response.status_code == 201
    assert data == {
        "result": "true", "username": "ilya"
    }


@pytest.mark.asyncio
async def test_create_habit(client, session):
    user = ProfileORM(
        username="ilya",
        last_name="M",
        first_name="Ilya",
        chat_id=2132213,
        user_id=8437878539782983,
    )
    await session.add(user)
    await session.commit()

    response = client.post(
        url="/api/habit",
        json={
            "title": "drink water",
            "time": "10:00",
            "user_id": 8437878539782983
        }
    )
    data = response.json()
    assert response.status_code == 201
    assert data == {"result": "true", "message": "Запись успешно добавлена!"}


@pytest.mark.asyncio
async def test_delete_habit(client, session):
    habit = HabitORM(
        title="drink water",
        time="10:00"
    )
    await session.add(habit)
    await session.commit()

    response = client.delete(
        url="/api/habit",
        json={
            "title": "drink water"
        }
    )
    data = response.json()
    assert data == {"result": "true", "message": "Привычка успешно удалена."}


@pytest.mark.asyncio
async def test_change_title_habit(client, session):
    habit = HabitORM(
        title="drink water",
        time="10:00"
    )
    await session.add(habit)
    await session.commit()

    response = client.patch(
        url="/api/habit/title",
        json={
            "title": "drink water",
            "new_title": "выпить воды"
        }
    )
    data =  response.json()
    assert data == {"result": "true", "message": "Название привычки успешно изменено."}


@pytest.mark.asyncio
async def test_change_time_habit(client, session):
    habit = HabitORM(
        title="drink water",
        time="10:00"
    )
    await session.add(habit)
    await session.commit()

    response = client.patch(
        url="api/habit/time",
        json={
            "title": "drink water",
            "time": "9:30",
        }
    )
    data = response.json()
    assert data == {"result": "true", "message": "Время успешно изменено."}


@pytest.mark.asyncio
async def test_change_status_habit(client, session):
    habit = HabitORM(
        title="drink water",
        time="10:00"
    )
    await session.add(habit)
    await session.commit()

    response = client.patch(
        url="api/habit/time",
        json={
            "title": "drink water",
            "status": "Выполнено",
        }
    )
    data = response.json()
    assert data ==  {"result": "true", "message": "Вы выполнили задание. Продалжайте в том же духе!"}