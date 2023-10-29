#! /bin/bash

echo -n $(hexdump -n 16 -v -e '"0x" 32/1 "%02x" "\n"' /dev/urandom)