FROM zephyrprojectrtos/ci-base as build

# Clone latest master
RUN git clone --depth=1 https://github.com/zephyrproject-rtos/zephyr && cd zephyr && git checkout 44e691e20e0b323ad67227ee072bd4166c75d894

RUN west init -l zephyr && west update
RUN cd zephyr && ZEPHYR_TOOLCHAIN_VARIANT=gcc west build -b native_posix samples/bluetooth/handsfree

## Second stage
FROM i386/debian:bookworm

RUN apt-get update && apt-get install -y --no-install-recommends strace socat adduser && rm -rf /var/lib/apt/lists/*
COPY tcp_bluetooth.sh /
COPY --from=build /zephyr/build/zephyr/zephyr.elf /

RUN adduser --disabled-password --gecos '' user && \
    adduser --disabled-password --gecos '' flagreader

COPY ./flag.txt /flag.txt

CMD timeout 3m socat tcp-listen:1337,reuseaddr,fork exec:/tcp_bluetooth.sh,nofork,su=nobody
