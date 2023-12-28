#!/bin/env bash

IFNAME=$1

ip link add dev ${IFNAME} type vcan
ip link set ${IFNAME} mtu 72
ip link set up ${IFNAME}

tc qdisc replace dev ${IFNAME} root tbf rate 16kbit latency 100ms burst 2000
