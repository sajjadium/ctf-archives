#!/bin/sh

# Run admin
ynetd -p 6000 -lm -1 -lt 15 -t 30 -lpid 256 /home/ctf/admin.py &

# Start and wait for database
mysqld_safe &
while ! mysqladmin --silent ping; do sleep 0.1; done

# Dispatch to HackMD entrypoint
export CMD_AUTO_VERSION_CHECK=false
export CMD_DB_URL="mysql://hackmd:__DB_PASSWORD__@127.0.0.1:3306/hackmd"
export CMD_USECDN=false
export CMD_ALLOW_ANONYMOUS=true
export CMD_ALLOW_PDF_EXPORT=false
(while true; do su hackmd --login --whitelist-environment="CMD_AUTO_VERSION_CHECK,CMD_DB_URL,CMD_USECDN,CMD_ALLOW_ANONYMOUS,CMD_ALLOW_PDF_EXPORT" --command="cd /home/hackmd/app/ && exec /home/hackmd/app/docker-entrypoint.sh"; done) &

# Run nginx
nginx -g 'daemon off;'

