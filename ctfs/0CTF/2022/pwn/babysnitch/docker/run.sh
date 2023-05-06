#!/bin/bash

# Deny connection by default
sed -i "s/allow/deny/" /etc/opensnitchd/default-config.json 
sed -i "s/ACCEPT/DROP/" /etc/opensnitchd/system-fw.json 
systemctl start opensnitch
# Trigger your RCE!
chmod +x /home/test/test
su test -c /home/test/test
sleep 100
