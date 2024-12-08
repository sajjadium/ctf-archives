# syntax=docker/dockerfile:latest
FROM ubuntu:22.04@sha256:0e5e4a57c2499249aafc3b40fcd541e9a456aab7296681a3994d631587203f97 AS builder

#Enable APT package caching
RUN rm -f /etc/apt/apt.conf.d/docker-clean && \
    echo 'Binary::apt::APT::Keep-Downloaded-Packages "true";' > /etc/apt/apt.conf.d/keep-cache

RUN dpkg --add-architecture i386

#Install base packages
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked \
    apt update && \
    apt install -y --no-install-recommends \
        gcc-multilib

RUN useradd -u 1000 jail

FROM pwn.red/jail@sha256:ee52ad5fd6cfed7fd8ea30b09792a6656045dd015f9bef4edbbfa2c6e672c28c

COPY --from=builder / /srv

RUN mkdir -p /srv/app/exec
COPY flag /srv/app/exec

RUN ls

COPY order66 /srv/app/run
RUN chmod 755 /srv/app/run
COPY flag /srv/app/flag

COPY jail-hook.sh /jail/hook.sh