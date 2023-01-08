#!/bin/bash

sleep 10 && lpadmin -p rwctf -E -v beh:/1/3/5/socket://printer:9100 &
/usr/sbin/cupsd -f -C /etc/cups/cupsd.conf -s /etc/cups/cups-files.conf 
