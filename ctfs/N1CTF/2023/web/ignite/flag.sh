#!/bin/bash
echo ${FLAG} > /flag
chmod 600 /flag

export FLAG=not_flag
FLAG=not_flag

rm -f /flag.sh