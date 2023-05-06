FROM python:3.9-slim

RUN pip3 install flask mysql-connector-python gunicorn

WORKDIR /app

COPY ponydb.py ./
COPY templates templates/

ENV SECRET_KEY=REDACTED
ENV DB_HOST=127.0.0.1
ENV DB_USER=iheartponies
ENV DB_PASS=REDACTED
ENV DB=ponies
ENV FLAG=uiuctf{REDACTED}

EXPOSE 1337

CMD mount -t tmpfs none /tmp && gunicorn -b 0.0.0.0:1337 ponydb:app
