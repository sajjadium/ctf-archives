FROM pwn.red/jail:0.3.0
COPY --from=ubuntu:20.04 / /srv
COPY babypwn /srv/app/run
COPY flag.txt /srv/app
