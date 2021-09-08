FROM rust:latest AS build

RUN apt-get update && apt-get install -y clang libudev-dev git

RUN rustup component add rustfmt

RUN mkdir /build

WORKDIR /build
RUN git clone https://github.com/solana-labs/solana.git && cd solana && git checkout 03b930515bc554396bc69d811be834d22978a1d3
WORKDIR /build/solana
COPY vuln.patch /build/solana
RUN git apply vuln.patch
RUN cargo build --release --bin solana-test-validator

COPY setup/ /build/setup
WORKDIR /build/setup
RUN cargo run --bin generate_ledger

COPY flag-program/ /build/flag-program
WORKDIR /build/flag-program
RUN cargo build --release


FROM ubuntu:20.04

RUN apt-get update && apt-get install -y clang libudev-dev git

COPY --from=build /build/setup/ledger/ /ledger/
COPY --from=build /build/flag-program/target/release/libflag.so /usr/bin/libflagloader_program.so
COPY --from=build /build/solana/target/release/solana-test-validator /usr/bin/solana-test-validator

ENV FLAG="ALLES!{placeholder}"
EXPOSE 1024

CMD ["solana-test-validator", "-l", "/ledger/", "--rpc-port", "1024", "--dynamic-port-range", "1025-65535"]