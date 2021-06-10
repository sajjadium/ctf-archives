FROM ubuntu:18.04

RUN apt-get update

RUN useradd -d /home/challenge/ -m -p challenge -s /bin/bash challenge
RUN echo "challenge:challenge" | chpasswd
 
WORKDIR /home/challenge
COPY ./emoji .
COPY ./flag .
COPY ./ynetd .
COPY ./run.sh .
COPY ./libc-2.31.so .
COPY ./ld-2.31.so .

RUN chown -R root:root /home/challenge/

USER challenge
CMD ./run.sh

