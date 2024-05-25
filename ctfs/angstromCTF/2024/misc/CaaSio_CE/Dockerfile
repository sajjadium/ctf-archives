FROM pwn.red/jail

COPY --from=node:22-bookworm-slim / /srv
COPY --chmod=755 caasio.js /srv/app/run
COPY flag.txt /srv/app/flag.txt
