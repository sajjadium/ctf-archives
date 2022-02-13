FROM ubuntu:18.04
MAINTAINER JSec

RUN groupadd -r warmup && useradd -r -g warmup warmup
RUN apt-get update
RUN apt-get install xinetd -y
RUN chmod 774 /tmp
RUN chmod -R 774 /var/tmp
RUN chmod -R 774 /dev
RUN chmod -R 774 /run
RUN chmod 1733 /tmp /var/tmp /dev/shm

COPY ./xinetd /etc/xinetd.d/warmup

WORKDIR /home/warmup/
COPY ./share/ ./
RUN chown root:warmup ./ -R
RUN chmod 550 ./warmup
RUN chmod 550 ./run.sh

CMD ["/usr/sbin/xinetd","-dontfork"]
