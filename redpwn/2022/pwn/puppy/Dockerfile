FROM pwn.red/jail:0.3.0

COPY --from=ubuntu@sha256:bace9fb0d5923a675c894d5c815da75ffe35e24970166a48a4460a48ae6e0d19 / /srv
COPY puppy /srv/app/run
COPY flag.txt /srv/app/
