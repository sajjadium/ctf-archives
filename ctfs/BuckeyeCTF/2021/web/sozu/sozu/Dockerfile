# lightly modified from https://github.com/sozu-proxy/sozu/blob/main/Dockerfile

FROM alpine:latest as builder

RUN apk update && apk add --no-cache --virtual .build-dependencies \
  cargo \
  build-base \
  file \
  libgcc \
  musl-dev \
  rust \
  git
RUN apk add --no-cache openssl-dev \
  llvm-libunwind \
  pkgconfig

RUN git clone https://github.com/sozu-proxy/sozu.git /source

WORKDIR /source/bin
RUN cargo build --release --features use-openssl

FROM alpine:latest as bin


RUN apk update && apk add --no-cache openssl-dev \
  llvm-libunwind \
  libgcc \
  bash

COPY --from=builder /source/target/release/sozu sozu
COPY start.sh /start.sh
EXPOSE 3000

ENTRYPOINT ["/start.sh"]

