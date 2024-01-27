FROM ubuntu:22.04 AS base

RUN apt-get clean && \
    apt-get update && \
    apt-get install -qy git && \
    git clone https://github.com/googleprojectzero/domato /domato

FROM python:3.10 AS py

# use the jail base image
FROM pwn.red/jail
ENV JAIL_MEM=20M JAIL_TIME=10 JAIL_PORT=9999

COPY --from=base /domato /srv/domato
COPY --from=py / /srv

COPY rwctf /srv/domato/rwctf
COPY chal.py /srv/domato/chal.py
COPY flag /flag

RUN mkdir /srv/app && \
    mv /flag /srv/app/flag_$(md5sum /flag | awk '{print $1}')

COPY run.sh /srv/app/run
