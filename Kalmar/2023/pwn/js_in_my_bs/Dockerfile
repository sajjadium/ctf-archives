FROM ubuntu:22.04

RUN apt-get update
RUN apt-get install -y xinetd python3 libglib2.0-dev libfdt-dev libpixman-1-dev zlib1g-dev ninja-build libnfs-dev libiscsi-dev build-essential

COPY qemu-system-i386 /
COPY run.sh /
COPY ynetd /
COPY bios /bios
COPY bootjs.bin /

EXPOSE 10000
CMD ./ynetd -p 10000 "timeout 600 /run.sh"
