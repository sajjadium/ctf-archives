FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Etc/UTC

RUN apt-get update \ 
    && apt-get upgrade -y \
    && apt-get install -y \
    build-essential \
    wget \
    ca-certificates \ 
    cmake

RUN apt-get clean autoclean \ 
    && rm -rf /var/lib/apt/lists/*

WORKDIR /home/builder

RUN mkdir bus
COPY bus ./bus/
COPY main.cpp ./
COPY CMakeLists.txt ./
COPY build.sh ./

VOLUME /binaries

RUN mkdir /magic/

RUN ./build.sh /magic/

ENTRYPOINT [ "./build.sh", "/binaries/" ]

