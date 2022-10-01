FROM pwn.red/jail:0.3.0
COPY --from=ubuntu:jammy-20220815 / /srv
COPY challenge /srv/app/run
COPY flag.txt /srv/app/
