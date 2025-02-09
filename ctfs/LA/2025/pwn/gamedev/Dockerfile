FROM pwn.red/jail

COPY --from=debian@sha256:b5ace515e78743215a1b101a6f17e59ed74b17132139ca3af3c37e605205e973 / /srv
COPY chall /srv/app/run
COPY flag.txt /srv/app/flag.txt
RUN chmod 755 /srv/app/run
