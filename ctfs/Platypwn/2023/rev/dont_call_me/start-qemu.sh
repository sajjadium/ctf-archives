#!/bin/ash

if [ -z $FLAG_LOCATION_PHYS ]; then
    echo "Please set the FLAG_LOCATION_PHYS environment variable."
    exit 1
fi

if [ -z $FLAG ]; then
    echo "Please set the FLAG environment variable."
    exit 1
fi

bootfile=$(mktemp)
echo "$FLAG" > $bootfile
touch /dev/shm/qemu-ram
truncate -s 0 /dev/shm/qemu-ram
truncate -s 64M /dev/shm/qemu-ram
dd "if=$bootfile" of=/dev/shm/qemu-ram "seek=$FLAG_LOCATION_PHYS" conv=notrunc bs=1 2>/dev/null
rm $bootfile

exec qemu-system-x86_64 \
    -drive file=os.img,media=disk,format=raw \
    -M pc \
    -machine memory-backend=pc.ram \
    -object memory-backend-file,id=pc.ram,size=64M,mem-path=/dev/shm/qemu-ram,share=on,dump=on \
    -nographic \
    -chardev stdio,id=char0,signal=off -serial chardev:char0 \
    -net none \
    -monitor none
