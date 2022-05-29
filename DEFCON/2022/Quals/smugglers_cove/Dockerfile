FROM ubuntu:20.04

WORKDIR /challenge
ARG DEBIAN_FRONTEND=noninteractive
# upgrade ran at Fri May 27 15:18:42 UTC 2022 (see packages.txt)
RUN apt-get update && apt-get upgrade -y && apt-get install curl -y && apt list --installed > /packages.txt

COPY libluajit-5.1.so.2 /usr/local/lib/libluajit-5.1.so.2
COPY cove dig_up_the_loot /challenge/

RUN ldconfig && chmod 111 /challenge/dig_up_the_loot
RUN adduser --no-create-home --disabled-password --gecos "" user

USER user

ENTRYPOINT ["/challenge/cove"]
