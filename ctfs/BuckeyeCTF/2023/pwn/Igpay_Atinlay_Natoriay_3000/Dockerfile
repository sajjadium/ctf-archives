FROM rust:slim@sha256:ff798ceb500fa43c91db10db881066057fefd36e16d531e7b1ed228ab2246175 as build

RUN rustup target add x86_64-unknown-linux-musl 

WORKDIR /app
COPY chal/ /app

RUN cargo build --release --target x86_64-unknown-linux-musl

RUN cp target/x86_64-unknown-linux-musl/release/igpay-atinlay-natoriay-3000 ./igpay-atinlay-natoriay-3000 && \
    chmod 755 ./igpay-atinlay-natoriay-3000 ./run

FROM pwn.red/jail@sha256:ee52ad5fd6cfed7fd8ea30b09792a6656045dd015f9bef4edbbfa2c6e672c28c as prod

COPY --from=alpine:latest@sha256:7144f7bab3d4c2648d7e59409f15ec52a18006a128c733fcff20d3a4a54ba44a / /srv
COPY --from=build /app/run /app/igpay-atinlay-natoriay-3000 /srv/app/

ENV JAIL_ENV_FLAG="bctf{fake_flag}"