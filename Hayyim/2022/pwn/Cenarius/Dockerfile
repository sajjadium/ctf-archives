FROM ubuntu:21.10
MAINTAINER JSec

RUN groupadd -r cenarius && useradd -r -g cenarius cenarius
RUN apt-get update
RUN apt-get install xinetd -y
RUN chmod 774 /tmp
RUN chmod -R 774 /var/tmp
RUN chmod -R 774 /dev
RUN chmod -R 774 /run
RUN chmod 1733 /tmp /var/tmp /dev/shm

COPY ./xinetd /etc/xinetd.d/cenarius

WORKDIR /home/cenarius/
COPY ./share/ ./
RUN chown root:cenarius ./ -R
RUN chmod 550 ./cenarius
RUN chmod 550 ./run.sh

CMD ["/usr/sbin/xinetd","-dontfork"]
