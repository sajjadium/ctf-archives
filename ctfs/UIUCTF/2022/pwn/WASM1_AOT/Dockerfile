# To build:
# DOCKER_BUILDKIT=1 docker build . --target release --output type=local,dest=../challenge

FROM wasmedge/wasmedge:latest AS wasmedge

COPY build.sh /root/build.sh
RUN /root/build.sh

FROM --platform=linux/amd64 ubuntu:20.04 AS build

RUN apt-get -y update && apt-get -y install build-essential

WORKDIR /root
COPY --from=wasmedge /root/export/ ./
COPY Makefile ./
COPY chal.c ./
COPY Dockerfile ./
COPY build.sh ./

RUN make
RUN tar czvf /root/handout.tar.gz chal libwasmedge_c.so chal.c Makefile Dockerfile build.sh

FROM scratch AS release

COPY --from=build /root/handout.tar.gz /
