FROM ubuntu:19.04
MAINTAINER Billy
RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install xinetd libseccomp-dev python -y
RUN useradd -m note
COPY ./share /home/note
COPY ./xinetd /etc/xinetd.d/note
COPY ./flag /home/note
RUN chmod 774 /tmp
RUN chmod -R 774 /var/tmp
RUN chmod -R 774 /dev
RUN chmod -R 774 /run
RUN chmod 1733 /tmp /var/tmp /dev/shm
RUN chown -R root:root /home/note
CMD ["/usr/sbin/xinetd","-dontfork"]
