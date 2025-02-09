FROM pwn.red/jail

COPY --from=debian:bookworm-slim / /srv
COPY the-eye /srv/app/run
COPY msg.txt /srv/app/msg.txt
RUN chmod 755 /srv/app/run
