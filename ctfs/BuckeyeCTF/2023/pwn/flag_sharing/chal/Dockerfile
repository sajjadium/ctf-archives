FROM ubuntu:22.04@sha256:b492494d8e0113c4ad3fe4528a4b5ff89faa5331f7d52c5c138196f69ce176a6 as base

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get -y update && apt-get install -y build-essential \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/ctf/chal
WORKDIR /home/ctf/chal
COPY challenge.c Makefile ./
RUN make

# latest as of 9/21/23
FROM pwn.red/jail@sha256:ee52ad5fd6cfed7fd8ea30b09792a6656045dd015f9bef4edbbfa2c6e672c28c

ENV JAIL_CPU=1000
ENV JAIL_TIME=300
ENV JAIL_MEM=50M
COPY --from=base / /srv
COPY run.sh /run.sh
RUN mkdir -p /srv/app && cp /srv/home/ctf/chal/challenge /srv/app/run
CMD ["/run.sh"]
