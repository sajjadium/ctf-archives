FROM ubuntu:22.04

RUN apt-get update && apt install qemu-system -y

COPY ./bzImage /bzImage
COPY ./rootfs.cpio /rootfs.cpio
COPY ./run.sh /run.sh

CMD ["sh", "/run.sh"]
