FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update
RUN apt-get install -y cargo socat

COPY . /challenge
WORKDIR /challenge

RUN cargo build --release
RUN tar -c -f optimal_technology_project.tar.gz -z src/main.rs Dockerfile Cargo.toml

ENTRYPOINT [ "socat", "tcp-l:23451,reuseaddr,fork", "exec:/challenge/target/release/optimal_technology_project"]

# Add your own secret.rs with:
# `pub const MSG: &str = "<your local flag>";`