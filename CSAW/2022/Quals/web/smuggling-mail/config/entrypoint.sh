#!/usr/bin/env sh

sed -i "s/TOKEN/$(base64 < /dev/urandom | fold -w 64 | tr '/+' '_-' | head -n 1)/" /etc/varnish/varnish.vcl
/usr/bin/supervisord -c /etc/supervisor/supervisord.conf
