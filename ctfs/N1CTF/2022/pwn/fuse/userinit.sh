#!/bin/sh
export PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
mkdir /proc
mkdir /dev
mount -t proc proc /proc
mount -t devtmpfs devfs /dev
/spawner -e -s 1001 /usr/bin/fuse_server /work & # run as fuse user
cd /work
mkdir usr
mount --bind -o ro /usr usr
mkdir etc
mount --bind -o ro /etc etc
ln -s ./usr/bin ./bin
ln -s ./usr/sbin ./sbin
ln -s ./usr/lib ./lib
ln -s ./usr/lib64 ./lib64
ln -s ./usr/lib32 ./lib32

mkdir -p home/ctf # place your exp here
mount -t tmpfs -o uid=1000,gid=1000,mode=777,size=8M none home/ctf

echo "I will give you a shell.."
/spawner -e -d 83886080 -u -r -f 5 -c /work /bin/bash # inherit environ , run as random user , RLIM_DATA=80M , MAX NPROC=5 , chroot /work , PR_SET_NO_NEW_PRIVS