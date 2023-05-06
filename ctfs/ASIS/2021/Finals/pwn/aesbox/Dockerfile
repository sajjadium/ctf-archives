FROM ubuntu:20.04

RUN apt-get update

RUN useradd -d /home/challenge/ -m -p challenge -s /bin/bash challenge
RUN echo "challenge:challenge" | chpasswd

WORKDIR /home/challenge
COPY ./aes
RUN echo "ASIS{fake_flag}" > flagXXXXXXXXXXXXXXXXXXX.txt
COPY ./ynetd .
COPY ./run.sh .

RUN chown -R root:root /home/challenge/

USER challenge
CMD ./run.sh
