FROM python:3.7.3-slim

RUN apt-get update
RUN apt-get install curl -y
ADD requirements.txt /requirements.txt

RUN pip install -r /requirements.txt

ADD . /app/
WORKDIR /app/

EXPOSE 1024
ENTRYPOINT gunicorn --bind 0.0.0.0:1024 server:app