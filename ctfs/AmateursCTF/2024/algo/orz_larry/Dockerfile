FROM rust:alpine as builder
WORKDIR /usr/src/orz-larry
COPY . .
RUN cargo install --path .

FROM pwn.red/jail

COPY --from=builder /usr/local/cargo/bin/orz-larry /srv/app/run
COPY flag.txt /srv/app/flag.txt

ENV JAIL_TIME=15
ENV JAIL_MEM=32M
