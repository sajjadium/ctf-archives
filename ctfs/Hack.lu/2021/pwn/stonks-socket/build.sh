#!/bin/sh

pushd "module"
sudo docker build -t stonks-builder .

if !(sudo docker run --name stonks-builder -v "$PWD:/pwd" stonks-builder make -C /pwd); then
    sudo docker rm stonks-builder
    echo "kernel module build failed"
    exit
fi
sudo docker cp stonks-builder:/pwd/stonks_socket.ko ../
sudo docker cp stonks-builder:/boot/vmlinuz-5.11.0-38-generic ../
sudo docker rm stonks-builder
popd

