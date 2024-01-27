FROM ubuntu:latest
MAINTAINER peternguyen
RUN apt-get update
RUN apt-get install socat python3 libssl-dev libcap2-bin libcap-ng-utils -y

RUN useradd -m interface
RUN useradd -u 1001 backend

RUN chmod 774 /tmp
RUN chmod -R 774 /var/tmp
RUN chmod -R 774 /dev
RUN chmod -R 774 /run
RUN chmod 1733 /tmp /var/tmp /dev/shm

ADD entry.sh /entry.sh
RUN chmod +x /entry.sh

ADD start.sh /home/interface
ADD flag1 /home/interface/
ADD flag2 /home/interface/
ADD notes_manager/build/interface /home/interface/interface
ADD notes_manager/build/backend /home/interface/backend
#ADD notes_manager.xinetd /etc/xinetd.d/notes

#RUN chmod 644 /etc/xinetd.d/notes
RUN chown -R root:interface /home/interface/
RUN chmod 755 /home/interface
RUN chmod 755 /home/interface/interface
RUN chmod 750 /home/interface/start.sh
RUN setcap cap_setuid,cap_setgid,cap_kill=+ep /home/interface/interface

RUN chmod 755 /home/interface/backend
RUN chown root:backend /home/interface/backend

RUN chown root:interface /home/interface/flag1
RUN chmod 440 /home/interface/flag1
RUN chown root:backend /home/interface/flag2
RUN chmod 440 /home/interface/flag2

User interface
CMD ["/entry.sh"]
#CMD ["/usr/sbin/xinetd"," -dontfork"]
#CMD [/usr/sbin/xinetd, -dontfork]
