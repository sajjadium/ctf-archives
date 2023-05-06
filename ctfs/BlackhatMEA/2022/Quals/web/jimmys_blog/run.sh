#!/bin/bash

# Replace the flag with the live one
bash -c "sed -i 's/placeholder_for_flag/`echo $FLAG`/g' /etc/nginx/sites-available/default"

# Run the challenge
nginx && su ctf && node ./index.js
