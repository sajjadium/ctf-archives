#!/bin/sh

set -eu

bits=26
nonce=$(head -c12 /dev/urandom | base64)

cat <<EOF
Send the output of: hashcash -mb${bits} ${nonce}
EOF

if head -n1 | hashcash -cqb${bits} -df /dev/null -r "${nonce}"; then
	exec /home/ctf/app/launch.sh
else
	echo Stamp verification failed
fi
