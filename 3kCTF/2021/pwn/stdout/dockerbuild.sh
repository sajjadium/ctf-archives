#!/bin/sh

# run as root.
sudo docker build -t stdout .
sudo docker run --name stdout -p 9998:9998 -d stdout

echo "-----------------------------------------------------------"
echo "Now you can connect to the challenge ex (nc 127.0.0.1 9998)"
echo "-----------------------------------------------------------"
