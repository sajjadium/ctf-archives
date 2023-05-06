# build stage
FROM rust:1.67.1-bullseye as builder

WORKDIR /root/app
COPY . .

RUN cargo build --release --bin hanko

# final stage
FROM debian:bullseye-slim

# Setup magick
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl ca-certificates libfontconfig1 libx11-6 libharfbuzz0b libfribidi0 && \
    rm -rf /var/lib/apt/lists/*

ARG MAGICK_URL="https://github.com/ImageMagick/ImageMagick/releases/download/7.1.0-51/ImageMagick--gcc-x86_64.AppImage"
RUN curl --location --fail -o /usr/local/bin/magick $MAGICK_URL && \
    chmod 755 /usr/local/bin/magick
ENV APPIMAGE_EXTRACT_AND_RUN=1

RUN mkdir ./data

COPY --from=builder /root/app/target/release/hanko /usr/local/bin/hanko

RUN echo 'FAKE{REDACTED}' > /flag_A
ENV FLAG_B="FAKE{REDACTED}"

ENV RUST_LOG="hanko,tower_http=TRACE,INFO"
ENV LISTEN_ADDR="0.0.0.0:3000"
ENTRYPOINT ["hanko"]
