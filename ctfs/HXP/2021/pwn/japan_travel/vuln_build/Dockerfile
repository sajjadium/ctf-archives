FROM ubuntu:trusty

RUN apt update -y && apt upgrade -y && apt install -y build-essential cmake

ADD src/ src/

ADD CMakeLists.txt CMakeLists.txt

RUN mkdir build && \
    cd build && \
    cmake ../ && \
    make
