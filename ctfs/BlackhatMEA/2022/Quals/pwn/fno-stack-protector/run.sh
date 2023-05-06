#!/bin/bash
echo $FLAG > ./flag.txt
unset FLAG
./ynetd -p 1337 ./main
