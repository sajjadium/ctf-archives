FROM ubuntu:20.04

RUN apt-get update && apt-get install -y xinetd
RUN adduser --no-create-home --disabled-password --gecos "" vending
WORKDIR /vending
COPY vending .
COPY xinetd.conf /etc/xinetd.d/vending
CMD ["/usr/sbin/xinetd", "-dontfork"]
