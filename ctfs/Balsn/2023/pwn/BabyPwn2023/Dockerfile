FROM ubuntu:22.04
MAINTAINER YingMuo

RUN apt-get update
RUN apt-get install xinetd -qy
RUN useradd -m chall
RUN chown -R root:root /home/chall
RUN chmod -R 755 /home/chall

CMD ["/usr/sbin/xinetd","-dontfork"]
