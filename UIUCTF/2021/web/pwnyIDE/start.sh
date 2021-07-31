#! /bin/bash

# simulate a slow ftp server, like in the olden days
tcpslow -l 8021 -f 21 -d 500 &
node index.js
