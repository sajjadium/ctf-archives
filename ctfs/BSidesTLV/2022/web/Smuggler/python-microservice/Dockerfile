FROM python:3.9-alpine

ARG USERNAME=app
WORKDIR /usr/src/app
COPY requirements.txt .

RUN set -eux; \
    \
    pip install -r requirements.txt; \
    \
    adduser --disabled-password --no-create-home --gecos ${USERNAME} ${USERNAME}

COPY server.py .
COPY flag.txt .

USER ${USERNAME}

EXPOSE 80
CMD [ "python", "server.py" ]
