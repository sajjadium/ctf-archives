FROM ubuntu:latest
RUN apt-get update
RUN apt-get install xinetd libseccomp-dev -y
RUN useradd -m asianparent
RUN chmod 774 /tmp
RUN chmod -R 774 /var/tmp
RUN chmod -R 774 /dev
RUN chmod -R 774 /run
RUN chmod 1733 /tmp /var/tmp /dev/shm
RUN chown -R root:root /home/asianparent
CMD ["/usr/sbin/xinetd","-dontfork"]