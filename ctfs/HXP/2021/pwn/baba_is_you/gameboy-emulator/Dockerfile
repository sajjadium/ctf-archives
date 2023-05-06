# docker build -t build-emulator . && docker run -d --name build-emulator build-emulator && docker cp $(docker ps -aqf "name=^build-emulator$"):/emulator/target/release/emulator ../tas-emulator && docker rm build-emulator

FROM debian:bullseye


RUN DEBIAN_FRONTEND=noninteractive apt-get update && \
    apt-get install -y \
        curl build-essential pkg-config libudev-dev \
    && rm -rf /var/lib/apt/lists/

RUN curl https://sh.rustup.rs -sSf | bash -s -- -y
ENV PATH="/root/.cargo/bin:${PATH}"

RUN mkdir -p /emulator
WORKDIR /emulator

COPY mooneye-gb/ /emulator/mooneye-gb/
COPY Cargo.toml Cargo.lock rustfmt.toml /emulator/
COPY src/ /emulator/src/

RUN cargo build --release
