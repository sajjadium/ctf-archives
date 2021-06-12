#!/usr/bin/env sh

# Output to tmpfs to enforce file size limit, then move to /opt/transfer so the
# parent can retrieve it
/usr/bin/gcc -o "/tmp/$1" "/opt/transfer/$1.c" && \
mv "/tmp/$1" /opt/transfer
