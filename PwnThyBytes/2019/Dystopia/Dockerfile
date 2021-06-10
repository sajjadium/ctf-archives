FROM debian:10
MAINTAINER Sin__

RUN apt-get update -y
RUN apt-get install xinetd  -y



RUN useradd -U -m dystopia

ADD --chown=root:root flag /home/dystopia/
ADD --chown=root:root xinetd /etc/xinetd.d/dystopia

EXPOSE 13372/tcp


RUN chmod 774 /tmp
RUN chmod -R 774 /var/tmp
RUN chmod -R 774 /dev
RUN chmod -R 774 /run
RUN chmod 1733 /tmp /var/tmp /dev/shm

RUN chown -R root:root /home/dystopia
ADD --chown=root:root dystopia.elf /home/dystopia/dystopia

CMD ["/usr/sbin/xinetd","-dontfork"]
