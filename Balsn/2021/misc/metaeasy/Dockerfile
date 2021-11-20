FROM ubuntu:20.04
RUN apt-get update && apt-get -y upgrade
RUN apt-get install -y xinetd python3
RUN useradd -m metaeasy
RUN chmod 774 /tmp
RUN chmod -R 774 /var/tmp
RUN chmod -R 774 /dev
RUN chmod -R 774 /run
RUN chmod 1733 /tmp /var/tmp /dev/shm
COPY ./src /home/metaeasy
RUN chown -R root:root /home/metaeasy
COPY ./xinetd /etc/xinetd.d/xinetd
CMD ["/usr/sbin/xinetd","-dontfork"]