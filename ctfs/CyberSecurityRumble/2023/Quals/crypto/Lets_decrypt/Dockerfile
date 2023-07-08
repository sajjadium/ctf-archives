FROM python:3.11-slim-buster

RUN apt update && apt upgrade -y

RUN pip install pipenv
RUN pip install gunicorn[gevent]=="20.1.0"

WORKDIR /app

COPY Pipfile .
COPY Pipfile.lock .
RUN pipenv install --deploy --system

COPY . .

CMD python init_app.py && gunicorn -c gunicorn.conf.py