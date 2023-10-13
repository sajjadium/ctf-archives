FROM python:3.11-alpine

RUN pip install pipenv \
    && apk add socat

WORKDIR /app

ADD app.py /app/
ADD oracle.py /app/

CMD ["socat", "tcp-listen:5555,fork,reuseaddr", "system:pipenv run python3 app.py"]
