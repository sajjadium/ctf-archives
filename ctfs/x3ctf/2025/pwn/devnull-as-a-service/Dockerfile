FROM docker.io/library/ubuntu:oracular

RUN useradd -m -d /home/ctf -s /bin/false ctf && \
    chown -R root:root /home/ctf && \
    chmod -R 555 /home/ctf

COPY dev_null /home/ctf/dev_null
COPY flag.txt /home/ctf/flag.txt
COPY ynetd /home/ctf/ynetd

RUN chmod 555 /tmp && \
    chmod 555 /var/tmp && \
    chmod 555 /dev && \
    chmod 555 /run

USER ctf
WORKDIR /home/ctf

EXPOSE 1337

CMD ["/bin/sh", "-c", "/home/ctf/ynetd -p 1337 /home/ctf/dev_null -se y"]