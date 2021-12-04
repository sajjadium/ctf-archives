FROM ubuntu:18.04
MAINTAINER ddaa
RUN apt-get update -y
RUN apt-get install libtdb-dev libtdb-dev -y
RUN useradd -m metatalk
RUN usermod -a -G shadow metatalk
RUN chmod 774 /tmp
RUN chmod -R 774 /var/tmp
RUN chmod -R 774 /dev
RUN chmod -R 774 /run
RUN chmod 1733 /tmp /var/tmp /dev/shm
RUN chown -R root:root /home/metatalk
CMD su metatalk -c "LD_LIBRARY_PATH=/home/metatalk /home/metatalk/afpd -d -F /home/metatalk/afp.conf"
