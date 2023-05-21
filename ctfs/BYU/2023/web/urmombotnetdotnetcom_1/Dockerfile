FROM python:3.11.3-bullseye
RUN apt-get update && apt-get upgrade -y && apt-get install -y default-libmysqlclient-dev && rm -rf /var/lib/apt/lists/*

RUN mkdir /app
WORKDIR /app
RUN useradd -M -d /app ctf

COPY app /app

RUN chown -R root:ctf /app 
RUN chmod -R 750 /app

RUN pip3 install flask PyJWT Flask-MySQLdb

USER ctf

CMD ["python3", "/app/server.py"]