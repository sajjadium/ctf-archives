#!/bin/bash

pow(){
    difficulty=$1
    if [ $difficulty -gt 60 ]; then
        echo 'too hard'
        exit
    fi
    chalprefix=$(hexdump -n 8 -e '2/4 "%08x" 1 "\n"' /dev/urandom)
    echo "sha256($chalprefix+???) == $(printf '0%.0s' $(seq 0 $difficulty))($difficulty)..."
    printf "> "
    read -t 600 answer
    res=$(printf "$chalprefix$answer"|sha256sum|awk '{print $1}'|cut -c1-15|tr [a-f] [A-F])
    rshift=$((60-$difficulty))
    res=$(echo "obase=10; ibase=16; $res" | bc)
    if [ $(($res>>$rshift)) -ne 0 ]; then
        echo 'POW failed'
        exit
    else
        echo 'POW passed'
    fi
}

prepare_env(){
    WORKDIR=`mktemp -d -p "/tmp/"`
    mkdir -p $WORKDIR/lib/x86_64-linux-gnu/
    mkdir -p $WORKDIR/lib64/
    mkdir -p $WORKDIR/usr/bin
    mkdir -p $WORKDIR/home/HouseofCats/writable/
    cp /lib/x86_64-linux-gnu/libc-2.31.so $WORKDIR/lib/x86_64-linux-gnu/libc.so.6
    cp /lib/x86_64-linux-gnu/ld-2.31.so $WORKDIR/lib64/ld-linux-x86-64.so.2
    cp /lib/x86_64-linux-gnu/libpthread-2.31.so $WORKDIR/lib/x86_64-linux-gnu/libpthread.so.0
    cp /lib/x86_64-linux-gnu/librt-2.31.so $WORKDIR/lib/x86_64-linux-gnu/librt.so.1
    cp /usr/bin/timeout $WORKDIR/usr/bin/timeout
    cp /home/HouseofCats/house_of_cats $WORKDIR/home/HouseofCats/house_of_cats
    chmod -R 555 $WORKDIR
    chmod 777 $WORKDIR/home/HouseofCats/writable/
}

exec 2>/dev/null

pow 22

prepare_env
chroot --userspec=HouseofCats:HouseofCats $WORKDIR timeout 900 /home/HouseofCats/house_of_cats
RES=`head -c 10 $WORKDIR/home/HouseofCats/writable/check`

if [ $RES = "asimplechk" ];
then
    echo "Check passed"
    cp /home/HouseofCats/flag $WORKDIR/home/HouseofCats/flag
    chroot --userspec=HouseofCats:HouseofCats $WORKDIR timeout 900 /home/HouseofCats/house_of_cats
else
    echo "Check failed"
fi
rm -fr $WORKDIR
