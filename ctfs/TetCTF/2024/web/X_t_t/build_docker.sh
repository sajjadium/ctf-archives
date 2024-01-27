#!/bin/bash
docker network create --subnet 172.19.0.0/16 net_1
sudo iptables --insert DOCKER-USER -s 172.19.0.0/16 -j REJECT --reject-with icmp-port-unreachable
sudo iptables --insert DOCKER-USER -s 172.19.0.0/16 -m state --state RELATED,ESTABLISHED -j RETURN
chal="${CHAL:-electron}"
docker rm -f "$chal"
docker build --tag="$chal" .
docker run -p 80:80 -d --network net_1 --rm --name="${chal}" "${chal}"
