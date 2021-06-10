FROM debian:buster 

COPY run.sh /run.sh
COPY start.sh /start.sh
COPY bzImage /bzImage
COPY rootfs.ssh /rootfs.ssh

RUN apt-get update \
     && apt-get install -y qemu-system
CMD /start.sh
