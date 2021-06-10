#!/bin/sh

# run as root.
sudo docker build -t iterrun .
sudo docker run --name iterrun -p 9997:9997 -d iterrun

echo "-----------------------------------------------------------"
echo "Now you can connect to the challenge ex (nc 127.0.0.1 9997)"
echo "-----------------------------------------------------------"
