FROM ubuntu:focal
MAINTAINER James

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update
RUN apt-get install xinetd -y
RUN useradd -m UnicornsAisle

CMD ["/usr/sbin/xinetd","-dontfork"]
