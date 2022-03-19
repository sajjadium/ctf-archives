FROM ubuntu:20.04

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get -y update --fix-missing && apt-get -y upgrade
RUN groupadd -r pwn && useradd -r -g pwn pwn

RUN chmod 1733 /tmp /var/tmp /dev/shm

RUN echo "fak3pts{*** REDUCTED ***}" > /flag.txt
RUN chmod 444 /flag.txt
RUN mv /flag.txt /flag-$(md5sum flag.txt | awk '{print $1}').txt

WORKDIR /home/pwn
ADD ./bin/redis-lite-server redis-lite-server
RUN chmod 555 redis-lite-server
RUN chown -R root:pwn /home/pwn

USER pwn
