FROM docker.io/library/ubuntu:22.04@sha256:0e5e4a57c2499249aafc3b40fcd541e9a456aab7296681a3994d631587203f97 as builder

RUN useradd -u 1000 jail

FROM pwn.red/jail@sha256:ee52ad5fd6cfed7fd8ea30b09792a6656045dd015f9bef4edbbfa2c6e672c28c

COPY --from=builder / /srv

COPY main /srv/app/run
COPY flag.txt /srv/app/flag.txt

RUN chmod 755 /srv/app/run 
RUN chmod 744 /srv/app/flag.txt

ENV JAIL_TIME 60
ENV JAIL_MEM 20M