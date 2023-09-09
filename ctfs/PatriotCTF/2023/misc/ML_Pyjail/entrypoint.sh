#! /bin/bash

PORT=4444
EXEC="./MLjail/app.py"
while :
do
    socat TCP-LISTEN:$PORT,reuseaddr,fork EXEC:"$EXEC,stderr"
done
