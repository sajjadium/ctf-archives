FROM ubuntu:16.04

RUN sed -i "s/http:\/\/archive.ubuntu.com/http:\/\/mirrors.huaweicloud.com/g" /etc/apt/sources.list
RUN apt-get update && apt-get -y dist-upgrade
RUN apt-get install -y lib32z1 xinetd build-essential

RUN useradd -m ctf
RUN mkdir -p /home/ctf
COPY ./flag /home/ctf/

COPY ./qemu-system-x86_64 /home/ctf/qemu-system-x86_64
COPY ./rootfs.cpio /home/ctf/rootfs.cpio
COPY ./start.sh /home/ctf/start.sh
COPY ./vmlinuz-4.8.0-52-generic /home/ctf/vmlinuz-4.8.0-52-generic
COPY ./ctf.xinetd /etc/xinetd.d/ctf
COPY ./pc-bios /home/ctf/pc-bios

COPY ./lib/libgio-2.0.so.0 /usr/lib/x86_64-linux-gnu/
COPY ./lib/libglib-2.0.so.0  /usr/lib/x86_64-linux-gnu/
COPY ./lib/libgobject-2.0.so.0  /usr/lib/x86_64-linux-gnu/
COPY ./lib/libjpeg.so.8  /usr/lib/x86_64-linux-gnu/
COPY ./lib/liblzo2.so.2  /usr/lib/x86_64-linux-gnu/
COPY ./lib/libpixman-1.so.0  /usr/lib/x86_64-linux-gnu/
COPY ./lib/libpng12.so.0  /usr/lib/x86_64-linux-gnu/
COPY ./lib/libgmodule-2.0.so.0 /usr/lib/x86_64-linux-gnu/
COPY ./lib/libffi.so.6 /usr/lib/x86_64-linux-gnu/
RUN chmod 755 /usr/lib/x86_64-linux-gnu/libgio-2.0.so.0 
RUN chmod 755 /usr/lib/x86_64-linux-gnu/libglib-2.0.so.0
RUN chmod 755 /usr/lib/x86_64-linux-gnu/libgobject-2.0.so.0
RUN chmod 755 /usr/lib/x86_64-linux-gnu/libjpeg.so.8
RUN chmod 755 /usr/lib/x86_64-linux-gnu/liblzo2.so.2
RUN chmod 755 /usr/lib/x86_64-linux-gnu/libpixman-1.so.0
RUN chmod 755 /usr/lib/x86_64-linux-gnu/libpng12.so.0
RUN chmod 755 /usr/lib/x86_64-linux-gnu/libgmodule-2.0.so.0
RUN chmod 755 /usr/lib/x86_64-linux-gnu/libffi.so.6
RUN chmod 755 /home/ctf/flag
RUN chmod 755 /home/ctf/qemu-system-x86_64
RUN chmod 755 /home/ctf/rootfs.cpio
RUN chmod 755 /home/ctf/start.sh
RUN chmod 755 /home/ctf/vmlinuz-4.8.0-52-generic

COPY ./ctf.xinetd /etc/xinetd.d/ctf
COPY ./pc-bios /home/ctf/pc-bios
RUN chown root:ctf /home/ctf/start.sh && chmod 750 /home/ctf/start.sh
RUN echo 'ctf - nproc 1500' >>/etc/security/limits.conf

RUN cp -R /lib* /home/ctf && \
    cp -R /usr/lib* /home/ctf

RUN mkdir /home/ctf/dev && \
    mknod /home/ctf/dev/null c 1 3 && \
    mknod /home/ctf/dev/zero c 1 5 && \
    mknod /home/ctf/dev/random c 1 8 && \
    mknod /home/ctf/dev/urandom c 1 9 && \
    chmod 666 /home/ctf/dev/*

RUN mkdir /home/ctf/bin && \
    cp /bin/sh /home/ctf/bin && \
    cp /bin/ls /home/ctf/bin && \
    cp /bin/cat /home/ctf/bin && \
    cp /usr/bin/timeout /home/ctf/bin

RUN chown -R root:ctf /home/ctf && \
    chmod -R 750 /home/ctf && \
    chmod 740 /home/ctf/flag

CMD exec /bin/bash -c "/etc/init.d/xinetd start ; trap : TERM INT; sleep infinity & wait"
EXPOSE 8888
#/etc/init.d/xinetd start