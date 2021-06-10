FROM ubuntu:focal
MAINTAINER James

RUN apt-get update
RUN apt-get install xinetd bsdmainutils bc -qy
RUN useradd -m HouseofCats
RUN chown -R root:root /home/HouseofCats
RUN chmod -R 755 /home/HouseofCats

CMD ["/usr/sbin/xinetd","-dontfork"]
