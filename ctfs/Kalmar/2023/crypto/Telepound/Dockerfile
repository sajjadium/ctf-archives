# builder

FROM alpine:latest AS builder

RUN apk add --no-cache curl gcc musl-dev

RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs > rustup.sh
RUN sh ./rustup.sh -y --profile minimal

COPY src src
COPY aes_frast aes_frast
COPY Cargo.toml Cargo.toml
COPY Cargo.lock Cargo.lock

RUN source "$HOME/.cargo/env" && cargo build --release

# deployment

FROM alpine:latest

RUN apk add --no-cache socat

COPY flag.txt ./
COPY --from=builder /target/release/telepound ./
EXPOSE 13337

CMD ["./telepound"]
