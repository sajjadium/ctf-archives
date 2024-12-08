#!/bin/bash
#socat TCP-LISTEN:1234,fork,reuseaddr system:
[[ $(pgrep -f qemu-system | wc -l) -ge 10 ]] && echo "Bathroom is occupied" && exit 1
export A=$(($$ % 55000 + 10000))
cp ZealOS.qcow2 ZealOS.qcow2$A
timeout -k 120 120  ./run_qemu.sh $A ZealOS.qcow2$A -nographic </dev/null >/dev/null & 
echo "Spinning up your temple... (god needs about 10 seconds to gather his thoughts)"
sleep 10
timeout -k 110 110 socat STDIN TCP:localhost:$A
wait
rm ZealOS.qcow2$A
