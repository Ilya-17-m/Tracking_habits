FROM python:3.12

WORKDIR /app

RUN pip install --upgrade pip \
    poetry==2.2.1

COPY ../poetry.lock pyproject.toml ./

RUN poetry install

COPY . .

EXPOSE 8000

CMD ["poetry", "run", "gunicorn", "views:app"]