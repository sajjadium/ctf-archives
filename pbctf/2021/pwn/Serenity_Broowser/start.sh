#!/bin/bash

DIR=`mktemp -d`
SOCKET=$DIR/mon.sock
cd $DIR
cp /serenity/disk.qcow2 /serenity/Prekernel /serenity/Kernel ./

echo -n "Launching SerenityOS..."
timeout 120 qemu-system-i386 -m 512M -cpu max -d guest_errors -no-reboot -smp 1 \
    -drive file=disk.qcow2,format=qcow2,index=0,media=disk -snapshot \
    -debugcon file:debug.log -kernel Prekernel -initrd Kernel \
    -device e1000,netdev=net0 -netdev user,id=net0,hostfwd=tcp::0-:2323 \
    -nographic -enable-kvm -serial none -monitor "unix:$SOCKET,server,nowait" > /dev/null 2>&1 &
QEMU_PID=$!

function finish() {
    rm -rf "$DIR"
    kill $QEMU_PID > /dev/null 2>&1
}
trap finish EXIT

until [ -S "$SOCKET" ]
do
     sleep 1
     echo -n "."
done

PORT=$(echo "info usernet" | socat - "unix-connect:$SOCKET" | grep 2323 | tr -s ' ' | cut -d' ' -f5)
socat - TCP:127.0.0.1:$PORT
