FROM alpine:latest as builder

RUN apk update && apk add gcc make musl-dev

RUN wget https://yx7.cc/code/ynetd/ynetd-0.1.2.tar.xz && \
    (echo "71c53f507b8fd75ef32bfebe4d476d1967a1332e  ynetd-0.1.2.tar.xz" | sha1sum -c) && \
    tar -xJf ynetd-0.1.2.tar.xz && cd ynetd-0.1.2 && CFLAGS="-static" make

### Stage 0: the base avatar2-core image
FROM ubuntu:20.04 AS base

### Stage 1: The avatar2-core build image
FROM base AS build-core

# avatar2 build dependencies
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends git cmake pkg-config build-essential python3-dev python3-pip libcapstone-dev && \
    pip3 install --upgrade --no-cache-dir pip

RUN git clone https://github.com/avatartwo/avatar2 /root/avatar2/
RUN cd /root/avatar2 && \
    python3 setup.py install



### Stage 2: Build avatar-qemu
FROM base AS build-avatar-qemu
ARG QEMU_TARGETS="arm-softmmu"

RUN sed -i '/deb-src .*-security main restricted/s/^#//g' /etc/apt/sources.list
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get build-dep -y qemu && \
    apt-get install -y git ninja-build

RUN git clone https://github.com/avatartwo/avatar-qemu /root/avatar-qemu/
RUN cd /root/avatar-qemu/ && \
    git checkout dev/qemu-6.2
RUN mkdir -p /root/avatar-qemu/build && cd /root/avatar-qemu/build && \
    ../configure \
        --without-default-features \
        --enable-tcg \
        --prefix=/usr/local/ \
        --target-list="${QEMU_TARGETS}" && \
    make -j "$(nproc)"
RUN cd /root/avatar-qemu/build/ && make install


### Stage 3: Build firmware
FROM base AS build-firmware

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y curl

RUN mkdir gcc-arm-none-eabi && curl -SL https://developer.arm.com/-/media/Files/downloads/gnu-rm/10.3-2021.10/gcc-arm-none-eabi-10.3-2021.10-x86_64-linux.tar.bz2 | tar xjC /gcc-arm-none-eabi --strip-components 1
ENV PATH="/gcc-arm-none-eabi/bin:${PATH}"

COPY firmware /firmware
RUN cd /firmware && ./build.sh

### Stage 3: Assemble the final image
FROM base AS avatar2

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends python3 python3-setuptools libcapstone3 gdb gdbserver gdb-multiarch && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY --from=build-core /usr/local /usr/local

RUN apt-get update && \
    apt-get install -y --no-install-recommends libfdt1 libpixman-1-0 libslirp-dev

COPY --from=build-avatar-qemu /usr/local /usr/local
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

ENV AVATAR2_QEMU_EXECUTABLE=/usr/local/bin/qemu-system-arm

COPY --from=build-firmware /firmware/build/firmware.bin /firmware.bin
COPY ./flag /flag
COPY chal.py /chal.py

EXPOSE 1234/tcp
EXPOSE 1024/tcp

COPY --from=builder /ynetd-0.1.2/ynetd /ynetd

CMD /ynetd -p 1024 "AVATAR2_QEMU_EXECUTABLE=$AVATAR2_QEMU_EXECUTABLE /usr/bin/python3 /chal.py"
