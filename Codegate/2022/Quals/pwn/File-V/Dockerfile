FROM ubuntu:18.04

RUN apt update
RUN apt install -y xinetd
RUN useradd ctf

RUN mkdir /home/ctf
ADD file-v /home/ctf/file-v
ADD run.sh /home/ctf/run.sh
ADD README.md.v /home/ctf/README.md.v
ADD flag.v /home/ctf/flag.v
ADD flag /home/ctf/flag

RUN chmod 460 /home/ctf/*
RUN chown ctf:root /home/ctf/*
RUN chmod +x /home/ctf/file-v
RUN chmod +x /home/ctf/run.sh

ADD xinetd /etc/xinetd.d/
ADD libc-2.27.so /lib/x86_64-linux-gnu/libc-2.27.so
EXPOSE 5555

CMD ["/usr/sbin/xinetd","-dontfork"]
