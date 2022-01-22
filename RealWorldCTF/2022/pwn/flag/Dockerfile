FROM ubuntu:20.04

RUN sed -i "s/http:\/\/archive.ubuntu.com/http:\/\/mirrors.aliyun.com/g" /etc/apt/sources.list && \
	sed -i "s/http:\/\/security.ubuntu.com/http:\/\/mirrors.aliyun.com/g" /etc/apt/sources.list
RUN  apt-get update && \
        apt-get -y dist-upgrade

RUN apt install -y --no-install-recommends ca-certificates qemu-system-arm python3 python3-pip

RUN pip install requests

COPY ./flag.py /

EXPOSE 5555

CMD qemu-system-arm -m 64 -nographic -machine vexpress-a9 -net user,hostfwd=tcp::5555-:80 -net nic -kernel /mnt/flag.bin
