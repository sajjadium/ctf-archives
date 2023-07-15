FROM ubuntu:22.04
ENV DEBIAN_FRONTEND noninteractive

RUN apt-get -y update --fix-missing && apt-get -y upgrade
RUN apt-get -y install xinetd cowsay
RUN groupadd -r pwn && useradd -r -g pwn pwn

RUN echo '#!/bin/bash\n\
service xinetd restart && /bin/sleep infinity' > /etc/init.sh
RUN echo 'service pwn\n\
{\n\
  type = UNLISTED\n\
  disable = no\n\
  socket_type = stream\n\
  protocol = tcp\n\
  wait = no\n\
  user = pwn\n\
  bind = 0.0.0.0\n\
  port = 9999\n\
  server = /home/pwn/aush\n\
}' > /etc/xinetd.d/pwn
RUN chmod 500 /etc/init.sh
RUN chmod 444 /etc/xinetd.d/pwn
RUN chmod 1733 /tmp /var/tmp /dev/shm

RUN echo "nek0pts{*** REDACTED ***}" > /flag.txt
RUN chmod 444 /flag.txt
RUN mv /flag.txt /flag-$(md5sum flag.txt | awk '{print $1}').txt

WORKDIR /home/pwn
ADD aush .
RUN chmod 550 aush

RUN chown -R root:pwn /home/pwn
RUN service xinetd restart
