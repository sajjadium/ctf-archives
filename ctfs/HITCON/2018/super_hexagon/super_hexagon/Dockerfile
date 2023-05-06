FROM ubuntu:18.04
MAINTAINER seanwu
RUN apt-get update
RUN apt-get install xinetd -y
RUN useradd -m super_hexagon
RUN chmod 774 /tmp
RUN chmod -R 774 /var/tmp
RUN chmod -R 774 /dev
RUN chmod -R 774 /run
RUN chmod 1733 /tmp /var/tmp /dev/shm
RUN chown -R root:root /home/super_hexagon
CMD ["/usr/sbin/xinetd","-dontfork"]
