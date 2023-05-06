#!/usr/bin/env sh
mv flag.txt /flag_`head -c 16 /dev/urandom | xxd -p | tr -d ' ' | tr -d '\n'`.txt
chown root:ctf /flag_*.txt
chmod 440 /flag_*.txt
nginx
su ctf -c /home/ctf/launch_servers.sh
