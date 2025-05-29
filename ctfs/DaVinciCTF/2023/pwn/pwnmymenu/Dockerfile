FROM ubuntu@sha256:b2175cd4cfdd5cdb1740b0e6ec6bbb4ea4892801c0ad5101a81f694152b6c559 AS app

RUN apt-get update 
RUN apt-get install -y build-essential binutils-x86-64-linux-gnu
RUN rm -rf /var/lib/apt/lists/*

FROM pwn.red/jail

COPY --from=app / /srv

COPY run /srv/app/run
COPY lvl1.c /srv/app/lvl1.c
COPY lvl2.c /srv/app/lvl2.c
COPY lvl3.c /srv/app/lvl3.c
COPY seccomp-bpf.h /srv/app/seccomp-bpf.h
# RUN cp /srv/bin/bash /srv/app/run

ENV JAIL_ENV_TMP=/tmp
ENV JAIL_MEM=50M
ENV JAIL_TMP_SIZE=50M

