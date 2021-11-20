FROM ubuntu:latest
MAINTAINER James

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update
RUN apt-get install xinetd qemu-system-x86 -y
RUN useradd -m ElfFortress

CMD ["/usr/sbin/xinetd","-dontfork"]
