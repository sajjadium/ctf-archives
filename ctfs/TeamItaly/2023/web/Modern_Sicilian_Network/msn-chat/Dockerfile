# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

WORKDIR /app

RUN apt-get update
RUN apt-get -y install gcc
RUN rm -rf /var/lib/apt/lists/*
RUN pip3 install pymysql Flask Flask-SQLAlchemy Flask-SocketIO argon2-cffi eventlet gevent-websocket requests

COPY . .

EXPOSE 6900

CMD [ "flask", "run", "--host", "0.0.0.0", "--port", "6900" ]