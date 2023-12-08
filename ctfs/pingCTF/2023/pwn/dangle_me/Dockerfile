FROM debian:stable-slim@sha256:cd763f86078e1b4daea9de030256224caf9fb3b3c54e381c08ade14ccfb4baa3 as base
WORKDIR /app
COPY dangle run
COPY flag.txt flag.txt

FROM pwn.red/jail
COPY --from=base / /srv
ENV JAIL_TIME=180
