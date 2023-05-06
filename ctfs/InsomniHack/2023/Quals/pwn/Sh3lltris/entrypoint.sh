#! /bin/sh

shell=$(echo $1 | base64 -d)
./shellcode $shell
sleep 2
