FROM ubuntu:18.04 AS builder

RUN apt update && apt install -y --no-install-recommends \
        python3-minimal \
        libc6-dev \
        gcc \
        g++ \
        make

RUN useradd -u 1000 ctf

FROM pwn.red/jail
COPY --from=builder / /srv

RUN mkdir -p /srv/app/quizzes
COPY gui.py flag.txt main.py /srv/app/
COPY quizzes /srv/app/tmp

COPY run.sh /srv/app/run
RUN chmod 755 /srv/app/run

COPY jail-hook.sh /jail/hook.sh
