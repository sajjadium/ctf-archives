#!/bin/bash
cd /tmp
dir_name=`tr -dc A-Za-z0-9 </dev/urandom | head -c 13`
mkdir $dir_name
while [ $? -ne 0 ]
do
    dir_name=`tr -dc A-Za-z0-9 </dev/urandom | head -c 13`
    mkdir $dir_name
done
sleep 60 && rm -rf $dir_name &
cd $dir_name
timeout 60 /chall
