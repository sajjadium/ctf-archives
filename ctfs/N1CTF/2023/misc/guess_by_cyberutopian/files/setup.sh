#!/bin/sh
cd /files
useradd -m ctf

mv ctf.xinetd /etc/xinetd.d/ctf

mv start.sh /
mv flag /
mv readflag /

mv * /home/ctf

chown root:root /start.sh /etc/xinetd.d/ctf /home/ctf/* /flag /readflag
chmod 755 /start.sh /etc/xinetd.d/ctf /home/ctf/*
chmod 400 /flag
chmod 4555 /readflag

rmdir /files