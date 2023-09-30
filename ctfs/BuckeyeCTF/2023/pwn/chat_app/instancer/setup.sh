#!/bin/bash

set -x
set -e

# This is setup for the instancer. Nothing in this file is supposed to be relevant to the solution.

# Server subnet
ip link add veth0 type veth peer veth1
ip addr add 10.0.4.1/24 dev veth0
ip link set up veth0
ip link set up veth1

# Client subnet
ip link add veth2 type veth peer veth3
ip addr add 10.0.5.1/24 dev veth2
ip link set up veth2
ip link set up veth3

echo 1 > /proc/sys/net/ipv4/ip_forward

NUM_SERVERS="${CHALL_NUM_SERVERS:-5}"
PORT_BASE="${CHALL_PORT_BASE:-7000}"
for i in $(seq 1 $NUM_SERVERS); do
  NUM=$((i + 1))
  PORT=$((NUM + PORT_BASE))
  iptables -A FORWARD -i eth0 -o veth0 -p tcp -d 10.0.4.$NUM --dport 8000 -m state --state ESTABLISHED,RELATED -j ACCEPT
  iptables -A PREROUTING -t nat -p tcp -i eth0 --dport $PORT -j DNAT --to-destination 10.0.4.$NUM:8000
  iptables -A POSTROUTING -t nat -o eth0 -j MASQUERADE

  # Allow traffic between matching client/server pairs (for the same team)
  iptables -A FORWARD -i veth2 -o veth0 -p tcp -s 10.0.5.$NUM -d 10.0.4.$NUM --dport 8000 -m state --state NEW,ESTABLISHED,RELATED -j ACCEPT
done

# Drop all other traffic between client/server pairs
iptables -A FORWARD -i veth2 -o veth0 -j DROP

# fix cgroupsv2 (see nsjail issue #196) -- this is not relevant to the challenge
mkdir /sys/fs/cgroup/tmp
echo "0" > /sys/fs/cgroup/tmp/cgroup.procs
echo "+memory +pids +cpu" > /sys/fs/cgroup/cgroup.subtree_control

source /venv/bin/activate
python3 server.py