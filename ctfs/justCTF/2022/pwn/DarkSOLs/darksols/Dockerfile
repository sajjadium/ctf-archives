FROM rust:1.59

RUN apt-get update -y && apt-get install libudev-dev libssl-dev pkg-config -y

WORKDIR /app
COPY Cargo.toml Cargo.lock ./
COPY src ./src
COPY spl-token ./spl-token

ARG FLAG
ENV FLAG=$FLAG

RUN cargo build --release

COPY darksols.so evil-contract.so ./

EXPOSE 8080

CMD [ "./target/release/dark-sols" ]

