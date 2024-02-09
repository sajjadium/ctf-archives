#!/bin/bash

# Define colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# ASCII banner
BANNER="
 ${RED}_____                  ___  ___                   ${NC}
${RED}|_   _|                 |  \/  |                   ${NC}
  ${GREEN}| | ___ _ __ _ __ __ _| .  . | ___  _____      __ ${NC}
  ${GREEN}| |/ _ \ '__| '__/ _\` | |\/| |/ _ \/ _ \ \ /\ / / ${NC}
  ${YELLOW}| |  __/ |  | | | (_| | |  | |  __/ (_) \ V  V /  ${NC}
  ${YELLOW}\_/\___|_|  |_|  \__,_\_|  |_/\___|\___/ \_/\_/   ${NC}
"
echo -e "$BANNER"
echo -e "${YELLOW}[+] Welcome challenger to the epic IAC Madness${NC}"
python3 challenge.py