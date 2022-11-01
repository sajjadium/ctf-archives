FROM python:3-alpine

RUN apk update \
    # Install Docker CLI
    && apk add docker-cli \
    # Install python dependencies
    && pip install flask gunicorn requests PyMySQL

ADD ./src/ /app/
WORKDIR /app/

VOLUME [ "/var/run/docker.sock" ]
VOLUME [ "/app/config.json" ]

ENV PORT=80 BIND_ADDR=0.0.0.0
EXPOSE 80


#ENTRYPOINT python app.py config.json
ENTRYPOINT gunicorn -b "${BIND_ADDR}:${PORT}" --access-logfile - --error-logfile - app:app
