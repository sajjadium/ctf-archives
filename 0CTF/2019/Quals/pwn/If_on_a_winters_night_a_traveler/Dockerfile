FROM ubuntu:18.04

RUN apt-get -y update
RUN apt-get -y upgrade
RUN apt-get install -y python xinetd
RUN chmod 1733 /tmp /var/tmp /dev/shm

RUN useradd -m calvino
COPY vim /home/calvino/
RUN chown root:calvino /home/calvino/vim
RUN chmod 750 /home/calvino/vim
COPY service.py /home/calvino/
RUN chown root:calvino /home/calvino/service.py
RUN chmod 750 /home/calvino/service.py
COPY flag /flag
COPY xinetd /etc/xinetd.d/xinetd
RUN chown root:calvino /flag
RUN chmod 440 /flag

RUN service xinetd restart

CMD ["/usr/sbin/xinetd", "-dontfork"]
