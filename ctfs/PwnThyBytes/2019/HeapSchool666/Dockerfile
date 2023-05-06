FROM debian:stretch
MAINTAINER Sin__


RUN apt-get update -y
RUN apt-get install xinetd libseccomp2 -y




RUN useradd -U -m heapschool666

ADD --chown=root:root HeapSchool666 /home/heapschool666/
ADD --chown=root:root flag /home/heapschool666/
ADD --chown=root:root xinetd /etc/xinetd.d/heapschool666


RUN chmod 774 /tmp
RUN chmod -R 774 /var/tmp
RUN chmod -R 774 /dev
RUN chmod -R 774 /run
RUN chmod 1733 /tmp /var/tmp /dev/shm
RUN chown -R root:root /home/heapschool666

EXPOSE 13370/tcp

CMD ["/usr/sbin/xinetd","-dontfork"]
