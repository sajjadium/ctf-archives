FROM ubuntu:20.04

RUN apt-get update
RUN apt-get install -y openssl libseccomp-dev
RUN useradd -d /home/challenge/ -m -p challenge -s /bin/bash challenge
RUN echo "challenge:challenge" | chpasswd

WORKDIR /home/challenge
COPY ./easysbx .
RUN echo "ASIS{fake_flag}" > flagXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX-xx
COPY ./ynetd .
COPY ./run.sh .
COPY ./lol .
COPY ./readflg .
RUN chown -R root:root /home/challenge/

USER challenge

CMD ./run.sh
