FROM ubuntu:16.04
MAINTAINER c2w2m2

RUN apt update
RUN apt install -y xinetd
ENV TERM=linux

RUN useradd ctf

CMD ["/usr/sbin/xinetd","-dontfork"]

