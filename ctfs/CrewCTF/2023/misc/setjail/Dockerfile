FROM python:3.10 as chroot

RUN apt-get update && apt-get -y install socat

RUN groupadd -g 1000 -r user && useradd -u 1000 -r -g user user
RUN chmod 1733 /tmp /var/tmp /dev/shm

RUN mkdir -p /home/user

WORKDIR /home/user

COPY src/readflag.c /home/user/readflag.c
COPY src/main.py /home/user/main.py
COPY src/void.py /home/user/void.py
COPY src/entry.sh /home/user/entry.sh

RUN gcc readflag.c -o readflag && rm readflag.c

RUN chmod 550 *.py entry.sh
RUN chmod 110 readflag
RUN chown root:user *.py readflag entry.sh

CMD /home/user/entry.sh
