FROM ubuntu:latest@sha256:c920ba4cfca05503764b785c16b76d43c83a6df8d1ab107e7e6610000d94315c

COPY vault /srv/vault 
COPY ld.so.2 /srv/ld.so.2
COPY libc.so.6 /srv/libc.so.6
RUN apt update &&  apt install -y socat && useradd -m -s /bin/bash chall

USER chall

ENTRYPOINT ["socat", "TCP-LISTEN:5000,reuseaddr,fork", "EXEC:\"./srv/ld.so.2 --library-path /srv ./srv/vault\""]
