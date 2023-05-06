DIR="$(dirname "$(readlink -f "$0")")"
qemu-system-x86_64 -monitor /dev/null \
    -cpu max,+smap,+smep,check \
    -m 64 -nographic \
    -kernel "$DIR/bzImage" \
    -initrd "$DIR/initramfs.cpio.gz" \
    -append "console=ttyS0 init='/init'"
