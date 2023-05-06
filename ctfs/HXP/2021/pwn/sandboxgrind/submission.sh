#!/bin/bash

set +B -feu -o pipefail
umask go=

echo '                     _ _                         _           _ '
echo '                    | | |                       (_)         | |'
echo ' ___  __ _ _ __   __| | |__   _____  ____ _ _ __ _ _ __   __| |'
echo '/ __|/ _` | ´_ \ / _` | ´_ \ / _ \ \/ / _` | ´__| | ´_ \ / _` |'
echo '\__ \ (_| | | | | (_| | |_) | (_) >  < (_| | |  | | | | | (_| |'
echo '|___/\__,_|_| |_|\__,_|_.__/ \___/_/\_\__, |_|  |_|_| |_|\__,_|'
echo '                                       __/ |                   '
echo '                                      |___/                    '
echo ''
echo 'Submit base64-encoded executables, end with EOF'

BINARY="$(mktemp --suffix="$(< /dev/urandom tr -dc a-zA-WYZ0-9 | head -c 24)")"
function cleanup {
    rm -f -- "${BINARY}"
}
trap cleanup EXIT

# Keep unredirected stdout for error messages
exec {OUT}>&1

# Decode the input
sed '/^$/q' 2>&${OUT} <&0 | base64 -d 2>&${OUT} >"${BINARY}"
echo "Thank you, running your binary now. (sha256: $(sha256sum "${BINARY}" | sed 's/[^0-9a-f].*//'))"
chmod +x "${BINARY}"

# Run in the sandbox
/sandboxgrind/bin/valgrind --vgdb=no --quiet --tool=sandboxgrind ${BINARY} 2>&${OUT}

echo 'Done.'
