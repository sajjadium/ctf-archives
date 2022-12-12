FROM ubuntu:20.04

RUN apt-get update

RUN useradd -d /home/ctf/ -m -p ctf -s /bin/bash ctf
RUN echo "ctf:ctf" | chpasswd

WORKDIR /home/ctf

COPY chall .
COPY flag.txt .
COPY ynetd .

RUN chown -R root:root /home/ctf

USER ctf
EXPOSE 1337
CMD ./ynetd -p 1337 ./chall
