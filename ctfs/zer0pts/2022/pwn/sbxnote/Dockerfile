FROM ubuntu:20.04

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get -y update --fix-missing && apt-get -y upgrade
RUN apt-get -y install xinetd
RUN groupadd -r pwn && useradd -r -g pwn pwn

ADD etc/pwn.xinetd /etc/xinetd.d/pwn
ADD etc/init.sh    /etc/init.sh
ADD bin/redir.sh   /home/pwn/.redir.sh
RUN chmod 700  /etc/init.sh
RUN chmod 550  /home/pwn/.redir.sh
RUN chmod 1733 /tmp /var/tmp /dev/shm

WORKDIR /home/pwn
RUN echo fak3pts{sample_flag} > flag.txt
ADD bin/chall chall
RUN chmod 440 flag.txt
RUN chmod 550 chall
RUN mv flag.txt flag-$(md5sum flag.txt | awk '{print $1}').txt

RUN chown -R root:pwn /home/pwn

RUN ls /home/pwn -lh

RUN service xinetd restart
