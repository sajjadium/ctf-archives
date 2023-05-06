FROM python:3-alpine

RUN apk update
RUN apk add py-pip
RUN pip install flask gunicorn requests logzero
ENV LIBRARY_PATH=/lib:/usr/lib

ADD . /app/
WORKDIR /app/

ENV PORT=5000 BIND_ADDR=0.0.0.0

RUN python init.py
ENTRYPOINT gunicorn -w 8 -b "${BIND_ADDR}:${PORT}" --access-logfile - --error-logfile - app:app