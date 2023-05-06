FROM ubuntu:18.04

RUN apt-get update

RUN useradd -d /home/challenge/ -m -p challenge -s /bin/bash challenge
RUN echo "challenge:challenge" | chpasswd
 
WORKDIR /home/challenge
COPY ./challenge_bin/butterfly .
COPY ./extras/flag .
COPY ./extras/ynetd .
COPY ./extras/run.sh .

RUN chown -R root:root /home/challenge/

USER challenge
CMD ./run.sh

