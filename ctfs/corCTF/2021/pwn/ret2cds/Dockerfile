FROM ubuntu:20.04

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update
RUN apt-get install -y openjdk-11-jdk

RUN useradd -m ret2cds

COPY ./chall /home/ret2cds
RUN mkdir /opt/nc-java
COPY ./server /opt/nc-java

RUN chmod 755 /home/ret2cds/*
RUN chmod 754 /home/ret2cds/flag.txt

RUN chmod 755 /opt/nc-java/*

COPY ./start.sh /start.sh
RUN chmod 755 /start.sh

USER ret2cds

CMD ["/start.sh"]