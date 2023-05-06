#!/bin/sh

set -eu

bits=26
nonce=$(head -c12 /dev/urandom | base64)

echo Send the output of: hashcash -mb$bits $nonce

if head -n1 | hashcash -cqb$bits -df /dev/null -r "$nonce"; then
	exec /opt/launch.sh
else
	echo Stamp verification failed
fi
