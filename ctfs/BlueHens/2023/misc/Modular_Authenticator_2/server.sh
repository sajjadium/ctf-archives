#!/bin/bash
which socat > /dev/null 2> /dev/null
if [[ $? == 0 ]]
then
    socat TCP-LISTEN:3000,fork,reuseaddr "EXEC:python3 server.py"
else
    echo "Please install socat. Try sudo apt update && sudo apt install socat."
    exit 1
fi
