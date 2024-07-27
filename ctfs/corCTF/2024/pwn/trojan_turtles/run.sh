#!/bin/sh

qemu-system-x86_64 \
    -m 1024 \
    -nographic \
    -no-reboot \
    -kernel bzImage \
    -append "console=ttyS0 root=/dev/sda quiet loglevel=3 rd.systemd.show_status=auto rd.udev.log_level=3 panic=-1 net.ifnames=0 pti=off no5lvl" \
    -hda chall.qcow2 \
    -snapshot \
    -netdev user,id=net \
    -device e1000,netdev=net \
    -monitor /dev/null \
    -cpu host \
    -smp cores=2 \
    --enable-kvm
