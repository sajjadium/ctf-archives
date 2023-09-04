# shamelessly copied from https://github.com/otter-sec/sol-ctf-framework/blob/main/examples/moar-horse-5/challenge/Dockerfile

FROM ubuntu:latest
COPY --from=krallin/ubuntu-tini /usr/bin/tini /tini
ENTRYPOINT ["/tini", "--"]

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get -y install libudev-dev libssl-dev pkg-config && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY gft-server gft.so flag.txt ./

RUN chmod +x ./gft-server
RUN chmod +x ./gft.so

RUN ln -sf /usr/lib/x86_64-linux-gnu/libcrypto.so.3 /usr/lib/x86_64-linux-gnu/libcrypto.so.1.1 && \
    ln -sf /usr/lib/x86_64-linux-gnu/libssl.so.3 /usr/lib/x86_64-linux-gnu/libssl.so.1.1

EXPOSE 5000
USER nobody
CMD ["/app/gft-server"]
