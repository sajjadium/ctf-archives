FROM python:3.11-alpine

RUN apk add --update gcc musl-dev py3-gunicorn

COPY ./requirements.txt .

RUN adduser -S bocchi
USER bocchi

RUN pip install -r requirements.txt

USER root
COPY flag.txt readflag.c /

RUN gcc readflag.c -o readflag
RUN chmod 4755 readflag && \
	chmod 600 flag.txt


WORKDIR /src
COPY src .

USER bocchi

CMD gunicorn -b 0.0.0.0:10024 -w20 main:app
