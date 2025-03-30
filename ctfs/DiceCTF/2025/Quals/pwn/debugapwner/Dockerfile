FROM ubuntu@sha256:ed1544e454989078f5dec1bfdabd8c5cc9c48e0705d07b678ab6ae3fb61952d2 AS base
RUN apt-get update && \
    apt-get install -y libelf-dev python3

FROM pwn.red/jail
ENV JAIL_TMP_SIZE=32000000
ENV JAIL_TIME=10000
COPY --from=base / /srv

COPY server.py /srv/app/run
COPY dwarf /srv/dwarf
COPY flag.txt /srv/flag.txt

