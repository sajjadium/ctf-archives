FROM python:3.8-slim

WORKDIR /app

COPY requirements.txt /requirements.txt
RUN pip3 install -r /requirements.txt

COPY app/ /app/

RUN mkdir /tmp/uploads

CMD gunicorn -w 4 -b 0.0.0.0:5000 --chdir / --timeout 10 "app:create_app()"