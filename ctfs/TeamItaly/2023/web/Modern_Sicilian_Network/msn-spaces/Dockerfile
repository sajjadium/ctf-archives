# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

WORKDIR /app

RUN pip3 install pymysql Flask Flask-SQLAlchemy timeago

COPY . .

EXPOSE 6969

CMD [ "flask", "run", "--host", "0.0.0.0", "--port", "6969" ]