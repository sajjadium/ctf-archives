FROM rust:slim

WORKDIR /app

COPY ./server .

RUN cargo build --release

CMD ["./target/release/rustshop"]
