FROM rust:1.54.0-bullseye AS build

RUN sh -c "$(curl -sSfL https://release.solana.com/v1.7.10/install)"
ENV PATH="/root/.local/share/solana/install/active_release/bin:${PATH}"

RUN apt-get update && apt-get install -y clang libudev-dev

RUN rustup component add rustfmt

RUN mkdir /build

COPY program/ /build/program
WORKDIR /build/program
RUN cargo build-bpf

COPY cli/ /build/cli
COPY keys/ /build/keys
COPY flag-program/ /build/flag-program
COPY Cargo.lock Cargo.toml  /build/

WORKDIR /build/
RUN cargo build --release
RUN cp /build/program/target/deploy/store.so /build/ && cargo run --release --bin store-cli -- -k /build/keys/rich-boi.json initialize-ledger


FROM ubuntu:20.04

RUN apt-get update && apt-get install -y curl && sh -c "$(curl -sSfL https://release.solana.com/v1.7.10/install)"
ENV PATH="/root/.local/share/solana/install/active_release/bin:${PATH}"

COPY --from=build /build/ledger/ /ledger/
COPY --from=build /build/target/release/store-cli /usr/bin/
COPY --from=build /build/keys/ /keys/
COPY --from=build /build/target/release/libflag.so /root/.local/share/solana/install/active_release/bin/libflagloader_program.so

ENV FLAG="ALLES!{placeholder}"
EXPOSE 1024

CMD ["/bin/sh", "-c", "((sleep 2; store-cli -k /keys/rich-boi.json setup /keys/flag-depot.json $(dd if=/dev/urandom count=8 bs=1 | od -A n -t u8)) &); solana-test-validator -l /ledger/ --rpc-port 1024 --dynamic-port-range 1025-65535"]
