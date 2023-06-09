# docker build -t type_this . && docker run -p 1337:1337 type_this
FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get -y upgrade
RUN apt-get install -yq socat wget python3-pip libgtk2.0-0 libnss3 libatk-bridge2.0-0 libgl1 libxkbcommon-x11-0 libgbm-dev libasound2
RUN python3 -m pip install validators

RUN useradd -d /home/ctf/ -m -p ctf -s /bin/bash ctf && echo "ctf:ctf" | chpasswd

RUN mkdir /home/ctf/attempts
RUN chmod 777 /home/ctf/attempts

USER ctf
WORKDIR /home/ctf

COPY entrypoint.sh entrypoint.sh
COPY visit.py visit.py
COPY flag flag
RUN mv flag flag-$(cat /dev/urandom | tr -cd 'a-f0-9' | head -c 32)

COPY chrome /home/ctf/chrome

EXPOSE 1337

CMD ./entrypoint.sh
