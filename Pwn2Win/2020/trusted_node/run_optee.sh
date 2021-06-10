#!/bin/bash

PORT1=$1
PORT2=$2

function help {
	echo "USAGE: ./run_optee.sh PORT1 PORT2"
        echo "tip: listen with \"nc -l PORT\" for each port"
	exit 1
}

if [[ -z $PORT1 ]]
then
	help
fi

if [[ -z $PORT2 ]]
then
        help
fi


cd optee_files

echo c | ./qemu-system-aarch64 \
        -nographic \
        -serial tcp:localhost:$PORT1 -serial tcp:localhost:$PORT2 \
        -smp 1 \
        -S -machine virt,secure=on -cpu cortex-a57 \
        -d unimp -semihosting-config enable,target=native \
        -m 580 \
        -bios bl1.bin \
        -initrd rootfs.cpio.gz \
        -kernel Image -no-acpi \
        -object rng-random,filename=/dev/urandom,id=rng0 -device virtio-rng-pci,rng=rng0,max-bytes=1024,period=1000 -netdev user,id=vmnic -device virtio-net-device,netdev=vmnic

