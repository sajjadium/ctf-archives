FROM ubuntu:18.04

RUN apt-get update

RUN useradd -d /home/challenge/ -m -p challenge -s /bin/bash challenge
RUN echo "challenge:challenge" | chpasswd
 
WORKDIR /home/challenge
COPY ./share/server .
COPY ./share/flag .
COPY ./share/ynetd .
COPY ./share/run.sh .

RUN chown -R root:root /home/challenge/

USER challenge
CMD ./run.sh

