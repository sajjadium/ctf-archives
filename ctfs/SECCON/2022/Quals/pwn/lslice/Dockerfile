FROM ubuntu:22.04

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get -y update --fix-missing && apt-get -y upgrade
RUN apt-get -y install xinetd python3 hashcash
RUN groupadd -r pwn && useradd -r -g pwn pwn

ADD etc/pwn.xinetd /etc/xinetd.d/pwn
ADD etc/init.sh    /etc/init.sh
ADD etc/redir.sh   /home/pwn/.redir.sh
RUN chmod 550 /home/pwn/.redir.sh
RUN chmod 700 /etc/init.sh
RUN chmod 1733 /tmp /var/tmp /dev/shm

WORKDIR /home/pwn
ADD flag.txt flag.txt
ADD bin/lua    lua
ADD bin/app.py app.py
RUN chmod 440 flag.txt
RUN chmod 550 lua
RUN chmod 550 app.py
RUN mv flag.txt flag-$(md5sum flag.txt | awk '{print $1}').txt

RUN chown -R root:pwn /home/pwn

RUN ls /home/pwn -lh

RUN service xinetd restart
