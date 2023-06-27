FROM debian:10.8-slim as kernel_build
RUN apt-get update
RUN apt-get install -y \
    bc \
    bison \
    build-essential \
    cpio \
    flex \
    libelf-dev \
    libncurses-dev \
    libssl-dev \
    vim-tiny \
    curl
RUN curl -O https://cdn.kernel.org/pub/linux/kernel/v6.x/linux-6.1.35.tar.xz && tar -xvf linux-6.1.35.tar.xz && rm -rf linux-6.1.35.tar.xz
RUN apt-get install -y kmod
RUN cd linux-6.1.35 && \
    make defconfig && \
    make kvm_guest.config && \
    make -j16 && \
    make -j16 modules_install
RUN cd /linux-6.1.35 && make install

RUN mkdir -p /uaf_shield
RUN apt install -y cmake && apt clean
COPY / /uaf_shield
RUN cd /uaf_shield/kernel_driver && make KERNEL_VERSION=6.1.35
RUN cd /uaf_shield/ && mkdir -p build && cd build && cmake .. && cmake --build .


FROM ubuntu:22.04 as ubuntu_create_img
RUN apt update && apt install -y \ 
    qemu-utils \
    debootstrap \
    guestfs-tools && \
    apt clean

COPY --from=kernel_build /boot /boot
RUN mkdir -p /uaf_shield
COPY /build_qemu/* /uaf_shield/
COPY --from=kernel_build /uaf_shield/kernel_driver/uaf_shield.ko /uaf_shield
COPY --from=kernel_build /uaf_shield/build/uaf/uaf /uaf_shield
COPY --from=kernel_build /linux-6.1.35 /linux-6.1.35
COPY --from=kernel_build /lib/modules/6.1.35 /lib/modules/6.1.35
ENV OUTPUT_IMG=/uaf_shield/image.img
ENV MNT_DIR=/uaf_shield/qemu-file-system
RUN mkdir -p $MNT_DIR
ARG FLAG="BSidesTLV2023{DUMMY_FLAG}"
RUN debootstrap --arch amd64 --include=openssl,socat,kmod,sudo,xxd,procps,cron bullseye $MNT_DIR && \ 
    echo $FLAG > $MNT_DIR/usr/lib/flag.txt && \
    cp -r /uaf_shield/uaf $MNT_DIR/usr/bin/uaf && \
    chown root:root $MNT_DIR/usr/bin/uaf && \
    chmod +x $MNT_DIR/usr/bin/uaf && \
    mkdir -p $MNT_DIR/uaf_driver && \
    cp -r /uaf_shield/uaf_shield.ko $MNT_DIR/uaf_driver && \
    cp /uaf_shield/prepare_chrooted_system.sh $MNT_DIR/usr/local/bin && \
    chmod +x $MNT_DIR/usr/local/bin/prepare_chrooted_system.sh && \
    chroot $MNT_DIR /usr/local/bin/prepare_chrooted_system.sh && \
    rm $MNT_DIR/usr/local/bin/prepare_chrooted_system.sh && \
    SUPERMIN_KERNEL=/boot/vmlinuz-6.1.35 virt-make-fs --type=ext3 --format=qcow2 --size=1G $MNT_DIR $OUTPUT_IMG && \
    rm -rf $MNT_DIR

FROM alpine as run_qemu
COPY --from=kernel_build /boot /boot
RUN mkdir -p /uaf_shield
COPY --from=ubuntu_create_img /uaf_shield/image.img /uaf_shield/image.img
RUN apk add qemu-system-x86_64
CMD qemu-system-x86_64 \
    -nographic \
    -drive file=/uaf_shield/image.img,index=0,media=disk,format=qcow2 \
    -net nic -net user,hostfwd=tcp::8080-:8080 \
    -kernel /boot/vmlinuz-6.1.35 \
    -append "console=ttyS0 root=/dev/sda rw noresume" -m 2048 -smp 1 \
    -cpu qemu64,+la57
