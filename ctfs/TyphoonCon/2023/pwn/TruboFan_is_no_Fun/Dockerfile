FROM pwn.red/jail

ENV JAIL_TMP_SIZE=10M
ENV JAIL_MEM=20M

COPY --from=debian:10.0 / /srv/

RUN mkdir /srv/app/

COPY snapshot_blob.bin /srv/app/
COPY d8 /srv/app/
COPY flag.txt /srv/app/

COPY run /srv/app/

