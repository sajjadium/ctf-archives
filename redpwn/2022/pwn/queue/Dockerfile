FROM pwn.red/jail:0.3.0

COPY --from=ubuntu@sha256:b2339eee806d44d6a8adc0a790f824fb71f03366dd754d400316ae5a7e3ece3e / /srv
COPY queue /srv/app/run
COPY flag.txt /srv/app/
