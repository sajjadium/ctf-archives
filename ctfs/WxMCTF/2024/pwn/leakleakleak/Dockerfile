FROM pwn.red/jail

COPY --from=ubuntu:22.04 / /srv

RUN mkdir /srv/app
COPY flag.txt /srv/app/flag.txt
COPY leakleakleak /srv/app/run