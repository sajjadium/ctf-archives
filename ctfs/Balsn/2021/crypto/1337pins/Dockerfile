FROM python:3.9-slim
MAINTAINER sasdf

RUN apt-get update -y --fix-missing && \
    apt-get install -y \
        xinetd \
    && \
    rm -rf /var/lib/apt/lists/* && \
    useradd -m ctf && \
    chmod 774 /tmp && \
    chmod -R 774 /var/tmp && \
    chmod -R 774 /dev && \
    chmod -R 774 /run && \
    chmod 1733 /tmp /var/tmp /dev/shm && \
    echo '[*] Done'

COPY ./src /home/ctf
COPY ./flag.txt /flag.txt
COPY ./xinetd /etc/xinetd.d/xinetd

RUN chown -R root:root /home/ctf && \
    chmod 755 /home/ctf/server.py && \
    chown -R root:root /etc/xinetd.d/xinetd && \
    echo '[*] Done'

EXPOSE 27491
CMD ["/usr/sbin/xinetd", "-dontfork"]
