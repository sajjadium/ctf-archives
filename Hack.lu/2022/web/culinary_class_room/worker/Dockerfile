FROM python:3.10-slim as common

ENV POETRY_VIRTUALENVS_IN_PROJECT=true
ENV POETRY_NO_INTERACTION=1

WORKDIR /usr/src/app

RUN apt update && apt upgrade -y

FROM common as builder

RUN apt install -y gcc
COPY readFlag.c ./
RUN gcc readFlag.c -o readFlag

FROM common
RUN pip install --upgrade pip poetry

COPY poetry.lock pyproject.toml ./
COPY --from=builder /usr/src/app/readFlag ./readFlag
RUN chown root:root readFlag
RUN chmod +s readFlag

RUN poetry install --no-dev

COPY app.py ./
ARG FLAG=lehack_{FLAG_PLACEHOLDER}
RUN echo ${FLAG} > flag.txt
RUN chmod 400 flag.txt
USER nobody
EXPOSE 5000
CMD poetry run gunicorn -w 4 -b 0.0.0.0:5000 app:app