FROM pwn.red/jail

COPY --from=fedora@sha256:dfb5e6183f515192b37df9356622b676461a41b724d9f92953433dca3e85deb1 / /srv
COPY monty /srv/app/run
COPY flag.txt /srv/app/flag.txt
RUN chmod 755 /srv/app/run
