#!/bin/bash

set -e

echo "bsidestlv2023" > /etc/hostname
printf "127.0.0.1    localhost.localdomain localhost\n127.0.1.1    bsidestlv2023\n" > /etc/hosts

useradd -p $(openssl passwd -1 bsides) --home /home/bsides -s /bin/bash bsides
mkdir /home/bsides
chown -R bsides:bsides /home/bsides/
cd /home/bsides

chmod -R 700 /home/bsides

usermod -aG sudo bsides

echo auto enp0s3 >> /etc/network/interfaces
echo iface enp0s3 inet dhcp >> /etc/network/interfaces

echo "@reboot su bsides -c \
'/bin/sh > \
/home/bsides/crontab.log 2>&1'" | crontab -u root -

(crontab -l ; echo "@reboot mount -o remount,rw,hidepid=2 /proc > \
/dev/null") | crontab -u root -

(crontab -l ; echo "@reboot /usr/sbin/insmod /uaf_driver/uaf_shield.ko > \
/dev/null") | crontab -u root -

(crontab -l ; echo "@reboot socat -t120 -T30 \"TCP4-LISTEN:8080,fork,reuseaddr\" \"EXEC:/usr/bin/uaf,pty,setuid=bsides,echo=0,raw,iexten=0\" & > \
/dev/null") | crontab -u root -

exit
