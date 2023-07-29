FROM ubuntu:22.04

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && \
    apt-get install -y python3

RUN useradd -m daydream && \
    mkdir /opt/daydream && \
    mkdir /opt/daydream/usr && \
    mkdir /opt/daydream/bin && \
    cp -R /lib* /opt/daydream && \
    cp -R /usr/lib* /opt/daydream/usr && \
    cp /bin/* /opt/daydream/bin && \
    cp -R /usr/bin* /opt/daydream/usr

RUN mkdir /opt/daydream/dev && \
    mknod /opt/daydream/dev/null c 1 3 && \
    mknod /opt/daydream/dev/zero c 1 5 && \
    mknod /opt/daydream/dev/random c 1 8 && \
    mknod /opt/daydream/dev/urandom c 1 9 && \
    chmod 666 /opt/daydream/dev/*

COPY daydream main.py wrapper /opt/daydream/

RUN chmod -R o-w /opt/daydream/daydream && \
    chmod 550 /opt/daydream/main.py && \
    chmod 550 /opt/daydream/wrapper && \
    chmod 555 /opt/daydream/daydream

EXPOSE 5000
CMD ["/usr/sbin/chroot", "/opt/daydream", "./main.py"]
