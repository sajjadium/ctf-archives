FROM ubuntu:latest

RUN apt-get update -y
RUN apt-get install xinetd -y

RUN getent passwd pivot || useradd -m pivot

COPY ./pivot /etc/xinetd.d/pivot
COPY ./share/run.sh /home/pivot/run.sh
COPY ./share/pivot /home/pivot/pivot
COPY ./init.sh /init.sh

RUN chmod +x /init.sh
RUN chmod +x /home/pivot/run.sh

RUN chown -R root:root /init.sh
RUN chown -R root:pivot /home/pivot
RUN chmod -R 755 /home/pivot

RUN echo pivot > /etc/cron.deny
RUN chmod 644 /etc/cron.deny
RUN chmod 644 /etc/xinetd.d/pivot

RUN chmod -R 774 /var/tmp
RUN chmod -R 774 /tmp
RUN chmod -R 774 /dev
RUN chmod -R 774 /run
RUN chmod 1733 /dev/shm

WORKDIR /home/pivot
