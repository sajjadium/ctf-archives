qemu-system-x86_64 -m 128M -initrd initramfs.cpio.gz -kernel ./bzImage -nographic -monitor /dev/null -append "kpti=1 kaslr root=/dev/ram rw console=ttyS0 oops=panic paneic=1 quiet" -s 2>/dev/null
