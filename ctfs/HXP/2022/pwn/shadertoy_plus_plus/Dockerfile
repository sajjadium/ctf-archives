# see docker-compose.yml

FROM ubuntu:22.04

RUN apt-get update && apt-get install -y --no-install-recommends xorg

RUN rm -rf /var/lib/apt/lists/ && rm -rf /usr/lib/systemd/

RUN useradd --create-home --shell /bin/bash ctf
WORKDIR /home/ctf

# Copy ynetd for serving connections
COPY ynetd /sbin/

# Copy challenge-specific files
COPY libs /home/ctf/gfx_libs
COPY hxp_gpu /home/ctf/hxp_gpu
COPY flag.txt /home/ctf/flag.txt
COPY run.sh /home/ctf/run.sh

RUN chmod 555 /home/ctf && \
    chown -R root:root /home/ctf && \
    chmod -R 000 /home/ctf/* && \
    chmod 500 /sbin/ynetd && \
    chmod -R 555 /home/ctf/gfx_libs/ && \
    chmod 555 /home/ctf/run.sh && \
    chmod 555 /home/ctf/hxp_gpu && \
    chmod 444 /home/ctf/flag.txt

USER ctf
RUN ! find / -writable -or -user $(id -un) -or -group $(id -Gn|sed -e 's/ / -or -group /g') 2> /dev/null | grep -Ev -m 1 '^(/dev/|/run/|/proc/|/sys/|/tmp|/var/tmp|/var/lock)'

USER root
EXPOSE 1024

CMD ynetd -pow 28 -p 1024 -lt 320 -t 40 -lm 536870912 /home/ctf/run.sh

