# Operating system builder

# 4M
ARG FLAG_LOCATION_PHYS=4194304
FROM --platform=amd64 alpine:3.17 AS builder
ARG FLAG_LOCATION_PHYS
RUN apk add --update --no-cache \
    gcc \
    make \
    nasm \
    && true

WORKDIR /challenge

COPY ./ ./
RUN make all FLAG_LOCATION_PHYS=${FLAG_LOCATION_PHYS}

# The wrapper for running the OS
FROM --platform=amd64 alpine:3.17
ARG FLAG_LOCATION_PHYS

RUN apk add --update --no-cache \
    qemu-system-x86_64 \
    socat \
    && true

WORKDIR /challenge

COPY --from=builder /challenge/os.img ./os.img
COPY ./start-qemu.sh ./start-qemu.sh

ENV FLAG=PP{this-is-not-a-valid-flag-only-demo}

ENV FLAG_LOCATION_PHYS=${FLAG_LOCATION_PHYS}

CMD [ "socat", "-d", "TCP-LISTEN:1337,reuseaddr,fork,max-children=1", "exec:'ash /challenge/start-qemu.sh',pty,stderr,setsid,sane,sigint"]
