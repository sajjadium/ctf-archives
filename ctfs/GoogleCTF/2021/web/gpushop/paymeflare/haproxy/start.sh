#!/bin/bash

/tmp/haproxy/force-reload.sh & 
rm -rf /var/lib/haproxy/socket/dataplane.sock 
umask 111
haproxy -W -db -f /usr/local/etc/haproxy/haproxy.cfg

