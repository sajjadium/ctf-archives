FROM ubuntu:20.04

RUN apt-get update && apt-get install -y xinetd
RUN adduser --no-create-home --disabled-password --gecos "" engine
WORKDIR /engine
COPY engine .
COPY xinetd.conf /etc/xinetd.d/engine
CMD ["/usr/sbin/xinetd", "-dontfork"]
