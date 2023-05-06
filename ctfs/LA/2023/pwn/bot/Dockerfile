FROM pwn.red/jail

COPY --from=debian@sha256:98d3b4b0cee264301eb1354e0b549323af2d0633e1c43375d0b25c01826b6790 / /srv
COPY bot /srv/app/run
COPY flag.txt /srv/app/flag.txt

ENV JAIL_TIME=60

RUN chmod 755 /srv/app/run
