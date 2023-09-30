#!/bin/bash

set -e
set -x

echo 1 > /proc/sys/net/ipv4/ip_forward

NUM_SERVERS="${CHAL_NUM_SERVERS:-5}"
PORT_BASE="${CHAL_PORT_BASE:-7000}"
export CHAL_NET_PREFIX="chal-nsjail-net-"
for i in $(seq 1 $NUM_SERVERS); do
  NUM=$((i + 1))
  PORT=$((NUM + PORT_BASE))
  NET="$CHAL_NET_PREFIX$NUM"
  docker network rm $NET || true
  docker network create --internal --subnet=10.0.$NUM.0/24 --gateway=10.0.$NUM.1 $NET
  docker network connect --ip 10.0.$NUM.2 $NET $HOSTNAME --alias router2

  iptables -A FORWARD -i eth0 -o eth$i -p tcp -d 10.0.$NUM.3 --dport 5000 -m state --state ESTABLISHED,RELATED -j ACCEPT
  iptables -A PREROUTING -t nat -p tcp -i eth0 --dport $PORT -j DNAT --to-destination 10.0.$NUM.3:5000
  iptables -A POSTROUTING -t nat -o eth$i -j MASQUERADE
done

docker rm -f $(docker ps -a -q --filter ancestor=$CHAL_IMAGE_NAME --format="{{.ID}}") || true
source venv/bin/activate
python3 ./server.py
