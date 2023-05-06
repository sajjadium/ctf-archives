#!/bin/sh

/etc/init.d/xinetd start;
trap : TERM INT; sleep infinity & wait
