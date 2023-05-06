FROM ubuntu:latest
MAINTAINER ddaa
RUN apt update -y
RUN apt install libwrap0-dev libldap2-dev -y
RUN useradd -m ctf
RUN chmod 774 /tmp
RUN chmod -R 774 /var/tmp
RUN chmod -R 774 /dev
RUN chmod -R 774 /run
RUN chmod 1733 /tmp /var/tmp /dev/shm
RUN chown -R root:root /home/ctf
CMD su ctf -c "LD_LIBRARY_PATH=/home/ctf /home/ctf/afpd -d -F /home/ctf/afp.conf"
