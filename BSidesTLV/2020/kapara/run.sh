#!/bin/bash

kernel=$1
hda=$2
echo "🍍 🛀   🍕"
if [ -z $kernel ]; then
	echo "pass the kernel argument 😮😮 😮😮"
	exit 1
fi

if [ -z $hda ]; then
	echo "pass the hda argument 🙄"
	exit 1
fi

qemu=(
    qemu-system-x86_64
    -kernel $kernel
    -m 2048
    -boot order=nc
    -watchdog i6300esb
    -rtc base=localtime
    -hda $hda
    -device e1000,netdev=net0
    -netdev user,id=net0,hostfwd=tcp::5555-:22
    -nographic
    -no-reboot
)

append=(
    hung_task_panic=1
    earlyprintk=ttyS0,115200
    debug
    apic=debug
    sysrq_always_enabled
    rcupdate.rcu_cpu_stall_timeout=100
    panic=-1
    softlockup_panic=1
    nmi_watchdog=panic
    load_ramdisk=2
    prompt_ramdisk=0
    console=tty0
    console=ttyS0,115200
    root=/dev/sda rw 
    drbd.minor_count=8
    noksalr
)

"${qemu[@]}" --append "${append[*]}"
