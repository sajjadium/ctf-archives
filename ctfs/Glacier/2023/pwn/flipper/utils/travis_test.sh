#!/bin/bash

HDD_IMAGE="SWEB.qcow2"


echo "Building architecture $1"
yes | make $1
make

echo "Running architecture $1"

rm -rf /tmp/qemu.in /tmp/qemu.out /tmp/qemu /tmp/out.log
mkfifo -m a=rw /tmp/qemu.in
mkfifo -m a=rw /tmp/qemu.out

if [[ "$1" == "x86_64" ]]; 
then
    qemu-system-x86_64 -m 8M -drive file=${HDD_IMAGE},index=0,media=disk -cpu qemu64 -debugcon file:/tmp/out.log -monitor pipe:/tmp/qemu -nographic -display none > /dev/null 2> /dev/null &
fi
if [[ "$1" == "x86_32" ]] || [[ "$1" == "x86_32_pae" ]]; 
then
    qemu-system-i386 -m 8M -drive file=${HDD_IMAGE},index=0,media=disk -cpu qemu64 -debugcon file:/tmp/out.log -monitor pipe:/tmp/qemu -nographic -display none > /dev/null 2> /dev/null &
fi
if [[ "$1" == "arm_rpi2" ]]; 
then
    exit 0 # not supported in the travis qemu
    qemu-system-arm -kernel kernel.x -cpu arm1176 -m 512 -M raspi2 -no-reboot -drive if=sd,file=${HDD_IMAGE} -serial file:/tmp/out.log -d guest_errors,unimp -monitor pipe:/tmp/qemu -nographic -display none > /dev/null 2> /dev/null &
    sleep 2
fi
if [[ "$1" == "arm_icp" ]]; 
then
    qemu-system-arm -M integratorcp -m 8M -kernel kernel.x -sd ${HDD_IMAGE} -no-reboot -serial file:/tmp/out.log -d guest_errors,unimp -monitor pipe:/tmp/qemu -nographic -display none > /dev/null 2> /dev/null &
fi
if [[ "$1" == "armv8_rpi3" ]];
then
    if [[ $(qemu-system-aarch64 -machine help | grep raspi3 | wc -l) != "0" ]]; then
        qemu-system-aarch64 -M raspi3 -cpu cortex-a53 -m 1024 -drive file=SWEB-flat.vmdk,if=sd,format=raw -no-reboot -kernel kernel.x -serial file:/tmp/out.log -d guest_errors,unimp -monitor pipe:/tmp/qemu -nographic -display none  > /dev/null 2> /dev/null  &
        sleep 10
    else
        echo "QEMU version is too old to support the raspberry pi 3"
        exit 0
    fi
fi


sleep 2
echo "sendkey kp_enter" > /tmp/qemu.in
sleep 3
echo "sendkey h" > /tmp/qemu.in
echo "sendkey e" > /tmp/qemu.in
echo "sendkey l" > /tmp/qemu.in
echo "sendkey p" > /tmp/qemu.in
echo "sendkey kp_enter" > /tmp/qemu.in
sleep 2
echo "quit" > /tmp/qemu.in

HAS_SHELL=$(grep -c "SWEB: />" /tmp/out.log)
HAS_HELP=$(grep -c "Command Help" /tmp/out.log)

if [[ $HAS_SHELL > 0 ]] && [[ $HAS_HELP > 0 ]]; 
then
    echo "SWEB boots and has a (working) shell"
    exit 0
fi

if [[ $HAS_SHELL > 0 ]] && [[ $HAS_HELP == 0 ]];
then
    echo "SWEB boots but has no working shell"
    exit 0
fi

if [[ $HAS_SHELL == 0 ]];
then
    echo "SWEB does not boot to a shell"
    exit 1
fi
