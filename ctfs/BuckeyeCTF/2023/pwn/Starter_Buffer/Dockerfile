FROM ubuntu:jammy-20230816 AS app

WORKDIR /app
COPY buffer flag.txt ./

FROM pwn.red/jail@sha256:ee52ad5fd6cfed7fd8ea30b09792a6656045dd015f9bef4edbbfa2c6e672c28c as prod
COPY --from=app / /srv
RUN mv /srv/app/buffer /srv/app/run