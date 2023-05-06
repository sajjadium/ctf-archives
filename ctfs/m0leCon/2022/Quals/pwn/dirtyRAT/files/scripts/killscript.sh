#! /bin/bash

>&2 echo "Cleaning user $2 (PID=$1) in 60 seconds."
sleep 60
kill -9 $1
rm -rf /tmp/$2 && >&2 echo "User $2 (PID=$1) cleared."