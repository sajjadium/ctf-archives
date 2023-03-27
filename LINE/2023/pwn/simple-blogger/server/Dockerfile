FROM ubuntu:jammy AS chroot
# FROM ghcr.io/google/nsjail/nsjail:latest

ENV DEBIAN_FRONTEND noninteractive
ENV DOCKER_BUILDKIT 0
ENV COMPOSE_DOCKER_CLI_BUILD 0

RUN mkdir -p /home/ctf
RUN groupadd -g 1000 ctf
RUN useradd -d /home/ctf -u 1000 -g 1000 ctf -s /usr/sbin/nologin
RUN chown -R ctf:ctf /home/ctf

RUN apt update -y && apt upgrade -y
RUN apt install -y sqlite3 libsodium-dev

FROM ubuntu:jammy
COPY --from=chroot / /chroot
COPY ./nsjail /home/ctf/
COPY ./nsjail.cfg /home/ctf/

RUN apt update -y && apt upgrade -y
RUN apt install -y socat
# for nsjail
RUN apt-get -y update && apt-get install -y \
    bison \
    flex \
    libprotobuf-dev \
    libnl-route-3-dev \
    libtool \
    pkg-config \
    protobuf-compiler

EXPOSE 13443
CMD socat TCP-LISTEN:13443,reuseaddr,fork EXEC:"/home/ctf/nsjail --config /home/ctf/nsjail.cfg -- /home/ctf/server"