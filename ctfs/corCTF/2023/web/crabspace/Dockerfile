# build phase
FROM rust:slim AS builder

WORKDIR /app
COPY . .
RUN cargo build --release

# final image
FROM debian:bullseye-slim

COPY flag.txt /flag.txt

WORKDIR /app
COPY --from=builder /app/target/release/crabspace ./
COPY --from=builder /app/public ./public
COPY --from=builder /app/templates ./templates

RUN useradd -ms /bin/bash user
USER user

ENV SECRET secretsecretsecretsecretsecretsecretsecretsecretsecretsecretsecr

CMD ["/app/crabspace"]