#!/usr/bin/env bash
if [[ -z "$USERNAME" ]]; then
    USERNAME=$(</proc/sys/kernel/random/uuid)
fi
if [[ -z "$PASSWORD" ]]; then
    PASSWORD=$(</proc/sys/kernel/random/uuid)
fi
if [[ -z "$CHANNEL" ]]; then
    CHANNEL=$(</proc/sys/kernel/random/uuid)
fi
if [[ -z "$SERVER" ]]; then
    SERVER="http://localhost:3000"
fi

printf "[+] Bot initializing...\n"
printf "[-] Username: %s\n" "$USERNAME"
printf "[-] Password: %s\n" "$PASSWORD"
printf "[-] Channel: %s\n" "$CHANNEL"
printf "[-] Server: %s\n" "$SERVER"
jq -n --arg username "$USERNAME" --arg password "$PASSWORD" '{username: $username, password: $password}' > /tmp/credentials.json
printf "[+] Bot registering...\n"
curl "$SERVER/register" -X POST -H 'Content-Type: application/json' -d @/tmp/credentials.json
printf "\n"
rm /tmp/credentials.json
mkdir -p ~/.config/harmony
jq -n --arg username "$USERNAME" --arg password "$PASSWORD" --arg channel "$CHANNEL" --arg server "$SERVER" '{"channels":{($username):{($channel):true}},"serverUrl":$server,"defaultChannel":$channel,"auth":{"username":$username,"password":$password}}' > ~/.config/harmony/config.json

printf "[+] Bot starting...\n"
Xvfb :0 &
DISPLAY=:0 ./harmony --no-sandbox
