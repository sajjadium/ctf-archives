# echo 'hxp{XXX}' > flag.txt && docker build -t notes . && docker run -d -p 31337:31337 --cap-add=SYS_ADMIN notes && nc 127.0.0.1 31337

FROM debian:buster

RUN apt-get update && apt-get install --no-install-recommends -y \
        libpango1.0 && \
    rm -rf /var/lib/apt/lists/

RUN useradd --create-home --shell /bin/bash ctf
WORKDIR /home/ctf

COPY ynetd /sbin/

COPY vuln flag.txt /home/ctf/

RUN chmod 555 /home/ctf && \
    chown -R root:root /home/ctf && \
    chmod -R 000 /home/ctf/* && \
    chmod 500 /sbin/ynetd

RUN chmod 555 vuln && \
    chmod 444 flag.txt

USER ctf
RUN (find --version && id --version && sed --version && grep --version) > /dev/null
RUN ! find / -writable -or -user $(id -un) -or -group $(id -Gn|sed -e 's/ / -or -group  /g') 2> /dev/null | grep -Ev -m 1 '^(/dev/|/run/|/proc/|/sys/|/tmp|/var/tmp|/var/lock)'
USER root

EXPOSE 31337
CMD ["ynetd", "-u", "ctf", "-p", "31337", "-lt", "10", "-lm", "134217728", "/home/ctf/vuln"]

