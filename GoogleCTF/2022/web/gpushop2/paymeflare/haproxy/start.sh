#!/bin/bash

/tmp/haproxy/force-reload.sh & 
python3 /tmp/haproxy/update_pubkey.py & 
rm -rf /var/lib/haproxy/socket/dataplane.sock 
umask 111
haproxy -W -db -f /usr/local/etc/haproxy/haproxy.cfg

