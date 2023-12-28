#!/bin/sh

IFNAME=$1
NETNSPID=$2

#echo "Delete device"
ip link del ${IFNAME} || true
echo "Add device" ${IFNAME} ${NETNSPID}
ip link add ${IFNAME} type vxcan peer name vcan0 netns $NETNSPID
ip link set ${IFNAME} mtu 72
ip link set up ${IFNAME}
nsenter -t $NETNSPID -n ip link set vcan0 up

tc qdisc replace dev ${IFNAME} root tbf rate 16kbit latency 100ms burst 2000
