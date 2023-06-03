FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get -y install \
     python3 python3-pip supervisor

#COPYING FILES
COPY requirements.txt .

#USERS SETTINGS
RUN  pip3 install -r requirements.txt 

COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
COPY challenge/flask/ /srv/app/flask/
COPY flag.txt /flag.txt

WORKDIR /srv/app/flask
