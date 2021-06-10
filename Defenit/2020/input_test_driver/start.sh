#!/bin/bash

# inspired by d0now's belluminar script

echo "Enter the url for your exploit (max: 3MB)"
echo "It will be saved in /exp"
echo "Use mediafire, etc. to upload exploit"
echo -n "URL : "
read EXP_LINK

if [ ! -d tmp ] ; then
    mkdir tmp;
fi

cd tmp

    RANDOM_SUFIX=$(mktemp -u XXXXXXXXXX)
    ROOTFS_NAME=rootfs."$RANDOM_SUFIX"
    mkdir $ROOTFS_NAME
    cd $ROOTFS_NAME ; cpio -id -v < ../../rootfs.cpio 2>/dev/null ; cd ..

    if [ -n "EXP_LINK" ] ; then
        curl --max-filesize 3m $EXP_LINK -o $ROOTFS_NAME/exp
        chmod 755 $ROOTFS_NAME/exp
        if [ $? -ne 0 ] ; then
            rm -dR $ROOTFS_NAME
            exit;
        fi
        cd $ROOTFS_NAME ; find . | cpio -o --format=newc > ../$ROOTFS_NAME.cpio 2>/dev/null ; cd ..
        rm -dR $ROOTFS_NAME
    fi

cd ..

qemu-system-x86_64 \
-m 64M \
-kernel ./bzImage \
-initrd ./tmp/"$ROOTFS_NAME".cpio  \
-append 'root=/dev/ram rw console=ttyS0 oops=panic panic=1 quiet kaslr' \
-netdev user,id=t0, -device e1000,netdev=t0,id=nic0 \
-nographic  \
-cpu qemu64,smep \
-smp 1 \

rm ./tmp/"$ROOTFS_NAME".cpio
