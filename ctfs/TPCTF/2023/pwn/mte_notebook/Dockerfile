FROM ubuntu:22.04
RUN apt-get update && apt-get install qemu-system-arm -y
RUN apt-get install cpio -y
COPY Image /
COPY vm_rootfs /vm_rootfs
COPY run.sh /
CMD ["bash", "/run.sh"]
