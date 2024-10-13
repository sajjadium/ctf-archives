FROM ubuntu:focal AS builder

ARG DEBIAN_FRONTEND=noninteractive
RUN apt update  && apt install -y \
    build-essential cmake curl libmpfr-dev libmpc-dev libgmp-dev e2fsprogs \
    ninja-build qemu-utils ccache rsync genext2fs unzip wget \
    gcc-10 g++-10 libpixman-1-dev libgtk-3-dev git

RUN git clone https://github.com/SerenityOS/serenity /serenity \
    && cd /serenity && git checkout d8de352eadce62789a00f8d6da6c2e77903e9180

WORKDIR /serenity
RUN Meta/serenity.sh rebuild-toolchain

COPY disable_assertions.patch add_js_method.patch filesystem.patch /serenity/
RUN git apply disable_assertions.patch
RUN git apply add_js_method.patch
RUN git apply filesystem.patch
COPY flag.txt Base/flag.txt

RUN Meta/serenity.sh build
RUN Meta/serenity.sh image

RUN qemu-img convert -f raw -O qcow2 /serenity/Build/i686/_disk_image /serenity/Build/i686/disk.qcow2
CMD bash

FROM ubuntu:focal

ARG DEBIAN_FRONTEND=noninteractive
RUN apt update  && apt install -y qemu-system-i386 xinetd socat

COPY --from=builder /serenity/Build/i686/disk.qcow2 /serenity/disk.qcow2
COPY --from=builder /serenity/Build/i686/Kernel/Kernel /serenity/Kernel
COPY --from=builder /serenity/Build/i686/Kernel/Prekernel/Prekernel /serenity/Prekernel

WORKDIR /serenity/
COPY ctf.xinetd /etc/xinetd.d/ctf
COPY start.sh /start.sh
RUN useradd -ms /bin/bash ctf

EXPOSE 2323

CMD ["/bin/sh", "-c", "chmod +666 /dev/kvm && /usr/sbin/xinetd -dontfork"]
