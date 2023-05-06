FROM ubuntu:18.04
MAINTAINER JSec

RUN groupadd -r Cooldown && useradd -r -g Cooldown Cooldown
RUN apt-get update
RUN apt-get install xinetd -y
RUN chmod 774 /tmp
RUN chmod -R 774 /var/tmp
RUN chmod -R 774 /dev
RUN chmod -R 774 /run
RUN chmod 1733 /tmp /var/tmp /dev/shm

COPY ./xinetd /etc/xinetd.d/Cooldown

WORKDIR /home/Cooldown/
COPY ./share/ ./
RUN chown root:Cooldown ./ -R
RUN chmod 550 ./Cooldown
RUN chmod 550 ./run.sh

CMD ["/usr/sbin/xinetd","-dontfork"]
