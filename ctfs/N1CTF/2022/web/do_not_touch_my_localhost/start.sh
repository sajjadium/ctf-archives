#!/bin/bash

export networkAddr=$(ip route get 8.8.8.8 | head -1 | cut -d' ' -f7)
sed -i "s/{{networkAddr}}/$networkAddr/g" /app/proxy_blocker/manifest.json
echo $flag > /flag
chmod 700 /flag
unset flag
caddy start --config /caddy/Caddyfile
cd /app
su -c ./main app