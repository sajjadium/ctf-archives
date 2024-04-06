FROM python:3.10-slim as runner

FROM pwn.red/jail

COPY --from=runner / /srv
COPY chal.py /srv/app/run
COPY flag.txt /srv/app/
COPY zig-linux-x86_64-0.11.0.tar.xz /srv/app/
RUN  cd /srv/app && tar -xf zig-linux-x86_64-0.11.0.tar.xz && mv zig-linux-x86_64-0.11.0 zig

RUN chmod +x /srv/app/run

ENV JAIL_MEM=150M JAIL_PIDS=30 JAIL_ENV_HOME=/tmp JAIL_TMP_SIZE=64M JAIL_TIME=300