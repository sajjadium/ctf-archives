#!/bin/bash
# set -x

cd /home/pwnbox
echo "Enter the link for your exploit (max: 3MB)"
echo "It will be saved in /home/user/exp"
echo -n "link : "
read  EXP_LINK

if [ ! -d tmp ] ; then mkdir tmp;fi
cd tmp

    RANDOM_SUFIX=$(mktemp -u XXXXXXXXXX)
    ROOTFS_NAME=rootfs."$RANDOM_SUFIX"
    mkdir $ROOTFS_NAME
    cd $ROOTFS_NAME ; cat ../../rootfs.img | gunzip | cpio --extract ; cd ..

    if [ -n "$EXP_LINK" ]; then
        curl  --max-filesize 3m  $EXP_LINK -o $ROOTFS_NAME/home/user/exp
        if [ $? -ne 0 ] ; then exit;fi
    fi

    cd $ROOTFS_NAME ; find . | cpio -o -H newc | gzip > ../$ROOTFS_NAME.img ; cd ..
    rm -dR $ROOTFS_NAME

cd ..

qemu-system-x86_64 \
        -enable-kvm \
        -cpu kvm64,+smep,+smap \
	-m 64 \
	-kernel bzImage \
	-nographic \
	-append "console=ttyS0 init=/init quiet" \
	-initrd tmp/"$ROOTFS_NAME".img \
	-monitor /dev/null
