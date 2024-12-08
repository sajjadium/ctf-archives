FROM docker.io/library/ubuntu@sha256:278628f08d4979fb9af9ead44277dbc9c92c2465922310916ad0c46ec9999295 AS builder

FROM pwn.red/jail@sha256:ee52ad5fd6cfed7fd8ea30b09792a6656045dd015f9bef4edbbfa2c6e672c28c

COPY --from=builder / /srv

COPY chal /srv/app/run
COPY flag.txt /srv/app/flag.txt

RUN chmod 755 /srv/app/run 
RUN chmod 744 /srv/app/flag.txt

ENV JAIL_TIME=300
ENV JAIL_MEM=50M
