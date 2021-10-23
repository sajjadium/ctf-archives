#!/bin/bash
ip link add veth0 type veth peer veth1
ip addr add 10.0.4.1/24 dev veth0
ip link set up veth0
ip link set up veth1
echo 1 > /proc/sys/net/ipv4/ip_forward

NUM_SERVERS="${CHALL_NUM_SERVERS:-5}"
PORT_BASE="${CHALL_PORT_BASE:-7000}"
for i in $(seq 1 $NUM_SERVERS); do
  NUM=$((i + 1))
  PORT=$((NUM + PORT_BASE))
  iptables -A FORWARD -i eth0 -o veth0 -p tcp -d 10.0.4.$NUM --dport 8000 -m state --state ESTABLISHED,RELATED -j ACCEPT
  iptables -A PREROUTING -t nat -p tcp -i eth0 --dport $PORT -j DNAT --to-destination 10.0.4.$NUM:8000
  iptables -A POSTROUTING -t nat -o eth0 -j MASQUERADE

done
source /venv/bin/activate
python3 /server.py
