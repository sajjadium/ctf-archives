FROM python:3.10

WORKDIR /app

RUN pip install poetry

COPY ./src/app/pyproject.toml /app/pyproject.toml
COPY ./src/app/poetry.lock /app/poetry.lock
RUN poetry config virtualenvs.create false && poetry install

COPY ./src/app/static/ /app/static/
COPY ./src/app/templates/ /app/templates/
COPY ./src/app/uwsgi.ini /app/uwsgi.ini

COPY ./src/app/*.py /app/

RUN adduser app && chown -R app /app

ENTRYPOINT ["poetry", "run", "uwsgi", "--ini", "/app/uwsgi.ini"]