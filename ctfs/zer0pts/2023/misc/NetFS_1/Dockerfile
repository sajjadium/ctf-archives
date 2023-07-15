FROM python:3.11-slim

RUN apt-get -y update --fix-missing
RUN apt-get -y upgrade
RUN apt-get -y install python3
RUN groupadd -r ctf && useradd -r -g ctf ctf
RUN chmod 1733 /tmp /var/tmp /dev/shm

WORKDIR /home/ctf
ADD secret secret
ADD public public
ADD server.py .
RUN chmod 440 secret/* public/*
RUN chmod 550 server.py

RUN chown -R root:ctf /home/ctf

USER ctf
CMD ./server.py
