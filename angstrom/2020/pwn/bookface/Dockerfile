#IMPORTANT: on host system: sysctl vm.mmap_min_addr=0
FROM ubuntu:xenial

RUN apt-get update
RUN apt-get install -y xinetd zsh

COPY xinetd.conf /etc/xinetd.d/ctf

WORKDIR /ctf
RUN mkdir /ctf/users

COPY bookface .
COPY server.sh .
COPY flag.txt .
RUN chmod +x server.sh
RUN chmod +x bookface
RUN chown -R 1000 /ctf

EXPOSE 1337

ENTRYPOINT ["xinetd", "-dontfork", "-limit", "256"]
