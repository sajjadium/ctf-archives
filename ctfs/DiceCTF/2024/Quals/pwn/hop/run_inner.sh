#!/bin/sh

echo "Send your exploit, followed by 'EOF'"
input=""
while IFS= read -r line; do
    if [ "${line}" = "EOF" ]; then
        break
    fi
    echo "${line}" >> /tmp/exploit.js
done
/app/js /tmp/exploit.js

