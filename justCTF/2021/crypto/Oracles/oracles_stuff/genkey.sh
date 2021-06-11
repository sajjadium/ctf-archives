#!/bin/bash

ssh-keygen -b 1024 -t rsa -m PEM -f ./key -q -N "" <<< y
openssl asn1parse -i -dump -in ./key | tail -n +3 | cut -d: -f 4 > ./key_parsed
mv ./key_parsed key
rm ./key.pub
