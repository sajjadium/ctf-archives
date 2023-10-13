#!/bin/sh
iptables -P INPUT   DROP
iptables -P FORWARD DROP
iptables -P OUTPUT  DROP

iptables -A INPUT  -p tcp -m multiport --dports 8000 -m state --state NEW,ESTABLISHED -j ACCEPT
iptables -A OUTPUT -p tcp -m multiport --sports 8000 -m state --state ESTABLISHED     -j ACCEPT

gunicorn -b 0.0.0.0:8000 -w "${WORKER:-4}" 'server:app'