FROM ubuntu:20.04

RUN apt-get update && apt-get install -y xinetd
RUN adduser --no-create-home --disabled-password --gecos "" problem
COPY target/debug/tinebpf /problem
COPY flag.txt /flag.txt
COPY xinetd.conf /etc/xinetd.d/problem
CMD ["/usr/sbin/xinetd", "-dontfork"]
