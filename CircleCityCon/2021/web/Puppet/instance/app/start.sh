#!/usr/bin/env sh
mkdir -p ~/Documents
echo $FLAG > ~/Documents/flag_`head -c 16 /dev/urandom | xxd -p | tr -d ' ' | tr -d '\n'`.txt
node app.js
