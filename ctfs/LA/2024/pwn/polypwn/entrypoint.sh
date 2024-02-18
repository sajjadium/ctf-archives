#!/bin/sh

mount binfmt_misc -t binfmt_misc /proc/sys/fs/binfmt_misc
mount --bind /proc /srv/proc
chroot /srv update-binfmts --enable qemu-mips64
chroot /srv update-binfmts --enable qemu-arm
umount /srv/proc
exec /jail/run
