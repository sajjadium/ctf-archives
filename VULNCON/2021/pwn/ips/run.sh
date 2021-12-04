qemu-system-x86_64 \
  -m 256M \
  -initrd initramfs.cpio.gz \
  -kernel ./bzImage -nographic \
  -monitor /dev/null \
  -append "kpti=1 +smep +smap kaslr root=/dev/ram rw console=ttyS0 oops=panic paneic=1 quiet"
