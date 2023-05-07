#!/bin/bash

echo "$(cat pad.bin)$FLAG" > flag.bin
ls -alF ./pad.bin
x=$(openssl rand -hex 32)
echo $x
openssl enc -aes-256-cbc -K $x -iv $(openssl rand -hex 16) -in flag.bin -out ciphertext.bin
