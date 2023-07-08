FROM python:3.10.9

RUN DEBIAN_FRONTEND=noninteractive apt update && DEBIAN_FRONTEND=noninteractive apt upgrade -y 

RUN mkdir /app
WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY app.py app.py


ENTRYPOINT [ "/usr/local/bin/gunicorn", "-b", "0.0.0.0:9696", "app:app" ]