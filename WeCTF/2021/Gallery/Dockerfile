FROM python:3.8.2-alpine3.11
RUN apk add --no-cache sqlite-dev

WORKDIR /home/src
RUN apk update && apk add gcc libc-dev make git libffi-dev openssl-dev python3-dev libxml2-dev libxslt-dev
RUN pip install flask gunicorn google-cloud-storage peewee
COPY . .

CMD ["gunicorn", "main:app", "--workers", "20", "--timeout", "2", "-b", "0.0.0.0:1000"]