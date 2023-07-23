#!/bin/sh

KERNEL_PATH="../bzImage"

if [ -z "$1" ]
then
    echo "NO CPIO"
    return 1
fi

if [ -z "$2" ]
then
    echo "No exploit found. Booting."
    qemu-system-x86_64 \
        -m 256M\
        -kernel $KERNEL_PATH \
        -initrd $1  \
        -cpu kvm64,+smep,+smap \
        -append "console=ttyS0 oops=panic panic=1 kpti=1 nokaslr quiet" \
        -monitor /dev/null \
        -serial mon:stdio \
        -virtfs local,path=/tmp,mount_tag=host0,security_model=passthrough,id=foobar \
        -nographic -s
else
    echo "Exploit found. Booting."
    echo "Compiled $2"
    gcc -static $2.c -o $2 -lpthread
    qemu-system-x86_64 -no-reboot \
        -m 256M\
        -kernel $KERNEL_PATH \
        -initrd $1  \
        -cpu kvm64,+smep,+smap \
        -append "console=ttyS0 oops=panic panic=1 kpti=1 kaslr quiet" \
        -drive file=$2,format=raw \
        -monitor /dev/null \
        -serial mon:stdio \
        -virtfs local,path=/tmp,mount_tag=host0,security_model=passthrough,id=foobar \
        -nographic -s
fi
