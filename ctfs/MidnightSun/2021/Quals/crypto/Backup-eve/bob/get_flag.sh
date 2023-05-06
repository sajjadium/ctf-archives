#!/bin/sh
openssl enc -aes-256-cbc -d -k $(cat ../password.bob) -in flag.enc 2>/dev/null
