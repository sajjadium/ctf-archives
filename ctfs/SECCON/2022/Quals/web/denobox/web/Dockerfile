FROM rust:1.64.0 as builder

WORKDIR /usr/src/denobox
RUN cargo init
COPY ["Cargo.toml", "Cargo.lock", "./"]
RUN cargo build --release
RUN rm -f target/release/deps/denobox*

COPY src src
RUN cargo install --locked --path .


FROM denoland/deno:1.27.0

WORKDIR /app
COPY views views
COPY sandbox sandbox
RUN chmod 1777 sandbox

COPY --from=builder /usr/local/cargo/bin/denobox /usr/local/bin/denobox

USER deno
CMD while true; do \
    rm -rf sandbox/*; \
    sleep 30m; \
    done & \
    denobox
