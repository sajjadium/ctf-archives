FROM rust@sha256:79ddef683780336ce47c56c86184cf49e4f36c598d8f0bfe9453f52437b1b9a9

RUN apt-get update && apt-get install -qy libudev-dev

WORKDIR /app
COPY Cargo.toml Cargo.lock ./
COPY src ./src

COPY chall ./chall

RUN cargo build --release

RUN sh -c "$(curl -sSfL https://release.solana.com/v1.16.9/install)"
ENV PATH="/root/.local/share/solana/install/active_release/bin:${PATH}"
RUN cd chall && cargo build-bpf

ENV FLAG="n1ctf{wow_funny_fake_flag}"

CMD [ "./target/release/framework" ]