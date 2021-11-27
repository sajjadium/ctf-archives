sudo qemu-system-x86_64 -M pc -m 512M -smp 1 \
    -enable-kvm -cpu host \
    -kernel bzImage \
    -append "root=/dev/vda console=ttyS0,115200n8" \
    -drive file=rootfs.ext2,format=raw,if=virtio \
    -nographic
