FROM rust as build

ADD src /build/src
ADD Cargo.toml /build/Cargo.toml

WORKDIR /build

RUN cargo build --release

FROM debian:buster-slim

ARG port
ARG name

RUN apt update; apt -y install socat
COPY --from=build /build/target/release/$name /crypto/$name
ADD flag.txt flag.txt

RUN echo "exec socat -s TCP-LISTEN:$port,reuseaddr,fork EXEC:/crypto/$name,stderr" > /crypto/docker_entrypoint.sh

ENTRYPOINT ["sh", "/crypto/docker_entrypoint.sh"]
