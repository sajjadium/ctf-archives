#!/bin/sh

# run as root.
sudo docker build -t masterc .
sudo docker run --name masterc -p 9999:9999 -d masterc
echo "-----------------------------------------------------------"
echo "Now you can connect to the challenge ex (nc 127.0.0.1 9999)"
echo "-----------------------------------------------------------"
