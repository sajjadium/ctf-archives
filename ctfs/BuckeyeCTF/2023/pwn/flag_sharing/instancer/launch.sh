#!/bin/bash

iptables -S FORWARD | grep $1 | grep NEW | cut -d " " -f 2- | xargs -rL1 iptables -D
iptables -A FORWARD -i eth0 -s $3 -o $2 -p tcp -d $1 --dport 5000 -m state --state NEW -j ACCEPT
docker run --rm -d --network $4 --ip $1 --network-alias chal --privileged $5
