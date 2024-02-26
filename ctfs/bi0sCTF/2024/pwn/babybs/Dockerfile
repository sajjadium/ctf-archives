FROM ubuntu:22.04

RUN apt-get update
RUN apt-get install -y xinetd python3 qemu-system-i386 build-essential

COPY run.sh /
COPY ynetd /
COPY babybs.bin /

EXPOSE 10000
CMD ./ynetd -p 10000 "timeout 150 /run.sh"
