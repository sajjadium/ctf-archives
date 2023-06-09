# docker build -t connect4 . && docker run -p 1337:1337 connect4
FROM ubuntu:22.10

ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update --fix-missing && apt-get upgrade -y
RUN apt-get install -y make socat

RUN echo "dd0ddeaf2293dd418123b8fb03022337d7ac6ac3  /lib/x86_64-linux-gnu/libc.so.6" | sha1sum -c

RUN adduser --disabled-password --gecos "" user

WORKDIR /home/user/

COPY game_server/target/release/game_server game_server
COPY game_client/client client
COPY entrypoint.sh entrypoint.sh

EXPOSE 1337
USER user

CMD ./entrypoint.sh
