FROM ubuntu:22.04 AS app

COPY chall /app/run
COPY key* /app/
COPY flag /flag

# You don't need to care about this
FROM pwn.red/jail
COPY --from=app / /srv