#! /bin/sh

nohup sh -c "qemu-system-x86_64 -m 256 -smp 2 -kernel /bzImage  -initrd /rootfs.cpio -nic type=user,hostfwd=tcp::12345-:12345,hostfwd=udp::1337-:1337 -append "console=ttyS0" -nographic" &

sleep infinity
