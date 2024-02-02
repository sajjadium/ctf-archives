FROM pwn.red/jail
COPY --from=ubuntu@sha256:dca176c9663a7ba4c1f0e710986f5a25e672842963d95b960191e2d9f7185ebe / /srv

COPY flag.txt /srv/app/
COPY chall /srv/app/run