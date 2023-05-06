FROM ubuntu:22.04

RUN apt-get update && \
  apt-get -y install socat

RUN groupadd ctf && useradd -g ctf ctf
COPY challenge/ /home/ctf/
WORKDIR /home/ctf
USER ctf

EXPOSE 7777
ENTRYPOINT ["socat", "tcp-l:7777,reuseaddr,fork", "EXEC:./wargames"]

