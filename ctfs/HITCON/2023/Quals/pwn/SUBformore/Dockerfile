FROM ubuntu:22.04@sha256:dfd64a3b4296d8c9b62aa3309984f8620b98d87e47492599ee20739e8eb54fbf as base

WORKDIR /app
COPY run.sh run
COPY lessequalmore lessequalmore
COPY chal.txt chal.txt
COPY flag.txt flag.txt


FROM pwn.red/jail
COPY --from=base / /srv
ENV JAIL_TIME=30 JAIL_CPU=500 JAIL_MEM=10M
