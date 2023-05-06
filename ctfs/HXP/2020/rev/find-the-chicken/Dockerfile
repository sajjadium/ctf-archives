# touch wrapper.py && docker build -t find-the-chicken . && docker run --cap-add=SYS_ADMIN --security-opt apparmor=unconfined -ti -p 55657:1024 find-the-chicken

FROM debian:buster

RUN DEBIAN_FRONTEND=noninteractive apt-get update && \
    apt-get install -y \
        python3 build-essential python3-requests \
    && rm -rf /var/lib/apt/lists/

RUN useradd --create-home --shell /bin/bash ctf
WORKDIR /home/ctf

COPY ynetd /sbin/
COPY wrapper.py dmg_boot.bin tas-emulator *.gb /home/ctf/

RUN chown -R root:root /home/ctf && \
    chmod 555 /home/ctf && \
    chmod -R 000 /home/ctf/* && \
    chmod 500 /sbin/ynetd && \
    chmod 555 /home/ctf/tas-emulator && \
    chmod 555 /home/ctf/wrapper.py && \
    chmod 444 /home/ctf/*.gb && \
    chmod 444 /home/ctf/dmg_boot.bin && \
    echo '32fbbd84168d3482956eb3c5051637f5 dmg_boot.bin' | md5sum  --check

USER ctf
RUN ! find / -writable -or -user $(id -un) -or -group $(id -Gn|sed -e 's/ / -or -group /g') 2> /dev/null | grep -Ev -m 1 '^(/dev/|/run/|/proc/|/sys/|/tmp|/var/tmp|/var/lock)'

USER root

EXPOSE 1024
CMD if [ -f /home/ctf/main-with-flag.gb ] ; then \
        echo '[+] running in remote mode' && \
        mv /home/ctf/main-with-flag.gb /home/ctf/main.gb && \
        ynetd -lt 60 -t 600 "/home/ctf/wrapper.py" ; \
    else \
        echo '[+] running in local mode' && \
        ynetd -lt 60 -t 600 "/home/ctf/tas-emulator playback STDIN -r terminal:5"; \
    fi
