FROM ubuntu:focal@sha256:c9820a44b950956a790c354700c1166a7ec648bc0d215fa438d3a339812f1d01

RUN apt update

RUN dpkg --add-architecture i386 && \
    apt-get -y update && \
    apt install -y \
    libc6:i386 \
    libc6-dbg:i386 \
    libc6-dbg \
    lib32stdc++6 \
    g++-multilib

RUN useradd -p ctf ctf
RUN echo "ctf:ctf" | chpasswd

RUN mkdir /app
WORKDIR /app

COPY main .
COPY libc.so.6 .
COPY ld-linux.so.2 .
COPY flag.txt .
COPY ynetd .
COPY run.sh .

USER ctf
CMD ./ynetd -p 1234 ./run.sh

