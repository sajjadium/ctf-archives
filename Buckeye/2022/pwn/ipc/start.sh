#!/bin/bash
setpriv --reuid=server --regid=server --groups server,ctf --inh-caps -setgid,-setuid,-setpcap --bounding-set -setgid,-setuid,-setpcap --no-new-privs ./server &
sleep 0.5 # if flag_client starts too fast it's msgget will fail and will immediately crash
setpriv --reuid=flag --regid=flag --groups flag,ctf --inh-caps -setgid,-setuid,-setpcap --bounding-set -setgid,-setuid,-setpcap --no-new-privs ./flag_client &

# This is the user's shell
setpriv --reuid=n00b --regid=n00b --groups n00b,ctf --inh-caps -setgid,-setuid,-setpcap --bounding-set -setgid,-setuid,-setpcap --no-new-privs /bin/bash -i

