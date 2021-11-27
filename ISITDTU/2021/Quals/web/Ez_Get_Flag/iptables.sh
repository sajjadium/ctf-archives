#!/bin/bash
IPT="/usr/sbin/iptables"

echo "Set default policy to 'DROP'"
$IPT -P INPUT   DROP
$IPT -P FORWARD DROP
$IPT -P OUTPUT  DROP

echo "Allowing new and established incoming connections to port 5000"
$IPT -A INPUT  -p tcp -m multiport --dports 5000 -m state --state NEW,ESTABLISHED -j ACCEPT
$IPT -A OUTPUT -p tcp -m multiport --sports 5000 -m state --state ESTABLISHED     -j ACCEPT

exit 0