FROM rust:1-slim-bullseye

RUN apt-get update && apt-get install -y libudev-dev libssl-dev pkg-config

WORKDIR /app
COPY Cargo.toml Cargo.lock ./
COPY src ./src

RUN cargo build --release

COPY beachside.so ./

EXPOSE 8080

CMD [ "./target/release/beachside" ]
