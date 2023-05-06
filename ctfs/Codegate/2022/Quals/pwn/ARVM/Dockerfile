FROM ubuntu:21.10


RUN apt update
RUN apt install -y xinetd qemu-user-static  gcc-arm-linux-gnueabi

RUN useradd ctf

RUN mkdir /home/ctf
ADD app /home/ctf/app
ADD run.sh /home/ctf/run.sh
ADD flag_XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX /home/ctf/flag_XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

RUN chmod 460 /home/ctf/*
RUN chown ctf:root /home/ctf/*
RUN chmod +x /home/ctf/app
RUN chmod +x /home/ctf/run.sh

ADD xinetd /etc/xinetd.d/
EXPOSE 1234

CMD ["/usr/sbin/xinetd","-dontfork"]