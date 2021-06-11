#!/bin/bash

# wait for mysql
until nc -v -w30 127.0.0.1 3306;
do
    echo "MySQL is unavailable - waiting for it... 😴"
    sleep 2;
done

# run in background tmux
tmux new-session -d -s tf2-console -d 'tf2/srcds_run -game tf -console -insecure +sv_pure 1 +map ctf_hellfire +maxplayers 6 +sv_password "${SRCDS_PW}"'

# dump last 100 lines from tmux console
while true; do
  tmux capture-pane -pS -100 -t tf2-console
  sleep 1;
done

## attach to tmux console:
# tmux attach -t tf2-console
