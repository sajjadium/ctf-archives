FROM rust:alpine AS builder

RUN apk add --no-cache musl-dev
RUN rustup target add x86_64-unknown-linux-musl

COPY Cargo.lock Cargo.toml /build/
COPY ./src /build/src
COPY ./templates /build/templates

WORKDIR /build
RUN cargo build --release

FROM scratch

EXPOSE 3000

COPY --from=builder /build/target/release/tasktracker /

USER 1000
CMD ["/tasktracker"]
