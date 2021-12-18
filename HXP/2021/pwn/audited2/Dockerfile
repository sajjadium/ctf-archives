# Running locally:
# 1) echo 'hxp{FLAG}' > flag.txt
# 2) docker build -t audited2 .
# 3) docker run -p 8007:1024 --rm --cap-add=SYS_ADMIN --security-opt apparmor=unconfined -it audited2

# Build and install the auditing module
FROM debian:bullseye AS builder

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 python3-dev python3-wheel python3-setuptools build-essential && \
    rm -rf /var/lib/apt/lists

COPY module/ /root/module
WORKDIR /root/module
RUN python3 setup.py install --record /root/auditor-files.txt && \
    tar --absolute-names -cvf /root/auditor-module.tar --files-from=/root/auditor-files.txt

# Start from scratch, no need to keep GCC around
FROM debian:bullseye

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 && \
    rm -rf /var/lib/apt/lists

COPY --from=builder /root/auditor-module.tar /root/
RUN tar -xvf /root/auditor-module.tar && \
    rm -f /root/auditor-module.tar

RUN useradd --create-home --shell /bin/bash ctf
WORKDIR /home/ctf
COPY audited.py /home/ctf/
COPY ynetd /sbin/
COPY flag.txt docker-stuff/readflag /

RUN chown root:1337 /flag.txt /readflag && \
    chmod 040 /flag.txt && \
    chmod 2555 /readflag

RUN chmod 555 /home/ctf && \
    chown -R root:root /home/ctf && \
    chmod -R 000 /home/ctf/* && \
    chmod 500 /sbin/ynetd && \
    chmod 005 /home/ctf/audited.py

RUN find / -ignore_readdir_race -type f \( -perm -4000 -o -perm -2000 \) -not -wholename /readflag -delete
USER ctf
RUN (find --version && id --version && sed --version && grep --version) > /dev/null
RUN ! find / -writable -or -user $(id -un) -or -group $(id -Gn|sed -e 's/ / -or -group /g') 2> /dev/null | grep -Ev -m 1 '^(/tmp|/var/mail|/var/spool/mail|/var/tmp|/var/lock|/run/lock|/dev|/proc)'

USER root
EXPOSE 1024
CMD ynetd -np y -t 15 -sh n /home/ctf/audited.py
