#!/bin/sh
mkdir /flag
echo 'corctf{flag}' > /flag/$(head /dev/urandom | tr -dc a-z | head -c 8).txt
genisoimage -o /opt/flag.iso /flag/*
qemu-system-x86_64 -smp 6 -m 8G -cpu host,hv_relaxed,hv_vapic,hv_spinlocks=0x1fff,hv_time,hv_reset,hv_runtime,hv_synic,hv_stimer,hv_tlbflush,hv_ipi,hv_vpindex -enable-kvm -drive file=/mnt/boxman/windows.qcow2,if=ide -drive file=/opt/flag.iso,media=cdrom,readonly=on -net nic -net user,hostfwd=tcp:0.0.0.0:8080-10.0.2.15:8080 -nographic -serial none -monitor none -snapshot