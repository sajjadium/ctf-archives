#!/bin/bash
docker kill qemu;docker rm qemu;
docker build -t qemu-uusb .
docker run --privileged --name qemu -it -p 1337:1234 qemu-uusb
