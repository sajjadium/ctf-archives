#!/bin/sh
trap 'umount /chroot/mnt' EXIT

runuser -u ctf /d3fuse /chroot/mnt && \
chroot --userspec=1000:1000 /chroot /bin/timeout -k 5 300 /bin/sh
