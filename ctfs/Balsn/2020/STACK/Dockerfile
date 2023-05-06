FROM ubuntu:focal
MAINTAINER James

RUN apt-get update
RUN apt-get install xinetd -qy
RUN useradd -m STACK
RUN chown -R root:root /home/STACK
RUN chmod -R 755 /home/STACK

CMD ["/usr/sbin/xinetd","-dontfork"]
