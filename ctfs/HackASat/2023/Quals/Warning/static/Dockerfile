FROM ubuntu:22.04

ARG DEBIAN_FRONTEND=noninteractive

ARG TZ=Etc/UTC

RUN apt update \ 
    && apt upgrade -y \
    build-essential \
    cmake \
    && apt-get clean autoclean \ 
    && rm -rf /var/lib/apt/lists/*

WORKDIR /home/builder 
VOLUME /binaries 
COPY *.cpp ./
COPY CMakeLists.txt ./
COPY *.sh ./

RUN mkdir /warning

RUN cmake -B build . &&\
    cmake --build build &&\
    cp ./build/warning /warning/

ENTRYPOINT [ "./build.sh","/binaries" ]
