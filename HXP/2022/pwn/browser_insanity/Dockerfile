# see docker-compose.yml

FROM ubuntu:20.04

RUN apt-get update && apt-get install -y --no-install-recommends \
        python3 procps qemu-system-x86 \
 && rm -rf /var/lib/apt/lists/

RUN useradd --create-home --shell /bin/bash ctf
WORKDIR /home/ctf

COPY ynetd /sbin/

COPY enter_challenge.py run_vm.sh kolibri.img ynetd /home/ctf/
ADD images /tmp/

RUN if [ -f /tmp/flag_real.img ] ; then \
        echo '[+] running on server with real flag' && \
        mv -v /tmp/flag_real.img /home/ctf/flag.img ; \
    else \
        echo '[+] running locally with fake flag' && \
        mv -v /tmp/flag_fake.img /home/ctf/flag.img ; \
    fi

RUN chmod 555 /home/ctf && \
    chown -R root:root /home/ctf && \
    chmod -R 000 /home/ctf/* && \
    chmod 500 /sbin/ynetd && \
    chmod 555 /home/ctf/enter_challenge.py && \
    chmod 555 /home/ctf/run_vm.sh && \
    chmod 444 /home/ctf/kolibri.img && \
    chmod 444 /home/ctf/flag.img

RUN find / -ignore_readdir_race -type f \( -perm -4000 -o -perm -2000 \) -not -wholename /readflag -delete
USER ctf
RUN ! find / -writable -or -user $(id -un) -or -group $(id -Gn|sed -e 's/ / -or -group /g') 2> /dev/null | grep -Ev -m 1 '^(/dev/|/run/|/proc/|/sys/|/tmp|/var/tmp|/var/lock)'
USER root

EXPOSE 1024

CMD ynetd -pow 28 -t 120 -lt 150 -lm -1 /home/ctf/enter_challenge.py
