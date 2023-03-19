#!/bin/bash

IMG="disk.img"
SUBDIRS="kernel"
KERNEL="kernel/kernel.bin"

cd $(dirname $0)

for SUBDIR in $SUBDIRS
do
	if ! $SUBDIR/build.sh $1
	then
		echo "$SUBDIR build failed"
		exit 1
	fi
done

if [[ $1 != sysroot ]] && [[ $1 != clean ]] && [[ $1 != fmt ]]
then
	if [[ $KERNEL -nt $IMG ]]
	then
		./gen-img.sh $KERNEL $IMG
	fi
fi
