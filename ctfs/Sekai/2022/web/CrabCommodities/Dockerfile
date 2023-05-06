# build phase
FROM rust:slim AS builder

WORKDIR /app
COPY ./chall .
RUN cargo build --release

# final image
FROM debian:bullseye-slim

WORKDIR /app
COPY --from=builder /app/target/release/crabcommodities ./

RUN useradd -ms /bin/bash user
USER user

CMD ["/app/crabcommodities"]