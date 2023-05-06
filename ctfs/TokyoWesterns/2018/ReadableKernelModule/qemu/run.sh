#!/bin/bash
qemu-system-x86_64 -kernel bzImage -m 64M -initrd rootfs.cpio -append "root=/dev/ram console=ttyS0 oops=panic panic=1 quiet kaslr" -nographic -monitor /dev/null -net user -net nic -device e1000 -smp cores=2,threads=2 -cpu kvm64,+smep,+smap 2>/dev/null
