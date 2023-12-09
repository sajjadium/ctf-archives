#!/bin/sh
set -e

if [ ! -f /flag ]; then
	echo $FLAG > /flag
	chown root:root /flag && chmod 0600 /flag
	chmod u+s /readflag && chmod +x /readflag
fi
export FLAG=

su clickhouse -m -c 'JDBC_BRIDGE_HOME=/app PATH=$JAVA_HOME/bin:$PATH /app/docker-entrypoint.sh' &
/entrypoint.sh
