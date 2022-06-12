FROM rust:1.59

RUN apt-get update -y && apt-get install libudev-dev libssl-dev pkg-config -y

WORKDIR /app
COPY Cargo.toml Cargo.lock ./
COPY src ./src

ARG FLAG
ENV FLAG=$FLAG

RUN cargo build --release

COPY leagueoflamports.so ./

EXPOSE 8080

CMD [ "./target/release/league_of_lamports" ]
