#! /bin/sh


sudo tunctl -t tap100 -u nobody
sudo ifconfig tap100 10.10.10.2/24

sudo iptables -P FORWARD ACCEPT
sudo iptables -A INPUT -p icmp --icmp-type echo-request -j REJECT 
sudo iptables -t nat -I PREROUTING -p icmp -d 0.0.0.0/0 -j DNAT --to-destination 10.10.10.10
sudo iptables -t nat -I POSTROUTING -p icmp -d 10.10.10.10 -j SNAT --to-source 10.10.10.2
echo 1 | sudo tee /proc/sys/net/ipv4/ip_forward

while true;
do
    sudo rm -f /tmp/flag.txt
    sudo cp flag.txt /tmp
    sudo chmod 644 /tmp/flag.txt
    sudo chown nobody /tmp/flag.txt
    sudo setpriv --reuid=nobody --regid=netdev --init-groups \
        timeout 60 \
        qemu-system-i386 -cdrom kernel.iso \
        -hda /tmp/flag.txt \
        -netdev tap,id=n1,ifname=tap100,script=no,downscript=no \
        -device virtio-net-pci,netdev=n1,mac=01:02:03:04:05:06 \
        -m 64M -display none \
        -monitor /dev/null
    sleep 1
done


