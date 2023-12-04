# ----------------- Bot Builder
FROM rust:1.74-slim AS rust-builder
WORKDIR /builder

RUN apt-get update; apt-get install -y clang pkg-config build-essential libssl-dev

COPY Cargo.toml Cargo.lock ./
COPY src/ ./src/
RUN cargo build --release

# ----------------- Runtime
FROM us.gcr.io/blaz-ctf/ctf-server:latest

COPY daemon.py /home/user/
COPY --from=rust-builder /builder/target/release/frontrun-bot /home/user/

CMD ["python3", "-u", "/home/user/daemon.py"]