#!/bin/bash
# socat passes the player's TCP socket as stdin/stdout.
# The client uses dup(stdin) for AFC, redirects stdout to /dev/null internally.
exec timeout 60 /challenge/client
