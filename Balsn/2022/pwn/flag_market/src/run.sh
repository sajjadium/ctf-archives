#!/bin/bash

export LD_PRELOAD=/usr/local/lib/libpcsclite.so.1
exec 2>/dev/null
timeout 1800 /home/flag_market/flag_market
