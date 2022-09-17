#!/bin/sh
if [ ! -f /flag ]; then
	echo $FLAG > /flag
	chown root:root /flag && chmod 0600 /flag
	chmod u+s /readflag && chmod +x /readflag
fi

export FLAG=
chmod -R 0777 /app/standalone/deployments
chmod -R 0777 /app/standalone/data/content
su ctf -c '/app/bin/standalone.sh -b 0.0.0.0 &'
while :
do
	sleep 1
	(curl 127.0.0.1:8080/app/ | grep Hello) && chmod -R 0755 /app/standalone/deployments && chmod -R 0755 /app/standalone/data/content && break
done

nginx
tail -f /var/log/nginx/access.log
