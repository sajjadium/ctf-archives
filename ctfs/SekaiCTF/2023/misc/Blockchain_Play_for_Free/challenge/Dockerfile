FROM debian:bullseye-slim
COPY --from=krallin/ubuntu-tini /usr/bin/tini /tini
ENTRYPOINT ["/tini", "--"]

RUN apt-get update && \
    apt-get -y install libudev-dev libssl-dev pkg-config && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY arcade-server Arcade.so flag.txt ./

EXPOSE 8080
USER nobody
CMD ["/app/arcade-server"]