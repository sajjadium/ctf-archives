FROM rust@sha256:0372c87d4372dc1ae23caaf287f643f7c5ca799b40405efbb1bdf67588cc2629

RUN apt-get update && apt-get install -qy libudev-dev tini

WORKDIR /app
COPY Cargo.toml Cargo.lock ./
COPY src ./src

COPY chall ./chall

RUN cargo build --release

RUN sh -c "$(curl -sSfL https://release.solana.com/v1.10.32/install)"
ENV PATH="/root/.local/share/solana/install/active_release/bin:${PATH}"
RUN cd chall && cargo build-bpf

ENTRYPOINT [ "tini", "-g", "--" ]
CMD [ "./target/release/framework" ]
