FROM python:3.8-slim-buster

RUN mkdir /app

RUN pip3 install flask pillow pyjwt cryptography

RUN apt update && apt install -y steghide

WORKDIR /app/keys

RUN openssl genrsa -out private.pem 3072 && openssl rsa -in private.pem -pubout -out public.pem

COPY . /app

WORKDIR /app

EXPOSE 1337

CMD python3 app.py
