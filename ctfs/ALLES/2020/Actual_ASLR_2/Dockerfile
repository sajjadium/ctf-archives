# docker build -t aaslr . && docker run -p 1024:1024 --rm -it aaslr

FROM ubuntu:19.04

RUN useradd -d /home/ctf/ -m -p ctf -s /bin/bash ctf
RUN echo "ctf:ctf" | chpasswd

WORKDIR /home/ctf

COPY aaslr .
COPY flag1 .
COPY flag2 .
COPY ynetd .

RUN chown -R root:root /home/ctf

USER ctf
ENTRYPOINT ./ynetd ./aaslr
