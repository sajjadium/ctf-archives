#!/bin/sh

cd /home
timeout 1m qemu-system-x86_64 -kernel bzImage -enable-kvm -no-reboot -m 32M --nographic -smp cores=1,threads=1 -cpu kvm64,+smep -append 'console=ttyS0 oops=panic panic=1'
