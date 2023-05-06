#!/bin/sh

exec 2>/dev/null
./linux rootfstype=hostfs rootflags=$(pwd)/fs r init=/init
