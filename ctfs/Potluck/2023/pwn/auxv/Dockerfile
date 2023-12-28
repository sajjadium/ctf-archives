FROM ubuntu:22.04 AS app

ARG DEBIAN_FRONTEND="noninteractive"
RUN apt update
RUN apt -y install qemu-system-x86

WORKDIR /app/

ADD run.sh ./run
ADD prebuilt_system ./prebuilt_system


FROM pwn.red/jail
COPY --from=app / /srv

ENV JAIL_PORT=31337 JAIL_TIME=300 JAIL_CONNS=500 JAIL_CONNS_PER_IP=5 JAIL_PIDS=20 JAIL_MEM=300M JAIL_CPU=300 JAIL_POW=5000
