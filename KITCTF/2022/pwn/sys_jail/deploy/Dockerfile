# docker build -t sys_jail . && docker run -p 1339:1339 -t sys_jail
FROM ubuntu:20.04

ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y socat hashcash python3 qemu-system-x86-64

RUN useradd -d /home/ctf/ -m -p ctf -s /bin/bash ctf && echo "ctf:ctf" | chpasswd

WORKDIR /home/ctf/

EXPOSE 1339
USER ctf

COPY bzImage bzImage
COPY initramfs.cpio.gz initramfs.cpio.gz
COPY launch.sh launch.sh
COPY pow.py pow.py

ENTRYPOINT [ "socat", "tcp-l:1339,reuseaddr,fork", "EXEC:'/usr/bin/stdbuf -i0 -o0 -e0 python3 pow.py \"./launch.sh\"'" ]
