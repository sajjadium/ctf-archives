FROM ubuntu:focal
MAINTAINER James

RUN apt-get update
RUN apt-get install xinetd bsdmainutils bc -qy
RUN useradd -m HouseofCats

CMD ["/usr/sbin/xinetd","-dontfork"]
