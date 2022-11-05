FROM lukemathwalker/cargo-chef:latest-rust-1.65.0 AS chef
WORKDIR /src

FROM chef AS planner
COPY . .
RUN cargo chef prepare --recipe-path recipe.json

FROM chef AS builder
COPY --from=planner /src/recipe.json recipe.json
RUN cargo chef cook --release --recipe-path recipe.json
COPY . .
RUN cargo build --release

FROM ubuntu:22.04
RUN apt-get update && apt-get install -y locales
RUN sed -i '/en_US.UTF-8/s/^# //g' /etc/locale.gen && \
    locale-gen
ENV LC_ALL en_US.UTF-8
ENV LANG en_US.UTF-8
RUN apt-get update && apt-get install -y gcc gdb wget python3 file python3-pip tmux gdbserver
RUN wget -O ~/.gdbinit-gef.py -q https://gef.blah.cat/py
RUN pip3 install pwntools
RUN echo source ~/.gdbinit-gef.py >> ~/.gdbinit
COPY flag /flag
COPY --from=builder /src/target/release/rattlespike /opt/rattlespike
COPY --from=builder /src/target/release/playground /opt/playground
