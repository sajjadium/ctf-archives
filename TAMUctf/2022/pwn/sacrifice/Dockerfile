FROM rust:slim-buster as build

COPY src /opt/sacrifice/src
COPY Cargo.toml /opt/sacrifice/Cargo.toml

RUN cargo build --release --manifest-path /opt/sacrifice/Cargo.toml

FROM rust:slim-buster

COPY --from=build /opt/sacrifice/target/release/sacrifice /sacrifice/server
COPY std-lol /sacrifice/std-lol
COPY flag.txt /sacrifice
COPY static/ /sacrifice/static
COPY runners/ /sacrifice/runners

WORKDIR /sacrifice

EXPOSE 7777

ENTRYPOINT ["/sacrifice/server"]
