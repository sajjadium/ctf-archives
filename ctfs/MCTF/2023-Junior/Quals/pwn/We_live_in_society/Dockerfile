FROM ubuntu:22.04 AS app
RUN apt-get -y update && apt-get -y update  
ARG DEBIAN_FRONTEND=noninteractive
RUN apt install -y build-essential

FROM pwn.red/jail
COPY --from=app / /srv

ARG BIN_NAME FLAG

COPY ./$BIN_NAME /srv/app/run

RUN echo $FLAG > /srv/app/flag.txt
ENV JAIL_MEM=50M JAIL_PIDS=10 JAIL_TIME=30 JAIL_CPU=30 JAIL_DEV=null,zero,urandom
