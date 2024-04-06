FROM python:3.10-slim as runner

FROM pwn.red/jail

COPY --from=runner / /srv
COPY chal.py /srv/app/
COPY flag.txt /srv/app/
COPY zig-linux-x86_64-0.11.0.tar.xz /srv/app/
COPY run.sh /srv/app/run
COPY chroot.sh /srv/app/
COPY hook.sh /jail/hook.sh
RUN  cd /srv/app && tar -xf zig-linux-x86_64-0.11.0.tar.xz && mv zig-linux-x86_64-0.11.0 zig

RUN chmod +x /srv/app/run

ENV JAIL_MEM=128M JAIL_DEV=null,zero,urandom,ptmx JAIL_PIDS=20 JAIL_ENV_HOME=/tmp JAIL_TMP_SIZE=64M