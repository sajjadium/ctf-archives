FROM ubuntu:18.04

RUN apt update
RUN apt install -y xinetd libseccomp-dev
RUN useradd ctf

RUN mkdir /home/ctf
ADD isolated /home/ctf/isolated
ADD run.sh /home/ctf/run.sh
ADD flag /home/ctf/flag

RUN chmod 460 /home/ctf/*
RUN chown ctf:root /home/ctf/*
RUN chmod +x /home/ctf/isolated
RUN chmod +x /home/ctf/run.sh

ADD xinetd /etc/xinetd.d/
ADD libc-2.27.so /lib/x86_64-linux-gnu/libc-2.27.so
EXPOSE 7777

CMD ["/usr/sbin/xinetd","-dontfork"]
