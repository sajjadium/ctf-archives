#!/bin/sh
echo "[C(OOOO)RCPU]"
head -n 1 | base64 -d > /tmp/user_rom.rom
./cpu_entry
