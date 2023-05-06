FROM ubuntu:20.04

RUN apt-get update && \
DEBIAN_FRONTEND=noninteractive apt-get install -y xinetd qemu-system-x86 hashcash && \
addgroup ctf && \
adduser --disabled-password --gecos "" --ingroup ctf ctf

COPY app.xinetd /etc/xinetd.d/app

WORKDIR /home/ctf/app
COPY bzImage initramfs.cpio.gz launch.sh launch_pow.sh ./

CMD service xinetd start && tail -F /var/log/xinetdlog
