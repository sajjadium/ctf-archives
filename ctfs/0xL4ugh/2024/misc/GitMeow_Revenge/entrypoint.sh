#!/bin/bash

# Define colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# ASCII banner
BANNER="
 ${RED}_____ _ _  ___  ___                   ${NC}
${RED}|  __ (_) | |  \/  |                   ${NC}
${GREEN}| |  \/_| |_| .  . | ___  _____      __ ${NC}
${GREEN}| | __| | __| |\/| |/ _ \/ _ \ \ /\ / / ${NC}
${YELLOW}| |_\ \ | |_| |  | |  __/ (_) \ V  V /  ${NC}
 ${YELLOW}\____/_|\__\_|  |_/\___|\___/ \_/\_/   ${NC}
"
echo -e "$BANNER"
echo -e "${YELLOW}[+] Welcome challenger to the epic GIT Madness, can you read${NC} ${RED}/flag.txt?${NC}"


# General configs
git config --global --add safe.directory /tmp
git config --global user.email "zAbuQasem@0xL4ugh.com"
git config --global user.name "zAbuQasem"

# Adding alot of files
i=1
while [ "$i" -le 1000 ]; do
  echo '0xl4ugh{f4k3_fl4g_f0r_n00b5}' > /tmp/$(head -n 10 /dev/urandom | md5sum | cut -d ' ' -f1).txt
  i=$((i + 1))
done

python3 challenge.py