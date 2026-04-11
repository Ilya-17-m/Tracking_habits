FROM python:3.12

WORKDIR /app

RUN pip install --upgrade pip \
    poetry==2.2.1

COPY poetry.lock pyproject.toml ./

RUN poetry install

COPY /backend .

CMD ["poetry", "run", "gunicorn", "views:app"]