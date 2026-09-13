FROM python:3.14.2-alpine3.23 AS chall

WORKDIR /app

RUN apk add --no-cache build-base && pip install pycryptodome==3.23.0

COPY src/ .
COPY flag /
RUN chmod +x chall.py

FROM pwn.red/jail
WORKDIR /
COPY --from=chall / /srv
RUN ln -s /app/chall.py /srv/app/run
ENV JAIL_MEM=120M \
    JAIL_PORT=5000 \
    JAIL_PIDS=32 \
    JAIL_TIME=300 \
    JAIL_TMP_SIZE=16M \
    JAIL_SYSCALLS=clone,wait4,landlock_create_ruleset,landlock_add_rule,landlock_restrict_self,prctl
