# syntax=docker/dockerfile:latest

FROM docker.io/library/ubuntu@sha256:562456a05a0dbd62a671c1854868862a4687bf979a96d48ae8e766642cd911e8 as builder


# Enable APT package caching
RUN rm -f /etc/apt/apt.conf.d/docker-clean && \
    echo 'Binary::apt::APT::Keep-Downloaded-Packages "true";' > /etc/apt/apt.conf.d/keep-cache

# Install packages
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked \
    apt-get update && \
    apt-get install -y curl unzip python3 clang git

ADD --link "https://github.com/github/codeql-cli-binaries/releases/download/v2.19.0/codeql-linux64.zip" ./
RUN unzip codeql-linux64.zip && rm codeql-linux64.zip

COPY flag.txt /flag.txt
WORKDIR /app
RUN git clone --recursive https://github.com/github/vscode-codeql-starter.git 
RUN cd vscode-codeql-starter && git checkout 4933b40c49c58c62a6dc6147fb7023268f0e52a2
COPY glas/example.qlx vscode-codeql-starter/codeql-custom-queries-cpp/example.qlx
COPY glas/dot_codeql vscode-codeql-starter/codeql-custom-queries-cpp/.codeql


RUN useradd -u 1000 jail || true

FROM pwn.red/jail@sha256:ee52ad5fd6cfed7fd8ea30b09792a6656045dd015f9bef4edbbfa2c6e672c28c

COPY --from=builder / /srv

COPY --chmod=0755 chal.py srv/app/run
RUN chmod -R 755 /srv/app/vscode-codeql-starter/codeql-custom-queries-cpp/

ENV JAIL_TIME 120
ENV JAIL_MEM 12G
ENV JAIL_TMP_SIZE 20M
ENV JAIL_POW 10000
ENV JAIL_PIDS 10000
ENV JAIL_CPU 1000
