# Copyright 2021 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

FROM busybox:musl as busybox-grab

FROM gentoo/stage3:amd64-musl-vanilla as gentoo-build

RUN emerge-webrsync

# We don't have CAP_PTRACE for this to function properly
RUN rm /usr/bin/sandbox

RUN USE=static emerge -v dev-util/strace
RUN USE='-* binary caps qemu seavgabios seccomp static static-libs static-user virtfs xattr qemu_softmmu_targets_x86_64 '"$(python --version | sed -r 's/Python ([0-9]+)\.([0-9]+)(\.([0-9]+))/python_targets_python\1_\2/')" emerge -v app-emulation/qemu

COPY src/ /tmp/

RUN gcc -static -Os /tmp/qemud.c -o /tmp/qemud
RUN gcc -static -Os /tmp/jail.c -o /tmp/jail
RUN gcc -static -Os /tmp/exploit_me.c -o /tmp/exploit_me
RUN gcc -static -Os /tmp/seccomp_loader.c -o /tmp/seccomp_loader

FROM ubuntu:20.04 as kernel-build

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y wget build-essential && \
    apt-get install -y gawk flex bison bc zstd && \
    apt-get install -y libncurses-dev libssl-dev libssl-dev libelf-dev libudev-dev libpci-dev libiberty-dev

RUN apt-get install -y gcc-$(gcc --version | grep -oP '([0-9]+)\.([0-9]+).([0-9]+)' | uniq | cut -d. -f1)-plugin-dev

RUN mkdir /kernel
RUN wget https://cdn.kernel.org/pub/linux/kernel/v5.x/linux-5.12.14.tar.xz -O /kernel/linux.tar.xz
RUN tar -C /kernel -xf /kernel/linux.tar.xz

RUN mkdir /initrd
RUN mkdir -p /initrd/bin /initrd/sbin /initrd/usr/bin /initrd/usr/sbin /initrd/usr/local/bin /initrd/usr/local/sbin

COPY src/init /initrd/init
RUN chmod 755 /initrd/init
COPY --from=busybox-grab /bin/busybox /initrd/bin/

COPY src/jail.c src/exploit_me.c src/seccomp_loader.c /initrd/usr/local/bin/
COPY src/flag /initrd/
COPY --from=gentoo-build /tmp/jail /tmp/exploit_me /tmp/seccomp_loader /initrd/usr/local/bin/

COPY --from=gentoo-build /usr/bin/strace /initrd/usr/bin/

COPY kernel/kconfig /kernel/linux-5.12.14/.config
COPY kernel/patch /tmp/kernel.patch
COPY kernel/CVE-2021-33909.patch /tmp/CVE-2021-33909.patch
RUN patch -p1 -d /kernel/linux-5.12.14 < /tmp/CVE-2021-33909.patch
RUN patch -p1 -d /kernel/linux-5.12.14 < /tmp/kernel.patch

RUN make -j$(nproc) -C /kernel/linux-5.12.14

FROM busybox:musl as chroot

RUN mkdir /home/user/

COPY --from=gentoo-build /tmp/qemud /home/user/

COPY --from=kernel-build /kernel/linux-5.12.14/arch/x86/boot/bzImage /home/user/

RUN mkdir /usr/share/

COPY --from=gentoo-build /usr/bin/qemu-system-x86_64 /usr/bin/
COPY --from=gentoo-build /usr/share/qemu /usr/share/qemu
COPY --from=gentoo-build /usr/share/seavgabios /usr/share/seavgabios
COPY --from=gentoo-build /usr/share/seabios /usr/share/seabios

RUN rm /usr/share/qemu/edk2-*

FROM gcr.io/kctf-docker/challenge@sha256:460914265211af5fd006c4ceb4d2628817e9645570033827cf8db136a540b54f

COPY --from=chroot / /chroot
RUN mkdir -p /chroot/proc

COPY nsjail.cfg /home/user/

CMD kctf_setup && \
    kctf_drop_privs \
    socat TCP-LISTEN:1337,reuseaddr,fork EXEC:'kctf_pow nsjail --config /home/user/nsjail.cfg -- /home/user/qemud /home/user/bzImage'
