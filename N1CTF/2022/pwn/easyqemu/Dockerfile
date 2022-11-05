FROM ubuntu:20.04

RUN sed -i "s/http:\/\/archive.ubuntu.com/http:\/\/mirrors.tuna.tsinghua.edu.cn/g" /etc/apt/sources.list && \
    apt update && apt-get -y dist-upgrade && \
    DEBIAN_FRONTEND=noninteractive \
    apt-get install -y lib32z1 xinetd git libglib2.0-dev libfdt-dev libpixman-1-dev  libasound2 libpng16-16 libbrlapi0.7 libpulse0 zlib1g-dev libxen* libvdeplug* libfuse* libnfs*
RUN apt install -y xinetd

ENV FLAG="N1CTF{flag}"

RUN groupadd -r ctf && useradd -r -g ctf ctf

RUN rm -rf /ctf
COPY ./src/ctf /home/ctf
COPY ./src/ctf.xinetd /etc/xinetd.d/ctf
COPY ./src/start.sh /start.sh
COPY ./src/spawner /spawner

RUN chown -R ctf:ctf /home/ctf && chmod -R 555 /home/ctf && \
    chmod 555 /start.sh && \
    chmod 555 /home/ctf/run.sh && \
    chmod 444 /etc/xinetd.d/ctf && \
    chmod u+x /home/ctf/qemu-system-x86_64 && \
    chown root:root /spawner && chmod 500 /spawner

CMD ["/bin/sh", "/start.sh"]
