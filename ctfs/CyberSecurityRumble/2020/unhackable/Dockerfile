FROM ubuntu:18.04

RUN apt-get update && apt-get -y upgrade
RUN apt-get install -y qemu-system-x86 xinetd && rm -rf /var/lib/apt/lists/*

# challenge files
RUN useradd -s /bin/bash ctf
COPY run.sh /home/
COPY bzImage /home/
COPY qemu_svc /etc/xinetd.d/

CMD find / -perm -777 -type d -exec chmod 755 {} \; && xinetd -dontfork
