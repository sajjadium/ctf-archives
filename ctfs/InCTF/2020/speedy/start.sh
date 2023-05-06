#!/bin/sh
/etc/init.d/xinetd start;
tail --retry -s 1 -f /var/log/xinetd
sleep infinity;
