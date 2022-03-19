FROM python:3.10-slim-buster

ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update

WORKDIR /app
ADD requirements.txt ./
RUN pip install -r requirements.txt

ADD secret.py  ./
ADD crawler.py ./

ENTRYPOINT python3 crawler.py
