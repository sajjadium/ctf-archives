# Origin image
FROM ubuntu:16.04

# update
RUN apt update -y

RUN apt upgrade -y

# Setup Server Environment
RUN apt install -y \
    libsqlite3-dev \
    socat

# add new user if it is needed
RUN useradd -d /home/ctf/ -m -p ctf -s /bin/bash ctf
RUN echo "ctf:ctf" | chpasswd

# Change work directory
WORKDIR /home/ctf


RUN chmod 555 /home/ctf
RUN chmod 770 /tmp

# Change user
USER ctf

# Entry point
ENTRYPOINT socat tcp-l:5555,fork,reuseaddr exec:./client && /bin/bash
