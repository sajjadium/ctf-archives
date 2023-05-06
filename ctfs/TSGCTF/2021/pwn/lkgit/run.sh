qemu-system-x86_64 \
  -kernel ./bzImage \
  -initrd ./rootfs.cpio \
  -nographic \
  -monitor /dev/null \
  -cpu kvm64,smep,smap \
  -append "console=ttyS0 kaslr oops=panic panic=1 quiet" \
  -no-reboot \
  -m 256M