FROM ubuntu:16.04

RUN apt-get update && apt-get -y dist-upgrade 
RUN apt-get install -y bridge-utils

RUN apt-get install -y net-tools
RUN apt-get install -y iproute2
RUN apt-get install -y qemu-user
RUN apt-get install -y wget
RUN apt-get install -y curl
RUN apt-get install -y nginx

RUN rm /etc/nginx/sites-enabled/*
RUN rm /etc/nginx/nginx.conf

COPY ./nginx.conf /etc/nginx/nginx.conf
COPY ./start.sh /start.sh
COPY ./pwn /pwn
COPY flag /flag

CMD ["/start.sh"]
