#!/usr/bin/env sh

echo "ctf:$PASSWORD" | chpasswd && \
exec dropbear -R -F -E -w -p 9999
