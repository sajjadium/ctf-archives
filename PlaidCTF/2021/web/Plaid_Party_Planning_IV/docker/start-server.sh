#!/bin/sh

# configure authentication
#
if [ "${NOPROTECT:-no}" = "yes" ]; then
	sed -i /auth_basic/d /etc/nginx/conf.d/default.conf
else 
    htpasswd -bc /etc/nginx/.htpasswd ppp "$(cat /run/secrets/ppp-basic-auth)"
fi

# start both processs and ensure the container exits as soon as either one of them does

nginx -g 'daemon off;' & pid=$!
{ /pppiv/pppiv.exe -docroot /usr/share/nginx/html -port 8000 -db "$DBURL"; kill $pid; } &
trap "kill -QUIT %1 %2" EXIT

wait %1
kill -QUIT %1 %2