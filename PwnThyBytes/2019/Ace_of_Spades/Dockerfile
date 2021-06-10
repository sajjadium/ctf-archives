FROM ubuntu:16.04
MAINTAINER monosource

RUN dpkg --add-architecture i386
RUN apt-get update -y
RUN apt-get install xinetd  -y
RUN apt-get install git gdb -y
RUN apt-get install libc6 -y
RUN apt-get install libc6:i386 -y

RUN useradd -U -m ace_of_spades

ADD --chown=root:root xinetd /etc/xinetd.d/ace_of_spades

EXPOSE 13375/tcp

RUN chmod 774 /tmp
RUN chmod -R 774 /var/tmp
RUN chmod -R 774 /dev
RUN chmod -R 774 /run
RUN chmod 1733 /tmp /var/tmp /dev/shm

RUN chown -R root:root /home/ace_of_spades
ADD --chown=root:root ace_of_spades /home/ace_of_spades/ace_of_spades
ADD --chown=root:root flag /home/ace_of_spades/flag

CMD ["/usr/sbin/xinetd","-dontfork"]