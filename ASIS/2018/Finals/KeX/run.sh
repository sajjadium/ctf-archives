qemu-system-mipsel -m 64 -kernel vmlinux -hda rootfs.ext2 -monitor /dev/null -nographic  -append "root=/dev/hda console=/dev/ttyS0"
