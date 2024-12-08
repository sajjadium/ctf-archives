#!/bin/bash
PORT=${1:-5000}
DISK=${2:-ZealOS_fake_flag.qcow2}
qemu-system-x86_64 -monitor none -machine q35,accel=kvm -m 2G -smp 1 -rtc base=localtime -nic user,model=pcnet,hostfwd=tcp::$PORT-:9002 -hda $DISK $3
