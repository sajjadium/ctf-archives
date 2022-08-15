#!/bin/sh

qemu-system-x86_64 \
    -m 1G \
    -nographic \
    -no-reboot \
    -kernel bzImage \
    -append "console=ttyS0 root=/dev/sda quiet loglevel=3 rd.systemd.show_status=auto rd.udev.log_level=3 oops=panic panic=-1 net.ifnames=0 pti=on" \
    -hda coros.qcow2 \
    -snapshot \
    -monitor /dev/null \
    -cpu qemu64,+smep,+smap,+rdrand \
    -smp cores=4 \
    --enable-kvm
