FROM ubuntu:22.04

RUN apt-get update
RUN apt-get install -y xinetd python3 libglib2.0-dev libfdt-dev libpixman-1-dev zlib1g-dev ninja-build libnfs-dev libiscsi-dev build-essential

COPY qemu-system-x86_64 /
COPY run.sh /
COPY bzImage /
COPY init.cpio /
COPY ynetd /
COPY bios /

EXPOSE 10003

CMD ./ynetd -p 10003 "timeout 600 /run.sh"
