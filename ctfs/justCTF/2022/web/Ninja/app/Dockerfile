FROM ubuntu:20.04

RUN apt-get update -y && \
    apt-get install -y python3-pip python3

COPY . /app

WORKDIR /app

RUN pip3 install -r requirements.txt

EXPOSE 5000
ENTRYPOINT sh -c "flask db init --directory /tmp/migrations && flask db migrate --directory /tmp/migrations && flask db upgrade --directory /tmp/migrations && FLASK_APP=app.py flask run --host 0.0.0.0"
