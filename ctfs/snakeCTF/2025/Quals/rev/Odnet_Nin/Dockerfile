FROM alpine:3.22 AS builder

RUN apk add --no-cache libc6-compat musl-dev gmp-dev

WORKDIR /app
COPY ./* .

ENV LD_LIBRARY_PATH="/app"

ENTRYPOINT exec ./coderunner
