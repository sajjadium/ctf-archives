FROM python:3.11-slim-bullseye

RUN apt update -y && apt install -y socat \
	&& adduser --disabled-password --home /app user \
	&& pip3 install pylfsr

COPY --chown=user . /app

RUN chmod 755 /app/entry.sh /app/chall.py

EXPOSE ${LISTEN_PORT}

ENTRYPOINT ["/app/entry.sh"]
