FROM python:3-alpine

RUN mkdir /app
WORKDIR /app

RUN addgroup -S appgroup && adduser -S appuser -G appgroup
RUN apk update && apk add python3-dev gcc g++ libc-dev supervisor 

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

EXPOSE 1337

COPY requirements.txt .
COPY flag /
COPY config/supervisord.conf /etc/supervisord.conf

COPY challenge .
RUN pip install --no-cache-dir -r requirements.txt 

ENTRYPOINT [ "/usr/bin/supervisord", "-c", "/etc/supervisord.conf" ]