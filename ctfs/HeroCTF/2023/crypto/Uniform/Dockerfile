FROM python:3.11-alpine

RUN apk --update add socat \
	&& adduser -D --home /app user

COPY --chown=user . /app

RUN chmod 755 /app/entry.sh /app/chall.py

EXPOSE ${LISTEN_PORT}

ENTRYPOINT ["/app/entry.sh"]