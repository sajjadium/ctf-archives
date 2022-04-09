FROM ubuntu:22.04

RUN apt-get update && apt-get install -y xinetd libc++-dev libc++abi-dev
RUN adduser --no-create-home --disabled-password --gecos "" problem
COPY problem flag.txt /
COPY xinetd.conf /etc/xinetd.d/problem
CMD ["/usr/sbin/xinetd", "-dontfork"]
