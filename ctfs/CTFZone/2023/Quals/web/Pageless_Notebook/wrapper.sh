#!/bin/bash
set -m

chmod 744 /tmp/flag.txt 
su appuser -c 'fastcgi-mono-server /applications=/:/app/ /socket=tcp:127.0.0.1:9000 -v' &
/etc/init.d/nginx start
fg %1