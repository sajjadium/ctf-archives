# shamelessly copied from https://github.com/otter-sec/sol-ctf-framework/blob/main/examples/moar-horse-5/challenge/Dockerfile

FROM ubuntu:21.10
COPY --from=krallin/ubuntu-tini /usr/bin/tini /tini
ENTRYPOINT ["/tini", "--"]

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get -y install libudev-dev libssl-dev pkg-config && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY solnote-server solnote.so flag.txt ./

RUN chmod +x ./solnote-server
RUN chmod +x ./solnote.so

EXPOSE 5000
USER nobody
CMD ["/app/solnote-server"]
