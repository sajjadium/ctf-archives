#!/bin/sh
set -e

if [ ! -f /flag ]; then
	echo $FLAG > /flag
	chown root:root /flag && chmod 0600 /flag
	chmod u+s /readflag && chmod +x /readflag
fi
export FLAG=

python3 /init_db.py &
su hive -m -c '/entrypoint.sh'
