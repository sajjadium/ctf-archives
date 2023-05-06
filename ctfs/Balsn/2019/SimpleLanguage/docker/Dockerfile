FROM ubuntu:18.04
MAINTAINER Billy
RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install xinetd libseccomp-dev -y
RUN apt-get install python3 -y
RUN apt-get install socat
RUN useradd -m SimpleLanguage
COPY ./share /home/SimpleLanguage
COPY ./xinetd /etc/xinetd.d/SimpleLanguage
RUN chmod 774 /tmp
RUN chmod -R 774 /var/tmp
RUN chmod -R 774 /dev
RUN chmod -R 774 /run
RUN chmod 1733 /tmp /var/tmp /dev/shm
RUN chown -R root:root /home/SimpleLanguage
CMD ["/usr/sbin/xinetd","-dontfork"]
