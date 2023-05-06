#!/bin/sh
if [ -z "$1" ]
then
    echo "[+] ${0} <flag.txt>"
    exit 1
else
    clamscan --bytecode-unsigned=yes --quiet -dflag.cbc "$1"
    if [ $? -eq 1 ]
    then
        echo "Correct!"
    else
        echo "Wrong..."
    fi
fi
