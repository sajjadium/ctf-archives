#! /bin/sh
if [ ! -d /dev/net ];then
    mkdir /dev/net
    mknod /dev/net/tun c 10 200
fi

if [ -z "$ROUTE_NET" ];then
    ROUTE_NET="10.1.1.0/24"
fi

#echo 1 > /proc/sys/net/ipv4/ip_forward
iptables -t nat -A POSTROUTING -d $ROUTE_NET -j MASQUERADE
iptables -P FORWARD ACCEPT

cd /app
./sslvpnd -t 4 -i 172.31.0.1/16 -r $ROUTE_NET -k ./cert/ca.crt -c ./cert/cert.pem




