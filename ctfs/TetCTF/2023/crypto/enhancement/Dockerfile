FROM ubuntu:latest

RUN apt-get -y update && apt-get install -y
RUN apt-get -y install g++ cmake socat
RUN apt-get -y install libsecp256k1-dev

RUN useradd enhancement -m
COPY . /home/enhancement

USER enhancement:enhancement
WORKDIR /home/enhancement

RUN mkdir ./build
RUN cmake -B./build -S . -D CMAKE_BUILD_TYPE=Release
RUN cmake --build ./build

CMD socat -T 30 -d -d TCP-LISTEN:31340,reuseaddr,fork EXEC:"./build/enhancement"
