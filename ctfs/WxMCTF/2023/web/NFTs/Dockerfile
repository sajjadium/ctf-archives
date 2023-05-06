FROM docker.io/python:3.11-alpine

ENV FLAG=flag{}
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

COPY ./requirements.txt /app/

RUN pip install --trusted-host pypi.python.org -r requirements.txt

COPY . /app

EXPOSE 5000

ENTRYPOINT ["/bin/sh", "launch.sh"]