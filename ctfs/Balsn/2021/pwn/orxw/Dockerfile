FROM ubuntu:20.04
MAINTAINER how2hack
RUN apt-get update --fix-missing
RUN apt-get upgrade -y
RUN apt-get install xinetd -y
RUN useradd -m orxw
RUN chmod 774 /tmp
RUN chmod -R 774 /var/tmp
RUN chmod -R 774 /dev
RUN chmod -R 774 /run
RUN chmod 1733 /tmp /var/tmp /dev/shm
COPY ./src /home/orxw
RUN chown -R root:root /home/orxw
COPY ./xinetd /etc/xinetd.d/xinetd
CMD ["/usr/sbin/xinetd","-dontfork"]
