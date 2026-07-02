FROM python:3.12-slim

WORKDIR /app

RUN pip install --upgrade pip
RUN pip install poetry=2.2.1

COPY poetry.lock pyproject.toml ./

RUN poetry install --no-root

COPY . .

CMD ["python", "views.py"]
