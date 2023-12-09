#!/bin/bash

# please figure out the real flag.

if [ $# != 1 ]; then
    echo "Use: bash $0 flag{00000000000000000000000000000000}"
    exit 0
fi
FLAG=$1

if [ -f "flagchecker.js" -a -f "node" ]; then
    cmd1=$(shasum ./node | grep 0d764e25cde6f7a7832acd2f225d289bc62a683e)
    cmd2=$(shasum ./flagchecker.js | grep 3b6da8d3bf840566d6408b1102a03a3b0111e325)
    if [ "$cmd1" == "" -o "$cmd2" == "" ]; then
        echo "File compromised"
        exit 0
    fi
    ./node ./flagchecker.js $FLAG
else
    echo "No such files"
    exit 0
fi
