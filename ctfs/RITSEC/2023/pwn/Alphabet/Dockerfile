FROM ubuntu@sha256:2adf22367284330af9f832ffefb717c78239f6251d9d0f58de50b86229ed1427 AS app
RUN apt-get update

FROM pwn.red/jail
COPY --from=app / /srv
COPY alphabet.bin /srv/app/run
COPY flag.txt /srv/app/
