FROM python:3.11-buster

RUN pip install poetry

WORKDIR /app

COPY poetry.lock pyproject.toml /app/

RUN poetry install

ENTRYPOINT ["poetry", "run", "flask", "--app", "absurdres", "run", "--port", "55416", "--host", "0.0.0.0"]